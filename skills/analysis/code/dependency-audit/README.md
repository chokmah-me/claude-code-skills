# Dependency Audit

A Claude Code skill for quickly listing runtime dependencies with version numbers across multiple languages and package managers.

## Overview

Dependency Audit analyzes your project to extract runtime dependencies with version information. Supports 7 major package managers and provides dependency counts for quick security audits and dependency reviews.

## Supported Languages & Package Managers

- **Node.js**: package.json (npm/yarn/pnpm)
- **Python**: requirements.txt (pip)
- **Rust**: Cargo.toml (cargo)
- **Go**: go.mod (go modules)
- **Ruby**: Gemfile (bundler)
- **PHP**: composer.json (composer)
- **Java**: pom.xml (maven)

## How It Works

1. **Auto-detects package manager** by checking for dependency files in priority order
2. **Extracts dependencies** with version numbers in native format
3. **Counts total dependencies** for quick overview
4. **Outputs first 20** dependencies for token efficiency

## Usage

Simply invoke the skill in your project directory:

```bash
/dependency-audit
```

The skill will automatically:
- Detect your project's package manager
- Extract dependencies with versions
- Show total dependency count

## Output Format

### Node.js Project (package.json)

```
=== Node.js Dependencies (package.json) ===
@types/node@^18.16.3
cors@^2.8.5
dotenv@^16.0.3
express@^4.18.2
jsonwebtoken@^9.0.0
mongoose@^7.2.0

Total: 18 runtime dependencies
```

### Python Project (requirements.txt)

```
=== Python Dependencies (requirements.txt) ===
Django==4.2.0
Flask==2.3.2
numpy==1.24.3
pandas==2.0.2
requests==2.31.0

Total: 28 dependencies
```

### Rust Project (Cargo.toml)

```
=== Rust Dependencies (Cargo.toml) ===
actix-web="4.3"
clap={ version="4.3", features=["derive"] }
serde={ version="1.0", features=["derive"] }
tokio={ version="1.28", features=["full"] }

Total: 15 dependencies
```

## Verification Workflow

### Step 1: Run the Skill

```bash
/dependency-audit
```

### Step 2: Check for Vulnerabilities

After seeing dependencies, check for security issues:

```bash
# Node.js - Check for known vulnerabilities
npm audit

# Show only high/critical issues
npm audit --json | jq '.vulnerabilities | to_entries[] | select(.value.severity == "high" or .value.severity == "critical")'

# Python - Check for security issues
pip-audit  # Requires: pip install pip-audit

# Rust - Check advisories
cargo audit  # Requires: cargo install cargo-audit

# Go - Check vulnerabilities
go list -json -m all | nancy sleuth  # Requires nancy tool
```

### Step 3: Check for Updates

Check if dependencies are outdated:

```bash
# Node.js
npm outdated

# Python
pip list --outdated

# Rust
cargo outdated  # Requires: cargo install cargo-outdated

# Go
go list -u -m all

# Ruby
bundle outdated

# PHP
composer outdated
```

### Step 4: Verify Usage

Check if a dependency is actually used in code:

```bash
# Node.js/TypeScript
grep -rn "require.*lodash\|import.*lodash\|from.*lodash" . --include="*.js" --include="*.ts"

# Python
grep -rn "import requests\|from requests" . --include="*.py"

# Rust
grep -rn "use serde\|extern crate serde" . --include="*.rs"
```

## Known Limitations

### What This Skill Shows

- ✅ **Declared dependencies**: What's in your dependency file
- ✅ **Version ranges**: As specified (^4.18.2, ==4.2.0, etc.)
- ✅ **Runtime dependencies**: Production packages only
- ✅ **Direct dependencies**: Top-level packages

### What This Skill Doesn't Show

- ❌ **Dev dependencies**: devDependencies, [dev-dependencies], test packages
- ❌ **Transitive dependencies**: Nested dependencies of your packages
- ❌ **Resolved versions**: Actual installed versions in node_modules/venv
- ❌ **Lockfile info**: Exact versions from package-lock.json, Cargo.lock

### Comparison Table

| Aspect | This Skill | Full Lockfile Parse |
|--------|------------|---------------------|
| Token cost | ~600-800 | ~20,000+ |
| Speed | Instant | Slow |
| Direct deps | ✅ | ✅ |
| Transitive deps | ❌ | ✅ |
| Exact versions | ❌ | ✅ |
| Version ranges | ✅ | ❌ |

## For Complete Dependency Info

Use language-specific tools:

```bash
# Node.js - Full dependency tree
npm list --all

# Python - All installed packages
pip freeze
pip list

# Rust - Complete dependency tree
cargo tree

# Go - All module dependencies
go list -m all

# Ruby - Bundle info
bundle list

# PHP - Complete dependencies
composer show
```

## Token Efficiency

- **This skill**: ~600-800 tokens
- **Manual approach**: Reading package-lock.json or Cargo.lock (~20,000+ tokens)
- **Savings**: 96% reduction in token usage
- **Benefit**: Quick overview enables targeted vulnerability research

## Advanced Usage

### Custom Output Limit

