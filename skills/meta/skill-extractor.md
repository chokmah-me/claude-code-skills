# skill-extractor

**Automated Skill Discovery & Documentation** - Intelligently extract reusable skills from your Claude Code conversations and build your personal skill library effortlessly.

## 🎯 Purpose

Transform your ad-hoc Claude Code solutions into reusable, documented skills. skill-extractor analyzes your conversation history, identifies patterns, and automatically generates properly formatted skills that you and your team can use repeatedly.

## 🚀 Key Features

- **🔍 Intelligent Pattern Recognition**: Automatically identifies reusable commands and workflows
- **📋 Auto-Documentation**: Generates comprehensive skill descriptions and usage examples
- **🏗️ Skill Library Builder**: Organizes extracted skills into categorized collections
- **🔄 Continuous Learning**: Improves extraction quality based on your usage patterns
- **👥 Team Sharing**: Export skills for team collaboration and knowledge sharing

## 📋 Usage

### Basic Skill Extraction

```bash
# Extract skills from recent conversations
claude skills use skill-extractor --source recent --limit 50

# Extract from specific conversation
claude skills use skill-extractor --source-conversation "debug-session-123"

# Extract from file or directory
claude skills use skill-extractor --source-file ~/claude-history/debug.log
claude skills use skill-extractor --source-dir ~/.claude/history/
```

### Advanced Extraction

```bash
# Extract with custom patterns
claude skills use skill-extractor --source recent --patterns "debug,analyze,optimize"

# Extract specific types of skills
claude skills use skill-extractor --source recent --types "analysis,automation"

# Extract with quality filtering
claude skills use skill-extractor --source recent --min-quality 0.8
```

### Skill Management

```bash
# List extracted skills
claude skills use skill-extractor --action list

# Review and approve extracted skills
claude skills use skill-extractor --action review

# Export skills for sharing
claude skills use skill-extractor --action export --format json --output my-skills.json

# Import shared skills
claude skills use skill-extractor --action import --file team-skills.json
```

## 🎛️ Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| source | string | Conditional | Source type: recent, conversation, file, directory |
| source-conversation | string | Conditional | Specific conversation ID (required if source=conversation) |
| source-file | string | Conditional | File path (required if source=file) |
| source-dir | string | Conditional | Directory path (required if source=directory) |
| limit | int | No | Number of recent conversations to analyze (default: 100) |
| patterns | string | No | Comma-separated patterns to focus extraction |
| types | string | No | Skill types to extract: analysis, automation, debugging, etc. |
| min-quality | float | No | Minimum quality score (0.0-1.0, default: 0.7) |
| action | string | No | Management action: list, review, export, import |
| format | string | No | Export format: json, yaml, markdown (default: json) |
| output | string | No | Output file path (for export action) |
| file | string | Conditional | Import file path (required for import action) |

## 💡 Examples

### Extract from Recent Debugging Sessions

```bash
# Extract debugging skills from last 50 conversations
claude skills use skill-extractor --source recent --limit 50 --patterns "debug,error,fix"

# Review and refine extracted skills
claude skills use skill-extractor --action review

# Install promising skills
python install.py --skills extracted-debug-skill-1 extracted-debug-skill-2
```

### Build Personal Skill Library

```bash
# Extract from your complete history
claude skills use skill-extractor --source-dir ~/.claude/history/ --min-quality 0.8

# Organize by category
claude skills use skill-extractor --action organize --by-category

# Export your skill library
claude skills use skill-extractor --action export --format json --output my-skill-library.json
```

### Team Knowledge Sharing

```bash
# Extract from team conversations
claude skills use skill-extractor --source-dir /team/claude-logs/ --patterns "optimization,best-practices"

# Export for team sharing
claude skills use skill-extractor --action export --format yaml --output team-optimization-skills.yaml

# Team members import
claude skills use skill-extractor --action import --file team-optimization-skills.yaml
```

## 🎁 Output

### Extraction Results
```json
{
  "extraction_summary": {
    "conversations_analyzed": 50,
    "skills_extracted": 12,
    "high_quality_skills": 8,
    "categories": {
      "debugging": 4,
      "analysis": 3,
      "automation": 2,
      "optimization": 3
    }
  },
  "extracted_skills": [
    {
      "name": "api-debugger-enhanced",
      "category": "debugging",
      "quality_score": 0.89,
      "description": "Advanced API debugging with request/response analysis",
      "usage_pattern": "Used in 15 conversations, 89% success rate",
      "complexity": "medium",
      "dependencies": []
    },
    {
      "name": "performance-analyzer-pro",
      "category": "analysis", 
      "quality_score": 0.92,
      "description": "Comprehensive performance analysis with bottleneck identification",
      "usage_pattern": "Used in 8 conversations, 92% success rate",
      "complexity": "high",
      "dependencies": ["profiling-tools"]
    }
  ]
}
```

