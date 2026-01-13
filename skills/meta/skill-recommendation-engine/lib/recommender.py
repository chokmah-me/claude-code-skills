"""
Main Recommendation Engine

Orchestrates all components to generate intelligent skill recommendations.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional

# Import all components
from .skill_metadata import SkillMetadataLoader, SkillMetadata
from .context_analyzer import ContextAnalyzer, ContextAnalysis
from .project_analyzer import ProjectAnalyzer, ProjectState
from .user_patterns import UserPatternAnalyzer, UserPreferences
from .skill_utility import SkillUtilityScorer, SkillUtility
from .confidence_scorer import ConfidenceScorer


@dataclass
class Recommendation:
    """Represents a single skill recommendation."""
    skill: SkillMetadata
    confidence: float  # 0-100
    context: ContextAnalysis
    reasoning: str
    category: str  # Immediate Needs, Quick Wins, etc.

    def __post_init__(self):
        """Categorize based on confidence after initialization."""
        if not self.category:  # Only categorize if not already set
            if self.confidence >= 90:
                self.category = "🎯 Immediate Needs"
            elif self.confidence >= 80:
                self.category = "⚡ Quick Wins"
            elif self.confidence >= 70:
                self.category = "🔍 Investigation Worthy"
            elif self.confidence >= 60:
                self.category = "📈 Future Considerations"
            else:
                self.category = "💡 Low Priority"


class SkillRecommender:
    """Main recommendation engine that coordinates all analysis components."""

    def __init__(self, skills_dir: Optional[str] = None, data_dir: Optional[str] = None):
        """
        Initialize the recommender.

        Args:
            skills_dir: Directory containing skills (for metadata loader)
            data_dir: Directory for user data storage
        """
        self.skills_metadata = SkillMetadataLoader(repo_root=skills_dir)
        self.context_analyzer = ContextAnalyzer()
        self.project_analyzer = ProjectAnalyzer()
        self.user_patterns = UserPatternAnalyzer(data_dir=data_dir)
        self.skill_utility = SkillUtilityScorer()
        self.confidence_scorer = ConfidenceScorer()

    def recommend(
        self,
        top_n: int = 5,
        min_confidence: float = 60.0,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Recommendation]:
        """
        Generate skill recommendations based on current context.

        Args:
            top_n: Number of top recommendations to return
            min_confidence: Minimum confidence threshold (0-100)
            filters: Optional filters (e.g., {'category': 'development'})

        Returns:
            List of Recommendation objects sorted by confidence.
        """
        # 1. Gather context
        context = self.context_analyzer.analyze()
        project_state = self.project_analyzer.analyze()
        user_prefs = self.user_patterns.load_preferences()

        # 2. Score all skills
        recommendations = []
        all_skills = self.skills_metadata.load_all_skills()

        for skill_name, skill_meta in all_skills.items():
            # Apply filters if provided
            if filters:
                if 'category' in filters and skill_meta.category != filters['category']:
                    continue
                if 'priority' in filters and skill_meta.priority != filters['priority']:
                    continue

            # Get utility scores
            utility = self.skill_utility.get_utility_score(skill_name)

            # Calculate confidence
            confidence = self.confidence_scorer.calculate_confidence(
                skill=skill_meta,
                context=context,
                project_state=project_state,
                user_prefs=user_prefs,
                skill_utility=utility
            )

            # Only include if meets minimum confidence
            if confidence >= min_confidence:
                reasoning = self._generate_reasoning(skill_meta, context, project_state, confidence)

                recommendations.append(
                    Recommendation(
                        skill=skill_meta,
                        confidence=confidence,
                        context=context,
                        reasoning=reasoning,
                        category=""  # Will be set in __post_init__
                    )
                )

        # 3. Sort by confidence (highest first) and return top N
        recommendations.sort(key=lambda r: r.confidence, reverse=True)
        return recommendations[:top_n]

    def _generate_reasoning(
        self,
        skill: SkillMetadata,
        context: ContextAnalysis,
        project_state: ProjectState,
        confidence: float
    ) -> str:
        """
        Generate human-readable explanation for recommendation.

        Args:
            skill: SkillMetadata object
            context: ContextAnalysis object
            project_state: ProjectState object
            confidence: Confidence score

        Returns:
            Reasoning string
        """
        reasons = []

        # Activity-based reasoning
        if context.current_activity and context.current_activity != "exploring":
            reasons.append(f"Currently {context.current_activity}")

        # File type reasoning
        if context.file_types:
            file_types_str = ", ".join(sorted(context.file_types)[:3])
            reasons.append(f"Working with {file_types_str} files")

        # Recent changes reasoning
        if context.recent_changes.get('modified'):
            count = len(context.recent_changes['modified'])
            if count > 0:
                reasons.append(f"{count} file{'s' if count != 1 else ''} modified")

        # Project state reasoning
        if project_state.repository_age_days > 365:
            reasons.append(f"Mature project ({project_state.repository_age_days // 365}+ years old)")

        if project_state.test_coverage_estimate == "low":
            reasons.append("Low test coverage detected")

        if project_state.dependency_count > 50:
            reasons.append(f"Many dependencies ({project_state.dependency_count})")

        # Skill-specific reasoning
        if skill.name == "quick-test-runner" and context.current_activity == "coding":
            reasons.append("Validate changes quickly")
        elif skill.name == "diff-summariser" and context.recent_changes.get('modified'):
            reasons.append("Review changes before committing")
        elif skill.name == "dead-code-hunter" and project_state.repository_age_days > 365:
            reasons.append("Old codebase likely has unused code")
        elif skill.name == "dependency-audit" and project_state.dependency_count > 20:
            reasons.append("Review dependency health")

        # Default reasoning if no specific reasons
        if not reasons:
            reasons.append(f"{skill.description}")

        return " - ".join(reasons[:4])  # Limit to 4 reasons for brevity

    def recommend_for_scenario(self, scenario: str) -> List[Recommendation]:
        """
        Get recommendations for a specific scenario.

        Args:
            scenario: Scenario name (e.g., "new_project", "code_review", "debugging")

        Returns:
            List of recommendations tailored to the scenario.
        """
        scenario_filters = {
            "new_project": {"priority": "high"},
            "code_review": {},  # Will rely on context analysis
            "debugging": {},
            "refactoring": {},
            "testing": {}
        }

        filters = scenario_filters.get(scenario, {})
        return self.recommend(top_n=5, min_confidence=60.0, filters=filters)

    def get_recommendation_summary(self, recommendations: List[Recommendation]) -> Dict[str, Any]:
        """
        Generate a summary of recommendations.

        Args:
            recommendations: List of Recommendation objects

        Returns:
            Summary dict with statistics and groupings.
        """
        if not recommendations:
            return {
                "total_count": 0,
                "by_category": {},
                "by_skill_category": {},
                "average_confidence": 0.0
            }

        # Group by confidence category
        by_category = {}
        for rec in recommendations:
            cat = rec.category
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(rec.skill.name)

        # Group by skill category
        by_skill_category = {}
        for rec in recommendations:
            cat = rec.skill.category
            if cat not in by_skill_category:
                by_skill_category[cat] = []
            by_skill_category[cat].append(rec.skill.name)

        # Calculate average confidence
        avg_confidence = sum(r.confidence for r in recommendations) / len(recommendations)

        return {
            "total_count": len(recommendations),
            "by_category": by_category,
            "by_skill_category": by_skill_category,
            "average_confidence": round(avg_confidence, 1),
            "top_recommendation": recommendations[0].skill.name if recommendations else None
        }
