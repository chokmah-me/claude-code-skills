# GitHub Actions Workflows

This document describes all automated workflows in the Claude Code skills repository.

## Workflow Status Overview

| Workflow | Status | Runs On | Purpose |
|----------|--------|---------|---------|
| Documentation Validation | ✅ Active | Push/PR | Validate skill documentation |
| Consistency Check | ✅ Active | Push/PR | Check naming & structure |
| Skill Testing | ✅ Active | Push/PR/Nightly | Test all skills |
| Manifest Builder | ✅ Active | main/Release | Generate manifest files |
| Dependency Analysis | ✅ Active | main/Weekly | Analyze skill dependencies |
| Simple Test | ✅ Active | Push/PR | Basic test suite |
| README Auto-Update | ✅ Active | main | Update README stats |
| Snapshot State Manager | ✅ Active | Push/PR | Manage session snapshots |

---

## Active Workflows

### 1. Documentation Validation
**File**: `.github/workflows/documentation-validation.yml`

**Purpose**: Validate that all skill documentation meets required standards

**Triggers**:
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**What it does**:
1. Checks out code
2. Sets up Python 3.10
3. Runs `validate_docs.py`
4. Uploads validation report

**Artifacts**:
- `validation-report.json` - Detailed validation results

**Required sections checked**:
- `# ` (Main heading)
- `## Description`
- `## Triggers`
- `## Usage`
- `## Parameters`
- `## Output`

**Failure conditions**:
- Missing required sections
- Empty file
- Invalid markdown

**Expected runtime**: ~30 seconds

---

### 2. Consistency Check
**File**: `.github/workflows/consistency-check.yml`

**Purpose**: Enforce consistent directory structure and naming conventions

**Triggers**:
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**What it does**:
1. Checks out code
2. Sets up Python 3.10
3. Runs `check_consistency.py`
4. Uploads consistency report

**Artifacts**:
- `consistency-report.txt` - Issues and warnings

**Checks performed**:
- Skill directories use kebab-case naming
- SKILL.md files have correct capitalization
- Skills are under valid categories
- All skills present in manifest

**Failure conditions**:
- Improperly named directories
- Manifest misalignment
- Invalid category placement

**Expected runtime**: ~20 seconds

---

### 3. Skill Testing
**File**: `.github/workflows/skill-testing.yml`

**Purpose**: Run comprehensive tests on all skill documentation

**Triggers**:
- Push to `main` or `develop`
- Pull requests to `main` or `develop`
- Nightly schedule (2 AM UTC)

**What it does**:
1. Checks out code
2. Sets up Python 3.10
3. Runs `test_skills.py`
4. Uploads test results

**Artifacts**:
- `test-results.json` - Detailed test results

**Tests performed**:
- Required sections present
- Code examples/blocks exist
- Triggers are defined
- Document structure valid

**Failure conditions**:
- Missing required sections
- No code examples
- Missing triggers
- Invalid markdown

**Expected runtime**: ~45 seconds

---

### 4. Manifest Builder
**File**: `.github/workflows/manifest-builder.yml`

**Purpose**: Generate and maintain unified manifest files

**Triggers**:
- Push to `main` branch
- Release published
- Manual trigger (`workflow_dispatch`)

**What it does**:
1. Checks out code with token
2. Sets up Python 3.10
3. Runs `build_manifest.py`
4. Commits changes if manifest changed
5. Uploads manifest artifacts

**Artifacts**:
- `SKILL_MANIFEST.json` - Machine-readable manifest
- `UNIFIED_SKILL_MANIFEST.md` - Human-readable manifest

**Generates**:
- Complete skill listing
- Skills grouped by category
- Metadata for each skill
- Trigger phrases

**Auto-commits**:
- Only if manifest files changed
- Commit message: "chore: update skill manifest"

**Expected runtime**: ~1 minute

---

### 5. Dependency Analysis
**File**: `.github/workflows/dependency-analysis.yml`

**Purpose**: Analyze skill dependencies and detect circular references

**Triggers**:
- Push to `main` branch
- Weekly schedule (3 AM UTC, Sundays)
- Manual trigger (`workflow_dispatch`)

**What it does**:
1. Checks out code
2. Sets up Python 3.10
3. Runs `analyze_dependencies.py`
4. Uploads dependency graph

**Artifacts**:
- `dependency-graph.json` - Dependency graph with analysis

**Analyzes**:
- References between skills
- Circular dependencies
- Suggested skill bundles
- Dependency chains

