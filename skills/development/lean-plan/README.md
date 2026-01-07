# Lean Plan Skill - Usage Guide

## Overview

The `lean-plan` skill provides token-efficient planning for software development tasks. Creates minimal, focused plans that maximize progress while minimizing token usage - perfect for long sessions or token-conscious development.

**Token Efficiency**: ~200 tokens vs ~800 comprehensive planning (75% reduction)

## Quick Start

### Natural Language Invocation
```
"Create a lean plan for this feature"
"Give me a minimal plan for refactoring"
"What's the most token-efficient approach?"
```

### Direct Skill Invocation
```
/lean-plan
```

## When to Use

✅ **Token-Conscious Scenarios**:
- Long development sessions (20+ messages)
- Complex multi-step projects
- Token budget approaching limits
- Quick planning needed

✅ **Efficiency Focus**:
- Rapid prototyping
- Spike solutions
- Proof-of-concept development
- Time-boxed exploration

✅ **Iterative Development**:
- Agile-style development
- Continuous adaptation
- Minimal upfront planning
- Frequent course correction

## Planning Process

### Phase 1: Essential Context Capture
Extracts minimum viable context:
- Core objective (1 sentence)
- Key constraints (≤3 items)
- Success criteria (1-2 statements)
- Risk factors (if critical)

### Phase 2: Minimal Step Generation
Creates essential steps only:
- 3-5 core steps maximum
- Clear, actionable items
- Logical dependencies
- Token-efficient descriptions

### Phase 3: Priority & Focus
Establishes clear priorities:
- Critical path identification
- Risk mitigation focus
- Value-maximizing sequence
- Flexibility preservation

### Phase 4: Adaptive Framework
Provides adaptation guidance:
- Success indicators
- Failure recovery
- Pivot triggers
- Next-step decisions

## Example Usage

### Example 1: Feature Development
```
User: "Create a lean plan for adding user authentication"

Claude: 🎯 Creating lean plan for user authentication...

📋 LEAN PLAN - User Authentication (Est. 8 tokens)

**Core Objective**: Add secure user authentication to existing API

**Key Constraints**:
- Must integrate with current JWT system
- Token budget: conserve for implementation
- Time: complete within session

**Essential Steps**:
1. ✅ Extend User model with auth fields (15 min)
2. ✅ Create login/register endpoints (30 min)  
3. ✅ Add JWT token generation (20 min)
4. ⏳ Implement middleware protection (25 min)
5. ⏳ Test with existing endpoints (20 min)

**Success Indicators**:
- Login returns valid JWT
- Protected endpoints require auth
- Tests pass

**Next Decision Point**: After step 3, evaluate if remaining budget sufficient for full implementation or need to simplify.

💡 Token Efficiency: 95% saved vs comprehensive plan
```

### Example 2: Refactoring Task
```
User: "Give me a minimal plan for refactoring this legacy code"

Claude: 🎯 Generating lean refactoring plan...

📋 LEAN PLAN - Legacy Code Refactoring (Est. 6 tokens)

**Core Objective**: Extract business logic from monolithic controller

**Critical Constraints**:
- Must preserve existing behavior
- Limited token budget for analysis
- Need working code quickly

**Essential Steps**:
1. ✅ Identify business logic sections (10 min)
2. ✅ Extract to service classes (40 min)
3. ⏳ Update controller to use services (20 min)
4. ⏳ Run tests to verify behavior (15 min)

**Risk Mitigation**:
- Keep original code commented during extraction
- Test after each extraction
- Commit frequently

**Pivot Triggers**:
- Tests failing after extraction → rollback and smaller steps
- Too complex → extract smaller pieces
- Running long → simplify scope

**Next Decision**: After step 2, assess if full extraction feasible or need to scope down.

⏱️ Total estimated: 85 minutes
🎯 Focus: Behavior preservation over perfection
```

### Example 3: Bug Fix Planning
```
User: "Quick plan for fixing this race condition"

Claude: 🚨 Creating lean plan for race condition fix...

📋 LEAN PLAN - Race Condition Fix (Est. 4 tokens)

**Problem**: Concurrent access causing data corruption

**Critical Path**:
1. ✅ Reproduce race condition (5 min)
2. ✅ Identify critical section (10 min)
3. ⏳ Add synchronization (15 min)
4. ⏳ Verify fix with tests (10 min)

**Success Criteria**:
- No more data corruption
- Performance acceptable (<10% impact)
- Tests pass concurrently

**Fallback Plan**:
If synchronization too complex → use simpler locking
If performance impact high → optimize critical section

**Immediate Next Step**: Reproduce the issue to confirm understanding

⚡ Focus: Quick fix over comprehensive solution
🎯 Priority: Data integrity first, performance second
```

## Planning Principles

### 🔪 Ruthless Prioritization
Keep only what matters:
- Critical path items only
- Risk mitigation essentials
- Success/failure indicators
- Nothing nice-to-have

