# Skill Extractor Meta-Skill - Usage Guide

## Overview

The `skill-extractor` meta-skill analyzes extended Claude Code sessions to identify recurring workflows and extract them into reusable skill definitions. Transforms ad-hoc procedures into formalized, reusable skills that can be invoked by name in future sessions.

**Token Efficiency**: ~1.5K tokens vs 5K+ manual workflow formalization (70% reduction)

## Quick Start

### Natural Language Invocation
```
"Extract the workflow we just did into a skill"
"Create a skill from this repetitive process"
"Formalize this multi-step procedure we keep doing"
```

### Direct Skill Invocation
```
/skill-extractor
```

## When to Use

✅ **Workflow Repetition**:
- After 15+ message exchanges with repeated manual patterns
- When you notice yourself doing the same multi-step workflow multiple times
- User says: "extract workflow", "create skill from session", "formalize this pattern"

✅ **Procedure Standardization**:
- Converting ad-hoc processes into reusable procedures
- Documenting successful approaches for future use
- Creating team standards for common tasks
- Building institutional knowledge

✅ **Skill Development**:
- Identifying patterns worth formalizing
- Creating domain-specific workflows
- Building specialized tools for your project
- Extending Claude Code capabilities

## Analysis Process

### Step 1: Session History Analysis
Reviews the conversation and identifies:
- Repeated tool sequences (e.g., always Grep → Read → Edit → Bash test)
- Decision patterns (e.g., "if test fails, do X; else do Y")
- Manual workflows that could be automated
- Domain-specific procedures (e.g., "always check X before Y in this codebase")

### Step 2: Pattern Recognition
Identifies extractable patterns by asking:
- Has this workflow been done 2+ times in this session?
- Would it save effort if formalized?
- Is it general enough to reuse across sessions?
- Is it scoped to <1000 tokens execution?

### Step 3: Workflow Components Extraction
Documents the pattern as:

```markdown
**Workflow Name**: [descriptive-name]

**Trigger**: [when to invoke this]

**Steps**:
1. [Tool/action] - [purpose]
2. [Tool/action] - [purpose]
3. Decision: if [condition] then [branch A] else [branch B]
4. [Tool/action] - [purpose]

**Inputs**: [what user provides]
**Outputs**: [what skill produces]
**Token Budget**: ~[estimate] tokens
```

### Step 4: Skill Generation
Uses the template to create a new skill:

1. Choose skill category: `analysis/code`, `analysis/formal`, `development`, `git`, or `meta`
2. Create directory: `~/.claude/skills/[category]/[skill-name]/`
3. Generate `SKILL.md` following the template structure
4. Include:
   - Clear purpose (1-2 sentences)
   - Trigger conditions (when to invoke)
   - Step-by-step instructions
   - Anti-patterns to avoid
   - Example usage

### Step 5: Validation & Presentation
Before finalizing:
- Verifies it solves a real recurring problem
- Ensures steps are clear and actionable
- Confirms another Claude Code session could execute it without context
- Validates it's scoped to <1000 tokens execution

Shows the user:

```markdown
## Extracted Skill: [name]

**Category**: [analysis/code | development | git | meta]
**Purpose**: [1-line description]

**Workflow Pattern Detected**:
- Seen [N] times in this session
- Average [X] steps per invocation
- Est. token savings: [Y] per future use

**Generated files**:
- `~/.claude/skills/[category]/[skill-name]/SKILL.md`

**Test command**: `/[skill-name]` or reference in future sessions
```

## Example Usage

### Example 1: API Testing Workflow
```
User: We've tested APIs the same way 3 times now. Extract this workflow.

Claude: 🔍 Analyzing session for extractable workflow patterns...

📊 Pattern Analysis:
- Workflow occurrences: 3 times
- Average steps per execution: 6
- Estimated token savings: 400 tokens per use
- Pattern confidence: High

🎯 Extracted Skill: api-test-workflow

**Category**: analysis/code
**Purpose**: Systematic API endpoint testing with validation

**Workflow Pattern Detected**:
- Seen 3 times in this session
- Average 6 steps per invocation
- Est. token savings: 400 per future use

**Generated Skill**:
- `~/.claude/skills/analysis/code/api-test-workflow/SKILL.md`

**Test command**: `/api-test-workflow`

💡 Usage:
"Test the user authentication API endpoints" or "/api-test-workflow"
```

