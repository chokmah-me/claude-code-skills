# 🚀 GitHub Actions Setup Guide

This repository now includes **5 automated GitHub Actions** for maintenance and quality assurance. Follow this guide to set up and use them effectively.

## 📋 Quick Setup

### 1. **Repository Configuration**
If you haven't already, push this repository to GitHub:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git

# Push to GitHub
git push -u origin master
```

### 2. **Enable GitHub Actions**
1. Go to your repository on GitHub
2. Click on **Settings** → **Actions** → **General**
3. Ensure **Actions permissions** are enabled
4. Set **Workflow permissions** to allow read/write if needed

### 3. **Add Skills Inventory Markers**
The README Auto-Updater workflow looks for these markers in your `README.md`:

```markdown
<!-- SKILLS_INVENTORY_START -->
<!-- SKILLS_INVENTORY_END -->
```

These markers should already be present in your README from the initial setup.

## 🎯 Available Workflows

### **Skill Template Validator** 
- **Trigger**: Pull requests that modify skills
- **Purpose**: Ensures skills follow template structure
- **Checks**: SKILL.md structure, required sections, token efficiency mentions

### **README Auto-Updater**
- **Trigger**: Push to main branch, weekly schedule
- **Purpose**: Updates skills inventory in README
- **Features**: Automatic categorization, skill counts, last updated timestamp

### **Changelog Automation**
- **Trigger**: Push to main, PR merges, manual dispatch
- **Purpose**: Maintains changelog from commits
- **Features**: Conventional commit parsing, automatic categorization, release creation

### **Skill Consistency Checker**
- **Trigger**: Weekly schedule, pull requests, manual dispatch
- **Purpose**: Validates consistency across skills
- **Checks**: Naming conventions, file structures, quality scoring, dependencies

### **Documentation Link Validator**
- **Trigger**: Weekly schedule, documentation changes, manual dispatch
- **Purpose**: Checks for broken links
- **Validates**: Internal links, external URLs, special links (mailto, tel)

## 🚀 Manual Usage

Run any workflow manually using GitHub CLI:

```bash
# List available workflows
gh workflow list

# Run a specific workflow
gh workflow run skill-template-validator.yml
gh workflow run readme-auto-update.yml
gh workflow run changelog-automation.yml
gh workflow run skill-consistency-checker.yml
gh workflow run documentation-link-validator.yml

# Run with parameters (for changelog)
gh workflow run changelog-automation.yml -f version="3.1.0" -f release_type="minor"
```

## 📊 Monitoring

### **Workflow Status**
- Check the **Actions** tab in your GitHub repository
- View workflow runs, logs, and artifacts
- Monitor success/failure rates

### **PR Integration**
- Workflows automatically comment on pull requests with results
- Failed checks provide detailed feedback
- Success confirmations with summary statistics

### **Artifacts**
Each workflow generates artifacts you can download:
- Validation reports (JSON format)
- Detailed analysis results
- Summary documents

## 🔧 Customization

### **Environment Variables**
Edit the workflows to customize behavior:

```yaml
env:
  PYTHON_VERSION: '3.11'        # Python version to use
  TEST_TIMEOUT: '300'           # Timeout in seconds
  MAX_RETRIES: '3'              # Retry attempts for external links
```

### **Schedule Frequency**
Modify cron expressions in workflow files:

```yaml
schedule:
  - cron: '0 12 * * 1'  # Weekly on Monday at 12:00 UTC
  - cron: '0 6 * * *'   # Daily at 6:00 UTC
```

### **Trigger Conditions**
Adjust when workflows run by modifying the `on:` section:

```yaml
on:
  pull_request:
    paths:
      - 'skills/**'
      - '.claude/skills/**'
  push:
    branches: [ main, develop ]
  workflow_dispatch:
```

## 🛠️ Troubleshooting

### **Workflow Failures**
1. Check the **Actions** tab for detailed logs
2. Look for error messages in the workflow output
3. Verify file paths and repository structure
4. Ensure proper permissions are set

### **Common Issues**

**"No changes detected"**
- This is normal if no actual changes are needed
- Check the workflow logs for analysis results

**Link validation finds broken links**
- Some external sites may block automated requests
- Manually verify suspicious links in browser
- Consider if links are false positives

**Skill template validation fails**
- Ensure skills follow the template structure
- Check for required sections: Purpose, Usage, Examples
- Add token efficiency mentions for Claude skills

### **Debug Mode**
Enable debug logging by adding repository secrets:
- `ACTIONS_STEP_DEBUG: true`
- `ACTIONS_RUNNER_DEBUG: true`

## 📈 Benefits You'll See

### **Immediate Benefits**
- ✅ Consistent skill documentation
- ✅ Automated README updates
- ✅ Early issue detection in PRs
- ✅ Working documentation links

### **Long-term Benefits**
- 🤖 Reduced manual maintenance
- 📊 Quality metrics and trends
- 🔄 Automated repository upkeep
- 🎯 Standardized skill structure

### **Developer Experience**
- 📝 Clear validation feedback
- 🚀 Streamlined contribution process
- 📋 Automated quality checks
- 🔄 Continuous maintenance

## 🆘 Getting Help

### **GitHub Actions Documentation**
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Python setup action](https://github.com/actions/setup-python)
- [GitHub CLI workflows](https://cli.github.com/manual/gh_workflow)

### **Repository Issues**
- Check workflow logs in the Actions tab
- Review generated artifacts for detailed reports
- Verify repository structure matches expected format
- Ensure GitHub Actions are enabled in repository settings

---

## 🎉 Success Indicators

You'll know the setup is working when you see:

1. **Green checkmarks** on workflow runs in the Actions tab
2. **Automatic PR comments** with validation results
3. **Updated README** with current skills inventory
4. **Maintained changelog** with recent changes
5. **Clean link validation** reports

---

**Need help?** Check the workflow logs first - they contain detailed information about what each action is doing and any issues encountered.

**Ready to go?** Your repository now has enterprise-grade automation for maintaining skill quality and consistency! 🚀