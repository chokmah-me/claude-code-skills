# session-snapshot

**The Ultimate Claude Code Session Manager** - Capture, save, and resume complete Claude Code session contexts with intelligent metadata management.

## 🎯 Purpose

Never lose track of your Claude Code conversations again. session-snapshot provides comprehensive session management that preserves debugging contexts, analysis results, development progress, and multi-step workflows across conversations.

## 🚀 Key Features

- **📸 Complete Context Capture**: Save entire session states with conversation history, file contexts, and command outputs
- **🔄 Intelligent Resume**: Restore sessions with full context, including open files and working directories
- **💡 Smart Metadata**: Automatic tagging, categorization, and searchable session descriptions
- **🎯 Workflow Preservation**: Maintain complex multi-step processes across conversation breaks
- **🔍 Advanced Search**: Find sessions by tags, content, time periods, or custom metadata

## 📋 Usage

### Basic Session Management

```bash
# Start a new named session
claude skills use session-snapshot --action start --name "debug-production-issue"

# Save current session with tags
claude skills use session-snapshot --action save --tags "api,debug,production" --description "Investigating API timeout issues"

# List all saved sessions
claude skills use session-snapshot --action list

# Resume a specific session
claude skills use session-snapshot --action resume --name "debug-production-issue"

# Delete old sessions
claude skills use session-snapshot --action delete --name "old-debug-session"
```

### Advanced Features

```bash
# Auto-save every 10 minutes during active sessions
claude skills use session-snapshot --action enable-autosave --interval 600

# Search for sessions
claude skills use session-snapshot --action search --query "production debug"

# Export session for sharing
claude skills use session-snapshot --action export --name "debug-production-issue" --format json

# Import shared session
claude skills use session-snapshot --action import --file shared-session.json
```

## 🎛️ Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action | string | Yes | Action to perform: start, save, resume, list, delete, search, export, import |
| name | string | Conditional | Session name (required for start, save, resume, delete, export) |
| tags | string | No | Comma-separated tags for categorization |
| description | string | No | Detailed session description |
| query | string | Conditional | Search query (required for search action) |
| format | string | No | Export format: json, yaml, txt (default: json) |
| file | string | Conditional | Import file path (required for import action) |
| interval | int | No | Auto-save interval in seconds (default: 600) |

## 💡 Examples

### Debugging Session Management

```bash
# Start debugging session
claude skills use session-snapshot --action start --name "api-timeout-debug" --tags "api,timeout,debug"

# Work on debugging... then save progress
claude skills use session-snapshot --action save --name "api-timeout-debug" --description "Identified issue in database connection pool"

# Later, resume where you left off
claude skills use session-snapshot --action resume --name "api-timeout-debug"
```

### Multi-Step Analysis Workflow

```bash
# Start complex analysis
claude skills use session-snapshot --action start --name "performance-analysis" --tags "performance,optimization"

# Save intermediate results
claude skills use session-snapshot --action save --name "performance-analysis" --description "Completed initial profiling, identified 3 bottlenecks"

# Continue analysis days later
claude skills use session-snapshot --action resume --name "performance-analysis"
```

### Team Collaboration

```bash
# Export session for team member
claude skills use session-snapshot --action export --name "security-audit" --format json --output audit-session.json

# Team member imports session
claude skills use session-snapshot --action import --file audit-session.json --name "security-audit-continue"
```

## 🎁 Output

### Successful Operations
```json
{
  "status": "success",
  "action": "save",
  "session_name": "debug-production-issue",
  "timestamp": "2024-01-15T10:30:00Z",
  "metadata": {
    "tags": ["api", "debug", "production"],
    "description": "Investigating API timeout issues",
    "files_context": 12,
    "conversation_length": 45,
    "session_duration": "2h 15m"
  }
}
```

### Session List
```json
{
  "sessions": [
    {
      "name": "debug-production-issue",
      "created": "2024-01-15T08:15:00Z",
      "last_modified": "2024-01-15T10:30:00Z",
      "tags": ["api", "debug", "production"],
      "description": "Investigating API timeout issues"
    },
    {
      "name": "performance-analysis",
      "created": "2024-01-14T14:00:00Z",
      "last_modified": "2024-01-14T16:45:00Z",
      "tags": ["performance", "optimization"],
      "description": "Analyzing application performance bottlenecks"
    }
  ]
}
```

## ⚠️ Important Notes

- **Storage Location**: Sessions are stored in `~/.claude/sessions/` by default
- **Auto-Cleanup**: Old sessions (>30 days) are automatically archived
- **Size Limits**: Individual sessions limited to 50MB, archive older content
- **Privacy**: Sessions contain full conversation context - be mindful of sensitive data
- **Compatibility**: Works best with Claude Code v1.0+, some features require v1.2+

## 🔄 Integration with Other Skills

### With skill-extractor
```bash
# Extract reusable skills from saved sessions
claude skills use skill-extractor --source-session "debug-production-issue"
```

### With workflow-automator
```bash
# Create automated workflows that preserve session context
claude skills use workflow-automator --session "performance-analysis" --steps "profile,optimize,validate"
```

### With productivity-tracker
```bash
# Track time spent in different session types
claude skills use productivity-tracker --analyze-sessions --category debug
```

## 🛠️ Advanced Configuration

### Custom Storage Backend
```bash
# Configure cloud storage for session backup
export CLAUDE_SESSION_STORAGE="s3://my-bucket/claude-sessions/"
export CLAUDE_SESSION_ENCRYPTION="aes256"
```

### Session Templates
```bash
# Create reusable session templates
claude skills use session-snapshot --action create-template --name "debug-template" --tags "debug,template"

# Start session from template
claude skills use session-snapshot --action start --template "debug-template"
```

## 🚨 Troubleshooting

### Common Issues

**Session not found**: Verify session name and check `session-snapshot --action list`
**Permission denied**: Ensure write access to `~/.claude/sessions/`
**Out of storage**: Archive or delete old sessions, increase storage limits
**Import failed**: Check file format and compatibility with current version

### Debug Mode
```bash
# Enable debug logging
export CLAUDE_SESSION_DEBUG="true"
claude skills use session-snapshot --action list
```

## 📊 Statistics and Analytics

Session-snapshot provides detailed analytics:
- Total sessions saved
- Average session duration
- Most active time periods
- Popular tags and categories
- Storage usage trends

Access analytics:
```bash
claude skills use session-snapshot --action analytics --period 30d
```

---

**💡 Pro Tip**: Use session-snapshot with skill-extractor to build a knowledge base from your most successful debugging and analysis sessions!