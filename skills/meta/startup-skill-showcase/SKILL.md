# Startup Skill Showcase Meta-Skill

---
name: startup-skill-showcase
description: Intuitive skill discovery and showcase system that presents your available Claude Code skills at startup, with special emphasis on meta-skills and useful workflows. Provides easy access to skill documentation and usage examples.
---

# Startup Skill Showcase System

## Purpose
Provides an intuitive, visually appealing showcase of all available Claude Code skills at startup, with special emphasis on meta-skills like session-snapshot, and organizes skills by usefulness and category for easy discovery by both users and agents.

## When to Invoke
- Automatically at Claude Code startup
- When user says: "show my skills", "what skills do I have", "list available skills"
- When agent needs to discover available capabilities
- When user wants skill recommendations

## Showcase Structure

### 🎯 Meta Skills (Essential - Show First)
**Critical for session management and productivity:**
- `session-snapshot` - Save/restore session state
- `skill-extractor` - Extract workflows into reusable skills
- `startup-skill-showcase` - This skill showcase system

### ⚡ Quick Start Skills (High Utility)
**Most commonly needed skills:**
- `lean-plan` - Token-efficient planning
- `quick-test-runner` - Fast development feedback
- `diff-summariser` - Review changes quickly
- `repo-briefing` - Understand codebase status

### 🔍 Analysis Skills (Code Quality)
- `api-contract-sniffer` - API validation
- `dead-code-hunter` - Find unused code
- `dependency-audit` - Security & updates
- `anti-pattern-sniffer` - Proof quality (formal)
- `lemma-dependency-graph` - Proof structure (formal)
- `proof-obligations-snapshot` - Track verification (formal)
- `tactic-usage-count` - Optimize proofs (formal)

### 🛠️ Development Skills (Coding)
- `refactoring` - Safe code restructuring

### 📁 Git Skills (Version Control)
- `migrate-repo` - Repository migration

## Startup Display Format

### Welcome Header
```
🚀 Welcome to Claude Code! Your skills are ready.

📊 Skill Inventory: [X] skills available across [Y] categories
🎯 Meta Skills: 3 essential tools for session management
⚡ Quick Access: 4 high-utility skills for immediate use
🔍 Analysis: 7 code quality and formal verification tools
🛠️ Development: 1 safe refactoring skill
📁 Git: 1 repository management skill
```

### Featured Skills Section
```
⭐ FEATURED META SKILLS (Essential for Productivity):

🎯 session-snapshot
   Save/restore session state for long projects
   Usage: "Save a snapshot" or "/session-snapshot"
   Why: Never lose context on multi-day projects

🎯 skill-extractor  
   Turn repetitive workflows into reusable skills
   Usage: "Extract this workflow" or "/skill-extractor"
   Why: Automate your common development patterns

🎯 startup-skill-showcase
   This skill showcase system
   Usage: "Show my skills" or "/startup-skill-showcase"
   Why: Discover and access all your capabilities
```

### Quick Access Skills
```
⚡ QUICK ACCESS (Most Useful Skills):

🚀 lean-plan
   Token-efficient planning for complex tasks
   Usage: "Create a lean plan" or "/lean-plan"
   When: Starting complex projects with token constraints

⚡ quick-test-runner
   Fast feedback on code changes
   Usage: "Run quick tests" or "/quick-test-runner"  
   When: Need rapid validation during development

⚡ diff-summariser
   Understand changes without reading full diff
   Usage: "Summarize these changes" or "/diff-summariser"
   When: Reviewing PRs or understanding commits

⚡ repo-briefing
   Comprehensive repository health assessment
   Usage: "Brief me on this repo" or "/repo-briefing"
   When: Joining new projects or assessing codebase health
```

## Interactive Features

### Skill Discovery Commands
```
"Show all my skills" - Display complete inventory
"Show meta skills" - Focus on session management tools
"Show analysis skills" - Code quality and verification tools
"What should I use for [task]?" - Get skill recommendations
"Help me choose a skill" - Interactive skill selection
```

### Smart Recommendations
Based on context:
- **New project**: Recommend `lean-plan`, `repo-briefing`
- **Code changes**: Recommend `quick-test-runner`, `diff-summariser`
- **Long session**: Recommend `session-snapshot`
- **Repetitive work**: Recommend `skill-extractor`
- **API work**: Recommend `api-contract-sniffer`
- **Legacy code**: Recommend `dead-code-hunter`, `refactoring`

### Usage Examples by Scenario

#### Starting a New Project
```
"I'm starting a new feature with limited tokens"
→ Recommend: lean-plan, repo-briefing, session-snapshot

"Show me what I need to understand this codebase"
→ Recommend: repo-briefing, dead-code-hunter, api-contract-sniffer
```

