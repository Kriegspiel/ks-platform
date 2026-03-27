# Slice 910 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

cd ks-home
npm ci
npm run lint
npm run test -- --runInBand --watch=false
npm run routes:validate
npm run content:schema:check
npm run build
```

## Thresholds / Coverage Gates

- Route validation must report 0 missing required routes.
- Content schema validation must report 0 invalid documents.
- Unit test coverage floor: lines >= 80%, branches >= 75%.

## CI Merge Gates

Required checks:

- `website-lint`
- `website-unit`
- `routes-contract-check`
- `content-schema-check`

## Accessibility / Smoke / Regression

- Automated keyboard-route smoke over required pages must pass.
- No broken internal nav links in route crawl.

## Skip Policy + Prereqs

- No skips allowed for route/schema checks on `main`.
- Any environment-based skip must include owner + mitigation ETA.
