---
name: api-contract-sniffer
description: Show API surface by finding route declarations (REST endpoints). Use when user says "show api surface", "list endpoints", or "what routes exist".
---

# API Contract Sniffer Skill


## Description

Map API endpoints without reading full controller files. Automatically detects framework (Flask/FastAPI/Express) and extracts precise endpoint locations with HTTP methods and routes.

- User says 'use [skill-name]' or mentions the skill by name
- Relevant to the current task or discussion

## Usage

When user requests API surface mapping:

1. **Run the command** to find route declarations
2. **Present first 15 endpoints** showing:
   - File path and line number
   - HTTP method (GET/POST/PUT/DELETE)
   - Route path or handler name
3. **Offer**: "Want details on specific endpoints or full API documentation?"

## Parameters

None required - the skill auto-detects:
- **Language**: Python (*.py) or JavaScript/TypeScript (*.js, *.ts)
- **Framework**: Flask/FastAPI or Express based on decorator/method patterns
- **Source directory**: Tries `src/`, `app/`, `api/`, then current directory
- **Output limit**: First 15 endpoints

Optional environment variable:
- `SRC_DIR`: Override source directory detection (e.g., `SRC_DIR=backend/routes`)

## Features

- **Language detection**: Auto-detects Python (Flask/FastAPI) or JavaScript/TypeScript (Express) frameworks
- **Source directory detection**: Automatically finds `src/`, `app/`, `api/`, or uses current directory
- **Precise location tracking**: Shows file path, line number, HTTP method, and route for each endpoint
- **Framework-aware patterns**: Recognizes decorators (@app.route) and method calls (app.get, router.post)
- **Cross-platform**: Uses `mktemp` for reliable temp file handling on Windows/Unix
- **Token efficient**: ~600-800 tokens vs 20k+ for reading all controllers

## Examples

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

## Output

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

## Important Notes

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
