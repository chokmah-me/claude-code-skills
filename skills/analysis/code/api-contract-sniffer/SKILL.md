---
name: api-contract-sniffer
description: Show API surface by finding route declarations (REST endpoints). Use when user says "show api surface", "list endpoints", or "what routes exist".
---

# API Contract Sniffer Skill

## 🎯 Purpose

Map API endpoints without reading full controller files. Automatically detects framework (Flask/FastAPI/Express) and extracts precise endpoint locations with HTTP methods and routes.

## 🚀 Key Features

- **Language detection**: Auto-detects Python (Flask/FastAPI) or JavaScript/TypeScript (Express) frameworks
- **Source directory detection**: Automatically finds `src/`, `app/`, `api/`, or uses current directory
- **Precise location tracking**: Shows file path, line number, HTTP method, and route for each endpoint
- **Framework-aware patterns**: Recognizes decorators (@app.route) and method calls (app.get, router.post)
- **Cross-platform**: Uses `mktemp` for reliable temp file handling on Windows/Unix
- **Token efficient**: ~600-800 tokens vs 20k+ for reading all controllers

## 📋 Usage

When user requests API surface mapping:

1. **Run the command** to find route declarations
2. **Present first 15 endpoints** showing:
   - File path and line number
   - HTTP method (GET/POST/PUT/DELETE)
   - Route path or handler name
3. **Offer**: "Want details on specific endpoints or full API documentation?"

## Command

```bash
# Detect source directory (API code locations)
SRC_DIR=$(test -d src && echo "src" || test -d app && echo "app" || test -d api && echo "api" || echo ".")

# Create temp directory (cross-platform)
TMPD=$(mktemp -d 2>/dev/null || mktemp -d -t 'api-sniffer')

# Detect language and extract endpoints
if ls *.py 2>/dev/null || find "$SRC_DIR" -name "*.py" 2>/dev/null | head -1 | grep -q .; then
  echo "=== Python API Endpoints (Flask/FastAPI) ==="

  # Extract Flask decorator routes: @app.route('/path', methods=['GET'])
  grep -rn '@app\.route\|@router\.\(get\|post\|put\|delete\|patch\)' "$SRC_DIR" --include="*.py" > "$TMPD/py_routes.txt" 2>/dev/null

  # Extract FastAPI function-based routes: @app.get("/path")
  grep -rn '@app\.\(get\|post\|put\|delete\|patch\)\|@router\.\(get\|post\|put\|delete\|patch\)' "$SRC_DIR" --include="*.py" >> "$TMPD/py_routes.txt" 2>/dev/null

  # Format: filepath:line METHOD /route
  if [ -s "$TMPD/py_routes.txt" ]; then
    cat "$TMPD/py_routes.txt" | sed -E 's/@(app|router)\.(get|post|put|delete|patch)\(["'\''](.*?)["'\''].*/@\1.\2 \3/' | \
    sed -E 's/@(app|router)\.route\(["'\''](.*?)["'\''].*methods=\[["'\''](.*?)["'\'']\].*/@\1.route \3 \2/' | \
    sed -E 's/^([^:]+):([0-9]+):.*@(app|router)\.(get|post|put|delete|patch|route) /\1:\2 \U\4\E /' | \
    head -15
  else
    echo "No Python API endpoints found"
  fi

elif ls *.js *.ts 2>/dev/null || find "$SRC_DIR" -name "*.js" -o -name "*.ts" 2>/dev/null | head -1 | grep -q .; then
  echo "=== JavaScript/TypeScript API Endpoints (Express) ==="

  # Extract Express routes: app.get('/path', ...), router.post('/api/users', ...)
  grep -rn '\(app\|router\)\.\(get\|post\|put\|delete\|patch\|use\)(' "$SRC_DIR" --include="*.js" --include="*.ts" > "$TMPD/js_routes.txt" 2>/dev/null

  # Format: filepath:line METHOD /route
  if [ -s "$TMPD/js_routes.txt" ]; then
    cat "$TMPD/js_routes.txt" | sed -E 's/(app|router)\.(get|post|put|delete|patch|use)\(["'\''](.*?)["'\''].*/\1.\2 \3/' | \
    sed -E 's/^([^:]+):([0-9]+):.*\.(get|post|put|delete|patch|use) /\1:\2 \U\3\E /' | \
    head -15
  else
    echo "No JavaScript/TypeScript API endpoints found"
  fi

else
  echo "No Python or JS/TS files detected"
fi

# Clean up temp directory
rm -rf "$TMPD"
```

## 🎁 Output

