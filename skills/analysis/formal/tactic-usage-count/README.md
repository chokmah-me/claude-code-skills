# Tactic Usage Count Skill - Usage Guide

## Overview

The `tactic-usage-count` skill analyzes formal verification code to identify tactic usage patterns, performance bottlenecks, and optimization opportunities. Provides insights for improving proof efficiency and maintainability.

**Token Efficiency**: ~400 tokens vs ~1.2K manual analysis (65% reduction)

## Quick Start

### Natural Language Invocation
```
"Analyze tactic usage in my Coq proofs"
"Show me which tactics I use most often"
"Identify performance bottlenecks in my Lean proofs"
```

### Direct Skill Invocation
```
/tactic-usage-count
```

## What It Analyzes

✅ **Usage Statistics**:
- Tactic frequency counts
- Tactic sequence patterns
- Automation effectiveness
- Performance timing data

✅ **Pattern Recognition**:
- Common tactic sequences
- Inefficient patterns
- Redundant applications
- Optimization opportunities

✅ **Performance Insights**:
- Slow-performing tactics
- Memory usage patterns
- Proof checking speed
- Automation bottlenecks

## Analysis Process

### Phase 1: Tactic Extraction
Identifies all tactic usage:
- Tactic names and arguments
- Application contexts
- Sequence relationships
- Performance characteristics

### Phase 2: Statistical Analysis
Computes usage statistics:
- Frequency distributions
- Pattern frequencies
- Performance metrics
- Success/failure rates

### Phase 3: Pattern Recognition
Identifies common patterns:
- Frequent sequences
- Inefficient combinations
- Redundant applications
- Automation opportunities

### Phase 4: Optimization Suggestions
Provides improvement recommendations:
- Performance optimizations
- Simplification opportunities
- Automation strategies
- Best practice suggestions

## Example Usage

### Example 1: Basic Tactic Analysis
```
User: "Analyze tactic usage in my proof file"

Claude: 🔍 Analyzing tactic usage patterns...

📊 Tactic Usage Statistics:
- File: proofs/basic_logic.v
- Total tactics: 234
- Unique tactics: 18
- Analysis time: 0.8 seconds

📈 Most Used Tactics:
1. 'intros' - 45 times (19.2%)
2. 'apply' - 38 times (16.2%)
3. 'simpl' - 31 times (13.2%)
4. 'rewrite' - 27 times (11.5%)
5. 'reflexivity' - 19 times (8.1%)

🎯 Tactic Sequences:
1. 'intros; apply' - 12 occurrences
2. 'simpl; rewrite' - 8 occurrences
3. 'destruct; intros' - 6 occurrences

⚠️ Potential Issues:
1. Tactic: 'simpl'
   Usage: 31 times
   Issue: May cause unnecessary computation
   Suggestion: Use 'cbn' or 'lazy' for better control
   
2. Pattern: 'apply assumption'
   Usage: 15 times
   Issue: Could use 'assumption' directly
   Suggestion: Replace with single 'assumption'

💡 Optimization Opportunities:
1. Create custom tactic for 'intros; apply' sequence
2. Use 'auto' for simple applications
3. Optimize 'simpl' usage with targeted reduction
```

