# Manifest Generator - Usage Guide

## Overview

The `manifest-generator` meta-skill automatically creates and maintains unified skill manifests for your Claude Code skills ecosystem. It scans skill directories, extracts metadata, generates comprehensive documentation, and keeps skill inventories up-to-date across your development environment.

**Purpose**: Skill inventory management, documentation automation, ecosystem organization, team standardization

## Quick Start

### Natural Language Invocation
```
"Generate a skill manifest for my skills"
"Create an inventory of all available skills"
"Update my skill documentation"
"Show me what skills I have installed"
"Generate a team skill catalog"
```

### Direct Skill Invocation
```
/manifest-generator
```

## When to Use

✅ **Skill Inventory Management**:
- Maintain overview of installed skills
- Track skill versions and updates
- Document skill capabilities
- Create skill catalogs for teams

✅ **Documentation Automation**:
- Generate comprehensive skill documentation
- Keep skill lists synchronized
- Create searchable skill inventories
- Automate documentation updates

✅ **Team Collaboration**:
- Share skill inventories with team members
- Standardize skill documentation format
- Create team skill knowledge bases
- Facilitate skill adoption across teams

✅ **Ecosystem Maintenance**:
- Identify missing or outdated skills
- Track skill dependencies
- Monitor skill usage patterns
- Plan skill ecosystem improvements

## Generation Process

### Step 1: Skill Discovery and Scanning
Automatically scan skill directories:

**Discovery Process**:
```python
# Scan for skill directories
skills_root = Path.home() / ".claude" / "skills"
categories = ["meta", "development", "git", "analysis"]

for category in categories:
    category_path = skills_root / category
    if category_path.exists():
        for skill_dir in category_path.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                discovered_skills.append({
                    "name": skill_dir.name,
                    "category": category,
                    "path": skill_dir,
                    "skill_file": skill_dir / "SKILL.md"
                })
```

**Metadata Extraction**:
```python
# Extract skill metadata from SKILL.md frontmatter
def extract_skill_metadata(skill_file):
    with open(skill_file, 'r') as f:
        content = f.read()
    
    # Parse YAML frontmatter
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = yaml.safe_load(frontmatter_match.group(1))
        return {
            "name": frontmatter.get("name"),
            "description": frontmatter.get("description"),
            "category": determine_category(skill_file),
            "priority": frontmatter.get("priority", "medium"),
            "dependencies": frontmatter.get("dependencies", [])
        }
    
    # Fallback to file parsing
    return extract_metadata_from_content(content)
```

### Step 2: Content Analysis and Enrichment
Analyze skill content for additional insights:

**Skill Content Analysis**:
```python
def analyze_skill_content(skill_file):
    with open(skill_file, 'r') as f:
        content = f.read()
    
    analysis = {
        "complexity": estimate_complexity(content),
        "use_cases": extract_use_cases(content),
        "examples": extract_examples(content),
        "token_efficiency": extract_token_info(content),
        "related_skills": find_related_skills(content),
        "last_updated": get_file_timestamp(skill_file)
    }
    
    return analysis
```

**Cross-Reference Analysis**:
```python
def cross_reference_skills(skills_data):
    # Build skill relationship graph
    skill_graph = build_skill_graph(skills_data)
    
    # Identify skill combinations
    skill_combinations = find_workflow_combinations(skill_graph)
    
    # Detect missing skills or gaps
    skill_gaps = identify_skill_gaps(skills_data)
    
    return {
        "relationships": skill_graph,
        "combinations": skill_combinations,
        "gaps": skill_gaps
    }
```

### Step 3: Manifest Generation
Create comprehensive documentation:

**Unified Skill Manifest Structure**:
```markdown
# Claude Code Skills - Unified Manifest

**Generated**: YYYY-MM-DD HH:MM:SS
**Total Skills**: 19
**Categories**: 4
**Coverage**: Comprehensive

## 📊 Executive Summary

- **Meta Skills**: 6 skills for workflow enhancement
- **Development Skills**: 3 skills for coding productivity  
- **Git Skills**: 3 skills for version control
- **Analysis Skills**: 8 skills for code quality
- **Token Savings**: Up to 90% reduction in manual effort
- **Time Savings**: Average 45 minutes per development session

## 🏆 Priority Skills (Start Here)

### 🔥 Essential Skills (Use Daily)
1. **session-snapshot** - Never lose work again
2. **lean-plan** - Token-efficient planning
3. **skill-recommendation-engine** - Discover relevant skills
4. **repo-briefing** - Understand codebases quickly

### ⚡ Productivity Boosters (Use Weekly)
5. **quick-test-runner** - Efficient testing workflows
6. **dependency-audit** - Security and maintenance
7. **dead-code-hunter** - Code cleanup
8. **skill-extractor** - Automate your workflows
```

