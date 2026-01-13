"""
User Behavior Patterns Module

Manages user preferences, feedback history, and learning from user interactions.
Implements 20% weight of the recommendation algorithm.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Set, List, Optional, Any

# Import ContextAnalysis for type hinting
try:
    from .context_analyzer import ContextAnalysis
except ImportError:
    ContextAnalysis = Any  # Fallback for standalone usage


@dataclass
class UserPreferences:
    """Represents user preferences and learned patterns."""
    preferred_skills: Set[str] = field(default_factory=set)
    avoided_skills: Set[str] = field(default_factory=set)
    skill_success_rates: Dict[str, float] = field(default_factory=dict)
    complexity_tolerance: str = "medium"  # low, medium, high
    domain_expertise: Set[str] = field(default_factory=set)
    last_updated: str = ""


@dataclass
class FeedbackEntry:
    """Represents a single feedback entry."""
    timestamp: str
    skill: str
    context: Dict[str, Any]
    outcome: str  # success, failure
    user_rating: Optional[int] = None  # 1-5
    notes: str = ""


class UserPatternAnalyzer:
    """Analyzes and manages user behavior patterns."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize user pattern analyzer.

        Args:
            data_dir: Directory for storing user data.
                     Defaults to skills/meta/skill-recommendation-engine/data/
        """
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            # Auto-detect data directory
            self.data_dir = self._find_data_dir()

        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.preferences_file = self.data_dir / "preferences.json"
        self.feedback_file = self.data_dir / "feedback_history.json"

    def _find_data_dir(self) -> Path:
        """
        Find or create the data directory.

        Returns:
            Path to data directory.
        """
        # Try to find skill-recommendation-engine directory
        current = Path.cwd()

        # Check if we're already in the skill directory
        if (current / "SKILL.md").exists() and "recommendation" in current.name.lower():
            return current / "data"

        # Search for the skill in parent directories
        for parent in [current] + list(current.parents):
            skill_dir = parent / "skills" / "meta" / "skill-recommendation-engine"
            if skill_dir.exists():
                return skill_dir / "data"

        # Fallback: create in current directory
        return current / "data"

    def load_preferences(self) -> UserPreferences:
        """
        Load user preferences from storage.

        Returns:
            UserPreferences object with loaded data or defaults.
        """
        if not self.preferences_file.exists():
            return UserPreferences()

        try:
            with open(self.preferences_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            return UserPreferences(
                preferred_skills=set(data.get("preferred_skills", [])),
                avoided_skills=set(data.get("avoided_skills", [])),
                skill_success_rates=data.get("skill_success_rates", {}),
                complexity_tolerance=data.get("complexity_tolerance", "medium"),
                domain_expertise=set(data.get("domain_expertise", [])),
                last_updated=data.get("last_updated", "")
            )
        except (json.JSONDecodeError, IOError, Exception):
            return UserPreferences()

    def save_preferences(self, prefs: UserPreferences) -> None:
        """
        Save user preferences to storage.

        Args:
            prefs: UserPreferences object to save.
        """
        prefs.last_updated = datetime.utcnow().isoformat() + "Z"

        data = {
            "version": "1.0",
            "last_updated": prefs.last_updated,
            "preferred_skills": list(prefs.preferred_skills),
            "avoided_skills": list(prefs.avoided_skills),
            "skill_success_rates": prefs.skill_success_rates,
            "complexity_tolerance": prefs.complexity_tolerance,
            "domain_expertise": list(prefs.domain_expertise)
        }

        try:
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass  # Silently fail if can't write

    def load_feedback_history(self) -> List[FeedbackEntry]:
        """
        Load feedback history from storage.

        Returns:
            List of FeedbackEntry objects.
        """
        if not self.feedback_file.exists():
            return []

        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            entries = []
            for entry_data in data.get("feedback", []):
                entries.append(FeedbackEntry(
                    timestamp=entry_data["timestamp"],
                    skill=entry_data["skill"],
                    context=entry_data.get("context", {}),
                    outcome=entry_data.get("outcome", "unknown"),
                    user_rating=entry_data.get("user_rating"),
                    notes=entry_data.get("notes", "")
                ))
            return entries

        except (json.JSONDecodeError, IOError, Exception):
            return []

    def save_feedback_entry(self, entry: FeedbackEntry) -> None:
        """
        Save a new feedback entry.

        Args:
            entry: FeedbackEntry to save.
        """
        history = self.load_feedback_history()
        history.append(entry)

        data = {
            "version": "1.0",
            "feedback": [asdict(entry) for entry in history]
        }

        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def record_feedback(
        self,
        skill: str,
        context: Any,
        outcome: str,
        rating: Optional[int] = None,
        notes: str = ""
    ) -> None:
        """
        Record feedback about a skill usage.

        Args:
            skill: Skill name
            context: ContextAnalysis object (or dict for compatibility)
            outcome: "success" or "failure"
            rating: Optional 1-5 rating
            notes: Optional notes
        """
        # Convert context to dict if needed
        if hasattr(context, '__dict__'):
            context_dict = asdict(context) if hasattr(context, '__dataclass_fields__') else context.__dict__
            # Convert sets to lists for JSON serialization
            if 'file_types' in context_dict and isinstance(context_dict['file_types'], set):
                context_dict['file_types'] = list(context_dict['file_types'])
        else:
            context_dict = context if isinstance(context, dict) else {}

        # Create feedback entry
        entry = FeedbackEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            skill=skill,
            context=context_dict,
            outcome=outcome,
            user_rating=rating,
            notes=notes
        )

        # Save feedback
        self.save_feedback_entry(entry)

        # Update preferences based on feedback
        self._update_preferences_from_feedback(skill, outcome, rating)

    def _update_preferences_from_feedback(
        self,
        skill: str,
        outcome: str,
        rating: Optional[int]
    ) -> None:
        """
        Update user preferences based on new feedback.

        Args:
            skill: Skill name
            outcome: success or failure
            rating: Optional rating 1-5
        """
        prefs = self.load_preferences()

        # Update success rate
        if skill not in prefs.skill_success_rates:
            prefs.skill_success_rates[skill] = 0.5  # Start at neutral

        current_rate = prefs.skill_success_rates[skill]

        # Update based on outcome
        if outcome == "success":
            new_rate = current_rate * 0.8 + 0.2  # Move towards 1.0
        else:
            new_rate = current_rate * 0.8  # Move towards 0.0

        prefs.skill_success_rates[skill] = max(0.0, min(1.0, new_rate))

        # Update preferred/avoided based on rating
        if rating is not None:
            if rating >= 4:
                prefs.preferred_skills.add(skill)
                prefs.avoided_skills.discard(skill)
            elif rating <= 2:
                prefs.avoided_skills.add(skill)
                prefs.preferred_skills.discard(skill)

        self.save_preferences(prefs)

    def calculate_skill_affinity(self, skill: str, context: Optional[Any] = None) -> float:
        """
        Calculate user affinity for a skill.

        Args:
            skill: Skill name
            context: Optional ContextAnalysis for context-aware affinity

        Returns:
            Affinity score 0.0-1.0
        """
        prefs = self.load_preferences()
        score = 0.0

        # Check if in preferred skills
        if skill in prefs.preferred_skills:
            score += 0.3

        # Check if in avoided skills (strong negative signal)
        if skill in prefs.avoided_skills:
            return 0.0

        # Add success rate contribution
        if skill in prefs.skill_success_rates:
            score += prefs.skill_success_rates[skill] * 0.5

        # Context similarity bonus (if context provided)
        if context:
            history = self.load_feedback_history()
            similar_successes = sum(
                1 for entry in history
                if entry.skill == skill
                and entry.outcome == "success"
                and self._is_similar_context(entry.context, context)
            )
            if similar_successes > 0:
                score += min(0.2, similar_successes * 0.05)

        return min(1.0, score)

    def _is_similar_context(self, ctx1: Dict[str, Any], ctx2: Any) -> bool:
        """
        Check if two contexts are similar.

        Args:
            ctx1: Context dict from history
            ctx2: Current context

        Returns:
            True if contexts are similar.
        """
        # Simple similarity check
        if isinstance(ctx2, dict):
            ctx2_dict = ctx2
        elif hasattr(ctx2, '__dict__'):
            ctx2_dict = ctx2.__dict__
        else:
            return False

        # Check activity match
        if ctx1.get("current_activity") == ctx2_dict.get("current_activity"):
            return True

        # Check file type overlap
        ctx1_types = set(ctx1.get("file_types", []))
        ctx2_types = set(ctx2_dict.get("file_types", []))
        if ctx1_types and ctx2_types and len(ctx1_types & ctx2_types) > 0:
            return True

        return False

    def determine_complexity_tolerance(self) -> str:
        """
        Determine user's complexity tolerance from history.

        Returns:
            "low", "medium", or "high"
        """
        prefs = self.load_preferences()

        # If already set, return it
        if prefs.complexity_tolerance != "medium":
            return prefs.complexity_tolerance

        # Otherwise, infer from feedback history
        history = self.load_feedback_history()
        if not history:
            return "medium"

        # Check for complex skills usage
        complex_skills = {
            "skill-extractor", "refactoring", "lemma-dependency-graph",
            "anti-pattern-sniffer", "quantum-circuit-optimizer"
        }

        complex_successes = sum(
            1 for entry in history
            if entry.skill in complex_skills and entry.outcome == "success"
        )

        if complex_successes >= 3:
            return "high"
        elif complex_successes == 0 and len(history) > 5:
            return "low"
        else:
            return "medium"
