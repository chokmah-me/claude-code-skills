# API Contract Sniffer

A Claude Code skill for quickly discovering REST API endpoints across Python (Flask/FastAPI) and JavaScript/TypeScript (Express) projects.

## Overview

API Contract Sniffer analyzes your codebase to find route declarations with precise file locations, line numbers, HTTP methods, and route paths. This helps map your API surface without reading full controller files.

## Supported Frameworks

- **Python**: Flask (`@app.route`, `@app.get`) and FastAPI (`@router.get`, `@router.post`)
- **JavaScript/TypeScript**: Express (`app.get()`, `router.post()`)

## How It Works

1. **Auto-detects project framework** by scanning for `.py`, `.js`, or `.ts` files
2. **Finds source directory** automatically (`src/`, `app/`, `api/`, or current directory)
3. **Extracts route declarations** with decorators and method calls
4. **Parses HTTP methods and paths** using sed patterns
5. **Reports** the first 15 endpoints with precise file locations

## Usage

Simply invoke the skill in your project directory:

```bash
/api-contract-sniffer
```

The skill will automatically:
- Detect your project's framework
- Find the appropriate source directory
- Generate a report of API endpoints

## Output Format

### Python Projects (Flask/FastAPI)

```
=== Python API Endpoints (Flask/FastAPI) ===
src/api/users.py:42 GET /api/users
src/api/users.py:67 POST /api/users
src/api/users.py:89 DELETE /api/users/<id>
src/api/auth.py:15 POST /api/auth/login
src/api/health.py:8 GET /health
```

### JavaScript/TypeScript Projects (Express)

```
=== JavaScript/TypeScript API Endpoints (Express) ===
src/routes/users.ts:23 GET /api/users
src/routes/users.ts:45 POST /api/users
src/routes/users.ts:67 PUT /api/users/:id
src/routes/auth.js:12 POST /api/auth/login
src/server.js:18 GET /health
```

Each line shows:
- **File path**: Relative path to the controller/route file
- **Line number**: Where the endpoint is defined
- **HTTP method**: GET, POST, PUT, DELETE, PATCH, USE
- **Route path**: The URL path for the endpoint

## Verification Workflow

**Important**: The skill finds declarations, not runtime behavior. Always verify endpoints are actually registered.

### Step 1: Run the Skill

```bash
/api-contract-sniffer
```

### Step 2: Verify Individual Endpoints

For each endpoint, check all references:

```bash
# Replace /api/users with the actual route
grep -rn "'/api/users'\|/api/users" . --include="*.py" --include="*.js" --include="*.ts" --color=always | head -20
```

This shows:
- All occurrences in the codebase
- Tests that exercise the endpoint
- Client code that calls the API

### Step 3: Check for False Negatives

The skill may miss:
- **Dynamically registered routes** (added at runtime via loops or config)
- **Routes in separate config files** (YAML, JSON, or external configs)
- **Middleware-wrapped endpoints** (hidden behind middleware layers)
- **Auto-generated REST APIs** (ORM-based CRUD endpoints)

### Step 4: Use Framework Tools for Complete Mapping

For comprehensive route listing:

```bash
# Flask
flask routes

# Express (if routes script exists)
npm run routes
```

## Known Limitations

### False Negatives

The skill may miss:

| Scenario | Example | Why It's Missed |
|----------|---------|-----------------|
| Dynamic routes | `for path in paths: app.route(path)` | Not in static code |
| Config-based routes | Routes in `routes.yaml` | Not in source files |
| Blueprint routes | Registered via `app.register_blueprint()` | Complex registration |
| Middleware routes | Hidden by `app.use(middleware)` | Indirection |
| Auto-generated APIs | ORM-based CRUD | Generated at runtime |

### Framework-Specific Patterns

**Flask/FastAPI patterns detected**:
- `@app.route('/path', methods=['GET'])`
- `@app.get('/path')`, `@app.post('/path')`
- `@router.get('/path')`, `@router.post('/path')`

**Express patterns detected**:
- `app.get('/path', handler)`
- `router.post('/api/path', handler)`
- `app.use('/middleware')`

## Token Efficiency

- **This skill**: ~600-800 tokens
- **Manual approach**: Reading all controller files (~20,000+ tokens)
- **Savings**: 96% reduction in token usage

