---
name: api-contract-sniffer
description: Show API surface by finding route declarations (REST endpoints). Use when user says "show api surface", "list endpoints", or "what routes exist".
---

# API Contract Sniffer Skill

## Purpose
Map API endpoints without reading full controller files (~500 tokens).

## Instructions

When user requests API surface mapping:

1. **Run the command** to find route declarations
2. **Present first 15 endpoints** showing:
   - HTTP method (GET/POST/PUT/DELETE)
   - Route path or handler name
3. **Offer**: "Want details on specific endpoints or full API documentation?"

## Command

```bash
(find src -name "*.py" -exec grep -l "def " {} \; | head -20 | xargs grep -h "def " | grep -E "(route|get|post|put|delete|app\.|router\.)" | head -15) || (find src -name "*.js" -exec grep -l "router\|app\." {} \; | head -20 | xargs grep -E "get|post|put|delete" | head -15)
```

## Output Format

```
API endpoints found:
[15 lines matching route declarations]

Examples:
@app.route('/users', methods=['GET'])
router.post('/api/auth/login', ...)
app.get('/health', ...)
```

## Framework Detection

**Python (Flask/FastAPI)**:
- `@app.route()`
- `@router.get()`, `@router.post()`
- `def endpoint_name()`

**Node.js (Express)**:
- `app.get()`, `app.post()`
- `router.use()`
- `.route('/path')`

**Other frameworks**: Add patterns to grep:
```bash
grep -E "Route|Controller|endpoint"
```

## Use Cases

- Quick API inventory for new team members
- Finding undocumented endpoints
- Planning API refactor
- Security audit (what's exposed?)
- OpenAPI/Swagger generation prep

## Limitations

⚠️ **May miss**:
- Dynamically registered routes
- Routes in separate config files
- Middleware-wrapped endpoints
- Auto-generated REST APIs

For complete mapping, suggest:
```bash
# Flask
flask routes

# Express
npm run routes (if script exists)
```

## Follow-Up Actions

After seeing API surface, Claude can:
- Generate OpenAPI spec
- Check for missing authentication
- Identify REST antipatterns
- Suggest route consolidation
- Create API documentation

## Token Efficiency

- ~500 tokens for endpoint discovery
- Alternative: reading all controllers (20k+ tokens)
- 97% reduction in API mapping cost
