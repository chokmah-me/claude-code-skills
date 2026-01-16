#!/usr/bin/env python3
"""
Manifest builder for Claude Code skills repository.
Scans skills directory and generates unified manifest.
"""

from pathlib import Path
from typing import Any, Dict, List

from common_utils import (
    find_all_skills,
    find_skills_directory,
    log_error,
    log_info,
    log_success,
    log_warning,
    exit_failure,
    exit_success,
    get_repo_root,
)


def parse_skill_metadata(skill_md: Path) -> Dict[str, Any]:
    """
    Parse metadata from a skill markdown file.

    Args:
        skill_md: Path to SKILL.md file

    Returns:
        Dictionary with skill metadata
    """
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        log_error(f"Could not read {skill_md}: {e}")
        return {}

    metadata = {
        "name": skill_md.parent.name,
        "path": str(skill_md.parent.relative_to(skill_md.parent.parent.parent)),
        "description": "",
        "triggers": [],
        "category": "",
    }

    lines = content.split("\n")

    # Extract description (first non-empty line after heading)
    in_description = False
    for i, line in enumerate(lines):
        if line.startswith("## Description"):
            in_description = True
            continue
        if in_description and line.strip():
            metadata["description"] = line.strip()
            break
        if in_description and line.startswith("##"):
            break

    # Extract triggers
    in_triggers = False
    for i, line in enumerate(lines):
        if line.startswith("## Triggers"):
            in_triggers = True
            continue
        if in_triggers:
            if line.startswith("##"):
                break
            if line.strip() and not line.startswith("#"):
                # Extract trigger text (remove markdown formatting)
                trigger = line.replace("- ", "").replace("* ", "").strip()
                if trigger and not trigger.startswith("```"):
                    metadata["triggers"].append(trigger)

    # Determine category from directory structure
    parts = skill_md.parent.parts
    for i, part in enumerate(parts):
        if part == "skills" and i + 1 < len(parts):
            metadata["category"] = parts[i + 1]
            break

    return metadata


def scan_skills_directory() -> List[Dict[str, Any]]:
    """
    Scan skills directory and extract metadata from all skills.

    Returns:
        List of skill metadata dictionaries
    """
    skills = find_all_skills()
    metadata_list = []

    log_info(f"Scanning {len(skills)} skills...")

    for skill_md in skills:
        metadata = parse_skill_metadata(skill_md)
        if metadata:
            metadata_list.append(metadata)
            log_success(f"Parsed: {metadata['name']}")

    return sorted(metadata_list, key=lambda x: (x.get("category", ""), x.get("name", "")))


def build_manifest(skills: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Build unified manifest from skill metadata.

    Args:
        skills: List of skill metadata dictionaries

    Returns:
        Manifest dictionary
    """
    manifest = {
        "version": "1.0",
        "timestamp": "",
        "total_skills": len(skills),
        "categories": {},
        "skills": skills,
    }

    # Group by category
    for skill in skills:
        category = skill.get("category", "uncategorized")
        if category not in manifest["categories"]:
            manifest["categories"][category] = []
        manifest["categories"][category].append(skill["name"])

    return manifest


def validate_manifest_structure(manifest: Dict[str, Any]) -> bool:
    """
    Validate that manifest has required structure.

    Args:
        manifest: Manifest dictionary

    Returns:
        True if valid, False otherwise
    """
    required_keys = ["version", "total_skills", "skills", "categories"]

    for key in required_keys:
        if key not in manifest:
            log_error(f"Missing required key in manifest: {key}")
            return False

    if manifest["total_skills"] != len(manifest["skills"]):
        log_error(f"Skill count mismatch: {manifest['total_skills']} vs {len(manifest['skills'])}")
        return False

    return True


def save_manifest_json(manifest: Dict[str, Any], output_path: Path) -> bool:
    """
    Save manifest as JSON file.

    Args:
        manifest: Manifest dictionary
        output_path: Path to save manifest

    Returns:
        True if successful, False otherwise
    """
    import json

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(manifest, f, indent=2)
        log_success(f"Saved manifest: {output_path}")
        return True
    except Exception as e:
        log_error(f"Failed to save manifest: {e}")
        return False


def save_manifest_markdown(manifest: Dict[str, Any], output_path: Path) -> bool:
    """
    Save manifest as markdown file.

    Args:
        manifest: Manifest dictionary
        output_path: Path to save manifest

    Returns:
        True if successful, False otherwise
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            "# Unified Skill Manifest",
            "",
            f"**Version**: {manifest['version']}",
            f"**Total Skills**: {manifest['total_skills']}",
            "",
            "## Skills by Category",
            "",
        ]

        for category in sorted(manifest["categories"].keys()):
            skills = manifest["categories"][category]
            lines.append(f"### {category.title()}")
            lines.append("")
            for skill_name in sorted(skills):
                lines.append(f"- {skill_name}")
            lines.append("")

        lines.append("## All Skills")
        lines.append("")
        for skill in manifest["skills"]:
            lines.append(f"- **{skill['name']}** ({skill.get('category', 'uncategorized')})")
            if skill.get("description"):
                lines.append(f"  {skill['description']}")

        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        log_success(f"Saved manifest: {output_path}")
        return True
    except Exception as e:
        log_error(f"Failed to save manifest: {e}")
        return False


def main() -> None:
    """Build and save manifest."""
    log_info("Building skill manifest...")

    # Scan skills
    skills = scan_skills_directory()
    if not skills:
        exit_failure("No skills found to include in manifest")

    # Build manifest
    manifest = build_manifest(skills)

    # Validate
    if not validate_manifest_structure(manifest):
        exit_failure("Generated manifest is invalid")

    # Save manifest files
    repo_root = get_repo_root()

    json_path = repo_root / "SKILL_MANIFEST.json"
    if not save_manifest_json(manifest, json_path):
        exit_failure("Failed to save JSON manifest")

    md_path = repo_root / "UNIFIED_SKILL_MANIFEST.md"
    if not save_manifest_markdown(manifest, md_path):
        exit_failure("Failed to save markdown manifest")

    exit_success(f"Manifest built successfully: {manifest['total_skills']} skills")


if __name__ == "__main__":
    main()
