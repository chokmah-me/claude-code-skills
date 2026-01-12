import re
from pathlib import Path
import yaml
import json
from datetime import datetime
import sys

class DocumentationValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.stats = {'total_skills': 0, 'valid_skills': 0, 'missing_docs': 0}

    def validate_skill(self, skill_path, category, skill_name):
        '''Validate a single skill's documentation'''
        self.stats['total_skills'] += 1
        skill_valid = True

        print(f'[SCAN] Validating {category}/{skill_name}...')

        # Check required files
        skill_dir = Path(skill_path)

        # SKILL.md is required
        skill_file = skill_dir / 'SKILL.md'
        if not skill_file.exists():
            self.errors.append(f'{category}/{skill_name}: Missing SKILL.md')
            skill_valid = False
        else:
            self.validate_skill_file(skill_file, category, skill_name)

        # README.md is highly recommended
        readme_file = skill_dir / 'README.md'
        if not readme_file.exists():
            self.warnings.append(f'{category}/{skill_name}: Missing README.md')
        else:
            self.validate_readme_file(readme_file, category, skill_name)

        # template.md is recommended for meta skills
        template_file = skill_dir / 'template.md'
        if category == 'meta' and not template_file.exists():
            self.warnings.append(f'{category}/{skill_name}: Meta skill missing template.md')
        elif template_file.exists():
            self.validate_template_file(template_file, category, skill_name)

        if skill_valid:
            self.stats['valid_skills'] += 1
            print(f'  [OK] {skill_name} documentation is valid')
        else:
            self.stats['missing_docs'] += 1
            print(f'  [ERROR] {skill_name} has documentation issues')

    def validate_skill_file(self, file_path, category, skill_name):
        '''Validate SKILL.md content'''
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for required sections
            required_sections = ['Purpose:', 'Usage:', 'Examples:']
            for section in required_sections:
                if section not in content:
                    self.warnings.append(f'{category}/{skill_name}: SKILL.md missing {section}')

            # Check for skill invocation pattern
            if f'/{skill_name}' not in content:
                self.warnings.append(f'{category}/{skill_name}: SKILL.md should show skill invocation pattern')

            # Validate YAML frontmatter if present
            if content.startswith('---'):
                try:
                    parts = content.split('---')
                    if len(parts) >= 3:
                        yaml_content = parts[1]
                        metadata = yaml.safe_load(yaml_content)
                        if not isinstance(metadata, dict):
                            self.warnings.append(f'{category}/{skill_name}: Invalid YAML frontmatter')
                except yaml.YAMLError as e:
                    self.warnings.append(f'{category}/{skill_name}: YAML parsing error: {e}')

        except Exception as e:
            self.errors.append(f'{category}/{skill_name}: Error reading SKILL.md: {e}')

    def validate_readme_file(self, file_path, category, skill_name):
        '''Validate README.md content'''
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for recommended sections
            recommended_sections = ['Overview', 'Usage', 'Examples', 'Installation']
            found_sections = 0
            for section in recommended_sections:
                if section.lower() in content.lower():
                    found_sections += 1

            if found_sections < 3:
                self.warnings.append(f'{category}/{skill_name}: README.md missing recommended sections')

            # Check for code examples
            if '```' not in content:
                self.warnings.append(f'{category}/{skill_name}: README.md should include code examples')

            # Check for token efficiency metrics (especially for meta skills)
            if category == 'meta' and 'token' not in content.lower():
                self.warnings.append(f'{category}/{skill_name}: Meta skill README should mention token efficiency')

        except Exception as e:
            self.errors.append(f'{category}/{skill_name}: Error reading README.md: {e}')

    def validate_template_file(self, file_path, category, skill_name):
        '''Validate template.md content'''
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for template placeholders
            template_placeholders = ['{{', '}}', 'PLACEHOLDER', 'TODO']
            found_placeholders = sum(1 for placeholder in template_placeholders if placeholder in content)

            if found_placeholders == 0:
                self.warnings.append(f'{category}/{skill_name}: template.md should contain placeholders for customization')

            # Check for usage instructions
            if 'usage' not in content.lower() and 'how to' not in content.lower():
                self.warnings.append(f'{category}/{skill_name}: template.md should include usage instructions')

        except Exception as e:
            self.errors.append(f'{category}/{skill_name}: Error reading template.md: {e}')

    def generate_report(self):
        '''Generate validation report'''
        print('\n' + '='*60)
        print('[LIST] DOCUMENTATION VALIDATION REPORT')
        print('='*60)

        total = self.stats['total_skills']
        valid = self.stats['valid_skills']
        missing = self.stats['missing_docs']
        success_rate = (valid/max(total, 1)*100)

        print(f'\n[STATS] Statistics:')
        print(f'  Total Skills: {total}')
        print(f'  Valid Skills: {valid}')
        print(f'  Missing Docs: {missing}')
        print(f'  Success Rate: {success_rate:.1f}%')

        if self.errors:
            print(f'\n[ERROR] Errors ({len(self.errors)}):')
            for error in self.errors:
                print(f'  - {error}')

        if self.warnings:
            print(f'\n[WARN]  Warnings ({len(self.warnings)}):')
            for warning in self.warnings:
                print(f'  - {warning}')

        print('\n' + '='*60)

        # Return appropriate exit code
        if self.errors:
            print('[ERROR] Documentation validation FAILED')
            return False
        elif self.warnings:
            print('[WARN]  Documentation validation PASSED with warnings')
            return True
        else:
            print('[OK] Documentation validation PASSED')
            return True

