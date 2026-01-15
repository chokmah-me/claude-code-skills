<!-- SKILLS_INVENTORY_START -->
## 📋 Skills Inventory

*Last updated: 2026-01-15 23:06 UTC*

**Total Skills:** 23  
**Categories:** 6  
**Skills with README:** 22  

### Analysis / Code (4 skills)

#### Api Contract Sniffer
Show API surface by finding route declarations (REST endpoints). Use when user says "show api surface", "list endpoints", or "what routes exist".

**Purpose:** Map API endpoints without reading full controller files. Automatically detects framework (Flask/FastAPI/Express) and extracts precise endpoint locations with HTTP methods and routes.

**Location:** `skills/analysis/code/api-contract-sniffer/`  
**Documentation:** [README](skills/analysis/code/api-contract-sniffer/README.md)  

#### Ascii Sanitizer
Detect and remove unsafe Unicode/emoji characters that break YAML and GitHub Actions. Use when user says "sanitize code", "remove emojis", "fix unicode errors", or "yaml safe characters".

**Purpose:** Prevent CI/CD pipeline failures caused by non-ASCII characters (emojis, smart quotes, Unicode symbols) in code, configuration files, and documentation. This skill detects problematic characters that break YAML parsers and GitHub Actions workflows, then provides safe ASCII replacements.

**Location:** `skills/analysis/code/ascii-sanitizer/`  
**Documentation:** No README  

#### Dead Code Hunter
Find potentially unused functions, classes, and exports by comparing declarations to imports. Use when user says "find dead code", "unused functions", or "what can we delete".

**Purpose:** Identify exported symbols that are never imported across Python and JavaScript/TypeScript codebases. This skill helps find potentially unused code by comparing declarations against imports, enabling safe cleanup and technical debt reduction.

**Location:** `skills/analysis/code/dead-code-hunter/`  
**Documentation:** [README](skills/analysis/code/dead-code-hunter/README.md)  

#### Dependency Audit
List top-level runtime dependencies from package.json, requirements.txt, or other lock files. Use when user says "audit deps", "check dependencies", or "what packages do we use".

**Purpose:** List runtime dependencies with version numbers across multiple languages and package managers. Automatically detects dependency files and provides package count statistics for quick security audits.

**Location:** `skills/analysis/code/dependency-audit/`  
**Documentation:** [README](skills/analysis/code/dependency-audit/README.md)  

### Analysis / Formal (4 skills)

#### Anti Pattern Sniffer
Find fragile Coq proof patterns in .v files. Use when user says "coq anti-patterns", "check proof quality", or "find fragile proofs".

**Purpose:** Detect common Coq proof anti-patterns that cause brittleness (~800 tokens).

**Location:** `skills/analysis/formal/anti-pattern-sniffer/`  
**Documentation:** [README](skills/analysis/formal/anti-pattern-sniffer/README.md)  

#### Lemma Dependency Graph
Show most-applied lemmas in Coq proofs. Use when user says "lemma graph", "proof dependencies", or "which lemmas are critical".

**Purpose:** Identify critical lemmas by usage frequency - entry points for refactoring (~1k tokens).

**Location:** `skills/analysis/formal/lemma-dependency-graph/`  
**Documentation:** [README](skills/analysis/formal/lemma-dependency-graph/README.md)  

#### Proof Obligations Snapshot
Show admitted/open Coq proofs from .v files. Use when user says "coq obligations", "show proof TODOs", or "what proofs are incomplete".

**Purpose:** Get instant TODO list of admitted or incomplete proofs (~700 tokens).

**Location:** `skills/analysis/formal/proof-obligations-snapshot/`  
**Documentation:** [README](skills/analysis/formal/proof-obligations-snapshot/README.md)  

#### Tactic Usage Count
Count Coq tactic usage frequency in .v files. Use when user says "tactic census", "what tactics do we use", or "analyze proof style".

**Purpose:** Census of proof tactics to identify patterns and over-reliance (~600 tokens).

**Location:** `skills/analysis/formal/tactic-usage-count/`  
**Documentation:** [README](skills/analysis/formal/tactic-usage-count/README.md)  

### Analysis / Quantum (1 skills)

#### Quantum Circuit Optimizer
Optimize quantum circuits by reducing gate count, depth, and identifying optimization opportunities. Use when user says "optimize quantum circuit", "reduce circuit depth", or "analyze quantum gates".

**Purpose:** Analyze and optimize quantum circuits to reduce gate count, circuit depth, and identify optimization opportunities without executing full simulation (~800 tokens).

**Location:** `skills/analysis/quantum/quantum-circuit-optimizer/`  
**Documentation:** [README](skills/analysis/quantum/quantum-circuit-optimizer/README.md)  

### Development (4 skills)

#### Lean Plan
Enter token-efficient planning mode. Load ≤2k-token repo snapshot, adopt guard-rail persona, and produce concise checklist plans. Use when user says "start planning mode" or "plan this feature".

**Purpose:** Enter planning mode with minimal token usage by loading compact context and constraining verbosity.

**Location:** `skills/development/lean-plan/`  
**Documentation:** [README](skills/development/lean-plan/README.md)  

#### Matarao
Publish and manage blog posts on Mataroa via API. Create, update, and retrieve posts from URLs or local files. Use when user says "publish to mataroa", "update blog post", or "fetch mataroa post".

**Purpose:** Manage Mataroa blog posts directly from Claude Code without leaving your terminal. Publish from local markdown files or URLs, update existing posts, and retrieve content for editing (~700 tokens per operation vs 3000+ manual).

**Location:** `skills/development/matarao/`  
**Documentation:** [README](skills/development/matarao/README.md)  

