---
name: skill-upgrader
description: Systematically upgrade existing Claude Code skills to production quality with multi-language support, precise output, and comprehensive documentation. Use when improving substandard skills or adding missing features.
---

# Skill Upgrader

## 🎯 Purpose

Systematically upgrade existing Claude Code skills from basic/broken implementations to production-ready quality. Applies a proven pattern: multi-language detection, precise output formats, verification helpers, and comprehensive documentation.

## 🚀 Key Features

- **Proven upgrade pattern**: Based on successful improvements to dead-code-hunter, api-contract-sniffer, and dependency-audit
- **Standardized quality**: Ensures all required emoji sections and documentation
- **Multi-language support**: Adds language/framework auto-detection where applicable
- **Precise output**: Changes from generic output to file:line or structured formats
- **Verification helpers**: Adds commands to verify skill findings
- **Comprehensive docs**: Generates README.md with examples, workflows, troubleshooting
- **Token efficient**: Follows established pattern rather than reinventing each time

## 📋 Usage

When you need to upgrade a skill:

1. **Identify target skill** - Usually substandard, broken, or missing features
2. **Run this skill** - Applies systematic upgrade pattern
3. **Test upgraded skill** - Verify improvements work
4. **Commit and document** - Push changes with detailed commit message

## 🎛️ Parameters

- **skill_path**: Path to skill directory (e.g., `skills/analysis/code/skill-name/`)
- **upgrade_type**: Type of upgrade needed
  - `full` - Complete overhaul (broken/basic skills)
  - `enhance` - Add missing features to working skills
  - `standardize` - Add required sections and documentation only

## Instructions

### Step 1: Analyze Current Skill

Read the existing skill to understand current state:

```bash
# Read current SKILL.md
Read: skills/[category]/[skill-name]/SKILL.md

# Check if README exists
ls skills/[category]/[skill-name]/README.md
```

Identify deficiencies:
- [ ] Broken or inadequate command
- [ ] No language/framework detection
- [ ] Generic output (no file:line or structured format)
- [ ] Missing emoji sections (🎯 🚀 📋 🎛️ 💡 🎁 ⚠️)
- [ ] No README.md or inadequate documentation
- [ ] No verification helper commands
- [ ] No cross-platform support (temp directories, etc.)

### Step 2: Apply Core Improvements

Based on skill type, apply appropriate improvements:

#### For Analysis/Search Skills (grep-based)

1. **Add language detection**:
```bash
if ls *.py 2>/dev/null || find "$SRC_DIR" -name "*.py" 2>/dev/null | head -1 | grep -q .; then
  echo "=== Python Analysis ==="
  # Python-specific grep patterns
elif ls *.js *.ts 2>/dev/null || find "$SRC_DIR" -name "*.js" -o -name "*.ts" 2>/dev/null | head -1 | grep -q .; then
  echo "=== JavaScript/TypeScript Analysis ==="
  # JS/TS-specific grep patterns
else
  echo "No supported files detected"
fi
```

2. **Add source directory detection**:
```bash
SRC_DIR=$(test -d src && echo "src" || test -d lib && echo "lib" || test -d app && echo "app" || echo ".")
```

3. **Fix grep patterns**:
- Use `grep -rn` (not `-rh`) for file:line output
- Add word boundaries `\b` where needed
- Use sed to extract precise information
- Format as `file:line info` or `file:line TYPE details`

4. **Add cross-platform support**:
```bash
TMPD=$(mktemp -d 2>/dev/null || mktemp -d -t 'skill-name')
# ... use $TMPD for temp files
rm -rf "$TMPD"
```

#### For Dependency/Package Skills

1. **Add multi-format support**:
```bash
if [ -f "package.json" ]; then
  # Node.js logic
elif [ -f "requirements.txt" ]; then
  # Python logic
elif [ -f "Cargo.toml" ]; then
  # Rust logic
# ... add more formats
fi
```

2. **Extract version information**:
- Use `jq` for JSON parsing
- Use sed/awk for TOML/plain text
- Format as `package@version` or `package==version`

3. **Add statistics**:
- Show total count
- Show top N results (head -20)

### Step 3: Add Required Emoji Sections

Ensure all required sections exist in SKILL.md:

```markdown
## 🎯 Purpose
[1-2 sentences describing what problem it solves]

## 🚀 Key Features
- **Feature 1**: Description
- **Feature 2**: Description
[3-6 bullet points with bold headers]

## 📋 Usage
[Clear instructions for when and how to invoke]

## 🎛️ Parameters
[List parameters or "None required - auto-detects..."]

## 💡 Examples
### Example 1: [Scenario]
[Complete example with input and output]

## 🎁 Output
[Show example output format with code blocks]

## ⚠️ Important Notes
[Warnings, limitations, false positives/negatives]
```

