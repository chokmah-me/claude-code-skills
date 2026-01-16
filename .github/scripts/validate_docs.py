#!/usr/bin/env python3
"""
Documentation validation script for Claude Code skills.
Validates that skill documentation meets required standards.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

from common_utils import (
    find_all_skills,
    load_json,
    log_error,
    log_info,
    log_success,
    log_warning,
    save_json,
    exit_failure,
    exit_success,
)


REQUIRED_SECTIONS = [
    "# ",  # Header
    "## Description",
    "## Triggers",
    "## Usage",
    "## Parameters",
    "## Output",
]


def validate_skill_md(skill_path: Path) -> Dict[str, Any]:
    """
    Validate a single skill markdown file.

    Args:
        skill_path: Path to SKILL.md file

    Returns:
        Validation result dictionary
    """
    result = {
        "file": str(skill_path),
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    if not skill_path.exists():
        result["valid"] = False
        result["errors"].append("File does not exist")
        return result

    try:
        content = skill_path.read_text(encoding="utf-8")
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Could not read file: {e}")
        return result

    if not content.strip():
        result["valid"] = False
        result["errors"].append("File is empty")
        return result

    # Check for required sections
    missing_sections = []
    for section in REQUIRED_SECTIONS:
        if section not in content:
            missing_sections.append(section)

    if missing_sections:
        result["valid"] = False
        for section in missing_sections:
            result["errors"].append(f"Missing section: {section}")

    # Basic markdown validation
    lines = content.split("\n")
    if not any(line.startswith("# ") for line in lines):
        result["valid"] = False
        result["errors"].append("No main heading (# ) found")

    # Check for code block examples
    if "```" not in content:
        result["warnings"].append("No code examples found in documentation")

    return result


def validate_all_skills() -> Dict[str, Any]:
    """
    Validate all skills in the repository.

    Returns:
        Summary of validation results
    """
    skills = find_all_skills()
    results = {
        "total": len(skills),
        "valid": 0,
        "invalid": 0,
        "skills": [],
        "summary": "",
    }

    if not skills:
        log_warning("No skills found to validate")
        return results

    log_info(f"Validating {len(skills)} skills...")

    for skill_path in skills:
        result = validate_skill_md(skill_path)
        results["skills"].append(result)

        if result["valid"]:
            results["valid"] += 1
            log_success(f"Valid: {skill_path.parent.name}")
        else:
            results["invalid"] += 1
            log_error(f"Invalid: {skill_path.parent.name}")
            for error in result["errors"]:
                log_error(f"  - {error}")

    results["summary"] = f"Valid: {results['valid']}/{results['total']}, Invalid: {results['invalid']}/{results['total']}"
    return results


def main() -> None:
    """Run documentation validation."""
    results = validate_all_skills()

    # Save validation report
    report_path = Path("validation-report.json")
    save_json(results, report_path)

    log_info(results["summary"])

    if results["invalid"] > 0:
        exit_failure(f"Documentation validation failed: {results['invalid']} skills have issues")
    else:
        exit_success("All skills passed documentation validation")


if __name__ == "__main__":
    main()
