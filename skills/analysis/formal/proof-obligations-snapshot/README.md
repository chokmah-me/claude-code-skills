# Proof Obligations Snapshot Skill - Usage Guide

## Overview

The `proof-obligations-snapshot` skill captures and analyzes remaining proof obligations in formal verification projects. Tracks progress, identifies bottlenecks, and provides insights for completing large-scale verification efforts.

**Token Efficiency**: ~500 tokens vs ~1.5K manual tracking (65% reduction)

## Quick Start

### Natural Language Invocation
```
"What's left to prove in my project?"
"Show me remaining proof obligations"
"Track progress on my verification effort"
```

### Direct Skill Invocation
```
/proof-obligations-snapshot
```

## What It Tracks

✅ **Proof Obligations**:
- Admitted lemmas without proofs
- Proof sketches marked "TODO"
- Axioms used without justification
- Incomplete case analyses

✅ **Progress Metrics**:
- Total vs completed proofs
- Proof complexity distribution
- Estimated remaining effort
- Completion timeline projections

✅ **Quality Indicators**:
- Proof obligation criticality
- Dependency impact analysis
- Risk assessment for remaining work
- Priority suggestions

## Analysis Process

### Phase 1: Obligation Discovery
Finds all unfinished proofs:
- Admitted lemmas (`Admitted.`)
- Proof sketches (`Proof. (* TODO *)`)
- Axiom dependencies
- Incomplete sections

### Phase 2: Impact Analysis
Analyzes obligation importance:
- Dependency graph analysis
- Critical path identification
- Usage frequency analysis
- Blocking relationship assessment

### Phase 3: Effort Estimation
Estimates completion effort:
- Complexity analysis
- Historical data comparison
- Similar proof identification
- Developer experience factors

### Phase 4: Progress Tracking
Tracks completion status:
- Snapshot comparisons
- Trend analysis
- Burndown projections
- Milestone tracking

## Example Usage

### Example 1: Project Status Check
```
User: "What's the status of proof obligations in my project?"

Claude: 📊 Taking snapshot of proof obligations...

📈 Proof Obligations Status:
- Project: Abstract Algebra Library
- Files analyzed: 12 Coq files
- Total lemmas: 156
- Completed proofs: 134 (86%)
- Remaining obligations: 22
- Analysis time: 2.1 seconds

🎯 Remaining Proof Obligations:

HIGH PRIORITY (5 obligations):
1. Lemma: group_theory_associativity
   File: algebra/group_theory.v:234
   Type: Admitted (no proof)
   Dependencies: 12 other lemmas
   Estimated effort: 4-6 hours
   Blocker: Yes (critical for group theory)
   
2. Lemma: ring_homomorphism_properties
   File: algebra/ring_theory.v:189
   Type: Proof sketch (50% complete)
   Dependencies: 8 lemmas
   Estimated effort: 2-3 hours
   Strategy: Follow similar homomorphism patterns

MEDIUM PRIORITY (8 obligations):
3. Lemma: field_extension_uniqueness
   File: algebra/field_theory.v:345
   Type: Admitted
   Dependencies: 5 lemmas
   Estimated effort: 3-4 hours
   Notes: Requires Galois theory knowledge

LOW PRIORITY (9 obligations):
12. Lemma: auxiliary_inequality_7
    File: utils/inequalities.v:123
    Type: Proof sketch (20% complete)
    Dependencies: None
    Estimated effort: 30 minutes
    Notes: Utility lemma, not blocking

📊 Progress Analysis:
- Completion rate: 86% (good)
- Critical path items: 5 (need attention)
- Estimated completion: 25-30 hours
- Trend: +3% this week (steady progress)
```

### Example 2: Sprint Planning Support
```
User: "Help me plan the next sprint for proof completion"

Claude: 📋 Analyzing proof obligations for sprint planning...

🎯 Sprint Planning Recommendations:

WEEK 1 (High Priority):
- Target: Complete 3 critical obligations
- Focus: group_theory_associativity, ring_homomorphism_properties
- Estimated effort: 12-15 hours
- Success criteria: Unblocks 20 dependent lemmas

WEEK 2 (Medium Priority):
- Target: Complete 4 medium obligations
- Focus: field_extension_uniqueness, polynomial_factorization
- Estimated effort: 10-12 hours
- Success criteria: Completes core algebraic structures

WEEK 3 (Cleanup):
- Target: Complete 8 low-priority obligations
- Focus: Auxiliary lemmas and utilities
- Estimated effort: 6-8 hours
- Success criteria: 95% overall completion

📊 Risk Assessment:
- High-risk items: 2 (require domain expertise)
- Medium-risk: 5 (standard complexity)
- Low-risk: 15 (straightforward)
- External dependencies: None

💡 Resource Allocation:
- Senior developer: 60% (high-priority items)
- Mid-level developer: 30% (medium-priority)
- Junior developer: 10% (low-priority, with guidance)
```

