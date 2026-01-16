#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Common utilities for GitHub Actions workflow scripts.
Provides shared functions for JSON handling, file discovery, logging, and exit codes.
"""

import json
import sys
import os
from pathlib import Path
from typing import Any, Dict, List

# Ensure UTF-8 output on all platforms
if sys.stdout.encoding != "utf-8":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    else:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# Color codes for terminal output
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


def log_info(message: str) -> None:
    """Print info message in blue."""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.RESET}")


def log_success(message: str) -> None:
    """Print success message in green."""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def log_warning(message: str) -> None:
    """Print warning message in yellow."""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")


def log_error(message: str) -> None:
    """Print error message in red."""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def get_repo_root() -> Path:
    """
    Get the repository root directory.
    Traverses up from the script location until .git is found.
    """
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise RuntimeError("Could not find repository root (.git directory)")


def load_json(path: str | Path) -> Dict[str, Any]:
    """
    Load JSON file with error handling.

    Args:
        path: Path to JSON file

    Returns:
        Parsed JSON data as dictionary

    Raises:
        SystemExit: If file doesn't exist or JSON is invalid
    """
    path = Path(path)
    if not path.exists():
        log_error(f"File not found: {path}")
        sys.exit(1)

    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in {path}: {e}")
        sys.exit(1)


def save_json(data: Dict[str, Any], path: str | Path, pretty: bool = True) -> None:
    """
    Save data to JSON file.

    Args:
        data: Dictionary to save
        path: Output file path
        pretty: Use pretty formatting (default True)
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(path, "w") as f:
            if pretty:
                json.dump(data, f, indent=2)
            else:
                json.dump(data, f)
        log_success(f"Saved: {path}")
    except Exception as e:
        log_error(f"Failed to save {path}: {e}")
        sys.exit(1)


def find_files(pattern: str, directory: str | Path = ".") -> List[Path]:
    """
    Recursively find files matching glob pattern.

    Args:
        pattern: Glob pattern (e.g., "**/*.md")
        directory: Root directory to search (default current)

    Returns:
        List of matching Path objects
    """
    directory = Path(directory)
    return sorted(directory.glob(pattern))


def find_skills_directory() -> Path:
    """
    Find the skills directory in the repository.

    Returns:
        Path to skills directory

    Raises:
        SystemExit: If skills directory not found
    """
    repo_root = get_repo_root()
    skills_dir = repo_root / "skills"

    if not skills_dir.exists():
        log_error(f"Skills directory not found at {skills_dir}")
        sys.exit(1)

    return skills_dir


def find_all_skills() -> List[Path]:
    """
    Find all skill directories in the repository.

    Returns:
        List of paths to skill SKILL.md files
    """
    skills_dir = find_skills_directory()
    skill_files = list(skills_dir.glob("**/SKILL.md"))

    if not skill_files:
        log_warning("No SKILL.md files found")

    return sorted(skill_files)


def exit_success(message: str = "Success") -> None:
    """Exit with code 0 (success)."""
    log_success(message)
    sys.exit(0)


def exit_warning(message: str = "Warning") -> None:
    """Exit with code 2 (warning)."""
    log_warning(message)
    sys.exit(2)


def exit_failure(message: str = "Failure") -> None:
    """Exit with code 1 (failure)."""
    log_error(message)
    sys.exit(1)


if __name__ == "__main__":
    # Self-test
    log_info("Testing common_utils module")
    repo_root = get_repo_root()
    log_success(f"Found repo root: {repo_root}")

    skills = find_all_skills()
    log_info(f"Found {len(skills)} skills")

    exit_success("common_utils self-test passed")
