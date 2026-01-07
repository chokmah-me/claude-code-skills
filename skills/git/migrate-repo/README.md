# migrate-repo Skill - Usage Guide

## Overview

The `migrate-repo` skill automates GitHub repository migration between accounts or organizations while preserving complete history, tags, branches, and metadata.

**Token Efficiency**: ~3.5K tokens vs ~5-8K manual coordination (40-60% reduction)

## Quick Start

### Option 1: Natural Language Invocation (Recommended)

Simply tell Claude what you want to migrate:

```
"Migrate the dyb5784/my-awesome-project repository to chokmah-me"
```

Claude will automatically use the migrate-repo skill and guide you through the process.

### Option 2: Direct Skill Invocation

```bash
claude skills migrate-repo
```

Then follow the interactive prompts.

### Option 3: Manual Execution

Read the SKILL.md file and execute the 9 phases step-by-step.

## Prerequisites

Before starting a migration, ensure you have:

1. **GitHub CLI installed and authenticated**
   ```bash
   gh auth status
   ```

2. **Access to both accounts**
   - Source account (where repo currently lives)
   - Destination account (where repo will move)

3. **Personal Access Token (PAT)**
   - Scopes required: `repo`, `admin:org`
   - Generate at: https://github.com/settings/tokens

4. **Admin permissions**
   - Admin access on source repository
   - Ability to create repos in destination org/account

## Migration Process

The skill executes 9 phases automatically:

### Phase 1: Backup Mirror
Creates a complete mirror clone in your temp directory as a safety net.

### Phase 2: Create Destination Repository
Creates a new empty repository at the destination with your specified settings.

### Phase 3: Push Mirror
Pushes all branches, tags, and commit history to the new repository using your PAT.

### Phase 4: Verify Transfer
Confirms all tags, branches, and commits transferred successfully.

### Phase 5: Update Documentation
Searches for and updates any hardcoded repository references in documentation files.

### Phase 6: Configure Metadata
Applies repository description and topics (labels) to the new repository.

### Phase 7: Archive Source
Makes the old repository private and archives it (read-only) to prevent confusion.

### Phase 8: Final Verification
Double-checks both source and destination repositories are in the correct state.

### Phase 9: Cleanup
Removes temporary files and directories created during migration.

## Interactive Parameters

When you invoke the skill, Claude will prompt you for:

1. **Source Repository**
   - Format: `owner/repo-name`
   - Example: `dyb5784/claude-code-playbook`

2. **Destination Organization/Account**
   - Format: `username` or `org-name`
   - Example: `chokmah-me`

3. **Personal Access Token**
   - Your GitHub PAT with `repo` and `admin:org` scopes
   - Example: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

4. **Repository Description** (Optional)
   - Brief description for the new repository
   - Example: "AI development toolkit for Claude Code"

5. **Repository Topics** (Optional)
   - Comma-separated list of topics
   - Example: "ai-development,claude,developer-tools"

## Example Migration Session

```
User: Migrate dyb5784/roo-kimi-playbook to chokmah-me

Claude: I'll help you migrate that repository. Let me gather the details:

📋 Migration Parameters:
- Source: dyb5784/roo-kimi-playbook
- Destination Org: chokmah-me
- I'll need your PAT for the mirror push

[Claude prompts for PAT and optional parameters]

🔍 Analyzing source repository...
- Branches: 1 (master)
- Tags: 2 (v4.1.0, v4.1.3)
- Size: ~3.1 MB

⚙️ Executing 9-Phase Migration...

Phase 1: Creating backup mirror... ✓
Phase 2: Creating destination repository... ✓
Phase 3: Pushing mirror... ✓
Phase 4: Verifying transfer... ✓
Phase 5: Checking documentation... ✓
Phase 6: Configuring metadata... ✓
Phase 7: Archiving source repository... ✓
Phase 8: Final verification... ✓
Phase 9: Cleanup... ✓

✅ Repository Migration Complete!

📊 Migration Summary:
- Source: https://github.com/dyb5784/roo-kimi-playbook (archived, private)
- Destination: https://github.com/chokmah-me/roo-kimi-playbook
- Branches: 1 (default: master)
- Tags: 2 tags transferred (v4.1.0, v4.1.3)
- Commits: Full history preserved (13 commits)
- Documentation: 3 files updated

🔄 Update Local Clones:
git remote set-url origin https://github.com/chokmah-me/roo-kimi-playbook.git
git fetch origin
```

## Safety Features

1. **Backup First**: Full mirror created before any modifications
2. **Verification Gates**: Every critical phase is verified before proceeding
3. **Rollback Capability**: Can restore from backup if anything fails
4. **No Premature Destruction**: Source repo only modified after destination is verified
5. **Archive, Don't Delete**: Old repo kept private and archived (not deleted)

## Common Scenarios

### Scenario 1: Personal → Organization
Moving your personal projects to a company/team organization.

```
Source: yourname/personal-project
Destination: company-org
```

### Scenario 2: Organization → Organization
Consolidating repositories under a single organization.

```
Source: old-org/legacy-project
Destination: new-org
```

### Scenario 3: Account Transfer
Moving repos between your own GitHub accounts.