## Advanced Usage

### Custom Source Directory

If your project has a non-standard structure, override the source directory:

```bash
# Force specific directory
SRC_DIR="backend/routes" /api-contract-sniffer
```

### Framework-Specific Analysis

Force framework detection:

```bash
# Analyze only Python endpoints
cd my-api && grep -rn '@app\.route\|@router\.\(get\|post\|put\|delete\|patch\)' src/ --include="*.py"

# Analyze only Express endpoints
cd my-api && grep -rn '\(app\|router\)\.\(get\|post\|put\|delete\|patch\|use\)(' src/ --include="*.js" --include="*.ts"
```

## Integration with Other Skills

- **Use after**: `/repo-briefing` to understand project structure first
- **Combine with**: `/dead-code-hunter` to find unused endpoint handlers
- **Follow up with**: `/quick-test-runner` to verify endpoint tests exist
- **Use before**: API documentation generation or refactoring

## Use Cases

1. **New team members** - Quick API inventory
2. **Security audit** - What endpoints are exposed?
3. **API refactoring** - Identify endpoints to consolidate
4. **Documentation** - Generate OpenAPI/Swagger specs
5. **Testing** - Find endpoints missing tests

## Best Practices

1. **Run regularly** during API development
2. **Verify output** - don't trust blindly, check framework tools too
3. **Document missing endpoints** - add comments for dynamic routes
4. **Use for planning** - before major API refactors
5. **Combine with tests** - ensure all endpoints have test coverage
6. **Check authentication** - verify endpoints have proper auth

## Troubleshooting

### "No Python or JS/TS files detected"

- Verify you're in the project root directory
- Check if files have correct extensions (`.py`, `.js`, `.ts`)
- Try specifying `SRC_DIR` explicitly

### Missing endpoints in output

- Check if routes are registered dynamically
- Look for routes in config files (YAML, JSON)
- Use framework-specific tools (`flask routes`, `npm run routes`)
- Verify blueprint/router registration

### Too many false positives

- Focus on files in `routes/`, `api/`, `controllers/` directories
- Check file:line to verify actual route definitions
- Use verification helper to check if endpoint is actually called

## Examples

### Example 1: Map Flask API

```bash
$ cd my-flask-api
$ /api-contract-sniffer

=== Python API Endpoints (Flask/FastAPI) ===
src/api/users.py:42 GET /api/users
src/api/users.py:67 POST /api/users
src/api/users.py:89 DELETE /api/users/<id>
src/api/auth.py:15 POST /api/auth/login
src/api/auth.py:28 POST /api/auth/refresh
src/api/health.py:8 GET /health

# Verify first endpoint
$ grep -rn "'/api/users'" . --include="*.py"
src/api/users.py:42:@app.route('/api/users', methods=['GET'])
tests/test_api.py:15:    response = client.get('/api/users')
# Endpoint is tested ✓
```

### Example 2: Express API Security Audit

```bash
$ cd my-express-api
$ /api-contract-sniffer

=== JavaScript/TypeScript API Endpoints (Express) ===
src/routes/users.ts:23 GET /api/users
src/routes/users.ts:45 POST /api/users
src/routes/auth.js:12 POST /api/auth/login
src/routes/admin.js:8 DELETE /api/admin/users/:id
src/server.js:18 GET /health

# Check if admin endpoint requires auth
$ grep -B5 "DELETE /api/admin/users" src/routes/admin.js
5: const requireAdmin = require('../middleware/auth');
6:
7: router.delete('/api/admin/users/:id',
8:   requireAdmin,  // ✓ Has auth middleware
9:   async (req, res) => {
```

### Example 3: Finding Undocumented Endpoints

```bash
$ /api-contract-sniffer > endpoints.txt
$ # Compare with API docs
$ cat docs/api.md | grep -o '/api/[^)]*' | sort > documented.txt
$ comm -13 documented.txt <(cat endpoints.txt | awk '{print $3}' | sort)
# Shows endpoints missing from docs
```

## Contributing

Found a bug or have suggestions? Issues and PRs welcome at the [claude-code-skills repository](https://github.com/chokmah-me/claude-code-skills).

## License

Part of the claude-code-skills collection. See repository root for license information.
