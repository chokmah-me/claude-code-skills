import re
from pathlib import Path
from datetime import datetime, timezone

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
        skills_dir = Path('skills')

        if not skills_dir.exists():
            print('[X] skills directory not found')
            return

        print('[*] Scanning skills directory...')

        for category_dir in skills_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('.'):
                continue

            category = category_dir.name
            print(f'  [+] Found category: {category}')

            # Check if this is a nested category (like analysis/code, analysis/formal)
            has_subcategories = any(
                item.is_dir() and not item.name.startswith('.') and not (item / 'SKILL.md').exists()
                for item in category_dir.iterdir()
            )

            if has_subcategories:
                # Handle nested structure (analysis/code/*, analysis/formal/*)
                for subcategory_dir in category_dir.iterdir():
                    if not subcategory_dir.is_dir() or subcategory_dir.name.startswith('.'):
                        continue

                    subcategory = f"{category}/{subcategory_dir.name}"

                    # Check if this subcategory has skills or is itself a skill
                    if (subcategory_dir / 'SKILL.md').exists():
                        # This is actually a skill, not a subcategory
                        if category not in self.skills_inventory:
                            self.skills_inventory[category] = []
                        skill_info = self.analyze_skill(subcategory_dir, category, subcategory_dir.name)
                        self.skills_inventory[category].append(skill_info)
                        self.stats['total_skills'] += 1
                        if skill_info['has_readme']:
                            self.stats['skills_with_readme'] += 1
                    else:
                        # This is a subcategory with skills inside
                        if subcategory not in self.skills_inventory:
                            self.skills_inventory[subcategory] = []

                        print(f'    [+] Found subcategory: {subcategory}')

                        for skill_dir in subcategory_dir.iterdir():
                            if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                                skill_name = skill_dir.name
                                skill_info = self.analyze_skill(skill_dir, subcategory, skill_name)
                                self.skills_inventory[subcategory].append(skill_info)
                                self.stats['total_skills'] += 1

                                if skill_info['has_readme']:
                                    self.stats['skills_with_readme'] += 1
            else:
                # Handle flat structure (git/*, meta/*, development/*)
                if category not in self.skills_inventory:
                    self.skills_inventory[category] = []

                for skill_dir in category_dir.iterdir():
                    if skill_dir.is_dir() and not skill_dir.name.startswith('.'):
                        skill_name = skill_dir.name
                        skill_info = self.analyze_skill(skill_dir, category, skill_name)
                        self.skills_inventory[category].append(skill_info)
                        self.stats['total_skills'] += 1

                        if skill_info['has_readme']:
                            self.stats['skills_with_readme'] += 1

        self.stats['categories'] = len(self.skills_inventory)
        print(f'[=] Found {self.stats["total_skills"]} skills across {self.stats["categories"]} categories')

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

                # Try to extract frontmatter first (YAML between ---)
                frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
                if frontmatter_match:
                    frontmatter = frontmatter_match.group(1)
                    desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', frontmatter)
                    if desc_match:
                        info['description'] = desc_match.group(1).strip()

                # Look for purpose section
                purpose_match = re.search(r'##?\s*(?:🎯\s*)?Purpose:?\s*\n\s*(.+?)(?:\n\n|\n##|$)', content, re.IGNORECASE | re.DOTALL)
                if purpose_match:
                    info['purpose'] = purpose_match.group(1).strip().split('\n')[0]

                # If no description yet, look for first meaningful line
                if not info['description']:
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('---') and len(line) > 10:
                            info['description'] = line[:100] + '...' if len(line) > 100 else line
                            break

            except Exception as e:
                print(f'[!] Error reading {skill_file}: {e}')

        return info

    def generate_inventory_markdown(self):
        '''Generate markdown for skills inventory'''
        markdown = f'\n## 📋 Skills Inventory\n\n'
        markdown += f'*Last updated: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}*\n\n'
        markdown += f'**Total Skills:** {self.stats["total_skills"]}  \n'
        markdown += f'**Categories:** {self.stats["categories"]}  \n'
        markdown += f'**Skills with README:** {self.stats["skills_with_readme"]}  \n\n'

        if not self.skills_inventory:
            markdown += 'No skills found in repository.\n'
            return markdown

        # Sort categories alphabetically
        for category in sorted(self.skills_inventory.keys()):
            skills = self.skills_inventory[category]
            if skills:
                markdown += f'### {category.replace("/", " / ").title()} ({len(skills)} skills)\n\n'

                # Sort skills alphabetically
                for skill in sorted(skills, key=lambda x: x['name']):
                    skill_path = f'{category}/{skill["name"]}'
                    readme_link = f'[README](skills/{skill_path}/README.md)' if skill['has_readme'] else 'No README'

                    markdown += f'#### {skill["name"].replace("-", " ").title()}\n'
                    if skill['description']:
                        markdown += f'{skill["description"]}\n\n'
                    if skill['purpose']:
                        markdown += f'**Purpose:** {skill["purpose"]}\n\n'
                    markdown += f'**Location:** `skills/{skill_path}/`  \n'
                    markdown += f'**Documentation:** {readme_link}  \n\n'

        return markdown

    def update_readme_timestamp(self):
        '''Update the Last updated timestamp in README.md'''
        readme_path = Path('README.md')

        if not readme_path.exists():
            print('[X] README.md not found')
            return False

        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update timestamp at the bottom of README
            current_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            updated_content = re.sub(
                r'\*\*Last updated\*\*:\s*\d{4}-\d{2}-\d{2}[^\n]*',
                f'**Last updated**: {current_date} (Auto-updated by workflow)',
                content
            )

            if updated_content != content:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                print(f'[OK] Updated README.md timestamp to {current_date}')
                return True
            else:
                print('[i] README.md timestamp already current')
                return False

        except Exception as e:
            print(f'[X] Error updating README.md: {e}')
            return False

    def update_skills_inventory(self):
        '''Update SKILLS_INVENTORY.md with skills inventory'''
        inventory_path = Path('SKILLS_INVENTORY.md')

        try:
            # Generate new inventory
            self.scan_skills()
            inventory_markdown = self.generate_inventory_markdown()

            # Add markers for consistency
            content = (
                '<!-- SKILLS_INVENTORY_START -->\n' +
                inventory_markdown.strip() + '\n' +
                '<!-- SKILLS_INVENTORY_END -->\n'
            )

            # Write inventory file
            with open(inventory_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print('[OK] SKILLS_INVENTORY.md updated successfully')

            # Also update README.md timestamp
            self.update_readme_timestamp()

            return True

        except Exception as e:
            print(f'[X] Error updating SKILLS_INVENTORY.md: {e}')
            return False

# Run the updater
updater = ReadmeUpdater()
success = updater.update_skills_inventory()
exit(0 if success else 1)
