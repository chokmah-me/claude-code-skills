---
name: repo-briefing
description: Generate a token-efficient repository summary with structure, README, package metadata, and recent commits. Use when user asks for "repo briefing", "summarize repo", or "what's the state of this code".
---

# Repository Briefing Skill

## Purpose
Generate a ≤2000-token snapshot giving Claude context to start work without loading full file trees.

## Instructions

When the user requests a repository briefing:

1. **Run the one-liner command** below to gather context
2. **Present the output** in a structured format
3. **End with**: "Ask for any extra files or folders you need; I'll fetch them selectively."

## Command

```bash
echo -e "---\nREPO_STRUCTURE:\n$(find . -type f \( -iname "*.py" -o -iname "*.js" -o -iname "*.ts" -o -iname "*.json" -o -iname "*.md" \) | grep -E '(^./(src|lib|test|docs)|README)' | head -40 | tree --fromfile . 2>/dev/null || tree -L 2)\n---\nREADME_HEAD:\n$(head -100 README.md 2>/dev/null)\n---\nPACKAGE_META:\n$(cat package.json 2>/dev/null || cat pyproject.toml 2>/dev/null || cat Cargo.toml 2>/dev/null || echo "no meta")\n---\nRECENT_COMMITS:\n$(git log --oneline -10 2>/dev/null)\n---\n"
```

## Output Structure

```
---
REPO_STRUCTURE:
[filtered file tree from src/lib/test/docs]

---
README_HEAD:
[first 100 lines of README]

---
PACKAGE_META:
[package.json or pyproject.toml or Cargo.toml]

---
RECENT_COMMITS:
[last 10 commits]

---
```

## Follow-up

After presenting the briefing, remind the user:
"Ask for any extra files or folders you need; I'll fetch them selectively."
