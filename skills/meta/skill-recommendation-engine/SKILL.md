# Skill Recommendation Engine Meta-Skill

---
name: skill-recommendation-engine
description: Intelligent skill recommendation system that analyzes current context, user behavior, and project state to suggest the most useful Claude Code skills. Provides personalized, context-aware skill suggestions with usage predictions and confidence scores.
---

# Skill Recommendation Engine

## Purpose
Intelligently recommends the most useful Claude Code skills based on current context, project state, user behavior patterns, and skill utility analysis. Helps both users and agents discover relevant skills they might not know they need.

## When to Invoke
- When user asks: "What should I use for [task]?", "Help me choose", "What skill do I need?"
- When user seems stuck or asks for help without specifying skills
- When starting new types of work (new project, debugging, refactoring, etc.)
- When agent needs to determine optimal skill sequence for autonomous operation
- Proactively when context changes suggest skill opportunities

## Recommendation Algorithm

### Context Analysis (40% weight)
Analyzes current situation:
```python
def analyze_context():
    return {
        'current_activity': detect_current_work(),  # coding, debugging, reviewing, etc.
        'file_types': analyze_open_files(),         # .py, .js, .md, .v (Coq), etc.
        'recent_changes': get_git_status(),         # modified, added, deleted files
        'project_type': identify_project_type(),    # web, ml, formal, mobile, etc.
        'time_context': get_session_metadata(),     # time of day, session length
        'token_budget': estimate_remaining_tokens() # conservation needs
    }
```

### Project State Analysis (30% weight)
Evaluates project health and needs:
```python
def analyze_project_state():
    return {
        'repository_age': get_repo_age(),
        'test_coverage': estimate_test_coverage(),
        'code_complexity': analyze_complexity(),
        'dependency_health': check_dependencies(),
        'documentation_completeness': assess_docs(),
        'recent_activity': analyze_commit_patterns()
    }
```

### User Behavior Patterns (20% weight)
Learns from user history:
```python
def analyze_user_patterns():
    return {
        'preferred_skills': get_frequently_used(),
        'avoided_skills': get_rarely_used(),
        'success_rate': get_skill_success_rates(),
        'complexity_preference': determine_complexity_tolerance(),
        'domain_expertise': assess_domain_knowledge()
    }
```

### Skill Utility Scoring (10% weight)
Base utility scores from skill metadata:
```python
def get_skill_utility():
    return {
        'frequency_of_need': get_historical_usage(),
        'token_efficiency': get_token_savings(),
        'time_savings': get_time_reduction(),
        'success_probability': get_reliability_score(),
        'learning_curve': get_ease_of_use()
    }
```

## Recommendation Categories

### 🎯 Immediate Needs (90%+ confidence)
Skills that address current context directly:
- **Context**: "I just made code changes"
- **Recommendation**: `quick-test-runner`, `diff-summariser`
- **Confidence**: 95%
- **Reason**: "You modified 3 Python files - these skills will validate changes quickly"

### ⚡ Quick Wins (80-89% confidence)
High-value, low-effort skills:
- **Context**: Starting new project
- **Recommendation**: `lean-plan`, `repo-briefing`
- **Confidence**: 85%
- **Reason**: "New project with token constraints - lean planning will help manage budget"

### 🔍 Investigation Worthy (70-79% confidence)
Skills that might reveal important insights:
- **Context**: Legacy codebase
- **Recommendation**: `dead-code-hunter`, `dependency-audit`
- **Confidence**: 75%
- **Reason**: "8-year-old codebase likely has technical debt worth investigating"

### 📈 Future Considerations (60-69% confidence)
Skills for upcoming phases:
- **Context**: After successful refactoring
- **Recommendation**: `skill-extractor`, `session-snapshot`
- **Confidence**: 65%
- **Reason**: "You've successfully refactored - consider extracting this pattern for future use"

## Context-Specific Recommendations

### New Project Scenario
```
User: "Starting a new feature with limited tokens"

Context Analysis:
- Activity: New feature development
- Token budget: Constrained
- Project: Fresh start
- Recommendation confidence: 90%

Recommendations:
1. 🎯 lean-plan (95% confidence) - Token-efficient planning
   "Start with lean planning to manage your token budget effectively"

2. ⚡ repo-briefing (88% confidence) - Understand codebase
   "Get quick understanding of existing code structure and patterns"

3. 🎯 session-snapshot (85% confidence) - Save progress
   "Plan to save checkpoints for this multi-step feature development"

Alternative approaches if tokens run low:
- Use lean-plan with minimal scope
- Manual exploration instead of repo-briefing
- Save snapshots only at major milestones
```

