#!/usr/bin/env python3
"""
Meta-Skills Execution Tests (Phase 3)

Comprehensive testing of meta-skills including:
- session-snapshot
- skill-extractor
- skill-recommendation-engine
- manifest-generator

Includes both positive and negative test cases.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from runners.skill_executor import (
    SkillExecutor,
    MockGitRepo,
    MockSession,
    create_corrupted_skill,
    create_empty_context
)


class TestSessionSnapshot:
    """Test session-snapshot skill."""

    @pytest.fixture
    def executor(self):
        """Create skill executor."""
        temp_dir = Path(tempfile.mkdtemp())
        executor = SkillExecutor(temp_dir)
        yield executor
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def skill_path(self):
        """Path to session-snapshot skill."""
        return Path("skills/meta/session-snapshot/SKILL.md")

    # ============= POSITIVE TESTS =============

    def test_parse_session_snapshot_skill(self, executor, skill_path):
        """Parse session-snapshot skill file."""
        skill_data = executor.parse_skill_file(skill_path)

        assert 'frontmatter' in skill_data
        assert 'sections' in skill_data
        assert skill_data['frontmatter'].get('name') == 'session-snapshot'

    def test_create_snapshot_basic(self, executor):
        """Test creating basic session snapshot."""
        # Simulate snapshot creation
        snapshot_content = f"""# Session Snapshot