def check_consistency():
    '''Check consistency between different documentation files'''
    errors = []
    warnings = []

    skills_dir = Path('skills')
    if not skills_dir.exists():
        print('[ERROR] Skills directory not found')
        return False

    for category_dir in skills_dir.iterdir():
        if category_dir.is_dir() and category_dir.name != '__pycache__':
            category = category_dir.name

            for skill_dir in category_dir.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    skill_name = skill_dir.name

                    skill_file = skill_dir / 'SKILL.md'
                    readme_file = skill_dir / 'README.md'

                    if skill_file.exists() and readme_file.exists():
                        # Check for consistency between SKILL.md and README.md
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            skill_content = f.read().lower()

                        with open(readme_file, 'r', encoding='utf-8') as f:
                            readme_content = f.read().lower()

                        # Check if skill purpose is consistent
                        skill_purpose = re.search(r'purpose:(.*?)(?:\n|$)', skill_content)
                        readme_purpose = re.search(r'# (.*?)(?:\n|$)', readme_content)

                        if skill_purpose and readme_purpose:
                            skill_desc = skill_purpose.group(1).strip()
                            readme_desc = readme_purpose.group(1).strip()

                            # Simple similarity check (could be improved)
                            if len(skill_desc) > 10 and len(readme_desc) > 10:
                                similarity = len(set(skill_desc.split()) & set(readme_desc.split())) / max(len(set(skill_desc.split())), 1)
                                if similarity < 0.2:
                                    warnings.append(f'{category}/{skill_name}: Purpose descriptions seem inconsistent between SKILL.md and README.md')

                        # Check if examples are present in both
                        skill_has_examples = 'example' in skill_content
                        readme_has_examples = 'example' in readme_content

                        if skill_has_examples and not readme_has_examples:
                            warnings.append(f'{category}/{skill_name}: SKILL.md has examples but README.md does not')
                        elif not skill_has_examples and readme_has_examples:
                            warnings.append(f'{category}/{skill_name}: README.md has examples but SKILL.md does not')

    # Report results
    if warnings:
        print(f'\n[WARN]  Consistency Warnings ({len(warnings)}):')
        for warning in warnings:
            print(f'  - {warning}')

    if errors:
        print(f'\n[ERROR] Consistency Errors ({len(errors)}):')
        for error in errors:
            print(f'  - {error}')
        return False

    print('[OK] Documentation consistency check completed')
    return True

