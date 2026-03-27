# Slice 930 - Implementation Plan

## Files / Areas

- Blog/changelog page templates and list renderers
- Content collection loaders/parsers
- Frontmatter and markdown lint rules
- Feed/sitemap generation jobs
- Content-change trigger and static regeneration pipeline config

## Tasks

1. Build blog index and detail templates with tags, author/date, reading-time metadata.
2. Build changelog index/detail templates with release version, category labels, and backward links.
3. Implement slug collision detection and duplicate-publish guards.
4. Add markdown lint + link lint + frontmatter schema validation commands.
5. Implement content-update trigger so `ks-home` static pages regenerate on `Kriegspiel/content` changes.
6. Add preview mode for draft posts and changelog entries.
7. Generate RSS/Atom feeds and sitemap outputs; ensure canonical URLs align with route policy.

## Acceptance Criteria

- Blog and changelog pages resolve deterministically from `Kriegspiel/content` source.
- Invalid frontmatter, duplicate slugs, broken links, sitemap errors, or feed errors fail CI.
- Content-update trigger runs static regeneration for affected routes and passes verification checks.
- Draft content is hidden from production builds.
- Feed and sitemap generation succeed and include required metadata fields.
