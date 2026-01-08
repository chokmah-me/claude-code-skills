# Skill Recommendation Engine - Usage Guide

## Overview

The `skill-recommendation-engine` meta-skill analyzes your current workflow context and suggests the most relevant Claude Code skills to use. It intelligently matches your development tasks, code patterns, and session history with available skills to provide personalized recommendations.

**Use Cases**: Skill discovery, workflow optimization, productivity enhancement, team onboarding

## Quick Start

### Natural Language Invocation
```
"What skills should I use for this refactoring task?"
"Recommend skills for API development"
"I'm working on database optimization - any relevant skills?"
"Show me skills for security analysis"
```

### Direct Skill Invocation
```
/skill-recommendation-engine
```

## When to Use

✅ **Skill Discovery**:
- New to Claude Code skills ecosystem
- Unsure which skills exist for specific tasks
- Want to explore advanced capabilities
- Looking for workflow optimization opportunities

✅ **Contextual Assistance**:
- Starting complex development tasks
- Working with unfamiliar technologies
- Need specialized analysis or debugging
- Want to improve development efficiency

✅ **Team Onboarding**:
- Introducing team members to available tools
- Standardizing development workflows
- Creating skill usage guidelines
- Building team skill knowledge base

✅ **Workflow Optimization**:
- Repetitive manual tasks that could be automated
- Complex multi-step processes
- Time-consuming analysis procedures
- Error-prone manual operations

## Recommendation Process

### Step 1: Analyze Current Context
Extract relevant information from your session:

**Context Sources**:
- Recent conversation history (last 10-15 messages)
- File types and technologies mentioned
- Task descriptions and goals
- Error messages or challenges encountered
- Development phase (planning, coding, debugging, testing)

**Key Indicators**:
- Programming languages: Python, JavaScript, TypeScript, Java, etc.
- Frameworks: React, Django, Express, Spring, etc.
- Task types: Refactoring, debugging, testing, analysis, etc.
- File patterns: `.py`, `.js`, `.md`, `.json`, `.yml`, etc.
- Keywords: "optimize", "debug", "refactor", "analyze", "test", etc.

### Step 2: Match Against Skill Database
Compare context with available skills:

**Meta Skills** (for workflow management):
- `session-snapshot` - For long/complex sessions
- `skill-extractor` - For formalizing workflows
- `skill-recommendation-engine` - For discovering skills (recursive!)

**Development Skills** (for coding tasks):
- `lean-plan` - For token-efficient planning
- `quick-test-runner` - For testing workflows
- `refactoring` - For code restructuring

**Git Skills** (for version control):
- `diff-summariser` - For code review workflows
- `migrate-repo` - For repository management
- `repo-briefing` - For repository understanding

**Analysis Skills** (for code inspection):
- `api-contract-sniffer` - For API validation
- `dead-code-hunter` - For cleanup tasks
- `dependency-audit` - For security/maintenance
- `anti-pattern-sniffer` - For formal verification
- `lemma-dependency-graph` - For proof analysis
- `proof-obligations-snapshot` - For formal methods
- `tactic-usage-count` - For proof optimization

### Step 3: Generate Personalized Recommendations
Rank and present skills by relevance:

```markdown
## Recommended Skills for Your Context

### 🔥 High Priority (Immediate Use)
1. **[skill-name]** - [Brief description]
   - **Why**: [Specific reason based on your context]
   - **Usage**: `/skill-name` or "[natural language trigger]"
   - **Expected benefit**: [Time saved, quality improvement, etc.]

### ⚡ Medium Priority (Consider Soon)
2. **[skill-name]** - [Brief description]
   - **Why**: [Contextual reason]
   - **Usage**: `/skill-name`
   - **When**: [Specific scenario]

### 💡 Future Reference (Keep in Mind)
3. **[skill-name]** - [Brief description]
   - **Use case**: [When this would be valuable]
   - **Trigger**: [What to watch for]
```

## Real-World Examples

### Example 1: Web Development Project
**User Context**: "I'm building a REST API with Node.js and Express, need to validate the endpoints and check for security issues"

**Recommended Skills**:
```
🔥 High Priority:
1. api-contract-sniffer - Validate your API endpoints match specifications
   - Why: You're building REST API endpoints
   - Usage: /api-contract-sniffer
   - Expected benefit: Catch API contract violations early

⚡ Medium Priority:
2. dependency-audit - Check for vulnerable npm packages
   - Why: Node.js projects often have security vulnerabilities
   - Usage: /dependency-audit
   - When: Before deploying to production

3. quick-test-runner - Set up automated testing
   - Why: API endpoints need comprehensive testing
   - Usage: /quick-test-runner
   - When: After implementing endpoints
```

