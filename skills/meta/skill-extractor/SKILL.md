# Skill Extractor Meta-Skill

## Purpose
Analyze extended Claude Code sessions to identify recurring workflows and extract them into reusable skill definitions.

## When to Use
- After 15+ message exchanges with repeated manual patterns
- When you notice yourself doing the same multi-step workflow multiple times
- User says: "extract workflow", "create skill from session", "formalize this pattern"

## Instructions

### Step 1: Analyze Session History

Review the conversation and identify:
- **Repeated tool sequences** (e.g., always Grep → Read → Edit → Bash test)
- **Decision patterns** (e.g., "if test fails, do X; else do Y")
- **Manual workflows** that could be automated
- **Domain-specific procedures** (e.g., "always check X before Y in this codebase")

Ask yourself:
- Has this workflow been done 2+ times in this session?
- Would it save effort if formalized?
- Is it general enough to reuse across sessions?

### Step 2: Extract Workflow Components

Document the pattern as:

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

### Step 3: Generate Skill Definition

Use the template at `meta/skill-extractor/template.md` to create a new skill:

1. Choose skill category: `analysis/code`, `analysis/formal`, `development`, `git`, or `meta`
2. Create directory: `~/.claude/skills/[category]/[skill-name]/`
3. Generate `SKILL.md` following the template structure
4. Include:
   - Clear purpose (1-2 sentences)
   - Trigger conditions (when to invoke)
   - Step-by-step instructions
   - Anti-patterns to avoid
   - Example usage

### Step 4: Validate Extracted Skill

Before finalizing:
- [ ] Does it solve a real recurring problem?
- [ ] Are steps clear and actionable?
- [ ] Could another Claude Code session execute this without context?
- [ ] Is it scoped to <1000 tokens execution?

### Step 5: Present to User

Show the user:
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

## Anti-Patterns

❌ Don't extract one-time operations
❌ Don't create skills for trivial 1-2 step tasks
❌ Don't extract workflows that are highly context-specific

✅ Extract workflows repeated 2+ times
✅ Extract multi-step procedures (4+ steps)
✅ Extract patterns with decision logic

## Token Efficiency

- Analysis phase: 200-500 tokens
- Skill generation: 300-800 tokens
- Total: <1500 tokens

## Output Format

Create skill following this structure:

```markdown
# [Skill Name]

## Purpose
[1-2 sentence description]

## When to Use
- [Trigger condition 1]
- [Trigger condition 2]

## Instructions

### Step 1: [Name]
[Detailed instructions with tool calls]

### Step 2: [Name]
[More instructions]

## Anti-Patterns
❌ Don't [bad practice]
✅ Do [good practice]

## Token Efficiency
- [Phase]: [estimate] tokens
```
