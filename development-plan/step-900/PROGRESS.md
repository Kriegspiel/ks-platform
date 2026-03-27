# Step 900 Progress

Status: IN PROGRESS (910 + 920 COMPLETE)
Last Updated: 2026-03-27

## Slice Checklist

- [x] `910` Information architecture, routing, and content contracts
- [x] `920` Landing/home + leaderboard experience
- [ ] `930` Blog + changelog system and editorial pipeline
- [ ] `940` Rules, trust surfaces, and discoverability (SEO/analytics/legal)
- [ ] `950` Preview, deploy, regression, and launch readiness for website track
- [ ] `960` Content repository organization and operational hygiene

## Test Evidence

- Slice 910 execution PASS (ks-home PR #16, content PR #3).
- Slice 920 execution PASS (ks-home PR #17, content PR #4).
- ks-home gates PASS for slice 920:
  - npm ci
  - npm run lint
  - npm run test -- --runInBand --watch=false
  - npm run test:coverage:check -- --lines 82 --functions 82 --branches 78 --statements 82
  - npm run test:e2e -- --grep "home|leaderboard"
  - npm run test:smoke -- --routes=/,/leaderboard,/rules
  - npm run test:a11y -- --routes=/,/leaderboard
  - npm run test:visual -- --suite=marketing-core
  - npm run routes:validate
  - npm run content:schema:check
  - npm run content:source-contract:check
  - npm run build
- Coverage evidence from slice 920 run: lines 99.45%, branches 90.47%, functions 100%, statements 99.45%.
- No CI checks configured on website repos yet; merge completed after local gate pass evidence.

## Blockers

- None for slice 920.
- Slice 930 can begin.

## Discovery Notes

- Step 900 creates a full website/content execution packet spanning product marketing, content operations, and trust/discoverability.
- `Kriegspiel/content` is explicitly treated as the source of truth for public content consumed by `ks-home`.
- Any content update must trigger static page regeneration, with automated validation for markdown/frontmatter/links/build/sitemap/feed before merge or deploy.
- Required public pages are explicitly tracked as release scope: home, leaderboard, blog, changelog, rules.
- SEO, analytics, legal/privacy, and content pipeline controls are treated as first-class delivery requirements, not post-launch cleanup.

## Handoff

- Start at `step-900/CHECKLIST.md`.
- Execute slices in order `910` → `960` unless a dependency exception is documented and approved.
- Record command outputs and PASS/FAIL evidence as each slice completes.