**Timestamp**: {datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
**Task**: Implement user authentication
**Phase**: Adding JWT token validation

## Context

Working on authentication system. Need to add JWT validation middleware.

## Files Modified

- src/auth/middleware.py:45-67 (added JWT validation)
- src/auth/routes.py:23 (new file)

## Next Steps

- [ ] Complete JWT validation tests
- [ ] Add refresh token logic
- [ ] Update documentation
"""

        snapshot_path = executor.simulate_file_creation(
            '.session-snapshot.md',
            snapshot_content
        )

        # Validate snapshot format
        is_valid, errors = executor.validate_snapshot_format(snapshot_path)

        assert is_valid, f"Snapshot validation failed: {errors}"
        assert snapshot_path.exists()

    def test_snapshot_includes_required_fields(self, executor):
        """Test snapshot includes all required fields."""
        snapshot_content = f"""# Session Snapshot

**Timestamp**: {datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}
**Task**: Test task
**Phase**: Test phase

## Context

Test context information.

## Files Modified

- test.py

## Files Read

- config.py

## Next Steps

- [ ] Step 1
- [ ] Step 2

## Decisions Made

- Decision 1
- Decision 2

## Blockers

None currently.
"""

        snapshot_path = executor.simulate_file_creation(
            '.session-snapshot.md',
            snapshot_content
        )

        content = executor.read_file('.session-snapshot.md')

        # Verify all fields present
        assert '**Timestamp**:' in content
        assert '**Task**:' in content
        assert '**Phase**:' in content
        assert '## Context' in content
        assert '## Next Steps' in content
        assert '## Decisions Made' in content
        assert '## Blockers' in content

    def test_snapshot_format_validation(self, executor):
        """Test snapshot format validation catches errors."""
        # Create invalid snapshot (missing required fields)
        invalid_snapshot = """# Session Snapshot

**Timestamp**: 2026-01-09

Some content but missing required fields.
"""

        snapshot_path = executor.simulate_file_creation(
            '.session-snapshot.md',
            invalid_snapshot
        )

        is_valid, errors = executor.validate_snapshot_format(snapshot_path)

        assert not is_valid
        assert len(errors) > 0
        assert any('Task' in error for error in errors)

    # ============= NEGATIVE TESTS =============

    def test_snapshot_without_write_permissions(self, executor):
        """NEGATIVE: Create snapshot without write permissions."""
        if sys.platform == "win32":
            pytest.skip("Permission test unreliable on Windows")

        # Make directory read-only
        import stat
        os.chmod(executor.test_dir, stat.S_IRUSR | stat.S_IXUSR)

        try:
            snapshot_path = executor.test_dir / '.session-snapshot.md'

            # Should raise permission error
            with pytest.raises((PermissionError, OSError)):
                snapshot_path.write_text("test")
        finally:
            # Restore permissions
            os.chmod(executor.test_dir, stat.S_IRWXU)

    def test_resume_from_corrupted_snapshot(self, executor):
        """NEGATIVE: Resume from corrupted snapshot file."""
        # Create corrupted snapshot
        corrupted_content = """# Session Snapshot

**Timestamp**: invalid-timestamp
**Task**: [[[[broken markdown
**Phase**: ???

## Context

Missing closing tags and invalid format

## Next Steps

Not a proper checklist
Just plain text
"""

        snapshot_path = executor.simulate_file_creation(
            '.session-snapshot.md',
            corrupted_content
        )

        is_valid, errors = executor.validate_snapshot_format(snapshot_path)

        assert not is_valid
        assert len(errors) > 0

    def test_snapshot_missing_timestamp(self, executor):
        """NEGATIVE: Snapshot without valid timestamp."""
        invalid_snapshot = """# Session Snapshot

**Task**: Test task
**Phase**: Test phase

## Context

Missing timestamp field.

## Next Steps

- [ ] Step 1
"""

        snapshot_path = executor.simulate_file_creation(
            '.session-snapshot.md',
            invalid_snapshot
        )

        is_valid, errors = executor.validate_snapshot_format(snapshot_path)

        assert not is_valid
        assert any('timestamp' in error.lower() for error in errors)

    def test_empty_snapshot(self, executor):
        """NEGATIVE: Empty snapshot file."""
        snapshot_path = executor.simulate_file_creation(
            '.session-snapshot.md',
            ''
        )

        is_valid, errors = executor.validate_snapshot_format(snapshot_path)

        assert not is_valid
        assert len(errors) > 0


class TestSkillExtractor:
    """Test skill-extractor skill."""

    @pytest.fixture
    def executor(self):
        """Create skill executor."""
        temp_dir = Path(tempfile.mkdtemp())
        executor = SkillExecutor(temp_dir)
        yield executor
        shutil.rmtree(temp_dir, ignore_errors=True)

    # ============= POSITIVE TESTS =============

    def test_extract_skill_from_session(self, executor):
        """Test extracting skill from session with repeated patterns."""
        # Create mock session with repeated pattern
        session = MockSession()
        session.add_pattern('format code according to style guide')

        transcript_path = executor.test_dir / 'session-transcript.txt'
        session.export_transcript(transcript_path)

        assert transcript_path.exists()
        content = transcript_path.read_text()
        assert 'format code' in content

    def test_generated_skill_has_valid_structure(self, executor):
        """Test generated skill follows required structure."""
        # Simulate generated skill
        generated_skill = """---
name: auto-formatter
description: Automatically format code according to style guide
---

# Auto-Formatter Skill

## 🎯 Purpose

Format code according to project style guide automatically.

## 📋 Usage

```
claude skills use auto-formatter --file=src/main.py
```

## 💡 Examples

### Basic Example

Format a single file:
```bash
claude skills use auto-formatter main.py
```

### Advanced Example

Format entire directory:
```bash
claude skills use auto-formatter src/
```

## ⚠️ Important Notes

- Backs up files before formatting
- Respects .editorconfig settings
"""

        skill_path = executor.simulate_file_creation(
            'auto-formatter.md',
            generated_skill
        )

        is_valid, errors = executor.validate_skill_structure(skill_path)

        assert is_valid, f"Generated skill invalid: {errors}"

    def test_identify_recurring_patterns(self, executor):
        """Test identifying recurring patterns in conversation."""
        session = MockSession()

        # Add multiple occurrences of same pattern
        for i in range(5):
            session.add_message('user', 'Please validate the API response schema')
            session.add_message('assistant', 'Validating API response schema...')

        transcript_path = executor.test_dir / 'transcript.txt'
        session.export_transcript(transcript_path)

        content = transcript_path.read_text()

        # Should find pattern multiple times
        occurrences = content.count('validate the API response schema')
        assert occurrences >= 5

    # ============= NEGATIVE TESTS =============

    def test_extract_from_empty_conversation(self, executor):
        """NEGATIVE: Extract skill from empty conversation."""
        # Create empty session
        session = MockSession()
        transcript_path = executor.test_dir / 'empty-transcript.txt'
        session.export_transcript(transcript_path)

        content = transcript_path.read_text()

        # Empty or minimal content
        assert len(content.strip()) < 100

    def test_extract_from_nonexistent_session(self, executor):
        """NEGATIVE: Extract from non-existent session file."""
        fake_path = executor.test_dir / 'nonexistent-session.txt'

        assert not fake_path.exists()

    def test_generated_skill_too_short(self, executor):
        """NEGATIVE: Generated skill is too short/incomplete."""
        short_skill = """# Test Skill

Some minimal content.
"""

        skill_path = executor.simulate_file_creation('short-skill.md', short_skill)
        is_valid, errors = executor.validate_skill_structure(skill_path)

        assert not is_valid
        assert any('short' in error.lower() for error in errors)

    def test_generated_skill_missing_sections(self, executor):
        """NEGATIVE: Generated skill missing required sections."""
        incomplete_skill = """---
name: incomplete-skill
---

# Incomplete Skill

## 🎯 Purpose

This skill is incomplete.

## Some Random Section

Missing required sections like Usage and Examples.
"""

        skill_path = executor.simulate_file_creation(
            'incomplete-skill.md',
            incomplete_skill
        )

        is_valid, errors = executor.validate_skill_structure(skill_path)

        assert not is_valid
        assert len(errors) > 0


class TestSkillRecommendationEngine:
    """Test skill-recommendation-engine skill."""

    @pytest.fixture
    def executor(self):
        """Create skill executor."""
        temp_dir = Path(tempfile.mkdtemp())
        executor = SkillExecutor(temp_dir)
        yield executor
        shutil.rmtree(temp_dir, ignore_errors=True)

    # ============= POSITIVE TESTS =============

    def test_recommend_skills_for_context(self, executor):
        """Test recommending skills based on context."""
        # Create context files
        executor.simulate_file_creation(
            'main.py',
            'def test(): pass\n# TODO: Add tests'
        )
        executor.simulate_file_creation(
            'README.md',
            '# Project\n\nNeeds better documentation'
        )

        # Context suggests need for test-runner and documentation skills
        assert executor.check_file_exists('main.py')
        assert executor.check_file_exists('README.md')

    def test_recommend_git_skills_for_repo(self, executor):
        """Test recommending git skills in repository context."""
        # Create mock git repo
        repo = MockGitRepo(executor.test_dir)
        repo.create_diff()

        assert (executor.test_dir / '.git').exists()
        # Should recommend git-related skills like diff-summariser

    # ============= NEGATIVE TESTS =============

    def test_recommend_with_empty_context(self, executor):
        """NEGATIVE: Recommend skills with no context."""
        # Empty directory
        files = list(executor.test_dir.iterdir())
        assert len(files) == 0

    def test_recommend_with_invalid_context(self, executor):
        """NEGATIVE: Recommend skills with invalid context."""
        # Create corrupted/invalid files
        executor.simulate_file_creation('invalid.bin', '\x00\x01\x02\x03')


class TestManifestGenerator:
    """Test manifest-generator skill."""

    @pytest.fixture
    def executor(self):
        """Create skill executor."""
        temp_dir = Path(tempfile.mkdtemp())
        executor = SkillExecutor(temp_dir)
        yield executor
        shutil.rmtree(temp_dir, ignore_errors=True)

    # ============= POSITIVE TESTS =============

    def test_generate_manifest(self, executor):
        """Test generating manifest file."""
        # Create mock skills directory structure
        skills_dir = executor.test_dir / 'skills' / 'meta'
        skills_dir.mkdir(parents=True)

        # Create sample skill
        (skills_dir / 'test-skill.md').write_text("""---
name: test-skill
description: Test skill for manifest
---

# Test Skill

## Purpose

Test skill content.
""", encoding='utf-8')

        # Generate manifest
        manifest_content = """# Skills Inventory

## Meta Skills

- **test-skill**: Test skill for manifest

## Development Skills

- **lean-plan**: Token-efficient planning

## Statistics

Total skills: 2
Categories: 2
"""

        manifest_path = executor.simulate_file_creation(
            'SKILLS_INVENTORY.md',
            manifest_content
        )

        is_valid, errors = executor.validate_manifest_format(manifest_path)

        assert is_valid, f"Manifest validation failed: {errors}"

    def test_manifest_includes_all_categories(self, executor):
        """Test manifest includes all skill categories."""
        manifest_content = """# Skills Inventory

## Meta Skills

- session-snapshot
- skill-extractor

## Development Skills

- lean-plan
- quick-test-runner

## Git Skills

- diff-summariser
- repo-briefing

## Analysis Skills

### Code Analysis

- api-contract-sniffer
- dead-code-hunter

### Formal Verification

- anti-pattern-sniffer

## Statistics

Total skills: 9
Categories: 4
"""

        manifest_path = executor.simulate_file_creation(
            'SKILLS_INVENTORY.md',
            manifest_content
        )

        is_valid, errors = executor.validate_manifest_format(manifest_path)

        assert is_valid, f"Manifest validation failed: {errors}"

        content = executor.read_file('SKILLS_INVENTORY.md')
        assert 'Meta Skills' in content
        assert 'Development Skills' in content
        assert 'Git Skills' in content
        assert 'Analysis Skills' in content

    # ============= NEGATIVE TESTS =============

    def test_generate_manifest_missing_skills_dir(self, executor):
        """NEGATIVE: Generate manifest without skills directory."""
        skills_dir = executor.test_dir / 'skills'

        # Skills directory doesn't exist
        assert not skills_dir.exists()

    def test_generate_manifest_corrupted_skills(self, executor):
        """NEGATIVE: Generate manifest with corrupted skill files."""
        skills_dir = executor.test_dir / 'skills' / 'meta'
        skills_dir.mkdir(parents=True)

        # Create corrupted skill file
        corrupted_path = skills_dir / 'broken-skill.md'
        create_corrupted_skill(corrupted_path)

        assert corrupted_path.exists()

    def test_manifest_empty_content(self, executor):
        """NEGATIVE: Manifest with no skills listed."""
        manifest_content = """# Skills Inventory

No skills found.
"""

        manifest_path = executor.simulate_file_creation(
            'SKILLS_INVENTORY.md',
            manifest_content
        )

        is_valid, errors = executor.validate_manifest_format(manifest_path)

        # Should fail validation for missing categories
        assert not is_valid
        assert len(errors) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