### Code Changes Scenario
```
User: "I just made some changes to the authentication module"

Context Analysis:
- Activity: Code modification
- Files: auth/login.py, auth/middleware.py (modified)
- Git status: 2 files modified, 1 new file
- Recommendation confidence: 93%

Recommendations:
1. ⚡ quick-test-runner (96% confidence) - Fast validation
   "Validate your authentication changes with targeted tests"

2. ⚡ diff-summariser (92% confidence) - Review changes
   "Understand what you changed before proceeding"

3. 🔍 api-contract-sniffer (78% confidence) - Check API integrity
   "Ensure your auth changes don't break API contracts"

Priority: Test first, then review changes, then deeper analysis
```

### Code Quality Scenario
```
User: "This codebase feels messy, want to improve it"

Context Analysis:
- Project age: 5 years
- Complexity: High (average cyclomatic: 24)
- Test coverage: 45% (low)
- Dependencies: 12 high-severity CVEs
- Recommendation confidence: 88%

Recommendations:
1. 🔍 dead-code-hunter (90% confidence) - Find cleanup opportunities
   "Identify unused code that's contributing to messiness"

2. 🔍 dependency-audit (87% confidence) - Security & updates
   "Address security vulnerabilities in dependencies"

3. 🛠️ refactoring (82% confidence) - Systematic improvement
   "Plan safe refactoring to reduce complexity"

4. 🔍 api-contract-sniffer (75% confidence) - API consistency
   "Ensure API consistency during cleanup"

Strategy: Start with cleanup, then security, then structural improvements
```

### Formal Verification Scenario
```
User: "Working on Coq proofs for my verification project"

Context Analysis:
- File types: .v files (Coq)
- Activity: Proof development
- Recent: Multiple proof attempts
- Recommendation confidence: 85%

Recommendations:
1. 🔍 anti-pattern-sniffer (88% confidence) - Proof quality
   "Check your Coq proofs for common anti-patterns"

2. 🔍 lemma-dependency-graph (85% confidence) - Proof structure
   "Understand dependencies between your lemmas"

3. 🔍 proof-obligations-snapshot (80% confidence) - Track progress
   "Snapshot remaining proof obligations for tracking"

4. 🔍 tactic-usage-count (75% confidence) - Optimize proofs
   "Analyze tactic usage for performance optimization"

Note: These are specialized for formal verification work
```

## Interactive Recommendation Process

### Initial Assessment
```
User: "What should I use?"

Claude: 🤔 Let me analyze your current situation...

📊 Context Analysis:
- Current activity: Code modification detected
- Recent files: 3 Python files modified
- Git status: Working directory has changes
- Token budget: Adequate (estimated 8000 remaining)

🎯 Top Recommendations (90%+ confidence):

1. ⚡ quick-test-runner
   Validate your changes before proceeding
   Confidence: 94% | Tokens: ~300 | Time: ~30s
   
2. ⚡ diff-summariser  
   Review what you changed quickly
   Confidence: 91% | Tokens: ~400 | Time: ~20s

3. 🎯 session-snapshot
   Save state before major testing
   Confidence: 87% | Tokens: ~400 | Time: ~15s

💡 Quick start: "Run quick tests" or "/quick-test-runner"
```

### Follow-up Refinement
```
User: "What about security?"

Claude: 🔒 Adding security-focused recommendations...

Updated Analysis:
- User interest: Security added to requirements
- Context: Authentication code changes
- Priority adjustment: Security elevated

🔐 Security-Focused Recommendations:

1. 🔍 api-contract-sniffer (85% confidence)
   "Check API contracts for security issues"
   Validates authentication endpoints are secure

2. 🔍 dependency-audit (80% confidence)
   "Audit dependencies for vulnerabilities"
   Check for known CVEs in auth dependencies

3. 🔍 dead-code-hunter (75% confidence)
   "Find unused authentication code"
   Remove potentially vulnerable dead code

Security strategy: Contract validation → Dependency check → Cleanup
```

