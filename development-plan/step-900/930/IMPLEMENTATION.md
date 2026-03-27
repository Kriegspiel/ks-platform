# Slice 930 - Implementation Plan

## Files / Areas

- Blog/changelog page templates and list renderers
- Content collection loaders/parsers
- Frontmatter and markdown lint rules
- Feed/sitemap generation jobs

## Tasks

1. Build blog index and detail templates with tags, author/date, reading-time metadata.
2. Build changelog index/detail templates with release version, category labels, and backward links.
3. Implement slug collision detection and duplicate-publish guards.
4. Add markdown lint + link lint + frontmatter schema validation commands.
5. Add preview mode for draft posts and changelog entries.
6. Generate RSS/Atom feeds and ensure canonical URLs align with route policy.

## Acceptance Criteria

- Blog and changelog pages resolve deterministically from content source.
- Invalid frontmatter, duplicate slugs, and broken links fail CI.
- Draft content is hidden from production builds.
- Feed generation succeeds and includes required metadata fields.
