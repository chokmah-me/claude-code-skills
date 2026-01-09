# Claude Code Skills Directory

[![Skill Template Validator](https://github.com/chokmah-me/claude-code-skills/actions/workflows/skill-template-validator.yml/badge.svg)](https://github.com/chokmah-me/claude-code-skills/actions/workflows/skill-template-validator.yml)

Hierarchical organization of reusable Claude Code workflows and procedures.

## Directory Structure

```
~/.claude/skills/
├── analysis/              # Code and codebase inspection
│   ├── code/             # General software analysis
│   │   ├── api-contract-sniffer/
│   │   ├── dead-code-hunter/
│   │   └── dependency-audit/
│   ├── formal/           # Formal verification (Coq/proof systems)
│   │   ├── anti-pattern-sniffer/
│   │   ├── lemma-dependency-graph/
│   │   ├── proof-obligations-snapshot/
│   │   └── tactic-usage-count/
│   └── quantum/          # Quantum computing optimization
│       └── quantum-circuit-optimizer/
├── development/          # Active development workflows
│   ├── lean-plan/        # Token-efficient planning mode
│   ├── quick-test-runner/
│   └── refactoring/      # Code restructuring workflows
├── git/                  # Version control operations
│   ├── diff-summariser/
│   ├── migrate-repo/
│   └── repo-briefing/
└── meta/                 # Self-improvement and skill management
    ├── claude-startup-integration/  # Startup configuration and setup
    ├── manifest-generator/          # Generate skill manifests
    ├── session-snapshot/            # Save and resume session state
    ├── skill-extractor/             # Extract workflows from sessions → new skills
    ├── skill-recommendation-engine/ # Recommend skills based on context
    └── startup-skill-showcase/      # Showcase available skills
```

## Categories

### analysis/code
**Purpose**: Inspect codebases for quality, security, and maintainability issues

- `api-contract-sniffer` - Detect API contract violations
- `dead-code-hunter` - Find unused functions/imports
- `dependency-audit` - Check for outdated/vulnerable dependencies

### analysis/formal
**Purpose**: Formal verification and proof system analysis (Coq, Lean, etc.)

- `anti-pattern-sniffer` - Detect proof anti-patterns
- `lemma-dependency-graph` - Visualize proof dependencies
- `proof-obligations-snapshot` - Track unproven obligations
- `tactic-usage-count` - Analyze proof tactics

### analysis/quantum
**Purpose**: Quantum computing circuit analysis and optimization

- `quantum-circuit-optimizer` - Optimize quantum circuits by reducing gate count and depth

### development
**Purpose**: Active coding and refactoring workflows

- `lean-plan` - Token-efficient planning mode
- `quick-test-runner` - Fast test execution workflows
- `refactoring` - Code restructuring procedures

### git
**Purpose**: Version control and repository operations

- `diff-summariser` - Summarize git diffs for review
- `migrate-repo` - Transfer repos between accounts/orgs
- `repo-briefing` - Generate compact repository summaries

### meta ⭐
**Purpose**: Skills that improve the skills system itself

- `claude-startup-integration` - Configure and optimize Claude Code startup
- `manifest-generator` - Generate and manage skill manifests
- `session-snapshot` - Save and resume complete session state
- `skill-extractor` - **NEW!** Analyze sessions to create new skills from recurring workflows
- `skill-recommendation-engine` - Recommend relevant skills based on context
- `startup-skill-showcase` - Display and demonstrate available skills

## Using Skills

### Invoke by name
```
User: /lean-plan
User: /diff-summariser
```

### Reference in instructions
```
User: "Use the skill-extractor to formalize the workflow we just did"
```

### Let Claude auto-detect
Claude will proactively invoke relevant skills when patterns match skill descriptions.

## Creating New Skills

### Manual Creation
1. Choose category: `analysis/code`, `analysis/formal`, `development`, `git`, or `meta`
2. Create directory: `~/.claude/skills/[category]/[skill-name]/`
3. Copy template: `cp meta/skill-extractor/template.md [category]/[skill-name]/SKILL.md`
4. Fill in the template sections
5. Test with `/[skill-name]`

### Auto-Extraction (Recommended ⭐)
After an extended session with repeated workflows:

```
User: /skill-extractor

Claude will:
1. Analyze the last 15-30 messages
2. Identify recurring patterns
3. Generate a new skill definition
4. Place it in the appropriate category
```

## Skill Structure

Every skill should have:

```
[skill-name]/
├── SKILL.md          # Main skill definition (required)
├── README.md         # Extended documentation (optional)
├── examples/         # Example usage (optional)
└── templates/        # Reusable templates (optional)
```

## Token Budgets

Good skills should execute in:
- Quick lookups: <500 tokens
- Standard workflows: 500-1500 tokens
- Complex procedures: 1500-3000 tokens

If a skill consistently exceeds 3000 tokens, consider splitting it.

## Maintenance

### Automated Workflows

This repository uses comprehensive GitHub Actions automation:

**Validation & Quality**:
- ✅ **skill-template-validator** - Validates SKILL.md structure on every PR
- ✅ **readme-auto-update** - Auto-generates skills inventory

**Release Automation**:
- ✅ **post-tag-maintenance** - After tagging a release:
  - Updates date references in all documentation
  - Generates CHANGELOG.md entry
  - Creates/updates sitemap.xml
  - Updates skill metadata with version info
  - Commits changes back to main branch

**Repository Health**:
- ✅ **freshness-maintenance** - Weekly checks (Mondays 00:00 UTC):
  - Identifies stale content (6+ months old)
  - Detects outdated documentation (1+ year old)
  - Checks for broken internal links
  - Creates GitHub issues for attention needed

**State Management**:
- ✅ **snapshot-state-manager** - Daily snapshot management (00:00 UTC):
  - Archives session snapshots older than 30 days
  - Cleans archived snapshots older than 90 days
  - Generates snapshot state reports
  - Maintains snapshot inventory

### Old Flat Structure
The old flat structure still exists in `~/.claude/skills/` root:
- These are preserved for backward compatibility
- New skills should use the hierarchical structure
- Old skills can be manually removed after confirming copies work

### Cleanup (Optional)
```bash
cd ~/.claude/skills
# Remove old flat skills after verifying new structure works
rm -rf anti-pattern-sniffer api-contract-sniffer dead-code-hunter \
       dependency-audit diff-summariser lemma-dependency-graph \
       migrate-repo proof-obligations-snapshot quick-test-runner \
       refactoring repo-briefing tactic-usage-count
```

## Contributing

When you discover a useful workflow:
1. Use `/skill-extractor` to formalize it
2. Test the generated skill in a new session
3. Refine the instructions based on usage
4. Share with other Claude Code users!

---

**Last updated**: 2026-01-09 (Extracted skills inventory to separate file)

<!-- SKILLS_INVENTORY_START -->
See [SKILLS_INVENTORY.md](SKILLS_INVENTORY.md) for complete skill details.

<!-- SKILLS_INVENTORY_END -->
