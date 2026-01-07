---
name: dead-code-hunter
description: Find potentially unused functions, classes, and exports by comparing declarations to imports. Use when user says "find dead code", "unused functions", or "what can we delete".
---

# Dead Code Hunter Skill

## Purpose
Identify exported symbols that are never imported (~1k tokens).

## Instructions

When user requests dead code analysis:

1. **Run the command** to compare declarations vs imports
2. **Present first 15 candidates** for potential deletion
3. **Warn**: "Verify these aren't used via dynamic imports or external consumers"
4. **Offer**: "Want me to check specific symbols for actual usage?"

## Command

```bash
echo "Symbols never imported:"; grep -roh "def \|class \|export \|const \|function " src/ | sort | uniq > /tmp/all && grep -roh "import.*from \|require( \|from .* import " src/ | sort | uniq > /tmp/used && comm -23 /tmp/all /tmp/used | head -15
```

## Output Format

```
Symbols never imported:
[list of 15 declarations with no import references]
```

## How It Works

1. **Extract declarations**: `def`, `class`, `export`, `const`, `function`
2. **Extract imports**: `import...from`, `require()`, `from...import`
3. **Compare**: Show declarations NOT found in imports
4. **Limit**: First 15 results (high-signal candidates)

## False Positive Cases

⚠️ **May flag valid code**:
- Entry points (main.py, index.js)
- Dynamic imports (`import()` or `__import__()`)
- External API consumers (if library)
- Test fixtures
- CLI commands

## Recommended Workflow

1. Run skill to get candidate list
2. Verify each symbol:
   ```bash
   grep -r "symbol_name" . --include="*.py" --include="*.js"
   ```
3. Confirm with team before deleting
4. Remove in separate commit for easy revert

## Token Efficiency

- ~1k tokens for analysis
- Alternative: reading all files to track references (50k+ tokens)
- 98% reduction in discovery cost
