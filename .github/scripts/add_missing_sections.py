#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add missing documentation sections to skills.
Intelligently inserts missing sections based on existing content.
"""

import re
from pathlib import Path
from common_utils import find_all_skills, log_info, log_success, log_error, exit_success, exit_failure


# Default content for missing sections
DEFAULT_SECTIONS = {
    "Description": "A concise description of what this skill does and its primary purpose.",
    "Triggers": "- User says 'use [skill-name]' or mentions the skill by name\n- Relevant to the current task or discussion",
    "Usage": "When user requests this skill:\n\n1. Perform the primary action\n2. Report findings or results\n3. Offer next steps or related actions",
    "Parameters": "No additional parameters required.",
    "Output": "Results of the skill execution in a clear, actionable format.",
}

SECTION_ORDER = [
    "Description",
    "Triggers",
    "Usage",
    "Parameters",
    "Features",
    "Examples",
    "Output",
    "Configuration",
    "Important Notes",
    "Best Practices",
]


def extract_sections(content: str) -> dict:
    """Extract all current sections from skill content."""
    sections = {}
    section_pattern = r"^## (.+)$"
    current_section = None
    current_content = []

    for line in content.split("\n"):
        match = re.match(section_pattern, line)
        if match:
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = match.group(1)
            current_content = [line]
        else:
            if current_section:
                current_content.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def rebuild_content(skill_md: Path, sections: dict) -> str:
    """Rebuild skill content with properly ordered sections."""
    # Read frontmatter if present
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception:
        return ""

    frontmatter = ""
    if content.startswith("---"):
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if match:
            frontmatter = match.group(0)

    # Get title
    title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
    title = f"# {title_match.group(1)}\n\n" if title_match else "# Skill\n\n"

    # Build content with proper section order
    ordered_content = [frontmatter, title] if frontmatter else [title]

    for section in SECTION_ORDER:
        if section in sections:
            ordered_content.append(sections[section])
            ordered_content.append("")

    return "\n".join(ordered_content).strip() + "\n"


def add_missing_sections(skill_md: Path) -> bool:
    """Add missing sections to a skill."""
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        log_error(f"Could not read {skill_md}: {e}")
        return False

    # Extract existing sections
    sections = extract_sections(content)

    # Add missing required sections
    missing = []
    for required in ["Description", "Triggers", "Usage", "Parameters", "Output"]:
        if required not in sections:
            sections[required] = DEFAULT_SECTIONS.get(required, "")
            missing.append(required)

    if not missing:
        return True  # No changes needed

    # Rebuild content with all sections
    new_content = rebuild_content(skill_md, sections)

    # Write updated content
    try:
        skill_md.write_text(new_content, encoding="utf-8")
        return True
    except Exception as e:
        log_error(f"Could not write {skill_md}: {e}")
        return False


def main() -> None:
    """Add missing sections to all skills."""
    skills = find_all_skills()

    if not skills:
        exit_failure("No skills found")

    log_info(f"Adding missing sections to {len(skills)} skills...")

    updated = 0
    failed = 0

    for skill_md in skills:
        skill_name = skill_md.parent.name
        if add_missing_sections(skill_md):
            updated += 1
            log_success(f"Updated: {skill_name}")
        else:
            failed += 1
            log_error(f"Failed: {skill_name}")

    log_info(f"\nUpdate complete: {updated}/{len(skills)} successful")

    if failed > 0:
        exit_failure(f"Failed to update {failed} skills")
    else:
        exit_success(f"All {updated} skills updated with missing sections")


if __name__ == "__main__":
    main()