#### During Development
```
"I just made changes, need quick validation"
→ Recommend: quick-test-runner, diff-summariser

"Working on a complex multi-step refactor"
→ Recommend: session-snapshot, refactoring, lean-plan
```

#### Code Review & Quality
```
"Reviewing a pull request"
→ Recommend: diff-summariser, api-contract-sniffer

"Want to improve code quality"
→ Recommend: dead-code-hunter, dependency-audit, refactoring
```

#### Formal Verification (if applicable)
```
"Working on Coq/Lean proofs"
→ Recommend: anti-pattern-sniffer, lemma-dependency-graph, 
            proof-obligations-snapshot, tactic-usage-count
```

## Implementation

### Step 1: Generate Skill Inventory
```python
def generate_skill_inventory():
    skills = {
        'meta': {
            'session-snapshot': {
                'purpose': 'Session state management',
                'usage': 'Save a snapshot before major changes',
                'priority': 'critical',
                'tokens': 400,
                'examples': ['Save a snapshot', '/session-snapshot']
            },
            'skill-extractor': {
                'purpose': 'Workflow formalization',
                'usage': 'Extract repetitive workflows into skills',
                'priority': 'high',
                'tokens': 1500,
                'examples': ['Extract this workflow', '/skill-extractor']
            }
        },
        'quick_access': {
            'lean-plan': {
                'purpose': 'Token-efficient planning',
                'usage': 'Plan complex tasks within token limits',
                'priority': 'high',
                'tokens': 200,
                'examples': ['Create a lean plan', '/lean-plan']
            }
        }
    }
    return skills
```

### Step 2: Create Visual Display
```python
def create_showcase_display(skills):
    display = f"""
🚀 Welcome to Claude Code! Your skills are ready.

📊 Skill Inventory: {count_total_skills(skills)} skills across {count_categories(skills)} categories
🎯 Meta Skills: {count_meta_skills(skills)} essential tools for session management
⚡ Quick Access: {count_quick_access_skills(skills)} high-utility skills for immediate use

⭐ FEATURED META SKILLS (Essential for Productivity):

{format_meta_skills(skills['meta'])}

⚡ QUICK ACCESS (Most Useful Skills):

{format_quick_access_skills(skills['quick_access'])}

💡 Commands: "Show all my skills" | "What should I use for [task]?" | "Help me choose"
"""
    return display
```

### Step 3: Interactive Recommendations
```python
def recommend_skills_for_task(task_description):
    task_lower = task_description.lower()
    
    if any(word in task_lower for word in ['test', 'validate', 'check']):
        return ['quick-test-runner', 'diff-summariser']
    elif any(word in task_lower for word in ['plan', 'organize', 'structure']):
        return ['lean-plan', 'session-snapshot']
    elif any(word in task_lower for word in ['refactor', 'restructure', 'clean']):
        return ['refactoring', 'dead-code-hunter']
    elif any(word in task_lower for word in ['security', 'vulnerability', 'audit']):
        return ['dependency-audit', 'api-contract-sniffer']
    elif any(word in task_lower for word in ['proof', 'coq', 'lean', 'formal']):
        return ['anti-pattern-sniffer', 'lemma-dependency-graph']
    else:
        return ['repo-briefing', 'skill-extractor']  # Default discovery
```

## Agent Discovery Interface

### Machine-Readable Format
```json
{
  "skills": {
    "meta": {
      "session-snapshot": {
        "purpose": "Session state management",
        "category": "meta",
        "tokens": 400,
        "trigger": "save snapshot|checkpoint|session state",
        "path": "~/.claude/skills/meta/session-snapshot/",
        "priority": "critical",
        "confidence": 0.95
      }
    },
    "quick_access": {
      "lean-plan": {
        "purpose": "Token-efficient planning",
        "category": "development",
        "tokens": 200,
        "trigger": "lean plan|minimal plan|token efficient",
        "priority": "high",
        "confidence": 0.88
      }
    }
  },
  "recommendations": {
    "new_project": ["lean-plan", "repo-briefing"],
    "code_changes": ["quick-test-runner", "diff-summariser"],
    "long_session": ["session-snapshot"],
    "repetitive_work": ["skill-extractor"]
  }
}
```

### Agent Commands
```
"List all skills in JSON format" - Machine-readable inventory
"What skills are available for automation?" - Agent-focused query
"Show skills by category" - Organized for programmatic access
"Recommend skills for autonomous operation" - Self-setup assistance
```

## Startup Integration

### Automatic Triggering
Showcase appears when:
- Claude Code session starts
- User enters new project directory
- After `/clear` or context reset
- When user seems lost ("help", "what can I do")

### Contextual Activation
Smart detection:
- New file types detected (offer relevant skills)
- Git status changes (suggest appropriate tools)
- Long session detected (recommend session-snapshot)
- Repetitive patterns (suggest skill-extractor)

