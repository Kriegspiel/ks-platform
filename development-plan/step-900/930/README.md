# Slice 930 - Blog + Changelog System and Editorial Pipeline

## Objective

Create durable blog/changelog publishing surfaces with strict content validation and preview workflow.

## Scope

- Blog list/detail/archive surfaces
- Changelog list/detail surfaces with semantic version/date ordering
- Authoring workflow (Markdown/MDX + frontmatter contracts)
- Content-triggered static regeneration for `ks-home`
- Feed generation and content QA automation

## Deliverables

- Implemented `/blog`, `/blog/:slug`, `/changelog`, `/changelog/:slug`
- Editorial pipeline docs and commands
- RSS/Atom and sitemap integration
- Verified content-update trigger from `Kriegspiel/content` to static regeneration in `ks-home`
