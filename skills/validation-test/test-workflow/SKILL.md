---
version: 1.0.0
category: validation-test
tags: [workflow, test, validation]
---

# Workflow Test Skill

## Purpose:
This skill is designed to test the GitHub Actions workflow validation and ensure all automation is working correctly.

## Usage:
Use this skill by calling `/test-workflow` to validate that the GitHub Actions workflows are functioning properly.

## Examples:
```
/test-workflow validation-type=full
/test-workflow check=skill-template
/test-workflow mode=diagnostic
```

## Token Efficiency:
This skill is optimized for minimal token usage while providing comprehensive workflow validation. It uses efficient parameter parsing and focused validation logic.

## Workflow Testing:
This skill will trigger the following validations:
- Skill template structure validation
- README inventory updates
- Documentation link checking
- Skill consistency verification

## Notes:
- Created specifically for workflow testing
- Validates automation pipeline functionality
- Ensures proper error handling and reporting