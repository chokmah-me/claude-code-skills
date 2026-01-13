---
name: matarao
description: Publish and manage blog posts on Mataroa via API. Create, update, and retrieve posts from URLs or local files. Use when user says "publish to mataroa", "update blog post", or "fetch mataroa post".
---

# matarao

## 🎯 Purpose
Manage Mataroa blog posts directly from Claude Code without leaving your terminal. Publish from local markdown files or URLs, update existing posts, and retrieve content for editing (~700 tokens per operation vs 3000+ manual).

## 🚀 Key Features
- **Create posts** from local markdown files or remote URLs
- **Update existing posts** with new content or metadata
- **Retrieve posts** to review or edit locally
- **Secure authentication** via JSON config file
- **No rate limiting** - unlimited API calls to Mataroa

## 📋 Usage

### Prerequisites
Create config file at `~/.claude/matarao-config.json`:
```json
{
  "api_key": "your-mataroa-api-key-here",
  "base_url": "https://mataroa.blog/api/"
}
```

Get your API key from: https://mataroa.blog/api/docs/

### Basic Operations

**Create post from local file**:
```bash
title="My New Post" && \
body=$(cat path/to/post.md) && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X POST https://mataroa.blog/api/posts/ \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"$title\",\"body\":\"$body\"}"
```

**Create post from URL**:
```bash
title="Remote Article" && \
body=$(curl -s https://example.com/article.md) && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X POST https://mataroa.blog/api/posts/ \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"$title\",\"body\":\"$body\"}"
```

**Get single post**:
```bash
slug="my-post-slug" && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X GET "https://mataroa.blog/api/posts/$slug/" \
  -H "Authorization: Bearer $api_key"
```

**Update post**:
```bash
slug="my-post-slug" && \
new_body=$(cat updated-post.md) && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X PATCH "https://mataroa.blog/api/posts/$slug/" \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"body\":\"$new_body\"}"
```

## 🎛️ Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes (create) | Post title for new posts |
| body | string | No | Post content (markdown supported) |
| slug | string | Yes (get/update) | Post URL slug identifier |
| published_at | ISO date | No | Publication timestamp (ISO 8601 format, e.g. "2026-01-13") |
| source | path/URL | Yes | Local file path or remote URL for content |

## 💡 Examples

### Example 1: Publish Local Markdown File
```bash
# Create a new post from existing markdown
title="Getting Started with Claude Code" && \
body=$(cat blog/getting-started.md) && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X POST https://mataroa.blog/api/posts/ \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"$title\",\"body\":\"$body\"}"

# Expected output:
{
  "ok": true,
  "slug": "getting-started-with-claude-code",
  "url": "https://yourblog.mataroa.blog/blog/getting-started-with-claude-code/"
}
```

### Example 2: Fetch and Publish from URL
```bash
# Fetch content from remote URL and publish
title="Remote Article" && \
body=$(curl -s https://raw.githubusercontent.com/user/repo/main/article.md) && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X POST https://mataroa.blog/api/posts/ \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"$title\",\"body\":\"$body\"}"

# Use case: Publish documentation from your repository
```

### Example 3: Update Existing Post
```bash
# Make edits locally, then update on Mataroa
slug="getting-started-with-claude-code" && \
updated_content=$(cat blog/getting-started-v2.md) && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X PATCH "https://mataroa.blog/api/posts/$slug/" \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"body\":\"$updated_content\",\"title\":\"Getting Started with Claude Code (Updated)\"}"
```

### Example 4: Retrieve Post for Local Editing
```bash
# Download post to edit locally
slug="my-post" && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X GET "https://mataroa.blog/api/posts/$slug/" \
  -H "Authorization: Bearer $api_key" | jq -r '.body' > local-edit.md

# Edit local-edit.md, then update:
updated=$(cat local-edit.md) && \
curl -X PATCH "https://mataroa.blog/api/posts/$slug/" \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"body\":\"$updated\"}"
```

### Example 5: Schedule Publication
```bash
# Create post with specific publication timestamp
title="Future Post" && \
body=$(cat draft.md) && \
publish_date="2026-02-01" && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X POST https://mataroa.blog/api/posts/ \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"$title\",\"body\":\"$body\",\"published_at\":\"$publish_date\"}"

# Note: Leave published_at empty to unpublish/create draft
```

## 🎁 Output

All API responses include:
- `ok`: true/false success indicator
- `slug`: Post URL identifier
- `title`: Post title
- `body`: Full post content
- `published_at`: Publication timestamp (null for drafts)
- `url`: Full public URL to post

### Success Response Example
```json
{
  "ok": true,
  "slug": "my-post-title",
  "title": "My Post Title",
  "body": "Full markdown content...",
  "published_at": "2026-01-13",
  "url": "https://yourblog.mataroa.blog/blog/my-post-title/"
}
```

### Error Response Example
```json
{
  "ok": false,
  "error": "Authentication failed"
}
```

## ⚠️ Important Notes

- **Config file required**: Create `~/.claude/matarao-config.json` before first use
- **API key security**: Never commit config file to git (add to .gitignore)
- **Trailing slashes**: All Mataroa API endpoints MUST end with `/` (API requirement)
- **Content-Type header**: Must be `application/json` for all requests
- **No rate limiting**: Mataroa API has no rate limits
- **Slug uniqueness**: Post slugs auto-generated from title, must be unique per blog
- **Unpublishing**: Set `published_at` to empty string to unpublish post
- **JSON escaping**: Special characters in content must be properly escaped
- **jq dependency**: Requires `jq` command-line tool for JSON parsing (install via package manager)

