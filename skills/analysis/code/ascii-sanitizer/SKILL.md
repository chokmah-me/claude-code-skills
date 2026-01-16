---
name: ascii-sanitizer
description: Detect and remove unsafe Unicode/emoji characters that break YAML and GitHub Actions. Use when user says "sanitize code", "remove emojis", "fix unicode errors", or "yaml safe characters".
---

# ASCII Sanitizer

## Description
Prevent CI/CD pipeline failures caused by non-ASCII characters (emojis, smart quotes, Unicode symbols) in code, configuration files, and documentation. This skill detects problematic characters that break YAML parsers and GitHub Actions workflows, then provides safe ASCII replacements.

## Features
- Detect non-ASCII characters in source files (emojis, Unicode symbols, smart quotes, zero-width spaces)
- Show exact file locations with line numbers and character codes
- Provide safe ASCII replacement suggestions
- Batch scan multiple file types (.yaml, .yml, .py, .md, .sh, .json)
- Optional auto-fix mode with safety warnings
- GitHub Actions integration available for automated PR checks

## Usage

### Basic Detection
Scan a single file for non-ASCII characters:
```bash
grep -Pn '[^\x00-\x7F]' file.yaml
```

### Batch Scanning
Find all files with Unicode issues:
```bash
find . -type f \( -name "*.yaml" -o -name "*.yml" -o -name "*.py" -o -name "*.md" -o -name "*.sh" \) -not -path "./.git/*" | xargs grep -l '[^\x00-\x7F]'
```

### Detailed Analysis
Show character codes and context:
```bash
grep -Pn '[^\x00-\x7F]' file.yaml | while read line; do
  echo "$line"
  echo "$line" | grep -oP '[^\x00-\x7F]' | xxd -p
done
```

### Auto-Fix Mode
Replace common problematic characters (review changes before applying):
```bash
# Smart quotes to straight quotes
sed -i "s/[""]/\"/g" file.yaml
sed -i "s/['']/'/g" file.yaml

# Em-dash to double dash
sed -i 's/—/--/g' file.yaml

# Ellipsis to three dots
sed -i 's/…/.../g' file.yaml

# Remove emojis and other Unicode symbols
sed -i 's/[^\x00-\x7F]//g' file.yaml
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--check-only` | Report issues without making changes | true |
| `--fix` | Auto-sanitize with safe replacements (requires confirmation) | false |
| `--extensions` | Comma-separated file extensions to scan | .yaml,.yml,.py,.md,.sh |
| `--exclude-dirs` | Directories to skip | .git,.venv,node_modules |
| `--show-codes` | Display Unicode codepoints (U+XXXX) | true |
| `--backup` | Create .bak files before fixing | true |

## Examples

### Example 1: Detect Unicode in GitHub Actions Workflow
```bash
# Scan workflow file
grep -Pn '[^\x00-\x7F]' .github/workflows/ci.yml

# Output:
# 12:    name: Build and Test
# 24:    - name: Run tests...
```

**Problem Found**: Smart quotes on line 12, emoji on line 24

**Fix**:
```bash
sed -i 's/[""]/"/g' .github/workflows/ci.yml
sed -i 's/[^\x00-\x7F]//g' .github/workflows/ci.yml
```

### Example 2: Sanitize Python Files with Emoji Comments
```bash
# Find Python files with non-ASCII
find . -name "*.py" | xargs grep -l '[^\x00-\x7F]'

# Output: ./src/main.py

# View problematic lines
grep -Pn '[^\x00-\x7F]' ./src/main.py

# Output:
# 42: # TODO: Fix this bug
```

**Fix**: Remove emoji or replace with `:rocket:`

### Example 3: Bulk Fix Repository Before CI Run
```bash
# 1. Find all affected files
FILES=$(find . -type f \( -name "*.yaml" -o -name "*.yml" \) -not -path "./.git/*" | xargs grep -l '[^\x00-\x7F]')

# 2. Create backups
for file in $FILES; do
  cp "$file" "$file.bak"
done

# 3. Apply fixes
for file in $FILES; do
  sed -i "s/[""]/\"/g" "$file"
  sed -i "s/['']/'/g" "$file"
  sed -i 's/—/--/g' "$file"
  sed -i 's/…/.../g' "$file"
  sed -i 's/[^\x00-\x7F]//g' "$file"
done

# 4. Verify fixes
git diff
```

## Output

The skill provides structured output showing:

1. **File Path**: Full path to affected file
2. **Line Number**: Exact location of non-ASCII character
3. **Line Content**: Context showing the problematic text
4. **Character Code**: Unicode codepoint (e.g., U+1F680 for rocket emoji)
5. **Suggested Fix**: Safe ASCII replacement

**Example Output**:
```
./github/workflows/test.yml:15
  name: "Deploy Application"
  Character: " (U+201C - LEFT DOUBLE QUOTATION MARK)
  Suggestion: Replace with straight quote: "

./src/config.py:42
  # TODO: Fix this bug
  Character: (U+1F680 - ROCKET)
  Suggestion: Remove emoji or use :rocket:
```

## Important Notes

### YAML-Breaking Characters
These characters commonly break YAML parsers:
- Smart quotes: " " (U+201C/201D) - Use `"` instead
- Smart apostrophes: ' ' (U+2018/2019) - Use `'` instead
- Em-dash: — (U+2014) - Use `--` instead
- Ellipsis: … (U+2026) - Use `...` instead
- Emojis: Any emoji - Remove or use `:emoji_name:` format
- Zero-width spaces: (U+200B) - Delete entirely

### Safe ASCII Range
- **Full ASCII**: 0x00-0x7F (0-127)
- **Printable ASCII**: 0x20-0x7E (32-126)
- **Control characters**: 0x00-0x1F (tabs, newlines are usually safe)

### Common Replacement Table
| Unicode Character | Codepoint | ASCII Replacement |
|-------------------|-----------|-------------------|
| " " (smart quotes) | U+201C/201D | " (0x22) |
| ' ' (smart apostrophes) | U+2018/2019 | ' (0x27) |
| — (em-dash) | U+2014 | -- (0x2D 0x2D) |
| – (en-dash) | U+2013 | - (0x2D) |
| … (ellipsis) | U+2026 | ... (0x2E 0x2E 0x2E) |
| Any emoji | U+1F300+ | [REMOVE or :name:] |
| Zero-width space | U+200B | [DELETE] |

### Safety Warnings
1. **Always backup** files before running auto-fix mode
2. **Review changes** with `git diff` before committing
3. **Test YAML files** after sanitization: `yamllint file.yaml`
4. **Check intentional Unicode**: Some strings legitimately need Unicode (UI text, internationalization)
5. **Emoji in strings vs code**: Comments/config = remove, user-facing strings = keep if intentional

### GitHub Actions Integration
To automatically check PRs for ASCII-safety, add the included workflow file to `.github/workflows/ascii-sanitizer.yml`. This will:
- Scan all code/config files on every PR
- Fail CI if non-ASCII characters are found
- Provide detailed error messages with file locations
- Prevent problematic code from merging

### Known Limitations
- Cannot distinguish between intentional Unicode (internationalization) and accidental (copy-paste)
- Some false positives in binary file paths or encoded strings
- Windows-1252 characters (common from copy-paste) may not all be caught by simple ASCII range check
