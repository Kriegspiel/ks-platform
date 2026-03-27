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
```

## CI Merge Gates

Required checks:

- `website-lint`
- `website-unit`
- `website-e2e-public-routes`
- `website-a11y-public-routes`
- `website-visual-regression`
- `website-smoke-public-routes`
- `website-seo-validate`
- `content-link-check`
- `content-frontmatter-check`
- `preview-deploy`

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

- Rollback drill must pass at least once before launch signoff.
