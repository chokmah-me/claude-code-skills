---
name: dead-code-hunter
description: Find potentially unused functions, classes, and exports by comparing declarations to imports. Use when user says "find dead code", "unused functions", or "what can we delete".
---

# Dead Code Hunter Skill


## Description

Identify exported symbols that are never imported across Python and JavaScript/TypeScript codebases. This skill helps find potentially unused code by comparing declarations against imports, enabling safe cleanup and technical debt reduction.

- User says 'use [skill-name]' or mentions the skill by name
- Relevant to the current task or discussion

## Usage

When user requests dead code analysis:

1. **Run the command** to compare declarations vs imports
2. **Present first 15 candidates** with file locations (e.g., `src/utils.py:42 def helper`)
3. **Warn**: "Verify these aren't used via dynamic imports or external consumers"
4. **Offer**: "Want me to verify any specific symbols? I can grep for all references to check actual usage."

## Parameters

None required - the skill auto-detects:
- **Language**: Python (*.py) or JavaScript/TypeScript (*.js, *.ts)
- **Source directory**: Tries `src/`, `lib/`, then current directory
- **Output limit**: First 15 unused symbols

Optional environment variable:
- `SRC_DIR`: Override source directory detection (e.g., `SRC_DIR=custom/path`)

## Features

- **Language detection**: Auto-detects Python or JavaScript/TypeScript projects
- **Source directory detection**: Automatically finds `src/`, `lib/`, or uses current directory
- **Precise location tracking**: Shows file path and line number for each unused symbol
- **Cross-platform**: Uses `mktemp` for reliable temp file handling on Windows/Unix
- **False positive awareness**: Includes verification helpers and warnings
- **Token efficient**: ~500-1k tokens vs 50k+ for manual analysis

## Examples

### Example 1: Python Project

```bash
$ /dead-code-hunter
=== Python Dead Code Analysis ===
Potentially unused Python symbols:
./src/utils/helpers.py:42 def format_legacy_date
./src/api/deprecated.py:15 class OldAPIClient
./tests/fixtures/unused.py:8 def create_mock_user
```

### Example 2: JavaScript/TypeScript Project

```bash
$ /dead-code-hunter
=== JavaScript/TypeScript Dead Code Analysis ===
Potentially unused JS/TS symbols:
src/utils/tax.ts:23 calculateStateTax
lib/formatters.js:67 formatCurrency
components/old/Unused.tsx:5 UnusedComponent
```

### Example 3: Verifying a Specific Symbol

```bash
$ grep -rn "\bformat_legacy_date\b" . --include="*.py" --color=always
./src/utils/helpers.py:42:def format_legacy_date(date):
# No other references found - likely safe to delete
```

## Output

```
=== Python Dead Code Analysis ===
Potentially unused Python symbols:
src/utils/helpers.py:42 def unused_helper_function
src/models/user.py:128 class MyUnusedClass
lib/legacy/old_api.py:15 def old_deprecated_method
...
```

or

```
=== JavaScript/TypeScript Dead Code Analysis ===
Potentially unused JS/TS symbols:
src/utils/tax.ts:23 calculateTax
lib/formatters.js:67 formatDate
components/old/Unused.tsx:5 UnusedComponent
...
```

## Important Notes

**This skill identifies candidates for deletion, not guaranteed dead code.**

Always verify before deleting:
- Entry points (`if __name__ == "__main__"`, main functions)
- Dynamic imports (`import()`, `__import__()`, `require()`)
- External API consumers (if your code is a library)
- String-based references (`getattr`, `eval`, reflection)
- Test fixtures (used by framework conventions)
- Framework hooks (lifecycle methods, decorators)

Use the verification helper to check actual usage before deletion.
