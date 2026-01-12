# Dependency Audit Skill - Usage Guide

## Overview

The `dependency-audit` skill analyzes project dependencies to identify security vulnerabilities, outdated packages, licensing issues, and optimization opportunities. Keeps your codebase secure and maintainable.

**Token Efficiency**: ~500 tokens vs ~1.2K manual audit (60% reduction)

## Quick Start

### Natural Language Invocation
```
"Audit dependencies for security issues"
"Check if any packages need updating"
"Review license compatibility in our dependencies"
```

### Direct Skill Invocation
```
/dependency-audit
```

## What It Audits

✅ **Security Vulnerabilities**:
- Known CVEs in dependencies
- High-risk package versions
- Malicious package detection
- Supply chain security issues

✅ **Version Management**:
- Outdated packages
- Deprecated dependencies
- End-of-life versions
- Pre-release/beta usage

✅ **License Compliance**:
- License compatibility
- Copyleft obligations
- Commercial restrictions
- License changes in updates

✅ **Performance & Size**:
- Bundle size impact
- Duplicate dependencies
- Unused dependencies
- Heavy-weight packages

## Audit Process

### Phase 1: Dependency Discovery
Identifies all dependency sources:
- Package manager files (`package.json`, `requirements.txt`, etc.)
- Lock files (`package-lock.json`, `Pipfile.lock`, etc.)
- Container dependencies (`Dockerfile`, `docker-compose.yml`)
- CI/CD dependencies (`.github/workflows`, etc.)

### Phase 2: Security Scanning
Checks for known vulnerabilities:
- National Vulnerability Database (NVD)
- GitHub Security Advisories
- Package manager security feeds
- Community-maintained vulnerability databases

### Phase 3: Version Analysis
Evaluates dependency versions:
- Latest stable releases
- Security update availability
- Breaking change assessment
- Compatibility analysis

### Phase 4: License Review
Analyzes licensing implications:
- License compatibility matrix
- Commercial usage restrictions
- Attribution requirements
- Copyleft obligations

### Phase 5: Optimization Assessment
Identifies improvement opportunities:
- Bundle size optimization
- Alternative lightweight packages
- Native API replacements
- Tree-shaking potential

## Example Usage

### Example 1: Security-Focused Audit
```
User: "Check for security vulnerabilities in our dependencies"

Claude: 🔍 Auditing dependencies for security issues...

📊 Audit Summary:
- Dependencies analyzed: 127 packages
- Direct dependencies: 23
- Transitive dependencies: 104
- Scan time: 3.2 seconds

🚨 Critical Security Issues:
1. Package: lodash@4.17.15
   CVE: CVE-2021-23337
   Severity: HIGH
   Issue: Command injection vulnerability
   Fix: Update to lodash@>=4.17.21
   
2. Package: axios@0.21.1
   CVE: CVE-2021-3749
   Severity: HIGH
   Issue: Regular expression DoS
   Fix: Update to axios@>=0.21.2

⚠️ High Priority Updates:
1. Package: express@4.17.1
   Current: 4.17.1
   Latest: 4.18.2
   Breaking changes: None
   Security fixes: 3 medium-severity
   
2. Package: jsonwebtoken@8.5.1
   Current: 8.5.1
   Latest: 9.0.2
   Breaking changes: Minor (algorithm handling)
   Security fixes: 2 vulnerabilities

📈 Security Score: 6.5/10 (Improvement needed)
```

### Example 2: License Compliance Check
```
User: "Review license compatibility for commercial use"

Claude: 📋 Reviewing dependency licenses for commercial compatibility...

🔍 License Analysis:
- Total packages: 89
- License types found: 12
- Commercial restrictions: 3 packages
- Copyleft obligations: 2 packages

⚠️ License Issues:
1. Package: gpl-package@1.2.3
   License: GPL-3.0
   Issue: Strong copyleft - requires open-sourcing
   Recommendation: Replace with MIT-licensed alternative
   Alternative: mit-alternative@2.1.0 (API compatible)
   
2. Package: commercial-package@3.1.4
   License: Commercial
   Issue: Requires paid license for commercial use
   Action: Verify license purchase
   Documentation: https://vendor.com/licensing

✅ Compatible Licenses:
- MIT: 45 packages
- Apache-2.0: 23 packages
- BSD-3-Clause: 12 packages
- ISC: 9 packages

📊 Compliance Score: 7.2/10 (Mostly compliant)
```

