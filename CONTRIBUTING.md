# Contributing to Claude Code Skills 🤝

Thank you for your interest in contributing to the Claude Code Skills ecosystem! This guide will help you get started with creating, testing, and submitting your skills.

## 🌟 Why Contribute?

- **Impact**: Help thousands of Claude Code users work more efficiently
- **Recognition**: Get credited for your contributions in our community
- **Learning**: Deepen your understanding of Claude Code and AI-assisted development
- **Network**: Connect with other skilled developers in the ecosystem

## 🚀 Quick Start

### 1. Fork & Clone
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/claude-code-skills.git
cd claude-code-skills
```

### 2. Create Your Skill
```bash
# Use our templates for consistency
cp templates/skill-template.md skills/YOUR_CATEGORY/your-skill-name.md
```

### 3. Test Your Skill
```bash
# Install your skill locally
python install.py --skills your-skill-name

# Test it with Claude Code
claude skills use your-skill-name
```

### 4. Submit Your Contribution
```bash
git add .
git commit -m "Add your-skill-name: Brief description"
git push origin main
# Create a Pull Request on GitHub
```

## 📋 Skill Categories

Choose the most appropriate category for your skill:

### 🎯 Meta Skills
Workflow management, session handling, skill discovery tools
- **Examples**: session-snapshot, skill-extractor, workflow-automator

### 💻 Development Skills
Code generation, debugging, refactoring, development utilities
- **Examples**: code-generator, debug-assistant, refactor-pro

### 🔀 Git & Version Control
Repository analysis, commit optimization, branch management
- **Examples**: repo-analyzer, commit-optimizer, branch-manager

### 🔍 Analysis & Debugging
Performance profiling, security scanning, quality assessment
- **Examples**: performance-profiler, security-scanner, dependency-analyzer

## 🛠️ Skill Development Guidelines

### Skill Structure
Your skill should follow this structure:

```markdown
# Skill Name

Brief, compelling description of what this skill does.

## 🎯 Purpose

Clear explanation of the problem this skill solves.

## 🚀 Usage

### Basic Usage
```bash
claude skills use skill-name --param value
```

### Advanced Options
```bash
claude skills use skill-name --advanced --option value
```

## 📋 Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1 | string | Yes | Description of parameter |
| param2 | int | No | Optional parameter description |

## 💡 Examples

### Example 1: Basic Usage
```bash
# Show what this example does
claude skills use skill-name --input file.txt
```

### Example 2: Advanced Usage
```bash
# Show advanced features
claude skills use skill-name --advanced --filter pattern
```

## 🎁 Output

Describe what output the user can expect.

## ⚠️ Notes

- Important considerations
- Known limitations
- Best practices
```

### Writing Effective Skills

#### 1. Clear Purpose Statement
- What specific problem does this solve?
- Who is the target user?
- When should someone use this skill?

#### 2. Comprehensive Examples
- Include basic and advanced usage
- Show real-world scenarios
- Provide before/after comparisons

#### 3. Parameter Documentation
- Clearly explain each parameter
- Include valid value ranges
- Mark required vs optional parameters

#### 4. Error Handling
- Anticipate common mistakes
- Provide helpful error messages
- Suggest solutions to problems

## 🧪 Testing Your Skill

### Pre-Submission Checklist

- [ ] Skill follows the template structure
- [ ] All examples work as described
- [ ] Parameters are properly documented
- [ ] Error cases are handled gracefully
- [ ] Skill installs without errors
- [ ] No conflicts with existing skills

### Testing Process

1. **Install Your Skill**
   ```bash
   python install.py --skills your-skill-name --dry-run
   python install.py --skills your-skill-name
   ```

2. **Test Basic Functionality**
   ```bash
   claude skills use your-skill-name --help
   claude skills use your-skill-name --test
   ```

3. **Test All Examples**
   - Copy each example from your documentation
   - Verify it produces expected output
   - Test edge cases and error conditions

4. **Cross-Platform Testing**
   - Test on Windows, macOS, and Linux if possible
   - Ensure file paths work correctly
   - Verify no OS-specific dependencies

### Validation Tools

#### Automated Validation (GitHub Actions)
Your pull request will be automatically validated by our GitHub Actions workflow:
- ✅ **Skill Structure**: Validates SKILL.md format and required sections
- ✅ **Documentation**: Checks for proper Purpose, Usage, and Examples sections
- ✅ **Token Efficiency**: Ensures skills mention token optimization
- ✅ **YAML Frontmatter**: Validates metadata structure when present
- ✅ **Skill Invocation**: Verifies proper skill name references

The validation runs automatically when you create a pull request and will comment with detailed results.

#### Manual Validation
```bash
# Run skill validation locally
python tests/validate_skills.py --skill your-skill-name