Modify the skill command to show more/fewer dependencies:

```bash
# Show first 50 dependencies (change all head -20 to head -50)
cat package.json | jq -r '.dependencies // {} | to_entries[] | "\(.key)@\(.value)"' | sort | head -50
```

### Check Specific Dependency File

Force checking a specific file:

```bash
# Force package.json even if other files exist
cat package.json | jq -r '.dependencies // {} | to_entries[] | "\(.key)@\(.value)"' | sort

# Force requirements.txt
grep -v '^#' requirements.txt | grep -v '^$' | sort
```

### Include Dev Dependencies

Modify for Node.js to include devDependencies:

```bash
cat package.json | jq -r '.dependencies // {}, .devDependencies // {} | to_entries[] | "\(.key)@\(.value)"' | sort | uniq
```

## Integration with Other Skills

- **Use with**: `/dead-code-hunter` to find unused dependencies
- **Follow up**: Web search for CVE vulnerabilities on specific packages
- **Before**: `/repo-briefing` to understand project structure
- **After**: `/quick-test-runner` to verify tests pass with updated deps

## Use Cases

1. **Security audit** - Quick vulnerability assessment before deployment
2. **Dependency review** - Understand what packages the project uses
3. **Onboarding** - Help new developers understand dependencies
4. **License compliance** - Identify packages for license audit
5. **Migration planning** - Assess dependencies before major upgrades
6. **Bloat detection** - Find heavy or unnecessary dependencies

## Best Practices

1. **Run regularly** - Check dependencies monthly or before releases
2. **Follow up with audits** - Use `npm audit`, `pip-audit`, `cargo audit`
3. **Check for updates** - Keep dependencies current for security
4. **Review new deps** - Audit before adding new dependencies
5. **Document choices** - Record why specific versions are used
6. **Monitor CVEs** - Subscribe to security advisories for key packages

## Troubleshooting

### "No dependency file found"

- Verify you're in the project root directory
- Check if you have a supported dependency file
- Supported files: package.json, requirements.txt, Cargo.toml, go.mod, Gemfile, composer.json, pom.xml

### Missing dependencies in output

- Skill only shows runtime dependencies (not dev)
- Check if dependencies are in a different section (devDependencies, etc.)
- For complete list, use language-specific tools (`npm list`, `pip freeze`)

### Version numbers not showing

- **Node.js/PHP**: Ensure `jq` is installed (`jq --version`)
- **Python**: Check requirements.txt format (package==version)
- **Rust**: Verify Cargo.toml [dependencies] section format

### Wrong dependency file detected

The skill checks files in priority order:
1. package.json
2. requirements.txt
3. Cargo.toml
4. go.mod
5. Gemfile
6. composer.json
7. pom.xml

If you have multiple files and want a specific one, modify the command to check only that file.

## Examples

### Example 1: Node.js Express API

```bash
$ cd my-express-api
$ /dependency-audit

=== Node.js Dependencies (package.json) ===
@types/node@^18.16.3
cors@^2.8.5
dotenv@^16.0.3
express@^4.18.2
jsonwebtoken@^9.0.0
mongoose@^7.2.0
winston@^3.8.2

Total: 18 runtime dependencies

# Check for vulnerabilities
$ npm audit
found 2 vulnerabilities (1 moderate, 1 high)

# Show details
$ npm audit --json | jq '.vulnerabilities'
```

### Example 2: Python Django Project

```bash
$ cd my-django-app
$ /dependency-audit

=== Python Dependencies (requirements.txt) ===
Django==4.2.0
celery==5.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.6
redis==4.5.5
requests==2.31.0

Total: 12 dependencies

# Check for outdated packages
$ pip list --outdated
Package               Version   Latest
--------------------- --------- ------
celery                5.2.7     5.3.1
requests              2.31.0    2.31.2
```

### Example 3: Rust CLI Tool

```bash
$ cd my-rust-cli
$ /dependency-audit

=== Rust Dependencies (Cargo.toml) ===
clap={ version="4.3", features=["derive"] }
serde={ version="1.0", features=["derive"] }
serde_json="1.0"
tokio={ version="1.28", features=["full"] }

Total: 8 dependencies

# Check for security advisories
$ cargo audit
No vulnerabilities found!
```

### Example 4: Multi-Language Monorepo

```bash
# Backend (Node.js)
$ cd backend
$ /dependency-audit
=== Node.js Dependencies (package.json) ===
express@^4.18.2
...
Total: 23 runtime dependencies

# Frontend (different package.json)
$ cd ../frontend
$ /dependency-audit
=== Node.js Dependencies (package.json) ===
react@^18.2.0
...
Total: 31 runtime dependencies

# CLI tool (Rust)
$ cd ../cli
$ /dependency-audit
=== Rust Dependencies (Cargo.toml) ===
clap={ version="4.3", features=["derive"] }
...
Total: 12 dependencies
```

## Contributing

Found a bug or have suggestions? Issues and PRs welcome at the [claude-code-skills repository](https://github.com/chokmah-me/claude-code-skills).

## License

Part of the claude-code-skills collection. See repository root for license information.
