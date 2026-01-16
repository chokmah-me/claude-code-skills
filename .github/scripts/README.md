# GitHub Actions Scripts

This directory contains reusable Python scripts for Claude Code skills repository automation.

## Overview

All scripts follow consistent patterns:
- **Exit Code 0**: Success
- **Exit Code 1**: Critical failure
- **Exit Code 2**: Warnings (non-fatal issues)
- **Logging**: Color-coded output with emojis
- **Utilities**: Shared functions in `common_utils.py`

## Scripts

### 1. `common_utils.py`
Shared utilities used by all other scripts.

**Functions**:
- `load_json(path)` - Load JSON files with error handling
- `save_json(data, path)` - Save data to JSON with pretty formatting
- `find_files(pattern, directory)` - Recursively find files by glob pattern
- `find_all_skills()` - Find all SKILL.md files in repository
- `get_repo_root()` - Get repository root directory
- `log_info/warning/error/success()` - Colored logging functions
- `exit_success/failure/warning()` - Standardized exit handlers

**Used by**: All other scripts

---

### 2. `validate_docs.py`
Validates skill documentation meets required standards.

**Purpose**: Ensure all skills have complete, properly-formatted documentation

**Validates**:
- Required sections: Description, Triggers, Usage, Parameters, Output
- File exists and is readable
- Basic markdown structure
- Code examples present

**Output**: `validation-report.json`

**Exit Codes**:
- `0` - All skills valid
- `1` - One or more skills have validation errors
- `2` - Some skills missing code examples

**Usage**:
```bash
python .github/scripts/validate_docs.py
python .github/scripts/validate_docs.py --verbose
```

---

### 3. `check_consistency.py`
Validates skill directory structure and naming conventions.

**Purpose**: Enforce repository-wide consistency standards

**Checks**:
- Directory names are kebab-case
- SKILL.md filenames are uppercase
- Skills organized under valid categories
- All skills present in manifest

**Output**: Console output with details

**Exit Codes**:
- `0` - All checks passed
- `1` - Issues found
- `2` - Warnings only

**Usage**:
```bash
python .github/scripts/check_consistency.py
python .github/scripts/check_consistency.py --verbose
```

---

### 4. `build_manifest.py`
Scans all skills and generates unified manifest files.

**Purpose**: Keep manifest files automatically updated

**Generates**:
- `SKILL_MANIFEST.json` - Machine-readable manifest
- `UNIFIED_SKILL_MANIFEST.md` - Human-readable manifest

**Extracts from skills**:
- Name, description, triggers
- Category placement
- Metadata from markdown headers

**Output**: JSON and Markdown manifest files

**Exit Codes**:
- `0` - Manifest generated successfully
- `1` - Failed to scan or save
- `2` - Warnings during generation

**Usage**:
```bash
python .github/scripts/build_manifest.py
python .github/scripts/build_manifest.py --dry-run
```

---

### 5. `test_skills.py`
Runs comprehensive tests on skill documentation.

**Purpose**: Ensure skills are properly documented and functional

**Tests**:
- Required sections present and have content
- Code blocks/examples exist
- Trigger phrases defined
- Main heading (title) present
- Markdown structure valid

**Output**: `test-results.json`

**Exit Codes**:
- `0` - All tests passed
- `1` - Some tests failed
- `2` - Tests passed with warnings

**Usage**:
```bash
python .github/scripts/test_skills.py
python .github/scripts/test_skills.py --verbose
```

---

### 6. `analyze_dependencies.py`
Analyzes skill dependencies and builds dependency graphs.

**Purpose**: Identify circular dependencies and suggest skill bundles

**Analyzes**:
- References between skills
- Dependency graph structure
- Circular dependencies
- Suggested skill bundles

**Output**: `dependency-graph.json`

**Exit Codes**:
- `0` - Analysis complete, no critical issues
- `1` - Circular dependencies detected
- `2` - Analysis complete with warnings

**Usage**:
```bash
python .github/scripts/analyze_dependencies.py
python .github/scripts/analyze_dependencies.py --verbose
```

---

## Running Locally

### Prerequisites
```bash
python 3.10+
git
```

### Run All Validation Scripts
```bash
cd /path/to/repo
python .github/scripts/validate_docs.py
python .github/scripts/check_consistency.py
python .github/scripts/test_skills.py
python .github/scripts/build_manifest.py
python .github/scripts/analyze_dependencies.py
```

### Run Individual Script
```bash
python .github/scripts/validate_docs.py --verbose
```

### Check Exit Codes
```bash
python .github/scripts/validate_docs.py
echo "Exit code: $?"
```

## Integration with GitHub Actions

These scripts are called from workflow files:
- `documentation-validation.yml` - Calls `validate_docs.py`
- `consistency-check.yml` - Calls `check_consistency.py`
- `skill-testing.yml` - Calls `test_skills.py`
- `manifest-builder.yml` - Calls `build_manifest.py`
- `dependency-analysis.yml` - Calls `analyze_dependencies.py`

Workflows run automatically on:
- **Push to main/develop**
- **Pull requests to main/develop**
- **Manual triggers** (`workflow_dispatch`)
- **Schedules** (nightly/weekly for heavy operations)

## Troubleshooting

### Import Errors
If you see `ImportError: No module named 'common_utils'`, ensure you're running from the repository root:
```bash
cd /path/to/claude-code-skills
python .github/scripts/validate_docs.py
```

### Permission Denied
Make scripts executable:
```bash
chmod +x .github/scripts/*.py
```

### Missing Dependencies
Install Python dependencies:
```bash
pip install pyyaml jsonschema markdown-it-py networkx
```

## Adding New Scripts

When creating a new script:
1. Import `common_utils` for shared functions
2. Follow naming convention: `action-name.py`
3. Include docstring with purpose
4. Use consistent logging: `log_info/warning/error/success()`
5. Exit with appropriate code (0, 1, or 2)
6. Add entry to this README
7. Create corresponding workflow file

## Contributing

- Keep scripts focused and single-purpose
- Use `common_utils` for shared functionality
- Log all significant operations
- Exit with meaningful codes
- Document new scripts in README
