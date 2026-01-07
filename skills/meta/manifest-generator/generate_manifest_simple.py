#!/usr/bin/env python3
"""
Claude Code Skills Manifest Generator (Simple Version)
Scans skill directories and generates unified manifest without external dependencies
"""

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

SKILLS_ROOT = Path.home() / ".claude" / "skills"
MANIFEST_PATH = SKILLS_ROOT / "UNIFIED_SKILL_MANIFEST.md"

def parse_skill_frontmatter(skill_path):
    """Extract name and description from SKILL.md frontmatter"""
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            return None, None
            
        frontmatter = frontmatter_match.group(1)
        
        # Parse simple key: value pairs
        metadata = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"\'')
        
        return metadata.get('name'), metadata.get('description')
    except Exception as e:
        print(f"Error parsing {skill_path}: {e}")
        return None, None

def categorize_skill(skill_path):
    """Determine category from directory structure"""
    relative_path = skill_path.relative_to(SKILLS_ROOT)
    parts = relative_path.parts
    
    if len(parts) >= 3:
        # analysis/code, analysis/formal, etc.
        return f"{parts[0]}/{parts[1]}"
    elif len(parts) == 2:
        # development, git, meta
        return parts[0]
    else:
        return "root"

def extract_triggers(description):
    """Extract trigger phrases from description"""
    if not description:
        return []
    
    # Look for "Use when user says" patterns
    triggers = []
    patterns = [
        r'Use when user says [""](.*?)[""]',
        r'Use when user says ([^,.]+)',
        r'Use when (?:user says )?[""](.*?)[""]',
        r'Trigger: [""](.*?)[""]'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, description, re.IGNORECASE)
        triggers.extend(matches)
    
    return triggers

def estimate_tokens(skill_path):
    """Estimate token usage based on skill complexity"""
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple heuristic based on content length and complexity
        if len(content) < 1000:
            return "~300"
        elif len(content) < 2000:
            return "~500"
        elif len(content) < 3000:
            return "~800"
        else:
            return "~1000+"
    except:
        return "~500"

def scan_skills():
    """Scan for all skills in the directory structure"""
    skills = []
    
    # Find all SKILL.md files
    for skill_file in SKILLS_ROOT.rglob("SKILL.md"):
        # Skip manifest itself and generator
        if skill_file == MANIFEST_PATH:
            continue
        if "manifest-generator" in str(skill_file):
            continue
            
        name, description = parse_skill_frontmatter(skill_file)
        if not name or not description:
            continue
            
        category = categorize_skill(skill_file)
        triggers = extract_triggers(description)
        tokens = estimate_tokens(skill_file)
        
        skills.append({
            'name': name,
            'description': description,
            'category': category,
            'triggers': triggers,
            'tokens': tokens,
            'path': str(skill_file.relative_to(SKILLS_ROOT)).replace('\\', '/')
        })
    
    return skills