## Usage Examples

### Example 1: Startup Display
```
[Claude Code starts]

🚀 Welcome to Claude Code! Your skills are ready.

📊 Skill Inventory: 14 skills across 5 categories
🎯 Meta Skills: 3 essential tools for session management
⚡ Quick Access: 4 high-utility skills for immediate use
🔍 Analysis: 7 code quality and formal verification tools
🛠️ Development: 1 safe refactoring skill
📁 Git: 1 repository management skill

⭐ FEATURED META SKILLS (Essential for Productivity):

🎯 session-snapshot
   Save/restore session state for long projects
   Usage: "Save a snapshot" or "/session-snapshot"
   Why: Never lose context on multi-day projects

🎯 skill-extractor  
   Turn repetitive workflows into reusable skills
   Usage: "Extract this workflow" or "/skill-extractor"
   Why: Automate your common development patterns

⚡ QUICK ACCESS (Most Useful Skills):

🚀 lean-plan
   Token-efficient planning for complex tasks
   Usage: "Create a lean plan" or "/lean-plan"
   When: Starting complex projects with token constraints

⚡ quick-test-runner
   Fast feedback on code changes
   Usage: "Run quick tests" or "/quick-test-runner"  
   When: Need rapid validation during development

💡 Commands: "Show all my skills" | "What should I use?" | "Help me choose"
```

### Example 2: Interactive Skill Selection
```
User: "What should I use for testing my changes?"

Claude: 🤔 Based on your context, I recommend:

🎯 For quick validation: quick-test-runner
   Runs fast tests on your recent changes
   Usage: "Run quick tests" or "/quick-test-runner"
   Why: You modified 2 Python files - perfect for rapid feedback

🔍 For comprehensive analysis: api-contract-sniffer
   Checks API changes for issues
   Usage: "Check API contracts" or "/api-contract-sniffer"
   Why: Validates your changes don't break API consistency

📊 For change review: diff-summariser
   Summarizes what you changed
   Usage: "Summarize my changes" or "/diff-summariser"
   Why: Helps you understand impact before testing

💡 Start with: "Run quick tests" - it's fast and will validate your changes immediately
```

### Example 3: Agent Self-Setup
```
Agent: "What skills should I use for autonomous operation?"

Claude: 🤖 Agent Skills Discovery:

🎯 Essential for Autonomy:
- session-snapshot: Save/restore state during long operations
- skill-extractor: Formalize successful patterns for reuse
- lean-plan: Efficient planning within token constraints

⚡ High-Value Automation:
- quick-test-runner: Validate changes automatically
- dead-code-hunter: Clean up code during refactoring
- dependency-audit: Monitor security automatically
- repo-briefing: Assess repository health

🔍 Analysis & Quality:
- api-contract-sniffer: Validate API consistency
- diff-summariser: Review changes efficiently
- refactoring: Safe code restructuring

Machine-readable format: "List skills in JSON format"
```

## Advanced Features

### Personalized Recommendations
Learn from usage:
- Track which skills user prefers
- Adapt showcase ordering
- Customize based on expertise level
- Learn from feedback

### Usage Analytics
Track effectiveness:
- Skill discovery rates
- Feature usage frequency
- User satisfaction scores
- Recommendation success rates

### Team Collaboration
Share across team:
- Standardize skill preferences
- Share successful patterns
- Build team skill libraries
- Collaborative skill development

## Best Practices

### 1. Clear Visual Hierarchy
- Use consistent icons and colors
- Group related skills together
- Highlight most important skills
- Provide clear navigation

### 2. Actionable Information
- Include specific usage examples
- Explain when to use each skill
- Provide confidence levels
- Offer next steps

### 3. Progressive Disclosure
- Start with essential information
- Offer more details on demand
- Don't overwhelm newcomers
- Layer complexity appropriately

### 4. Context Awareness
- Adapt to current situation
- Consider user experience level
- Offer relevant suggestions
- Time recommendations appropriately

## Success Metrics

### User Engagement
Measure effectiveness:
- Skill discovery rate
- Feature usage frequency
- User satisfaction scores
- Time to skill activation

### Agent Integration
Assess automation:
- Agent skill adoption
- Autonomous operation success
- Machine-readable format usage
- Self-setup completion rates

## Implementation Notes

### Performance Considerations
- Cache skill metadata for fast loading
- Lazy load detailed skill information
- Optimize for startup speed
- Minimize token usage

### Maintenance
Keep current:
- Update as new skills added
- Refresh skill metadata regularly
- Adapt to user feedback
- Evolve with usage patterns

---

**Ready to showcase your skills?** This system will make your Claude Code skills easily discoverable and intuitive to use for both humans and agents!