## Configuration Examples

### Example 1: Personal Developer Manifest
**User Context**: Solo developer working on multiple projects

**Generated Configuration**:
```json
{
  "manifest_type": "personal",
  "user_profile": {
    "primary_languages": ["Python", "JavaScript", "TypeScript"],
    "development_focus": "full_stack_web",
    "experience_level": "intermediate",
    "team_size": 1
  },
  "skill_priorities": {
    "essential": ["session-snapshot", "lean-plan", "repo-briefing"],
    "productivity": ["quick-test-runner", "dependency-audit"],
    "quality": ["dead-code-hunter", "api-contract-sniffer"],
    "advanced": ["skill-extractor", "skill-recommendation-engine"]
  },
  "custom_sections": {
    "daily_workflow": "session-snapshot → lean-plan → development → quick-test-runner",
    "weekly_maintenance": "dependency-audit → dead-code-hunter",
    "project_onboarding": "repo-briefing → skill-recommendation-engine"
  }
}
```

### Example 2: Enterprise Team Manifest
**User Context**: Development team of 15 engineers in corporate environment

**Generated Configuration**:
```json
{
  "manifest_type": "enterprise_team",
  "team_profile": {
    "team_size": 15,
    "primary_stack": ["Java", "Spring", "React", "PostgreSQL"],
    "compliance_requirements": ["SOX", "GDPR"],
    "security_focus": true
  },
  "skill_standardization": {
    "mandatory": ["session-snapshot", "dependency-audit", "diff-summariser"],
    "recommended": ["lean-plan", "quick-test-runner", "repo-briefing"],
    "optional": ["skill-extractor", "anti-pattern-sniffer"]
  },
  "compliance_sections": {
    "audit_trail": "All skill usage logged with timestamps",
    "security_scanning": "dependency-audit runs on all projects",
    "code_review": "diff-summariser standard for PRs"
  }
}
```

### Example 3: Open Source Project Manifest
**User Context**: Open source project with multiple contributors

**Generated Configuration**:
```json
{
  "manifest_type": "open_source",
  "project_profile": {
    "contributor_count": 25,
    "languages": ["Python", "C++", "JavaScript"],
    "license": "MIT",
    "governance": "maintainer_led"
  },
  "contribution_friendly": {
    "beginner_skills": ["repo-briefing", "skill-recommendation-engine"],
    "review_skills": ["diff-summariser", "dependency-audit"],
    "quality_skills": ["dead-code-hunter", "api-contract-sniffer"]
  },
  "community_sections": {
    "getting_started": "New contributor skill onboarding guide",
    "contribution_guides": "Skill-enhanced contribution workflows",
    "maintainer_tools": "Advanced skills for project maintainers"
  }
}
```

## Real-World Usage Scenarios

### Scenario 1: New Team Member Onboarding
**Challenge**: Help new developer understand available tools

**Solution Process**:
```bash
# Step 1: Generate personalized manifest
/manifest-generator
# Creates: PERSONAL_SKILL_MANIFEST.md

# Step 2: Review recommendations
# Focus on: Essential → Productivity → Quality

# Step 3: Interactive exploration
# Use: startup-skill-showcase for hands-on learning

# Step 4: Gradual adoption
# Week 1: Essential skills
# Week 2: Productivity skills  
# Week 3: Quality skills
```

**Expected Outcome**: New team member productive with skills in 1 week vs 1 month

### Scenario 2: Team Skill Audit
**Challenge**: Understand team's skill usage and identify gaps

**Audit Process**:
```bash
# Step 1: Generate team manifest
/manifest-generator --team --output TEAM_MANIFEST.md

# Step 2: Analyze usage patterns
# Review: Most used, least used, never used skills

# Step 3: Identify gaps
# Compare: Current usage vs recommended skills

# Step 4: Create improvement plan
# Target: Skills that would boost productivity

# Step 5: Training implementation
# Use: startup-skill-showcase for team training
```

**Audit Results Example**:
```markdown
## Team Skill Audit Results

**Team Size**: 8 developers
**Skills Available**: 19
**Skills Used**: 12 (63%)
**Skills Never Used**: 7 (37%)

**Most Used**:
1. session-snapshot (100% of team)
2. lean-plan (88% of team)
3. dependency-audit (75% of team)

**Never Used** (Training Opportunities):
1. skill-extractor (0% adoption)
2. anti-pattern-sniffer (0% adoption)
3. lemma-dependency-graph (0% adoption)

**Recommended Focus**: anti-pattern-sniffer training for code quality improvement
```

### Scenario 3: Project-Specific Skill Configuration
**Challenge**: Set up optimal skills for specific project type