### Example 2: Security Audit Pattern
```
User: Extract the security audit workflow we just completed

Claude: 🔍 Analyzing security audit session patterns...

📊 Pattern Analysis:
- Workflow occurrences: 4 times across 28 messages
- Complexity: Medium-High (8 steps average)
- Domain specificity: High (security-focused)
- Extraction value: Very High

🎯 Extracted Skill: security-audit-workflow

**Category**: analysis/code
**Purpose**: Comprehensive security vulnerability assessment

**Workflow Pattern Detected**:
- Seen 4 times in this session
- Average 8 steps per invocation  
- Est. token savings: 650 per future use

**Generated files**:
- `~/.claude/skills/analysis/code/security-audit-workflow/SKILL.md`

**Test command**: `/security-audit-workflow`

⚠️ Security Focus: This workflow handles sensitive security analysis
```

### Example 3: Refactoring Pattern Extraction
```
User: We keep doing similar refactoring. Create a skill for this pattern.

Claude: 🔍 Detecting refactoring workflow patterns...

📊 Pattern Recognition:
- Pattern type: "Extract service layer from controller"
- Occurrences: 5 instances in session
- Consistency: High (similar structure each time)
- Complexity: Medium (6-8 steps)
- Generalizability: High (applicable to many controllers)

🎯 Extracted Skill: extract-service-layer

**Category**: development
**Purpose**: Systematically extract business logic to service layer

**Workflow Pattern Detected**:
- Seen 5 times in this session
- Average 7 steps per invocation
- Est. token savings: 500 per future use

**Generated Skill**:
- `~/.claude/skills/development/extract-service-layer/SKILL.md`

**Test command**: `/extract-service-layer`

🏗️ Architecture Impact: This creates more maintainable, testable code structure
```

## Example Session Patterns to Extract

### Pattern 1: "Test-Driven Refactoring"
```
Grep for function → Read implementation → Edit with refactor →
Run tests → If fail, revert and try alternative → If pass, commit
```

### Pattern 2: "Security Audit Loop"
```
Grep for auth/validation → Read each file → Check for OWASP patterns →
Document findings → Suggest fixes → Verify fixes don't break tests
```

### Pattern 3: "Dependency Update Workflow"
```
Read package.json → Check for outdated deps → Update one-by-one →
Run tests after each → If break, pin previous version → Document breaking changes
```

### Pattern 4: "API Documentation Generator"
```
Find API endpoints → Read route definitions → Extract parameter requirements →
Generate OpenAPI spec → Create example requests → Validate against implementation
```

### Pattern 5: "Performance Profiling Sequence"
```
Identify slow endpoints → Add timing middleware → Generate load test →
Profile with cProfile → Analyze bottlenecks → Suggest optimizations → Verify improvements
```

## Anti-Patterns

❌ Don't extract one-time operations
❌ Don't create skills for trivial 1-2 step tasks
❌ Don't extract workflows that are highly context-specific
❌ Don't create skills that require >1000 tokens execution

✅ Extract workflows repeated 2+ times
✅ Extract multi-step procedures (4+ steps)
✅ Extract patterns with decision logic
✅ Extract domain-specific but generalizable workflows

## Token Efficiency

- Analysis phase: 200-500 tokens
- Skill generation: 300-800 tokens
- Total: <1500 tokens
- Future usage savings: 60-80% per invocation

## Skill Categories

### 🔍 Analysis Skills
Code inspection and analysis:
- Security vulnerability detection
- Performance bottleneck identification
- Code quality assessment
- Architecture analysis

### ⚙️ Development Skills
Development workflows:
- Refactoring procedures
- Testing strategies
- Debugging sequences
- Optimization workflows

### 📁 Git Skills
Version control workflows:
- Repository analysis
- Change management
- Release procedures
- Collaboration patterns

### 🧠 Meta Skills
Self-improvement workflows:
- Skill extraction (this skill!)
- Session management
- Pattern recognition
- Workflow optimization

