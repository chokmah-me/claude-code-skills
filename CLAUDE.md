# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is **claude-code-skills**, a collection of 22 production-ready Claude Code skills organized hierarchically by category (meta, development, git, analysis). The repository includes installation tools, validation frameworks, and templates for creating new skills.

## Commands Reference

### Installation & Validation
```bash
# Install all skills
python install.py --all

# Install by category
python install.py --category meta
python install.py --category development
python install.py --category git
python install.py --category analysis

# Install specific skills
python install.py --skills session-snapshot skill-extractor

# Verify installation
python install.py --verify

# Dry run (preview without installing)
python install.py --all --dry-run
```

### Testing & Validation
```bash
# Validate all skills
python tests/validate_skills.py

# Validate specific category
python tests/validate_skills.py --category meta

# Run skill functionality tests
python tests/test_skills.py

# Verbose output
python tests/validate_skills.py --verbose
```

### Git Operations
```bash
# Standard workflow
git status
git add .
git commit -m "message"
git push origin main

# View recent commits
git log --oneline -10
```

## Architecture & Structure

### Hierarchical Skill Organization

```
skills/
├── meta/                          # 6 meta-skills (workflow management)
│   ├── session-snapshot/          # Session state management
│   ├── skill-extractor/           # Auto-discover skills from sessions
│   ├── skill-recommendation-engine/
│   ├── claude-startup-integration/
│   ├── startup-skill-showcase/
│   └── manifest-generator/
├── development/                   # 4 development skills
│   ├── lean-plan/
│   ├── quick-test-runner/
│   ├── refactoring/
│   └── matarao/                   # Mataroa blog publishing
├── git/                           # 3 git skills
│   ├── diff-summariser/
│   ├── migrate-repo/
│   └── repo-briefing/
└── analysis/                      # 9 analysis skills
    ├── code/                      # General code analysis
    │   ├── api-contract-sniffer/
    │   ├── ascii-sanitizer/       # Unicode/emoji sanitization
    │   ├── dead-code-hunter/
    │   └── dependency-audit/
    ├── formal/                    # Formal verification (Coq/proof systems)
    │   ├── anti-pattern-sniffer/
    │   ├── lemma-dependency-graph/
    │   ├── proof-obligations-snapshot/
    │   └── tactic-usage-count/
    └── quantum/                   # Quantum computing
        └── quantum-circuit-optimizer/
```

### Skill Structure Standard

Each skill follows this structure:
```
skill-name/
├── SKILL.md          # Primary skill definition (required)
│                     # Contains: description, purpose, usage, parameters, examples
├── README.md         # Extended documentation (optional)
├── examples/         # Example usage (optional)
└── templates/        # Reusable templates (optional)
```

### Key Files

- **install.py**: Python-based installer with dependency management, category-based installation, and validation
- **tests/validate_skills.py**: Validates skill structure, documentation quality, required sections
- **tests/test_skills.py**: Functional testing for skills
- **templates/**: Skill creation templates for consistent structure
- **CONTRIBUTING.md**: Comprehensive guidelines for creating and submitting skills

## Skill Development

### Creating a New Skill

1. **Choose appropriate category**: meta, development, git, or analysis (code/formal)
2. **Copy template**: Use `templates/skill-template.md` as starting point
3. **Follow required structure**:
   - Must include: Purpose, Key Features, Usage, Parameters, Examples, Output, Important Notes
   - Optional: Integration with Other Skills, Advanced Configuration, Best Practices, Troubleshooting
4. **Validate before submission**: `python tests/validate_skills.py --skill your-skill-name`

### Required Skill Sections

Per `tests/validate_skills.py:21-29`, every skill MUST include:
- `# {skill_name}` - Title
- `## 🎯 Purpose` - What problem it solves
- `## 🚀 Key Features` - Main capabilities
- `## 📋 Usage` - How to use it
- `## 🎛️ Parameters` - Configuration options
- `## 💡 Examples` - Real usage examples
- `## 🎁 Output` - What it produces
- `## ⚠️ Important Notes` - Warnings/limitations

### Skill Metadata Format

Skills should include frontmatter (see `skills/meta/session-snapshot/SKILL.md:1-4`):
```yaml
---
name: skill-name
description: Brief description for auto-discovery
---
```

## Installation System Architecture

The installer (`install.py`) provides:
- **Category-based installation**: Install entire categories at once
- **Dependency management**: Ensures required skills are installed first
- **Cross-platform support**: Works on Windows, macOS, Linux
- **Dry-run mode**: Preview changes without installing
- **Automatic directory detection**: Finds Claude skills directory (`~/.claude/skills`, `~/AppData/Roaming/Claude/skills`, etc.)

Default installation target: `~/.claude/skills/`

## Flagship Meta-Skills

The repository's key differentiators are meta-skills that improve Claude Code workflows:

1. **session-snapshot**: Save/restore session state for crash recovery and long sessions
2. **skill-extractor**: Auto-generate new skills from recurring conversation patterns
3. **skill-recommendation-engine**: Context-aware skill suggestions based on current work
4. **claude-startup-integration**: Optimize Claude Code startup and configuration
5. **startup-skill-showcase**: Interactive demonstration of available skills
6. **manifest-generator**: Generate and manage skill manifests with version control

## Development Philosophy

- **Token efficiency**: Skills should execute in <3000 tokens (simple: <500, standard: 500-1500, complex: 1500-3000)
- **Hierarchical organization**: Category-based structure for discoverability
- **Template-driven**: Consistent structure via templates
- **Community-focused**: Designed for contribution and sharing
- **Quality-first**: Comprehensive validation framework ensures consistency

## Testing & Validation Standards

Before committing changes to skills:
1. Run `python tests/validate_skills.py` to ensure structure compliance
2. Verify all required sections are present
3. Check that examples are clear and functional
4. Ensure parameter documentation is complete
5. Test installation with `python install.py --skills your-skill --dry-run`

## Git Workflow

This is a GitHub repository: https://github.com/chokmah-me/claude-code-skills

Standard workflow:
1. Make changes to skills or infrastructure
2. Validate with `python tests/validate_skills.py`
3. Test installation if modifying installer
4. Commit with descriptive messages
5. Push to remote

## Important Notes

- **NOT a monorepo**: This is a single-purpose repository for Claude Code skills
- **Python 3.8+ required**: For installation and testing scripts
- **No package.json**: This is a Python-based project, not Node.js
- **Skills are markdown**: Skill definitions are `.md` files, not code
- **Installation copies files**: The installer copies skills to `~/.claude/skills/` directory where Claude Code reads them
