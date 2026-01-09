#!/usr/bin/env python3
"""
Skill Validation Suite

Comprehensive validation for Claude Code skills including structure,
syntax, documentation quality, and installation readiness.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse

# Fix Unicode encoding issues on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class SkillValidator:
    """Validates Claude Code skills for structure and quality."""
    
    REQUIRED_SECTIONS = [
        "# {skill_name}",
        "## 🎯 Purpose",
        "## 🚀 Key Features",
        "## 📋 Usage",
        "## 🎛️ Parameters",
        "## 💡 Examples",
        "## 🎁 Output",
        "## ⚠️ Important Notes"
    ]
    
    OPTIONAL_SECTIONS = [
        "## 🔄 Integration with Other Skills",
        "## 🛠️ Advanced Configuration",
        "## 🎯 Best Practices",
        "## 🚨 Troubleshooting",
        "## 📊 Analytics and Insights"
    ]
    
    def __init__(self, skills_dir: str = "skills", verbose: bool = False):
        self.skills_dir = Path(skills_dir)
        self.verbose = verbose
        self.validation_results = {}
        
    def log(self, message: str, level: str = "INFO"):
        """Log messages with verbosity control."""
        if self.verbose or level in ["ERROR", "WARNING"]:
            print(f"[{level}] {message}")
    
    def validate_all_skills(self) -> Dict[str, Dict]:
        """Validate all skills in the skills directory."""
        self.log("Starting comprehensive skill validation...")
        
        if not self.skills_dir.exists():
            self.log(f"Skills directory not found: {self.skills_dir}", "ERROR")
            return {}
        
        # Find all skill files
        skill_files = list(self.skills_dir.rglob("*.md"))
        self.log(f"Found {len(skill_files)} skill files to validate")
        
        results = {}
        for skill_file in skill_files:
            skill_name = skill_file.stem
            self.log(f"Validating skill: {skill_name}")
            results[skill_name] = self.validate_skill_file(skill_file)
        
        self.validation_results = results
        return results
    
    def validate_skill_file(self, skill_file: Path) -> Dict:
        """Validate a single skill file."""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            skill_name = skill_file.stem
            category = skill_file.parent.name
            
            self.log(f"Validating structure for {skill_name}")
            
            validation_result = {
                "file": str(skill_file),
                "skill_name": skill_name,
                "category": category,
                "valid": True,
                "errors": [],
                "warnings": [],
                "recommendations": [],
                "quality_score": 0.0
            }
            
            # Structure validation
            self._validate_structure(content, skill_name, validation_result)
            
            # Content validation
            self._validate_content(content, validation_result)
            
            # Documentation quality
            self._validate_documentation_quality(content, validation_result)
            
            # Parameter table validation
            self._validate_parameter_table(content, validation_result)
            
            # Example validation
            self._validate_examples(content, validation_result)
            
            # Calculate quality score
            validation_result["quality_score"] = self._calculate_quality_score(validation_result)
            
            # Determine overall validity
            validation_result["valid"] = len(validation_result["errors"]) == 0
            
            return validation_result
            
        except Exception as e:
            self.log(f"Error validating {skill_file}: {e}", "ERROR")
            return {
                "file": str(skill_file),
                "skill_name": skill_file.stem if skill_file.stem else "unknown",
                "category": "unknown",
                "valid": False,
                "errors": [f"File reading error: {e}"],
                "warnings": [],
                "recommendations": [],
                "quality_score": 0.0
            }
    
    def _validate_structure(self, content: str, skill_name: str, result: Dict):
        """Validate skill structure and required sections."""
        # Check main header
        main_header_pattern = f"^# {re.escape(skill_name)}$"
        if not re.search(main_header_pattern, content, re.MULTILINE):
            result["errors"].append(f"Missing or incorrect main header: '# {skill_name}'")
        
        # Check required sections
        for section_pattern in self.REQUIRED_SECTIONS:
            pattern = section_pattern.format(skill_name=skill_name)
            if not re.search(re.escape(pattern), content, re.MULTILINE):
                # Try flexible pattern matching
                section_name = pattern.split(":")[0].strip()
                if not re.search(f"^{re.escape(section_name)}", content, re.MULTILINE):
                    result["errors"].append(f"Missing required section: {section_name}")
        
        # Check for section order (basic)
        section_positions = {}
        for section_pattern in self.REQUIRED_SECTIONS:
            pattern = section_pattern.format(skill_name=skill_name)
            match = re.search(re.escape(pattern), content, re.MULTILINE)
            if match:
                section_positions[pattern] = match.start()
        
        # Verify sections appear in reasonable order
        sorted_positions = sorted(section_positions.values())
        if sorted_positions != list(sorted_positions):
            result["warnings"].append("Sections may not be in optimal order")
    
    def _validate_content(self, content: str, result: Dict):
        """Validate content quality and completeness."""
        # Check for empty sections
        section_pattern = r'^## (.+)$\n*(.*?)(?=^## |^# |\Z)'
        sections = re.findall(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        for section_title, section_content in sections:
            section_content = section_content.strip()
            if not section_content or len(section_content) < 10:
                result["warnings"].append(f"Section '{section_title}' appears to be very short or empty")
        
        # Check for minimum content length
        content_length = len(content)
        if content_length < 1000:
            result["warnings"].append(f"Content length ({content_length}) is quite short")
        elif content_length < 500:
            result["errors"].append(f"Content length ({content_length}) is too short for a comprehensive skill")
        
        # Check for emoji usage (should have some for readability)
        emoji_pattern = r'[🎯🚀📋🎛️💡🎁⚠️🔄🛠️]'
        emoji_count = len(re.findall(emoji_pattern, content))
        if emoji_count < 5:
            result["recommendations"].append("Consider adding more emojis for better section identification and readability")
    
    def _validate_documentation_quality(self, content: str, result: Dict):
        """Validate documentation quality and completeness."""
        # Check for code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        if len(code_blocks) < 2:
            result["warnings"].append("Consider adding more code examples")
        
        # Check for command examples
        command_pattern = r'claude skills use \w+'
        commands = re.findall(command_pattern, content)
        if len(commands) < 3:
            result["warnings"].append("Consider adding more usage examples with 'claude skills use' commands")
        
        # Check for parameter documentation
        parameter_section = re.search(r'## 🎛️ Parameters[\s\S]*?(?=## |# |\Z)', content, re.MULTILINE)
        if parameter_section:
            # Check for parameter table format
            if '|' not in parameter_section.group():
                result["warnings"].append("Parameter section should use table format for better readability")
        else:
            result["errors"].append("Missing parameter documentation section")
        
        # Check for output examples
        if '## 🎁 Output' not in content:
            result["warnings"].append("Consider adding output examples section")
    
    def _validate_parameter_table(self, content: str, result: Dict):
        """Validate parameter table format and completeness."""
        parameter_section = re.search(r'## 🎛️ Parameters[\s\S]*?(?=## |# |\Z)', content, re.MULTILINE)
        if not parameter_section:
            return
        
        param_section_content = parameter_section.group()
        
        # Look for markdown tables
        table_pattern = r'\|(.+?)\|\s*\n\|[-:\s|]+\|\s*\n((?:\|.+?\|\s*\n?)*)'
        tables = re.findall(table_pattern, param_section_content)
        
        if not tables:
            result["warnings"].append("Parameter section should use markdown table format")
            return
        
        # Validate table headers
        for table_header, table_rows in tables:
            header_cells = [cell.strip() for cell in table_header.split('|')]
            expected_headers = ["Parameter", "Type", "Required", "Description"]
            
            # Check if all expected headers are present
            missing_headers = []
            for expected in expected_headers:
                if not any(expected.lower() in header.lower() for header in header_cells):
                    missing_headers.append(expected)
            
            if missing_headers:
                result["warnings"].append(f"Parameter table missing headers: {missing_headers}")
    
    def _validate_examples(self, content: str, result: Dict):
        """Validate examples section quality and variety."""
        examples_section = re.search(r'## 💡 Examples[\s\S]*?(?=## |# |\Z)', content, re.MULTILINE)
        if not examples_section:
            result["errors"].append("Missing examples section")
            return
        
        examples_content = examples_section.group()
        
        # Count different types of examples
        basic_examples = len(re.findall(r'###.*[Bb]asic', examples_content))
        advanced_examples = len(re.findall(r'###.*[Aa]dvanced', examples_content))
        
        if basic_examples == 0:
            result["warnings"].append("Consider adding basic usage examples")
        if advanced_examples == 0:
            result["warnings"].append("Consider adding advanced usage examples")
        
        # Check for code blocks in examples
        example_code_blocks = re.findall(r'```[\s\S]*?```', examples_content)
        if len(example_code_blocks) < 2:
            result["warnings"].append("Examples section should include multiple code examples")
    
    def _calculate_quality_score(self, result: Dict) -> float:
        """Calculate overall quality score based on validation results."""
        base_score = 1.0
        
        # Deduct for errors
        base_score -= len(result["errors"]) * 0.2
        
        # Deduct for warnings
        base_score -= len(result["warnings"]) * 0.05
        
        # Deduct for missing recommendations
        if len(result["recommendations"]) > 3:
            base_score -= 0.1
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, base_score))
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate a comprehensive validation report."""
        if not self.validation_results:
            return "No validation results available. Run validate_all_skills() first."
        
        total_skills = len(self.validation_results)
        valid_skills = sum(1 for result in self.validation_results.values() if result["valid"])
        average_quality = sum(result["quality_score"] for result in self.validation_results.values()) / total_skills
        
        report = []
        report.append("=" * 60)
        report.append("CLAUDE CODE SKILLS VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"Total Skills Validated: {total_skills}")
        report.append(f"Valid Skills: {valid_skills}")
        report.append(f"Invalid Skills: {total_skills - valid_skills}")
        report.append(f"Average Quality Score: {average_quality:.2f}/1.00")
        report.append("")
        
        # Detailed results by skill
        report.append("DETAILED RESULTS:")
        report.append("-" * 40)
        
        for skill_name, result in sorted(self.validation_results.items()):
            status = "✅ VALID" if result["valid"] else "❌ INVALID"
            quality = result["quality_score"]
            
            report.append(f"\n{skill_name} ({result['category']})")
            report.append(f"  Status: {status}")
            report.append(f"  Quality: {quality:.2f}/1.00")
            report.append(f"  File: {result['file']}")
            
            if result["errors"]:
                report.append("  Errors:")
                for error in result["errors"]:
                    report.append(f"    • {error}")
            
            if result["warnings"]:
                report.append("  Warnings:")
                for warning in result["warnings"]:
                    report.append(f"    • {warning}")
            
            if result["recommendations"]:
                report.append("  Recommendations:")
                for rec in result["recommendations"]:
                    report.append(f"    • {rec}")
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report_text)
            self.log(f"Report saved to: {output_file}")
        
        return report_text


def main():
    """Main CLI interface for skill validation."""
    parser = argparse.ArgumentParser(description="Validate Claude Code skills")
    parser.add_argument("--skills-dir", default="skills", help="Skills directory path")
    parser.add_argument("--skill", help="Validate specific skill by name")
    parser.add_argument("--output", help="Output report to file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    validator = SkillValidator(args.skills_dir, args.verbose)
    
    if args.skill:
        # Validate specific skill
        skill_file = Path(args.skills_dir) / f"{args.skill}.md"
        if not skill_file.exists():
            print(f"❌ Skill file not found: {skill_file}")
            sys.exit(1)
        
        result = validator.validate_skill_file(skill_file)
        results = {args.skill: result}
    else:
        # Validate all skills
        results = validator.validate_all_skills()
    
    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        report = validator.generate_report(args.output)
        print(report)
    
    # Exit with error code if any skills are invalid
    invalid_count = sum(1 for result in results.values() if not result["valid"])
    if invalid_count > 0:
        print(f"\n❌ {invalid_count} skill(s) failed validation")
        sys.exit(1)
    else:
        print(f"\n✅ All skills passed validation")


if __name__ == "__main__":
    main()