## Configuration Options

**Analysis Scope**:
- `--recent=N`: Analyze last N messages only
- `--pattern=type`: Focus on specific pattern types
- `--min-occurrences=N`: Minimum repetitions required

**Extraction Criteria**:
- `--complexity=level`: Minimum complexity threshold
- `--generalizability=level`: How reusable should it be
- `--domain-specific`: Allow domain-specific patterns

**Output Control**:
- `--auto-create`: Create skill immediately
- `--preview-only`: Show what would be created
- `--detailed-analysis`: Show detailed pattern analysis

## Integration with Development

**During Active Development**:
```
1. Work on complex multi-step task
2. Notice repetition of manual patterns
3. /skill-extractor (identify extraction opportunity)
4. Continue with extracted skill available
```

**Post-Session Analysis**:
```
1. Complete extended development session
2. Review conversation for patterns
3. /skill-extractor (extract reusable workflows)
4. Build skill library for future use
```

**Team Knowledge Building**:
```
1. Multiple team members use similar patterns
2. Extract team-standard workflows
3. Share extracted skills across team
4. Build institutional knowledge base
```

## Quality Validation

### Before Extraction
Validate extraction value:
- Pattern occurs ≥2 times
- Saves significant tokens (>200 per use)
- Generalizable beyond current context
- Actionable by other Claude instances

### After Creation
Test extracted skill:
- Try `/skill-name` in new session
- Verify it produces expected results
- Check token usage efficiency
- Refine if necessary

### Maintenance
Keep skills current:
- Update as patterns evolve
- Remove obsolete skills
- Enhance with new learnings
- Share improvements with team

## Best Practices

### 1. Pattern Recognition
Look for genuine repetition:
- Similar tool sequences
- Repeated decision points
- Common problem-solving approaches
- Standard validation procedures

### 2. Generalization
Make patterns reusable:
- Remove project-specific details
- Parameterize variable inputs
- Focus on core logic
- Document assumptions

### 3. Documentation
Create clear instructions:
- Simple, actionable steps
- Clear trigger conditions
- Specific examples
- Expected outcomes

### 4. Testing
Validate effectiveness:
- Test in isolation
- Verify token efficiency
- Check result quality
- Gather feedback

## Success Metrics

### Extraction Quality
Measure skill value:
- Usage frequency
- Token savings achieved
- User satisfaction
- Error rates

### Pattern Recognition
Assess detection accuracy:
- True positive rate
- False positive minimization
- Missed opportunities
- User feedback

## Advanced Features

### Pattern Evolution
Track pattern changes:
- Version extracted skills
- Update with improvements
- Deprecate obsolete patterns
- Maintain pattern history

### Team Collaboration
Share across teams:
- Export skill definitions
- Import team standards
- Build organization playbook
- Create skill repositories

### Analytics Integration
Measure impact:
- Track skill usage
- Analyze efficiency gains
- Identify popular patterns
- Optimize extraction algorithms

## Troubleshooting

### Issue 1: No patterns detected
**Solution**: Ensure sufficient repetition (≥2 times) and complexity (≥4 steps)

### Issue 2: Patterns too context-specific
**Solution**: Generalize by removing project-specific details and parameterizing inputs

### Issue 3: Extracted skill doesn't work well
**Solution**: Test and refine the skill, simplify steps, clarify instructions

### Issue 4: Low usage of extracted skills
**Solution**: Promote awareness, demonstrate value, integrate into workflows

## Future Enhancements

### AI-Powered Pattern Detection
Advanced recognition:
- Machine learning pattern identification
- Semantic analysis of workflows
- Predictive skill suggestions
- Automatic optimization

### Collaborative Skill Building
Community features:
- Shared skill repositories
- Community skill ratings
- Collaborative refinement
- Version control integration

### Intelligent Skill Matching
Smart recommendations:
- Context-aware suggestions
- Automatic skill invocation
- Predictive workflow assistance
- Personalized skill libraries

---

**Ready to formalize your workflows?** Just tell Claude: "Extract this workflow into a skill" or "Create a skill from this pattern"!