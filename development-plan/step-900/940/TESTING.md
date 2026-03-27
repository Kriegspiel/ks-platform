# Slice 940 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

cd ks-home
npm ci
npm run lint
npm run test -- --runInBand --watch=false
npm run seo:validate -- --routes=/,/leaderboard,/blog,/changelog,/rules
npm run structured-data:check
npm run analytics:contract:test
npm run test:a11y -- --routes=/rules,/privacy,/terms
npm run build
```

## Thresholds / Coverage Gates

- SEO validator: 0 missing title/description/canonical tags on required routes.
- Structured data validator: 0 schema errors on emitted JSON-LD.
- Analytics contract test: 0 events with disallowed fields (PII guard hard fail).
- Accessibility: 0 critical/serious violations on trust/legal routes.

## CI Merge Gates

Required checks:

- `website-seo-validate`
- `website-structured-data-check`
- `analytics-contract-check`
- `website-a11y-trust-routes`

## Smoke / Regression

```bash
cd ks-home
npm run test:smoke -- --routes=/rules,/privacy,/terms
```

- Smoke route checks must pass before merge.
