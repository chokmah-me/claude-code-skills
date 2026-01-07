---
name: anti-pattern-sniffer
description: Find fragile Coq proof patterns in .v files. Use when user says "coq anti-patterns", "check proof quality", or "find fragile proofs".
---

# Anti-Pattern Sniffer Skill

## Purpose
Detect common Coq proof anti-patterns that cause brittleness (~800 tokens).

## Instructions

When user requests anti-pattern check:

1. **Run the command** to find suspect patterns
2. **Present first 20 matches** showing:
   - File name and line number
   - Anti-pattern type
   - Code snippet
3. **Warn**: "These patterns often break on minor changes"
4. **Offer**: "Want refactoring suggestions for specific patterns?"

## Command

```bash
grep -Hn "simpl in \*\|rewrite <-.*in \*\|destruct.*as \[\|induction.*using\|Qed\.$" *.v | grep -v "(*" | head -20
```

## Output Format

```
file.v:123:  simpl in *.
file.v:456:  destruct H as [].
file.v:789:  rewrite <- foo in *.
```

## Anti-Patterns Detected

### 1. `simpl in *` - Performance Killer
**Why bad**: Simplifies ALL hypotheses, often unnecessary
**Fix**: Use targeted `simpl in H` or `cbn` instead
```coq
(* Bad *)
simpl in *.

(* Good *)
simpl in H. cbn.
```

### 2. `rewrite <- ... in *` - Context Pollution
**Why bad**: Rewrites everywhere, hard to debug failures
**Fix**: Rewrite specific hypotheses
```coq
(* Bad *)
rewrite <- lemma in *.

(* Good *)
rewrite <- lemma in H1, H2.
```

### 3. `destruct ... as []` - Unnamed Variables
**Why bad**: Creates unnamed hypotheses, unreadable proofs
**Fix**: Use explicit names
```coq
(* Bad *)
destruct H as [].

(* Good *)
destruct H as [x [Hpos Hbound]].
```

### 4. `induction ... using` - Custom Schemes
**Why bad**: Often indicates missing helper lemma
**Fix**: Prove generalized lemma instead
```coq
(* Suspect *)
induction n using my_custom_ind.

(* Better *)
Lemma generalized_property : ...
apply generalized_property.
```

### 5. `Qed.` with trailing space - Formatting
**Why bad**: Inconsistent style, hard to grep
**Fix**: Use consistent `Qed.` without space

## False Positive Cases

⚠️ **May flag valid code**:
- Intentional `simpl in *` for small contexts
- Pattern matching with empty constructor
- Standard library induction schemes

## Recommended Workflow

1. Run skill to get candidate list
2. Review each match in context
3. Prioritize by proof importance
4. Refactor in separate commits
5. Re-run skill to verify fixes

## Additional Anti-Patterns (Manual Check)

These require reading proof context:
- Over-reliance on `admit`/`Admitted`
- Proof scripts >50 lines (should be lemmas)
- Copy-pasted proof blocks
- No comments in complex proofs
- Assertions without proof (`assert ... by admit`)

## Token Efficiency

- ~800 tokens for full scan
- Alternative: manual proof review (30k+ tokens)
- 96% reduction in quality audit cost
