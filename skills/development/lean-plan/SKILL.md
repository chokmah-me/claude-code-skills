---
name: lean-plan
description: Enter token-efficient planning mode. Load ≤2k-token repo snapshot, adopt guard-rail persona, and produce concise checklist plans. Use when user says "start planning mode" or "plan this feature".
---

# Lean Planning Skill

## Purpose
Enter planning mode with minimal token usage by loading compact context and constraining verbosity.

## Instructions

When user requests planning mode:

### Step 1: Load Repo Snapshot

Run this command to gather context:

```bash
echo -e "---\nREPO_STRUCTURE:\n$(find . -type f \( -iname "*.py" -o -iname "*.js" -o -iname "*.ts" \) | grep -E '(^./(src|lib|test)|README)' | head -40 | tree --fromfile . 2>/dev/null || tree -L 2)\n---\nREADME_HEAD:\n$(head -80 README.md 2>/dev/null)\n---\nPACKAGE_META:\n$(cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null || echo "no meta")\n---\nRECENT_COMMITS:\n$(git log --oneline -8 2>/dev/null)\n---"
```

### Step 2: Adopt Guard-Rail Persona

After presenting the snapshot, state these constraints:

```
You are in planning mode.
Goal: produce a concise, ordered task list that improves the requested area.

Constraints:
- Ask for files only when you must read them; skip boiler-plate
- Never paste whole files back—quote ≤5-line snippets
- Keep plan <50 lines; use check-boxes
- If a task needs external docs, note "[fetch: URL]" instead of pasting

Ready? Reply "OK" and wait for the user's improvement goal.
```

### Step 3: Create Plan

When user specifies their goal, produce a plan using this format:

```markdown
## Plan: [Feature/Fix Name]

**Goal**: [1-line objective]

**Pre-requisites**:
- [ ] Read: path/to/file.ts (check interface)
- [ ] Verify: existing test coverage

**Tasks**:
1. [ ] Update `module.py:42` - add validation logic
2. [ ] Create `new_feature.ts` - implement handler
3. [ ] Update tests in `test/` directory
4. [ ] [fetch: docs.library.com/api] - check latest API version

**Risk**: [1 sentence on main blocker]
**Est**: [time estimate]
```

## Anti-Patterns to Avoid

❌ Don't paste entire files (>10 lines)
❌ Don't read every file upfront
❌ Don't create verbose 100+ line plans

✅ Quote small snippets (≤5 lines)
✅ Read files selectively
✅ Create focused <50 line checklists

## Token Efficiency

- Good plan: 200-500 tokens
- Acceptable: 500-1000 tokens
- Too verbose: >1000 tokens (refactor it)
