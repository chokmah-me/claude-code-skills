#!/usr/bin/env python3
"""
Skill consistency checker for Claude Code skills repository.
Validates naming conventions, directory structure, and manifest alignment.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

from common_utils import (
    find_all_skills,
    find_skills_directory,
    load_json,
    log_error,
    log_info,
    log_success,
    log_warning,
    exit_failure,
    exit_success,
    get_repo_root,
)


def is_kebab_case(name: str) -> bool:
    """Check if name is in kebab-case."""
    if not name:
        return False
    # Allow lowercase letters, numbers, and hyphens only
    return all(c.islower() or c.isdigit() or c == "-" for c in name)


def check_directory_naming(skills_dir: Path) -> List[Dict[str, str]]:
    """
    Check that skill directories follow naming conventions.

    Returns:
        List of issues found
    """
    issues = []
    skill_dirs = [d for d in skills_dir.glob("**/*") if d.is_dir() and (d / "SKILL.md").exists()]

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name

        # Check kebab-case for leaf directory
        if not is_kebab_case(skill_name):
            issues.append({
                "type": "naming",
                "path": str(skill_dir),
                "message": f"Skill directory '{skill_name}' should be in kebab-case",
            })

    return issues


def check_file_names(skills_dir: Path) -> List[Dict[str, str]]:
    """
    Check that required files have correct names (uppercase SKILL.md).

    Returns:
        List of issues found
    """
    issues = []

    for skill_file in skills_dir.glob("**/SKILL.md"):
        # All SKILL.md files should exist - just verify they're uppercase
        if skill_file.name != "SKILL.md":
            issues.append({
                "type": "filename",
                "path": str(skill_file),
                "message": "Skill manifest must be named 'SKILL.md' (uppercase)",
            })

    # Check for incorrect skill.md (lowercase)
    for skill_file in skills_dir.glob("**/skill.md"):
        issues.append({
            "type": "filename",
            "path": str(skill_file),
            "message": "Found 'skill.md' (lowercase) - should be 'SKILL.md' (uppercase)",
        })

    return issues


def check_category_structure(skills_dir: Path) -> List[Dict[str, str]]:
    """
    Check that skills are organized under valid categories.

    Returns:
        List of issues found
    """
    issues = []
    valid_categories = ["analysis", "generation", "integration", "utility"]

    # Get top-level directories
    top_level = [d for d in skills_dir.iterdir() if d.is_dir()]

    for category_dir in top_level:
        category_name = category_dir.name

        # Check if category is valid
        if category_name not in valid_categories:
            log_warning(f"Category '{category_name}' is not in standard list: {valid_categories}")

    return issues


def verify_manifest_entries(skills_dir: Path) -> List[Dict[str, str]]:
    """
    Verify that all skills are represented in the manifest.

    Returns:
        List of issues found
    """
    issues = []
    repo_root = get_repo_root()

    # Try to load manifest
    manifest_path = repo_root / "UNIFIED_SKILL_MANIFEST.md"
    if not manifest_path.exists():
        log_warning(f"Manifest not found at {manifest_path}")
        return issues

    try:
        manifest_content = manifest_path.read_text()
    except Exception as e:
        issues.append({
            "type": "manifest",
            "path": str(manifest_path),
            "message": f"Could not read manifest: {e}",
        })
        return issues

    # Get all skill names from directories
    skill_dirs = [d for d in skills_dir.glob("**/SKILL.md")]
    skill_names = [d.parent.name for d in skill_dirs]

    # Check that each skill is mentioned in manifest
    for skill_name in skill_names:
        if skill_name not in manifest_content:
            issues.append({
                "type": "manifest",
                "path": f"skills/*/{skill_name}",
                "message": f"Skill '{skill_name}' not found in manifest",
            })

    return issues


def run_all_checks() -> Dict[str, Any]:
    """
    Run all consistency checks.

    Returns:
        Dictionary with results
    """
    skills_dir = find_skills_directory()

    results = {
        "total_issues": 0,
        "checks": {
            "naming": [],
            "filename": [],
            "category": [],
            "manifest": [],
        },
        "summary": "",
    }

    log_info("Running consistency checks...")

    # Run all checks
    naming_issues = check_directory_naming(skills_dir)
    results["checks"]["naming"] = naming_issues
    results["total_issues"] += len(naming_issues)

    filename_issues = check_file_names(skills_dir)
    results["checks"]["filename"] = filename_issues
    results["total_issues"] += len(filename_issues)

    category_issues = check_category_structure(skills_dir)
    results["checks"]["category"] = category_issues
    results["total_issues"] += len(category_issues)

    manifest_issues = verify_manifest_entries(skills_dir)
    results["checks"]["manifest"] = manifest_issues
    results["total_issues"] += len(manifest_issues)

    # Log results
    for check_type, issues in results["checks"].items():
        for issue in issues:
            log_error(f"{check_type}: {issue['message']}")

    results["summary"] = f"Found {results['total_issues']} consistency issues"
    return results


def main() -> None:
    """Run consistency checks."""
    results = run_all_checks()

    log_info(results["summary"])

    if results["total_issues"] > 0:
        exit_failure(f"Consistency checks failed: {results['total_issues']} issues found")
    else:
        exit_success("All consistency checks passed")


if __name__ == "__main__":
    main()