### Autonomous Agent Recommendations
```
Agent: "Planning autonomous operation sequence"

Claude: 🤖 Agent Skill Sequence Recommendation:

🎯 Autonomous Operation Plan:
1. /repo-briefing (understand codebase)
2. /lean-plan (plan within token budget)
3. /session-snapshot (save progress checkpoints)
4. [task-specific skills based on goal]
5. /skill-extractor (formalize successful patterns)

📊 Confidence Matrix:
- repo-briefing: 95% (essential for context)
- lean-plan: 92% (token management critical)
- session-snapshot: 89% (progress preservation)
- skill-extractor: 85% (pattern learning)

🔄 Adaptive Triggers:
- If token budget <2000: Switch to ultra-lean mode
- If complexity high: Add analysis skills
- If security context: Add security skills
- If formal verification: Add proof skills

Machine-readable format: "Recommend skills for autonomous operation"
```

## Confidence Scoring System

### Confidence Calculation
```python
def calculate_confidence(skill, context):
    base_score = skill.utility_score  # 0-100
    
    # Context match (0-40 points)
    context_match = analyze_context_relevance(skill, context) * 40
    
    # User pattern alignment (0-30 points)  
    pattern_match = analyze_user_alignment(skill, context) * 30
    
    # Project state relevance (0-20 points)
    state_match = analyze_project_fit(skill, context) * 20
    
    # Historical success (0-10 points)
    success_bonus = skill.historical_success_rate * 10
    
    return min(100, base_score + context_match + pattern_match + state_match + success_bonus)
```

### Confidence Levels
- **90-100%**: Near certainty - use immediately
- **80-89%**: High confidence - strongly recommend
- **70-79%**: Good confidence - worth considering
- **60-69%**: Moderate confidence - investigate further
- **<60%**: Low confidence - mention as possibility

## Personalization Features

### Learning from Feedback
```python
def process_feedback(skill, outcome, user_rating):
    # Update skill success rate
    skill.historical_success_rate = calculate_new_average(
        skill.historical_success_rate, 
        outcome.success, 
        user_rating
    )
    
    # Update user preferences
    if user_rating > 4:  # Liked
        user.preferred_skills.add(skill)
    elif user_rating < 3:  # Disliked
        user.avoided_skills.add(skill)
    
    # Update context patterns
    user.pattern_recognizer.update(context_snapshot, skill, outcome)
```

### Adaptive Recommendations
Personalize over time:
- Learn preferred complexity levels
- Adapt to domain expertise
- Adjust for token budget preferences
- Customize for work patterns

## Advanced Features

### Predictive Recommendations
Anticipate future needs:
- Based on project lifecycle stage
- Seasonal/temporal patterns
- Technology adoption curves
- Team development phases

### Collaborative Filtering
Team-based recommendations:
- Similar users' preferences
- Team skill adoption patterns
- Organizational standards
- Peer success rates

### A/B Testing
Continuous improvement:
- Test different recommendation strategies
- Measure engagement and success
- Optimize algorithms based on data
- Evolve recommendation quality

## Best Practices

### 1. Transparent Reasoning
Always explain why:
- Show confidence levels
- Provide clear rationale
- Explain trade-offs
- Offer alternatives

### 2. Respect User Autonomy
Support informed choice:
- Present options clearly
- Allow easy override
- Learn from feedback
- Adapt to preferences

### 3. Progressive Disclosure
Layer information appropriately:
- Start with top recommendations
- Offer more details on request
- Provide deeper analysis when needed
- Maintain clarity throughout

### 4. Continuous Learning
Improve over time:
- Track recommendation success
- Learn from user feedback
- Adapt to changing patterns
- Evolve with experience

## Success Metrics

### Recommendation Quality
Measure effectiveness:
- Acceptance rate: % of recommendations used
- Success rate: % that achieve desired outcome
- User satisfaction: Rating of recommendations
- Time to value: Speed of positive results

### User Experience
Assess satisfaction:
- Ease of discovery
- Clarity of explanations
- Relevance of suggestions
- Overall helpfulness

### System Performance
Monitor efficiency:
- Recommendation speed
- Accuracy of predictions
- Resource usage
- Scalability

---

**Ready for intelligent skill recommendations?** This engine will help you and agents discover the perfect Claude Code skills for any situation!