#!/usr/bin/env python3
"""
Skill testing script for Claude Code skills repository.
Tests skill documentation, code blocks, and manifest alignment.
"""

from pathlib import Path
from typing import Any, Dict, List

from common_utils import (
    find_all_skills,
    log_error,
    log_info,
    log_success,
    log_warning,
    save_json,
    exit_failure,
    exit_success,
)


class MarkdownDoc:
    """Simple markdown parser for skill documentation."""

    def __init__(self, content: str):
        self.content = content
        self.lines = content.split("\n")

    def has_section(self, section_name: str) -> bool:
        """Check if document has a section heading."""
        return any(line.strip().startswith(f"## {section_name}") for line in self.lines)

    def extract_section(self, section_name: str) -> str:
        """Extract content of a section."""
        in_section = False
        section_content = []

        for line in self.lines:
            if line.strip().startswith(f"## {section_name}"):
                in_section = True
                continue
            if in_section and line.startswith("##"):
                break
            if in_section:
                section_content.append(line)

        return "\n".join(section_content).strip()

    def count_code_blocks(self) -> int:
        """Count number of code blocks (```...```)."""
        count = 0
        in_block = False

        for line in self.lines:
            if line.startswith("```"):
                in_block = not in_block
                if in_block:
                    count += 1

        return count

    def get_title(self) -> str:
        """Extract main title from document."""
        for line in self.lines:
            if line.startswith("# "):
                return line[2:].strip()
        return ""


def validate_code_blocks(doc: MarkdownDoc) -> List[str]:
    """
    Validate code blocks in documentation.

    Returns:
        List of issues found
    """
    issues = []
    code_blocks = doc.count_code_blocks()

    if code_blocks == 0:
        issues.append("No code examples found")
    elif code_blocks < 2:
        issues.append("Only one code example found (recommend at least 2)")

    return issues


def test_trigger_phrases(doc: MarkdownDoc) -> bool:
    """
    Test that trigger section exists and has content.

    Returns:
        True if triggers are present
    """
    if not doc.has_section("Triggers"):
        return False

    triggers_section = doc.extract_section("Triggers")
    return len(triggers_section.strip()) > 0


def test_skill_documentation(skill_path: Path) -> Dict[str, Any]:
    """
    Run all tests on a skill's documentation.

    Args:
        skill_path: Path to SKILL.md file

    Returns:
        Test results dictionary
    """
    result = {
        "skill": skill_path.parent.name,
        "path": str(skill_path),
        "passed": True,
        "tests": {
            "sections": True,
            "code_blocks": True,
            "triggers": True,
        },
        "issues": [],
        "warnings": [],
    }

    try:
        content = skill_path.read_text(encoding="utf-8")
    except Exception as e:
        result["passed"] = False
        result["issues"].append(f"Could not read file: {e}")
        return result

    doc = MarkdownDoc(content)

    # Test 1: Required sections
    required_sections = ["Description", "Triggers", "Usage", "Parameters", "Output"]
    missing_sections = []

    for section in required_sections:
        if not doc.has_section(section):
            missing_sections.append(section)

    if missing_sections:
        result["passed"] = False
        result["tests"]["sections"] = False
        result["issues"].append(f"Missing sections: {', '.join(missing_sections)}")

    # Test 2: Code blocks
    code_block_issues = validate_code_blocks(doc)
    if code_block_issues:
        result["tests"]["code_blocks"] = False
        for issue in code_block_issues:
            result["warnings"].append(f"Code blocks: {issue}")

    # Test 3: Trigger phrases
    if not test_trigger_phrases(doc):
        result["passed"] = False
        result["tests"]["triggers"] = False
        result["issues"].append("No triggers defined or triggers section is empty")

    # Test 4: Title
    title = doc.get_title()
    if not title:
        result["passed"] = False
        result["issues"].append("No main heading (# ) found")

    return result


def run_all_tests() -> Dict[str, Any]:
    """
    Run tests on all skills.

    Returns:
        Summary of test results
    """
    skills = find_all_skills()

    test_results = {
        "total": len(skills),
        "passed": 0,
        "failed": 0,
        "skills": [],
        "summary": "",
    }

    if not skills:
        log_warning("No skills found to test")
        return test_results

    log_info(f"Testing {len(skills)} skills...")

    for skill_path in skills:
        result = test_skill_documentation(skill_path)
        test_results["skills"].append(result)

        if result["passed"]:
            test_results["passed"] += 1
            log_success(f"PASS: {result['skill']}")
        else:
            test_results["failed"] += 1
            log_error(f"FAIL: {result['skill']}")
            for issue in result["issues"]:
                log_error(f"  - {issue}")

        for warning in result["warnings"]:
            log_warning(f"  - {warning}")

    test_results["summary"] = f"Passed: {test_results['passed']}/{test_results['total']}, Failed: {test_results['failed']}/{test_results['total']}"
    return test_results


def main() -> None:
    """Run skill testing."""
    results = run_all_tests()

    # Save test results
    report_path = Path("test-results.json")
    save_json(results, report_path)

    log_info(results["summary"])

    if results["failed"] > 0:
        exit_failure(f"Skill testing failed: {results['failed']} skills have issues")
    else:
        exit_success("All skills passed testing")


if __name__ == "__main__":
    main()
