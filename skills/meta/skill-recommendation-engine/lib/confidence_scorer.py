"""
Confidence Scoring System

Calculates recommendation confidence by combining:
- Context match (40 points)
- User pattern alignment (30 points)
- Project state relevance (20 points)
- Utility + success bonus (10 points)
"""

from typing import Optional

# Import data structures
try:
    from .skill_metadata import SkillMetadata
    from .context_analyzer import ContextAnalysis
    from .project_analyzer import ProjectState
    from .user_patterns import UserPreferences
    from .skill_utility import SkillUtility
except ImportError:
    # Fallback for standalone usage
    SkillMetadata = None
    ContextAnalysis = None
    ProjectState = None
    UserPreferences = None
    SkillUtility = None


class ConfidenceScorer:
    """Calculates confidence scores for skill recommendations."""

    def __init__(self):
        """Initialize confidence scorer."""
        pass

    def calculate_confidence(
        self,
        skill: any,
        context: any,
        project_state: Optional[any],
        user_prefs: Optional[any],
        skill_utility: Optional[any]
    ) -> float:
        """
        Calculate recommendation confidence (0-100).

        Args:
            skill: SkillMetadata object
            context: ContextAnalysis object
            project_state: ProjectState object (optional)
            user_prefs: UserPreferences object (optional)
            skill_utility: SkillUtility object (optional)

        Returns:
            Confidence score 0-100
        """
        # Context match (40 points max)
        context_score = self.analyze_context_relevance(skill, context) * 40

        # User pattern alignment (30 points max)
        pattern_score = 0.0
        if user_prefs:
            pattern_score = self.analyze_user_alignment(skill, user_prefs, context) * 30

        # Project state relevance (20 points max)
        state_score = 0.0
        if project_state:
            state_score = self.analyze_project_fit(skill, project_state) * 20

        # Utility + success bonus (10 points max)
        success_score = 0.0
        if skill_utility:
            success_score = skill_utility.reliability_score * 10

        total = context_score + pattern_score + state_score + success_score
        return min(100.0, max(0.0, total))

    def analyze_context_relevance(self, skill: any, context: any) -> float:
        """
        Analyze how relevant a skill is to the current context.

        Args:
            skill: SkillMetadata object
            context: ContextAnalysis object

        Returns:
            Score 0.0-1.0
        """
        score = 0.0

        skill_name = skill.name if hasattr(skill, 'name') else str(skill)
        skill_category = skill.category if hasattr(skill, 'category') else ""

        activity = context.current_activity if hasattr(context, 'current_activity') else "exploring"
        file_types = context.file_types if hasattr(context, 'file_types') else set()
        project_type = context.project_type if hasattr(context, 'project_type') else "unknown"
        token_budget = context.token_budget_remaining if hasattr(context, 'token_budget_remaining') else 150000

        # Activity-based matching
        if activity == "coding":
            if skill_name in ["quick-test-runner", "diff-summariser", "api-contract-sniffer"]:
                score += 0.3
        elif activity == "refactoring":
            if skill_name in ["dead-code-hunter", "refactoring", "dependency-audit"]:
                score += 0.3
        elif activity == "testing":
            if skill_name in ["quick-test-runner"]:
                score += 0.4

        # File type matching
        if ".v" in file_types:  # Coq formal verification
            if skill_category == "analysis/formal":
                score += 0.3
        elif ".qasm" in file_types or ".qpy" in file_types:  # Quantum
            if skill_name == "quantum-circuit-optimizer":
                score += 0.4
        elif ".py" in file_types or ".js" in file_types or ".ts" in file_types:
            if skill_name in ["api-contract-sniffer", "dead-code-hunter", "dependency-audit"]:
                score += 0.2

        # Token budget considerations
        if token_budget < 50000:  # Low budget
            if skill_name in ["lean-plan", "dependency-audit", "diff-summariser"]:
                score += 0.2

        # Project type alignment
        if project_type == "formal_verification":
            if skill_category == "analysis/formal":
                score += 0.2
        elif project_type == "quantum":
            if skill_name == "quantum-circuit-optimizer":
                score += 0.3
        elif project_type in ["web", "python", "javascript"]:
            if skill_name in ["quick-test-runner", "api-contract-sniffer", "dependency-audit"]:
                score += 0.1

        return min(1.0, score)

    def analyze_user_alignment(self, skill: any, user_prefs: any, context: any) -> float:
        """
        Analyze how well a skill aligns with user preferences.

        Args:
            skill: SkillMetadata object
            user_prefs: UserPreferences object
            context: ContextAnalysis object

        Returns:
            Score 0.0-1.0
        """
        score = 0.0

        skill_name = skill.name if hasattr(skill, 'name') else str(skill)
        skill_category = skill.category if hasattr(skill, 'category') else ""
        skill_priority = skill.priority if hasattr(skill, 'priority') else "medium"

        preferred = user_prefs.preferred_skills if hasattr(user_prefs, 'preferred_skills') else set()
        avoided = user_prefs.avoided_skills if hasattr(user_prefs, 'avoided_skills') else set()
        success_rates = user_prefs.skill_success_rates if hasattr(user_prefs, 'skill_success_rates') else {}
        complexity = user_prefs.complexity_tolerance if hasattr(user_prefs, 'complexity_tolerance') else "medium"
        expertise = user_prefs.domain_expertise if hasattr(user_prefs, 'domain_expertise') else set()

        # Preferred skills boost
        if skill_name in preferred:
            score += 0.4

        # Avoided skills penalty (strong negative signal)
        if skill_name in avoided:
            return 0.0

        # Success rate boost
        if skill_name in success_rates:
            score += success_rates[skill_name] * 0.3

        # Domain expertise match
        skill_domain = skill_category.split('/')[0] if '/' in skill_category else skill_category
        if skill_domain in expertise:
            score += 0.2

        # Complexity match
        if complexity == "low":
            # Prefer simple, high-priority skills
            if skill_priority == "high" and skill_name in ["quick-test-runner", "diff-summariser", "dependency-audit"]:
                score += 0.1
        elif complexity == "high":
            # Prefer complex analysis skills
            if skill_category.startswith("analysis/"):
                score += 0.1

        return min(1.0, score)

    def analyze_project_fit(self, skill: any, project_state: any) -> float:
        """
        Analyze how well a skill fits the project state.

        Args:
            skill: SkillMetadata object
            project_state: ProjectState object

        Returns:
            Score 0.0-1.0
        """
        score = 0.0

        skill_name = skill.name if hasattr(skill, 'name') else str(skill)

        repo_age = project_state.repository_age_days if hasattr(project_state, 'repository_age_days') else 0
        test_coverage = project_state.test_coverage_estimate if hasattr(project_state, 'test_coverage_estimate') else "medium"
        dep_count = project_state.dependency_count if hasattr(project_state, 'dependency_count') else 0
        doc_quality = project_state.documentation_quality if hasattr(project_state, 'documentation_quality') else "adequate"
        complexity = project_state.complexity_indicators if hasattr(project_state, 'complexity_indicators') else {}

        # Old repositories benefit from cleanup
        if repo_age > 365:  # > 1 year old
            if skill_name in ["dead-code-hunter", "dependency-audit", "refactoring"]:
                score += 0.4

        # Low test coverage
        if test_coverage == "low":
            if skill_name == "quick-test-runner":
                score += 0.3

        # High dependency count
        if dep_count > 50:
            if skill_name == "dependency-audit":
                score += 0.4
        elif dep_count > 20:
            if skill_name == "dependency-audit":
                score += 0.2

        # Poor documentation
        if doc_quality == "poor":
            if skill_name in ["repo-briefing", "session-snapshot"]:
                score += 0.3

        # High complexity
        large_files = complexity.get("large_files", 0) if isinstance(complexity, dict) else 0
        if large_files > 5:
            if skill_name in ["refactoring", "dead-code-hunter"]:
                score += 0.3

        return min(1.0, score)

    def get_confidence_category(self, confidence: float) -> str:
        """
        Categorize confidence score.

        Args:
            confidence: Confidence score 0-100

        Returns:
            Category string with emoji
        """
        if confidence >= 90:
            return "🎯 Immediate Needs"
        elif confidence >= 80:
            return "⚡ Quick Wins"
        elif confidence >= 70:
            return "🔍 Investigation Worthy"
        elif confidence >= 60:
            return "📈 Future Considerations"
        else:
            return "💡 Low Priority"
