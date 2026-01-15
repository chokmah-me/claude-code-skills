# Dead Code Hunter

A Claude Code skill for identifying potentially unused functions, classes, and exports across Python and JavaScript/TypeScript codebases.

## Overview

Dead Code Hunter analyzes your codebase to find symbols (functions, classes, constants) that are defined but never imported elsewhere. This helps identify candidates for cleanup, reducing codebase size and maintenance burden.

## Supported Languages

- **Python**: Detects `def` and `class` declarations
- **JavaScript/TypeScript**: Detects `export`, `function`, `const`, and `class` declarations

## How It Works

1. **Auto-detects project language** by scanning for `.py`, `.js`, or `.ts` files
2. **Finds source directory** automatically (`src/`, `lib/`, or current directory)
3. **Extracts all declarations** with file locations and line numbers
4. **Extracts all imports** from the codebase
5. **Compares** declarations against imports to find unused symbols
6. **Reports** the first 15 candidates with precise file locations

## Usage

Simply invoke the skill in your project directory:

```bash
/dead-code-hunter
```

The skill will automatically:
- Detect your project's language
- Find the appropriate source directory
- Generate a report of potentially unused code

## Output Format

### Python Projects

```
=== Python Dead Code Analysis ===
Potentially unused Python symbols:
./src/utils/helpers.py:42 def format_legacy_date
./src/api/deprecated.py:15 class OldAPIClient
./lib/legacy/converter.py:128 def old_conversion_method
```

### JavaScript/TypeScript Projects

```
=== JavaScript/TypeScript Dead Code Analysis ===
Potentially unused JS/TS symbols:
src/utils/tax.ts:23 calculateStateTax
lib/formatters.js:67 formatCurrency
components/old/Unused.tsx:5 UnusedComponent
```

Each line shows:
- **File path**: Relative path to the file
- **Line number**: Where the symbol is defined
- **Declaration type**: `def`, `class`, `function`, `const`, etc.
- **Symbol name**: The actual name of the unused symbol

## Verification Workflow

**Important**: Not all flagged symbols are actually unused! Always verify before deleting.

### Step 1: Review Candidates

```bash
/dead-code-hunter
```

### Step 2: Verify Individual Symbols

For each candidate, check all references:

```bash
# Replace SymbolName with the actual symbol
grep -rn "\bSymbolName\b" . --include="*.py" --include="*.js" --include="*.ts" --color=always | head -20
```

This shows:
- All occurrences in the codebase
- Context around each occurrence
- Whether it's only defined but never used

### Step 3: Check for False Positives

Before deleting, verify the symbol isn't:
- An **entry point** (`if __name__ == "__main__"`, CLI command)
- **Dynamically imported** (`import()`, `__import__()`, `require()`)
- An **external API** (if your code is a library)
- Referenced via **string** (`getattr`, `eval`, reflection)
- A **test fixture** used by test framework conventions
- A **framework hook** (lifecycle methods, decorators)

### Step 4: Safe Deletion

If confirmed unused:
1. Delete the code
2. Commit separately for easy revert
3. Run tests to verify nothing broke
4. Confirm with team if unsure

## Known Limitations

### False Positives

The skill may flag valid code in these cases:

| Scenario | Example | Why It's Flagged |
|----------|---------|------------------|
| Entry points | `if __name__ == "__main__"` | No import statement |
| Dynamic imports | `__import__('module')` | String-based, not parsed |
| External consumers | Public library API | Used outside the codebase |
| String references | `getattr(obj, 'method')` | Not a standard import |
| Test fixtures | `@pytest.fixture` | Framework convention |
| Framework hooks | `componentDidMount()` | Called by framework |

### False Negatives

The skill may miss:

- Dead code that's imported but never called
- Circular unused dependencies
- Code only used in commented-out sections

## Token Efficiency

- **This skill**: ~500-1,000 tokens
- **Manual approach**: Reading all files to track references (~50,000+ tokens)
- **Savings**: 98% reduction in token usage

## Advanced Usage

### Custom Source Directory

If your project has a non-standard structure, modify the source directory detection:

```bash
# Force specific directory
SRC_DIR="custom/path" /dead-code-hunter
```

### Language-Specific Analysis

Force Python analysis even if JS files are present:

```bash
cd claude-code-skills
# Only analyze Python files in current directory
grep -rn '^\s*\(def\|class\) \w\+' . --include="*.py" | ...
```

## Integration with Other Skills

- **Use after**: `/repo-briefing` to understand project structure first
- **Combine with**: `/diff-summariser` to check recent changes before deletion
- **Follow up with**: `/quick-test-runner` to verify tests pass after cleanup

## Best Practices

1. **Run regularly** during refactoring phases
2. **Verify before deleting** - don't trust the output blindly
3. **Delete incrementally** - one symbol at a time in separate commits
4. **Test thoroughly** after each deletion
5. **Use version control** - easy rollback if something breaks
6. **Document reasons** in commit messages for future reference

## Troubleshooting

### "No Python or JS/TS files detected"

- Verify you're in the project root directory
- Check if files have correct extensions (`.py`, `.js`, `.ts`)
- Try specifying `SRC_DIR` explicitly

### Too many false positives

- Focus on files in `deprecated/`, `old/`, `legacy/` directories first
- Prioritize `_internal` or `_private` prefixed functions
- Verify symbols with no recent git changes (likely forgotten)

### Grep permission errors on Windows

- The skill uses `mktemp -d` for cross-platform temp files
- If issues persist, run in WSL or Git Bash

## Examples

### Example 1: Clean Python Project

```bash
$ cd my-python-api
$ /dead-code-hunter

=== Python Dead Code Analysis ===
Potentially unused Python symbols:
./api/v1/deprecated.py:23 def old_authentication
./utils/legacy_parser.py:8 class LegacyXMLParser
./helpers/unused.py:15 def format_old_date

# Verify first candidate
$ grep -rn "\bold_authentication\b" . --include="*.py"
./api/v1/deprecated.py:23:def old_authentication(token):
# Only definition found - safe to delete
```

### Example 2: JavaScript/TypeScript SPA

```bash
$ cd my-react-app
$ /dead-code-hunter

=== JavaScript/TypeScript Dead Code Analysis ===
Potentially unused JS/TS symbols:
src/components/OldButton.tsx:12 OldButton
src/utils/formatting.ts:45 formatPhoneNumber
lib/analytics/deprecated.js:8 trackLegacyEvent

# Check OldButton usage
$ grep -rn "\bOldButton\b" . --include="*.tsx" --include="*.ts"
src/components/OldButton.tsx:12:export const OldButton = () => {
src/components/index.ts:15:export { OldButton } from './OldButton';
# Still exported from index - might be used externally, don't delete
```

## Contributing

Found a bug or have suggestions? Issues and PRs welcome at the [claude-code-skills repository](https://github.com/chokmah-me/claude-code-skills).

## License

Part of the claude-code-skills collection. See repository root for license information.
