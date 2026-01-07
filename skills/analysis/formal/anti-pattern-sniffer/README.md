# Anti-Pattern Sniffer Skill - Usage Guide

## Overview

The `anti-pattern-sniffer` skill analyzes formal verification code (Coq, Lean, Isabelle) to detect proof anti-patterns, inefficient tactics, and structural issues that compromise proof quality and maintainability.

**Token Efficiency**: ~700 tokens vs ~2K manual review (65% reduction)

## Quick Start

### Natural Language Invocation
```
"Check my Coq proofs for anti-patterns"
"Sniff for inefficient proof tactics in Lean"
"Analyze this proof file for structural issues"
```

### Direct Skill Invocation
```
/anti-pattern-sniffer
```

## What It Detects

✅ **Tactical Anti-Patterns**:
- Overly complex tactic sequences
- Redundant tactic applications
- Inefficient automation usage
- Manual steps that could be automated

✅ **Structural Anti-Patterns**:
- Deep nesting without justification
- Poor lemma decomposition
- Inconsistent naming conventions
- Missing proof documentation

✅ **Logical Anti-Patterns**:
- Unnecessary case distinctions
- Redundant assumptions
- Overly specific proof steps
- Missing generalization opportunities

## Analysis Process

### Phase 1: Proof Structure Analysis
Parses proof scripts to understand:
- Lemma statements and types
- Proof block structure
- Tactic applications and sequencing
- Automation usage patterns

### Phase 2: Anti-Pattern Detection
Identifies common problematic patterns:
- Tactical complexity metrics
- Structural complexity analysis
- Automation effectiveness scoring
- Maintainability indicators

### Phase 3: Quality Assessment
Evaluates proof quality:
- Readability metrics
- Reusability potential
- Robustness indicators
- Performance implications

### Phase 4: Refactoring Suggestions
Provides improvement recommendations:
- Simplified tactic sequences
- Better structural organization
- Enhanced automation opportunities
- Documentation improvements

## Example Usage

### Example 1: Coq Proof Analysis
```
User: "Check this Coq proof for anti-patterns"

Claude: 🔍 Analyzing Coq proof for anti-patterns...

📊 Proof Analysis:
- File: proofs/list_theorems.v
- Lemmas analyzed: 8
- Total tactics: 234
- Analysis time: 1.8 seconds

🚨 Anti-Patterns Detected:

1. TACTICAL COMPLEXITY (High)
   Location: list_append_assoc (line 45-67)
   Pattern: 15-step manual induction
   Issue: Could use 'auto' or 'eauto'
   Suggestion: Replace with 'induction; auto with arith'
   Benefit: 80% reduction in proof size

2. REDUNDANT CASE ANALYSIS (Medium)
   Location: list_reverse_eq (line 89-112)
   Pattern: Unnecessary case distinction on empty list
   Issue: Cases could be unified
   Suggestion: Use 'destruct' with smarter case splitting
   Benefit: More maintainable proof

3. MISSING AUTOMATION (Medium)
   Location: Multiple lemmas
   Pattern: Manual application of basic lemmas
   Issue: Not leveraging 'auto' database
   Suggestion: Add lemmas to hint database
   Benefit: Faster proof checking

📈 Quality Metrics:
- Complexity score: 7.2/10 (needs improvement)
- Automation coverage: 45% (could be higher)
- Maintainability: 6.8/10 (moderate)
```

### Example 2: Lean Proof Optimization
```
User: "Analyze my Lean proofs for efficiency issues"

Claude: 🔍 Scanning Lean proofs for anti-patterns...

📋 Analysis Summary:
- Files analyzed: 3 Lean files
- Theorems: 15
- Proof steps: 412
- Processing time: 2.1 seconds

🎯 Key Anti-Patterns:

1. OVERLY SPECIFIC INDUCTION (Critical)
   Theorem: tree_balance_property
   Location: trees.lean:156-189
   Issue: Manual induction on tree structure
   Suggestion: Use 'induction' tactic with custom induction principle
   Impact: Proof becomes more general and reusable

2. DUPLICATION ACROSS PROOFS (High)
   Pattern: Similar case analysis in 6 different theorems
   Locations: trees.lean (multiple)
   Issue: No shared lemmas for common cases
   Suggestion: Extract common reasoning into helper lemmas
   Benefit: Reduces proof maintenance burden

3. INEFFICIENT AUTOMATION (Medium)
   Pattern: 'simp' with very long argument lists
   Locations: Throughout the codebase
   Issue: Poor automation strategy
   Suggestion: Create custom simp sets or use 'simp only'
   Performance: 30% faster proof checking

💡 Refactoring Recommendations:
1. Create shared lemma library for common patterns
2. Develop custom automation tactics
3. Implement consistent naming conventions
4. Add proof documentation and intuition
```

