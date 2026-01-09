# Comprehensive Test Suite for Claude Code Skills

## Overview

This test suite provides thorough coverage of all claude-code-skills functionality including:
- **Phase 2**: Enhanced installation tests with negative cases
- **Phase 3**: Meta-skills execution tests with validation

## Test Structure

```
tests/
├── README_TESTS.md              # This file
├── requirements.txt             # Test dependencies
├── test_skills.py               # Existing basic tests
├── validate_skills.py           # Existing validation
├── test_install_enhanced.py     # NEW - Enhanced install tests
├── test_meta_skills.py          # NEW - Meta-skills execution tests
├── runners/                     # Test utilities
│   ├── __init__.py
│   └── skill_executor.py        # Skill execution framework
└── fixtures/                    # Test data
    ├── mock_repos/
    ├── mock_sessions/
    ├── corrupted_skills/
    └── empty_contexts/
```

## Installation

Install test dependencies:

```bash
cd tests
pip install -r requirements.txt
```

## Running Tests

### Run All Tests

```bash
# From repository root
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html -v
```

### Run Specific Test Suites

```bash
# Enhanced installation tests (Phase 2)
pytest tests/test_install_enhanced.py -v

# Meta-skills tests (Phase 3)
pytest tests/test_meta_skills.py -v

# Original validation tests
python tests/validate_skills.py

# Original functionality tests
python tests/test_skills.py
```

### Run Specific Test Classes

```bash
# Session snapshot tests
pytest tests/test_meta_skills.py::TestSessionSnapshot -v

# Skill extractor tests
pytest tests/test_meta_skills.py::TestSkillExtractor -v

# Installation negative tests
pytest tests/test_install_enhanced.py -v -k "negative"
```

### Run with Markers

```bash
# Run only negative tests (once markers are added)
pytest tests/ -v -m negative

# Run only positive tests
pytest tests/ -v -m positive
```

## Test Coverage

### Phase 2: Enhanced Installation Tests

**Positive Tests:**
- ✅ Install specific skill
- ✅ Install by category (meta, development, git, analysis)
- ✅ Install all skills
- ✅ Verify installation
- ✅ List available skills
- ✅ Dry-run mode
- ✅ Handle duplicate installations
- ✅ Handle paths with spaces

**Negative Tests:**
- ✅ Install non-existent skill (should fail gracefully)
- ✅ Install invalid category (should error)
- ✅ Install to read-only directory (should fail)
- ✅ Install with conflicting options (should error)
- ✅ Empty skills list (should fail)
- ✅ Verify non-existent installation (should fail)

### Phase 3: Meta-Skills Execution Tests

#### session-snapshot

**Positive Tests:**
- ✅ Parse skill file
- ✅ Create basic snapshot
- ✅ Include all required fields (timestamp, task, phase, context, next steps)
- ✅ Validate snapshot format

**Negative Tests:**
- ✅ Create without write permissions (should fail)
- ✅ Resume from corrupted snapshot (should detect errors)
- ✅ Missing timestamp (should fail validation)
- ✅ Empty snapshot (should fail validation)

#### skill-extractor

**Positive Tests:**
- ✅ Extract skill from session with repeated patterns
- ✅ Generated skill has valid structure
- ✅ Identify recurring patterns in conversation

**Negative Tests:**
- ✅ Extract from empty conversation (should handle gracefully)
- ✅ Extract from non-existent session (should fail)
- ✅ Generated skill too short (should fail validation)
- ✅ Missing required sections (should fail validation)

#### skill-recommendation-engine

**Positive Tests:**
- ✅ Recommend skills based on context
- ✅ Recommend git skills for repository context

**Negative Tests:**
- ✅ Recommend with empty context (should handle gracefully)
- ✅ Recommend with invalid context (should handle gracefully)

#### manifest-generator

**Positive Tests:**
- ✅ Generate manifest file
- ✅ Include all categories (meta, development, git, analysis)

**Negative Tests:**
- ✅ Generate without skills directory (should fail)
- ✅ Generate with corrupted skill files (should handle errors)
- ✅ Empty manifest content (should fail validation)

## Test Utilities

### SkillExecutor

Main testing framework for executing skills in controlled environment:

```python
from runners.skill_executor import SkillExecutor

with SkillExecutor() as executor:
    # Parse skill file
    skill_data = executor.parse_skill_file(Path('skill.md'))

    # Create test files
    executor.simulate_file_creation('test.md', 'content')

    # Validate outputs
    is_valid, errors = executor.validate_snapshot_format(path)
```

### MockGitRepo

Simulate git repository for testing:

```python
from runners.skill_executor import MockGitRepo

repo = MockGitRepo(test_dir)
repo.create_diff()  # Simulate uncommitted changes
```

### MockSession

Simulate conversation sessions:

```python
from runners.skill_executor import MockSession

session = MockSession()
session.add_pattern('format code', occurrences=3)
session.export_transcript(Path('transcript.txt'))
```

## Expected Test Results

### Success Criteria

All tests should pass with:
- Installation tests: 100% pass rate
- Meta-skills tests: 100% pass rate
- Validation tests: All skills valid
- No unhandled exceptions

### Known Limitations

- Read-only directory tests may be unreliable on Windows
- Some permission tests are skipped on Windows platform
- Git tests require mock git environment (no actual git operations)

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Install test dependencies
  run: pip install -r tests/requirements.txt

- name: Run test suite
  run: pytest tests/ -v --cov --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Future Test Phases

### Phase 4: Integration Tests (Planned)
- Skill chains (repo-briefing → lean-plan → session-snapshot)
- Dependency resolution
- Cross-skill interactions

### Phase 5: Performance Tests (Planned)
- Token usage measurement
- Execution time benchmarks
- Memory usage profiling

### Phase 6: Development/Git/Analysis Skills (Planned)
- lean-plan execution
- quick-test-runner functionality
- diff-summariser output
- Code analysis skills (api-contract-sniffer, dead-code-hunter)
- Formal verification skills (Coq proof analysis)

## Contributing

When adding new tests:

1. Follow existing test structure
2. Include both positive and negative tests
3. Use descriptive test names
4. Add docstrings explaining test purpose
5. Update this README with new coverage
6. Ensure tests are platform-independent where possible

## Troubleshooting

### Import Errors

If you see import errors for `runners.skill_executor`:

```bash
# Ensure you're in the tests directory
cd tests

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/tests"
```

### Permission Errors on Windows

Some tests check file permissions. These may be skipped on Windows:

```python
if sys.platform == "win32":
    pytest.skip("Permission test unreliable on Windows")
```

### Pytest Not Found

Install pytest:

```bash
pip install pytest pytest-cov
```

## Contact

For questions or issues with the test suite, open an issue on the repository.
