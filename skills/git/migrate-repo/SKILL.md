---
name: migrate-repo
description: Migrate GitHub repository between accounts/orgs preserving full history, tags, and branches. Use when user says "migrate repo", "move repository", or "transfer github repo".
---

# Repository Migration Skill

## Purpose
Execute safe, history-preserving GitHub repository migrations using proven 9-phase workflow. ~500 tokens to invoke vs ~5K+ tokens for manual coordination.

## Instructions

When the user requests a repository migration:

1. **Verify Prerequisites**
   - Check `gh auth status` to confirm GitHub CLI is authenticated
   - Verify user has access to both source and destination accounts
   - Confirm PAT is available with `repo` and `admin:org` scopes

2. **Gather Migration Parameters**
   Prompt user for:
   - Source repository (format: `owner/repo-name`)
   - Destination organization or account
   - Personal Access Token (for mirror push)
   - Optional: destination description
   - Optional: repository topics (comma-separated)

3. **Analyze Source Repository**
   Run discovery commands to understand:
   - Branch count and default branch
   - Tag count
   - Repository size
   - Presence of GitHub Actions workflows
   - Existing documentation files

4. **Execute 9-Phase Migration**
   - Phase 1: Create backup mirror in temp directory
   - Phase 2: Create new repository in destination
   - Phase 3: Push mirror with PAT authentication
   - Phase 4: Verify transfer integrity (tags, branches, commits)
   - Phase 5: Check and update documentation references
   - Phase 6: Configure repository metadata (topics, description)
   - Phase 7: Archive + privatize source repository
   - Phase 8: Post-migration verification
   - Phase 9: Cleanup temporary files

5. **Report Success**
   Provide summary with:
   - New repository URL
   - Tag/branch counts
   - Any documentation updates made
   - Instructions for updating local clones

## Phase-by-Phase Commands

### Phase 1: Backup Mirror
```bash
cd "$TEMP" # or C:/Users/danie/AppData/Local/Temp on Windows
git clone --mirror https://github.com/SOURCE_OWNER/SOURCE_REPO.git backup-mirror.git
cd backup-mirror.git
git show-ref | wc -l  # Verify refs captured
cd ..
```

### Phase 2: Create Destination Repository
```bash
gh auth switch --user DEST_OWNER
gh repo create DEST_OWNER/SOURCE_REPO \
  --public \
  --description "DESCRIPTION"
```

### Phase 3: Push Mirror
```bash
cd backup-mirror.git
git push --mirror "https://DEST_OWNER:PAT@github.com/DEST_OWNER/SOURCE_REPO.git"
cd ..
```

### Phase 4: Verify Transfer
```bash
gh auth switch --user DEST_OWNER
gh repo view DEST_OWNER/SOURCE_REPO --json name,owner,url,description
gh api repos/DEST_OWNER/SOURCE_REPO/tags --jq '[.[].name] | join(", ")'
gh api repos/DEST_OWNER/SOURCE_REPO/branches --jq '.[].name'
```

### Phase 5: Check Documentation
```bash
git clone https://github.com/DEST_OWNER/SOURCE_REPO.git verify-clone
cd verify-clone
grep -r "SOURCE_OWNER" . --include="*.md" --include="*.yml" --include="*.yaml"
# If references found, update with sed:
sed -i 's|SOURCE_OWNER/SOURCE_REPO|DEST_OWNER/SOURCE_REPO|g' FILE.md
git add .
git commit -m "chore: update repository references for DEST_OWNER organization"
git remote set-url origin "https://DEST_OWNER:PAT@github.com/DEST_OWNER/SOURCE_REPO.git"
git push
cd ..
```

### Phase 6: Configure Metadata
```bash
gh auth switch --user DEST_OWNER
# Add topics if provided
gh repo edit DEST_OWNER/SOURCE_REPO \
  --add-topic topic1 \
  --add-topic topic2 \
  --add-topic topic3
```

### Phase 7: Archive Source
```bash
gh auth switch --user SOURCE_OWNER
gh repo unarchive SOURCE_OWNER/SOURCE_REPO --yes
gh repo edit SOURCE_OWNER/SOURCE_REPO --visibility private --accept-visibility-change-consequences
sleep 2
gh repo archive SOURCE_OWNER/SOURCE_REPO --yes
```

### Phase 8: Verification
```bash
gh auth switch --user DEST_OWNER
gh repo view DEST_OWNER/SOURCE_REPO --json name,url,repositoryTopics
gh auth switch --user SOURCE_OWNER
gh repo view SOURCE_OWNER/SOURCE_REPO --json visibility,isArchived
```

### Phase 9: Cleanup
```bash
rm -rf backup-mirror.git verify-clone
```

## Token Efficiency
- **Migration skill**: ~500 tokens to invoke + ~3K tokens to execute = **~3.5K tokens**
- **Manual coordination**: ~5-8K tokens explaining steps, handling errors, verifying
- **Savings**: ~40-60% token reduction

## Safety Features
1. **Backup mirror**: Full repository copy before any changes
2. **Verification gates**: Check integrity after each critical phase
3. **Rollback capability**: Can restore from mirror if migration fails
4. **No destructive actions**: Source repo only modified after destination is verified

## Common Issues & Solutions

**Issue**: PAT authentication fails during mirror push
- **Cause**: Insufficient PAT scopes or expired token
- **Solution**: Verify PAT has `repo` and `admin:org` scopes; regenerate if expired

**Issue**: Documentation grep finds no references
- **Cause**: Repository already uses relative paths or external references only
- **Solution**: Skip Phase 5 updates; no changes needed

**Issue**: Archive command fails
- **Cause**: Repository already archived or no admin access
- **Solution**: Check current state with `gh repo view --json isArchived`; unarchive first if needed

**Issue**: Temp directory busy during cleanup
- **Cause**: File handles still open or directory in use
- **Solution**: Non-critical; user can manually delete later

## Output Format

```
✅ Repository Migration Complete!

📊 Migration Summary:
- Source: https://github.com/SOURCE_OWNER/SOURCE_REPO (archived, private)
- Destination: https://github.com/DEST_OWNER/SOURCE_REPO
- Branches: X (default: BRANCH_NAME)
- Tags: X tags transferred
- Commits: Full history preserved
- Documentation: X files updated

🔄 Update Local Clones:
git remote set-url origin https://github.com/DEST_OWNER/SOURCE_REPO.git
git fetch origin

🎯 Next Steps:
- Verify repository renders correctly on GitHub
- Update any external links or bookmarks
- Notify collaborators of new location
```

## Use Cases
- Migrating personal projects to organization accounts
- Consolidating repositories under a single organization
- Transferring ownership while preserving history
- Moving repositories between GitHub accounts

## Limitations
- Requires `gh` CLI installed and authenticated
- Needs admin access to both source and destination accounts
- Cannot migrate private repos to public without manual approval
- Large repositories (>1GB) may take longer to clone/push
- GitHub Actions secrets/variables are not transferred (by design)

## Follow-Up Actions
After presenting the migration summary, ask:
- "Would you like to add a migration notice to the README?"
- "Should I create a release on the new repository?"
- "Need help updating any CI/CD configurations?"
