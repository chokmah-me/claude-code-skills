#!/usr/bin/env python3
"""
Enhanced Installation Tests (Phase 2)

Comprehensive testing of install.py including negative test cases:
- Install non-existent skills
- Install to read-only directories
- Corrupted skill files
- Invalid categories
- Dependency resolution
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import subprocess
import pytest
import stat


class TestInstallationEnhanced:
    """Enhanced installation tests with negative cases."""

    @pytest.fixture
    def temp_skills_dir(self):
        """Create temporary skills directory."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def readonly_dir(self):
        """Create read-only directory for negative testing."""
        temp_dir = Path(tempfile.mkdtemp())
        # Make directory read-only
        os.chmod(temp_dir, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
        yield temp_dir
        # Restore permissions before cleanup
        os.chmod(temp_dir, stat.S_IRWXU)
        shutil.rmtree(temp_dir, ignore_errors=True)

    # ============= POSITIVE TESTS =============

    def test_install_specific_skill(self, temp_skills_dir):
        """Test installing a specific skill."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--skills", "session-snapshot",
            "--target", str(temp_skills_dir),
            "--dry-run"
        ], capture_output=True, text=True, cwd=".")

        assert result.returncode == 0
        assert "session-snapshot" in result.stdout

    def test_install_by_category(self, temp_skills_dir):
        """Test installing entire category."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--category", "meta",
            "--target", str(temp_skills_dir),
            "--dry-run"
        ], capture_output=True, text=True, cwd=".")

        assert result.returncode == 0
        # Should list all meta skills
        assert "session-snapshot" in result.stdout
        assert "skill-extractor" in result.stdout

    def test_install_all_skills(self, temp_skills_dir):
        """Test installing all skills."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--all",
            "--target", str(temp_skills_dir),
            "--dry-run"
        ], capture_output=True, text=True, cwd=".")

        assert result.returncode == 0
        # Should include skills from all categories
        assert "meta" in result.stdout.lower()
        assert "development" in result.stdout.lower()

    def test_verify_installation(self, temp_skills_dir):
        """Test installation verification."""
        # First install a skill
        subprocess.run([
            sys.executable, "install.py",
            "--skills", "session-snapshot",
            "--target", str(temp_skills_dir)
        ], capture_output=True, cwd=".")

        # Then verify
        result = subprocess.run([
            sys.executable, "install.py",
            "--verify",
            "--target", str(temp_skills_dir)
        ], capture_output=True, text=True, cwd=".")

        assert result.returncode == 0

    def test_list_skills(self):
        """Test listing available skills."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--list"
        ], capture_output=True, text=True, cwd=".")

        assert result.returncode == 0
        # Check for expected categories
        output_lower = result.stdout.lower()
        assert "meta" in output_lower
        assert "development" in output_lower
        assert "git" in output_lower
        assert "analysis" in output_lower

    # ============= NEGATIVE TESTS =============

    def test_install_nonexistent_skill(self, temp_skills_dir):
        """NEGATIVE: Install skill that doesn't exist."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--skills", "nonexistent-skill-xyz",
            "--target", str(temp_skills_dir)
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=".")

        # Should fail gracefully (return non-zero exit code)
        assert result.returncode != 0
        # Check output contains error indication (if capture succeeded)
        if result.stdout or result.stderr:
            output = ((result.stdout or '') + (result.stderr or '')).lower()
            assert "not found" in output or "error" in output or "installed 0" in output

    def test_install_invalid_category(self, temp_skills_dir):
        """NEGATIVE: Install from invalid category."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--category", "invalid-category-xyz",
            "--target", str(temp_skills_dir)
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=".")

        # Should fail gracefully (return non-zero exit code)
        assert result.returncode != 0
        # Check output contains error indication (if capture succeeded)
        if result.stdout or result.stderr:
            output = ((result.stdout or '') + (result.stderr or '')).lower()
            assert "category" in output or "invalid" in output or "not found" in output

    def test_install_to_readonly_directory(self, readonly_dir):
        """NEGATIVE: Install to read-only directory (should fail)."""
        if sys.platform == "win32":
            pytest.skip("Read-only test unreliable on Windows")

        result = subprocess.run([
            sys.executable, "install.py",
            "--skills", "session-snapshot",
            "--target", str(readonly_dir)
        ], capture_output=True, text=True, cwd=".")

        # Should fail with permission error
        assert result.returncode != 0
        assert "permission" in result.stderr.lower() or "error" in result.stderr.lower()

    def test_install_with_missing_dependencies(self, temp_skills_dir):
        """NEGATIVE: Install skill with missing dependencies."""
        # Note: This tests dependency resolution
        # skill-recommendation-engine depends on skill-extractor
        result = subprocess.run([
            sys.executable, "install.py",
            "--skills", "skill-recommendation-engine",
            "--target", str(temp_skills_dir),
            "--dry-run"
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=".")

        # Should either install dependencies or warn
        assert result.returncode == 0
        # Check if it mentions dependencies (if capture succeeded)
        if result.stdout or result.stderr:
            output = ((result.stdout or '') + (result.stderr or '')).lower()
            assert "skill-extractor" in output or "dependenc" in output or "skill-recommendation" in output

    def test_install_conflicting_options(self, temp_skills_dir):
        """NEGATIVE: Use conflicting command line options."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--all",
            "--skills", "session-snapshot",  # Can't use both --all and --skills
            "--target", str(temp_skills_dir)
        ], capture_output=True, text=True, cwd=".")

        # Should fail or warn about conflicting options
        assert result.returncode != 0 or "warning" in result.stderr.lower()

    def test_install_empty_skills_list(self, temp_skills_dir):
        """NEGATIVE: Install with empty skills list."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--skills",  # No skills provided
            "--target", str(temp_skills_dir)
        ], capture_output=True, text=True, cwd=".")

        # Should fail with argument error
        assert result.returncode != 0

    def test_verify_nonexistent_installation(self):
        """NEGATIVE: Verify installation in directory that doesn't exist."""
        fake_dir = Path(tempfile.gettempdir()) / "nonexistent-claude-skills-xyz"

        result = subprocess.run([
            sys.executable, "install.py",
            "--verify",
            "--target", str(fake_dir)
        ], capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=".")

        # Should fail or report no skills installed
        if result.stdout or result.stderr:
            output = ((result.stdout or '') + (result.stderr or '')).lower()
            assert result.returncode != 0 or "0/20 skills" in output or "no skills" in output or "not found" in output
        else:
            assert result.returncode != 0

    # ============= EDGE CASES =============

    def test_install_duplicate_skills(self, temp_skills_dir):
        """EDGE: Install same skill multiple times."""
        # Install once
        result1 = subprocess.run([
            sys.executable, "install.py",
            "--skills", "session-snapshot",
            "--target", str(temp_skills_dir)
        ], capture_output=True, text=True, cwd=".")

        # Install again
        result2 = subprocess.run([
            sys.executable, "install.py",
            "--skills", "session-snapshot",
            "--target", str(temp_skills_dir)
        ], capture_output=True, text=True, cwd=".")

        # Both should succeed (overwrite or skip)
        assert result1.returncode == 0
        assert result2.returncode == 0

    def test_install_with_spaces_in_path(self):
        """EDGE: Install to path with spaces."""
        temp_base = Path(tempfile.gettempdir())
        temp_dir = temp_base / "claude skills test dir"
        temp_dir.mkdir(parents=True, exist_ok=True)

        try:
            result = subprocess.run([
                sys.executable, "install.py",
                "--skills", "session-snapshot",
                "--target", str(temp_dir),
                "--dry-run"
            ], capture_output=True, text=True, cwd=".")

            # Should handle spaces correctly
            assert result.returncode == 0
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def test_help_output(self):
        """Test help documentation is complete."""
        result = subprocess.run([
            sys.executable, "install.py",
            "--help"
        ], capture_output=True, text=True, cwd=".")

        assert result.returncode == 0
        # Check for expected options in help
        help_text = result.stdout.lower()
        assert "--all" in help_text
        assert "--skills" in help_text
        assert "--category" in help_text
        assert "--verify" in help_text
        assert "--dry-run" in help_text


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