### Step 4: Add Verification Helper

Add section showing how to verify findings:

```markdown
## Verification Helper

After finding candidates, verify individual items:

```bash
# Verify a specific item (replace with actual check)
echo "Checking references to 'item_name':"
grep -rn "\\bitem_name\\b" . --include="*.ext" --color=always | head -20
```

This shows:
- All occurrences in the codebase
- Context around each occurrence
- Whether it's actually used
```

### Step 5: Create Comprehensive README.md

Generate or update README.md with:

```markdown
# [Skill Name]

## Overview
[2-3 sentences describing the skill]

## Supported [Languages/Frameworks/Formats]
[List what it supports]

## How It Works
1. Step one
2. Step two
[High-level process]

## Usage
[Simple invocation example]

## Output Format
[Show examples for each supported type]

## Verification Workflow
### Step 1: Run the Skill
### Step 2: Verify Individual Items
### Step 3: Check for False Positives/Negatives
[Detailed verification process]

## Known Limitations
### False Positives/Negatives
[Table or list of limitation scenarios]

## Token Efficiency
[Comparison with manual approach]

## Advanced Usage
[Optional customizations]

## Integration with Other Skills
[Related skills to use before/after/with]

## Use Cases
[5-6 numbered use cases]

## Best Practices
[5-6 numbered practices]

## Troubleshooting
[Common issues and solutions]

## Examples
[3-4 complete real-world examples]

## Contributing
[Link to repository]

## License
[Link to license]
```

### Step 6: Test Upgraded Skill

Run the upgraded command to verify it works:

```bash
# Test on actual project
cd /path/to/test/project
[run the skill command]

# Verify output format is correct
# Check for errors
# Confirm improvements work
```

### Step 7: Commit and Push

Create detailed commit message:

```bash
git add skills/[category]/[skill-name]/
git commit -m "$(cat <<'EOF'
Improve [skill-name] with [key improvements]

Similar improvements to [reference skills]:
- Add [feature 1]
- Add [feature 2]
- Fix [issue 1]
- Add all required emoji sections per repository standards
- Complete rewrite of README.md to match new functionality

Changes:
- SKILL.md: +X lines with improved command and documentation
- README.md: +Y lines with examples, workflows, troubleshooting

Token efficiency: ~X-Y tokens (Z% reduction vs manual approach)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

git push origin main
```

### Step 8: Update Session Snapshot

Document the upgrade in session snapshot:

```markdown
### [Skill Name] (✅ Complete)

**Improvements applied:**
- [List of improvements]

**Statistics:**
- Commit: [SHA]
- Changes: +X/-Y lines
- Token efficiency: ~X tokens (Z% reduction vs manual)
- Status: Committed and pushed to origin/main
```

## Upgrade Pattern Checklist

Use this checklist for each skill upgrade:

**Core Improvements:**
- [ ] Add language/framework/format detection
- [ ] Add source directory auto-detection (if applicable)
- [ ] Fix grep patterns for precise output (file:line format)
- [ ] Add cross-platform support (mktemp for temp dirs)
- [ ] Extract version/detail information (if applicable)
- [ ] Add statistics/counts to output

**Documentation:**
- [ ] Add all 7 required emoji sections
- [ ] Add verification helper section
- [ ] Create or update README.md (comprehensive)
- [ ] Add 3+ complete examples
- [ ] Document known limitations
- [ ] Include troubleshooting section

**Testing & Commit:**
- [ ] Test upgraded command on real project
- [ ] Verify output format improvements
- [ ] Create detailed commit message
- [ ] Push to remote
- [ ] Update session snapshot

## 💡 Examples

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

## ⚠️ Important Notes

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

## Token Efficiency

- **Analysis phase**: ~500-800 tokens (read current skill, identify issues)
- **Core improvements**: ~1,000-1,500 tokens (rewrite command, add sections)
- **Documentation**: ~1,500-2,000 tokens (README generation)
- **Testing & commit**: ~300-500 tokens
- **Total**: ~3,500-5,000 tokens per skill upgrade

**Savings per future use**: ~10,000+ tokens (vs. figuring out pattern from scratch)

## Pattern Evolution

This skill is based on successful upgrades to 3 skills. As more skills are upgraded, the pattern may evolve. Update this skill to reflect:
- New improvement patterns discovered
- Additional language/framework support
- Better documentation structures
- Improved verification methods

## Related Skills

- `/lean-plan` - Plan the upgrade before executing
- `/session-snapshot` - Save state before/after major upgrades
- `/diff-summariser` - Review changes before committing
- `/skill-extractor` - Extract new patterns discovered during upgrades

---

**Pattern Source**: Extracted from session improving dead-code-hunter (abdd8bb), api-contract-sniffer (f3b16e7), and dependency-audit (1a454e3) on 2026-01-15.
