#!/usr/bin/env python3
"""
Claude Code Skills Installation Script

Intelligent installer for the Claude Code skills ecosystem.
Supports category-based installation, individual skill selection,
and automated dependency management.
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set


class SkillInstaller:
    """Main installer class for Claude Code skills."""
    
    def __init__(self, target_dir: Optional[str] = None):
        self.target_dir = target_dir or self._get_default_skills_dir()
        self.skills_manifest = self._load_skills_manifest()
        
    def _get_default_skills_dir(self) -> str:
        """Get the default Claude Code skills directory."""
        home = Path.home()
        
        # Common Claude Code skills locations
        possible_paths = [
            home / ".claude" / "skills",
            home / "claude" / "skills", 
            home / ".config" / "claude" / "skills",
            home / "AppData" / "Roaming" / "Claude" / "skills",  # Windows
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
                
        # Default to ~/.claude/skills if none exist
        default_path = home / ".claude" / "skills"
        default_path.mkdir(parents=True, exist_ok=True)
        return str(default_path)
    
    def _load_skills_manifest(self) -> Dict:
        """Load the skills manifest with categories and metadata."""
        return {
            "meta": {
                "description": "Meta-skills for workflow management and automation",
                "skills": {
                    "session-snapshot": {
                        "file": "skills/meta/session-snapshot/SKILL.md",
                        "description": "Complete session context management",
                        "priority": "high",
                        "dependencies": []
                    },
                    "skill-extractor": {
                        "file": "skills/meta/skill-extractor/SKILL.md", 
                        "description": "Automated skill discovery and documentation",
                        "priority": "high",
                        "dependencies": []
                    },
                    "skill-recommendation-engine": {
                        "file": "skills/meta/skill-recommendation-engine/SKILL.md",
                        "description": "Context-aware skill recommendations",
                        "priority": "medium",
                        "dependencies": ["skill-extractor"]
                    },
                    "claude-startup-integration": {
                        "file": "skills/meta/claude-startup-integration/SKILL.md",
                        "description": "Startup configuration and optimization",
                        "priority": "medium", 
                        "dependencies": []
                    },
                    "startup-skill-showcase": {
                        "file": "skills/meta/startup-skill-showcase/SKILL.md",
                        "description": "Interactive skill demonstration and showcase",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "manifest-generator": {
                        "file": "skills/meta/manifest-generator/SKILL.md",
                        "description": "Generate and manage skill manifests",
                        "priority": "low",
                        "dependencies": []
                    }
                }
            },
            "development": {
                "description": "Core development and coding skills",
                "skills": {
                    "lean-plan": {
                        "file": "skills/development/lean-plan/SKILL.md",
                        "description": "Token-efficient planning mode for complex tasks",
                        "priority": "high",
                        "dependencies": []
                    },
                    "quick-test-runner": {
                        "file": "skills/development/quick-test-runner/SKILL.md",
                        "description": "Fast test execution and validation workflows",
                        "priority": "high",
                        "dependencies": []
                    },
                    "refactoring": {
                        "file": "skills/development/refactoring/SKILL.md",
                        "description": "Code restructuring and modernization workflows",
                        "priority": "medium",
                        "dependencies": []
                    }
                }
            },
            "git": {
                "description": "Git and version control utilities",
                "skills": {
                    "diff-summariser": {
                        "file": "skills/git/diff-summariser/SKILL.md",
                        "description": "Summarize git diffs for code review",
                        "priority": "high",
                        "dependencies": []
                    },
                    "migrate-repo": {
                        "file": "skills/git/migrate-repo/SKILL.md",
                        "description": "Transfer repositories between accounts/orgs",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "repo-briefing": {
                        "file": "skills/git/repo-briefing/SKILL.md",
                        "description": "Generate compact repository summaries",
                        "priority": "medium",
                        "dependencies": []
                    }
                }
            },
            "analysis": {
                "description": "Code analysis and debugging tools",
                "skills": {
                    "api-contract-sniffer": {
                        "file": "skills/analysis/code/api-contract-sniffer/SKILL.md",
                        "description": "Detect API contract violations and inconsistencies",
                        "priority": "high",
                        "dependencies": []
                    },
                    "dead-code-hunter": {
                        "file": "skills/analysis/code/dead-code-hunter/SKILL.md",
                        "description": "Find unused functions, imports, and dead code",
                        "priority": "high",
                        "dependencies": []
                    },
                    "dependency-audit": {
                        "file": "skills/analysis/code/dependency-audit/SKILL.md",
                        "description": "Check for outdated and vulnerable dependencies",
                        "priority": "high",
                        "dependencies": []
                    },
                    "anti-pattern-sniffer": {
                        "file": "skills/analysis/formal/anti-pattern-sniffer/SKILL.md",
                        "description": "Detect proof anti-patterns in formal verification",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "lemma-dependency-graph": {
                        "file": "skills/analysis/formal/lemma-dependency-graph/SKILL.md",
                        "description": "Visualize proof dependencies and relationships",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "proof-obligations-snapshot": {
                        "file": "skills/analysis/formal/proof-obligations-snapshot/SKILL.md",
                        "description": "Track unproven obligations in formal systems",
                        "priority": "medium",
                        "dependencies": []
                    },
                    "tactic-usage-count": {
                        "file": "skills/analysis/formal/tactic-usage-count/SKILL.md",
                        "description": "Analyze proof tactics usage patterns",
                        "priority": "low",
                        "dependencies": []
                    },
                    "quantum-circuit-optimizer": {
                        "file": "skills/analysis/quantum/quantum-circuit-optimizer/SKILL.md",
                        "description": "Optimize quantum circuits by reducing gate count and depth",
                        "priority": "medium",
                        "dependencies": []
                    }
                }
            }
        }
    
    def get_skills_by_category(self, category: str) -> Dict[str, Dict]:
        """Get all skills in a specific category."""
        if category not in self.skills_manifest:
            raise ValueError(f"Unknown category: {category}")
        return self.skills_manifest[category]["skills"]
    
    def get_skill_info(self, skill_name: str) -> Optional[Dict]:
        """Get information about a specific skill."""
        for category_data in self.skills_manifest.values():
            if skill_name in category_data["skills"]:
                skill_info = category_data["skills"][skill_name].copy()
                skill_info["category"] = next(
                    cat for cat, data in self.skills_manifest.items()
                    if skill_name in data["skills"]
                )
                return skill_info
        return None
    
    def list_all_skills(self) -> Dict[str, List[str]]:
        """List all available skills organized by category."""
        return {
            category: list(data["skills"].keys())
            for category, data in self.skills_manifest.items()
        }
    
    def install_skill(self, skill_name: str, dry_run: bool = False) -> bool:
        """Install a single skill."""
        skill_info = self.get_skill_info(skill_name)
        if not skill_info:
            print(f"❌ Skill '{skill_name}' not found")
            return False
        
        source_file = Path(skill_info["file"])
        if not source_file.exists():
            print(f"❌ Skill file not found: {source_file}")
            return False
        
        target_file = Path(self.target_dir) / f"{skill_name}.md"
        
        if dry_run:
            print(f"📋 Would install: {skill_name}")
            print(f"   Source: {source_file}")
            print(f"   Target: {target_file}")
            return True
        
        try:
            # Install dependencies first
            for dep in skill_info.get("dependencies", []):
                print(f"📦 Installing dependency: {dep}")
                if not self.install_skill(dep, dry_run):
                    return False
            
            # Copy skill file
            shutil.copy2(source_file, target_file)
            print(f"✅ Installed: {skill_name} ({skill_info['description']})")
            return True
        except Exception as e:
            print(f"❌ Failed to install {skill_name}: {e}")
            return False
    
    def install_category(self, category: str, dry_run: bool = False) -> bool:
        """Install all skills in a category."""
        if category not in self.skills_manifest:
            print(f"❌ Unknown category: {category}")
            return False
        
        print(f"📂 Installing '{category}' category...")
        skills = self.get_skills_by_category(category)
        
        success_count = 0
        for skill_name in skills:
            if self.install_skill(skill_name, dry_run):
                success_count += 1
        
        print(f"✅ Installed {success_count}/{len(skills)} skills from '{category}' category")
        return success_count == len(skills)
    
    def install_all(self, dry_run: bool = False) -> bool:
        """Install all available skills."""
        print("📦 Installing all skills...")
        
        success_count = 0
        total_skills = sum(len(data["skills"]) for data in self.skills_manifest.values())
        
        for category in self.skills_manifest:
            category_skills = self.get_skills_by_category(category)
            category_success = 0
            
            for skill_name in category_skills:
                if self.install_skill(skill_name, dry_run):
                    category_success += 1
                    success_count += 1
            
            print(f"✅ Category '{category}': {category_success}/{len(category_skills)} skills")
        
        print(f"🎉 Total: {success_count}/{total_skills} skills installed successfully")
        return success_count == total_skills
    
    def uninstall_skill(self, skill_name: str) -> bool:
        """Uninstall a single skill."""
        target_file = Path(self.target_dir) / f"{skill_name}.md"
        
        if not target_file.exists():
            print(f"❌ Skill '{skill_name}' not installed")
            return False
        
        try:
            target_file.unlink()
            print(f"✅ Uninstalled: {skill_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to uninstall {skill_name}: {e}")
            return False
    
    def list_installed_skills(self) -> List[str]:
        """List all installed skills."""
        skills_dir = Path(self.target_dir)
        if not skills_dir.exists():
            return []
        
        return [f.stem for f in skills_dir.glob("*.md")]
    
    def verify_installation(self) -> Dict[str, bool]:
        """Verify installation status of all skills."""
        installed = set(self.list_installed_skills())
        all_skills = set()
        
        for category_data in self.skills_manifest.values():
            all_skills.update(category_data["skills"].keys())
        
        return {
            skill: skill in installed
            for skill in all_skills
        }


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Install Claude Code skills with intelligent dependency management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all                           # Install all skills
  %(prog)s --category meta                 # Install meta skills only
  %(prog)s --skills session-snapshot       # Install specific skills
  %(prog)s --list                          # List available skills
  %(prog)s --verify                        # Verify installation
  %(prog)s --uninstall old-skill           # Uninstall a skill
        """
    )
    
    # Installation options
    install_group = parser.add_mutually_exclusive_group()
    install_group.add_argument("--all", action="store_true",
                              help="Install all available skills")
    install_group.add_argument("--category", type=str,
                              help="Install all skills in a category")
    install_group.add_argument("--skills", nargs="+", type=str,
                              help="Install specific skills by name")
    
    # Other operations
    parser.add_argument("--list", action="store_true",
                       help="List all available skills")
    parser.add_argument("--verify", action="store_true",
                       help="Verify installation status")
    parser.add_argument("--installed", action="store_true",
                       help="List installed skills")
    parser.add_argument("--uninstall", type=str,
                       help="Uninstall a specific skill")
    
    # Options
    parser.add_argument("--target-dir", type=str,
                       help="Target directory for skill installation")
    parser.add_argument("--dry-run", action="store_true",
                       help="Preview installation without making changes")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Initialize installer
    installer = SkillInstaller(args.target_dir)
    
    # Handle different operations
    if args.list:
        print("📋 Available Skills by Category:")
        all_skills = installer.list_all_skills()
        for category, skills in all_skills.items():
            print(f"\n🔹 {category.upper()} ({len(skills)} skills):")
            for skill in skills:
                info = installer.get_skill_info(skill)
                print(f"   • {skill} - {info['description']}")
    
    elif args.installed:
        installed = installer.list_installed_skills()
        print(f"✅ Installed Skills ({len(installed)}):")
        for skill in sorted(installed):
            print(f"   • {skill}")
    
    elif args.verify:
        status = installer.verify_installation()
        print("🔍 Installation Status:")
        for skill, installed in sorted(status.items()):
            status_icon = "✅" if installed else "❌"
            print(f"   {status_icon} {skill}")
        
        total = len(status)
        installed = sum(status.values())
        print(f"\n📊 Summary: {installed}/{total} skills installed")
    
    elif args.uninstall:
        installer.uninstall_skill(args.uninstall)
    
    elif args.all:
        success = installer.install_all(args.dry_run)
        sys.exit(0 if success else 1)
    
    elif args.category:
        success = installer.install_category(args.category, args.dry_run)
        sys.exit(0 if success else 1)
    
    elif args.skills:
        success_count = 0
        for skill_name in args.skills:
            if installer.install_skill(skill_name, args.dry_run):
                success_count += 1
        print(f"🎉 Installed {success_count}/{len(args.skills)} requested skills")
        sys.exit(0 if success_count == len(args.skills) else 1)
    
    else:
        parser.print_help()
        print("\n💡 Use --list to see available skills")


if __name__ == "__main__":
    main()