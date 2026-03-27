# Slice 910 - Implementation Plan

## Files / Areas

- Website app routing and layout modules
- Content schema definitions and validators
- Navigation and sitemap seed config
- Documentation for route and slug policy

## Tasks

1. Create canonical route map for `/`, `/leaderboard`, `/blog`, `/blog/:slug`, `/changelog`, `/changelog/:slug`, `/rules`.
2. Define route deprecation/redirect policy and non-breaking URL migration rules.
3. Create required frontmatter schema: `title`, `slug`, `summary`, `publishedAt`, `updatedAt`, `author`, `tags`, `draft`, `version` (for changelog/rules where applicable).
4. Add schema validator command integrated into CI.
5. Define global nav/footer links, fallback pages, and 404/410 behavior.
6. Publish baseline budgets: LCP <= 2.5s p75, CLS <= 0.1, JS budget <= 220KB gz initial route.
7. Set accessibility floor: WCAG 2.2 AA checks for keyboard navigation, landmarks, heading order, and color contrast.

## Acceptance Criteria

- All required routes are documented and reachable in app router.
- Invalid content metadata fails local and CI validation.
- Redirect/deprecation policy exists and includes test cases.
- Baseline quality budgets are documented and referenced by subsequent slices.
