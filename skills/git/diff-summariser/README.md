# Diff Summariser Skill - Usage Guide

## Overview

The `diff-summariser` skill analyzes git diffs to provide concise, meaningful summaries of code changes. Perfect for code reviews, understanding historical changes, and tracking project evolution without reading through every line of diff.

**Token Efficiency**: ~400 tokens vs ~1.5K manual diff analysis (75% reduction)

## Quick Start

### Natural Language Invocation
```
"Summarize the changes in this commit"
"What did I change in the last few commits?"
"Review this pull request diff"
```

### Direct Skill Invocation
```
/diff-summariser
```

## What It Summarizes

✅ **Change Categories**:
- Added/removed functionality
- Modified business logic
- Refactoring activities
- Configuration changes
- Documentation updates

✅ **Impact Analysis**:
- Breaking changes identification
- Security implications
- Performance impacts
- Dependencies affected

✅ **Quality Indicators**:
- Code complexity changes
- Test coverage impact
- Potential issues
- Improvement opportunities

## Analysis Process

### Phase 1: Diff Parsing
Extracts change information:
- File-level modifications
- Function/method changes
- Import/dependency changes
- Configuration updates

### Phase 2: Semantic Analysis
Understands change meaning:
- Code structure analysis
- Logic flow changes
- API modifications
- Data structure changes

### Phase 3: Impact Assessment
Evaluates change significance:
- Risk level assessment
- Breaking change detection
- Performance implications
- Security considerations

### Phase 4: Summary Generation
Creates human-readable summary:
- Executive overview
- Detailed breakdown
- Action items
- Recommendations

## Example Usage

### Example 1: Single Commit Analysis
```
User: "Summarize the changes in commit abc123"

Claude: 📊 Analyzing diff for commit abc123...

📋 Commit Summary:
- Author: developer@company.com
- Date: 2026-01-07 14:30:00
- Files changed: 5
- Insertions: +127 lines
- Deletions: -43 lines

🎯 Primary Changes:

1. FEATURE: Enhanced user authentication system
   - Files: auth/login.py, auth/middleware.py
   - Added: Multi-factor authentication support
   - Modified: Login flow to support MFA challenges
   - Impact: Security enhancement, user-facing change

2. SECURITY: Implemented rate limiting for login attempts
   - Files: auth/rate_limiter.py, config/security.py
   - Added: Redis-based rate limiting with configurable thresholds
   - Modified: Login endpoint to enforce rate limits
   - Impact: Prevents brute force attacks

3. REFACTOR: Extracted authentication logic into service layer
   - Files: auth/services.py (new), auth/controller.py (modified)
   - Added: 67 lines of extracted business logic
   - Removed: 43 lines from controller
   - Impact: Better separation of concerns, improved testability

⚠️ Important Notes:
- New Redis dependency added (check infrastructure)
- Configuration changes required (see config/security.py)
- Database migration needed for MFA support

📊 Quality Metrics:
- Test coverage: +12% (new tests added)
- Cyclomatic complexity: -8% (logic simplified)
- Security score: +25% (rate limiting + MFA)

💡 Recommendations:
1. Review Redis configuration before deployment
2. Update deployment docs with new dependencies
3. Consider gradual MFA rollout to users
4. Monitor login performance with rate limiting
```

### Example 2: Pull Request Review
```
User: "Review this pull request for potential issues"

Claude: 📊 Analyzing pull request diff...

🔍 Pull Request Analysis:
- PR #247: "Implement payment processing"
- Files changed: 12
- Lines added: +456
- Lines removed: -89
- Complexity: High (payment system)

🚨 Critical Issues Identified:

1. SECURITY: Hardcoded API credentials
   Location: payment/processor.py:23
   Issue: Stripe secret key visible in code
   Severity: CRITICAL
   Recommendation: Use environment variables

2. PERFORMANCE: Missing database indexes
   Location: models/payment.py:45-67
   Issue: Foreign keys without indexes
   Severity: HIGH
   Recommendation: Add database migration for indexes

3. ERROR HANDLING: Insufficient exception handling
   Location: payment/service.py:89-134
   Issue: Generic exception catch blocks
   Severity: MEDIUM
   Recommendation: Specific exception handling

✅ Positive Aspects:

1. ARCHITECTURE: Well-structured service layer
   - Clean separation of concerns
   - Proper dependency injection
   - Good abstraction boundaries

2. TESTING: Comprehensive test coverage
   - Unit tests for all payment methods
   - Integration tests for payment flow
   - Mock external services appropriately

3. DOCUMENTATION: Clear API documentation
   - Payment endpoint documentation
   - Error response specifications
   - Usage examples provided

📊 Overall Assessment:
- Code quality: 7/10 (good structure, some issues)
- Security: 4/10 (critical credential issue)
- Performance: 6/10 (missing optimizations)
- Maintainability: 8/10 (good architecture)

🚦 Recommendation: REQUEST CHANGES
- Must fix: Hardcoded credentials
- Should fix: Database indexes
- Consider fixing: Exception handling

Next steps: Address security issues, then re-review.
```

