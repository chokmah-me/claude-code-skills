import re
from pathlib import Path
from datetime import datetime

class ReadmeUpdater:
    def __init__(self):
        self.skills_inventory = {}
        self.stats = {
            'total_skills': 0,
            'categories': 0,
            'skills_with_readme': 0
        }

    def scan_skills(self):
        '''Scan for skills in the repository'''
        skill_locations = [
            ('skills', 'skills'),
            ('.claude/skills', '.claude/skills')
        ]

        for base_path, display_name in skill_locations:
            skills_dir = Path(base_path)
            if skills_dir.exists():
                print(f'[*] Scanning {display_name} directory...')

                for category_dir in skills_dir.iterdir():
                    if category_dir.is_dir() and not category_dir.name.startswith('.'):
                        category = category_dir.name
                        if category not in self.skills_inventory:
                            self.skills_inventory[category] = []

                        print(f'  [+] Found category: {category}')

                        for skill_dir in category_dir.iterdir():
                            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                                skill_name = skill_dir.name
                                skill_info = self.analyze_skill(skill_dir, category, skill_name)
                                self.skills_inventory[category].append(skill_info)
                                self.stats['total_skills'] += 1

                                if skill_info['has_readme']:
                                    self.stats['skills_with_readme'] += 1

        self.stats['categories'] = len(self.skills_inventory)
        total = self.stats['total_skills']
        cats = self.stats['categories']
        print(f'[=] Found {total} skills across {cats} categories')

    def analyze_skill(self, skill_path, category, skill_name):
        '''Analyze a single skill'''
        skill_file = skill_path / 'SKILL.md'
        readme_file = skill_path / 'README.md'

        info = {
            'name': skill_name,
            'category': category,
            'has_readme': readme_file.exists(),
            'has_skill_md': skill_file.exists(),
            'description': '',
            'purpose': ''
        }

        # Extract description from SKILL.md
        if skill_file.exists():
            try:
                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Look for purpose or description
                purpose_match = re.search(r'Purpose:(.*?)(?:\n|$)', content, re.IGNORECASE)
                if purpose_match:
                    info['purpose'] = purpose_match.group(1).strip()

                # Look for first sentence as description
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('---'):
                        info['description'] = line[:100] + '...' if len(line) > 100 else line
                        break

            except Exception as e:
                print(f'[!] Error reading {skill_file}: {e}')

        return info

    def generate_skills_section(self):
        '''Generate the skills inventory section for README'''
        lines = []
        lines.append('## 🛠️ Available Skills\n')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M UTC')
        lines.append(f'*Last updated: {timestamp}*\n')

        # Add statistics
        lines.append('### 📊 Skills Statistics\n')
        total_skills = self.stats['total_skills']
        categories = self.stats['categories']
        with_readme = self.stats['skills_with_readme']
        lines.append(f'- **Total Skills**: {total_skills}')
        lines.append(f'- **Categories**: {categories}')
        lines.append(f'- **Skills with README**: {with_readme}')
        lines.append('')

        # Add skills by category
        for category, skills in sorted(self.skills_inventory.items()):
            if not skills:
                continue

            lines.append(f'### {category.title()}\n')

            for skill in sorted(skills, key=lambda x: x['name']):
                skill_name = skill['name']
                skill_line = f'- **{skill_name.replace("-", " ").title()}**'

                if skill['has_readme']:
                    # Link to README if it exists
                    skill_path = f'skills/{category}/{skill_name}'
                    if Path(f'.claude/skills/{category}/{skill_name}').exists():
                        skill_path = f'.claude/skills/{category}/{skill_name}'

                    skill_line += f' [`README`]({skill_path}/README.md)'

                skill_purpose = skill['purpose']
                skill_desc = skill['description']
                if skill_purpose:
                    skill_line += f' - {skill_purpose}'
                elif skill_desc:
                    skill_line += f' - {skill_desc}'

                lines.append(skill_line)

            lines.append('')

        return '\n'.join(lines)

    def update_readme(self):
        '''Update the README.md file with skills inventory'''
        readme_path = Path('README.md')

        if not readme_path.exists():
            print('[X] README.md not found')
            return False

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the skills inventory section
            start_marker = '<!-- SKILLS_INVENTORY_START -->'
            end_marker = '<!-- SKILLS_INVENTORY_END -->'

            if start_marker in content and end_marker in content:
                start_idx = content.find(start_marker) + len(start_marker)
                end_idx = content.find(end_marker)

                skills_section = self.generate_skills_section()
                new_content = content[:start_idx] + '\n' + skills_section + '\n' + content[end_idx:]

                if new_content != content:
                    with open(readme_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print('[OK] README.md updated successfully')
                    return True
                else:
                    print('[i] No changes needed in README.md')
                    return True
            else:
                print('[!] Skills section markers not found in README.md')
                print('  Add <!-- SKILLS_INVENTORY_START --> and <!-- SKILLS_INVENTORY_END --> to your README')
                return False

        except Exception as e:
            print(f'[X] Error updating README.md: {e}')
            return False

def main():
    '''Main function'''
    updater = ReadmeUpdater()

    # Scan for skills
    updater.scan_skills()

    # Update README
    if updater.update_readme():
        print('\\n[OK] Skills inventory updated in README.md')
        total_skills = updater.stats['total_skills']
        categories = updater.stats['categories']
        print(f'[=] Total skills: {total_skills}')
        print(f'[=] Categories: {categories}')
        return True
    else:
        print('\\n[X] Failed to update README.md')
        return False

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