### Example 2: Performance-Focused Analysis
```
User: "Find performance bottlenecks in my tactics"

Claude: 🔍 Scanning for tactic performance issues...

📋 Performance Analysis:
- Proofs analyzed: 12
- Total tactic applications: 567
- Slow tactics identified: 3
- Memory-intensive patterns: 2

🐌 Performance Bottlenecks:

1. Tactic: 'simpl' with complex terms
   Occurrences: 23
   Average time: 2.3 seconds
   Issue: Excessive computation on large terms
   Solution: Use 'cbn -[list_of_terms]' to skip expensive reduction
   Expected improvement: 80% faster

2. Tactic: 'rewrite' with many occurrences
   Pattern: 'rewrite lemma1, lemma2, ..., lemma8'
   Occurrences: 8
   Average time: 1.8 seconds
   Issue: Multiple rewrites in sequence
   Solution: Use 'rewrite !lemma1 !lemma2 ...' or create composite lemma
   Expected improvement: 60% faster

3. Tactic: 'auto' with large hint database
   Occurrences: 15
   Average time: 1.2 seconds
   Issue: Searching large hint space
   Solution: Use 'auto with specific_db' or 'eauto'
   Expected improvement: 50% faster

💾 Memory Usage Patterns:
1. Pattern: Repeated 'pose proof' without cleanup
   Issue: Accumulates proof context
   Solution: Use 'assert' or clean up with 'clear'
   
2. Pattern: Large term construction in tactics
   Issue: Builds complex terms repeatedly
   Solution: Use 'set' to name and reuse terms

📈 Optimization Potential:
- Total time reduction: 65%
- Memory usage improvement: 40%
- Proof checking speed: 3x faster
```

### Example 3: Automation Strategy Analysis
```
User: "How can I improve my automation strategy?"

Claude: 🤖 Analyzing automation opportunities...

📊 Automation Analysis:
- Manual tactics: 78% of total
- Semi-automated: 15% of total
- Fully automated: 7% of total
- Potential for automation: High

🎯 Automation Opportunities:

1. Pattern: 'intros; apply H; assumption'
   Occurrences: 24
   Current: Manual 3-step process
   Suggestion: Create 'auto_apply H' tactic
   Implementation: 'Ltac auto_apply H := intros; apply H; assumption.'
   Benefit: 24 lines → 1 line per usage

2. Pattern: 'induction n; [simpl; reflexivity | simpl; rewrite IHn]'
   Occurrences: 18
   Current: Repetitive induction patterns
   Suggestion: Create 'induct_solve' tactic
   Implementation: Custom induction with built-in simplification
   Benefit: Consistent automation, fewer errors

3. Pattern: 'destruct (eq_dec x y); [subst; auto | auto]'
   Occurrences: 31
   Current: Manual case analysis
   Suggestion: Use 'decide equality' automation
   Benefit: More robust, handles all cases

🔧 Custom Tactic Recommendations:

1. 'solve_base_case': Automated base case handling
2. 'solve_inductive_step': Standardized inductive steps
3. 'auto_equiv': Automated equivalence proofs
4. 'auto_inequality': Automated inequality reasoning

📈 Expected Improvements:
- Manual tactics reduced: 78% → 35%
- Proof size reduction: 40%
- Development speed: 2x faster
- Error rate: 60% reduction

💡 Implementation Strategy:
1. Start with most frequent patterns
2. Build custom tactic library incrementally
3. Test automation thoroughly
4. Document automation patterns
```

## Tactic Categories

### 🔧 Basic Tactics
Fundamental proof steps:
- `intros`, `apply`, `assumption`
- `simpl`, `cbn`, `unfold`
- `destruct`, `induction`, `case`

### ⚙️ Automation Tactics
Automated reasoning:
- `auto`, `eauto`, `trivial`
- `tauto`, `intuition`
- `omega`, `lia`, `nia`

### 🎯 Advanced Tactics
Specialized operations:
- `rewrite`, `setoid_rewrite`
- `pattern`, `change`
- `pose`, `set`, `remember`

### 🔍 Search Tactics
Goal-directed search:
- `eapply`, `eassumption`
- `exists`, `split`
- `left`, `right`

## Analysis Dimensions

### Usage Frequency
How often tactics are used:
```
High frequency: >20 times per file
Medium frequency: 5-20 times per file
Low frequency: <5 times per file
```

### Performance Impact
Effect on proof checking:
```
Fast: <0.1 seconds
Medium: 0.1-1.0 seconds
Slow: >1.0 seconds
```

### Success Rate
Effectiveness in completing goals:
```
High: >90% success rate
Medium: 70-90% success rate
Low: <70% success rate
```

## Pattern Recognition

### Common Sequences
Frequently occurring patterns:
```
'intros; apply' - Introduction and application
'simpl; rewrite' - Simplification and rewriting
'destruct; intros' - Case analysis and introduction
```

