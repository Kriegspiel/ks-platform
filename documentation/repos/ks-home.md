# ks-home

`ks-home` is the static public website generator for `kriegspiel.org`.

It owns:

- public homepage
- rules landing and rule detail pages
- blog
- changelog
- about
- static leaderboard
- public profile pages rendered for the public site

## Runtime role

- public host: `kriegspiel.org`
- rendering model: build-time static generation
- upstream content source: `content`
- upstream API source for certain pages: `ks-backend`

## Main layout

### `src/pages.mjs`

Primary page renderer.

Important render functions:

- `renderShell`
- `renderHomePage`
- `renderLeaderboardPage`
- `renderPublicProfilePage`
- `renderBlogIndex`
- `renderBlogDetail`
- `renderBlogArchive`
- `renderChangelogIndex`
- `renderChangelogDetail`
- `renderRulesPage`
- `renderRuleDetailPage`

This file is the center of the site’s page composition.

### `scripts/build.mjs`

Static build pipeline.

Responsibilities:

- read content
- fetch any needed API data
- call renderers
- write `dist/`

### `src/leaderboard.mjs`

Leaderboard normalization/sorting helpers.

Important rule:

- the public static leaderboard is human-only and overall-rating only

### `scripts/refresh-static-site.sh`

Operational refresh script.

Responsibilities:

- update detached worktrees for `ks-home` and `content`
- build with `KS_CONTENT_PATH` and `KS_API_BASE`
- rsync built output into the live `dist`

## Content contract

`ks-home` treats `content` as the source of truth for:

- blog entries
- changelog entries
- rules content
- snippets embedded into articles

It should not become a second editable content source.

## Important behaviors

### Static leaderboard

Behavior today:

- human-only
- overall-rating only
- static snapshot
- refreshed by the site refresh pipeline

### Rules and comparison pages

`ks-home` owns the public rendering and layout of:

- Berkeley rules
- Wild 16 rules
- comparison page

### Blog and changelog rendering

Supports:

- folder-based blog posts
- inline snippets/assets next to the article
- public archive/index pages

## Operational notes

- `ks-home` version is independent from backend/frontend versions
- content changes require a `ks-home` rebuild/refresh to become public
- `.site-refresh` is a workspace dependency used by the refresh script

## Testing

Important test clusters include:

- route smoke tests
- rules pages tests
- leaderboard/blog/changelog tests

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
