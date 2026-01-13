"""
Context Analysis Module

Analyzes the current working context to determine activity, file types,
and project characteristics. Implements 40% weight of the recommendation algorithm.
"""

import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set, Any, Optional


@dataclass
class ContextAnalysis:
    """Represents the current context analysis."""
    current_activity: str  # coding, debugging, reviewing, planning, exploring
    file_types: Set[str]  # {'.py', '.js', '.v', '.md'}
    recent_changes: Dict[str, List[str]]  # {modified: [...], added: [...], deleted: [...]}
    project_type: str  # web, python, formal_verification, quantum, polyglot, unknown
    session_metadata: Dict[str, Any] = field(default_factory=dict)
    token_budget_remaining: int = 150000  # Default budget


class ContextAnalyzer:
    """Analyzes current working context."""

    def __init__(self, working_dir: Optional[str] = None):
        """
        Initialize context analyzer.

        Args:
            working_dir: Working directory to analyze. Defaults to current directory.
        """
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()

    def analyze(self) -> ContextAnalysis:
        """
        Perform full context analysis.

        Returns:
            ContextAnalysis object with all context information.
        """
        git_status = self._get_git_status()
        file_types = self._analyze_file_types(git_status)
        project_type = self._identify_project_type(file_types)
        activity = self._detect_current_activity(git_status)
        token_budget = self._estimate_token_budget()

        return ContextAnalysis(
            current_activity=activity,
            file_types=file_types,
            recent_changes=git_status,
            project_type=project_type,
            session_metadata={},
            token_budget_remaining=token_budget
        )

    def _get_git_status(self) -> Dict[str, List[str]]:
        """
        Get git status of working directory.

        Returns:
            Dict with keys: modified, added, deleted, untracked
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode != 0:
                return {"modified": [], "added": [], "deleted": [], "untracked": []}

            # Parse git status output
            modified, added, deleted, untracked = [], [], [], []

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                status = line[:2]
                filepath = line[3:] if len(line) > 3 else ""

                if status[0] == 'M' or status[1] == 'M':
                    modified.append(filepath)
                elif status[0] == 'A':
                    added.append(filepath)
                elif status[0] == 'D' or status[1] == 'D':
                    deleted.append(filepath)
                elif status[0] == '?':
                    untracked.append(filepath)

            return {
                "modified": modified,
                "added": added,
                "deleted": deleted,
                "untracked": untracked
            }
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return {"modified": [], "added": [], "deleted": [], "untracked": []}

    def _analyze_file_types(self, git_status: Dict[str, List[str]]) -> Set[str]:
        """
        Extract file extensions from git status.

        Args:
            git_status: Git status dict from _get_git_status

        Returns:
            Set of file extensions (e.g., {'.py', '.js', '.md'})
        """
        file_types = set()

        for file_list in git_status.values():
            for filepath in file_list:
                ext = Path(filepath).suffix
                if ext:  # Only add if extension exists
                    file_types.add(ext.lower())

        return file_types

    def _identify_project_type(self, file_types: Set[str]) -> str:
        """
        Identify project type based on file extensions and markers.

        Args:
            file_types: Set of file extensions

        Returns:
            Project type string
        """
        # Check for specific file types
        if '.v' in file_types:
            return "formal_verification"

        if '.qasm' in file_types or '.qpy' in file_types:
            return "quantum"

        # Check for project markers
        if (self.working_dir / "package.json").exists():
            if '.js' in file_types or '.ts' in file_types or '.tsx' in file_types or '.jsx' in file_types:
                return "web"

        if (self.working_dir / "requirements.txt").exists() or (self.working_dir / "pyproject.toml").exists():
            if '.py' in file_types:
                return "python"

        if (self.working_dir / "Cargo.toml").exists():
            return "rust"

        if (self.working_dir / "go.mod").exists():
            return "go"

        # Fallback based on file types
        if '.py' in file_types:
            return "python"
        elif '.js' in file_types or '.ts' in file_types:
            return "javascript"
        elif '.java' in file_types:
            return "java"
        elif '.rs' in file_types:
            return "rust"
        elif '.go' in file_types:
            return "go"
        elif len(file_types) > 2:
            return "polyglot"
        else:
            return "unknown"

    def _detect_current_activity(self, git_status: Dict[str, List[str]]) -> str:
        """
        Detect current activity based on git status.

        Args:
            git_status: Git status dict

        Returns:
            Activity string: coding, refactoring, testing, debugging, planning, exploring
        """
        modified = git_status.get("modified", [])
        added = git_status.get("added", [])
        deleted = git_status.get("deleted", [])

        # Check for test files
        test_patterns = ['test', 'spec', '__test__', '.test.', '.spec.']
        has_test_files = any(
            any(pattern in f.lower() for pattern in test_patterns)
            for f in modified + added
        )

        if has_test_files:
            return "testing"

        # Check for large-scale changes (refactoring)
        total_changes = len(modified) + len(added) + len(deleted)
        if total_changes > 5:
            return "refactoring"

        # Check for modifications without additions/deletions (likely coding)
        if modified and not added and not deleted:
            return "coding"

        # Check for additions (new feature development)
        if added:
            return "coding"

        # Check for deletions (cleanup/refactoring)
        if deleted:
            return "refactoring"

        # No changes detected
        return "exploring"

    def _estimate_token_budget(self) -> int:
        """
        Estimate remaining token budget.

        Returns:
            Estimated token budget (default 150000 if not available)
        """
        # Try to read from environment variable if set
        budget_str = os.environ.get("CLAUDE_TOKEN_BUDGET", "150000")

        try:
            return int(budget_str)
        except ValueError:
            return 150000

    def detect_current_work(self) -> str:
        """
        Convenience method to detect current activity.

        Returns:
            Activity string
        """
        git_status = self._get_git_status()
        return self._detect_current_activity(git_status)

    def analyze_file_types_from_status(self, git_status_output: str) -> Set[str]:
        """
        Parse file types from raw git status output.

        Args:
            git_status_output: Raw git status --porcelain output

        Returns:
            Set of file extensions
        """
        file_types = set()

        for line in git_status_output.strip().split('\n'):
            if not line or len(line) < 3:
                continue

            filepath = line[3:]
            ext = Path(filepath).suffix
            if ext:
                file_types.add(ext.lower())

        return file_types
