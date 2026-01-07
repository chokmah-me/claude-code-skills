# 🎯 Claude Code Unified Skill Manifest - Usage Guide

## Overview

The **Unified Skill Manifest** system solves Claude Code's limitation of only discovering skills in the root `.claude/skills` directory by creating a master catalog that includes all skills organized in subdirectories.

## Problem Solved

**Before**: Claude Code only saw 4 skills in root directory  
**After**: Claude Code sees all 16+ skills across all categories  

## Quick Start

### 1. View All Available Skills
```
User: "What skills are available?"
User: "Show me all skills"
User: "List your capabilities"
```

**Response**: Shows the unified manifest with all 16+ skills organized by category

### 2. Use Specific Skills
```
User: "/session-snapshot"  # Save session state
User: "/skill-extractor"   # Extract workflow to skill
User: "/diff-summariser"   # Review git changes
```

### 3. Find Skills by Category
```
User: "Show me development skills"
User: "What git skills do you have?"
User: "I need analysis tools"
```

## Skill Categories

### 🚀 Development Skills (2)
- **lean-plan** - Token-efficient planning
- **quick-test-runner** - Fast testing workflows

### 🎯 Git Skills (3)
- **diff-summariser** - Summarize changes
- **migrate-repo** - Transfer repositories  
- **repo-briefing** - Project summaries

### 🔍 Code Analysis (3)
- **api-contract-sniffer** - Find API endpoints
- **dead-code-hunter** - Find unused code
- **dependency-audit** - Check dependencies

### 📐 Formal Verification (4)
- **anti-pattern-sniffer** - Coq proof patterns
- **lemma-dependency-graph** - Proof dependencies
- **proof-obligations-snapshot** - Track obligations
- **tactic-usage-count** - Analyze tactics

### ⭐ Meta Skills (5)
- **session-snapshot** - Save session state
- **skill-extractor** - Create new skills
- **skill-recommendation-engine** - Suggest skills
- **claude-startup-integration** - Optimize startup
- **startup-skill-showcase** - Show capabilities

## Common Workflows

### Before Starting Complex Work
```
User: "/session-snapshot"  # Save current state
# ... do work ...
User: "/session-snapshot"  # Save progress
```

### Code Review Process
```
User: "/diff-summariser"   # See what changed
User: "/repo-briefing"     # Understand context
```

### Creating New Skills
```
User: "We just did a useful workflow"
User: "/skill-extractor"   # Extract to reusable skill
```

### Analysis Tasks
```
User: "Find dead code in this project"
User: "/dead-code-hunter"  # Runs the analysis
```

## Auto-Detection Triggers

The manifest enables Claude to automatically suggest skills when you mention:

- **"skills"**, **"capabilities"**, **"what can you do"** → Shows full manifest
- **"save snapshot"**, **"checkpoint"** → Suggests `/session-snapshot`
- **"summarize changes"**, **"review diff"** → Suggests `/diff-summariser`
- **"extract workflow"**, **"make this a skill"** → Suggests `/skill-extractor`

## Maintenance

### Update Manifest After Adding Skills
```bash
cd ~/.claude/skills
python3 meta/manifest-generator/generate_manifest_simple.py
```

### Weekly Maintenance
Run the generator weekly to ensure the manifest stays current with any skill changes.

## Benefits

1. **Complete Discovery**: All 16+ skills visible to Claude Code
2. **Organized Access**: Skills grouped by functional category
3. **Quick Reference**: Most-used skills prominently displayed
4. **Usage Patterns**: Common workflows documented
5. **Auto-Detection**: Skills suggested based on context
6. **Token Efficiency**: Each skill shows estimated token usage

## Architecture

```
.claude/skills/
├── UNIFIED_SKILL_MANIFEST.md          # Master catalog (readable by Claude)
├── meta/manifest-generator/           # Maintenance tools
│   ├── SKILL.md                      # Generator skill definition
│   └── generate_manifest_simple.py   # Update script
├── analysis/
│   ├── code/                         # Code quality skills
│   └── formal/                       # Formal verification skills
├── development/                       # Development workflows
├── git/                              # Version control skills
└── meta/                             # System improvement skills
```

## Troubleshooting

### Manifest Not Updating
```bash
# Run generator manually
python3 ~/.claude/skills/meta/manifest-generator/generate_manifest_simple.py
```

### Skills Not Found
1. Check skill has proper `SKILL.md` with frontmatter
2. Verify skill is in correct directory structure
3. Run manifest generator to refresh

### Category Issues
1. Skills are auto-categorized by directory path
2. Root-level skills go in "Root" category
3. Use format: `category/subcategory/skill-name/`

## Future Enhancements

The manifest system can be extended with:
- Skill usage analytics
- Automatic skill recommendations
- Category expansion
- Token usage optimization
- Skill dependency tracking

---

**💡 Pro Tip**: The manifest generator runs automatically when you add new skills, but you can always run it manually to ensure your catalog is up-to-date!