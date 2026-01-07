# Dead Code Hunter Skill - Usage Guide

## Overview

The `dead-code-hunter` skill analyzes codebases to find unused functions, classes, imports, variables, and other dead code that can be safely removed. Helps reduce codebase size and improve maintainability.

**Token Efficiency**: ~600 tokens vs ~1.5K manual inspection (60% reduction)

## Quick Start

### Natural Language Invocation
```
"Find unused functions in the utils module"
"Hunt for dead code in the authentication service"
"Clean up unused imports in the data layer"
```

### Direct Skill Invocation
```
/dead-code-hunter
```

## What It Hunts

✅ **Function-Level Dead Code**:
- Unused functions and methods
- Unreachable code blocks
- Private methods never called
- Event handlers without bindings

✅ **Variable-Level Dead Code**:
- Unused local variables
- Class attributes never accessed
- Constants never referenced
- Parameters with default values never used

✅ **Import-Level Dead Code**:
- Unused imports and requires
- Duplicate imports
- Import aliases never used
- Star imports (`from module import *`)

✅ **Class-Level Dead Code**:
- Unused classes and interfaces
- Abstract methods never implemented
- Extension points never extended
- Mixins never mixed in

## Analysis Process

### Phase 1: Symbol Discovery
Identifies all defined symbols:
- Functions, methods, and procedures
- Classes, interfaces, and types
- Variables and constants
- Imports and dependencies

### Phase 2: Reference Analysis
Tracks all symbol usage:
- Direct calls and invocations
- Dynamic references (strings, reflection)
- Configuration-based usage
- Test file references

### Phase 3: Dead Code Detection
Compares definitions vs usage:
- Zero-reference symbols
- Reachability analysis
- Entry point analysis
- Configuration analysis

### Phase 4: Safety Verification
Validates removal safety:
- Public API checks
- Framework integration points
- Plugin/extension points
- Reflection usage

### Phase 5: Cleanup Report
Generates actionable report:
- Safe-to-remove items
- Conditional removal candidates
- Manual review required items
- Estimated impact metrics

## Example Usage

### Example 1: Utility Module Cleanup
```
User: "Find dead code in the utils module"

Claude: 🔍 Hunting for dead code in utils module...

📊 Analysis Results:
- Total symbols: 47 functions, 12 classes
- References found: 156 usage points
- Analysis time: 2.3 seconds

🎯 Dead Code Found:

SAFE TO REMOVE (12 items):
1. function: calculate_legacy_tax()
   Location: utils/financial.py:45-67
   Last reference: None (never used)
   Size: 23 lines
   
2. class: DeprecatedFormatter
   Location: utils/string_utils.py:89-134
   Last reference: Removed in commit abc123
   Size: 46 lines
   
3. import: from datetime import timezone
   Location: utils/__init__.py:12
   Issue: Import unused, timezone not referenced
   
REQUIRES REVIEW (3 items):
1. function: process_webhook_data()
   Location: utils/webhooks.py:78-95
   Issue: Only referenced in configuration file
   Action: Check if config is active

💾 Estimated Savings:
- Lines of code: 234 lines
- File size: ~8.2 KB
- Maintenance burden: -15% complexity
```

### Example 2: Large Codebase Analysis
```
User: "Analyze the entire backend for dead code"

Claude: 🔍 Scanning backend codebase for dead code...

📈 Analysis Summary:
- Files analyzed: 127 Python files
- Total symbols: 1,847 functions/classes
- Reference points: 3,291 usage locations
- Processing time: 8.7 seconds

🚨 High-Impact Dead Code:
1. Module: auth/legacy_auth.py (entire file)
   Size: 234 lines
   Issue: Superseded by oauth2 implementation
   Safety: ✅ Safe to remove (confirmed unused)
   
2. Function: deprecated_api_wrapper()
   Locations: 12 files
   Issue: Migration to v2 API complete
   Safety: ✅ Safe to remove

⚠️ Medium-Impact Candidates:
1. Configuration classes in config/
   Issue: Only referenced in default configs
   Action: Verify production usage
   
2. Debug utility functions
   Issue: Development-only code
   Action: Consider conditional compilation

📊 Code Quality Impact:
- Potential LOC reduction: 1,247 lines
- Complexity reduction: 18%
- Test coverage improvement: +5.2%
```

