#!/usr/bin/env python3
"""
Dependency analyzer for Claude Code skills repository.
Analyzes skill references and builds dependency graphs.
"""

from pathlib import Path
from typing import Any, Dict, List, Set

from common_utils import (
    find_all_skills,
    log_error,
    log_info,
    log_success,
    log_warning,
    save_json,
    exit_failure,
    exit_success,
)


class DependencyGraph:
    """Simple dependency graph for skills."""

    def __init__(self):
        self.nodes: Dict[str, Set[str]] = {}

    def add_edge(self, from_skill: str, to_skill: str) -> None:
        """Add dependency edge: from_skill depends on to_skill."""
        if from_skill not in self.nodes:
            self.nodes[from_skill] = set()
        self.nodes[from_skill].add(to_skill)

    def add_node(self, skill: str) -> None:
        """Add node if not exists."""
        if skill not in self.nodes:
            self.nodes[skill] = set()

    def find_cycles(self) -> List[List[str]]:
        """Find circular dependencies."""
        cycles = []
        visited = set()

        def dfs(node: str, path: List[str], rec_stack: Set[str]) -> None:
            visited.add(node)
            path.append(node)
            rec_stack.add(node)

            for neighbor in self.nodes.get(node, set()):
                if neighbor not in visited:
                    dfs(neighbor, path.copy(), rec_stack.copy())
                elif neighbor in rec_stack:
                    cycle = path[path.index(neighbor) :]
                    if cycle not in cycles:
                        cycles.append(cycle)

            rec_stack.remove(node)

        for node in self.nodes:
            if node not in visited:
                dfs(node, [], set())

        return cycles

    def to_dict(self) -> Dict[str, List[str]]:
        """Convert to dictionary format."""
        return {k: list(v) for k, v in self.nodes.items()}


def extract_skill_references(skill_md: Path) -> List[str]:
    """
    Extract references to other skills from documentation.

    Args:
        skill_md: Path to SKILL.md file

    Returns:
        List of referenced skill names
    """
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        log_error(f"Could not read {skill_md}: {e}")
        return []

    references = []
    skills_dir = skill_md.parent.parent.parent / "skills"

    # Look for references in the form: [skill-name](...)
    import re

    # Find all skill references (look for skill directory names in markdown links)
    for line in content.split("\n"):
        # Match [text](../path/to/skill)
        matches = re.findall(r"\[.*?\]\((.*?)\)", line)
        for match in matches:
            # Check if this looks like a skill reference
            if "skill" in match or ".." in match:
                # Extract skill name
                parts = match.split("/")
                for part in parts:
                    if part and not part.startswith("."):
                        skill_name = part.replace(".md", "")
                        if skill_name not in references:
                            references.append(skill_name)

    return references


def build_dependency_graph(skills: List[Path]) -> Dict[str, Any]:
    """
    Build complete dependency graph from all skills.

    Args:
        skills: List of SKILL.md paths

    Returns:
        Graph data with statistics
    """
    graph = DependencyGraph()
    skill_names = [s.parent.name for s in skills]

    log_info("Analyzing skill dependencies...")

    # Add all skills as nodes
    for skill_name in skill_names:
        graph.add_node(skill_name)

    # Extract references and build edges
    for skill_md in skills:
        skill_name = skill_md.parent.name
        references = extract_skill_references(skill_md)

        for ref in references:
            if ref in skill_names:
                graph.add_edge(skill_name, ref)
                log_info(f"  {skill_name} -> {ref}")

    return {
        "total_skills": len(skill_names),
        "graph": graph.to_dict(),
        "cycles": graph.find_cycles(),
    }


def detect_circular_deps(graph_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect and report circular dependencies.

    Args:
        graph_data: Dependency graph data

    Returns:
        List of cycle reports
    """
    cycles = graph_data.get("cycles", [])
    reports = []

    for cycle in cycles:
        report = {
            "cycle": cycle,
            "length": len(cycle),
            "severity": "high" if len(cycle) > 2 else "medium",
        }
        reports.append(report)
        log_error(f"Circular dependency detected: {' -> '.join(cycle)}")

    return reports


def suggest_bundles(graph_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Suggest skill bundles based on dependencies.

    Args:
        graph_data: Dependency graph data

    Returns:
        List of suggested bundles
    """
    graph_dict = graph_data.get("graph", {})
    bundles = []

    # Find skills with no dependencies (standalone)
    standalone = []
    for skill, deps in graph_dict.items():
        if not deps:
            standalone.append(skill)

    if standalone:
        bundles.append({
            "name": "Standalone Skills",
            "description": "Skills with no dependencies",
            "skills": sorted(standalone),
        })

    # Find highly connected skill groups (could be bundled)
    high_dependency = []
    for skill, deps in graph_dict.items():
        if len(deps) > 2:
            high_dependency.append({"skill": skill, "deps": len(deps)})

    if high_dependency:
        top_deps = sorted(high_dependency, key=lambda x: x["deps"], reverse=True)[:3]
        bundles.append({
            "name": "Core Skills",
            "description": "Skills with most dependencies",
            "skills": [s["skill"] for s in top_deps],
        })

    return bundles


def export_graph(graph_data: Dict[str, Any], output_path: Path) -> bool:
    """
    Export dependency graph as JSON.

    Args:
        graph_data: Graph data
        output_path: Output file path

    Returns:
        True if successful
    """
    try:
        save_json(graph_data, output_path)
        return True
    except Exception as e:
        log_error(f"Failed to export graph: {e}")
        return False


def main() -> None:
    """Analyze dependencies."""
    skills = find_all_skills()

    if not skills:
        exit_failure("No skills found to analyze")

    log_info(f"Analyzing {len(skills)} skills...")

    # Build graph
    graph_data = build_dependency_graph(skills)

    # Detect cycles
    cycles = detect_circular_deps(graph_data)
    graph_data["circular_dependencies"] = cycles

    # Suggest bundles
    bundles = suggest_bundles(graph_data)
    graph_data["suggested_bundles"] = bundles

    # Export
    output_path = Path("dependency-graph.json")
    if not export_graph(graph_data, output_path):
        exit_failure("Failed to export dependency graph")

    # Report summary
    summary = f"Analyzed {graph_data['total_skills']} skills"
    if cycles:
        summary += f", found {len(cycles)} circular dependencies"
    if bundles:
        summary += f", suggested {len(bundles)} bundles"

    exit_success(summary)


if __name__ == "__main__":
    main()