### Example 3: Historical Change Tracking
```
User: "What changed in the authentication system over the last week?"

Claude: 📊 Analyzing week's authentication changes...

📅 Weekly Authentication Changes Summary:

📈 Change Overview:
- Period: Jan 1-7, 2026
- Authors: 3 developers
- Commits: 12
- Files modified: 18
- Total changes: +892/-234 lines

🔄 Evolution Timeline:

Day 1 (Jan 1):
- SECURITY: Fixed JWT token validation vulnerability
- Impact: Prevents token tampering attacks
- Files: auth/jwt.py (critical security fix)

Day 3 (Jan 3):
- FEATURE: Added OAuth2 Google integration
- Impact: Users can now sign in with Google
- Files: auth/oauth.py, config/oauth.py (new feature)

Day 4 (Jan 4):
- REFACTOR: Extracted authentication service
- Impact: Better code organization, testability
- Files: auth/service.py (new), auth/controller.py (modified)

Day 5 (Jan 5):
- PERFORMANCE: Implemented authentication caching
- Impact: 40% faster login times
- Files: auth/cache.py (new), auth/middleware.py (modified)

Day 7 (Jan 7):
- BUGFIX: Fixed session timeout handling
- Impact: Users no longer unexpectedly logged out
- Files: auth/session.py, middleware/session.py

📊 Cumulative Impact:
- Security: +3 fixes (token, session, validation)
- Features: +2 additions (OAuth, caching)
- Performance: +40% improvement (caching)
- Architecture: +1 major refactor (service extraction)

🔍 Trend Analysis:
- Security focus: High priority on fixes
- Feature development: Steady progress
- Performance optimization: Proactive improvements
- Code quality: Consistent refactoring

💡 Insights:
1. Strong security focus this week
2. Good balance of features and fixes
3. Proactive performance improvements
4. Consistent architectural improvements
```

## Diff Analysis Categories

### 🏗️ Structural Changes
Architecture and organization:
- File reorganization
- Class/module restructuring
- Method signature changes
- Package/namespace updates

### 🔄 Logic Changes
Behavioral modifications:
- Algorithm updates
- Business rule changes
- Control flow modifications
- Data processing changes

### 🛡️ Security Changes
Protection and access:
- Authentication updates
- Authorization changes
- Input validation
- Encryption implementations

### ⚡ Performance Changes
Speed and efficiency:
- Algorithm optimization
- Caching implementation
- Database query improvements
- Resource usage optimization

### 📝 Quality Changes
Maintainability and standards:
- Code style updates
- Documentation additions
- Test coverage improvements
- Refactoring activities

## Configuration Options

**Analysis Scope**:
- `--single-commit`: Focus on one commit
- `--range=start..end`: Analyze commit range
- `--file=specific.py`: Analyze specific file changes

**Detail Level**:
- `--summary`: High-level overview
- `--detailed`: Comprehensive analysis
- `--security-focus`: Emphasize security aspects
- `--performance-focus`: Highlight performance impacts

**Output Format**:
- `--format=text`: Human-readable
- `--format=markdown`: Documentation-ready
- `--format=json`: Machine-readable

## Integration with Workflows

**Code Review Process**:
```
1. Developer creates PR
2. /diff-summariser analyzes changes
3. Reviewer uses summary for review
4. Issues identified and addressed
5. Summary included in merge documentation
```

**Release Management**:
```
1. Generate diff summary for release
2. Identify critical changes
3. Assess deployment risks
4. Create release notes
5. Plan rollout strategy
```

**Development Tracking**:
```
1. Daily/weekly change summaries
2. Track project evolution
3. Identify development patterns
4. Measure team productivity
5. Improve development processes
```

## Advanced Features

### Pattern Recognition
Identifies common change patterns:
- Refactoring patterns
- Bug fix patterns
- Feature addition patterns
- Security update patterns

### Risk Assessment
Evaluates change risk levels:
- Breaking change probability
- Regression likelihood
- Performance impact assessment
- Security vulnerability introduction

### Impact Prediction
Forecasts change effects:
- Dependency impact analysis
- Performance prediction
- Compatibility assessment
- Maintenance effort estimation

## Best Practices

### 1. Regular Usage
Integrate into daily workflow:
- Review morning changes
- Check PR summaries
- Track weekly progress
- Monitor project evolution

### 2. Focus on Value
Don't over-analyze:
- Focus on significant changes
- Skip trivial modifications
- Emphasize impactful updates
- Highlight critical issues

### 3. Action-Oriented
Drive decision-making:
- Identify required actions
- Prioritize based on impact
- Assign appropriate reviewers
- Plan follow-up activities

### 4. Collaborative Sharing
Communicate effectively:
- Share summaries with team
- Document important changes
- Track decision rationale
- Maintain change history

## Common Use Cases

### Daily Development
Track personal progress:
```
"What did I change today?"
"Summarize my commits from this morning"
```

### Code Review
Support review process:
```
"Review this PR for issues"
"Summarize changes for the reviewer"
```

### Release Planning
Prepare for deployment:
```
"What changed this sprint?"
"Summarize changes for release notes"
```

### Troubleshooting
Investigate issues:
```
"What changed in the last deployment?"
"Show recent changes to this module"
```

## Token Efficiency

- Single commit: ~200 tokens
- Medium PR (5-10 files): ~400 tokens
- Large change set: ~800 tokens
- Historical analysis: ~150 tokens per time period

## Related Skills

- `git/repo-briefing` - Understand repository context
- `analysis/code/api-contract-sniffer` - Check API changes
- `development/refactoring` - Analyze refactoring impact
- `analysis/code/dead-code-hunter` - Identify removed functionality

---

**Ready to understand your changes?** Just tell Claude: "Summarize this diff" or "Review these changes"!