### Example 3: Performance Optimization Audit
```
User: "Find opportunities to reduce bundle size"

Claude: 📦 Analyzing dependencies for bundle size optimization...

🎯 Size Optimization Opportunities:

Heavy Dependencies (Consider alternatives):
1. Package: moment@2.29.4
   Size: 232.7 KB (gzipped)
   Usage: Date formatting (3 functions only)
   Alternative: dayjs@1.11.9 (6.9 KB) - 97% smaller
   Migration effort: Low (similar API)
   
2. Package: lodash@4.17.21
   Size: 69.9 KB (gzipped)
   Usage: 8 utility functions
   Alternative: lodash-es + tree-shaking (12.3 KB)
   Savings: 82% size reduction

Duplicate Functionality:
1. Packages: axios, fetch-polyfill, node-fetch
   Issue: Multiple HTTP clients
   Solution: Standardize on native fetch
   Savings: 45.2 KB
   
2. Packages: underscore, lodash
   Issue: Overlapping utility libraries
   Solution: Choose one and migrate
   Savings: 28.1 KB

📈 Potential Savings:
- Bundle size reduction: 312 KB (28%)
- Load time improvement: ~180ms
- Mobile data savings: Significant
```

## Audit Types

### Security Audit
**Focus**: Vulnerabilities and security issues
```
/dependency-audit --type=security
```
**Reports**: CVEs, advisories, risk assessments

### Version Audit
**Focus**: Outdated packages and updates
```
/dependency-audit --type=versions
```
**Reports**: Update availability, breaking changes

### License Audit
**Focus**: Legal compliance and obligations
```
/dependency-audit --type=licenses
```
**Reports**: License compatibility, restrictions

### Performance Audit
**Focus**: Size and performance impact
```
/dependency-audit --type=performance
```
**Reports**: Bundle analysis, optimization suggestions

### Comprehensive Audit
**Focus**: All aspects combined
```
/dependency-audit --type=full
```
**Reports**: Complete dependency health assessment

## Risk Assessment

### 🔴 Critical Risk
- Known vulnerabilities with exploits
- Malicious packages
- License violations
- End-of-life dependencies

### 🟡 Medium Risk
- Outdated packages with security updates
- Incompatible licenses
- Performance bottlenecks
- Unmaintained packages

### 🟢 Low Risk
- Minor version updates available
- Non-critical security issues
- Suboptimal performance
- Missing documentation

## Integration with Development Workflow

**Regular Maintenance**:
```
Weekly: /dependency-audit --type=security
Monthly: /dependency-audit --type=full
Before releases: /dependency-audit --fail-on-high
```

**CI/CD Integration**:
```
# Add to pipeline
/dependency-audit --format=json --fail-on-critical
# Fails build if critical issues found
```

**Dependency Updates**:
```
1. /dependency-audit (current state)
2. Update dependencies
3. /dependency-audit (verify fixes)
4. Run test suite
5. Commit changes
```

## Configuration Management

**Package Manager Support**:
- npm/yarn: `package.json`, `package-lock.json`
- pip: `requirements.txt`, `Pipfile`, `pyproject.toml`
- Maven: `pom.xml`
- Gradle: `build.gradle`
- NuGet: `*.csproj`, `packages.config`

**Custom Rules**:
```json
{
  "ignorePackages": ["internal-package"],
  "severityOverrides": {
    "axios": "medium"
  },
  "licenseWhitelist": ["MIT", "Apache-2.0", "BSD"]
}
```

**Exclusions**:
- `--exclude-dev`: Skip development dependencies
- `--exclude-optional`: Skip optional dependencies
- `--ignore=CVE-2021-1234`: Ignore specific vulnerabilities

## Best Practices

1. **Regular Audits**: Schedule weekly security scans
2. **Update Promptly**: Apply security updates immediately
3. **License Awareness**: Understand license implications
4. **Minimize Dependencies**: Only use what you need
5. **Vendor Evaluation**: Research package maintainers

## Security Considerations

**Vulnerability Management**:
- Monitor security advisories
- Apply updates promptly
- Test security updates
- Document security decisions

**Supply Chain Security**:
- Use lock files
- Verify package integrity
- Avoid typosquatting packages
- Prefer well-maintained packages

## Troubleshooting

### Issue 1: "No dependencies found"
**Cause**: Unrecognized project structure
**Solution**: Specify package manager explicitly

### Issue 2: "Audit timed out"
**Cause**: Large dependency tree or slow network
**Solution**: Use `--timeout=60` or analyze smaller scope

### Issue 3: "False positive vulnerabilities"
**Cause**: Vulnerability in unused functionality
**Solution**: Review actual usage and suppress if appropriate

## Token Efficiency

- Security audit: ~300 tokens
- Version audit: ~400 tokens
- License audit: ~350 tokens
- Full comprehensive audit: ~500 tokens

## Related Skills

- `analysis/code/dead-code-hunter` - Find unused dependencies
- `analysis/code/api-contract-sniffer` - Check API security
- `git/diff-summariser` - Review dependency changes
- `development/refactoring` - Update dependencies safely

---

**Ready to audit?** Just tell Claude: "Audit my dependencies" or "Check for security vulnerabilities"!