**Configuration Process**:
```bash
# Step 1: Project analysis
# Identify: Technology stack, team size, project phase

# Step 2: Generate project-specific manifest
/manifest-generator --project-type web_api
# Creates: WEB_API_SKILL_MANIFEST.md

# Step 3: Customize for project needs
# Add: Project-specific skill combinations
# Remove: Irrelevant skills
# Modify: Priority rankings

# Step 4: Team distribution
# Share: Project manifest with team
# Train: Project-specific skill workflows
```

## Advanced Features

### Automated Manifest Updates
Set up continuous manifest maintenance:

```python
# Auto-update configuration
{
  "auto_update": {
    "enabled": true,
    "schedule": "weekly",
    "triggers": [
      "new_skill_installed",
      "skill_updated", 
      "manual_request"
    ],
    "notifications": {
      "email": true,
      "slack": true,
      "summary_report": true
    }
  }
}
```

### Integration with Development Workflow
Embed manifest generation in CI/CD:

```yaml
# GitHub Actions integration
name: Update Skill Manifest
on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday 9 AM
  workflow_dispatch:

jobs:
  update-manifest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Generate Skill Manifest
        run: |
          python /manifest-generator --ci-mode
          git add UNIFIED_SKILL_MANIFEST.md
          git commit -m "Update skill manifest - $(date)"
          git push
```

### Skill Analytics and Insights
Generate usage analytics:

```python
# Analytics generation
{
  "analytics": {
    "usage_patterns": {
      "frequency_analysis": true,
      "skill_combinations": true,
      "productivity_metrics": true
    },
    "trend_analysis": {
      "adoption_rates": true,
      "skill_lifecycle": true,
      "effectiveness_metrics": true
    },
    "recommendations": {
      "skill_gaps": true,
      "training_needs": true,
      "optimization_opportunities": true
    }
  }
}
```

## Troubleshooting

### Common Issues

**Issue 1: Skills Not Detected**
```bash
# Symptoms: Missing skills in manifest
# Diagnosis: Check skill file structure
# Solution:
- Verify SKILL.md files exist
- Check YAML frontmatter format
- Ensure proper directory structure
- Validate skill file permissions
```

**Issue 2: Manifest Generation Failures**
```bash
# Symptoms: Generation process crashes
# Diagnosis: Check for parsing errors
# Solution:
- Validate YAML syntax in skill files
- Check for special characters
- Verify file encoding (UTF-8)
- Review error logs for specifics
```

**Issue 3: Outdated Manifest Information**
```bash
# Symptoms: Stale or incorrect skill data
# Diagnosis: Check update mechanisms
# Solution:
- Enable auto-update features
- Set up regular regeneration schedule
- Implement change detection
- Configure notification systems
```

### Performance Optimization

**Large Skill Ecosystems**:
```python
# Optimization for 50+ skills
{
  "performance": {
    "incremental_updates": true,
    "parallel_processing": true,
    "caching": {
      "skill_metadata": 3600,  # 1 hour
      "file_hashes": 1800,     # 30 minutes
      "parsed_content": 900    # 15 minutes
    },
    "batch_processing": {
      "chunk_size": 10,
      "timeout": 30
    }
  }
}
```

## Token Efficiency

- **Skill Discovery**: ~200-300 tokens
- **Metadata Extraction**: ~150-250 tokens per skill
- **Content Analysis**: ~100-200 tokens per skill
- **Manifest Generation**: ~300-500 tokens
- **Total for 19 skills**: ~1200-1900 tokens
- **Value**: Saves 500+ tokens per skill discovery session vs manual search

## Integration with Other Skills

### With skill-recommendation-engine
```
/manifest-generator
# Generate comprehensive skill inventory
/skill-recommendation-engine
# Get personalized skill suggestions based on manifest
```

### With session-snapshot
```
/manifest-generator
# Create team skill catalog
/session-snapshot
# Save manifest state for team reference
```

### With startup-skill-showcase
```
/manifest-generator
# Generate skill inventory
/startup-skill-showcase
# Use manifest to create guided tours
```

## Best Practices

### Manifest Maintenance
```bash
# Regular maintenance schedule
- Daily: Check for new skills
- Weekly: Update usage statistics
- Monthly: Review and optimize categories
- Quarterly: Analyze skill ecosystem health
- Annually: Major restructuring if needed
```

### Team Collaboration
```bash
# Team manifest management
- Use version control for manifests
- Document skill adoption decisions
- Share manifest updates with team
- Collect feedback on skill usefulness
- Iterate based on team needs
```

---

**💡 Pro Tip**: Run this skill weekly to keep your skill documentation current. A well-maintained manifest becomes invaluable for team collaboration and onboarding!