### Skill Review Interface
```json
{
  "review_queue": [
    {
      "skill": "api-debugger-enhanced",
      "recommendation": "High quality, frequently used pattern",
      "auto_approved": true,
      "reasoning": "Consistent usage across 15+ conversations with high success rate"
    },
    {
      "skill": "custom-deployment-script",
      "recommendation": "Review recommended",
      "auto_approved": false,
      "reasoning": "Project-specific implementation, consider generalization"
    }
  ]
}
```

## ⚠️ Important Notes

- **Privacy**: Extractor analyzes conversation content - review extracted skills before sharing
- **Quality Threshold**: Higher quality scores (0.8+) produce more reliable skills
- **Pattern Recognition**: Some complex patterns may require manual refinement
- **Context Dependency**: Skills tied to specific projects may need generalization
- **Version Compatibility**: Extracted skills work best with Claude Code v1.2+

## 🔄 Integration with Other Skills

### With session-snapshot
```bash
# Extract skills from saved sessions
claude skills use skill-extractor --source-session "debug-production-issue"

# Save extraction session for later review
claude skills use session-snapshot --action start --name "skill-extraction-review"
```

### With workflow-automator
```bash
# Create automated skill extraction workflow
claude skills use workflow-automator --name "weekly-skill-extraction" --steps "extract,review,organize"
```

### With productivity-tracker
```bash
# Track skill usage patterns for better extraction
claude skills use productivity-tracker --analyze-skills --export-for-extraction
```

## 🛠️ Advanced Configuration

### Custom Extraction Rules
```bash
# Define custom extraction patterns
export CLAUDE_SKILL_PATTERNS="debug,analyze,optimize,refactor"
export CLAUDE_SKILL_MIN_QUALITY="0.85"
export CLAUDE_SKILL_MAX_COMPLEXITY="high"
```

### Machine Learning Enhancement
```bash
# Enable ML-based pattern recognition
export CLAUDE_SKILL_ML_MODE="enhanced"
export CLAUDE_SKILL_TRAINING_DATA="~/.claude/skill-training/"
```

### Team Extraction Settings
```bash
# Configure team-wide extraction
export CLAUDE_TEAM_EXTRACTION="true"
export CLAUDE_TEAM_SKILLS_REPO="/team/shared-skills/"
export CLAUDE_TEAM_APPROVAL_REQUIRED="true"
```

## 🎯 Quality Scoring

skill-extractor uses multiple factors to calculate quality scores:

### Usage Patterns (40%)
- Frequency of similar commands
- Success rate in conversations
- Consistency across contexts

### Documentation Quality (30%)
- Clarity of descriptions
- Completeness of examples
- Parameter documentation

### Reusability (20%)
- General applicability
- Minimal dependencies
- Clear input/output specifications

### Complexity Appropriateness (10%)
- Balanced complexity
- Appropriate for skill format
- Maintainable implementation

## 📊 Analytics and Insights

skill-extractor provides detailed analytics:
- Extraction success rates
- Popular skill categories
- Quality improvement trends
- Team contribution patterns

Access analytics:
```bash
claude skills use skill-extractor --action analytics --period 30d
```

## 🚨 Troubleshooting

### Common Issues

**No skills extracted**: Increase limit, check quality threshold, broaden patterns
**Low quality scores**: Review conversation clarity, add more examples
**Duplicate skills**: Adjust similarity threshold, refine extraction patterns
**Import failures**: Check file format, verify skill compatibility

### Debug Mode
```bash
# Enable debug logging
export CLAUDE_SKILL_EXTRACTOR_DEBUG="true"
claude skills use skill-extractor --source recent --limit 10
```

## 💡 Best Practices

### For Skill Creators
1. **Document as you go** - Add clear descriptions to your conversations
2. **Use consistent patterns** - Develop reusable command structures
3. **Test thoroughly** - Verify solutions work in multiple contexts
4. **Share knowledge** - Contribute high-quality skills to the community

### For Skill Users
1. **Review before installing** - Check extracted skills for relevance and quality
2. **Customize as needed** - Adapt skills to your specific requirements
3. **Provide feedback** - Rate skills to improve extraction quality
4. **Contribute improvements** - Enhance existing skills with your experience

---

**💡 Pro Tip**: Combine skill-extractor with session-snapshot to build a comprehensive knowledge base from your most successful Claude Code sessions!