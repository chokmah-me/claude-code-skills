# API Contract Sniffer Skill - Usage Guide

## Overview

The `api-contract-sniffer` skill analyzes codebases to detect API contract violations, missing documentation, and inconsistent endpoint definitions. It helps maintain API integrity across your codebase.

**Token Efficiency**: ~800 tokens vs ~2K manual inspection (60% reduction)

## Quick Start

### Natural Language Invocation
```
"Check for API contract violations in the user service"
"Sniff the authentication module for missing API docs"
"Analyze the payment endpoints for contract consistency"
```

### Direct Skill Invocation
```
/api-contract-sniffer
```

## What It Detects

✅ **Contract Violations**:
- Missing `@param` documentation
- Incorrect return type annotations
- Mismatched parameter names
- Missing error response documentation

✅ **Endpoint Issues**:
- Undocumented endpoints
- Inconsistent URL patterns
- Missing HTTP method specifications
- Duplicate endpoint definitions

✅ **Documentation Gaps**:
- Missing OpenAPI/Swagger specs
- Incomplete parameter descriptions
- Missing response examples
- Outdated API documentation

## Analysis Process

### Phase 1: Code Discovery
Scans for API-related files:
- Controller files (`*controller*`, `*api*`)
- Route definitions (`routes.js`, `urls.py`, etc.)
- API documentation (`swagger.yaml`, `openapi.json`)
- Service interfaces (`*service*`, `*interface*`)

### Phase 2: Contract Extraction
Extracts API contracts from:
- Function/method signatures
- Decorators and annotations
- Docstrings and comments
- Configuration files

### Phase 3: Validation
Checks for consistency between:
- Code implementation vs documentation
- Parameter definitions vs usage
- Return types vs actual returns
- Error handling vs documented errors

### Phase 4: Report Generation
Creates detailed findings with:
- Violation locations (file:line)
- Severity levels (critical, warning, info)
- Suggested fixes
- Contract coverage metrics

## Example Usage

### Example 1: REST API Analysis
```
User: "Check the user management API for contract issues"

Claude: 🔍 Analyzing user management API contracts...

📊 Discovery Results:
- Found 12 API endpoints in user_controller.py
- Located OpenAPI spec: docs/user-api.yaml
- Identified 8 service methods

⚠️ Contract Violations Found:
1. CRITICAL: Missing @param validation in create_user()
   Location: user_controller.py:45
   Issue: Email parameter lacks format validation
   Fix: Add @param email:string format=email

2. WARNING: Inconsistent return type in get_user()
   Location: user_controller.py:78
   Issue: Returns User object, doc says UserDTO
   Fix: Update documentation or change return type

3. INFO: Missing response example in update_user()
   Location: user_controller.py:112
   Issue: No example response provided
   Fix: Add response example to docstring

📈 Coverage: 75% (9/12 endpoints fully documented)
```

### Example 2: Microservice Contract Check
```
User: "Analyze the payment service contracts"

Claude: 🔍 Scanning payment service for API contract issues...

📋 Analysis Summary:
- Service: payment_service.py (1,247 lines)
- Endpoints: 15 payment-related APIs
- Documentation: payment-api.md (incomplete)

🚨 Critical Issues:
1. Missing error handling docs for payment failures
2. No timeout specifications for external calls
3. Currency parameter lacks validation rules

✅ Good Practices Found:
- Consistent naming conventions
- Proper HTTP status codes
- Clear parameter descriptions

💡 Recommendations:
1. Add comprehensive error response documentation
2. Include rate limiting information
3. Specify data formats (ISO 8601 dates, currency codes)
```

## Integration with Development Workflow

**Before API Changes**:
```
1. /api-contract-sniffer (baseline check)
2. Make API modifications
3. /api-contract-sniffer (verify no new violations)
4. Update documentation
```

**During Code Review**:
```
1. Reviewer runs /api-contract-sniffer
2. Checks for contract violations
3. Ensures documentation updates
4. Approves with contract compliance
```

**In CI/CD Pipeline**:
```
# Add to pre-commit or CI pipeline
/api-contract-sniffer --fail-on-critical
# Fails build if critical violations found
```

## Supported Languages & Frameworks

✅ **Primary Support**:
- Python (Flask, Django, FastAPI)
- JavaScript/TypeScript (Express, NestJS)
- Java (Spring Boot)
- C# (.NET Core/Web API)

✅ **Documentation Formats**:
- OpenAPI 3.0+
- Swagger 2.0
- JavaDoc/Docstrings
- TypeScript interfaces
- C# XML documentation

⚠️ **Limited Support**:
- GraphQL schemas
- gRPC proto files
- Custom annotation systems

## Configuration Options

**Severity Thresholds**:
- `--critical-only`: Report only critical violations
- `--warning-level`: Include warnings and above
- `--info-level`: Show all findings (most verbose)

**Scope Control**:
- `--path=src/api`: Analyze specific directory only
- `--exclude=tests`: Skip test files
- `--include=*.py`: Focus on specific file types

**Output Formats**:
- `--format=markdown`: Human-readable report
- `--format=json`: Machine-readable output
- `--format=sarif`: IDE integration format

## Common Issues & Solutions

### Issue 1: "No API endpoints found"
**Cause**: Non-standard project structure
**Solution**: Use `--path` parameter to specify API directory

### Issue 2: "Documentation coverage low"
**Cause**: Missing OpenAPI spec or inconsistent doc locations
**Solution**: Create centralized API documentation or use annotations

### Issue 3: "False positive violations"
**Cause**: Dynamic typing or runtime contract validation
**Solution**: Add suppression comments or adjust validation rules

## Best Practices

1. **Consistent Documentation**: Maintain API docs close to code
2. **Standard Patterns**: Use consistent endpoint naming and structure
3. **Validation Early**: Add contract validation to development workflow
4. **Regular Audits**: Run monthly contract compliance checks
5. **Team Standards**: Document your API contract standards

## Anti-Patterns to Avoid

❌ **Don't**:
- Mix contract validation with business logic
- Use overly complex contract definitions
- Ignore minor violations (they accumulate)
- Rely solely on automated checking

✅ **Do**:
- Keep contracts simple and clear
- Update documentation with code changes
- Review violations regularly
- Use consistent patterns across APIs

## Token Efficiency

- Small API (10 endpoints): ~400 tokens
- Medium API (50 endpoints): ~800 tokens
- Large API (100+ endpoints): ~1,200 tokens
- Report generation: ~200 tokens

## Related Skills

- `analysis/code/dead-code-hunter` - Find unused API endpoints
- `analysis/code/dependency-audit` - Check API dependencies
- `git/diff-summariser` - Review API changes
- `development/refactoring` - Restructure APIs safely

---

**Ready to analyze?** Just tell Claude: "Check my API contracts" or "Sniff for contract violations in [module]"!