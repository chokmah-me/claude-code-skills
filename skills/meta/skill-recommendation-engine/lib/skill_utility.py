"""
Skill Utility Scoring Module

Provides base utility scores for each skill based on frequency of need,
token efficiency, time savings, reliability, and ease of use.
Implements 10% weight of the recommendation algorithm.
"""

from dataclasses import dataclass
from typing import Dict, Optional

# Import skill metadata for type hinting
try:
    from .skill_metadata import SkillMetadata
except ImportError:
    SkillMetadata = None  # Fallback


@dataclass
class SkillUtility:
    """Represents utility metrics for a skill."""
    frequency_of_need: float  # 0.0-1.0
    token_efficiency: float  # 0.0-1.0
    time_savings: float  # 0.0-1.0
    reliability_score: float  # 0.0-1.0
    ease_of_use: float  # 0.0-1.0


class SkillUtilityScorer:
    """Manages utility scoring for skills."""

    def __init__(self):
        """Initialize utility scorer with base utility scores."""
        self.base_utilities = self._load_base_utilities()

    def _load_base_utilities(self) -> Dict[str, SkillUtility]:
        """
        Load base utility scores for all skills.

        Returns:
            Dict mapping skill names to SkillUtility objects.
        """
        return {
            # Meta skills
            "session-snapshot": SkillUtility(
                frequency_of_need=0.7,
                token_efficiency=0.9,
                time_savings=0.8,
                reliability_score=0.95,
                ease_of_use=0.9
            ),
            "skill-extractor": SkillUtility(
                frequency_of_need=0.5,
                token_efficiency=0.75,
                time_savings=0.85,
                reliability_score=0.8,
                ease_of_use=0.7
            ),
            "skill-recommendation-engine": SkillUtility(
                frequency_of_need=0.6,
                token_efficiency=0.8,
                time_savings=0.75,
                reliability_score=0.85,
                ease_of_use=0.85
            ),
            "claude-startup-integration": SkillUtility(
                frequency_of_need=0.4,
                token_efficiency=0.85,
                time_savings=0.7,
                reliability_score=0.9,
                ease_of_use=0.8
            ),
            "startup-skill-showcase": SkillUtility(
                frequency_of_need=0.3,
                token_efficiency=0.9,
                time_savings=0.6,
                reliability_score=0.9,
                ease_of_use=0.95
            ),
            "manifest-generator": SkillUtility(
                frequency_of_need=0.3,
                token_efficiency=0.85,
                time_savings=0.8,
                reliability_score=0.85,
                ease_of_use=0.75
            ),

            # Development skills
            "lean-plan": SkillUtility(
                frequency_of_need=0.6,
                token_efficiency=0.95,
                time_savings=0.8,
                reliability_score=0.85,
                ease_of_use=0.8
            ),
            "quick-test-runner": SkillUtility(
                frequency_of_need=0.9,
                token_efficiency=0.9,
                time_savings=0.95,
                reliability_score=0.9,
                ease_of_use=0.95
            ),
            "refactoring": SkillUtility(
                frequency_of_need=0.5,
                token_efficiency=0.7,
                time_savings=0.85,
                reliability_score=0.75,
                ease_of_use=0.7
            ),

            # Git skills
            "diff-summariser": SkillUtility(
                frequency_of_need=0.8,
                token_efficiency=0.95,
                time_savings=0.9,
                reliability_score=0.95,
                ease_of_use=0.95
            ),
            "migrate-repo": SkillUtility(
                frequency_of_need=0.2,
                token_efficiency=0.8,
                time_savings=0.9,
                reliability_score=0.85,
                ease_of_use=0.75
            ),
            "repo-briefing": SkillUtility(
                frequency_of_need=0.6,
                token_efficiency=0.85,
                time_savings=0.85,
                reliability_score=0.9,
                ease_of_use=0.9
            ),

            # Analysis / Code skills
            "api-contract-sniffer": SkillUtility(
                frequency_of_need=0.6,
                token_efficiency=0.9,
                time_savings=0.8,
                reliability_score=0.85,
                ease_of_use=0.85
            ),
            "dead-code-hunter": SkillUtility(
                frequency_of_need=0.5,
                token_efficiency=0.85,
                time_savings=0.85,
                reliability_score=0.8,
                ease_of_use=0.85
            ),
            "dependency-audit": SkillUtility(
                frequency_of_need=0.7,
                token_efficiency=0.9,
                time_savings=0.8,
                reliability_score=0.9,
                ease_of_use=0.9
            ),
            "ascii-sanitizer": SkillUtility(
                frequency_of_need=0.3,
                token_efficiency=0.85,
                time_savings=0.7,
                reliability_score=0.9,
                ease_of_use=0.85
            ),

            # Analysis / Formal skills
            "anti-pattern-sniffer": SkillUtility(
                frequency_of_need=0.4,
                token_efficiency=0.8,
                time_savings=0.75,
                reliability_score=0.8,
                ease_of_use=0.75
            ),
            "lemma-dependency-graph": SkillUtility(
                frequency_of_need=0.4,
                token_efficiency=0.75,
                time_savings=0.8,
                reliability_score=0.8,
                ease_of_use=0.7
            ),
            "proof-obligations-snapshot": SkillUtility(
                frequency_of_need=0.5,
                token_efficiency=0.85,
                time_savings=0.8,
                reliability_score=0.9,
                ease_of_use=0.85
            ),
            "tactic-usage-count": SkillUtility(
                frequency_of_need=0.3,
                token_efficiency=0.9,
                time_savings=0.7,
                reliability_score=0.85,
                ease_of_use=0.85
            ),

            # Analysis / Quantum skills
            "quantum-circuit-optimizer": SkillUtility(
                frequency_of_need=0.3,
                token_efficiency=0.8,
                time_savings=0.85,
                reliability_score=0.75,
                ease_of_use=0.7
            )
        }

    def get_utility_score(self, skill_name: str) -> SkillUtility:
        """
        Get utility scores for a specific skill.

        Args:
            skill_name: Name of the skill

        Returns:
            SkillUtility object with all metrics.
        """
        # Return base utility if available
        if skill_name in self.base_utilities:
            return self.base_utilities[skill_name]

        # Return default utility for unknown skills
        return SkillUtility(
            frequency_of_need=0.5,
            token_efficiency=0.7,
            time_savings=0.6,
            reliability_score=0.7,
            ease_of_use=0.7
        )

    def calculate_token_efficiency(self, skill_metadata: Optional[any] = None, token_estimate: int = 1000) -> float:
        """
        Calculate token efficiency score.

        Args:
            skill_metadata: Optional SkillMetadata object
            token_estimate: Token estimate if metadata not provided

        Returns:
            Token efficiency score 0.0-1.0 (higher is more efficient)
        """
        if skill_metadata and hasattr(skill_metadata, 'token_estimate'):
            tokens = skill_metadata.token_estimate
        else:
            tokens = token_estimate

        # Formula: efficiency decreases as tokens increase
        # 300 tokens = 0.9, 1500 tokens = 0.5, 3000 tokens = 0.0
        efficiency = 1.0 - (tokens / 3000.0)
        return max(0.0, min(1.0, efficiency))

    def estimate_time_savings(self, skill_name: str, category: str = "", priority: str = "medium") -> float:
        """
        Estimate time savings for a skill.

        Args:
            skill_name: Name of the skill
            category: Category (meta, development, git, analysis)
            priority: Priority level (high, medium, low)

        Returns:
            Time savings score 0.0-1.0
        """
        # Use base utility if available
        if skill_name in self.base_utilities:
            return self.base_utilities[skill_name].time_savings

        # Estimate based on category and priority
        base_score = 0.6

        # Category adjustments
        if category.startswith("meta"):
            base_score += 0.1
        elif category == "development":
            base_score += 0.15
        elif category == "git":
            base_score += 0.1
        elif category.startswith("analysis"):
            base_score += 0.05

        # Priority adjustments
        if priority == "high":
            base_score += 0.1
        elif priority == "low":
            base_score -= 0.1

        return max(0.0, min(1.0, base_score))

    def get_all_utilities(self) -> Dict[str, SkillUtility]:
        """
        Get all base utility scores.

        Returns:
            Dict mapping skill names to SkillUtility objects.
        """
        return self.base_utilities

    def calculate_overall_utility(self, skill_name: str) -> float:
        """
        Calculate an overall utility score (weighted average).

        Args:
            skill_name: Name of the skill

        Returns:
            Overall utility score 0.0-1.0
        """
        utility = self.get_utility_score(skill_name)

        # Weighted average of components
        overall = (
            utility.frequency_of_need * 0.3 +
            utility.token_efficiency * 0.2 +
            utility.time_savings * 0.3 +
            utility.reliability_score * 0.1 +
            utility.ease_of_use * 0.1
        )

        return overall
