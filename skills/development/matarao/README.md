# Matarao Blog Publishing Skill

Publish and manage blog posts on [Mataroa.blog](https://mataroa.blog) directly from Claude Code.

## Quick Start

### 1. Get Your API Key

Visit https://mataroa.blog/api/docs/ and copy your API key.

### 2. Create Config File

Create `~/.claude/matarao-config.json`:

**For single blog:**
```json
{
  "api_key": "your-api-key-here",
  "base_url": "https://mataroa.blog/api/"
}
```

**For multiple blogs:**
```json
{
  "default": "myblog",
  "myblog": {
    "api_key": "first-api-key",
    "base_url": "https://mataroa.blog/api/",
    "blog_url": "https://myblog.mataroa.blog"
  },
  "secondblog": {
    "api_key": "second-api-key",
    "base_url": "https://mataroa.blog/api/",
    "blog_url": "https://secondblog.mataroa.blog"
  }
}
```

### 3. Use the Skill

Just ask Claude Code to publish:

```
"Publish this markdown file to my blog: article.md"
```

Or for specific blogs:

```
"Publish article.md to my torah blog"
```

## What You Can Do

- **Publish** markdown files as blog posts
- **Update** existing posts
- **Retrieve** posts for editing
- **Manage multiple blogs** with one config

## Examples

### Publish a Post

```
"Publish my-article.md to mataroa"
```

### Update a Post

```
"Update the post 'my-first-post' with the content from updated-article.md"
```

### Publish to Specific Blog

```
"Publish this to my torah blog: torah-study.md"
```

## How It Works

Claude Code uses the Mataroa API to:
1. Read your markdown file
2. Format it as JSON
3. Send it to Mataroa's API
4. Return the published URL

All authentication is handled automatically using your config file.

## Troubleshooting

**"Authentication failed"**
- Check that `~/.claude/matarao-config.json` exists
- Verify your API key is correct

**"Post not found"**
- Use the exact slug from the post URL
- Slugs are lowercase with hyphens

## More Information

See [SKILL.md](./SKILL.md) for complete documentation including:
- All API parameters
- Advanced configuration
- Content preprocessing
- Integration with other skills
- Troubleshooting guide

## Tested Configuration

This skill has been tested with:
- Multiple blog setup (dybilar.mataroa.blog, torah.mataroa.blog)
- Windows environment
- Git Bash shell
- Without jq dependency (using JSON file method)

Both test posts were successfully published!