**Uses**:
- Skill cross-references in documentation
- Link analysis
- Graph traversal algorithms

**Expected runtime**: ~2 minutes

---

## Existing Passing Workflows

### Simple Test Workflow
**File**: `.github/workflows/simple-test.yml`

Status: ✅ Passing
Purpose: Basic test suite
Runs on: Push/PR

---

### README Auto-Update
**File**: `.github/workflows/readme-auto-update.yml`

Status: ✅ Passing
Purpose: Automatically update README with latest skill count
Runs on: Push to main

---

### Snapshot State Manager
**File**: `.github/workflows/snapshot-state-manager.yml`

Status: ✅ Passing
Purpose: Manage session snapshots for state recovery
Runs on: Push/PR

---

## Intentionally Disabled Workflows

### ASCII Sanitizer
**File**: `.github/workflows/ascii-sanitizer.yml`

Status: ⚠️ Disabled
Reason: Repository intentionally uses emojis in documentation and output
Purpose: Can be used as template for other repos requiring ASCII-only content

---

## Workflow Triggers Explained

### On Push
```yaml
on:
  push:
    branches: [main, develop]
```
Runs when code is pushed to these branches.

### On Pull Request
```yaml
on:
  pull_request:
    branches: [main, develop]
```
Runs when PR is opened/updated targeting these branches.

### On Schedule
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Every day at 2 AM UTC
```
Runs automatically on the specified schedule.

### Manual Trigger
```yaml
on:
  workflow_dispatch:
```
Can be manually triggered from GitHub Actions tab.

---

## Exit Codes

All scripts use consistent exit codes:

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Workflow passes ✅ |
| 1 | Failure | Workflow fails ❌ |
| 2 | Warning | Workflow passes with warnings ⚠️ |

---

## Viewing Workflow Results

### GitHub Actions Tab
1. Go to repository → Actions tab
2. Select workflow run
3. Click job to view logs
4. Download artifacts

### Artifacts
Each workflow uploads artifacts containing:
- JSON reports (machine-readable)
- Text reports (human-readable)
- Graph data

Artifacts are retained for:
- Regular reports: 30 days
- Manifests/graphs: 90 days

---

## Troubleshooting Failed Workflows

### Common Issues

**Documentation Validation fails**:
- Check skill SKILL.md for required sections
- Ensure proper markdown formatting
- See `.github/scripts/README.md` for required sections

**Consistency Check fails**:
- Verify directory names are kebab-case
- Check SKILL.md capitalization
- Verify manifest contains all skills

**Skill Testing fails**:
- Add code examples to documentation
- Define triggers section
- Add main heading

**Manifest Builder fails**:
- Verify no untracked skill files
- Check write permissions
- Review manifest data for integrity

**Dependency Analysis fails**:
- Check for circular dependencies
- Verify skill references are valid
- Review dependency graph output

---

## Performance

Typical workflow execution times:

| Workflow | Runtime | Notes |
|----------|---------|-------|
| Documentation Validation | ~30s | Fast, sequential checks |
| Consistency Check | ~20s | Directory scan only |
| Skill Testing | ~45s | Tests all skills |
| Manifest Builder | ~60s | Scans + file I/O + commit |
| Dependency Analysis | ~120s | Graph analysis algorithms |

**Total time for all workflows**: ~5 minutes

---

## Best Practices

1. **Local Testing**: Run scripts locally before pushing
   ```bash
   python .github/scripts/validate_docs.py
   ```

2. **Check Artifacts**: Review generated reports for insights
   - JSON reports contain details
   - Text reports are human-readable

3. **Manifest Updates**: Manifest builder auto-commits on main
   - Changes propagate to all branches
   - Helps keep skills in sync

4. **Dependency Awareness**: Check dependency graph for design issues
   - Circular dependencies should be resolved
   - Bundles can be optimized

5. **Schedule Awareness**: Heavy workflows run on schedule
   - Dependency analysis weekly
   - Reduces main branch load

---

## Adding New Workflows

When adding new workflows:
1. Create script in `.github/scripts/`
2. Create YAML workflow file in `.github/workflows/`
3. Use consistent logging from `common_utils.py`
4. Document in this file
5. Test on feature branch first

---

## Support

For issues with workflows:
1. Check GitHub Actions logs
2. Review script output in artifacts
3. See `.github/scripts/README.md` for script documentation
4. Check this file for workflow triggers and behavior
