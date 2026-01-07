# debug-assistant

**Advanced Debugging and Error Analysis** - Intelligent debugging assistance with automated error detection, root cause analysis, and solution recommendations for faster problem resolution.

## 🎯 Purpose

Transform debugging from a tedious manual process into an intelligent, systematic approach. debug-assistant analyzes errors, traces execution paths, identifies root causes, and suggests proven solutions based on patterns from thousands of debugging sessions.

## 🚀 Key Features

- **🔍 Automated Error Detection**: Identifies and categorizes errors across multiple languages and frameworks
- **📊 Root Cause Analysis**: Traces error origins through call stacks and dependencies
- **💡 Intelligent Solutions**: Recommends fixes based on similar resolved issues
- **🔄 Interactive Debugging**: Step-by-step debugging guidance with checkpoints
- **📈 Performance Impact**: Analyzes how fixes affect system performance

## 📋 Usage

### Basic Error Analysis

```bash
# Analyze error from command output
python app.py 2>&1 | claude skills use debug-assistant --analyze

# Debug specific error message
claude skills use debug-assistant --error "ModuleNotFoundError: No module named 'requests'"

# Analyze log file for errors
claude skills use debug-assistant --log-file app.log --analyze-errors
```

### Advanced Debugging

```bash
# Debug with context
claude skills use debug-assistant --error "TypeError" --code-file main.py --line 45

# Interactive debugging session
claude skills use debug-assistant --interactive --error-file error.txt

# Performance debugging
claude skills use debug-assistant --performance --slow-query logs/slow.log
```

### Code-Specific Debugging

```bash
# Debug Python exceptions
cat traceback.txt | claude skills use debug-assistant --language python

# Debug JavaScript errors
claude skills use debug-assistant --error "Uncaught TypeError" --language javascript

# Debug database issues
claude skills use debug-assistant --database-error "connection timeout" --db-type postgresql
```

## 🎛️ Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| analyze | flag | No | Analyze error from stdin/input |
| error | string | Conditional | Specific error message to analyze |
| log-file | string | Conditional | Log file path for error analysis |
| code-file | string | No | Source code file for context |
| line | int | No | Line number where error occurred |
| language | string | No | Programming language: python, javascript, java, etc. |
| interactive | flag | No | Enable interactive debugging mode |
| error-file | string | Conditional | File containing error details |
| performance | flag | No | Enable performance-focused debugging |
| slow-query | string | Conditional | Slow query log file |
| database-error | string | Conditional | Database-specific error |
| db-type | string | No | Database type: postgresql, mysql, mongodb, etc. |

## 💡 Examples

### Python Debugging

```bash
# Analyze Python traceback
python manage.py runserver 2>&1 | claude skills use debug-assistant --language python

# Debug with code context
claude skills use debug-assistant --error "AttributeError: 'NoneType'" --code-file models.py --line 23

# Interactive debugging
claude skills use debug-assistant --interactive --error "ImportError: cannot import name"
```

### Web Development Debugging

```bash
# Debug JavaScript errors
claude skills use debug-assistant --error "ReferenceError: $ is not defined" --language javascript

# Debug API issues
claude skills use debug-assistant --error "500 Internal Server Error" --log-file nginx.log

# Debug CSS issues
claude skills use debug-assistant --error "Failed to load resource" --language css
```

### Database Debugging

```bash
# Debug connection issues
claude skills use debug-assistant --database-error "connection refused" --db-type postgresql

# Analyze slow queries
claude skills use debug-assistant --performance --slow-query logs/postgresql-slow.log

# Debug migration errors
claude skills use debug-assistant --error "django.db.utils.ProgrammingError" --language python
```

## 🎁 Output

### Error Analysis Report
```json
{
  "error_analysis": {
    "error_type": "ModuleNotFoundError",
    "error_message": "No module named 'requests'",
    "severity": "high",
    "language": "python",
    "likely_causes": [
      "Missing dependency installation",
      "Virtual environment not activated",
      "Package name typo in import"
    ],
    "suggested_fixes": [
      {
        "fix": "pip install requests",
        "confidence": 0.95,
        "explanation": "Install the missing requests package"
      },
      {
        "fix": "source venv/bin/activate",
        "confidence": 0.85,
        "explanation": "Activate virtual environment if packages are installed there"
      }
    ],
    "prevention": "Add requests to requirements.txt and use virtual environments"
  }
}
```

### Interactive Debugging Session
```json
{
  "debugging_session": {
    "current_step": 1,
    "total_steps": 5,
    "next_action": "Check if virtual environment is activated",
    "commands_to_try": [
      "which python",
      "pip list | grep requests",
      "python -c \"import sys; print(sys.path)\""
    ],
    "explanation": "Let's verify your Python environment setup",
    "checkpoints": [
      "Virtual environment active",
      "Package installation verified",
      "Import test successful"
    ]
  }
}
```

## ⚠️ Important Notes

- **Context Required**: Provide as much context as possible for accurate analysis
- **Language Detection**: Auto-detects language but explicit specification improves accuracy
- **Privacy**: Error analysis may include code snippets - review output before sharing
- **Complex Errors**: Multi-layered errors may require step-by-step debugging
- **Performance**: Large log files may take time to analyze

## 🔄 Integration with Other Skills

### With session-snapshot
```bash
# Save debugging session for future reference
claude skills use session-snapshot --action start --name "debug-api-issues"
claude skills use debug-assistant --error "API timeout" --log-file app.log
claude skills use session-snapshot --action save --tags "debug,api,timeout"
```

### With performance-profiler
```bash
# Debug performance issues
claude skills use performance-profiler --analyze app.py
claude skills use debug-assistant --performance --slow-query profile.log
```

### With code-quality-checker
```bash
# Check code quality issues that might cause bugs
claude skills use code-quality-checker --file buggy.py
claude skills use debug-assistant --code-file buggy.py --line 45
```

## 🛠️ Advanced Configuration

### Custom Debugging Rules
```bash
# Configure debugging preferences
export CLAUDE_DEBUG_PREFERENCES="verbose,step-by-step"
export CLAUDE_DEBUG_LANGUAGE="python"
export CLAUDE_DEBUG_MAX_SUGGESTIONS="5"
```

### Integration Settings
```bash
# Configure external tools
export CLAUDE_DEBUG_STACK_ANALYZER="enabled"
export CLAUDE_DEBUG_PERFORMANCE_DB="~/.claude/debug-performance.db"
```

### Team Debugging
```bash
# Share debugging knowledge
export CLAUDE_TEAM_DEBUG_MODE="enabled"
export CLAUDE_TEAM_DEBUG_SHARE="true"
```

## 🎯 Debugging Best Practices

### Error Reporting
1. **Provide full context** - Include relevant code, logs, and environment details
2. **Be specific** - Exact error messages and line numbers help accuracy
3. **Include steps to reproduce** - Helps identify root causes
4. **Mention recent changes** - New dependencies, code changes, configuration updates

### Interactive Debugging
1. **Follow the workflow** - Complete all suggested steps
2. **Test incrementally** - Verify each fix before proceeding
3. **Document solutions** - Save successful debugging sessions
4. **Share knowledge** - Contribute solutions back to the community

---

**💡 Pro Tip**: Combine debug-assistant with session-snapshot to build a knowledge base of debugging solutions for your most common issues!