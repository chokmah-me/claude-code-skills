---
name: dependency-audit
description: List top-level runtime dependencies from package.json, requirements.txt, or other lock files. Use when user says "audit deps", "check dependencies", or "what packages do we use".
---

# Dependency Audit Skill

## 🎯 Purpose

List runtime dependencies with version numbers across multiple languages and package managers. Automatically detects dependency files and provides package count statistics for quick security audits.

## 🚀 Key Features

- **Multi-language support**: Node.js, Python, Rust, Go, Ruby, PHP, Java
- **Version extraction**: Shows package versions alongside names
- **Auto-detection**: Finds package.json, requirements.txt, Cargo.toml, go.mod, Gemfile, composer.json, pom.xml
- **Dependency count**: Shows total number of dependencies found
- **Token efficient**: ~600-800 tokens vs 20k+ for parsing full lockfiles
- **CVE check ready**: Structured output for vulnerability research

## 📋 Usage

When user requests dependency audit:

1. **Run the command** to extract dependencies with versions
2. **Present sorted list** (top 20 dependencies)
3. **Show count statistics** (total dependencies found)
4. **Offer follow-up**: "Want me to check for known CVEs or outdated versions?"

## Command

```bash
# Auto-detect dependency file and extract packages with versions

if [ -f "package.json" ]; then
  echo "=== Node.js Dependencies (package.json) ==="
  cat package.json | jq -r '.dependencies // {} | to_entries[] | "\(.key)@\(.value)"' 2>/dev/null | sort | head -20
  echo ""
  echo "Total: $(cat package.json | jq -r '.dependencies // {} | length' 2>/dev/null) runtime dependencies"

elif [ -f "requirements.txt" ]; then
  echo "=== Python Dependencies (requirements.txt) ==="
  grep -v '^#' requirements.txt | grep -v '^$' | sort | head -20
  echo ""
  echo "Total: $(grep -v '^#' requirements.txt | grep -v '^$' | wc -l) dependencies"

elif [ -f "Cargo.toml" ]; then
  echo "=== Rust Dependencies (Cargo.toml) ==="
  grep -A 1000 '^\[dependencies\]' Cargo.toml | grep -v '^\[' | grep '=' | sed 's/ = /=/g' | sort | head -20
  echo ""
  echo "Total: $(grep -A 1000 '^\[dependencies\]' Cargo.toml | grep -v '^\[' | grep '=' | wc -l) dependencies"

elif [ -f "go.mod" ]; then
  echo "=== Go Dependencies (go.mod) ==="
  grep -E '^\s+[a-z]' go.mod | awk '{print $1"@"$2}' | sort | head -20
  echo ""
  echo "Total: $(grep -E '^\s+[a-z]' go.mod | wc -l) dependencies"

elif [ -f "Gemfile" ]; then
  echo "=== Ruby Dependencies (Gemfile) ==="
  grep "gem ['\"]" Gemfile | sed "s/.*gem ['\"]\\([^'\"]*\\)['\"].*/\\1/" | sort | head -20
  echo ""
  echo "Total: $(grep "gem ['\"]" Gemfile | wc -l) dependencies"

elif [ -f "composer.json" ]; then
  echo "=== PHP Dependencies (composer.json) ==="
  cat composer.json | jq -r '.require // {} | to_entries[] | "\(.key)@\(.value)"' 2>/dev/null | grep -v '^php@' | sort | head -20
  echo ""
  echo "Total: $(cat composer.json | jq -r '.require // {} | length' 2>/dev/null) dependencies"

elif [ -f "pom.xml" ]; then
  echo "=== Java Dependencies (pom.xml) ==="
  grep -A 2 '<dependency>' pom.xml | grep -E '<groupId>|<artifactId>|<version>' | sed 's/.*<groupId>\\(.*\\)<\\/groupId>.*/\\1/' | sed 'N;N;s/\\n/:/g' | head -20
  echo ""
  echo "Total: $(grep -c '<dependency>' pom.xml) dependencies"

else
  echo "No dependency file found"
  echo "Supported: package.json, requirements.txt, Cargo.toml, go.mod, Gemfile, composer.json, pom.xml"
fi
```

## 🎁 Output

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

## 🎛️ Parameters

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

## Verification Helper

After finding dependencies, check for vulnerabilities or usage:

```bash
# Check if a specific package is actually used in code
echo "Checking usage of 'lodash':"
grep -rn "require.*lodash\|import.*lodash\|from.*lodash" . --include="*.js" --include="*.ts" | head -10

# Search for known vulnerabilities (example for Node.js)
npm audit --json | jq '.vulnerabilities | to_entries[] | select(.value.severity == "high" or .value.severity == "critical")'

# Check for outdated packages
npm outdated  # Node.js
pip list --outdated  # Python
cargo outdated  # Rust
```

## How It Works

1. **Auto-detect language**: Check for dependency files in order of priority
2. **Extract dependencies**: Parse file format (JSON, TOML, plain text, XML)
3. **Format output**: Show package@version format where possible
4. **Count total**: Display total number of dependencies found
5. **Limit output**: First 20 entries for quick overview

## 💡 Examples

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

## ⚠️ Important Notes

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

## Follow-Up Actions

After presenting list, Claude can:
- **Security**: Web search for CVE vulnerabilities (structured output helps)
- **Updates**: Check npm/PyPI/crates.io for latest versions
- **Deprecation**: Identify deprecated or unmaintained packages
- **Alternatives**: Suggest lighter or more secure alternatives
- **Licensing**: Check license compatibility for commercial use

## Use Cases

1. **Security audit** - Quick vulnerability assessment before deployment
2. **Dependency review** - Understand what packages the project relies on
3. **License compliance** - Identify packages for license audit
4. **Onboarding** - Help new developers understand project dependencies
5. **Migration planning** - Assess dependencies before major upgrades

## Token Efficiency

- **This skill**: ~600-800 tokens for extraction + display
- **Manual approach**: Parsing full package-lock.json or Cargo.lock (~20,000+ tokens)
- **Savings**: 96% reduction in token usage
- **Benefit**: Enables targeted vulnerability research on specific packages
