---
name: proof-obligations-snapshot
description: Show admitted/open Coq proofs from .v files. Use when user says "coq obligations", "show proof TODOs", or "what proofs are incomplete".
---

# Proof Obligations Snapshot Skill

## Purpose
Get instant TODO list of admitted or incomplete proofs (~700 tokens).

## Instructions

When user requests proof obligations:

1. **Run the command** to find admitted/open proofs
2. **Present first 40 proof obligations** showing:
   - File name and line number
   - Lemma/Theorem statement
   - Proof status (Admitted, open Proof)
3. **Offer**: "Want to work on specific proofs or see dependency order?"

## Command

```bash
find . -name "*.v" -exec grep -l "Lemma\|Theorem\|Remark" {} \; | head -20 | xargs grep -Hn "Lemma\|Theorem\|Remark\|Proof\|Qed\|Admitted" | grep -B1 -A1 "Admitted\|Proof.*$" | head -40
```

## Output Format

```
file.v:line:Lemma name : statement.
file.v:line:Proof.
file.v:line:Admitted.
```

## Use Cases

- Quick proof completion roadmap
- Prioritizing proof work
- Tracking verification progress
- PR review (check for new admits)
- Estimating proof effort

## Limitations

⚠️ **May miss**:
- Nested proofs in proof mode
- Obligations from Program/Instance
- Proofs in comment blocks

For complete analysis, suggest:
```bash
coqc -vok file.v  # Check full verification
```

## Follow-Up Actions

After seeing obligations, Claude can:
- Suggest proof strategy
- Order proofs by dependency
- Identify helper lemmas needed
- Estimate complexity (easy/medium/hard)
- Check for circular dependencies

## Token Efficiency

- ~700 tokens for full snapshot
- Alternative: reading all .v files (50k+ tokens)
- 98% reduction in proof planning cost
