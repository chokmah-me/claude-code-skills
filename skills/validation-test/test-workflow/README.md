# Workflow Test Skill

## Overview
This skill is specifically designed to test the GitHub Actions workflow automation in the repository. It ensures that all validation and maintenance workflows are functioning correctly.

## Installation
This skill is part of the repository and doesn't require separate installation.

## Usage Examples
```bash
# Test full workflow validation
/test-workflow validation-type=full

# Test specific components
/test-workflow check=skill-template
/test-workflow check=readme-update
/test-workflow check=link-validation

# Run in diagnostic mode
/test-workflow mode=diagnostic
```

## Testing Coverage
This skill validates:
- ✅ Skill template structure
- ✅ README auto-update functionality
- ✅ Documentation link validation
- ✅ Skill consistency checking
- ✅ Changelog automation

## Token Optimization
The skill is designed with token efficiency in mind:
- Concise parameter names
- Focused validation logic
- Minimal redundant processing
- Efficient error reporting

## Workflow Integration
When this skill is added to the repository, it automatically triggers:
1. Skill template validation
2. README inventory updates
3. Documentation checks
4. Consistency verification

This ensures the automation pipeline is working correctly.