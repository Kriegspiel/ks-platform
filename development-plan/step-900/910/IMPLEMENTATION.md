# Slice 910 - Implementation Plan

## Files / Areas

- Website app routing and layout modules
- Content schema definitions and validators
- Navigation and sitemap seed config
- Documentation for route and slug policy
- Cross-repo content-source contract docs (`Kriegspiel/content` and `ks-home`)

## Tasks

1. Create canonical route map for `/`, `/leaderboard`, `/blog`, `/blog/:slug`, `/changelog`, `/changelog/:slug`, `/rules`.
2. Define route deprecation/redirect policy and non-breaking URL migration rules.
3. Lock `Kriegspiel/content` as source-of-truth for blog/changelog/rules content consumed by `ks-home`.
4. Create required frontmatter schema: `title`, `slug`, `summary`, `publishedAt`, `updatedAt`, `author`, `tags`, `draft`, `version` (for changelog/rules where applicable).
5. Add schema validator command integrated into CI.
6. Define global nav/footer links, fallback pages, and 404/410 behavior.
7. Publish baseline budgets: LCP <= 2.5s p75, CLS <= 0.1, JS budget <= 220KB gz initial route.
8. Set accessibility floor: WCAG 2.2 AA checks for keyboard navigation, landmarks, heading order, and color contrast.

## Acceptance Criteria

- All required routes are documented and reachable in app router.
- Content-source contract is documented and referenced by slices 930/950/960.
- Invalid content metadata fails local and CI validation.
- Redirect/deprecation policy exists and includes test cases.
- Baseline quality budgets are documented and referenced by subsequent slices.
