# Lemma Dependency Graph Skill - Usage Guide

## Overview

The `lemma-dependency-graph` skill analyzes formal verification projects to visualize and analyze dependencies between lemmas, theorems, and definitions. Helps understand proof structure, identify bottlenecks, and optimize development workflow.

**Token Efficiency**: ~600 tokens vs ~1.8K manual analysis (65% reduction)

## Quick Start

### Natural Language Invocation
```
"Show me the dependency graph for my lemmas"
"Analyze lemma dependencies in this proof file"
"Visualize the structure of my Coq development"
```

### Direct Skill Invocation
```
/lemma-dependency-graph
```

## What It Analyzes

✅ **Lemma Dependencies**:
- Which lemmas depend on which others
- Transitive dependency chains
- Circular dependency detection
- Unused lemma identification

✅ **Proof Structure**:
- Hierarchical organization
- Proof complexity metrics
- Dependency depth analysis
- Critical path identification

✅ **Development Insights**:
- Development order suggestions
- Parallel proof opportunities
- Refactoring recommendations
- Maintainability assessment

## Analysis Process

### Phase 1: Lemma Discovery
Identifies all lemmas and theorems:
- Lemma statements and types
- Theorem declarations
- Definition dependencies
- Axiom dependencies

### Phase 2: Reference Extraction
Extracts all usage relationships:
- Direct lemma applications
- Implicit dependencies
- Section variable dependencies
- Module dependencies

### Phase 3: Graph Construction
Builds dependency network:
- Nodes: lemmas, theorems, definitions
- Edges: usage relationships
- Weights: usage frequency
- Categories: lemma types

### Phase 4: Analysis & Visualization
Generates insights and visualizations:
- Dependency graphs (text and DOT format)
- Critical path analysis
- Bottleneck identification
- Optimization suggestions

## Example Usage

### Example 1: Basic Dependency Analysis
```
User: "Show dependencies in my list theory"

Claude: 🔍 Analyzing lemma dependencies in list theory...

📊 Dependency Analysis:
- File: theories/lists.v
- Lemmas found: 23
- Dependencies: 41
- Analysis time: 1.2 seconds

🕸️ Dependency Graph:
list_length_nonnegative
├── list_length_zero_iff_empty
├── list_length_positive_iff_non_empty
└── list_length_append

list_append_assoc
├── list_append_nil
├── list_append_cons
└── list_length_append

list_reverse_eq
├── list_reverse_nil
├── list_reverse_cons
└── list_append_assoc

📈 Key Insights:
- Central lemmas: list_append_assoc, list_length_nonnegative
- Dependency depth: 3 levels
- No circular dependencies detected
- 2 independent lemma clusters found

💡 Development Suggestions:
1. Prove list_length_nonnegative first (foundation)
2. list_append_assoc enables many other proofs
3. list_reverse_eq can be proven in parallel
```

### Example 2: Complex Project Analysis
```
User: "Analyze dependencies across my entire Coq project"

Claude: 🔍 Building lemma dependency graph for entire project...

📋 Project Analysis:
- Files analyzed: 8 Coq files
- Total lemmas: 67
- Dependencies: 156
- Processing time: 3.4 seconds

🎯 Critical Path Analysis:
Longest dependency chain (7 levels):
set_theory_axioms → basic_set_operations → set_relations → 
ordered_sets → complete_lattices → fixed_point_theorems → 
knaster_tarski_lemma

🔍 Bottleneck Identification:
1. Lemma: induction_principle
   Dependencies: 12 other lemmas depend on it
   Risk: High - changes affect many proofs
   
2. Lemma: equality_definition
   Dependencies: 8 direct, 23 transitive
   Risk: Critical - fundamental to many proofs
   
3. Lemma: ordering_properties
   Dependencies: 6 direct, 15 transitive
   Risk: Medium - important but localized

📊 Dependency Metrics:
- Average dependencies per lemma: 2.3
- Maximum dependency depth: 7
- Circular dependencies: 0 (good!)
- Independent lemmas: 12 (can be proven in any order)

💡 Optimization Recommendations:
1. Stabilize equality_definition early (critical bottleneck)
2. Consider splitting induction_principle (high fan-out)
3. Prove independent lemmas in parallel
4. Review knaster_tarski_lemma chain for simplification
```

### Example 3: Refactoring Impact Analysis
```
User: "What happens if I change the induction principle?"

Claude: 🔍 Analyzing impact of changing induction principle...

⚠️ Impact Analysis:
Target lemma: induction_principle
Direct dependents: 12 lemmas
Transitive dependents: 34 lemmas
Total impact: 46 lemmas (69% of project)

🕸️ Affected Lemma Tree:
induction_principle
├── list_induction_cases (direct)
│   ├── list_append_properties (transitive)
│   ├── list_reverse_theorems (transitive)
│   └── list_sorting_lemmas (transitive)
├── tree_induction_cases (direct)
│   ├── tree_balance_properties (transitive)
│   └── tree_traversal_lemmas (transitive)
└── nat_induction_cases (direct)
    ├── arithmetic_lemmas (transitive)
    └── divisibility_theorems (transitive)

📊 Risk Assessment:
- Risk level: VERY HIGH
- Estimated rework: 15-20 hours
- Breaking changes: 46 proofs
- Testing required: Full regression

💡 Mitigation Strategies:
1. Create backwards-compatible version first
2. Prove new induction principle separately
3. Gradually migrate dependent lemmas
4. Add extensive regression tests
5. Consider creating induction framework
```

