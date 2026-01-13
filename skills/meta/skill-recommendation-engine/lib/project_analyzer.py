"""
Project State Analysis Module

Analyzes project health, age, complexity, and other state indicators.
Implements 30% weight of the recommendation algorithm.
"""

import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional


@dataclass
class ProjectState:
    """Represents project state analysis."""
    repository_age_days: int
    has_tests: bool
    test_coverage_estimate: str  # low, medium, high
    dependency_count: int
    has_security_issues: bool
    documentation_quality: str  # poor, adequate, good
    recent_commits_count: int
    complexity_indicators: Dict[str, Any] = field(default_factory=dict)


class ProjectAnalyzer:
    """Analyzes project state and health."""

    def __init__(self, working_dir: Optional[str] = None):
        """
        Initialize project analyzer.

        Args:
            working_dir: Project directory to analyze. Defaults to current directory.
        """
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()

    def analyze(self) -> ProjectState:
        """
        Perform full project state analysis.

        Returns:
            ProjectState object with all analysis results.
        """
        return ProjectState(
            repository_age_days=self._get_repo_age(),
            has_tests=self._check_for_tests(),
            test_coverage_estimate=self._estimate_test_coverage(),
            dependency_count=self._count_dependencies(),
            has_security_issues=self._check_security_indicators(),
            documentation_quality=self._assess_documentation(),
            recent_commits_count=self._analyze_commit_patterns(),
            complexity_indicators=self._analyze_complexity()
        )

    def _get_repo_age(self) -> int:
        """
        Get repository age in days since first commit.

        Returns:
            Number of days since first commit, or 0 if not a git repo.
        """
        try:
            result = subprocess.run(
                ["git", "log", "--reverse", "--format=%ct"],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0 or not result.stdout.strip():
                return 0

            first_commit_ts = int(result.stdout.strip().split('\n')[0])
            current_time = int(time.time())
            age_seconds = current_time - first_commit_ts
            return age_seconds // 86400  # Convert to days

        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError, Exception):
            return 0

    def _check_for_tests(self) -> bool:
        """
        Check if project has test files.

        Returns:
            True if test files are found.
        """
        test_patterns = [
            "**/test/**",
            "**/tests/**",
            "**/*test.py",
            "**/*test.js",
            "**/*.test.ts",
            "**/*.test.tsx",
            "**/*.spec.js",
            "**/*.spec.ts",
            "**/__tests__/**"
        ]

        for pattern in test_patterns:
            if list(self.working_dir.glob(pattern)):
                return True

        return False

    def _estimate_test_coverage(self) -> str:
        """
        Estimate test coverage based on test file to source file ratio.

        Returns:
            "low", "medium", or "high"
        """
        if not self._check_for_tests():
            return "low"

        try:
            # Count test files
            test_count = 0
            test_patterns = ["**/test*.py", "**/*test.py", "**/*test.js", "**/*.test.ts"]
            for pattern in test_patterns:
                test_count += len(list(self.working_dir.glob(pattern)))

            # Count source files (rough estimate)
            source_count = 0
            source_patterns = ["**/*.py", "**/*.js", "**/*.ts"]
            for pattern in source_patterns:
                files = list(self.working_dir.glob(pattern))
                # Exclude test files from source count
                source_count += len([f for f in files if 'test' not in str(f).lower()])

            if source_count == 0:
                return "low"

            coverage_ratio = test_count / source_count

            if coverage_ratio >= 0.6:
                return "high"
            elif coverage_ratio >= 0.2:
                return "medium"
            else:
                return "low"

        except Exception:
            return "low"

    def _count_dependencies(self) -> int:
        """
        Count project dependencies from package files.

        Returns:
            Number of dependencies found.
        """
        dep_count = 0

        # Python dependencies
        requirements_file = self.working_dir / "requirements.txt"
        if requirements_file.exists():
            try:
                content = requirements_file.read_text()
                # Count non-empty, non-comment lines
                dep_count += len([
                    line for line in content.split('\n')
                    if line.strip() and not line.strip().startswith('#')
                ])
            except Exception:
                pass

        # JavaScript/Node dependencies
        package_json = self.working_dir / "package.json"
        if package_json.exists():
            try:
                import json
                data = json.loads(package_json.read_text())
                dep_count += len(data.get('dependencies', {}))
                dep_count += len(data.get('devDependencies', {}))
            except Exception:
                pass

        # Rust dependencies
        cargo_toml = self.working_dir / "Cargo.toml"
        if cargo_toml.exists():
            try:
                content = cargo_toml.read_text()
                # Simple count of lines in [dependencies] section
                in_deps = False
                for line in content.split('\n'):
                    if '[dependencies]' in line:
                        in_deps = True
                    elif line.startswith('[') and in_deps:
                        break
                    elif in_deps and '=' in line:
                        dep_count += 1
            except Exception:
                pass

        return dep_count

    def _check_security_indicators(self) -> bool:
        """
        Check for potential security issues (basic heuristics).

        Returns:
            True if potential security issues detected.
        """
        # Check for old package-lock.json (>6 months)
        package_lock = self.working_dir / "package-lock.json"
        if package_lock.exists():
            try:
                stat = package_lock.stat()
                age_seconds = time.time() - stat.st_mtime
                if age_seconds > (180 * 86400):  # 6 months
                    return True
            except Exception:
                pass

        # Check for requirements.txt without version pins
        requirements_file = self.working_dir / "requirements.txt"
        if requirements_file.exists():
            try:
                content = requirements_file.read_text()
                # Check if most lines lack version specifiers
                lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
                unpinned = len([l for l in lines if '==' not in l and '>=' not in l])
                if unpinned > len(lines) / 2:
                    return True
            except Exception:
                pass

        return False

    def _assess_documentation(self) -> str:
        """
        Assess documentation quality.

        Returns:
            "poor", "adequate", or "good"
        """
        readme = self.working_dir / "README.md"
        docs_dir = self.working_dir / "docs"

        if not readme.exists():
            return "poor"

        try:
            readme_content = readme.read_text()
            readme_length = len(readme_content)

            has_docs_dir = docs_dir.exists() and docs_dir.is_dir()

            if readme_length > 3000 or has_docs_dir:
                return "good"
            elif readme_length > 1000:
                return "adequate"
            else:
                return "poor"

        except Exception:
            return "poor"

    def _analyze_commit_patterns(self) -> int:
        """
        Analyze recent commit activity.

        Returns:
            Number of commits in the last 30 days.
        """
        try:
            result = subprocess.run(
                ["git", "log", "--since=30 days ago", "--oneline"],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                return 0

            return len([line for line in result.stdout.strip().split('\n') if line])

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return 0

    def _analyze_complexity(self) -> Dict[str, Any]:
        """
        Analyze project complexity indicators.

        Returns:
            Dict with complexity metrics.
        """
        indicators = {
            "total_lines": 0,
            "large_files": 0,
            "max_file_size": 0,
            "avg_file_size": 0
        }

        try:
            # Find all source files
            source_patterns = ["**/*.py", "**/*.js", "**/*.ts", "**/*.java", "**/*.go", "**/*.rs"]
            all_files = []
            for pattern in source_patterns:
                all_files.extend(self.working_dir.glob(pattern))

            if not all_files:
                return indicators

            file_sizes = []
            for filepath in all_files[:100]:  # Limit to first 100 files for performance
                try:
                    lines = len(filepath.read_text().split('\n'))
                    file_sizes.append(lines)

                    if lines > 500:
                        indicators["large_files"] += 1

                except Exception:
                    continue

            if file_sizes:
                indicators["total_lines"] = sum(file_sizes)
                indicators["max_file_size"] = max(file_sizes)
                indicators["avg_file_size"] = sum(file_sizes) // len(file_sizes)

        except Exception:
            pass

        return indicators
