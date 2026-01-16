---
name: dependency-audit
description: List top-level runtime dependencies from package.json, requirements.txt, or other lock files. Use when user says "audit deps", "check dependencies", or "what packages do we use".
---

# Dependency Audit Skill


## Description

List runtime dependencies with version numbers across multiple languages and package managers. Automatically detects dependency files and provides package count statistics for quick security audits.

- User says 'use [skill-name]' or mentions the skill by name
- Relevant to the current task or discussion

## Usage

When user requests dependency audit:

1. **Run the command** to extract dependencies with versions
2. **Present sorted list** (top 20 dependencies)
3. **Show count statistics** (total dependencies found)
4. **Offer follow-up**: "Want me to check for known CVEs or outdated versions?"

## Parameters

None required - the skill auto-detects:
- **Language**: Checks for dependency files in priority order
- **Version format**: Extracts versions in native format (^4.18.2, ==4.2.0, etc.)
- **Output limit**: First 20 dependencies (configurable with `head -N`)

Supported dependency files (checked in order):
1. `package.json` - Node.js (npm/yarn/pnpm)
2. `requirements.txt` - Python (pip)
3. `Cargo.toml` - Rust (cargo)
4. `go.mod` - Go (go modules)
5. `Gemfile` - Ruby (bundler)
6. `composer.json` - PHP (composer)
7. `pom.xml` - Java (maven)

## Features

- **Multi-language support**: Node.js, Python, Rust, Go, Ruby, PHP, Java
- **Version extraction**: Shows package versions alongside names
- **Auto-detection**: Finds package.json, requirements.txt, Cargo.toml, go.mod, Gemfile, composer.json, pom.xml
- **Dependency count**: Shows total number of dependencies found
- **Token efficient**: ~600-800 tokens vs 20k+ for parsing full lockfiles
- **CVE check ready**: Structured output for vulnerability research

## Examples

### Example 1: Node.js Security Audit
```bash
$ cd my-express-app
$ /dependency-audit

=== Node.js Dependencies (package.json) ===
@types/node@^18.16.3
cors@^2.8.5
dotenv@^16.0.3
express@^4.18.2
jsonwebtoken@^9.0.0
mongoose@^7.2.0

Total: 18 runtime dependencies

# Follow up with CVE check
$ npm audit
found 2 vulnerabilities (1 moderate, 1 high)
```

### Example 2: Python Dependencies
```bash
$ cd my-django-project
$ /dependency-audit

=== Python Dependencies (requirements.txt) ===
Django==4.2.0
celery==5.2.7
psycopg2-binary==2.9.6
redis==4.5.5
requests==2.31.0

Total: 12 dependencies

# Check for outdated packages
$ pip list --outdated
```

### Example 3: Rust Project
```bash
$ cd my-rust-cli
$ /dependency-audit

=== Rust Dependencies (Cargo.toml) ===
clap={ version="4.3", features=["derive"] }
serde={ version="1.0", features=["derive"] }
tokio={ version="1.28", features=["full"] }

Total: 8 dependencies
```

## Output

### Node.js Project
```
=== Node.js Dependencies (package.json) ===
express@^4.18.2
lodash@^4.17.21
moment@^2.29.4
react@^18.2.0
typescript@^5.0.4

Total: 42 runtime dependencies
```

### Python Project
```
=== Python Dependencies (requirements.txt) ===
Django==4.2.0
Flask==2.3.2
numpy==1.24.3
pandas==2.0.2
requests==2.31.0

Total: 28 dependencies
```

### Rust Project
```
=== Rust Dependencies (Cargo.toml) ===
serde={ version="1.0", features=["derive"] }
tokio={ version="1.28", features=["full"] }
actix-web="4.3"
clap={ version="4.3", features=["derive"] }

Total: 15 dependencies
```

## Important Notes

**This skill extracts declared dependencies, not installed versions.**

Limitations:
- **Dev dependencies**: Only shows runtime dependencies (not devDependencies, [dev-dependencies], etc.)
- **Transitive dependencies**: Doesn't show nested/indirect dependencies (use lockfiles for that)
- **Version ranges**: Shows declared ranges (^4.18.2), not resolved versions
- **Lockfile sync**: May differ from actual installed versions in node_modules/venv

For complete dependency tree:
```bash
# Node.js
npm list --all

# Python
pip freeze

# Rust
cargo tree

# Go
go list -m all
```