# Test for common issues
python tests/test_skills.py --skill your-skill-name

# Check documentation quality
python tests/check_documentation.py --skill your-skill-name
```

## 📊 Quality Standards

### Must Have
- [ ] Clear, descriptive name
- [ ] Comprehensive documentation
- [ ] Working examples
- [ ] Proper error handling
- [ ] No security vulnerabilities

### Should Have
- [ ] Performance optimizations
- [ ] Edge case handling
- [ ] Cross-platform compatibility
- [ ] Integration with other skills
- [ ] Usage analytics (if applicable)

### Nice to Have
- [ ] Advanced configuration options
- [ ] Multiple output formats
- [ ] Plugin architecture
- [ ] Custom themes/styling
- [ ] Community contributions

## 🏷️ Skill Naming Conventions

### Good Names
- `session-snapshot` - Clear, descriptive, hyphenated
- `repo-analyzer` - Action-oriented, specific
- `performance-profiler` - Professional, comprehensive

### Avoid
- `my_skill` - Personal, not descriptive
- `tool` - Too generic
- `session_snapshot` - Underscores (use hyphens)

## 🔄 Submission Process

### 1. Prepare Your Submission
```bash
# Create a descriptive branch
git checkout -b add-skill-name

# Stage your changes
git add skills/category/skill-name.md
git add tests/test-skill-name.py  # if applicable

# Commit with clear message
git commit -m "Add skill-name: Brief description of what it does"
```

### 2. Pull Request Template

Use this template for your PR description:

```markdown
## 🎯 Skill Addition: Skill Name

### Description
Brief description of what this skill does and why it's useful.

### Category
- [ ] Meta Skills
- [ ] Development Skills  
- [ ] Git & Version Control
- [ ] Analysis & Debugging

### Features
- ✅ Feature 1
- ✅ Feature 2
- ✅ Feature 3

### Testing
- [ ] Installs successfully
- [ ] All examples work
- [ ] Cross-platform compatible
- [ ] No conflicts with existing skills

### Usage Example
```bash
claude skills use skill-name --example param
```

### Additional Notes
Any special considerations or notes for reviewers.
```

### 3. Review Process

1. **Automated Checks** - Our CI will validate:
   - Skill structure and syntax
   - Documentation completeness
   - Installation process
   - Basic functionality

2. **Community Review** - Other contributors will review:
   - Usefulness and relevance
   - Code quality and best practices
   - Documentation clarity
   - Integration potential

3. **Maintainer Review** - Core team will check:
   - Alignment with project goals
   - Long-term maintainability
   - Security considerations
   - Community impact

## 🐛 Reporting Issues

### Bug Reports
Include:
- Skill name and version
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Claude Code version)

### Feature Requests
Include:
- Use case description
- Proposed solution
- Alternative approaches
- Implementation considerations

### Security Issues
**DO NOT** create public issues for security vulnerabilities.
Email security concerns to: security@claude-code-skills.org

## 💡 Skill Ideas

Looking for inspiration? Here are some skill ideas we'd love to see:

### High Priority
- **api-tester** - Automated API testing and documentation
- **database-analyzer** - Database schema analysis and optimization
- **log-analyzer** - Log file analysis and pattern detection
- **config-validator** - Configuration file validation and suggestions

### Medium Priority
- **dependency-updater** - Safe dependency updating with testing
- **performance-monitor** - Real-time performance monitoring
- **code-formatter** - Intelligent code formatting with style guides
- **test-generator** - Automated test case generation

### Nice to Have
- **documentation-linter** - Documentation quality checking
- **commit-analyzer** - Commit message and code change analysis
- **release-manager** - Release automation and changelog generation
- **team-analyzer** - Team productivity and collaboration insights

## 🌟 Recognition

Contributors are recognized in:
- **README.md** - Main contributors section
- **CHANGELOG.md** - Feature additions and improvements
- **GitHub Contributors** - Automatic GitHub recognition
- **Community Spotlight** - Monthly featured contributors

## 📞 Getting Help

### Community Support
- **[GitHub Discussions](https://github.com/chokmah-me/claude-code-skills/discussions)** - General questions and discussions
- **[Discord Server](https://discord.gg/claude-code-skills)** - Real-time chat with contributors
- **[Stack Overflow](https://stackoverflow.com/questions/tagged/claude-code-skills)** - Technical questions

### Maintainer Contact
- **General Questions**: @maintainer-name
- **Technical Issues**: @tech-maintainer
- **Community Matters**: @community-manager

---

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.

## 🙏 Thank You!

Your contributions make the Claude Code ecosystem better for everyone. We appreciate your time, effort, and expertise!

---

**[⬆ Back to Top](#contributing-to-claude-code-skills-)**