#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill format migration script.
Converts skills from legacy format (emoji sections) to strict format.
"""

import sys
import re
from pathlib import Path
from common_utils import find_all_skills, log_info, log_success, log_error, exit_success, exit_failure


def migrate_skill_format(skill_md: Path) -> bool:
    """
    Migrate a skill from legacy format to strict format.

    Args:
        skill_md: Path to SKILL.md file

    Returns:
        True if successful, False otherwise
    """
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        log_error(f"Could not read {skill_md}: {e}")
        return False

    original = content

    # Keep frontmatter (if present)
    frontmatter = ""
    if content.startswith("---"):
        match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if match:
            frontmatter = match.group(0)
            content = content[len(frontmatter):]

    # Define mapping from emoji sections to strict sections
    section_mapping = [
        (r"## 🎯 Purpose", "## Description"),
        (r"## 🚀 Key Features", "## Features"),
        (r"## 📋 Usage", "## Usage"),
        (r"## 🎛️ Parameters", "## Parameters"),
        (r"## 💡 Examples?", "## Examples"),
        (r"## 🎁 Output", "## Output"),
        (r"## 🔧 Configuration", "## Configuration"),
        (r"## ⚙️ Configuration", "## Configuration"),
        (r"## ⚠️ Important Notes", "## Important Notes"),
        (r"## ⚠️ Warnings?", "## Important Notes"),
        (r"## 🎓 Best Practices", "## Best Practices"),
        (r"## 📚 Reference", "## Reference"),
        (r"## 🔗 Related", "## Related"),
        (r"## ✨ Advanced", "## Advanced"),
        (r"## 🆘 Troubleshooting", "## Troubleshooting"),
        (r"## 🔐 Security", "## Security"),
    ]

    # Apply replacements
    for old, new in section_mapping:
        content = re.sub(old, new, content)

    # Check if content changed
    new_full_content = frontmatter + content
    if new_full_content == original:
        return True  # No changes needed (already in correct format)

    # Write updated content
    try:
        skill_md.write_text(new_full_content, encoding="utf-8")
        return True
    except Exception as e:
        log_error(f"Could not write {skill_md}: {e}")
        return False


def main() -> None:
    """Migrate all skills to strict format."""
    skills = find_all_skills()

    if not skills:
        exit_failure("No skills found to migrate")

    log_info(f"Migrating {len(skills)} skills to strict format...")

    migrated = 0
    failed = 0

    for skill_md in skills:
        skill_name = skill_md.parent.name
        if migrate_skill_format(skill_md):
            migrated += 1
            log_success(f"Migrated: {skill_name}")
        else:
            failed += 1
            log_error(f"Failed: {skill_name}")

    log_info(f"\nMigration complete: {migrated}/{len(skills)} successful")

    if failed > 0:
        exit_failure(f"Migration failed for {failed} skills")
    else:
        exit_success(f"All {migrated} skills migrated successfully")


if __name__ == "__main__":
    main()
