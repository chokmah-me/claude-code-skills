---
name: lemma-dependency-graph
description: Show most-applied lemmas in Coq proofs. Use when user says "lemma graph", "proof dependencies", or "which lemmas are critical".
---

# Lemma Dependency Graph Skill

## Purpose
Identify critical lemmas by usage frequency - entry points for refactoring (~1k tokens).

## Instructions

When user requests lemma dependency graph:

1. **Run the command** to extract lemma call graph
2. **Present top 20 lemmas** showing:
   - Lemma name
   - Application count
3. **Interpret**: High-count lemmas are architectural; low-count may be dead
4. **Offer**: "Want to see dependencies of specific lemmas or suggest refactoring?"

## Command

```bash
grep -h "Lemma\|Theorem" *.v | sed 's/Lemma \|Theorem //' | cut -d: -f1 | sort | uniq | tee /tmp/lemmas && grep -h "apply \|exact \|refine " *.v | grep -oE "[a-zA-Z0-9_]+" | grep -F -f /tmp/lemmas | sort | uniq -c | sort -nr | head -20
```

## Output Format

```
Count Lemma_Name
----- ----------
   42 price_nonnegative
   38 update_price_monotonic
   27 total_dwell_nonnegative
   15 apply_loss_reduces_dwell
    8 valid_loss_pattern_delta
    2 obscure_helper_lemma
```

## How It Works

1. **Extract all lemmas**: grep for Lemma/Theorem declarations
2. **Save to temp file**: create reference list
3. **Find applications**: grep for `apply`/`exact`/`refine` statements
4. **Filter**: keep only lemma names from reference list
5. **Count and rank**: sort by usage frequency

## Interpreting Results

### High Count (>20 applications)
- **Core architectural lemmas**
- Should be stable (many dependents)
- Good candidates for documentation
- Consider splitting if doing too much

### Medium Count (5-20 applications)
- **Workhorse lemmas**
- Good abstraction level
- May benefit from generalization

### Low Count (1-4 applications)
- **Specialized helpers**
- Check if actually needed
- May indicate missing abstraction
- Candidates for inlining

### Zero Count
- **Dead code or entry points**
- If not main theorem: likely unused
- If main theorem: good (shouldn't be applied)

## Use Cases

- Identifying refactoring impact
- Planning proof reorganization
- Finding circular dependencies
- Discovering missing abstractions
- Prioritizing lemma documentation

## Limitations

⚠️ **May miss**:
- Lemmas used via `Hint` databases
- Auto-applied lemmas (auto, eauto)
- Lemmas used in `rewrite` chains
- Lemmas from imported modules

For complete graph:
```bash
coqdep *.v  # Show file dependencies
```

## Follow-Up Actions

After seeing graph, Claude can:
- Suggest lemma splitting (if count >50)
- Identify dead lemmas (count=0, not main theorem)
- Propose helper lemmas (high-repetition patterns)
- Recommend proof refactoring order
- Generate dependency visualization

## Advanced: Finding Circular Dependencies

If lemma A has high count but you suspect circularity:
```bash
grep -n "apply A\|exact A" file.v  # Find all uses
# Check if A's proof uses any of those contexts
```

## Token Efficiency

- ~1k tokens for full graph
- Alternative: manual dependency tracing (40k+ tokens)
- 97% reduction in architecture analysis cost