### Python (Flask/FastAPI)
```
=== Python API Endpoints (Flask/FastAPI) ===
src/api/users.py:42 GET /api/users
src/api/users.py:67 POST /api/users
src/api/auth.py:15 POST /api/auth/login
src/api/health.py:8 GET /health
```

### JavaScript/TypeScript (Express)
```
=== JavaScript/TypeScript API Endpoints (Express) ===
src/routes/users.ts:23 GET /api/users
src/routes/users.ts:45 POST /api/users
src/routes/auth.js:12 POST /api/auth/login
src/server.js:18 GET /health
```

Each line shows:
- **File path**: Relative path to the controller/route file
- **Line number**: Where the endpoint is defined
- **HTTP method**: GET, POST, PUT, DELETE, PATCH, USE
- **Route path**: The URL path for the endpoint

## 🎛️ Parameters

None required - the skill auto-detects:
- **Language**: Python (*.py) or JavaScript/TypeScript (*.js, *.ts)
- **Framework**: Flask/FastAPI or Express based on decorator/method patterns
- **Source directory**: Tries `src/`, `app/`, `api/`, then current directory
- **Output limit**: First 15 endpoints

Optional environment variable:
- `SRC_DIR`: Override source directory detection (e.g., `SRC_DIR=backend/routes`)

## Verification Helper

After finding endpoints, verify individual endpoint usage or check for callers:

```bash
# Verify a specific route (replace /api/users with actual route)
echo "Checking all references to '/api/users':"
grep -rn "'/api/users'\|/api/users" . --include="*.py" --include="*.js" --include="*.ts" --color=always | head -20

# Find tests for an endpoint
grep -rn "test.*users\|/api/users" tests/ --include="*.py" --include="*.js" --include="*.ts" | head -10
```

This shows:
- All occurrences of the route path in code
- Tests that exercise the endpoint
- Client code that calls the API

## How It Works

1. **Auto-detect language**: Check for Python (*.py) or JS/TS (*.js, *.ts) files
2. **Find source directory**: Try `src/`, `app/`, `api/`, or current directory
3. **Extract route declarations**:
   - Python: `@app.route()`, `@app.get()`, `@router.post()`, etc.
   - JS/TS: `app.get()`, `router.post()`, etc.
4. **Parse with sed**: Extract method and path from decorator/call
5. **Format output**: `file:line METHOD /path`
6. **Limit**: First 15 results (high-signal endpoints)

## Framework Detection

**Python (Flask/FastAPI)**:
- `@app.route('/path', methods=['GET'])`
- `@app.get('/path')`, `@app.post('/path')`
- `@router.get('/path')`, `@router.post('/path')`

**Node.js (Express)**:
- `app.get('/path', handler)`
- `router.post('/api/path', handler)`
- `app.use('/middleware')`

## 💡 Examples

### Example 1: Flask API
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
```

### Example 2: Express API
```bash
$ cd my-express-api
$ /api-contract-sniffer

=== JavaScript/TypeScript API Endpoints (Express) ===
src/routes/users.ts:23 GET /api/users
src/routes/users.ts:45 POST /api/users
src/routes/users.ts:67 PUT /api/users/:id
src/routes/auth.js:12 POST /api/auth/login
src/routes/auth.js:24 POST /api/auth/register
src/server.js:18 GET /health
```

### Example 3: Verifying Endpoint Usage
```bash
# Check if endpoint has tests
$ grep -rn "/api/users" tests/
tests/test_users.py:15:    response = client.get("/api/users")
tests/test_users.py:32:    response = client.post("/api/users", json=data)
# Endpoint is tested ✓
```

## ⚠️ Important Notes

**This skill identifies route declarations, not runtime behavior.**

May miss:
- **Dynamically registered routes** (routes added at runtime)
- **Routes in separate config files** (not in source code)
- **Middleware-wrapped endpoints** (hidden by middleware)
- **Auto-generated REST APIs** (ORM-based CRUD)

For complete mapping, use framework-specific tools:
```bash
# Flask
flask routes

# Express
npm run routes  # if script exists
```

## Use Cases

- Quick API inventory for new team members
- Finding undocumented endpoints
- Planning API refactor
- Security audit (what's exposed?)
- OpenAPI/Swagger generation prep

## Follow-Up Actions

After seeing API surface, Claude can:
- Generate OpenAPI spec
- Check for missing authentication
- Identify REST antipatterns
- Suggest route consolidation
- Create API documentation

## Token Efficiency

- **This skill**: ~600-800 tokens
- **Manual approach**: Reading all controllers (~20k+ tokens)
- **Savings**: 96% reduction in API mapping cost