def generate_doc_report():
    '''Generate comprehensive documentation report'''
    report = {
        'timestamp': datetime.now().isoformat(),
        'repository': 'claude-code-skills',
        'documentation_status': {},
        'statistics': {}
    }

    skills_dir = Path('skills')
    if not skills_dir.exists():
        print('[ERROR] Skills directory not found')
        return

    total_skills = 0
    skills_with_readme = 0
    skills_with_template = 0
    meta_skills = 0

    for category_dir in skills_dir.iterdir():
        if category_dir.is_dir() and category_dir.name != '__pycache__':
            category = category_dir.name
            report['documentation_status'][category] = {
                'skills': {},
                'total': 0,
                'with_readme': 0,
                'with_template': 0
            }

            for skill_dir in category_dir.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    skill_name = skill_dir.name
                    total_skills += 1
                    report['documentation_status'][category]['total'] += 1

                    skill_status = {
                        'skill_md': (skill_dir / 'SKILL.md').exists(),
                        'readme_md': (skill_dir / 'README.md').exists(),
                        'template_md': (skill_dir / 'template.md').exists()
                    }

                    if skill_status['readme_md']:
                        skills_with_readme += 1
                        report['documentation_status'][category]['with_readme'] += 1

                    if skill_status['template_md']:
                        skills_with_template += 1
                        report['documentation_status'][category]['with_template'] += 1

                    if category == 'meta':
                        meta_skills += 1

                    report['documentation_status'][category]['skills'][skill_name] = skill_status

    # Calculate statistics
    readme_cov = (skills_with_readme / max(total_skills, 1)) * 100
    template_cov = (skills_with_template / max(total_skills, 1)) * 100

    report['statistics'] = {
        'total_skills': total_skills,
        'skills_with_readme': skills_with_readme,
        'skills_with_template': skills_with_template,
        'meta_skills': meta_skills,
        'readme_coverage': readme_cov,
        'template_coverage': template_cov
    }

    # Save report
    with open('documentation-report.json', 'w') as f:
        json.dump(report, f, indent=2)

    # Generate markdown report
    with open('DOCUMENTATION_REPORT.md', 'w') as f:
        f.write('# Documentation Report\n\n')
        f.write(f'Generated: {report["timestamp"]}\n\n')

        f.write('## [STATS] Statistics\n\n')
        f.write(f'- **Total Skills**: {total_skills}\n')
        f.write(f'- **Skills with README**: {skills_with_readme} ({report["statistics"]["readme_coverage"]:.1f}%)\n')
        f.write(f'- **Skills with Templates**: {skills_with_template} ({report["statistics"]["template_coverage"]:.1f}%)\n')
        f.write(f'- **Meta Skills**: {meta_skills}\n\n')

        f.write('## [LIST] Category Breakdown\n\n')
        for category, data in report['documentation_status'].items():
            f.write(f'### {category.title()}\n')
            f.write(f'- Total: {data["total"]}\n')
            f.write(f'- With README: {data["with_readme"]}\n')
            f.write(f'- With Templates: {data["with_template"]}\n\n')

    print('[OK] Documentation report generated')
    print(f'[STATS] README coverage: {report["statistics"]["readme_coverage"]:.1f}%')
    print(f'[STATS] Template coverage: {report["statistics"]["template_coverage"]:.1f}%')

def main():
    validator = DocumentationValidator()

    # Scan skills directory
    skills_dir = Path('skills')
    if not skills_dir.exists():
        print('[ERROR] Skills directory not found')
        return False

    for category_dir in skills_dir.iterdir():
        if category_dir.is_dir() and category_dir.name != '__pycache__':
            category = category_dir.name
            print(f'[DIR] Scanning category: {category}')

            for skill_dir in category_dir.iterdir():
                if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                    validator.validate_skill(skill_dir, category, skill_dir.name)

    # Generate report and return status
    validation_passed = validator.generate_report()

    # Check consistency
    print('\n[SCAN] Checking documentation consistency...')
    consistency_passed = check_consistency()

    # Generate comprehensive report
    print('\n[LIST] Generating documentation report...')
    generate_doc_report()

    return validation_passed and consistency_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
