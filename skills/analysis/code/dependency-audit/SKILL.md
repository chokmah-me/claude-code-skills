---
name: dependency-audit
description: List top-level runtime dependencies from package.json, requirements.txt, or other lock files. Use when user says "audit deps", "check dependencies", or "what packages do we use".
---

# Dependency Audit Skill

## Purpose
Get runtime dependency list without parsing full lockfiles (~600 tokens).

## Instructions

When user requests dependency audit:

1. **Run the command** to extract dependency names
2. **Present sorted list** (top 20)
3. **Offer follow-up**: "Want me to check for known CVEs or outdated versions?"

## Command

```bash
(cat package.json | jq -r '.dependencies // {} | keys[]' 2>/dev/null || cat requirements.txt | grep -v '^#' | cut -d'=' -f1 2>/dev/null || echo "no lock file") | sort | uniq | head -20
```

## Output Format

```
Top-level runtime dependencies:
[sorted list of package names, no versions]
```

## Multi-Language Support

- **Node.js**: Reads `package.json` dependencies
- **Python**: Reads `requirements.txt`
- **Fallback**: Reports "no lock file" if neither found

## Follow-Up Actions

After presenting list, Claude can:
- Web search for CVE vulnerabilities (short list = fast)
- Check npm/PyPI for latest versions
- Identify deprecated packages
- Suggest lighter alternatives

## Token Efficiency

- ~600 tokens for full audit
- Alternative: parsing package-lock.json (20k+ tokens)
- Enables targeted vulnerability research without lockfile parsing
