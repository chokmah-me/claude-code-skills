---
name: session-snapshot
description: Save session state snapshots with precise resume instructions for crash recovery or context clearing. Use when user says "save snapshot", "checkpoint progress", or before long/risky operations.
---

# Session Snapshot Skill

## 🎯 Purpose
Create recoverable session snapshots that capture task context, decisions, and progress. Enables precise resume after crashes, context clears, or multi-day breaks.

## 🚀 Key Features

- **Session recovery**: Capture task context, decisions, and progress for precise resume after crashes or breaks
- **Token efficiency**: ~1500 tokens total vs 10k+ for restart (85% reduction)
- **Multi-level resume**: Quick resume (context intact), cold resume (new session), recovery from failure
- **Git integration**: Automatic .gitignore handling, commit SHA tracking
- **Rolling snapshot history**: Automatically maintains last 5 snapshots with timestamped files, auto-cleanup of older snapshots
- **Multiple snapshots**: Named snapshots for parallel tasks with independent rolling windows (`.session-snapshot-[name]-YYYYMMDD-HHMMSS.md`)
- **Clear resume workflow**: Step-by-step instructions for rebuilding context

## 📋 Usage

**When to use**:
- Before risky operations (major refactors, schema changes)
- Every 15-20 messages in long sessions
- User says: "save checkpoint", "snapshot state", "save progress"
- Before `/clear` or ending session
- Multi-day projects (save at end of each session)

### Instructions

### Step 1: Capture Session State

Extract current session information:

**Required fields**:
- `timestamp` - Current date/time
- `task_summary` - 1-line description of overall goal
- `current_phase` - Specific step in progress
- `files_modified` - List with line ranges or "new file"
- `files_read` - Context files examined
- `next_steps` - Ordered todo list (markdown checkboxes)

**Optional fields**:
- `decisions_made` - Key architectural choices
- `context_preservation` - Important background (≤200 words)
- `blockers` - Current issues preventing progress
- `test_status` - Pass/fail state
- `commit_sha` - Git commit before changes (if applicable)

### Step 2a: Auto-cleanup Old Snapshots

Before creating a new snapshot, clean up old ones to maintain rolling 5-snapshot window:

**For default snapshots:**

```bash
# Define snapshot pattern
SNAPSHOT_PATTERN=".session-snapshot-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9].md"

# Count existing snapshots
SNAPSHOT_COUNT=$(ls -1 ${SNAPSHOT_PATTERN} 2>/dev/null | wc -l)

# If >= 5, delete oldest to make room
if [ "$SNAPSHOT_COUNT" -ge 5 ]; then
  OLDEST=$(ls -1t ${SNAPSHOT_PATTERN} | tail -1)
  rm -f "${OLDEST}"
  echo "🗑️ Cleaned up 1 old snapshot (keeping 5 most recent)"
fi
```

**For named snapshots** (e.g., `snapshot_name="feature-auth"`):

```bash
# Define named snapshot pattern
SNAPSHOT_PATTERN=".session-snapshot-${snapshot_name}-[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9][0-9][0-9].md"

# Count and cleanup (same logic as above)
SNAPSHOT_COUNT=$(ls -1 ${SNAPSHOT_PATTERN} 2>/dev/null | wc -l)
if [ "$SNAPSHOT_COUNT" -ge 5 ]; then
  OLDEST=$(ls -1t ${SNAPSHOT_PATTERN} | tail -1)
  rm -f "${OLDEST}"
fi
```

### Step 2b: Generate Timestamped Snapshot File

Create timestamped snapshot in project root:

```bash
# Generate timestamp (UTC)
TIMESTAMP=$(date -u +"%Y%m%d-%H%M%S")

# Create filename
SNAPSHOT_FILE=".session-snapshot-${TIMESTAMP}.md"
# OR for named: SNAPSHOT_FILE=".session-snapshot-${snapshot_name}-${TIMESTAMP}.md"
```

Write snapshot content:

```markdown
# Session Snapshot

**Timestamp**: YYYY-MM-DDTHH:MM:SSZ
**Task**: [1-line summary]
**Phase**: [current step]

## Context

[2-4 sentences explaining what we're doing and why]

## Decisions Made

- [Key decision 1 with rationale]
- [Key decision 2 with rationale]

## Files Modified

- `path/to/file.py` (lines 20-150: extracted GraphTopology)
- `path/to/new_file.py` (new file: GraphTopology class)
- `tests/test_file.py` (lines 45-60: updated tests)

## Files Read (Context)

- `path/to/related.py` (understanding BaseAgent interface)
- `CLAUDE.md` (architectural constraints)

## Current State

**Test status**: ✅ All passing | ⚠️ 3 failing | ❌ Not run
**Git status**: Clean | Uncommitted changes | Staged changes
**Commit SHA**: abc123def (before modifications)

## Next Steps

- [ ] Update imports in network.py:25
- [ ] Run `pytest tests/test_network.py -v`
- [ ] Fix failing test_topology_creation
- [ ] Commit with message: "refactor: extract GraphTopology from NetworkEnvironment"

## Blockers

- [Issue 1]: [description and potential solution]
- [Issue 2]: [description and potential solution]

## Resume Instructions

### Quick Resume (if context intact)
```
Continue with next step: Update imports in network.py:25
```

### Cold Resume (new session/cleared context)
```
1. View most recent snapshot: cat $(ls -t .session-snapshot-*.md | head -1)
2. Read files in "Files Modified" to see current changes
3. Read files in "Files Read" for context
4. Check test status: pytest tests/test_network.py -v
5. Continue from "Next Steps" checklist
```

### Recovery from Failure
```
If changes broke something:
1. Check git status
2. Compare to commit SHA: git diff abc123def
3. Consider: git reset --hard abc123def (CAUTION: loses changes)
4. Review "Decisions Made" to understand approach
5. Try alternative approach or ask for guidance
```

---
*Generated by session-snapshot skill on YYYY-MM-DD*
*Snapshot: [N/5] in rolling window*
```

### Step 3: Update .gitignore

Ensure snapshots are not committed:

```bash
# Check if .gitignore exists and add pattern for all timestamped snapshots
if ! grep -q ".session-snapshot-.*\.md" .gitignore 2>/dev/null; then
  echo "" >> .gitignore
  echo "# Claude Code session snapshots (timestamped, auto-rotated)" >> .gitignore
  echo ".session-snapshot-*.md" >> .gitignore
fi
```

### Step 4: Confirm to User

Show brief confirmation with timestamp and snapshot count:

```markdown
✅ **Session snapshot saved**: `.session-snapshot-YYYYMMDD-HHMMSS.md`

**Snapshot**: 3/5 (rolling window)
**Task**: [summary]
**Phase**: [current]
**Next**: [first uncompleted todo]

**Resume command**:
- Same session: "Continue from snapshot"
- New session: "Read the most recent snapshot and continue"
- View all snapshots: `ls -lt .session-snapshot-*.md`
```

## Resume Workflow

When user returns after break/crash/clear:

### Step 0: List Available Snapshots

View your snapshot history (most recent first):

```bash
# All snapshots
ls -lt .session-snapshot-*.md

# Snapshots for specific task (e.g., "feature-auth")
ls -lt .session-snapshot-feature-auth-*.md

# View most recent snapshot
cat $(ls -t .session-snapshot-*.md | head -1)

# View specific older snapshot
cat .session-snapshot-20260107-120000.md
```

### Step 1: Load Snapshot

```bash
# Load most recent snapshot
cat $(ls -t .session-snapshot-*.md | head -1)

# OR load specific snapshot by timestamp
cat .session-snapshot-YYYYMMDD-HHMMSS.md
```

### Step 2: Validate State

Check if project state matches snapshot:

```bash
# Compare modified files
git status

# Check test status
pytest tests/ -v --tb=no -q

# Verify snapshot commit (if recorded)
git log --oneline -5
```

### Step 3: Rebuild Context

