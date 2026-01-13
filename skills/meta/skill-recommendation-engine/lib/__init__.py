"""
Skill Recommendation Engine - Public API

This library provides intelligent skill recommendations based on context analysis,
project state, user behavior patterns, and skill utility.

Usage:
    from skill_recommendation_engine import get_recommendations, record_feedback

    # Get recommendations
    recommendations = get_recommendations(top_n=3, min_confidence=70.0)
    for rec in recommendations:
        print(f"{rec.skill.name} ({rec.confidence:.1f}%): {rec.reasoning}")

    # Record feedback
    record_feedback("quick-test-runner", "success", rating=5, notes="Very helpful!")
"""

from typing import List, Optional

# Import main components
from .recommender import SkillRecommender, Recommendation
from .context_analyzer import ContextAnalysis, ContextAnalyzer
from .project_analyzer import ProjectState, ProjectAnalyzer
from .user_patterns import UserPreferences, UserPatternAnalyzer
from .skill_metadata import SkillMetadata, SkillMetadataLoader
from .skill_utility import SkillUtility, SkillUtilityScorer
from .confidence_scorer import ConfidenceScorer

__version__ = "1.0.0"
__all__ = [
    # Main functions
    "get_recommendations",
    "record_feedback",

    # Classes
    "SkillRecommender",
    "Recommendation",
    "ContextAnalysis",
    "ContextAnalyzer",
    "ProjectState",
    "ProjectAnalyzer",
    "UserPreferences",
    "UserPatternAnalyzer",
    "SkillMetadata",
    "SkillMetadataLoader",
    "SkillUtility",
    "SkillUtilityScorer",
    "ConfidenceScorer"
]


def get_recommendations(
    top_n: int = 5,
    min_confidence: float = 60.0,
    skills_dir: Optional[str] = None,
    data_dir: Optional[str] = None
) -> List[Recommendation]:
    """
    Quick function to get skill recommendations.

    Args:
        top_n: Number of recommendations to return (default 5)
        min_confidence: Minimum confidence threshold 0-100 (default 60)
        skills_dir: Optional skills directory for metadata
        data_dir: Optional data directory for user preferences

    Returns:
        List of Recommendation objects sorted by confidence.

    Example:
        >>> recommendations = get_recommendations(top_n=3, min_confidence=70.0)
        >>> for rec in recommendations:
        ...     print(f"{rec.skill.name} ({rec.confidence:.1f}%): {rec.reasoning}")
        quick-test-runner (92.5%): Currently coding - 3 files modified
        diff-summariser (85.0%): Working with .py files - Review changes before committing
        dependency-audit (72.3%): Mature project (2+ years old) - Review dependency health
    """
    recommender = SkillRecommender(skills_dir=skills_dir, data_dir=data_dir)
    return recommender.recommend(top_n=top_n, min_confidence=min_confidence)


def record_feedback(
    skill_name: str,
    outcome: str,
    rating: Optional[int] = None,
    notes: str = "",
    data_dir: Optional[str] = None
) -> None:
    """
    Record feedback about skill usage.

    Feedback is used to personalize future recommendations by tracking
    which skills work well for the user and in what contexts.

    Args:
        skill_name: Name of skill that was used
        outcome: "success" or "failure"
        rating: Optional 1-5 star rating
        notes: Optional text notes about the experience
        data_dir: Optional data directory for storing feedback

    Example:
        >>> record_feedback(
        ...     "quick-test-runner",
        ...     "success",
        ...     rating=5,
        ...     notes="Found bugs quickly before committing"
        ... )
        >>> # Feedback recorded in data/feedback_history.json
        >>> # User preferences updated in data/preferences.json
    """
    analyzer = UserPatternAnalyzer(data_dir=data_dir)
    context_analyzer = ContextAnalyzer()
    context = context_analyzer.analyze()

    analyzer.record_feedback(
        skill=skill_name,
        context=context,
        outcome=outcome,
        rating=rating,
        notes=notes
    )


def get_recommendations_for_scenario(
    scenario: str,
    skills_dir: Optional[str] = None,
    data_dir: Optional[str] = None
) -> List[Recommendation]:
    """
    Get recommendations tailored to a specific scenario.

    Args:
        scenario: Scenario name ("new_project", "code_review", "debugging", "refactoring", "testing")
        skills_dir: Optional skills directory
        data_dir: Optional data directory

    Returns:
        List of Recommendation objects for the scenario.

    Example:
        >>> recommendations = get_recommendations_for_scenario("new_project")
        >>> for rec in recommendations:
        ...     print(f"- {rec.skill.name}: {rec.skill.description}")
        - lean-plan: Token-efficient planning mode for complex tasks
        - repo-briefing: Generate compact repository summaries
        - session-snapshot: Complete session context management
    """
    recommender = SkillRecommender(skills_dir=skills_dir, data_dir=data_dir)
    return recommender.recommend_for_scenario(scenario)


def analyze_current_context(working_dir: Optional[str] = None) -> ContextAnalysis:
    """
    Analyze the current working context.

    Args:
        working_dir: Optional working directory (defaults to current)

    Returns:
        ContextAnalysis object with current activity, file types, etc.

    Example:
        >>> context = analyze_current_context()
        >>> print(f"Activity: {context.current_activity}")
        Activity: coding
        >>> print(f"File types: {context.file_types}")
        File types: {'.py', '.md'}
        >>> print(f"Project type: {context.project_type}")
        Project type: python
    """
    analyzer = ContextAnalyzer(working_dir=working_dir)
    return analyzer.analyze()


def get_user_preferences(data_dir: Optional[str] = None) -> UserPreferences:
    """
    Load user preferences and feedback history.

    Args:
        data_dir: Optional data directory

    Returns:
        UserPreferences object with preferred skills, success rates, etc.

    Example:
        >>> prefs = get_user_preferences()
        >>> print(f"Preferred skills: {prefs.preferred_skills}")
        Preferred skills: {'quick-test-runner', 'diff-summariser'}
        >>> print(f"Complexity tolerance: {prefs.complexity_tolerance}")
        Complexity tolerance: high
    """
    analyzer = UserPatternAnalyzer(data_dir=data_dir)
    return analyzer.load_preferences()


# Convenience aliases
recommend = get_recommendations
feedback = record_feedback
