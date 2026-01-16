---
name: refactoring
description: Systematic, safe code restructuring with comprehensive validation, testing, and rollback capabilities
---

# Refactoring Skill

## Description

Provides systematic, safe code restructuring capabilities with comprehensive validation. Handles complex refactorings while preserving behavior through built-in testing, rollback mechanisms, and step-by-step validation. Routes to specialized workflow templates based on refactoring type.

## Features

- **Safety-First Approach**: Automatic test execution before and after changes
- **Multiple Refactoring Types**: Extract, modernize, triage workflows
- **Rollback Capability**: Undo changes if tests fail
- **Token Efficient**: ~1.2K tokens vs ~3K manual refactoring (60% reduction)
- **Step-by-Step Validation**: Incremental changes with verification at each step
- **Workflow Routing**: Directs to specialized templates for different refactoring patterns

## Usage

### Natural Language Invocation
```
"Refactor this monolithic function into smaller pieces"
"Extract the business logic from this controller"
"Restructure this inheritance hierarchy"
"Modernize this legacy codebase"
"Triage and categorize code quality issues"
```

### Direct Skill Invocation
```
/refactoring
```

The skill analyzes your request and routes to the appropriate workflow template in the `workflows/` directory:
- **extract.md**: Extract functions/methods to new modules
- **modernize.md**: Update legacy code to modern patterns
- **triage.md**: Categorize and prioritize code quality issues

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| target | string | Yes | Code location to refactor (file path, function name, or code block) |
| refactoring_type | string | No | Specific type: "extract", "modernize", "triage" (auto-detected if not specified) |
| preserve_behavior | boolean | No | Ensure behavior preservation (default: true) |
| run_tests | boolean | No | Execute tests before/after (default: true) |
| incremental | boolean | No | Apply changes incrementally with validation (default: true) |

## Examples

### Example 1: Extract Method Refactoring
```
User: "Extract the validation logic from this user controller into a separate validator class"

Claude: I'll use the refactoring skill to safely extract the validation logic.
[Routes to workflows/extract.md]
[Creates new validator class]
[Moves validation logic]
[Updates imports and references]
[Runs tests to verify behavior preserved]

Result: Validation logic extracted to UserValidator class, all tests passing
```

### Example 2: Modernize Legacy Code
```
User: "Modernize this callback-based code to use async/await"

Claude: I'll use the refactoring skill to modernize the asynchronous patterns.
[Routes to workflows/modernize.md]
[Identifies callback patterns]
[Converts to promises/async-await]
[Updates error handling]
[Validates with tests]

Result: Modern async/await implementation, tests passing
```

### Example 3: Code Quality Triage
```
User: "Triage the code quality issues in this legacy module"

Claude: I'll use the refactoring skill to analyze and categorize issues.
[Routes to workflows/triage.md]
[Scans for anti-patterns]
[Categorizes by severity: critical, high, medium, low]
[Provides prioritized action plan]

Result: 15 issues found (3 critical, 5 high, 7 medium), prioritized remediation plan generated
```

## Output

The skill produces:
1. **Refactored Code**: Restructured code following best practices
2. **Test Results**: Before/after test execution results
3. **Change Summary**: Description of what was modified and why
4. **Validation Report**: Confirmation that behavior is preserved
5. **Rollback Instructions**: How to undo changes if needed

### Sample Output
```
✅ Refactoring Complete: Extract Validation Logic

Changes Applied:
- Created: src/validators/UserValidator.js (87 lines)
- Modified: src/controllers/UserController.js (-42 lines validation code)
- Updated: 3 import statements

Test Results:
- Before: 45/45 tests passing ✓
- After: 47/47 tests passing ✓ (2 new validator tests added)

Behavior Validation: ✓ All original functionality preserved

Rollback: git checkout src/controllers/UserController.js && rm src/validators/UserValidator.js
```

## Important Notes

### Safety Considerations
- **Always run tests**: The skill automatically runs tests before/after refactoring
- **Incremental changes**: Large refactorings are broken into validated steps
- **Rollback available**: All changes can be undone if issues arise
- **Preserve behavior**: Default mode ensures functionality is not altered

### When to Use
- Complex refactorings affecting multiple files
- Legacy code modernization
- Extract/split operations that require careful dependency management
- When test coverage exists to validate changes

### When NOT to Use
- Simple renaming (use IDE refactoring tools)
- Single-line changes
- Exploratory code modifications without tests

### Workflow Files
The skill routes to specialized templates in the `workflows/` directory:
- **workflows/extract.md**: Function/method extraction patterns
- **workflows/modernize.md**: Legacy code modernization patterns
- **workflows/triage.md**: Code quality assessment and prioritization

See `README.md` for detailed usage guide and comprehensive examples.

## 🔄 Integration with Other Skills

- **quick-test-runner**: Executes tests to validate refactorings
- **dead-code-hunter**: Identifies unused code before refactoring
- **session-snapshot**: Save state before major refactorings
- **lean-plan**: Plan complex multi-step refactoring sequences

## 🎯 Best Practices

1. **Test First**: Ensure test suite exists and passes before refactoring
2. **Small Steps**: Break large refactorings into incremental changes
3. **Save Snapshots**: Use session-snapshot before major restructuring
4. **Review Changes**: Examine diffs before committing
5. **Update Documentation**: Ensure docs reflect new structure

## 🚨 Troubleshooting

**Tests Failing After Refactoring**
- Review change summary for unintended modifications
- Check for missed import updates
- Use rollback instructions to undo changes
- Apply changes more incrementally

**Skill Routes to Wrong Workflow**
- Explicitly specify refactoring_type parameter
- Use more specific natural language description
- Invoke workflow file directly

**Performance Issues**
- Large codebases may require extended processing time
- Consider refactoring in smaller scopes
- Use incremental: false for faster execution (less safe)
