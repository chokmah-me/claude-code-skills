---
name: dead-code-hunter
description: Find potentially unused functions, classes, and exports by comparing declarations to imports. Use when user says "find dead code", "unused functions", or "what can we delete".
---

# Dead Code Hunter Skill

## 🎯 Purpose

Identify exported symbols that are never imported across Python and JavaScript/TypeScript codebases. This skill helps find potentially unused code by comparing declarations against imports, enabling safe cleanup and technical debt reduction.

## 🚀 Key Features

- **Language detection**: Auto-detects Python or JavaScript/TypeScript projects
- **Source directory detection**: Automatically finds `src/`, `lib/`, or uses current directory
- **Precise location tracking**: Shows file path and line number for each unused symbol
- **Cross-platform**: Uses `mktemp` for reliable temp file handling on Windows/Unix
- **False positive awareness**: Includes verification helpers and warnings
- **Token efficient**: ~500-1k tokens vs 50k+ for manual analysis

## 📋 Usage

When user requests dead code analysis:

1. **Run the command** to compare declarations vs imports
2. **Present first 15 candidates** with file locations (e.g., `src/utils.py:42 def helper`)
3. **Warn**: "Verify these aren't used via dynamic imports or external consumers"
4. **Offer**: "Want me to verify any specific symbols? I can grep for all references to check actual usage."

## 🎛️ Parameters

None required - the skill auto-detects:
- **Language**: Python (*.py) or JavaScript/TypeScript (*.js, *.ts)
- **Source directory**: Tries `src/`, `lib/`, then current directory
- **Output limit**: First 15 unused symbols

Optional environment variable:
- `SRC_DIR`: Override source directory detection (e.g., `SRC_DIR=custom/path`)

## Command

**Auto-detect language and find unused symbols:**

```bash
# Detect source directory
SRC_DIR=$(test -d src && echo "src" || test -d lib && echo "lib" || echo ".")

# Create temp directory (cross-platform)
TMPD=$(mktemp -d 2>/dev/null || mktemp -d -t 'dead-code')

# Detect language and run appropriate analysis
if ls *.py 2>/dev/null || find "$SRC_DIR" -name "*.py" 2>/dev/null | head -1 | grep -q .; then
  echo "=== Python Dead Code Analysis ==="
  # Extract Python declarations with filenames
  grep -rn '^\s*\(def\|class\) \w\+' "$SRC_DIR" --include="*.py" | sed 's/^\([^:]*\):\([0-9]*\):\s*\(def\|class\) \(\w\+\).*/\1:\2 \3 \4/' | sort -t' ' -k3 -u > "$TMPD/py_decl.txt"
  # Extract Python imports
  grep -rh '\(^from .* import \|^import \)' "$SRC_DIR" --include="*.py" | sed 's/.*import //;s/,/ /g;s/ as .*//g' | tr ' ' '\n' | grep -v '^$' | sort -u > "$TMPD/py_import.txt"
  # Extract just symbol names for comparison
  awk '{print $3}' "$TMPD/py_decl.txt" | sort -u > "$TMPD/py_decl_names.txt"
  # Find unused symbols
  comm -23 "$TMPD/py_decl_names.txt" "$TMPD/py_import.txt" > "$TMPD/py_unused.txt"
  echo "Potentially unused Python symbols:"
  grep -f "$TMPD/py_unused.txt" "$TMPD/py_decl.txt" | head -15

elif ls *.js *.ts 2>/dev/null || find "$SRC_DIR" -name "*.js" -o -name "*.ts" 2>/dev/null | head -1 | grep -q .; then
  echo "=== JavaScript/TypeScript Dead Code Analysis ==="
  # Extract JS/TS declarations with filenames
  grep -rn '\(export \(function\|class\|const\)\|^function\|^const\|^class\) \w\+' "$SRC_DIR" --include="*.js" --include="*.ts" | sed 's/^\([^:]*\):\([0-9]*\):\s*\(.*\)/\1:\2 \3/' | sed 's/^\([^:]*:[0-9]*\) .* \(\w\+\).*/\1 \2/' > "$TMPD/js_decl.txt"
  # Extract JS/TS imports
  grep -rh '\(^import .* from\|^const .* = require\)' "$SRC_DIR" --include="*.js" --include="*.ts" | sed 's/.*{\(.*\)}.*/\1/;s/,/ /g;s/import //;s/ as .*//g' | tr ' ' '\n' | grep -v '^$' | sort -u > "$TMPD/js_import.txt"
  # Extract just symbol names for comparison
  awk '{print $2}' "$TMPD/js_decl.txt" | sort -u > "$TMPD/js_decl_names.txt"
  # Find unused symbols
  comm -23 "$TMPD/js_decl_names.txt" "$TMPD/js_import.txt" > "$TMPD/js_unused.txt"
  echo "Potentially unused JS/TS symbols:"
  grep -f "$TMPD/js_unused.txt" "$TMPD/js_decl.txt" | head -15

else
  echo "No Python or JS/TS files detected"
fi

# Clean up temp directory
rm -rf "$TMPD"
```

## 🎁 Output

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

## How It Works

1. **Auto-detect language**: Check for Python (*.py) or JS/TS (*.js, *.ts) files
2. **Find source directory**: Try `src/`, `lib/`, or current directory
3. **Extract declarations**:
   - Python: `def function_name` and `class ClassName`
   - JS/TS: `export function`, `const`, `class`, standalone declarations
4. **Extract imports**: Parse import statements to find referenced symbols
5. **Compare**: Show declarations NOT found in any import statement
6. **Limit**: First 15 results (high-signal candidates)

## False Positive Cases

⚠️ **May flag valid code**:
- Entry points (main.py, index.js)
- Dynamic imports (`import()` or `__import__()`)
- External API consumers (if library)
- Test fixtures
- CLI commands

## Verification Helper

After finding candidates, verify individual symbols for actual usage:

```bash
# Verify a specific symbol (replace SymbolName with actual symbol)
echo "Checking all references to 'SymbolName':"
grep -rn "\bSymbolName\b" . --include="*.py" --include="*.js" --include="*.ts" --color=always | head -20
```

This shows:
- All occurrences (not just imports)
- Line numbers for context
- Whether it's actually used in code (not just defined)

## Recommended Workflow

1. **Run skill** to get candidate list
2. **Verify each symbol** using the verification helper above
3. **Check for**:
   - Dynamic imports (`__import__()`, `import()`)
   - External consumers (if library)
   - String-based references (`getattr`, `eval`, reflection)
   - Entry points (`if __name__ == "__main__"`)
4. **Confirm with team** before deleting
5. **Remove in separate commit** for easy revert

## ⚠️ Important Notes

**This skill identifies candidates for deletion, not guaranteed dead code.**

Always verify before deleting:
- Entry points (`if __name__ == "__main__"`, main functions)
- Dynamic imports (`import()`, `__import__()`, `require()`)
- External API consumers (if your code is a library)
- String-based references (`getattr`, `eval`, reflection)
- Test fixtures (used by framework conventions)
- Framework hooks (lifecycle methods, decorators)

Use the verification helper to check actual usage before deletion.

## 💡 Examples

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

## Token Efficiency

- **Command execution**: ~500-1k tokens
- **Alternative approach**: Reading all files to manually track references (50k+ tokens)
- **Savings**: 98% reduction in discovery cost