### Error Handling

**Missing config file**:
```bash
# Check if config exists
if [ ! -f ~/.claude/matarao-config.json ]; then
  echo "Error: Config file not found. Create ~/.claude/matarao-config.json"
  exit 1
fi
```

**Invalid API key**:
```
HTTP 401: Check your API key in ~/.claude/matarao-config.json
```

**Network errors**:
```bash
# Add timeout and retry logic
curl --max-time 30 --retry 3 --retry-delay 2 ...
```

**File not found**:
```bash
# Validate file exists before reading
if [ ! -f "path/to/post.md" ]; then
  echo "Error: File not found: path/to/post.md"
  exit 1
fi
```

## 🔄 Integration with Other Skills

### With session-snapshot
```bash
# Save checkpoint before bulk publishing
/session-snapshot

# Publish multiple posts
for file in blog/*.md; do
  title=$(basename "$file" .md) && \
  body=$(cat "$file") && \
  api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
  curl -X POST https://mataroa.blog/api/posts/ \
    -H "Authorization: Bearer $api_key" \
    -H "Content-Type: application/json" \
    -d "{\"title\":\"$title\",\"body\":\"$body\"}"
done

# Save updated state
/session-snapshot
```

### With repo-briefing
```bash
# Document your repository on your blog
/repo-briefing > repo-summary.md

# Then publish to Mataroa
title="My Project Overview" && \
body=$(cat repo-summary.md) && \
api_key=$(jq -r '.api_key' ~/.claude/matarao-config.json) && \
curl -X POST https://mataroa.blog/api/posts/ \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"$title\",\"body\":\"$body\"}"
```

### With lean-plan
```bash
# Plan migration workflow
/lean-plan

# Then execute with matarao skill:
# 1. Export posts from old platform
# 2. Convert to markdown
# 3. Publish to Mataroa using matarao skill
```

## 🎯 Use Cases

1. **Documentation Publishing**: Publish project docs from repository to blog
2. **Blog Migration**: Migrate existing posts from other platforms to Mataroa
3. **Content Syndication**: Publish articles from multiple sources to your blog
4. **Draft Management**: Create drafts locally, publish when ready
5. **Automated Posting**: CI/CD integration for automated blog updates
6. **Content Archival**: Retrieve posts for local backup or editing
7. **Multi-site Publishing**: Publish same content to multiple Mataroa blogs

## 🚨 Troubleshooting

**Issue 1: JSON parsing errors**
```bash
# Symptoms: "Invalid JSON" errors
# Solution: Properly escape quotes and special characters

# Use jq to safely encode JSON
body_json=$(jq -Rs '.' < post.md)
curl -X POST https://mataroa.blog/api/posts/ \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"$title\",\"body\":$body_json}"
```

**Issue 2: Config file not loading**
```bash
# Symptoms: "Authorization required" despite having config
# Solution: Verify config file format

cat ~/.claude/matarao-config.json
# Should output valid JSON with api_key field

# Test with jq:
jq -r '.api_key' ~/.claude/matarao-config.json
```

**Issue 3: Slug conflicts**
```bash
# Symptoms: "Post with slug already exists"
# Solution: Update existing post instead of creating new

# First, try to get the existing post
curl -X GET "https://mataroa.blog/api/posts/$slug/" \
  -H "Authorization: Bearer $api_key"

# If exists, use PATCH instead of POST
curl -X PATCH "https://mataroa.blog/api/posts/$slug/" \
  -H "Authorization: Bearer $api_key" \
  -H "Content-Type: application/json" \
  -d "{\"body\":\"$new_body\"}"
```

## 🛠️ Advanced Configuration

### Custom Config Location
```bash
# Use environment variable for custom config path
export MATARAO_CONFIG="/custom/path/to/config.json"
api_key=$(jq -r '.api_key' "${MATARAO_CONFIG:-~/.claude/matarao-config.json}")
```

### Multiple Blogs
```json
// ~/.claude/matarao-config.json
{
  "default": {
    "api_key": "key1",
    "base_url": "https://mataroa.blog/api/"
  },
  "work": {
    "api_key": "key2",
    "base_url": "https://mataroa.blog/api/"
  }
}
```

```bash
# Use specific blog profile
profile="work" && \
api_key=$(jq -r ".$profile.api_key" ~/.claude/matarao-config.json)
```

### Content Preprocessing
```bash
# Remove frontmatter before posting
body=$(sed '1,/^---$/d' < post.md | sed '1,/^---$/d')

# Or convert from other formats
body=$(pandoc -f docx -t markdown < article.docx)
```

## Token Efficiency

- Config loading: ~100 tokens
- Single API operation: ~300-500 tokens
- Local file reading: ~200-400 tokens (depends on file size)
- URL fetching: ~300-600 tokens
- Total per operation: **700-1200 tokens**
- Alternative (manual): ~3000+ tokens (reading API docs, crafting curl commands)
- **60-70% reduction** in API integration overhead

---

**Related Skills**:
- `git/repo-briefing` - Generate blog content from repository
- `meta/session-snapshot` - Save state during bulk operations
- `development/lean-plan` - Plan content migration workflows
