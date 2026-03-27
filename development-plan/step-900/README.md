# Step 900 - Website and Content Track

## Goal

Plan and execute the public-facing Kriegspiel web experience (marketing + content surfaces) with production-grade quality gates, including landing/home, leaderboard, blog, changelog, rules, and supporting SEO/analytics/legal/content-ops workflows.

Step 900 turns product capabilities from prior steps into a discoverable, indexable, and maintainable public web presence, with `Kriegspiel/content` as the source of truth and deterministic static regeneration in `ks-home` on content updates.

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
- Lock `Kriegspiel/content` as source-of-truth repository for public editorial content consumed by `ks-home`
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
- Require static page regeneration in `ks-home` whenever content in `Kriegspiel/content` changes
- Gate content quality with markdown, frontmatter, link, build, sitemap, and feed checks

### 940 — Rules, Trust Surfaces, and Discoverability (SEO/Analytics/Legal)
- Build canonical rules page with versioning and change reference links
- Implement SEO technical baseline (meta tags, OG/Twitter cards, canonical URLs, structured data)
- Define analytics events and privacy-aware instrumentation policy
- Add legal/trust surfaces (privacy policy, terms shell, cookie/telemetry disclosure where applicable)

### 950 — Preview, Deploy, Regression, and Launch Readiness for Website Track
- Add deterministic preview environments for website and content PRs
- Define CI merge gates for website/content surfaces including content-triggered static regeneration
- Require accessibility, smoke, visual-regression, and broken-link checks as release blockers
- Enforce rollback behavior on failed deploys (auto-revert to last known good release)

### 960 — Content Repository Organization and Operational Hygiene
- Define `Kriegspiel/content` information architecture (folders, naming, ownership metadata)
- Standardize content lifecycle states (draft/review/published/archived) and retention policy
- Enforce repository structure checks and ownership rules in CI
- Document contributor workflow for scalable, low-risk content operations


## Operator-Required Steps (Cloudflared + `kriegspiel.org`)

These steps are mandatory for production DNS/tunnel cutover and cannot be fully automated by the agent because they require Cloudflare account auth and/or Fil approval.

### Responsibility Split

| Area | Agent can automate | Requires Fil interaction/approval |
|---|---|---|
| Preflight + command prep | Generate/review runbook, validate local config, run dry-run checks | Confirm environment + approve production execution window |
| `cloudflared` auth | Verify binary/version, confirm service unit/files, run non-auth checks | `cloudflared tunnel login` in browser-backed Cloudflare session |
| Tunnel lifecycle | List/select existing tunnel, template config, install service files | Create new tunnel if needed and confirm tunnel UUID to use |
| DNS routing (`kriegspiel.org`) | Propose records and verify with `dig`/`curl` after change | Authorize `cloudflared tunnel route dns` for `kriegspiel.org` records |
| Cutover/rollback | Run smoke checks and rollback scripts after approval | Final go/no-go and rollback approval if production impact occurs |

### Required Operator Runbook (Production)

```bash
# 0) preflight (agent can run)
cloudflared --version
cloudflared tunnel list

# 1) interactive auth (Fil-required)
cloudflared tunnel login

# 2) create or select tunnel (Fil approval required for create)
cloudflared tunnel create ks-platform-prod        # only if no approved tunnel exists
cloudflared tunnel list                           # capture NAME + UUID used for prod

# 3) map DNS under kriegspiel.org (Fil approval required)
cloudflared tunnel route dns ks-platform-prod kriegspiel.org
cloudflared tunnel route dns ks-platform-prod app.kriegspiel.org
cloudflared tunnel route dns ks-platform-prod api.kriegspiel.org

# 4) install/restart service + checks (agent can run after approval)
sudo cloudflared service install
sudo systemctl restart cloudflared
sudo systemctl status cloudflared --no-pager
journalctl -u cloudflared -n 100 --no-pager

# 5) external verification (agent can run)
dig +short kriegspiel.org
DIG_APP=$(dig +short app.kriegspiel.org)
DIG_API=$(dig +short api.kriegspiel.org)
printf "app=%s\napi=%s\n" "$DIG_APP" "$DIG_API"
curl -I https://kriegspiel.org
curl -I https://app.kriegspiel.org
curl -I https://api.kriegspiel.org/health
```

### Acceptance Checks

- `cloudflared tunnel list` shows exactly one approved production tunnel in active use.
- `kriegspiel.org`, `app.kriegspiel.org`, and `api.kriegspiel.org` resolve through Cloudflare tunnel routing.
- `systemctl status cloudflared` is `active (running)` with no crash-loop.
- HTTPS checks return successful status (200/30x for site pages, 200 for API health).

### Rollback / Fallback Notes

- If DNS or tunnel verification fails, revert DNS routes to prior known-good target before retrying.
- Keep previous tunnel credentials/config available; do not delete old tunnel until 24h stable runtime.
- If post-cutover smoke fails, execute platform rollback then restore previous DNS mapping and re-run smoke.

## Exit Criteria

- All slices `910`-`960` complete with evidence and no unresolved critical issues
- Required pages live and validated: home, leaderboard, blog, changelog, rules
- SEO/analytics/legal/privacy baseline implemented and reviewed
- CI gates enforce automated website/content quality checks including static-regeneration checks on content updates
- Preview + production deploy and rollback flows documented and test-validated

## Out of Scope

- New gameplay mechanics or auth/session model changes
- Paid growth campaigns or ad-buy operations
- Full CMS migration beyond MVP editorial pipeline