### Example 3: Historical Progress Tracking
```
User: "Show me progress over the past month"

Claude: 📈 Analyzing proof obligation trends...

📊 Monthly Progress Report:

WEEK 4 (Current):
- Total obligations: 22
- Completed this week: 3
- Added this week: 1
- Net progress: -2

WEEK 3:
- Total obligations: 24
- Completed: 4
- Added: 2
- Net progress: -2

WEEK 2:
- Total obligations: 26
- Completed: 5
- Added: 0
- Net progress: -5

WEEK 1:
- Total obligations: 31
- Completed: 6
- Added: 1
- Net progress: -5

📈 Trend Analysis:
- Starting obligations: 31
- Current obligations: 22
- Monthly progress: -29%
- Average completion rate: 4.5 obligations/week

🎯 Velocity Insights:
- Consistent completion rate maintained
- New obligations being added (good sign - active development)
- On track for completion in 5-6 weeks
- Quality remains high (no major rework needed)

💡 Recommendations:
1. Maintain current velocity
2. Focus on high-priority items first
3. Consider parallel development for independent obligations
4. Schedule regular reviews to prevent technical debt
```

## Obligation Types

### 🔴 Critical Obligations
- Foundational lemmas blocking many others
- Core theoretical results
- Axioms requiring validation
- Security-critical properties

### 🟡 Standard Obligations
- Regular lemmas with moderate complexity
- Well-defined proof strategies
- Standard theoretical results
- Manageable proof effort

### 🟢 Utility Obligations
- Auxiliary lemmas
- Helper results
- Optimization properties
- Convenience definitions

## Priority Assessment

### Dependency Impact
High priority if many other lemmas depend on it:
```
Critical lemma → blocks 15 other proofs
Standard lemma → blocks 3 other proofs
Utility lemma → blocks 0 other proofs
```

### Theoretical Importance
Core theoretical results get higher priority:
- Fundamental properties
- Key structural results
- Main theorems of sections
- Foundation for future work

### Effort vs Value
Balance proof effort against theoretical value:
- High-value, low-effort: Do immediately
- High-value, high-effort: Plan carefully
- Low-value, low-effort: Fill in gaps
- Low-value, high-effort: Consider postponing

## Configuration Options

**Analysis Scope**:
- `--file=specific.v`: Analyze single file
- `--project-wide`: Full project analysis
- `--since=date`: Obligations since date

**Priority Filtering**:
- `--critical-only`: Show only critical items
- `--high-priority`: High and critical
- `--all`: Show all obligations

**Output Control**:
- `--format=summary`: Brief overview
- `--format=detailed`: Full analysis
- `--format=planning`: Sprint planning view

## Integration with Development

**Daily Development**:
```
1. Start session: /proof-obligations-snapshot
2. Pick 1-2 obligations to work on
3. Complete proofs
4. Update snapshot
```

**Team Coordination**:
```
1. Weekly team sync with obligation snapshot
2. Assign obligations based on expertise
3. Track progress collaboratively
4. Adjust priorities as needed
```

**Release Planning**:
```
1. Snapshot before release cycles
2. Plan obligation completion
3. Allocate resources appropriately
4. Monitor progress to deadlines
```

## Progress Tracking

### Burndown Charts
Visualize completion over time:
```
Week 1: 31 obligations
Week 2: 26 obligations  (-5)
Week 3: 22 obligations  (-4)
Week 4: 18 obligations  (-4)
```

### Velocity Metrics
Track completion rate:
- Obligations per week
- Hours per obligation
- Success rate
- Rework percentage

### Quality Metrics
Ensure proof quality:
- Proof complexity scores
- Review requirements
- Validation success
- Documentation completeness

## Best Practices

1. **Regular Snapshots**: Track progress consistently
2. **Priority Focus**: Work on high-impact obligations first
3. **Effort Estimation**: Improve estimation accuracy over time
4. **Team Coordination**: Use for planning and coordination
5. **Quality Maintenance**: Don't sacrifice quality for speed

## Common Challenges

### Challenge 1: Underestimating Effort
**Solution**: Track actual vs estimated time, adjust future estimates

### Challenge 2: Priority Changes
**Solution**: Regular priority review with stakeholders

### Challenge 3: New Obligations Added
**Solution**: Track addition rate, plan for ongoing work

### Challenge 4: Technical Debt
**Solution**: Balance new obligations with completing existing ones

## Success Criteria

**Completion Metrics**:
- >95% obligations completed
- Zero critical obligations remaining
- All high-priority obligations addressed
- Quality standards maintained

**Process Metrics**:
- Consistent progress tracking
- Accurate effort estimation
- Effective team coordination
- Stakeholder satisfaction

## Token Efficiency

- Small project (50 lemmas): ~200 tokens
- Medium project (200 lemmas): ~400 tokens
- Large project (1000+ lemmas): ~800 tokens
- Historical analysis: +100 tokens per time period

## Related Skills

- `analysis/formal/lemma-dependency-graph` - Understand proof structure
- `analysis/formal/anti-pattern-sniffer` - Ensure proof quality
- `analysis/formal/tactic-usage-count` - Analyze proof patterns
- `development/refactoring` - Restructure proofs efficiently

---

**Ready to track your progress?** Just tell Claude: "Show my proof obligations" or "Track verification progress"!