# Slice 950 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

# local parity gate
cd ks-home
npm ci
npm run lint
npm run test -- --runInBand --watch=false
npm run test:e2e -- --grep "home|leaderboard|blog|changelog|rules"
npm run test:a11y -- --routes=/,/leaderboard,/blog,/changelog,/rules
npm run test:visual -- --suite=full-public-site
npm run test:smoke -- --routes=/,/leaderboard,/blog,/changelog,/rules
npm run seo:validate -- --routes=/,/leaderboard,/blog,/changelog,/rules
npm run build

# content gates
cd ../content
npm ci
npm run lint:markdown
npm run lint:links
npm run validate:frontmatter

# content-triggered static regen + publication assets
cd ../ks-home
npm run content:trigger:simulate -- --from=../content --verify-static-regen
npm run sitemap:generate -- --check
npm run feeds:generate -- --check
```


## Operator-Required Steps: Cloudflared + `kriegspiel.org`

The CI gates below are automatable. The following production routing steps require operator interaction/approval.

### Responsibility Split

- **Fil-required:** `cloudflared tunnel login`, production tunnel create/selection approval, DNS route changes for `kriegspiel.org` domains, go/no-go for live cutover.
- **Agent-automatable (after approval):** service install/restart, status/log checks, DNS and HTTPS verification commands, rollback smoke validation.

### Production Runbook Snippet

```bash
# preflight
cloudflared --version
cloudflared tunnel list

# Fil-required auth/approval
cloudflared tunnel login
cloudflared tunnel create ks-platform-prod   # if needed and approved

# Fil-approved DNS mapping
cloudflared tunnel route dns ks-platform-prod kriegspiel.org
cloudflared tunnel route dns ks-platform-prod app.kriegspiel.org
cloudflared tunnel route dns ks-platform-prod api.kriegspiel.org

# agent-executable after approval
sudo cloudflared service install
sudo systemctl restart cloudflared
sudo systemctl status cloudflared --no-pager
journalctl -u cloudflared -n 100 --no-pager
```

### Acceptance Checks (Release Blocking)

```bash
# DNS should resolve to Cloudflare-managed target(s)
dig +short kriegspiel.org
dig +short app.kriegspiel.org
dig +short api.kriegspiel.org

# endpoint health
curl -fsS https://kriegspiel.org >/dev/null
curl -fsS https://app.kriegspiel.org >/dev/null
curl -fsS https://api.kriegspiel.org/health >/dev/null
```

- All three hostnames resolve and serve expected HTTPS responses.
- `cloudflared` service is running without restart loop.

### Rollback / Fallback

```bash
# 1) restore previous DNS route target (document prior mapping before cutover)
# 2) switch back to prior tunnel/config if needed
sudo systemctl restart cloudflared

# 3) verify previous stable endpoints
curl -fsS https://kriegspiel.org >/dev/null
curl -fsS https://app.kriegspiel.org >/dev/null
curl -fsS https://api.kriegspiel.org/health >/dev/null
```

- If any acceptance check fails, rollback is mandatory before closing deploy.

## CI Merge Gates

Required checks:

- `website-lint`
- `website-unit`
- `website-e2e-public-routes`
- `website-a11y-public-routes`
- `website-visual-regression`
- `website-smoke-public-routes`
- `website-seo-validate`
- `content-lint-markdown`
- `content-link-check`
- `content-frontmatter-check`
- `website-build-public`
- `website-static-regen-on-content`
- `website-sitemap-check`
- `website-feed-check`
- `preview-deploy-website-pr`
- `preview-deploy-content-pr`

## Regression Matrix (Release Blocking)

- Home render + CTA path
- Leaderboard data render + empty/error fallback
- Blog list/detail + pagination
- Changelog list/detail + version ordering
- Rules page render + revision metadata

Every row must be PASS or explicitly WAIVED with risk-owner approval.

## Post-Deploy Smoke + Rollback

```bash
# post-deploy smoke
curl -fsS https://<site-domain>/ >/dev/null
curl -fsS https://<site-domain>/leaderboard >/dev/null
curl -fsS https://<site-domain>/blog >/dev/null
curl -fsS https://<site-domain>/changelog >/dev/null
curl -fsS https://<site-domain>/rules >/dev/null

# rollback drill
./scripts/deploy/rollback.sh --to previous
./scripts/deploy/smoke.sh --routes /,/leaderboard,/blog,/changelog,/rules
```

- Failed deploys must auto-trigger rollback and produce PASS smoke evidence.
- Rollback drill must pass at least once before launch signoff.