def generate_manifest(skills):
    """Generate the unified manifest content"""
    # Categorize skills
    categories = defaultdict(list)
    for skill in skills:
        categories[skill['category']].append(skill)
    
    # Build manifest content
    content = f"""---
name: unified-skill-manifest
description: Master catalog of all {len(skills)}+ Claude Code skills organized by category. Use when user asks "what skills are available", "show me all skills", or "list capabilities".
---

# 🎯 Claude Code Unified Skill Manifest

**{len(skills)}+ Skills Available** • Organized by Category • Last Updated: {datetime.now().strftime('%Y-%m-%d')}

## 🌟 Quick Reference - Most Used Skills

| Skill | Category | Trigger Phrases | Tokens |
|-------|----------|----------------|----------|"""
    
    # Add top skills to quick reference
    top_skills = ['session-snapshot', 'skill-extractor', 'diff-summariser', 
                  'repo-briefing', 'lean-plan']
    
    for skill_name in top_skills:
        skill = next((s for s in skills if s['name'] == skill_name), None)
        if skill:
            triggers = ', '.join(skill['triggers'][:2]) if skill['triggers'] else 'Various'
            content += f"""
| **{skill['name']}** | {skill['category']} | {triggers} | {skill['tokens']} |"""
    
    content += """

## 📋 Complete Skill Catalog

"""
    
    # Add skills by category
    category_names = {
        'development': '🚀 Development Skills',
        'git': '🎯 Git & Repository Skills', 
        'analysis/code': '🔍 Analysis: Code Quality',
        'analysis/formal': '📐 Analysis: Formal Verification',
        'meta': '⭐ Meta Skills',
        'root': '📁 Root Level Skills'
    }
    
    category_descriptions = {
        'development': 'Active coding and refactoring workflows',
        'git': 'Version control and repository operations',
        'analysis/code': 'Inspect codebases for quality, security, and maintainability',
        'analysis/formal': 'Formal verification and proof system analysis (Coq, Lean, etc.)',
        'meta': 'Skills that improve the skills system itself',
        'root': 'Skills in root directory (legacy/uncategorized)'
    }
    
    for category_key in ['development', 'git', 'analysis/code', 'analysis/formal', 'meta', 'root']:
        if category_key in categories:
            category_skills = categories[category_key]
            content += f"""
### {category_names.get(category_key, category_key)} ({len(category_skills)})
*{category_descriptions.get(category_key, 'Various workflows')}*

"""
            for skill in sorted(category_skills, key=lambda x: x['name']):
                triggers_str = ', '.join(f'"{t}"' for t in skill['triggers'][:3]) if skill['triggers'] else 'Various triggers'
                content += f"""- **{skill['name']}** - {skill['description'].split('.')[0]}.  
  *Use when*: {triggers_str}  
  *Location*: `{skill['path']}`

"""
    
    content += f"""
## 🚀 Usage Patterns

### Common Workflows
1. **Before Major Work**: `/session-snapshot` → do work → `/session-snapshot`
2. **Code Review**: `/diff-summariser` → `/repo-briefing` 
3. **Analysis**: Choose category → pick specific skill
4. **Skill Creation**: Use workflow → `/skill-extractor` → test new skill

### Auto-Detection Triggers
- Mentioning "skills", "capabilities", "what can you do" → Show this manifest
- Task-related keywords → Suggest relevant skills
- Session patterns → Propose `/session-snapshot`

## 📊 Skill Statistics

- **Total Skills**: {len(skills)}+ active skills
- **Categories**: {len(categories)} (Development, Git, Analysis/Code, Analysis/Formal, Meta, Root)
- **Token Range**: 300-1000+ tokens per invocation
- **Coverage**: Code quality, development workflows, git operations, formal verification, system improvement

## 🔧 Skill Development

### Creating New Skills
1. Use `/skill-extractor` to formalize workflows
2. Manual creation: Choose category → create directory → add SKILL.md
3. Test thoroughly before adding to manifest

### Maintenance
- Run this generator after adding new skills
- Categories expand as new skill types emerge
- Deprecated skills are moved to archive section

---

**💡 Pro Tip**: Start with `/session-snapshot` before long tasks, use `/skill-extractor` to capture useful workflows, and check this manifest when exploring capabilities!

*Generated by manifest-generator skill on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return content

def main():
    """Main execution"""
    print("Scanning skills directory...")
    skills = scan_skills()
    print(f"Found {len(skills)} skills")
    
    print("Generating manifest...")
    manifest_content = generate_manifest(skills)
    
    print(f"Writing manifest to {MANIFEST_PATH}...")
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    
    print(f"Manifest updated with {len(skills)} skills!")
    print(f"Location: {MANIFEST_PATH}")
    
    # Show summary
    categories = defaultdict(int)
    for skill in skills:
        categories[skill['category']] += 1
    
    print("\nSkills by category:")
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count}")

if __name__ == "__main__":
    main()