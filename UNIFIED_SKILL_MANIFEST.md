---
name: unified-skill-manifest
description: Master catalog of all 16+ Claude Code skills organized by category. Use when user asks "what skills are available", "show me all skills", or "list capabilities".
---

# 🎯 Claude Code Unified Skill Manifest

**16+ Skills Available** • Organized by Category • Last Updated: 2026-01-07

## 🌟 Quick Reference - Most Used Skills

| Skill | Category | Trigger Phrases | Tokens |
|-------|----------|----------------|----------|
| **session-snapshot** | meta | save progress, snapshot, backup context | ~1000+ |
| **skill-extractor** | meta | extract workflow, create skill | ~800 |
| **diff-summariser** | git | summarize diff, show changes | ~500 |
| **repo-briefing** | git | analyze repo, codebase overview | ~500 |
| **lean-plan** | development | start planning, plan feature | ~800 |

## 📋 Complete Skill Catalog

### ⭐ Meta Skills (5)
*Skills that improve the skills system itself*

- **session-snapshot** - Save and restore complete session context for crash recovery and workflow continuity.
  *Use when*: "save snapshot", "backup context", "session save"  
  *Location*: `meta/session-snapshot/SKILL.md`

- **skill-extractor** - Transform successful workflows into reusable skills with automatic documentation.
  *Use when*: "extract workflow", "create skill", "automate this"  
  *Location*: `meta/skill-extractor/SKILL.md`

- **startup-skill-showcase** - Auto-detect new sessions and showcase available skills with meta-skill emphasis.
  *Use when*: "show skills", "what can you do", new session detected  
  *Location*: `meta/startup-skill-showcase/SKILL.md`

- **skill-recommendation-engine** - Context-aware skill suggestions based on conversation patterns and task analysis.
  *Use when*: "recommend skills", "what should I use", task transitions  
  *Location*: `meta/skill-recommendation-engine/SKILL.md`

- **claude-startup-integration** - Seamlessly integrate skill discovery into Claude Code's existing startup flow.
  *Use when*: "setup integration", "configure startup", skill visibility issues  
  *Location*: `meta/claude-startup-integration/SKILL.md`

### 🚀 Development Skills (2)
*Active coding and refactoring workflows*

- **lean-plan** - Token-efficient project planning with structured task breakdown and progress tracking.
  *Use when*: "start planning", "plan this feature", "break down tasks"  
  *Location*: `development/lean-plan/SKILL.md`

- **quick-test-runner** - Fast, focused testing with automatic test discovery and result summarization.
  *Use when*: "run tests", "quick test", "validate changes"  
  *Location*: `development/quick-test-runner/SKILL.md`

### 🎯 Git & Repository Skills (3)
*Version control and repository operations*

- **diff-summariser** - Summarize code changes without reading entire diffs, focusing on impact and intent.
  *Use when*: "summarize diff", "show changes", "what changed"  
  *Location*: `git/diff-summariser/SKILL.md`

- **migrate-repo** - Comprehensive repository migration with history preservation and dependency mapping.
  *Use when*: "migrate repo", "move repository", "transfer project"  
  *Location*: `git/migrate-repo/SKILL.md`

- **repo-briefing** - Generate comprehensive codebase overview with architecture analysis and key insights.
  *Use when*: "analyze repo", "codebase overview", "understand project"  
  *Location*: `git/repo-briefing/SKILL.md`

### 🔍 Analysis: Code Quality (3)
*Inspect codebases for quality, security, and maintainability*

- **api-contract-sniffer** - Show API surface by finding route declarations (REST endpoints).
  *Use when*: "show api surface", "find endpoints", "api analysis"  
  *Location*: `analysis/code/api-contract-sniffer/SKILL.md`

- **dead-code-hunter** - Find potentially unused functions, classes, and exports by comparing declarations to imports.
  *Use when*: "find dead code", "unused code", "cleanup analysis"  
  *Location*: `analysis/code/dead-code-hunter/SKILL.md`

- **dependency-audit** - List top-level runtime dependencies from package files with security insights.
  *Use when*: "audit deps", "check dependencies", "dependency analysis"  
  *Location*: `analysis/code/dependency-audit/SKILL.md`

### 📐 Analysis: Formal Verification (4)
*Formal verification and proof system analysis (Coq, Lean, etc.)*

- **anti-pattern-sniffer** - Find fragile Coq proof patterns and suggest improvements for robust proofs.
  *Use when*: "coq anti-patterns", "proof quality", "formal verification issues"  
  *Location*: `analysis/formal/anti-pattern-sniffer/SKILL.md`

- **lemma-dependency-graph** - Show most-applied lemmas in Coq proofs with usage frequency analysis.
  *Use when*: "lemma graph", "proof dependencies", "tactic analysis"  
  *Location*: `analysis/formal/lemma-dependency-graph/SKILL.md`

- **proof-obligations-snapshot** - Show admitted/open Coq proofs with progress tracking and completion status.
  *Use when*: "coq obligations", "open proofs", "proof progress"  
  *Location*: `analysis/formal/proof-obligations-snapshot/SKILL.md`

- **tactic-usage-count** - Count Coq tactic usage frequency for proof optimization and style analysis.
  *Use when*: "tactic census", "proof statistics", "tactic analysis"  
  *Location*: `analysis/formal/tactic-usage-count/SKILL.md`

### 📁 Root Level Skills (3)
*Skills in root directory (legacy/uncategorized)*

- **diff-summariser** - Summarize code changes without reading entire diffs.
  *Use when*: "summarize diff", "show changes"  
  *Location*: `diff-summariser/SKILL.md`

- **migrate-repo** - Comprehensive repository migration with history preservation.
  *Use when*: "migrate repo", "move repository"  
  *Location*: `migrate-repo/SKILL.md`

- **refactoring** - Safe code restructuring with dependency analysis and validation.
  *Use when*: "refactor code", "restructure", "modernize"  
  *Location*: `refactoring/SKILL.md`

- **repo-briefing** - Generate comprehensive codebase overview and analysis.
  *Use when*: "analyze repo", "codebase overview"  
  *Location*: `repo-briefing/SKILL.md`

## 🚀 Usage Patterns

### Common Workflows
1. **Before Major Work**: `/session-snapshot` → do work → `/session-snapshot`
2. **Code Review**: `/diff-summariser` → `/repo-briefing` 
3. **Analysis**: Choose category → pick specific skill
4. **Skill Creation**: Use workflow → `/skill-extractor` → test new skill

### Auto-Detection Triggers
- Mentioning "skills", "capabilities", "what can you do" → Show this manifest
- Task-related keywords → Suggest relevant skills
- Session patterns → Propose `/session-snapshot`

## 📊 Skill Statistics

- **Total Skills**: 16+ active skills
- **Categories**: 6 (Meta, Development, Git, Analysis/Code, Analysis/Formal, Root)
- **Token Range**: 300-1000+ tokens per invocation
- **Coverage**: Code quality, development workflows, git operations, formal verification, system improvement

## 🔧 Skill Development

### Creating New Skills
1. Use `/skill-extractor` to formalize workflows
2. Manual creation: Choose category → create directory → add SKILL.md
3. Test thoroughly before adding to manifest

### Maintenance
- Run manifest generator after adding new skills
- Categories expand as new skill types emerge
- Deprecated skills are moved to archive section

---

**💡 Pro Tip**: Start with `/session-snapshot` before long tasks, use `/skill-extractor` to capture useful workflows, and check this manifest when exploring capabilities!

*Generated on 2026-01-07*