## Dependency Types

### 🔗 Direct Dependencies
Immediate lemma applications:
```
Lemma A: ...
Lemma B: ... by applying Lemma A ...
```

### 🕸️ Transitive Dependencies
Indirect relationships through chains:
```
Lemma A → Lemma B → Lemma C
(Lemma C transitively depends on Lemma A)
```

### 📦 Section Dependencies
Dependencies on section variables:
```
Section MySection.
Variable x: nat.
Lemma depends_on_x: ...
```

### 🔧 Module Dependencies
Cross-module relationships:
```
Require Import Lists.
Lemma uses_list_lemmas: ...
```

## Visualization Formats

### Text Graph
Human-readable hierarchy:
```
lemma_name
├── dependency_1
├── dependency_2
└── dependency_3
```

### DOT Format
Graphviz-compatible format:
```
digraph dependencies {
  "lemma_name" -> "dependency_1";
  "lemma_name" -> "dependency_2";
}
```

### JSON Structure
Machine-readable format:
```json
{
  "lemma": "lemma_name",
  "dependencies": ["dep1", "dep2"],
  "dependents": ["lem1", "lem2"]
}
```

## Analysis Metrics

### Complexity Metrics
- **Dependency count**: Number of direct dependencies
- **Fan-out**: Number of lemmas depending on this one
- **Depth**: Longest path to foundational axioms
- **Centrality**: How critical this lemma is to the graph

### Quality Metrics
- **Modularity**: How well-organized the dependencies are
- **Reusability**: How often lemmas are reused
- **Stability**: How changes would propagate
- **Maintainability**: Ease of modification

### Performance Metrics
- **Analysis time**: Time to build complete graph
- **Memory usage**: Size of dependency data structure
- **Scalability**: How well it handles large projects

## Configuration Options

**Analysis Scope**:
- `--file=specific.v`: Analyze single file only
- `--module=ModuleName`: Focus on specific module
- `--project-wide`: Analyze entire project

**Output Control**:
- `--depth=3`: Limit dependency depth shown
- `--format=text|dot|json`: Choose output format
- `--critical-path`: Show only critical dependencies

**Filtering Options**:
- `--exclude-trivial`: Skip trivial dependencies
- `--include-axioms`: Include axiom dependencies
- `--hide-leaves`: Hide lemmas with no dependencies

## Integration with Proof Development

**Development Planning**:
```
1. /lemma-dependency-graph (understand structure)
2. Identify proof order
3. Prove foundational lemmas first
4. Build up dependency chain
```

**Code Review Process**:
```
1. Reviewer checks dependency impact
2. Analyzes new dependencies added
3. Reviews dependency complexity
4. Approves or requests changes
```

**Refactoring Planning**:
```
1. /lemma-dependency-graph (baseline)
2. Plan refactoring approach
3. Identify safe modification points
4. Execute refactoring incrementally
```

## Optimization Strategies

### Reduce Dependency Complexity
1. **Extract Common Lemmas**: Create shared foundations
2. **Minimize Dependencies**: Remove unnecessary relationships
3. **Generalize Lemmas**: Make them more reusable
4. **Document Dependencies**: Explain why dependencies exist

### Improve Parallel Development
1. **Identify Independent Lemmas**: Prove in parallel
2. **Create Stable Interfaces**: Minimize change impact
3. **Reduce Bottlenecks**: Distribute dependencies
4. **Plan Development Order**: Optimize for parallelism

### Enhance Maintainability
1. **Stable Foundations**: Get base lemmas right first
2. **Clear Hierarchies**: Organize dependencies logically
3. **Minimal Coupling**: Reduce unnecessary dependencies
4. **Document Rationale**: Explain dependency choices

## Common Issues & Solutions

### Issue 1: Circular Dependencies
**Problem**: Lemma A depends on Lemma B which depends on Lemma A
**Solution**: Extract common functionality or reorder proofs

### Issue 2: Deep Dependency Chains
**Problem**: 10+ levels of dependencies
**Solution**: Extract intermediate lemmas or generalize

### Issue 3: High Fan-Out Bottlenecks
**Problem**: One lemma that everything depends on
**Solution**: Decompose into smaller, focused lemmas

### Issue 4: Unused Lemmas
**Problem**: Lemmas that nothing depends on
**Solution**: Remove or move to appropriate location

## Best Practices

1. **Design for Stability**: Make foundational lemmas stable
2. **Minimize Coupling**: Reduce unnecessary dependencies
3. **Document Relationships**: Explain why dependencies exist
4. **Regular Analysis**: Periodically review dependency graphs
5. **Incremental Development**: Build dependencies incrementally

## Token Efficiency

- Small file (10 lemmas): ~200 tokens
- Medium file (50 lemmas): ~400 tokens
- Large project (200+ lemmas): ~800 tokens
- Cross-project analysis: ~150 tokens per file

## Related Skills

- `analysis/formal/anti-pattern-sniffer` - Detect proof quality issues
- `analysis/formal/tactic-usage-count` - Analyze tactic patterns
- `analysis/formal/proof-obligations-snapshot` - Track remaining work
- `development/refactoring` - Restructure proof dependencies

---

**Ready to visualize your proofs?** Just tell Claude: "Show my lemma dependencies" or "Analyze proof structure"!