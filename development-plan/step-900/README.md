# Step 900 - Website and Content Track

## Goal

Plan and execute the public-facing Kriegspiel web experience (marketing + content surfaces) with production-grade quality gates, including landing/home, leaderboard, blog, changelog, rules, and supporting SEO/analytics/legal/content-ops workflows.

Step 900 turns product capabilities from prior steps into a discoverable, indexable, and maintainable public web presence.

## Read First

- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [FRONTEND.md](../../FRONTEND.md)
- [INFRA.md](../../INFRA.md)
- [development-plan/PLAN.md](../PLAN.md)
- [development-plan/step-800/HANDOFF.md](../step-800/HANDOFF.md)

## Depends On

- `step-800`

## Scope-Based Slices

### 910 — Information Architecture, Routing, and Content Contracts
- Define canonical page map and route ownership for home, leaderboard, blog, changelog, and rules
- Formalize shared content/data contracts (metadata, author/date/version tags, structured frontmatter)
- Lock navigation, URL, and slug policy including redirects and deprecation behavior
- Publish non-functional baselines (performance budgets, accessibility floor, localization readiness)

### 920 — Landing/Home + Leaderboard Experience
- Design and implement conversion-ready landing/home surface
- Define leaderboard public-view model and update cadence
- Add empty/loading/error states and resilience behavior for leaderboard fetches
- Standardize layout/visual patterns shared by marketing and product-adjacent pages

### 930 — Blog + Changelog System and Editorial Pipeline
- Implement blog index/detail, changelog index/detail, and archive views
- Define authoring pipeline (Markdown/MDX conventions, linting, preview flow, publishing checklist)
- Add feeds/sitemaps metadata (RSS/Atom + entry metadata validity)
- Gate content quality with lint, link validation, and schema/frontmatter checks

### 940 — Rules, Trust Surfaces, and Discoverability (SEO/Analytics/Legal)
- Build canonical rules page with versioning and change reference links
- Implement SEO technical baseline (meta tags, OG/Twitter cards, canonical URLs, structured data)
- Define analytics events and privacy-aware instrumentation policy
- Add legal/trust surfaces (privacy policy, terms shell, cookie/telemetry disclosure where applicable)

### 950 — Preview, Deploy, Regression, and Launch Readiness for Website Track
- Add deterministic preview environments for content and UI changes
- Define CI merge gates for website/content surfaces
- Require accessibility, smoke, visual-regression, and broken-link checks as release blockers
- Publish launch/rollback runbook and ownership matrix for ongoing content ops

## Exit Criteria

- All slices `910`-`950` complete with evidence and no unresolved critical issues
- Required pages live and validated: home, leaderboard, blog, changelog, rules
- SEO/analytics/legal/privacy baseline implemented and reviewed
- CI gates enforce automated website/content quality checks
- Preview + production deploy and rollback flows documented and test-validated

## Out of Scope

- New gameplay mechanics or auth/session model changes
- Paid growth campaigns or ad-buy operations
- Full CMS migration beyond MVP editorial pipeline