### Inefficient Patterns
Suboptimal combinations:
```
'apply H; assumption' - Could use 'eapply'
'rewrite H; reflexivity' - Could use 'rewrite -> H'
'simpl; cbn' - Redundant simplification
```

### Redundant Applications
Unnecessary repetitions:
```
Multiple 'simpl' in sequence
Repeated 'intros' without new hypotheses
'apply' followed immediately by 'assumption'
```

## Optimization Strategies

### Tactic Simplification
Replace complex sequences:
```
Before: intros; apply H; assumption
After: eauto with H
```

### Performance Optimization
Improve speed:
```
Before: simpl (full reduction)
After: cbn -[expensive_operations]
```

### Automation Enhancement
Increase automation:
```
Before: Manual case analysis
After: 'decide equality' or 'auto'
```

## Configuration Options

**Analysis Focus**:
- `--performance`: Focus on speed issues
- `--automation`: Find automation opportunities
- `--patterns`: Analyze sequence patterns

**Scope Control**:
- `--file=specific.v`: Single file analysis
- `--project-wide`: Full project scan
- `--since=date`: Changes since date

**Output Control**:
- `--format=detailed`: Full analysis
- `--format=summary`: Key findings only
- `--format=commands`: Generate tactic definitions

## Integration with Development

**Proof Development**:
```
1. Write initial proof
2. /tactic-usage-count (analyze patterns)
3. Optimize based on suggestions
4. Compare before/after performance
```

**Code Review**:
```
1. Reviewer runs usage analysis
2. Checks for inefficient patterns
3. Suggests optimization opportunities
4. Author implements improvements
```

**Performance Tuning**:
```
1. Baseline: /tactic-usage-count --performance
2. Identify bottlenecks
3. Implement optimizations
4. Measure improvement
```

## Best Practices

### Efficient Tactic Usage
1. **Prefer Automation**: Use `auto` family when possible
2. **Targeted Simplification**: Use specific reduction strategies
3. **Batch Operations**: Combine related operations
4. **Avoid Redundancy**: Don't repeat unnecessary steps

### Performance Optimization
1. **Profile First**: Identify actual bottlenecks
2. **Target Expensive Operations**: Focus on slow tactics
3. **Use Incremental Approach**: Optimize gradually
4. **Test Thoroughly**: Ensure correctness preserved

### Automation Strategy
1. **Start Simple**: Begin with basic automation
2. **Build Gradually**: Develop custom tactics incrementally
3. **Document Patterns**: Record successful automation
4. **Share Knowledge**: Team-wide automation standards

## Performance Metrics

### Speed Improvements
- Tactic execution time
- Proof checking speed
- Interactive response time
- Batch processing performance

### Size Reductions
- Proof script size
- Number of tactic applications
- Memory usage during proofs
- Storage requirements

### Quality Improvements
- Error rate reduction
- Consistency improvements
- Maintainability enhancement
- Reusability increase

## Common Issues & Solutions

### Issue 1: Slow simplification
**Solution**: Use targeted reduction with `cbn` or `lazy`

### Issue 2: Inefficient rewriting
**Solution**: Batch rewrites or use `rewrite_strat`

### Issue 3: Poor automation results
**Solution**: Build custom hint databases

### Issue 4: Memory usage spikes
**Solution**: Clean up hypotheses with `clear`

## Token Efficiency

- Single file analysis: ~200 tokens
- Medium project: ~400 tokens
- Large project: ~800 tokens
- Optimization suggestions: +150 tokens

## Related Skills

- `analysis/formal/anti-pattern-sniffer` - Detect proof quality issues
- `analysis/formal/lemma-dependency-graph` - Understand proof structure
- `analysis/formal/proof-obligations-snapshot` - Track remaining work
- `development/refactoring` - Optimize proofs systematically

---

**Ready to optimize your tactics?** Just tell Claude: "Analyze my tactic usage" or "Find performance bottlenecks in my proofs"!