#!/usr/bin/env python3
"""
Example: Using the Skill Recommendation Engine library
This demonstrates how other skills can import and use the recommendation engine.
"""

import sys
from pathlib import Path

# Add parent directory to path for package imports
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

# Import the recommendation engine from lib subpackage
from lib import (
    get_recommendations,
    record_feedback,
    analyze_current_context,
    get_user_preferences
)


def main():
    print("=" * 70)
    print("Skill Recommendation Engine - Basic Usage Example")
    print("=" * 70)
    print()

    # Example 1: Analyze Current Context
    print(" Step 1: Analyzing current context...")
    print("-" * 70)
    context = analyze_current_context()
    print(f"Activity: {context.current_activity}")
    print(f"File types: {', '.join(sorted(context.file_types)) if context.file_types else 'None detected'}")
    print(f"Project type: {context.project_type}")
    print(f"Modified files: {len(context.recent_changes.get('modified', []))}")
    print(f"Token budget: {context.token_budget_remaining:,}")
    print()

    # Example 2: Get Recommendations
    print(" Step 2: Getting skill recommendations...")
    print("-" * 70)
    recommendations = get_recommendations(top_n=5, min_confidence=60.0)

    if not recommendations:
        print("No high-confidence recommendations at this time.")
        print("Try modifying some files or working in a git repository for better recommendations.")
        return

    print(f"Found {len(recommendations)} recommendations:\n")

    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec.skill.name}")
        print(f"   Category: {rec.category}")
        print(f"   Confidence: {rec.confidence:.1f}%")
        print(f"   Priority: {rec.skill.priority}")
        print(f"   Reasoning: {rec.reasoning}")
        print(f"   Description: {rec.skill.description}")
        print(f"   Token estimate: ~{rec.skill.token_estimate} tokens")
        print()

    # Example 3: Get User Preferences
    print(" Step 3: Checking user preferences...")
    print("-" * 70)
    prefs = get_user_preferences()
    print(f"Preferred skills: {', '.join(prefs.preferred_skills) if prefs.preferred_skills else 'None yet'}")
    print(f"Avoided skills: {', '.join(prefs.avoided_skills) if prefs.avoided_skills else 'None'}")
    print(f"Complexity tolerance: {prefs.complexity_tolerance}")
    print(f"Domain expertise: {', '.join(prefs.domain_expertise) if prefs.domain_expertise else 'None recorded'}")
    print()

    if prefs.skill_success_rates:
        print("Success rates:")
        for skill, rate in sorted(prefs.skill_success_rates.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {skill}: {rate*100:.0f}%")
        print()

    # Example 4: Record Feedback
    print(" Step 4: Recording feedback...")
    print("-" * 70)
    if recommendations:
        top_skill = recommendations[0].skill.name
        print(f"Recording positive feedback for '{top_skill}'...")

        record_feedback(
            skill_name=top_skill,
            outcome="success",
            rating=5,
            notes="Example feedback: Recommendation was helpful!"
        )

        print(f" Feedback recorded for {top_skill}")
        print("  This will improve future recommendations!")
    else:
        print("No recommendations to record feedback for.")
    print()

    # Example 5: Summary
    print(" Step 5: Recommendation Summary")
    print("-" * 70)
    if recommendations:
        print(f"Top recommendation: {recommendations[0].skill.name} ({recommendations[0].confidence:.1f}%)")
        print(f"Category distribution:")

        categories = {}
        for rec in recommendations:
            cat = rec.category
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1

        for cat, count in categories.items():
            print(f"  {cat}: {count} skill{'s' if count != 1 else ''}")

        avg_confidence = sum(r.confidence for r in recommendations) / len(recommendations)
        print(f"Average confidence: {avg_confidence:.1f}%")
    print()

    # Example 6: Usage Tips
    print(" Usage Tips")
    print("-" * 70)
    print(" Import from skill_recommendation_engine in your own skills")
    print(" Call get_recommendations() to get context-aware suggestions")
    print(" Use record_feedback() to improve recommendations over time")
    print(" Check preferences with get_user_preferences()")
    print(" Analyze context manually with analyze_current_context()")
    print()
    print("For more details, see README.md and lib/__init__.py")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
