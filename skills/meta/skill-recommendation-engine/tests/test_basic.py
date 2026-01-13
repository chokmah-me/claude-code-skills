"""
Basic tests for the skill recommendation engine.
"""

import sys
from pathlib import Path

# Add parent directory to path to allow package imports
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

from lib.skill_metadata import SkillMetadataLoader
from lib.context_analyzer import ContextAnalyzer
from lib.project_analyzer import ProjectAnalyzer
from lib.user_patterns import UserPatternAnalyzer
from lib.skill_utility import SkillUtilityScorer
from lib.confidence_scorer import ConfidenceScorer
from lib.recommender import SkillRecommender


def test_skill_metadata_loader():
    """Test skill metadata loading."""
    loader = SkillMetadataLoader()
    skills = loader.load_all_skills()

    assert len(skills) > 0, "Should load at least one skill"
    assert "quick-test-runner" in skills, "Should include quick-test-runner"

    skill = skills["quick-test-runner"]
    assert skill.name == "quick-test-runner"
    assert skill.priority == "high"
    assert skill.category == "development"
    print("[OK] test_skill_metadata_loader passed")


def test_context_analyzer():
    """Test context analysis."""
    analyzer = ContextAnalyzer()
    context = analyzer.analyze()

    assert hasattr(context, 'current_activity')
    assert hasattr(context, 'file_types')
    assert hasattr(context, 'project_type')
    assert context.token_budget_remaining > 0
    print("[OK] test_context_analyzer passed")


def test_project_analyzer():
    """Test project state analysis."""
    analyzer = ProjectAnalyzer()
    state = analyzer.analyze()

    assert hasattr(state, 'repository_age_days')
    assert hasattr(state, 'test_coverage_estimate')
    assert state.test_coverage_estimate in ["low", "medium", "high"]
    print("[OK] test_project_analyzer passed")


def test_user_patterns():
    """Test user pattern analyzer."""
    analyzer = UserPatternAnalyzer()
    prefs = analyzer.load_preferences()

    assert hasattr(prefs, 'preferred_skills')
    assert hasattr(prefs, 'skill_success_rates')
    assert prefs.complexity_tolerance in ["low", "medium", "high"]
    print("[OK] test_user_patterns passed")


def test_skill_utility():
    """Test skill utility scorer."""
    scorer = SkillUtilityScorer()
    utility = scorer.get_utility_score("quick-test-runner")

    assert 0.0 <= utility.frequency_of_need <= 1.0
    assert 0.0 <= utility.token_efficiency <= 1.0
    assert 0.0 <= utility.time_savings <= 1.0
    print("[OK] test_skill_utility passed")


def test_confidence_scorer():
    """Test confidence scoring."""
    scorer = ConfidenceScorer()
    loader = SkillMetadataLoader()
    analyzer = ContextAnalyzer()

    skill = loader.get_skill("quick-test-runner")
    context = analyzer.analyze()

    confidence = scorer.calculate_confidence(skill, context, None, None, None)

    assert 0.0 <= confidence <= 100.0
    print(f"[OK] test_confidence_scorer passed (confidence: {confidence:.1f}%)")


def test_recommender():
    """Test main recommender."""
    recommender = SkillRecommender()
    recommendations = recommender.recommend(top_n=5, min_confidence=0.0)

    assert isinstance(recommendations, list)
    assert len(recommendations) <= 5

    if recommendations:
        rec = recommendations[0]
        assert hasattr(rec, 'skill')
        assert hasattr(rec, 'confidence')
        assert hasattr(rec, 'reasoning')
        assert rec.confidence >= 0.0
        print(f"[OK] test_recommender passed ({len(recommendations)} recommendations)")
    else:
        print("[OK] test_recommender passed (no recommendations)")


def run_all_tests():
    """Run all tests."""
    print("Running basic tests...")
    print("=" * 60)

    tests = [
        test_skill_metadata_loader,
        test_context_analyzer,
        test_project_analyzer,
        test_user_patterns,
        test_skill_utility,
        test_confidence_scorer,
        test_recommender
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"[FAIL] {test.__name__} error: {e}")
            failed += 1

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
