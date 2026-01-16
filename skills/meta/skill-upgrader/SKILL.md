---
name: skill-upgrader
description: Systematically upgrade existing Claude Code skills to production quality with multi-language support, precise output, and comprehensive documentation. Use when improving substandard skills or adding missing features.
---

# Skill Upgrader


## Description
[1-2 sentences describing what problem it solves]

- User says 'use [skill-name]' or mentions the skill by name
- Relevant to the current task or discussion

## Usage
[Simple invocation example]

## Parameters
[List parameters or "None required - auto-detects..."]

## Features
- **Feature 1**: Description
- **Feature 2**: Description
[3-6 bullet points with bold headers]

## Examples

### Example 1: Upgrading dead-code-hunter

**Before**: Broken grep outputting `class ` and `def ` keywords
**After**: Language detection, precise `file:line def symbol_name` output

```bash
# Old broken output
class
def
export

# New precise output
./install.py:28 def __init__
./install.py:42 class SkillInstaller
./src/utils.py:15 def parse_config
```

**Improvements**:
- Added Python vs JS/TS detection
- Fixed grep to use `-rn` and sed parsing
- Added verification helper
- Complete README with 236 lines

### Example 2: Upgrading api-contract-sniffer

**Before**: Simple grep, hardcoded `src/` directory, no versions
**After**: Flask/FastAPI/Express detection, HTTP methods, precise locations

```bash
# Old generic output
@app.route('/users', methods=['GET'])
router.post('/api/auth/login', ...)

# New precise output
src/api/users.py:42 GET /api/users
src/api/users.py:67 POST /api/users
src/api/auth.py:15 POST /api/auth/login
```

**Improvements**:
- Added framework detection (Flask/FastAPI/Express)
- Source directory detection (src/, app/, api/)
- HTTP method extraction
- Complete README with 270 lines

### Example 3: Upgrading dependency-audit

**Before**: Only package.json and requirements.txt, no versions
**After**: 7 package managers, version extraction, counts

```bash
# Old output
express
lodash
moment

# New output
=== Node.js Dependencies (package.json) ===
express@^4.18.2
lodash@^4.17.21
moment@^2.29.4

Total: 42 runtime dependencies
```

**Improvements**:
- Added 7 package managers (Node, Python, Rust, Go, Ruby, PHP, Java)
- Version extraction (package@version format)
- Dependency statistics
- Complete README with 400 lines

## Output
[Show example output format with code blocks]

## Important Notes

**This skill applies a proven pattern, not arbitrary changes.**

Guidelines:
- **Use established patterns**: Follow the improvements from dead-code-hunter, api-contract-sniffer, and dependency-audit
- **Don't over-engineer**: Only add features that solve real problems
- **Test thoroughly**: Verify improvements work on real projects
- **Document comprehensively**: README should enable users to understand and verify results
- **Maintain token efficiency**: Document token savings (usually 96-98% reduction)

When NOT to use this skill:
- Skill is already production-ready
- Skill is fundamentally different (not grep/analysis based)
- Changes would break existing users
- Improvements don't follow established patterns

## Best Practices
[5-6 numbered practices]
