# Installation Guide

Comprehensive installation guide for the Claude Code Skills ecosystem.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Installation](#quick-installation)
- [Detailed Installation](#detailed-installation)
- [Category-Based Installation](#category-based-installation)
- [Advanced Installation](#advanced-installation)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space for skills and dependencies

### Claude Code Requirements

- **Claude Code**: Version 1.0 or higher
- **Active Account**: Valid Claude Code subscription
- **Skills Directory**: Configured skills directory

### Optional Dependencies

- **Git**: For version control integration
- **GitHub CLI**: For advanced GitHub features
- **Docker**: For containerized skill execution

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/chokmah-me/claude-code-skills.git
cd claude-code-skills
```

### 2. Install All Skills

```bash
# Install all available skills
python install.py --all

# Verify installation
python install.py --verify
```

### 3. Test Installation

```bash
# Test flagship meta-skills
claude skills use session-snapshot --help
claude skills use skill-extractor --help
```

## Detailed Installation

### Step 1: Environment Setup

#### Check Python Version
```bash
python --version
# Should show Python 3.8+
```

#### Verify Claude Code Installation
```bash
claude --version
# Should show Claude Code version
```

#### Configure Skills Directory
```bash
# Check current skills directory
claude config get skills.directory

# Set custom skills directory (optional)
claude config set skills.directory ~/my-claude-skills
```

### Step 2: Repository Setup

#### Clone Repository
```bash
git clone https://github.com/chokmah-me/claude-code-skills.git
cd claude-code-skills
```

#### Explore Available Skills
```bash
# List all available skills
python install.py --list

# Get detailed information
python install.py --list --verbose
```

### Step 3: Installation Options

#### Install All Skills
```bash
# Full installation
python install.py --all

# Dry run first (recommended)
python install.py --all --dry-run
```

#### Install by Category
```bash
# Install meta skills only
python install.py --category meta

# Install development skills
python install.py --category development

# Install analysis skills
python install.py --category analysis
```

#### Install Specific Skills
```bash
# Install specific skills
python install.py --skills session-snapshot skill-extractor

# Install with custom target directory
python install.py --skills session-snapshot --target-dir ~/custom-skills/
```

## Category-Based Installation

### 🎯 Meta Skills (Recommended First)

Meta skills provide foundational capabilities for other skills.

```bash
# Install all meta skills
python install.py --category meta

# Individual meta skills
python install.py --skills session-snapshot skill-extractor workflow-automator
```

**Included Skills:**
- session-snapshot - Session management
- skill-extractor - Skill discovery
- workflow-automator - Process automation
- context-manager - Context switching
- productivity-tracker - Efficiency monitoring

### 💻 Development Skills

Development-focused skills for coding and debugging.

```bash
# Install all development skills
python install.py --category development
```

**Included Skills:**
- code-generator - Intelligent code generation
- debug-assistant - Advanced debugging
- refactor-pro - Safe code refactoring

### 🔀 Git & Version Control Skills

Skills for repository management and version control.

```bash
# Install all Git skills
python install.py --category git
```

**Included Skills:**
- repo-analyzer - Repository analysis
- commit-optimizer - Commit optimization
- branch-manager - Branch management

### 🔍 Analysis & Debugging Skills

Comprehensive analysis and debugging capabilities.

```bash
# Install all analysis skills
python install.py --category analysis
```

**Included Skills:**
- performance-profiler - Performance optimization
- dependency-analyzer - Dependency analysis
- security-scanner - Security scanning
- code-quality-checker - Quality assessment
- architecture-visualizer - Architecture mapping
- test-coverage-analyzer - Test coverage
- complexity-analyzer - Complexity measurement
- documentation-generator - Documentation creation

## Advanced Installation

### Custom Installation Paths

```bash
# Install to custom directory
python install.py --all --target-dir /opt/claude-skills/

# Install to user directory
python install.py --all --target-dir ~/.local/share/claude-skills/
```

### Selective Installation

```bash
# Install high-priority skills only
python install.py --skills session-snapshot skill-extractor debug-assistant

# Install by complexity
python install.py --category meta --min-quality 0.8
```

### Batch Installation

```bash
# Install from skill list file
echo "session-snapshot\nskill-extractor\ndebug-assistant" > my-skills.txt
python install.py --from-file my-skills.txt

# Install multiple categories
python install.py --category meta --category development
```

## Verification

### Basic Verification

```bash
# Check installation status
python install.py --verify

# List installed skills
python install.py --installed
```

### Functional Verification

```bash
# Test meta skills
claude skills use session-snapshot --help
claude skills use skill-extractor --help

# Test development skills
claude skills use debug-assistant --help
claude skills use code-generator --help

# Test analysis skills
claude skills use performance-profiler --help
claude skills use repo-analyzer --help
```

### Advanced Verification

```bash
# Run comprehensive tests
python tests/validate_skills.py --verbose

# Test specific skills
python tests/test_skills.py --skill session-snapshot

# Performance testing
python tests/performance_tests.py
```

## Platform-Specific Instructions

### Windows Installation

```powershell
# Using PowerShell
python install.py --all

# Verify installation
python install.py --verify

# Test skills
claude skills use session-snapshot --help
```

**Windows-Specific Notes:**
- Use PowerShell or Command Prompt
- Ensure Python is in PATH
- Consider using Windows Terminal for better experience

### macOS Installation

```bash
# Using Homebrew Python
python3 install.py --all

# Verify installation
python3 install.py --verify

# Test skills
claude skills use session-snapshot --help
```

**macOS-Specific Notes:**
- Use python3 instead of python
- Consider using pyenv for Python version management
- Terminal.app or iTerm2 recommended

### Linux Installation

```bash
# Most distributions
python3 install.py --all

# Verify installation
python3 install.py --verify

# Test skills
claude skills use session-snapshot --help
```

**Linux-Specific Notes:**
- Use package manager Python or pyenv
- Ensure pip is available
- Consider virtual environments

## Docker Installation

### Using Pre-built Image

```bash
# Pull the official image
docker pull chokmah/claude-code-skills:latest

# Run installation
docker run -v ~/.claude/skills:/skills chokmah/claude-code-skills:latest install --all
```

### Building Custom Image

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN python install.py --all

CMD ["python", "install.py", "--verify"]
```

## Troubleshooting

### Common Issues

#### "Permission Denied" Errors
```bash
# Fix permissions
chmod +x install.py
sudo chown -R $USER:$USER ~/.claude/
```

#### "Python Not Found" Errors
```bash
# Check Python installation
which python3
python3 --version

# Install Python if missing
# (Use your system's package manager)
```

#### "Claude Code Not Found" Errors
```bash
# Verify Claude Code installation
claude --version

# Reinstall Claude Code if needed
# (Follow official Claude Code installation guide)
```

#### Skills Not Loading
```bash
# Verify skills directory
claude config get skills.directory
ls -la ~/.claude/skills/

# Check skill file permissions
chmod 644 ~/.claude/skills/*.md
```

### Advanced Troubleshooting

#### Enable Debug Mode
```bash
export CLAUDE_DEBUG=true
python install.py --all --verbose
```

#### Check Dependencies
```bash
# Verify all dependencies
python -c "import sys; print(sys.version)"
claude --version
```

#### Validate Installation
```bash
# Run validation tests
python tests/validate_skills.py --verbose
python tests/test_skills.py --verbose
```

### Getting Help

#### Community Support
- **[GitHub Discussions](https://github.com/chokmah-me/claude-code-skills/discussions)**
- **[Discord Server](https://discord.gg/claude-code-skills)**
- **[Stack Overflow](https://stackoverflow.com/questions/tagged/claude-code-skills)**

#### Professional Support
- **Email**: support@claude-code-skills.org
- **Documentation**: [Full Documentation](https://docs.claude-code-skills.org)
- **Video Tutorials**: [YouTube Channel](https://youtube.com/claude-code-skills)

---

**💡 Pro Tip**: Start with meta skills (session-snapshot, skill-extractor) as they provide the foundation for all other skills and enhance your overall Claude Code experience!