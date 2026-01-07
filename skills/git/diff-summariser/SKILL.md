---
name: diff-summariser
description: Summarize git diff changes with file stats and first 30 changed lines. Use when user says "summarise diff", "review recent changes", or "what changed in last commit".
---

# Diff Summariser Skill

## Purpose
Review PR/commit changes without loading entire files (~400 tokens).

## Instructions

When user requests a diff summary:

1. **Run the command** to get stats and key changes
2. **Present the output** showing:
   - Files touched with +/- counts
   - First 30 changed lines (additions/deletions)
3. **Offer**: "Want to see specific files in detail?"

## Command

```bash
git diff --stat HEAD~1..HEAD && echo "---" && git diff HEAD~1..HEAD --no-ext-diff | grep -E "^\+|^\-" | head -30
```

## Output Format

```
[File stats showing insertions/deletions]
---
[First 30 lines of actual changes]
```

## Use Cases

- Quick PR review before detailed analysis
- Understand scope of recent commit
- Identify which files had most changes
- Spot patterns in additions/deletions

## Token Efficiency

- ~400 tokens total
- Alternative would be 5-10k tokens reading all changed files
- 95% reduction in context loading
