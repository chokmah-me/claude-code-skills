---
name: tactic-usage-count
description: Count Coq tactic usage frequency in .v files. Use when user says "tactic census", "what tactics do we use", or "analyze proof style".
---

# Tactic Usage Count Skill

## Purpose
Census of proof tactics to identify patterns and over-reliance (~600 tokens).

## Instructions

When user requests tactic census:

1. **Run the command** to count tactic usage
2. **Present top 15 tactics** showing:
   - Tactic name
   - Usage count
3. **Warn**: "High automation (auto/eauto) may hide fragile proofs"
4. **Offer**: "Want to analyze specific proof styles or refactor automation?"

## Command

```bash
grep -rho "auto\|eauto\|lia\|nia\|ring\|field\|simpl\|cbn\|rewrite\|apply\|reflexivity\|tauto\|intuition" *.v 2>/dev/null | sort | uniq -c | sort -nr | head -15
```

## Output Format

```
Count Tactic
----- ------
  234 apply
  187 rewrite
  156 auto
   98 reflexivity
   67 simpl
```

## How It Works

1. **Extract tactics**: grep for common proof commands
2. **Count occurrences**: sort and count duplicates
3. **Rank**: sort by frequency
4. **Limit**: Top 15 most-used tactics

## Red Flags

⚠️ **Watch for**:
- `auto`/`eauto` > 30% of total: Over-reliance on automation
- `intuition` without constraints: Proof brittleness
- `simpl in *`: Performance anti-pattern
- Low `apply` count: Under-using lemmas
- High `rewrite` count: May need better lemmas

## Recommended Analysis

After census, check:
1. **Automation balance**: Should be 20-40% auto tactics
2. **Structured vs brute-force**: High `apply`/`exact` is good
3. **Domain tactics**: Should see `lra`/`lia` for arithmetic

## Tactic Categories

**Automation**: auto, eauto, tauto, intuition
**Arithmetic**: lia, nia, lra, nra, ring, field
**Simplification**: simpl, cbn, compute
**Application**: apply, exact, refine
**Rewriting**: rewrite, replace, subst
**Reflection**: reflexivity, trivial

## Token Efficiency

- ~600 tokens for full census
- Alternative: manual tactic audit (20k+ tokens)
- 97% reduction in style analysis cost
