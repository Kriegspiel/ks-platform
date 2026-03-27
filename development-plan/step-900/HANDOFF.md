# Step 900 Handoff Notes

## Purpose

Execution handoff packet for delivering and operating the Kriegspiel public website/content track.

## Current State (Planning Packet)

- Step 900 expanded into executable slices `910`-`960`.
- Each slice includes `README.md`, `IMPLEMENTATION.md`, `TESTING.md`, and `CHECKLIST.md`.
- Testing packets include exact commands, CI merge gates, accessibility requirements, smoke checks, visual regression expectations, link validation, static-regeneration verification, and rollback validation.

## Execution Strategy

1. **910 first** to lock IA/routes/contracts so downstream implementation does not churn.
2. **920 second** to deliver high-visibility home + leaderboard user surfaces.
3. **930 third** to establish repeatable editorial pipeline for blog and changelog content with content-driven static regeneration.
4. **940 fourth** to layer trust/discoverability controls (rules/SEO/analytics/legal) before release.
5. **950 fifth** to certify preview/deploy flows, content-PR previews, and release-blocking quality gates.
6. **960 last** to institutionalize content repository structure and contributor/ownership hygiene for long-term operations.

## Quality Guardrails

- Do not ship public pages without passing accessibility and broken-link checks.
- Do not merge content-path changes without markdown/frontmatter/link/build/sitemap/feed validation.
- `Kriegspiel/content` is the source of truth; content changes must trigger static page regeneration in `ks-home`.
- Preview deploys are required for both website PRs and content PRs.
- Failed deploys must trigger rollback behavior to last known good release before closeout.
- Analytics must be privacy-aware and documented; no silent tracking additions.
- Rules page changes require version tagging and explicit changelog linkage.

## Handoff to Operations

Step 900 should deliver:

- Production-ready public surfaces for home, leaderboard, blog, changelog, and rules
- Repeatable editorial workflow with deterministic validation gates
- Search/share discoverability baseline (SEO + social metadata) with legal/privacy guardrails
- Release and rollback runbook with clear ownership for content and platform operations
- Stable, enforceable content-repo organization standards for maintainable long-term publishing
