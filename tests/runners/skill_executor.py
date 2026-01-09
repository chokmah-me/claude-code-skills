#!/usr/bin/env python3
"""
Skill Execution Framework

Simulates Claude Code environment to execute and test skills.
Provides utilities for parsing skill instructions and validating outputs.
"""

import os
import re
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SkillOutput:
    """Result of skill execution."""
    success: bool
    files_created: List[Path]
    files_modified: List[Path]
    output: str
    errors: List[str]
    warnings: List[str]


class SkillExecutor:
    """Execute skills in controlled test environment."""

    def __init__(self, test_dir: Optional[Path] = None):
        self.test_dir = test_dir or Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()

    def __enter__(self):
        """Context manager entry."""
        os.chdir(self.test_dir)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        os.chdir(self.original_cwd)

    def parse_skill_file(self, skill_path: Path) -> Dict:
        """Parse skill file to extract instructions and parameters."""
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        frontmatter = {}
        frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if frontmatter_match:
            for line in frontmatter_match.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()

        # Extract sections
        sections = {}
        section_pattern = r'^## (.+)$\n(.*?)(?=^## |^# |\Z)'
        for match in re.finditer(section_pattern, content, re.MULTILINE | re.DOTALL):
            section_title = match.group(1).strip()
            section_content = match.group(2).strip()
            sections[section_title] = section_content

        return {
            'frontmatter': frontmatter,
            'sections': sections,
            'full_content': content
        }

    def extract_instructions(self, skill_data: Dict) -> List[str]:
        """Extract executable instructions from skill."""
        instructions = []

        # Look for instructions section
        for key in skill_data['sections']:
            if 'instruction' in key.lower():
                instruction_text = skill_data['sections'][key]
                # Extract numbered steps
                steps = re.findall(r'^\d+\.\s+(.+?)$', instruction_text, re.MULTILINE)
                instructions.extend(steps)

        return instructions

    def extract_code_blocks(self, text: str) -> List[Tuple[str, str]]:
        """Extract code blocks with language tags."""
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return [(lang or 'text', code.strip()) for lang, code in matches]

    def simulate_file_creation(self, filename: str, content: str) -> Path:
        """Simulate file creation in test environment."""
        file_path = self.test_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        return file_path

    def check_file_exists(self, filename: str) -> bool:
        """Check if file exists in test environment."""
        return (self.test_dir / filename).exists()

    def read_file(self, filename: str) -> str:
        """Read file from test environment."""
        return (self.test_dir / filename).read_text(encoding='utf-8')

    def validate_snapshot_format(self, snapshot_path: Path) -> Tuple[bool, List[str]]:
        """Validate session snapshot file format."""
        if not snapshot_path.exists():
            return False, ["Snapshot file not created"]

        errors = []
        content = snapshot_path.read_text(encoding='utf-8')

        # Required fields for session snapshot
        required_fields = [
            r'\*\*Timestamp\*\*:',
            r'\*\*Task\*\*:',
            r'\*\*Phase\*\*:',
            r'## Context',
            r'## Next Steps'
        ]

        for field_pattern in required_fields:
            if not re.search(field_pattern, content):
                errors.append(f"Missing required field: {field_pattern}")

        # Check for valid timestamp format
        timestamp_match = re.search(r'\*\*Timestamp\*\*:\s*(\d{4}-\d{2}-\d{2})', content)
        if not timestamp_match:
            errors.append("Invalid or missing timestamp format")

        return len(errors) == 0, errors

    def validate_skill_structure(self, skill_path: Path) -> Tuple[bool, List[str]]:
        """Validate generated skill file structure."""
        if not skill_path.exists():
            return False, ["Skill file not created"]

        errors = []
        content = skill_path.read_text(encoding='utf-8')

        # Required sections for skill files
        required_sections = [
            '# ',
            '## 🎯 Purpose',
            '## 📋 Usage',
            '## 💡 Examples'
        ]

        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")

        # Check minimum length
        if len(content) < 500:
            errors.append(f"Skill content too short: {len(content)} characters")

        return len(errors) == 0, errors

    def validate_manifest_format(self, manifest_path: Path) -> Tuple[bool, List[str]]:
        """Validate manifest file format."""
        if not manifest_path.exists():
            return False, ["Manifest file not created"]

        errors = []
        content = manifest_path.read_text(encoding='utf-8')

        # Check for skill listings
        if '## Skills' not in content and '# Skills' not in content:
            errors.append("Missing skills section")

        # Check for categories
        categories = ['meta', 'development', 'git', 'analysis']
        found_categories = sum(1 for cat in categories if cat in content.lower())

        if found_categories < 2:
            errors.append(f"Only found {found_categories} categories, expected at least 2")

        return len(errors) == 0, errors


class MockGitRepo:
    """Mock git repository for testing git-related skills."""

    def __init__(self, repo_dir: Path):
        self.repo_dir = repo_dir
        self._setup_repo()

    def _setup_repo(self):
        """Initialize mock git repo structure."""
        self.repo_dir.mkdir(parents=True, exist_ok=True)

        # Create .git directory
        (self.repo_dir / '.git').mkdir(exist_ok=True)

        # Create mock files
        (self.repo_dir / 'README.md').write_text('# Test Repository\n\nTest content.')
        (self.repo_dir / 'main.py').write_text('def hello():\n    print("Hello")')

    def create_diff(self):
        """Simulate uncommitted changes."""
        (self.repo_dir / 'main.py').write_text(
            'def hello():\n    print("Hello, World!")\n\ndef goodbye():\n    print("Goodbye")'
        )


class MockSession:
    """Mock conversation session for testing skill extraction."""

    def __init__(self):
        self.messages = []

    def add_message(self, role: str, content: str):
        """Add message to session."""
        self.messages.append({'role': role, 'content': content})

    def add_pattern(self, pattern: str, occurrences: int = 3):
        """Add recurring pattern to session."""
        for i in range(occurrences):
            self.add_message('user', f'Do {pattern} for item {i}')
            self.add_message('assistant', f'Completed {pattern} for item {i}')

    def export_transcript(self, output_path: Path):
        """Export session as transcript file."""
        transcript = []
        for msg in self.messages:
            transcript.append(f"[{msg['role'].upper()}]")
            transcript.append(msg['content'])
            transcript.append('')

        output_path.write_text('\n'.join(transcript), encoding='utf-8')


def create_corrupted_skill(output_path: Path):
    """Create malformed skill file for negative testing."""
    # Missing required sections, invalid YAML, etc.
    corrupted_content = """---
name: broken-skill
invalid yaml here:::
---

# Broken Skill

This skill is missing required sections and has formatting issues.

## Some Random Section

No structure or proper formatting.
"""
    output_path.write_text(corrupted_content, encoding='utf-8')


def create_empty_context(output_path: Path):
    """Create empty context directory for negative testing."""
    output_path.mkdir(parents=True, exist_ok=True)
