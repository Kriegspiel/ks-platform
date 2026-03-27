# Step 900 Progress

Status: IN PROGRESS (910 + 920 + 930 + 940 + 950 COMPLETE)
Last Updated: 2026-03-27

## Slice Checklist

- [x] `910` Information architecture, routing, and content contracts
- [x] `920` Landing/home + leaderboard experience
- [x] `930` Blog + changelog system and editorial pipeline
- [x] `940` Rules, trust surfaces, and discoverability (SEO/analytics/legal)
- [x] `950` Preview, deploy, regression, and launch readiness for website track
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

- Slice 930 execution PASS (ks-home PR #19, content PR #6).
- ks-home + content gates PASS for slice 930:
  - content: npm ci; npm run lint:markdown; npm run lint:links; npm run validate:frontmatter; npm run build:content-index
  - ks-home: npm ci; npm run test -- --runInBand --watch=false; npm run test:e2e -- --grep "blog|changelog"; npm run build; npm run content:trigger:simulate -- --from=../content --verify-static-regen; npm run sitemap:generate -- --check; npm run feeds:generate -- --check; npm run test:a11y -- --routes=/blog,/changelog; npm run test:smoke -- --routes=/blog,/changelog

- Slice 940 execution PASS (ks-home PR #20, content PR #7).
- ks-home + content gates PASS for slice 940:
  - content: npm ci; npm run lint:markdown; npm run lint:links; npm run validate:frontmatter; npm run build:content-index
  - ks-home: npm ci; npm run lint; npm run test -- --runInBand --watch=false; npm run seo:validate -- --routes=/,/leaderboard,/blog,/changelog,/rules; npm run structured-data:check; npm run analytics:contract:test; npm run test:a11y -- --routes=/rules,/privacy,/terms; npm run build; npm run test:smoke -- --routes=/rules,/privacy,/terms; npm run routes:validate

- Slice 950 execution PASS (ks-home PR #21, content PR #8).
- CI gate formalization shipped via GitHub Actions workflows:
  - ks-home: `.github/workflows/website-gates.yml`
  - content: `.github/workflows/content-gates.yml`
- ks-home + content gates PASS for slice 950:
  - ks-home: npm run lint; npm run test -- --runInBand --watch=false; npm run test:e2e -- --grep "home|leaderboard|blog|changelog|rules"; npm run test:a11y -- --routes=/,/leaderboard,/blog,/changelog,/rules; npm run test:visual -- --suite=full-public-site; npm run test:smoke -- --routes=/,/leaderboard,/blog,/changelog,/rules; npm run seo:validate -- --routes=/,/leaderboard,/blog,/changelog,/rules; npm run build; npm run content:trigger:simulate -- --from=../content --verify-static-regen; npm run sitemap:generate -- --check; npm run feeds:generate -- --check
  - content: npm ci; npm run lint:markdown; npm run lint:links; npm run validate:frontmatter; npm run build:content-index
- Rollback drill PASS using `./scripts/deploy/rollback.sh --to previous` against synthetic artifact links.
- Smoke script verified (`BASE_URL=https://example.com ./scripts/deploy/smoke.sh --routes "/"`).

## Blockers

- None for slice 920.
- None for slice 930.
- None for slice 940.
- No technical blocker for slice 960; launch cutover still depends on Fil-approved Cloudflare tunnel + DNS mapping.

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
