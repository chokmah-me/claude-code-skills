# Skill Upgrader

A meta-skill for systematically upgrading Claude Code skills from basic/broken implementations to production-ready quality.

## Overview

Skill Upgrader codifies the proven pattern used to successfully improve dead-code-hunter, api-contract-sniffer, and dependency-audit. It provides a systematic approach to adding multi-language support, precise output formats, verification helpers, and comprehensive documentation to existing skills.

## When to Use

- **Broken skills**: Commands produce incorrect or generic output
- **Basic skills**: Missing language detection, source directory detection, or version extraction
- **Incomplete skills**: Missing required emoji sections or documentation
- **Enhancement requests**: Adding features to working but limited skills

## The Upgrade Pattern

Based on 3 successful skill improvements, the pattern includes:

### Core Improvements
1. **Language/framework detection** - Auto-detect Python, JavaScript, Rust, etc.
2. **Source directory detection** - Fallback chain (src/, lib/, app/, .)
3. **Precise output** - file:line format or structured data (not generic text)
4. **Cross-platform support** - Use mktemp for temp directories
5. **Version extraction** - Show package@version or detailed info
6. **Statistics** - Show counts, totals, summaries

### Documentation Standards
1. **All 7 emoji sections** - 🎯 Purpose, 🚀 Key Features, 📋 Usage, 🎛️ Parameters, 💡 Examples, 🎁 Output, ⚠️ Important Notes
2. **Verification helpers** - Commands to verify skill findings
3. **Comprehensive README** - 300+ lines with examples, workflows, troubleshooting
4. **Token efficiency** - Document savings vs. manual approach

## Usage

```
User: "This skill is broken/substandard, upgrade it using the skill-upgrader pattern"

Claude applies:
1. Analyzes current skill (reads SKILL.md, README.md)
2. Identifies deficiencies (broken commands, missing sections)
3. Applies core improvements (language detection, precise output)
4. Adds all required emoji sections
5. Creates comprehensive README with examples
6. Tests upgraded skill
7. Commits with detailed message
8. Updates session snapshot
```

## Upgrade Checklist

Use this checklist for each skill upgrade:

### Core Improvements
- [ ] Add language/framework/format detection
- [ ] Add source directory auto-detection (if applicable)
- [ ] Fix grep patterns for precise output (file:line format)
- [ ] Add cross-platform support (mktemp for temp dirs)
- [ ] Extract version/detail information (if applicable)
- [ ] Add statistics/counts to output

### Documentation
- [ ] Add all 7 required emoji sections
- [ ] Add verification helper section
- [ ] Create or update README.md (comprehensive)
- [ ] Add 3+ complete examples
- [ ] Document known limitations
- [ ] Include troubleshooting section

### Testing & Commit
- [ ] Test upgraded command on real project
- [ ] Verify output format improvements
- [ ] Create detailed commit message
- [ ] Push to remote
- [ ] Update session snapshot

## Pattern Examples

### Pattern 1: Analysis Skills (grep-based)

**Before**:
```bash
grep -rh "pattern" src/ | head -20
# Output: pattern matches only, no context
```

**After**:
```bash
SRC_DIR=$(test -d src && echo "src" || test -d lib && echo "lib" || echo ".")
if ls *.py 2>/dev/null; then
  grep -rn "pattern" "$SRC_DIR" --include="*.py" | sed 's/...' | head -20
elif ls *.js 2>/dev/null; then
  grep -rn "pattern" "$SRC_DIR" --include="*.js" | sed 's/...' | head -20
fi
# Output: file:line info with precise details
```

### Pattern 2: Dependency Skills

**Before**:
```bash
cat package.json | jq -r '.dependencies | keys[]'
# Output: package names only, Node.js only
```

**After**:
```bash
if [ -f "package.json" ]; then
  cat package.json | jq -r '.dependencies // {} | to_entries[] | "\(.key)@\(.value)"' | head -20
  echo "Total: $(cat package.json | jq -r '.dependencies // {} | length') dependencies"
elif [ -f "requirements.txt" ]; then
  grep -v '^#' requirements.txt | head -20
  echo "Total: $(grep -v '^#' requirements.txt | wc -l) dependencies"
# ... add Cargo.toml, go.mod, Gemfile, etc.
fi
# Output: package@version with counts, multi-language support
```

## Case Studies

### Case Study 1: dead-code-hunter

**Original state**:
- Broken grep outputting keywords `class `, `def ` instead of symbol names
- No language detection
- No file:line information

**Upgraded to**:
- Python vs JavaScript/TypeScript detection
- Precise output: `./install.py:28 def __init__`
- Cross-platform temp directories
- Verification helper commands
- 236-line README with examples

**Commit**: abdd8bb (+346/-293 lines)

### Case Study 2: api-contract-sniffer

**Original state**:
- Simple grep for route declarations
- Hardcoded `src/` directory
- No HTTP method extraction
- Missing file locations

**Upgraded to**:
- Flask/FastAPI/Express framework detection
- Source directory detection (src/, app/, api/)
- HTTP method extraction: `src/api/users.py:42 GET /api/users`
- Verification helper for checking endpoint usage
- 270-line README with security examples

**Commit**: f3b16e7 (+397/-226 lines)

### Case Study 3: dependency-audit

**Original state**:
- Only package.json and requirements.txt
- No version numbers
- No statistics

**Upgraded to**:
- 7 package managers (Node, Python, Rust, Go, Ruby, PHP, Java)
- Version extraction: `express@^4.18.2`
- Dependency counts: `Total: 42 runtime dependencies`
- Security audit integration
- 400-line README with vulnerability workflows

