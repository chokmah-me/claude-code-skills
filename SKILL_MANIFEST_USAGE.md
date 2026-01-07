---
name: skill-manifest-usage
description: Guide for using the Unified Skill Manifest to access all 16+ Claude Code skills
---

# 🎯 Using the Unified Skill Manifest

## The Problem Solved

Claude Code only shows skills in the root `.claude/skills` directory (4 skills), but you have **16+ skills** organized in subdirectories. The **Unified Skill Manifest** solves this by providing a single, comprehensive catalog of ALL your skills.

## How to Access All Your Skills

### Method 1: Ask Claude Code Directly
```
What skills are available?
Show me all skills
List your capabilities
```
Claude will show the **Unified Skill Manifest** with all 16+ skills organized by category.

### Method 2: View the Manifest File
```bash
# Read the complete manifest
type C:\Users\danie\.claude\skills\UNIFIED_SKILL_MANIFEST.md

# Quick check for specific skills
findstr /c:"session-snapshot" C:\Users\danie\.claude\skills\UNIFIED_SKILL_MANIFEST.md
```

## 🌟 Quick Skill Reference

### Meta Skills (Your Productivity Foundation)
- **`session-snapshot`** - Save/restore session context
- **`skill-extractor`** - Turn workflows into skills
- **`startup-skill-showcase`** - Auto-showcase skills
- **`skill-recommendation-engine`** - Smart skill suggestions
- **`claude-startup-integration`** - Startup system integration

### Development Skills
- **`lean-plan`** - Efficient project planning
- **`quick-test-runner`** - Fast testing workflows

### Git Skills  
- **`diff-summariser`** - Summarize changes
- **`migrate-repo`** - Repository migration
- **`repo-briefing`** - Codebase analysis

### Analysis Skills
- **Code Quality**: `api-contract-sniffer`, `dead-code-hunter`, `dependency-audit`
- **Formal Verification**: `anti-pattern-sniffer`, `lemma-dependency-graph`, `proof-obligations-snapshot`, `tactic-usage-count`

## 🚀 Common Workflows

### Starting a New Session
1. **Check available skills**: "What skills do you have?"
2. **Save starting point**: `/session-snapshot`
3. **Get recommendations**: "Recommend skills for [your task]"

### Before Major Work
1. `/session-snapshot` (save current state)
2. Do your work
3. `/session-snapshot` (save final state)

### Code Analysis
1. `/repo-briefing` (understand codebase)
2. Choose analysis skill based on needs:
   - API analysis → `api-contract-sniffer`
   - Dead code → `dead-code-hunter` 
   - Dependencies → `dependency-audit`

### Creating Custom Skills
1. Use any workflow successfully
2. `/skill-extractor` (formalize as skill)
3. Test the new skill
4. Add to manifest if useful

## 📊 Skill Statistics

- **Total Skills**: 16+ active skills
- **Categories**: 6 (Meta, Development, Git, Analysis/Code, Analysis/Formal, Root)
- **Meta Skills**: 5 (including session-snapshot prominently featured)
- **Token Range**: 300-1000+ tokens per invocation

## 🔧 Maintenance

The manifest is automatically maintained. When you add new skills:

1. Run the generator:
```bash
cd C:\Users\danie\.claude\skills
python3 meta\manifest-generator\generate_manifest_simple.py
```

2. The manifest updates with new skills
3. All skills remain accessible through the unified interface

## 💡 Pro Tips

- **Always start with `/session-snapshot`** before long tasks
- **Use `/skill-extractor`** to capture useful workflows you discover
- **Check the manifest** when exploring new capabilities
- **Meta skills** are your productivity multipliers - learn them first!

---

**Remember**: Claude Code shows 4 skills, but your **Unified Skill Manifest** contains **16+ skills**. Just ask "What skills are available?" to see everything!