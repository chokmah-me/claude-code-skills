"""
Skill Metadata Management

This module provides functionality to load, parse, and cache skill metadata
from the claude-code-skills repository structure.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class SkillMetadata:
    """Represents metadata for a single skill."""
    name: str
    category: str
    description: str
    priority: str  # high, medium, low
    dependencies: List[str]
    file_path: str
    token_estimate: int = 1000  # Default estimate
    features: List[str] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)
    quality_score: float = 0.8  # Default quality score


class SkillMetadataLoader:
    """Loads and caches skill metadata from the repository."""

    def __init__(self, repo_root: Optional[str] = None):
        """
        Initialize the metadata loader.

        Args:
            repo_root: Root directory of claude-code-skills repo.
                      If None, attempts to auto-detect.
        """
        self.repo_root = Path(repo_root) if repo_root else self._find_repo_root()
        self._cache: Optional[Dict[str, SkillMetadata]] = None

    def _find_repo_root(self) -> Path:
        """Auto-detect repository root by searching for install.py."""
        current = Path.cwd()

        # Try current directory first
        if (current / "install.py").exists():
            return current

        # Try parent directories
        for parent in current.parents:
            if (parent / "install.py").exists():
                return parent

        # Default to current directory
        return current

    def _load_manifest_from_install_py(self) -> Dict:
        """
        Extract the skills manifest from install.py.

        Returns:
            Dict with structure: {category: {description: str, skills: {...}}}
        """
        # Hardcoded manifest matching install.py structure
        # In production, this could parse install.py dynamically
        return {
            "meta": {
                "description": "Meta-skills for workflow management and automation",
                "skills": {
                    "session-snapshot": {
                        "file": "skills/meta/session-snapshot/SKILL.md",
                        "description": "Complete session context management",
                        "priority": "high",
                        "dependencies": []
                    },
                    "skill-extractor": {
                        "file": "skills/meta/skill-extractor/SKILL.md",
                        "description": "Automated skill discovery and documentation",
                        "priority": "high",
                        "dependencies": []
                    },
                    "skill-recommendation-engine": {
                        "file": "skills/meta/skill-recommendation-engine/SKILL.md",
                        "description": "Context-aware skill recommendations",
                        "priority": "medium",
                        "dependencies": ["skill-extractor"]
                    },
                    "claude-startup-integration": {
                        "file": "skills/meta/claude-startup-integration/SKILL.md",
                        "description": "Startup configuration and optimization",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "startup-skill-showcase": {
                        "file": "skills/meta/startup-skill-showcase/SKILL.md",
                        "description": "Interactive skill demonstration and showcase",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "manifest-generator": {
                        "file": "skills/meta/manifest-generator/SKILL.md",
                        "description": "Generate and manage skill manifests",
                        "priority": "low",
                        "dependencies": []
                    }
                }
            },
            "development": {
                "description": "Core development and coding skills",
                "skills": {
                    "lean-plan": {
                        "file": "skills/development/lean-plan/SKILL.md",
                        "description": "Token-efficient planning mode for complex tasks",
                        "priority": "high",
                        "dependencies": []
                    },
                    "quick-test-runner": {
                        "file": "skills/development/quick-test-runner/SKILL.md",
                        "description": "Fast test execution and validation workflows",
                        "priority": "high",
                        "dependencies": []
                    },
                    "refactoring": {
                        "file": "skills/development/refactoring/SKILL.md",
                        "description": "Code restructuring and modernization workflows",
                        "priority": "medium",
                        "dependencies": []
                    }
                }
            },
            "git": {
                "description": "Git and version control utilities",
                "skills": {
                    "diff-summariser": {
                        "file": "skills/git/diff-summariser/SKILL.md",
                        "description": "Summarize git diffs for code review",
                        "priority": "high",
                        "dependencies": []
                    },
                    "migrate-repo": {
                        "file": "skills/git/migrate-repo/SKILL.md",
                        "description": "Transfer repositories between accounts/orgs",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "repo-briefing": {
                        "file": "skills/git/repo-briefing/SKILL.md",
                        "description": "Generate compact repository summaries",
                        "priority": "medium",
                        "dependencies": []
                    }
                }
            },
            "analysis": {
                "description": "Code analysis and debugging tools",
                "skills": {
                    "api-contract-sniffer": {
                        "file": "skills/analysis/code/api-contract-sniffer/SKILL.md",
                        "description": "Detect API contract violations and inconsistencies",
                        "priority": "high",
                        "dependencies": []
                    },
                    "dead-code-hunter": {
                        "file": "skills/analysis/code/dead-code-hunter/SKILL.md",
                        "description": "Find unused functions, imports, and dead code",
                        "priority": "high",
                        "dependencies": []
                    },
                    "dependency-audit": {
                        "file": "skills/analysis/code/dependency-audit/SKILL.md",
                        "description": "Check for outdated and vulnerable dependencies",
                        "priority": "high",
                        "dependencies": []
                    },
                    "ascii-sanitizer": {
                        "file": "skills/analysis/code/ascii-sanitizer/SKILL.md",
                        "description": "Detect and remove unsafe Unicode/emoji characters",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "anti-pattern-sniffer": {
                        "file": "skills/analysis/formal/anti-pattern-sniffer/SKILL.md",
                        "description": "Detect proof anti-patterns in formal verification",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "lemma-dependency-graph": {
                        "file": "skills/analysis/formal/lemma-dependency-graph/SKILL.md",
                        "description": "Visualize proof dependencies and relationships",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "proof-obligations-snapshot": {
                        "file": "skills/analysis/formal/proof-obligations-snapshot/SKILL.md",
                        "description": "Track unproven obligations in formal systems",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "tactic-usage-count": {
                        "file": "skills/analysis/formal/tactic-usage-count/SKILL.md",
                        "description": "Analyze proof tactics usage patterns",
                        "priority": "low",
                        "dependencies": []
                    },
                    "quantum-circuit-optimizer": {
                        "file": "skills/analysis/quantum/quantum-circuit-optimizer/SKILL.md",
                        "description": "Optimize quantum circuits by reducing gate count and depth",
                        "priority": "medium",
                        "dependencies": []
                    }
                }
            }
        }

    def _parse_token_estimates(self) -> Dict[str, int]:
        """
        Parse token estimates from SKILLS_INVENTORY.md if available.

        Returns:
            Dict mapping skill names to token estimates.
        """
        # Hardcoded estimates based on SKILLS_INVENTORY.md analysis
        # In production, could parse the file dynamically
        return {
            "api-contract-sniffer": 500,
            "ascii-sanitizer": 600,
            "dead-code-hunter": 1000,
            "dependency-audit": 600,
            "anti-pattern-sniffer": 800,
            "lemma-dependency-graph": 1000,
            "proof-obligations-snapshot": 700,
            "tactic-usage-count": 600,
            "quantum-circuit-optimizer": 800,
            "lean-plan": 1200,
            "quick-test-runner": 300,
            "refactoring": 1500,
            "diff-summariser": 400,
            "migrate-repo": 800,
            "repo-briefing": 1000,
            "session-snapshot": 400,
            "skill-extractor": 1200,
            "skill-recommendation-engine": 800,
            "claude-startup-integration": 600,
            "startup-skill-showcase": 500,
            "manifest-generator": 700
        }

    def load_all_skills(self) -> Dict[str, SkillMetadata]:
        """
        Load all skills from the manifest.

        Returns:
            Dict mapping skill name to SkillMetadata.
        """
        if self._cache is not None:
            return self._cache

        manifest = self._load_manifest_from_install_py()
        token_estimates = self._parse_token_estimates()
        skills = {}

        for category, cat_data in manifest.items():
            for skill_name, skill_data in cat_data["skills"].items():
                # Determine full category (e.g., "analysis/code", "analysis/formal")
                full_category = category
                if category == "analysis":
                    # Infer subcategory from file path
                    if "/code/" in skill_data["file"]:
                        full_category = "analysis/code"
                    elif "/formal/" in skill_data["file"]:
                        full_category = "analysis/formal"
                    elif "/quantum/" in skill_data["file"]:
                        full_category = "analysis/quantum"

                skills[skill_name] = SkillMetadata(
                    name=skill_name,
                    category=full_category,
                    description=skill_data["description"],
                    priority=skill_data["priority"],
                    dependencies=skill_data.get("dependencies", []),
                    file_path=skill_data["file"],
                    token_estimate=token_estimates.get(skill_name, 1000),
                    features=[],  # Could be populated by parsing SKILL.md
                    use_cases=[],  # Could be populated from SKILLS_INVENTORY
                    quality_score=0.8  # Default score
                )

        self._cache = skills
        return skills

    def get_skill(self, name: str) -> Optional[SkillMetadata]:
        """
        Retrieve metadata for a specific skill.

        Args:
            name: Skill name (e.g., "quick-test-runner")

        Returns:
            SkillMetadata if found, None otherwise.
        """
        skills = self.load_all_skills()
        return skills.get(name)

    def filter_by_category(self, category: str) -> List[SkillMetadata]:
        """
        Get all skills in a specific category.

        Args:
            category: Category name (e.g., "development", "analysis/formal")

        Returns:
            List of SkillMetadata objects in that category.
        """
        skills = self.load_all_skills()
        return [
            skill for skill in skills.values()
            if skill.category == category or skill.category.startswith(category + "/")
        ]

    def filter_by_priority(self, priority: str) -> List[SkillMetadata]:
        """
        Get all skills with a specific priority level.

        Args:
            priority: Priority level ("high", "medium", "low")

        Returns:
            List of SkillMetadata objects with that priority.
        """
        skills = self.load_all_skills()
        return [skill for skill in skills.values() if skill.priority == priority]

    def search_by_keyword(self, keyword: str) -> List[SkillMetadata]:
        """
        Search skills by keyword in name or description.

        Args:
            keyword: Search term (case-insensitive)

        Returns:
            List of matching SkillMetadata objects.
        """
        skills = self.load_all_skills()
        keyword_lower = keyword.lower()

        return [
            skill for skill in skills.values()
            if keyword_lower in skill.name.lower()
            or keyword_lower in skill.description.lower()
        ]

    def get_all(self) -> Dict[str, SkillMetadata]:
        """
        Get all skills as a dictionary.

        Returns:
            Dict mapping skill name to SkillMetadata.
        """
        return self.load_all_skills()