**Commit**: 1a454e3 (+575/-323 lines)

## Verification Workflow

### Before Upgrading
1. Read current SKILL.md
2. Identify specific deficiencies
3. Plan improvements based on skill type
4. Review similar skills for patterns

### During Upgrade
1. Apply core improvements systematically
2. Test each improvement incrementally
3. Verify output format is correct
4. Add documentation as you go

### After Upgrading
1. Test on real projects (multiple languages if applicable)
2. Verify all required sections present
3. Check README completeness
4. Review commit message accuracy
5. Update session snapshot

## Token Efficiency

### Analysis & Planning
- Read current skill: ~200-500 tokens
- Identify deficiencies: ~100-200 tokens
- Plan improvements: ~200-300 tokens

### Implementation
- Core command rewrite: ~500-800 tokens
- Add emoji sections: ~300-500 tokens
- Add verification helpers: ~200-300 tokens

### Documentation
- README creation: ~1,500-2,000 tokens
- Examples and workflows: ~500-800 tokens

### Testing & Commit
- Testing: ~100-200 tokens
- Commit message: ~100-200 tokens
- Session snapshot update: ~100-200 tokens

**Total per skill**: ~3,500-5,000 tokens
**Savings per future upgrade**: ~10,000+ tokens (vs. figuring out pattern from scratch)

## Best Practices

### 1. Follow Established Patterns
- Use the dead-code-hunter/api-contract-sniffer/dependency-audit pattern
- Don't reinvent solutions for common problems
- Apply proven language detection techniques

### 2. Test Thoroughly
- Run upgraded command on real projects
- Test each supported language/framework
- Verify edge cases (empty results, errors)

### 3. Document Comprehensively
- Examples should be complete and realistic
- Include troubleshooting for common issues
- Show verification workflows

### 4. Maintain Token Efficiency
- Document token savings vs. manual approach
- Keep commands focused and efficient
- Use head -N to limit output

### 5. Commit Systematically
- Detailed commit messages
- Reference similar improvements
- Include Co-Authored-By credit

### 6. Update Session Snapshot
- Document what was improved
- Record commit SHA and statistics
- Note lessons learned

## Known Limitations

### Pattern Applicability
This pattern works best for:
- ✅ Analysis skills (grep-based code search)
- ✅ Dependency/package management skills
- ✅ Code discovery skills
- ✅ Format detection skills

Less applicable for:
- ❌ Interactive skills requiring user input
- ❌ Skills with complex state management
- ❌ Skills that are already production-ready
- ❌ Skills with fundamentally different patterns

### Breaking Changes
Upgrading may introduce breaking changes:
- Output format changes (file:line instead of plain text)
- Different command invocation
- New dependencies (jq, sed, awk)

Always test thoroughly and document changes in commit message.

## Troubleshooting

### Issue: "Can't determine language to detect"

**Solution**: Review the skill's purpose. Not all skills need language detection. Examples:
- git skills (repo operations, not language-specific)
- meta skills (work on skills themselves)
- Some analysis skills (project-agnostic)

### Issue: "Original skill was working, upgrade broke it"

**Solution**:
1. Test upgraded command separately first
2. Keep original command in comments temporarily
3. Use git to show diff and identify issue
4. Revert specific changes that broke functionality

### Issue: "README is getting too long"

**Solution**: That's expected and good. Comprehensive READMEs should be 300-400+ lines with:
- Multiple examples (3-4)
- Complete verification workflows
- Detailed troubleshooting
- Integration suggestions
- Use cases and best practices

### Issue: "Not sure which improvements apply"

**Solution**: Use the checklist in SKILL.md and mark which apply:
- Analysis skills → language detection, file:line output
- Dependency skills → multi-format support, version extraction
- All skills → emoji sections, README, verification helpers

## Advanced Usage

### Upgrading Multiple Related Skills

If upgrading a family of related skills (e.g., all analysis/formal skills):
1. Upgrade one skill completely as template
2. Extract common patterns
3. Apply to remaining skills with variations
4. Document pattern evolution in skill-upgrader

### Creating Skill Variants

When upgrading reveals need for multiple related skills:
1. Create base skill with core functionality
2. Create specialized variants for specific use cases
3. Link between skills in README
4. Example: dependency-audit → dependency-audit-security (CVE focus)

### Pattern Evolution

As you upgrade more skills, update skill-upgrader itself:
1. Document new patterns discovered
2. Add new improvement categories
3. Update examples with latest successes
4. Refine checklist based on experience

## Integration with Other Skills

**Before upgrading**:
- `/lean-plan` - Plan upgrade strategy
- `/repo-briefing` - Understand repository context

**During upgrade**:
- `/skill-upgrader` - This skill
- Read/Edit/Write tools - Implement changes

**After upgrade**:
- `/diff-summariser` - Review changes
- `/quick-test-runner` - Run tests if applicable
- `/session-snapshot` - Document upgrade

## Contributing

Found improvements to the upgrade pattern? Update this skill:
1. Document new pattern in SKILL.md
2. Add example to README
3. Update checklist if needed
4. Test pattern on new skill upgrade
5. Commit with "Evolve skill-upgrader pattern" message

## License

Part of the claude-code-skills collection. See repository root for license information.

---

**Pattern established**: 2026-01-15 based on dead-code-hunter (abdd8bb), api-contract-sniffer (f3b16e7), and dependency-audit (1a454e3) improvements.