## Safety Levels

### 🟢 Safe to Remove
- Zero references across entire codebase
- Marked as deprecated/obsolete
- Only referenced in dead code itself
- Confirmed unused by runtime analysis

### 🟡 Conditional Removal
- Referenced only in configuration
- Test-only usage
- Development/debug code
- Seasonal/conditional features

### 🔴 Manual Review Required
- Public API surface
- Plugin/extension points
- Framework integration code
- Dynamic/referenced by name

## Supported Languages

✅ **Primary Support**:
- Python (functions, classes, imports)
- JavaScript/TypeScript (functions, classes, requires)
- Java (methods, classes, imports)
- C# (methods, classes, usings)

✅ **Import/Dependency Analysis**:
- Python: `import`, `from ... import`
- JS/TS: `require`, `import`, `export`
- Java: `import`, `package`
- C#: `using`, `namespace`

⚠️ **Limited Support**:
- Dynamic imports/requires
- Reflection-based usage
- Configuration-driven code
- Template-generated code

## Configuration Options

**Analysis Scope**:
- `--include-tests`: Include test files in analysis
- `--exclude-configs`: Skip configuration files
- `--depth=3`: Limit analysis depth for large codebases

**Safety Thresholds**:
- `--aggressive`: Find more potential dead code
- `--conservative`: Only obvious dead code
- `--safe-only`: Zero-risk recommendations only

**Output Control**:
- `--format=detailed`: Show full analysis
- `--format=summary`: Quick overview only
- `--format=commands`: Generate removal commands

## Integration with Development Workflow

**Pre-Refactoring**:
```
1. /dead-code-hunter (baseline)
2. Plan refactoring approach
3. Remove dead code first
4. Perform main refactoring
```

**Code Review Process**:
```
1. Developer runs /dead-code-hunter
2. Reviews suggested removals
3. Implements safe deletions
4. Documents conditional cases
```

**Maintenance Schedule**:
```
- Monthly: Run on actively developed modules
- Quarterly: Full codebase analysis
- Pre-release: Cleanup before major releases
```

## Automated Cleanup

**Safe Removal Mode**:
```
/dead-code-hunter --auto-remove-safe
# Automatically removes only safe items
```

**Preview Mode**:
```
/dead-code-hunter --dry-run
# Show what would be removed without changes
```

**Selective Cleanup**:
```
/dead-code-hunter --remove-types=imports,variables
# Only remove specific types of dead code
```

## Common Patterns & Solutions

### Pattern 1: Legacy Code Retention
**Issue**: Old code kept "just in case"
**Solution**: Use version control history instead

### Pattern 2: "Might Need Later" Code
**Issue**: Code kept for potential future use
**Solution**: Create feature branches or documentation

### Pattern 3: Commented-Out Code
**Issue**: Large blocks of commented code
**Solution**: Remove entirely (preserved in git history)

### Pattern 4: Debug/Development Code
**Issue**: Development utilities in production code
**Solution**: Move to development tools or conditional compilation

## Best Practices

1. **Regular Cleanup**: Don't let dead code accumulate
2. **Version Control**: Trust git to preserve history
3. **Incremental Removal**: Remove in small, testable chunks
4. **Documentation**: Document why code was removed
5. **Team Communication**: Coordinate cleanup with team

## Safety Guidelines

**Before Removing**:
- ✅ Verify no references in codebase
- ✅ Check configuration files
- ✅ Review test coverage
- ✅ Consider public API impact

**After Removing**:
- ✅ Run full test suite
- ✅ Verify build still works
- ✅ Check deployment processes
- ✅ Monitor for runtime issues

## Token Efficiency

- Small module (10 files): ~300 tokens
- Medium module (50 files): ~600 tokens
- Large codebase (200+ files): ~1,200 tokens
- Cleanup generation: ~150 tokens

## Related Skills

- `analysis/code/api-contract-sniffer` - Check API consistency
- `analysis/code/dependency-audit` - Find unused dependencies
- `development/refactoring` - Safe code restructuring
- `git/diff-summariser` - Review cleanup changes

---

**Ready to hunt?** Just tell Claude: "Find dead code in [module]" or "Clean up unused code in my project"!