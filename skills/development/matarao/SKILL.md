---
name: matarao
description: Publish and manage blog posts on Mataroa via API. Create, update, and retrieve posts from URLs or local files. Use when user says "publish to mataroa", "update blog post", or "fetch mataroa post".
---

# matarao


## Description
Manage Mataroa blog posts directly from Claude Code without leaving your terminal. Publish from local markdown files or URLs, update existing posts, and retrieve content for editing (~700 tokens per operation vs 3000+ manual).

- User says 'use [skill-name]' or mentions the skill by name
- Relevant to the current task or discussion

## Usage

### Quick Start

**Step 1**: Get your API key from https://mataroa.blog/api/docs/

**Step 2**: Ask Claude to publish a post:
```
"Publish this markdown file to my dybilar blog: post.md"
```

Claude will handle the API calls automatically using the matarao skill!

### Prerequisites
Create config file at `~/.claude/matarao-config.json`:

**Single blog:**
```json
{
  "api_key": "your-mataroa-api-key-here",
  "base_url": "https://mataroa.blog/api/"
}
```

**Multiple blogs:**
```json
{
  "default": "dybilar",
  "dybilar": {
    "api_key": "your_key_here",
    "base_url": "https://mataroa.blog/api/",
    "blog_url": "https://dybilar.mataroa.blog"
  },
  "torah": {
    "api_key": "your_key_here",
    "base_url": "https://mataroa.blog/api/",
    "blog_url": "https://torah.mataroa.blog"
  }
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

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| title | string | Yes (create) | Post title for new posts |
| body | string | No | Post content (markdown supported) |
| slug | string | Yes (get/update) | Post URL slug identifier |
| published_at | ISO date | No | Publication timestamp (ISO 8601 format, e.g. "2026-01-13") |
| source | path/URL | Yes | Local file path or remote URL for content |

## Features
- **Create posts** from local markdown files or remote URLs
- **Update existing posts** with new content or metadata
- **Retrieve posts** to review or edit locally
- **Secure authentication** via JSON config file
- **No rate limiting** - unlimited API calls to Mataroa

## Examples

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

## Output

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

## Important Notes

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
