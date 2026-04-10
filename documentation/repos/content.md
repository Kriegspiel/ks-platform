# content

`content` is the source-of-truth repo for public text content rendered on `kriegspiel.org`.

It is not a runtime app. It is an input repo consumed by `ks-home`.

## What lives here

- blog posts
- changelog entries
- rules pages
- public copy docs
- adjacent snippets and assets used inside articles

## Layout

Important top-level areas:

- `blog/`
- `changelog/`
- `rules/`
- `docs/`

## Blog structure

Blog is folder-based.

Pattern:

- `blog/<slug>/README.md`

Supporting assets and snippets live next to the entry:

- JSON request/response snippets
- shell snippets
- HTTP snippets
- article-local images/assets if needed

This makes each article self-contained.

## Changelog structure

Changelog entries are date-version markdown pages.

Examples:

- `2026-04-01-v1-0-0.md`
- `2026-04-02-v1-1-0.md`
- `2026-04-04-v1-2-0.md`

## Rules structure

Rules pages are markdown-backed public docs consumed by `ks-home`.

Current important pages include:

- Berkeley
- Wild 16
- comparison material

## Relationship to `ks-home`

`content` owns the editable text.
`ks-home` owns the rendering.

Operational rule:

- editing `content` alone does not publish anything
- the static site must be refreshed through `ks-home`

## Important documentation already inside this repo

- content organization docs
- content source contract docs

These explain:

- how entries are structured
- what downstream consumers expect

## What should not live here

- live runtime code
- deployment automation
- duplicated site-rendering logic

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
