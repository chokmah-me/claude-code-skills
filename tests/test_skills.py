#!/usr/bin/env python3
"""
Basic Skill Functionality Tests

Tests the core functionality of Claude Code skills including installation,
basic operations, and integration testing.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import subprocess
import argparse


class SkillTester:
    """Test suite for Claude Code skills functionality."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_results = {}
        self.temp_dir = None
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with verbosity control."""
        if self.verbose or level in ["ERROR", "WARNING"]:
            print(f"[{level}] {message}")
    
    def setup_test_environment(self):
        """Set up temporary test environment."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.log(f"Created test environment: {self.temp_dir}")
        
        # Create mock Claude Code skills directory
        skills_dir = self.temp_dir / ".claude" / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)
        
        return str(skills_dir)
    
    def cleanup_test_environment(self):
        """Clean up temporary test environment."""
        if self.temp_dir and self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)
            self.log("Cleaned up test environment")
    
    def test_installation_script(self) -> bool:
        """Test the installation script functionality."""
        self.log("Testing installation script...")
        
        try:
            # Test help output
            result = subprocess.run([
                sys.executable, "install.py", "--help"
            ], capture_output=True, text=True, cwd=".")
            
            if result.returncode != 0:
                self.log("Installation script help failed", "ERROR")
                return False
            
            if "--all" not in result.stdout:
                self.log("Installation script missing expected options", "ERROR")
                return False
            
            self.log("✅ Installation script help test passed")
            return True
            
        except Exception as e:
            self.log(f"Installation script test failed: {e}", "ERROR")
            return False
    
    def test_skill_listing(self) -> bool:
        """Test skill listing functionality."""
        self.log("Testing skill listing...")
        
        try:
            # Test list command
            result = subprocess.run([
                sys.executable, "install.py", "--list"
            ], capture_output=True, text=True, cwd=".")
            
            if result.returncode != 0:
                self.log("Skill listing failed", "ERROR")
                return False
            
            # Check for expected categories
            expected_categories = ["meta", "development", "git", "analysis"]
            output = result.stdout.lower()
            
            for category in expected_categories:
                if category not in output:
                    self.log(f"Missing category in listing: {category}", "WARNING")
            
            self.log("✅ Skill listing test passed")
            return True
            
        except Exception as e:
            self.log(f"Skill listing test failed: {e}", "ERROR")
            return False
    
    def test_dry_run_installation(self) -> bool:
        """Test dry-run installation functionality."""
        self.log("Testing dry-run installation...")
        
        try:
            # Test dry-run for specific skills
            result = subprocess.run([
                sys.executable, "install.py", 
                "--skills", "session-snapshot", "skill-extractor",
                "--dry-run"
            ], capture_output=True, text=True, cwd=".")
            
            if result.returncode != 0:
                self.log("Dry-run installation failed", "ERROR")
                return False
            
            # Check for dry-run indicators
            output = result.stdout
            if "Would install" not in output:
                self.log("Dry-run output missing expected content", "WARNING")
            
            self.log("✅ Dry-run installation test passed")
            return True
            
        except Exception as e:
            self.log(f"Dry-run installation test failed: {e}", "ERROR")
            return False
    
    def test_skill_files_exist(self) -> bool:
        """Test that expected skill files exist."""
        self.log("Testing skill file existence...")
        
        expected_skills = [
            ("meta", "session-snapshot.md"),
            ("meta", "skill-extractor.md"),
            ("development", "debug-assistant.md")
        ]
        
        all_exist = True
        for category, skill_file in expected_skills:
            skill_path = Path("skills") / category / skill_file
            if not skill_path.exists():
                self.log(f"Missing skill file: {skill_path}", "ERROR")
                all_exist = False
            else:
                self.log(f"✅ Found skill file: {skill_path}")
        
        return all_exist
    
    def test_skill_content_basic(self) -> bool:
        """Test basic content of skill files."""
        self.log("Testing skill content basics...")
        
        test_skills = [
            "skills/meta/session-snapshot.md",
            "skills/meta/skill-extractor.md"
        ]
        
        all_valid = True
        for skill_path in test_skills:
            try:
                with open(skill_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for basic structure
                required_elements = [
                    "# ",  # Main header
                    "## 🎯 Purpose",
                    "## 🚀 Key Features", 
                    "## 📋 Usage",
                    "claude skills use"  # Usage example
                ]
                
                for element in required_elements:
                    if element not in content:
                        self.log(f"Missing element in {skill_path}: {element}", "ERROR")
                        all_valid = False
                
                # Check minimum length
                if len(content) < 500:
                    self.log(f"Content too short in {skill_path}", "ERROR")
                    all_valid = False
                
                if all_valid:
                    self.log(f"✅ Basic content validation passed for {skill_path}")
                
            except Exception as e:
                self.log(f"Content validation failed for {skill_path}: {e}", "ERROR")
                all_valid = False
        
        return all_valid
    
    def test_readme_quality(self) -> bool:
        """Test README.md quality and completeness."""
        self.log("Testing README.md quality...")
        
        try:
            with open("README.md", 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Check for key sections
            key_sections = [
                "# Claude Code Skills",
                "## 🌟 Overview",
                "## 🚀 Quick Start",
                "## 📋 Available Skills",
                "## 🤝 Contributing",
                "## 📄 License"
            ]
            
            missing_sections = []
            for section in key_sections:
                if section not in readme_content:
                    missing_sections.append(section)
            
            if missing_sections:
                self.log(f"README missing sections: {missing_sections}", "WARNING")
            
            # Check for key features mentioned
            key_features = ["session-snapshot", "skill-extractor", "16+"]
            missing_features = []
            for feature in key_features:
                if feature not in readme_content:
                    missing_features.append(feature)
            
            if missing_features:
                self.log(f"README missing key features: {missing_features}", "WARNING")
            
            # Check minimum length
            if len(readme_content) < 2000:
                self.log("README content seems too short", "WARNING")
            
            self.log("✅ README quality test completed")
            return len(missing_sections) == 0 and len(missing_features) == 0
            
        except Exception as e:
            self.log(f"README quality test failed: {e}", "ERROR")
            return False
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests and return results."""
        self.log("Starting comprehensive skill testing...")
        
        tests = [
            ("Installation Script", self.test_installation_script),
            ("Skill Listing", self.test_skill_listing),
            ("Dry-run Installation", self.test_dry_run_installation),
            ("Skill Files Existence", self.test_skill_files_exist),
            ("Skill Content Basic", self.test_skill_content_basic),
            ("README Quality", self.test_readme_quality)
        ]
        
        results = {}
        for test_name, test_func in tests:
            try:
                results[test_name] = test_func()
            except Exception as e:
                self.log(f"Test {test_name} failed with exception: {e}", "ERROR")
                results[test_name] = False
        
        self.test_results = results
        return results
    
    def generate_test_report(self) -> str:
        """Generate a comprehensive test report."""
        if not self.test_results:
            return "No test results available. Run run_all_tests() first."
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result)
        failed_tests = total_tests - passed_tests
        
        report = []
        report.append("=" * 60)
        report.append("CLAUDE CODE SKILLS FUNCTIONAL TEST REPORT")
        report.append("=" * 60)
        report.append(f"Total Tests: {total_tests}")
        report.append(f"Passed: {passed_tests}")
        report.append(f"Failed: {failed_tests}")
        report.append(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        report.append("")
        
        # Detailed results
        report.append("DETAILED RESULTS:")
        report.append("-" * 40)
        
        for test_name, passed in sorted(self.test_results.items()):
            status = "✅ PASS" if passed else "❌ FAIL"
            report.append(f"{status} {test_name}")
        
        return "\n".join(report)


def main():
    """Main CLI interface for skill testing."""
    parser = argparse.ArgumentParser(description="Test Claude Code skills functionality")
    parser.add_argument("--skill", help="Test specific skill by name")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    tester = SkillTester(args.verbose)
    
    try:
        # Setup test environment
        tester.setup_test_environment()
        
        # Run tests
        if args.skill:
            print(f"Testing specific skill functionality not implemented yet: {args.skill}")
        else:
            results = tester.run_all_tests()
            report = tester.generate_test_report()
            print(report)
            
            # Exit with error code if any tests failed
            failed_count = sum(1 for result in results.values() if not result)
            if failed_count > 0:
                print(f"\n❌ {failed_count} test(s) failed")
                sys.exit(1)
            else:
                print(f"\n✅ All tests passed!")
                
    finally:
        # Cleanup
        tester.cleanup_test_environment()


if __name__ == "__main__":
    main()