### Example 2: Legacy Code Refactoring
**User Context**: "I inherited a large Python codebase, need to clean it up and refactor safely"

**Recommended Skills**:
```
🔥 High Priority:
1. dead-code-hunter - Find unused functions and imports
   - Why: Legacy code often accumulates dead code
   - Usage: /dead-code-hunter
   - Expected benefit: Remove 20-30% of unused code

2. refactoring - Safe refactoring workflows
   - Why: Large codebase needs systematic refactoring
   - Usage: /refactoring
   - Expected benefit: Reduce introduction of bugs

⚡ Medium Priority:
3. session-snapshot - Save progress during long refactoring
   - Why: Refactoring sessions can span multiple days
   - Usage: /session-snapshot
   - When: Every major milestone
```

### Example 3: Formal Verification Work
**User Context**: "I'm working with Coq proofs and need to analyze the proof structure and dependencies"

**Recommended Skills**:
```
🔥 High Priority:
1. lemma-dependency-graph - Visualize proof dependencies
   - Why: Complex proofs have intricate dependency structures
   - Usage: /lemma-dependency-graph
   - Expected benefit: Understand proof architecture

2. proof-obligations-snapshot - Track unproven obligations
   - Why: Keep track of what still needs proof
   - Usage: /proof-obligations-snapshot
   - When: During active proof development

⚡ Medium Priority:
3. anti-pattern-sniffer - Detect proof anti-patterns
   - Why: Improve proof quality and maintainability
   - Usage: /anti-pattern-sniffer
   - When: Before finalizing proofs
```

## Advanced Usage

### Custom Recommendation Profiles
Create personalized skill sets for different workflows:

```markdown
## Development Profiles

### 🚀 Rapid Prototyping
Priority: speed over perfection
Skills: lean-plan, quick-test-runner, session-snapshot

### 🔍 Deep Analysis
Priority: thoroughness over speed  
Skills: dependency-audit, dead-code-hunter, repo-briefing

### 🛡️ Security Focus
Priority: security and safety
Skills: dependency-audit, api-contract-sniffer, anti-pattern-sniffer

### 📊 Data Science
Priority: analysis and visualization
Skills: [relevant analysis skills for data work]
```

### Team Skill Mapping
For development teams:

```markdown
## Team Skill Adoption Strategy

1. **Beginners** (0-3 months):
   - Start with: session-snapshot, skill-recommendation-engine
   - Focus: Basic workflow optimization

2. **Intermediate** (3-12 months):
   - Add: skill-extractor, lean-plan, quick-test-runner
   - Focus: Workflow formalization and efficiency

3. **Advanced** (12+ months):
   - Master: All skills in relevant categories
   - Focus: Custom skill creation and team sharing
```

## Token Efficiency

- **Context Analysis**: ~150-200 tokens
- **Skill Matching**: ~100-150 tokens  
- **Recommendation Generation**: ~200-300 tokens
- **Total**: ~450-650 tokens per recommendation session
- **Value**: Can save 1000+ tokens by using optimal skills vs manual approaches

## Integration with Other Skills

### With session-snapshot
```
/skill-recommendation-engine
# Get recommendations
/session-snapshot  
# Save recommendations for future reference
```

### With skill-extractor
```
/skill-recommendation-engine
# Discover useful skills
# Use recommended skills extensively
/skill-extractor
# Extract your new workflow into a custom skill
```

### With startup-skill-showcase
```
/skill-recommendation-engine
# Get personalized recommendations
/startup-skill-showcase
# Explore recommended skills in detail
```

## Troubleshooting

### Low Confidence Recommendations
If recommendations seem generic:
- Provide more specific context about your task
- Mention specific technologies, frameworks, or goals
- Describe the problem you're trying to solve

### Too Many Recommendations
If overwhelmed with options:
- Ask for "top 3 recommendations"
- Specify your current priority (speed, quality, learning)
- Focus on one category of skills at a time

### No Relevant Skills Found
If no skills seem applicable:
- Your use case might need manual approach
- Consider using skill-extractor to create custom skills
- Check back as new skills are added to the ecosystem

---

**Pro Tip**: The more context you provide, the better the recommendations. Don't hesitate to mention specific technologies, constraints, or goals!