```
Source: old-account/my-repo
Destination: new-account
```

## Troubleshooting

### PAT Authentication Fails

**Error**: `remote: Invalid username or password`

**Solution**:
1. Verify PAT has `repo` and `admin:org` scopes
2. Check PAT hasn't expired
3. Regenerate PAT if needed: https://github.com/settings/tokens

### Documentation Updates Skip

**Message**: `No references found`

**Explanation**: Your repository uses relative paths or external references only. This is fine - skip Phase 5.

### Archive Command Fails

**Error**: `cannot archive repository`

**Solution**:
```bash
# Check current state
gh repo view SOURCE_OWNER/SOURCE_REPO --json isArchived

# If already archived, unarchive first
gh repo unarchive SOURCE_OWNER/SOURCE_REPO --yes
```

### Cleanup Directory Busy

**Error**: `cannot remove directory: Device or resource busy`

**Solution**: Non-critical. Manually delete later:
```bash
cd C:/Users/danie/AppData/Local/Temp
rm -rf backup-mirror.git verify-clone
```

## What Gets Migrated

✅ **Transferred**:
- All commits (complete history)
- All branches
- All tags and releases
- Repository description
- Repository topics/labels
- All files (including large files)

❌ **Not Transferred** (by design):
- GitHub Actions secrets
- GitHub Actions variables
- Collaborator permissions
- Issue/PR history
- Watchers/Stars/Forks counts
- Webhooks

## Security Notes

1. **PAT Handling**: PAT is only embedded in URL for mirror push (Phase 3). All other operations use `gh auth`.

2. **PAT in History**: The PAT appears in bash history. Clear after migration:
   ```bash
   history -c  # Clear current session
   ```

3. **PAT Exposure**: Never commit your PAT to any repository. The skill uses it transiently in URLs.

4. **Source Privacy**: Old repository is automatically made private to prevent public exposure after migration.

## Post-Migration Checklist

After successful migration:

- [ ] Verify new repository renders correctly on GitHub
- [ ] Check all tags are present
- [ ] Verify default branch is correct
- [ ] Update any CI/CD configurations with new repo URL
- [ ] Update external links (documentation, websites)
- [ ] Notify team members of new location
- [ ] Update local clones:
  ```bash
  git remote set-url origin https://github.com/NEW_OWNER/REPO.git
  git fetch origin
  ```
- [ ] Consider adding migration notice to README
- [ ] Update bookmarks/favorites

## Advanced Usage

### Dry Run (Analysis Only)

To analyze a repository without migrating:

```bash
# Check repository details
gh repo view OWNER/REPO --json name,description,defaultBranchRef,diskUsage

# Check tags
gh api repos/OWNER/REPO/tags --jq '[.[].name] | join(", ")'

# Check branches
gh api repos/OWNER/REPO/branches --jq '.[].name'
```

### Rollback After Failed Migration

If migration fails mid-process:

```bash
# Navigate to backup
cd C:/Users/danie/AppData/Local/Temp/backup-mirror.git

# Delete failed destination repo
gh repo delete DEST_OWNER/REPO --yes

# Restore to source (if source was modified)
git push --mirror https://github.com/SOURCE_OWNER/REPO.git
```

### Migrate to Different Repo Name

The skill preserves the original repo name. To migrate with a new name:

1. Complete migration with original name
2. Rename on GitHub:
   ```bash
   gh repo rename NEW_NAME --repo DEST_OWNER/OLD_NAME
   ```

## Best Practices

1. **Test with small repos first**: Get familiar with the process using a test repository.

2. **Migration window**: Plan migrations during low-traffic periods if the repo has active users.

3. **Notify collaborators**: Warn team members before migrating to minimize disruption.

4. **Document the move**: Add a migration notice to README with instructions for updating remotes.

5. **Keep PAT secure**: Generate a temporary PAT for migration, revoke after completion.

6. **Verify thoroughly**: Don't delete old repo until you've verified new one completely.

## Migration Size Estimates

| Repo Size | Migration Time |
|-----------|---------------|
| < 100 MB  | 5-10 minutes  |
| 100-500 MB| 10-20 minutes |
| 500 MB-1 GB| 20-30 minutes|
| > 1 GB    | 30+ minutes   |

*Times assume good network connectivity*

## Success Criteria

A successful migration has:

- ✅ All branches transferred
- ✅ All tags/releases present
- ✅ Commit history intact (compare count: `git log --oneline | wc -l`)
- ✅ Documentation references updated
- ✅ Repository metadata configured
- ✅ Source repository archived and private
- ✅ No broken links in new repository

## Getting Help

If you encounter issues not covered here:

1. Check the Common Issues section in SKILL.md
2. Verify prerequisites (gh auth, PAT scopes)
3. Review bash command output for specific errors
4. Ask Claude for help: "I'm getting [error] during migration phase [X]"

## Version History

- **v1.0** (2026-01-06): Initial release based on proven migration patterns

## License

This skill is part of the Claude Code skills system and follows the same license as your project.

---

**Ready to migrate?** Just tell Claude: "Migrate [source-repo] to [destination]" and let the skill handle the rest!