Read the exact files listed in snapshot:
- Files Modified: See what changed
- Files Read: Rebuild context understanding

### Step 4: Continue Execution

Pick up from "Next Steps" checklist. Mark completed items and proceed.

## 🎛️ Parameters

**None required** - The skill auto-captures session state from current context.

**Automatic timestamping**:
- **Default**: `.session-snapshot-YYYYMMDD-HHMMSS.md` (e.g., `.session-snapshot-20260115-143022.md`)
- **Named**: `.session-snapshot-[name]-YYYYMMDD-HHMMSS.md` (e.g., `.session-snapshot-feature-auth-20260115-143022.md`)
- **Rolling window**: Automatically keeps 5 most recent snapshots per namespace
- **Auto-cleanup**: Oldest snapshots deleted when 6th snapshot created

**Captured fields**:
- **Required**: timestamp, task_summary, current_phase, files_modified, files_read, next_steps
- **Optional**: decisions_made, context_preservation, blockers, test_status, commit_sha

## Anti-Patterns

❌ Don't snapshot every 2-3 messages (too frequent)
❌ Don't capture entire file contents (link to lines instead)
❌ Don't write verbose context (≤200 words)
❌ Don't skip "Next Steps" - crucial for resume

✅ Do snapshot before risky changes
✅ Do capture architectural decisions
✅ Do list specific file:line references
✅ Do provide clear resume instructions

## Token Efficiency

- Snapshot creation: ~400 tokens
- Snapshot file size: ~500-800 tokens
- Resume from cold start: ~600 tokens
- Total cost: ~1500 tokens (vs. restarting from scratch: 10k+ tokens)

## 📂 Snapshot History Management

### Automatic Rolling Window

- **Window size**: 5 snapshots per namespace
- **Cleanup trigger**: When creating 6th snapshot
- **Cleanup target**: Oldest snapshot(s) by modification time
- **Namespace isolation**: Default and each named snapshot maintain separate windows

### Listing Snapshots

```bash
# All snapshots (most recent first)
ls -lt .session-snapshot-*.md

# Specific namespace (e.g., "feature-auth")
ls -lt .session-snapshot-feature-auth-*.md

# Count snapshots
ls -1 .session-snapshot-*.md | wc -l

# View most recent snapshot
cat $(ls -t .session-snapshot-*.md | head -1)

# View specific older snapshot
cat .session-snapshot-20260110-120000.md
```

### Manual Cleanup

```bash
# Delete all snapshots (caution!)
rm .session-snapshot-*.md

# Delete specific namespace
rm .session-snapshot-feature-auth-*.md

# Keep only N most recent (e.g., 3 instead of 5)
ls -1t .session-snapshot-*.md | tail -n +4 | xargs rm -f
```

### Snapshot Archival

To preserve snapshots beyond the 5-window:

```bash
# Create archive directory
mkdir -p .snapshot-archive

# Move old snapshots to archive
mv .session-snapshot-20260110-*.md .snapshot-archive/

# Archive is not auto-cleaned (manual management only)
ls -lt .snapshot-archive/.session-snapshot-*.md
```

## 💡 Examples

### Example 1: Refactoring Session

**Trigger**:
```
User: We're about to extract GraphTopology from NetworkEnvironment. Save a snapshot first.
```

**Execution**:
1. Auto-cleanup: Check for existing snapshots (0 found, no cleanup needed)
2. Generate timestamp: 20260115-143022
3. Capture current state (clean git, tests passing)
4. Record decision: "Use composition over inheritance"
5. List files to modify: network.py, new graph_topology.py
6. Create .session-snapshot-20260115-143022.md with all context
7. Update .gitignore pattern

**Output**:
```
✅ Session snapshot saved: .session-snapshot-20260115-143022.md

Snapshot: 1/5 (rolling window)
Task: Extract GraphTopology component from NetworkEnvironment
Phase: Pre-refactoring checkpoint
Next: Create src/acp_simulation/environment/graph_topology.py

Resume: "Read the most recent snapshot and continue"
View all: `ls -lt .session-snapshot-*.md`
```