### ⚡ Speed Over Perfection
Optimize for rapid progress:
- Quick wins first
- Imperfect but working
- Iterative improvement
- Continuous validation

### 🎯 Focus Preservation
Maintain clear direction:
- Single primary objective
- Minimal constraints
- Clear success criteria
- Regular course correction

### 🔄 Adaptive by Design
Built for change:
- Flexible steps
- Pivot triggers
- Continuous feedback
- Easy course correction

## Comparison with Comprehensive Planning

| Aspect | Lean Plan | Comprehensive Plan |
|--------|-----------|-------------------|
| Token Usage | 50-100 tokens | 400-800 tokens |
| Step Count | 3-5 steps | 8-15 steps |
| Detail Level | Essential only | Thorough |
| Planning Time | 2-3 minutes | 10-15 minutes |
| Flexibility | High | Medium |
| Best For | Token conservation | Complex projects |
| Adaptability | Built-in | Requires replanning |

## When NOT to Use

❌ **Avoid When**:
- Safety-critical systems (medical, aerospace)
- Compliance-required documentation
- Multi-team coordination needed
- Complex architectural decisions
- High-risk financial systems

✅ **Use Full Planning Instead**:
- Comprehensive requirements gathering
- Detailed risk analysis
- Full stakeholder alignment
- Complete documentation
- Thorough review processes

## Configuration Options

**Scope Control**:
- `--ultra-lean`: Minimal 2-3 steps only
- `--standard`: 3-5 balanced steps
- `--extended`: 5-7 steps with options

**Focus Areas**:
- `--speed`: Prioritize rapid completion
- `--quality`: Balance speed and quality
- `--risk`: Emphasize risk mitigation

**Adaptation Level**:
- `--rigid`: Fixed plan, minimal adaptation
- `--flexible`: Built-in pivot points
- `--adaptive`: Continuous course correction

## Integration with Development

**Session Management**:
```
1. Start: /lean-plan (establish direction)
2. Execute: Work on essential steps
3. Check: Reassess after each milestone
4. Adapt: Adjust based on learnings
5. Complete: Finish or create new lean plan
```

**Token Budget Management**:
```
Budget: 10,000 tokens remaining
Action: Use lean-plan for 100 tokens
Implementation: 9,900 tokens available
Result: 99% of tokens for actual work
```

**Continuous Adaptation**:
```
Reality: Steps taking longer than expected
Response: Simplify remaining steps
Alternative: Reduce scope while maintaining value
Focus: Deliver working solution within constraints
```

## Success Indicators

### Quantitative Metrics
- Steps completed on time
- Token budget maintained
- Working solution delivered
- Quality standards met

### Qualitative Indicators
- Clear direction throughout
- Confident decision-making
- Rapid problem resolution
- Stakeholder satisfaction

### Adaptation Triggers
- Steps consistently taking 2x+ estimated time
- New complexities discovered
- Requirements changing significantly
- Token budget running low

## Best Practices

1. **Start Essential**: Begin with absolute minimum
2. **Stay Focused**: Resist scope creep
3. **Adapt Quickly**: Pivot when needed
4. **Measure Progress**: Track completion rates
5. **Communicate Simply**: Clear, brief updates

## Common Pitfalls

### ❌ Over-Planning
Adding too much detail defeats the purpose:
- Solution: Stick to essential steps only
- Check: Can you explain plan in 30 seconds?

### ❌ Under-Communicating
Too minimal to be useful:
- Solution: Include success criteria and pivot triggers
- Check: Would someone else understand the approach?

### ❌ Rigidity
Sticking to plan when reality changes:
- Solution: Use pivot triggers and adapt quickly
- Check: Are you learning and adjusting?

## Token Efficiency Examples

**Feature Development**:
- Comprehensive: 650 tokens
- Lean: 85 tokens
- Savings: 87%

**Bug Fix**:
- Comprehensive: 400 tokens
- Lean: 45 tokens
- Savings: 89%

**Refactoring**:
- Comprehensive: 800 tokens
- Lean: 95 tokens
- Savings: 88%

## When to Upgrade to Full Planning

### Upgrade Triggers
- Solution complexity exceeds initial understanding
- Multiple stakeholders need detailed coordination
- Safety/regulatory requirements emerge
- Token budget becomes less critical

### Transition Process
1. Complete current lean plan phase
2. Assess remaining complexity
3. Switch to comprehensive planning
4. Document learnings from lean approach

## Related Skills

- `development/quick-test-runner` - Validate lean solutions quickly
- `development/refactoring` - Iterate on lean implementations
- `analysis/code/dead-code-hunter` - Clean up after rapid development
- `meta/session-snapshot` - Save lean plan progress

---

**Ready to move fast?** Just tell Claude: "Create a lean plan" or "Give me the minimal approach"!