#### Quick Test Runner
Run tests impacted by recent changes and show last 20 lines of output. Use when user says "run impacted tests", "test my changes", or "did I break anything".

**Purpose:** Run only tests affected by recent changes, show failures without full output (~800 tokens).

**Location:** `skills/development/quick-test-runner/`  
**Documentation:** [README](skills/development/quick-test-runner/README.md)  

#### Refactoring
Systematic, safe code restructuring with comprehensive validation, testing, and rollback capabilities

**Purpose:** Provides systematic, safe code restructuring capabilities with comprehensive validation. Handles complex refactorings while preserving behavior through built-in testing, rollback mechanisms, and step-by-step validation. Routes to specialized workflow templates based on refactoring type.

**Location:** `skills/development/refactoring/`  
**Documentation:** [README](skills/development/refactoring/README.md)  

### Git (3 skills)

#### Diff Summariser
Summarize git diff changes with file stats and first 30 changed lines. Use when user says "summarise diff", "review recent changes", or "what changed in last commit".

**Purpose:** Review PR/commit changes without loading entire files (~400 tokens).

**Location:** `skills/git/diff-summariser/`  
**Documentation:** [README](skills/git/diff-summariser/README.md)  

#### Migrate Repo
Migrate GitHub repository between accounts/orgs preserving full history, tags, and branches. Use when user says "migrate repo", "move repository", or "transfer github repo".

**Purpose:** Execute safe, history-preserving GitHub repository migrations using proven 9-phase workflow. ~500 tokens to invoke vs ~5K+ tokens for manual coordination.

**Location:** `skills/git/migrate-repo/`  
**Documentation:** [README](skills/git/migrate-repo/README.md)  

#### Repo Briefing
Generate a token-efficient repository summary with structure, README, package metadata, and recent commits. Use when user asks for "repo briefing", "summarize repo", or "what's the state of this code".

**Purpose:** Generate a ≤2000-token snapshot giving Claude context to start work without loading full file trees.

**Location:** `skills/git/repo-briefing/`  
**Documentation:** [README](skills/git/repo-briefing/README.md)  

### Meta (7 skills)

#### Claude Startup Integration
Master integration system that orchestrates all startup skill discovery, showcases, recommendations, and user onboarding. Ensures seamless presentation of your complete Claude Code skill ecosystem at startup with intuitive access and agent-friendly interfaces.

**Purpose:** Master orchestration system that integrates all startup components (skill showcase, recommendation engine, skill discovery) into a seamless, intuitive experience. Ensures every user and agent can easily discover and access your complete Claude Code skill ecosystem.

**Location:** `skills/meta/claude-startup-integration/`  
**Documentation:** [README](skills/meta/claude-startup-integration/README.md)  

#### Manifest Generator
Automatically generate and update the unified skill manifest. Use when adding new skills, reorganizing structure, or maintaining skill catalog accuracy.

**Purpose:** Automatically scan the skills directory structure and generate/update the unified skill manifest that Claude Code can discover and read.

**Location:** `skills/meta/manifest-generator/`  
**Documentation:** [README](skills/meta/manifest-generator/README.md)  

#### Session Snapshot
Save session state snapshots with precise resume instructions for crash recovery or context clearing. Use when user says "save snapshot", "checkpoint progress", or before long/risky operations.

**Purpose:** Create recoverable session snapshots that capture task context, decisions, and progress. Enables precise resume after crashes, context clears, or multi-day breaks.

**Location:** `skills/meta/session-snapshot/`  
**Documentation:** [README](skills/meta/session-snapshot/README.md)  

#### Skill Extractor
Analyze extended Claude Code sessions to identify recurring workflows and extract them as reusable skills

**Purpose:** Analyze extended Claude Code sessions to identify recurring workflows and extract them into reusable skill definitions.

**Location:** `skills/meta/skill-extractor/`  
**Documentation:** [README](skills/meta/skill-extractor/README.md)  

#### Skill Recommendation Engine
Intelligent skill recommendation system that analyzes current context, user behavior, and project state to suggest the most useful Claude Code skills. Provides personalized, context-aware skill suggestions with usage predictions and confidence scores.

**Purpose:** Intelligently recommends the most useful Claude Code skills based on current context, project state, user behavior patterns, and skill utility analysis. Helps both users and agents discover relevant skills they might not know they need.

**Location:** `skills/meta/skill-recommendation-engine/`  
**Documentation:** [README](skills/meta/skill-recommendation-engine/README.md)  

#### Skill Upgrader
Systematically upgrade existing Claude Code skills to production quality with multi-language support, precise output, and comprehensive documentation. Use when improving substandard skills or adding missing features.

**Purpose:** Systematically upgrade existing Claude Code skills from basic/broken implementations to production-ready quality. Applies a proven pattern: multi-language detection, precise output formats, verification helpers, and comprehensive documentation.

**Location:** `skills/meta/skill-upgrader/`  
**Documentation:** [README](skills/meta/skill-upgrader/README.md)  

#### Startup Skill Showcase
Intuitive skill discovery and showcase system that presents your available Claude Code skills at startup, with special emphasis on meta-skills and useful workflows. Provides easy access to skill documentation and usage examples.

**Purpose:** Provides an intuitive, visually appealing showcase of all available Claude Code skills at startup, with special emphasis on meta-skills like session-snapshot, and organizes skills by usefulness and category for easy discovery by both users and agents.

**Location:** `skills/meta/startup-skill-showcase/`  
**Documentation:** [README](skills/meta/startup-skill-showcase/README.md)
<!-- SKILLS_INVENTORY_END -->