### Example 2: Resume After Crash

**Trigger**:
```
User: My session crashed. Read the most recent snapshot and continue.
```

**Execution**:
1. List snapshots: `ls -lt .session-snapshot-*.md` (shows 20260115-143022, 20260115-110530, 20260114-153422)
2. Load most recent: `cat $(ls -t .session-snapshot-*.md | head -1)`
3. Check git status (sees modified network.py)
4. Read network.py:20-150 to see partial extraction
5. Run tests → 3 failing
6. Review "Decisions Made" and "Blockers"
7. Continue from "Next Steps" checklist

**Output**:
```
📋 Resuming from snapshot (2026-01-15 14:30)

Snapshot: .session-snapshot-20260115-143022.md (3/5)
Task: Extract GraphTopology component
Progress: GraphTopology class created, imports partially updated
Tests: ⚠️ 3 failing (test_topology_creation, test_get_neighbors, test_graph_properties)

Next step: Fix failing tests by updating NetworkEnvironment imports

Continuing...
```

### Example 3: Multi-Day Project

**Day 1 End** (2026-01-06 17:30):
```
User: Save checkpoint before I leave for today.

Claude: ✅ Session snapshot saved: .session-snapshot-20260106-173000.md

Snapshot: 1/5
Task: Add enterprise topology support (hub-spoke, hierarchical)
Phase: Completed hub-spoke, starting hierarchical
Next: Implement hierarchical topology generator
```

**Day 2 Start** (2026-01-07 09:00):
```
User: Read the most recent snapshot and continue where we left off.

Claude: 📋 Resuming from snapshot (2026-01-07 09:00)

Available snapshots:
  .session-snapshot-20260107-090000.md (most recent, today)
  .session-snapshot-20260106-173000.md (yesterday)
  .session-snapshot-20260106-143500.md (2 days ago)

Loaded: .session-snapshot-20260106-173000.md
- Completed: Hub-spoke topology with gradient vulnerability
- Today: Implementing hierarchical topology (DMZ/internal/endpoints)
- Tests: All passing before hierarchical addition

Starting hierarchical implementation...
```

### Example 4: Parallel Task Snapshots with Independent Windows

**Trigger**:
```
User: I'm working on authentication and a bug fix in parallel. Save separate snapshots.
```

**Execution**:
Create named snapshots with independent rolling windows:
1. Auto-cleanup: Check `.session-snapshot-feature-auth-*.md` (0 found, no cleanup)
2. Create: `.session-snapshot-feature-auth-20260115-140000.md`
3. Auto-cleanup: Check `.session-snapshot-bugfix-race-*.md` (0 found, no cleanup)
4. Create: `.session-snapshot-bugfix-race-20260115-142000.md`

**Output**:
```
✅ **Snapshots saved** (independent rolling windows):

**Auth feature**:
- `.session-snapshot-feature-auth-20260115-140000.md` (Snapshot 1/5)
- Resume: `cat $(ls -t .session-snapshot-feature-auth-*.md | head -1)`

**Bug fix**:
- `.session-snapshot-bugfix-race-20260115-142000.md` (Snapshot 1/5)
- Resume: `cat $(ls -t .session-snapshot-bugfix-race-*.md | head -1)`

Each namespace maintains separate 5-snapshot window
```

### Example 5: Automatic Rolling Window Cleanup

**Scenario**: User saves 6th snapshot, triggering auto-cleanup

**Execution**:
1. Before snapshot 6: `ls .session-snapshot-*.md` shows 5 files
   - `.session-snapshot-20260110-120000.md` (oldest)
   - `.session-snapshot-20260111-140000.md`
   - `.session-snapshot-20260112-100000.md`
   - `.session-snapshot-20260114-160000.md`
   - `.session-snapshot-20260115-090000.md` (newest)
2. Auto-cleanup identifies oldest by timestamp: `20260110-120000`
3. Delete oldest: `rm .session-snapshot-20260110-120000.md`
4. Create snapshot 6: `.session-snapshot-20260115-143022.md`
5. Result: Still 5 snapshots, oldest is now `20260111-140000`

