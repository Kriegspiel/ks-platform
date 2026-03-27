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


## Operator-Required Cloudflared/Domain Cutover (`kriegspiel.org`)

This section is an explicit handoff for actions requiring human interaction.

### What the Agent Can Do

- Prepare exact commands, config templates, and dry-run checks.
- Validate `cloudflared` installation/version and existing tunnel inventory.
- Run post-change verification (`dig`, `curl`, smoke scripts) and attach evidence.
- Execute rollback scripts after explicit go-ahead.

### What Fil Must Do (Interactive/Approval)

1. Complete `cloudflared tunnel login` on the production host (`fil@rpi-server-02.localdomain`).
2. Approve/create/select the production tunnel used for `kriegspiel.org`.
3. Approve DNS route mapping for:
   - `kriegspiel.org`
   - `app.kriegspiel.org`
   - `api.kriegspiel.org`
4. Approve production cutover timing and any rollback execution that affects live traffic.

### Minimal Live Runbook

```bash
# interactive auth
cloudflared tunnel login

# tunnel selection/creation
cloudflared tunnel list
cloudflared tunnel create ks-platform-prod   # only if needed

# DNS mapping
cloudflared tunnel route dns ks-platform-prod kriegspiel.org
cloudflared tunnel route dns ks-platform-prod app.kriegspiel.org
cloudflared tunnel route dns ks-platform-prod api.kriegspiel.org

# service + validation
sudo cloudflared service install
sudo systemctl restart cloudflared
sudo systemctl status cloudflared --no-pager
curl -fsS https://kriegspiel.org >/dev/null
curl -fsS https://app.kriegspiel.org >/dev/null
curl -fsS https://api.kriegspiel.org/health >/dev/null
```

### Fallback

- On failed cutover checks: restore previous DNS routes, restart prior known-good tunnel/service config, and rerun smoke.
- Keep rollback evidence in step-900 validation logs before closing launch readiness.

## Handoff to Operations

Step 900 should deliver:

- Production-ready public surfaces for home, leaderboard, blog, changelog, and rules
- Repeatable editorial workflow with deterministic validation gates
- Search/share discoverability baseline (SEO + social metadata) with legal/privacy guardrails
- Release and rollback runbook with clear ownership for content and platform operations
- Stable, enforceable content-repo organization standards for maintainable long-term publishing


## Slice 930 complete

- Blog/changelog templates, archive, feed/sitemap checks, and content-triggered regen simulation shipped.
- Editorial pipeline documented in `content/docs/editorial-pipeline.md`.
- Draft preview flow enabled via `KS_PREVIEW_DRAFTS=true` in `ks-home` builds.