## Anti-Pattern Categories

### 🔴 Critical Issues
- unshelve admit without proof
- Admitted lemmas without documentation
- Circular proof dependencies
- Inconsistent axiom usage

### 🟡 High Impact
- Overly complex tactic sequences (>10 steps)
- Missing automation opportunities
- Poor lemma decomposition
- Inconsistent naming

### 🟢 Style Issues
- Inconsistent indentation
- Missing proof comments
- Suboptimal tactic choices
- Poor variable naming

## Supported Proof Systems

✅ **Primary Support**:
- Coq ( Gallina, Ltac, Ltac2)
- Lean 4
- Isabelle/HOL
- Agda

✅ **Tactical Analysis**:
- Tactic sequencing patterns
- Automation effectiveness
- Custom tactic evaluation
- Proof state analysis

⚠️ **Limited Support**:
- Custom proof languages
- Domain-specific automation
- Non-standard tactic systems

## Configuration Options

**Analysis Depth**:
- `--shallow`: Quick pattern detection
- `--deep`: Comprehensive analysis
- `--focus=theorem-name`: Analyze specific proofs

**Tolerance Levels**:
- `--strict`: Flag all anti-patterns
- `--moderate`: Focus on high-impact issues
- `--lenient`: Only critical problems

**Output Formats**:
- `--format=human`: Detailed explanations
- `--format=compact`: Summary only
- `--format=json`: Machine-readable

## Integration with Proof Development

**Pre-Commit Checks**:
```
1. Write initial proof
2. /anti-pattern-sniffer
3. Refactor based on suggestions
4. Finalize proof
```

**Code Review Process**:
```
1. Reviewer runs anti-pattern check
2. Identifies quality issues
3. Suggests improvements
4. Author refactors proof
```

**Continuous Integration**:
```
# Add to CI pipeline
/anti-pattern-sniffer --fail-on-critical
# Fails build if critical anti-patterns found
```

## Refactoring Workflow

### Step 1: Baseline Analysis
```
/anti-pattern-sniffer --format=detailed
# Get comprehensive quality report
```

### Step 2: Priority Assessment
```
Focus on critical and high-impact issues first
Address style issues during regular maintenance
```

### Step 3: Incremental Improvement
```
1. Fix one anti-pattern type at a time
2. Test proofs after changes
3. Document improvements made
4. Monitor for regressions
```

### Step 4: Quality Monitoring
```
Regular: /anti-pattern-sniffer --format=summary
Before releases: Full analysis with refactoring
```

## Common Anti-Patterns & Solutions

### Pattern 1: Manual Induction Overkill
**Issue**: 20+ step manual induction
**Solution**: Use automation or custom induction principles
**Example**: Replace with `induction; auto`

### Pattern 2: Tactic Soup
**Issue**: Long sequences of basic tactics
**Solution**: Create custom tactics or use automation
**Example**: Replace `intro; apply; assumption` with `eauto`

### Pattern 3: Missing Generalization
**Issue**: Overly specific proof steps
**Solution**: Generalize before proving
**Example**: Use `generalize dependent` appropriately

### Pattern 4: Poor Automation Strategy
**Issue**: Inefficient use of automation
**Solution**: Strategic automation with proper hints
**Example**: Build hint databases incrementally

## Best Practices

1. **Automation First**: Prefer automation over manual steps
2. **Lemma Extraction**: Create reusable helper lemmas
3. **Consistent Structure**: Use consistent proof organization
4. **Documentation**: Document proof intuition and strategy
5. **Regular Review**: Periodically review proof quality

## Performance Considerations

**Proof Checking Speed**:
- Complex tactics slow down checking
- Automation can improve or hinder performance
- Proper hint databases are crucial

**Maintainability**:
- Simple proofs are easier to modify
- Well-structured proofs support extension
- Good automation reduces brittleness

**Reusability**:
- General lemmas support multiple proofs
- Good abstraction enables proof reuse
- Consistent patterns aid understanding

## Token Efficiency

- Small proof (50 tactics): ~200 tokens
- Medium proof (200 tactics): ~400 tokens
- Large proof (500+ tactics): ~800 tokens
- Multi-file analysis: ~150 tokens per file

## Related Skills

- `analysis/formal/lemma-dependency-graph` - Visualize proof structure
- `analysis/formal/tactic-usage-count` - Analyze tactic patterns
- `analysis/formal/proof-obligations-snapshot` - Track remaining work
- `development/refactoring` - Restructure proofs safely

---

**Ready to improve your proofs?** Just tell Claude: "Check my proofs for anti-patterns" or "Analyze this proof for quality issues"!