**Output**:
```
🗑️ Cleaned up 1 old snapshot (keeping 5 most recent)
✅ Session snapshot saved: .session-snapshot-20260115-143022.md

Snapshot: 5/5 (rolling window full)
Task: Extract GraphTopology component
Phase: Post-refactoring validation
Next: Run full test suite and create PR

Resume: "Read the most recent snapshot and continue"
```

**Listing snapshots after cleanup**:
```
$ ls -lt .session-snapshot-*.md
.session-snapshot-20260115-143022.md  (most recent - just created)
.session-snapshot-20260115-090000.md
.session-snapshot-20260114-160000.md
.session-snapshot-20260112-100000.md
.session-snapshot-20260111-140000.md  (oldest - 20260110 was auto-deleted)
```

## 🎁 Output

### Snapshot File Structure

Creates timestamped snapshot in project root (e.g., `.session-snapshot-20260115-143022.md`):

```markdown
# Session Snapshot

**Timestamp**: 2026-01-15T14:30:00Z
**Task**: Extract GraphTopology component from NetworkEnvironment
**Phase**: Pre-refactoring checkpoint

## Context
We're extracting the graph topology logic from NetworkEnvironment into a separate GraphTopology class to improve modularity and testability.

## Decisions Made
- Use composition over inheritance for topology management
- Keep existing API surface for backward compatibility

## Files Modified
- `src/network.py` (lines 20-150: extracted GraphTopology)
- `src/graph_topology.py` (new file: GraphTopology class)
- `tests/test_network.py` (lines 45-60: updated tests)

## Next Steps
- [ ] Update imports in network.py:25
- [ ] Run `pytest tests/test_network.py -v`
- [ ] Commit with message: "refactor: extract GraphTopology"

## Resume Instructions
### Quick Resume: Continue with next step: Update imports
### Cold Resume: Read this file, check git status, run tests, continue from checklist
```

### Confirmation Message

Shows brief confirmation with timestamp and snapshot count:

```
✅ **Session snapshot saved**: `.session-snapshot-20260115-143022.md`

**Snapshot**: 3/5 (rolling window)
**Task**: Extract GraphTopology component
**Phase**: Pre-refactoring checkpoint
**Next**: Update imports in network.py:25

**Resume**: "Read the most recent snapshot and continue"
**List all**: `ls -lt .session-snapshot-*.md`
```

## Integration with Other Skills

**Before major refactoring**:
```
1. /session-snapshot (save state)
2. /refactoring (do the work)
3. /session-snapshot (save after completion)
```

**During long sessions**:
```
Every ~15 messages: Auto-suggest snapshot if user hasn't saved
```

**With git workflows**:
```
1. /session-snapshot (capture clean state)
2. Make changes
3. /diff-summariser (review changes)
4. Commit
5. /session-snapshot (update to new baseline)
```

## ⚠️ Important Notes

- Snapshots are **local only** (.gitignore'd with pattern `.session-snapshot-*.md`)
- **Timestamped files**: All snapshots use format `.session-snapshot-YYYYMMDD-HHMMSS.md`
- **Rolling window**: Each namespace (default or named) independently maintains 5 snapshots
- **Auto-cleanup**: Oldest snapshots automatically deleted when 6th snapshot created
- **Archive old snapshots**: Move to `.snapshot-archive/` directory to preserve beyond 5-window
- For team sharing: Remove .gitignore and commit snapshots deliberately
- Claude can auto-detect when to suggest snapshots (long sessions, risky ops)
- **Cross-platform**: Bash commands require bash environment (Git Bash on Windows, native on macOS/Linux)
- **Windows users**: Use Git Bash or WSL for timestamp generation and auto-cleanup; can create snapshots manually if needed

## Related Skills

- `meta/skill-extractor` - Extract workflow patterns into new skills
- `git/diff-summariser` - Review changes before snapshot
- `development/refactoring` - Major changes that need checkpoints
- `git/repo-briefing` - Initial project context (complement to snapshots)
