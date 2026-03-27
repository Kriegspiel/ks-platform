# Slice 920 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

cd ks-home
npm ci
npm run lint
npm run test -- --runInBand --watch=false
npm run test:coverage:check -- --lines 82 --functions 82 --branches 78 --statements 82
npm run test:e2e -- --grep "home|leaderboard"
npm run test:smoke -- --routes=/,/leaderboard,/rules
```

## Thresholds / Coverage Gates

- UI unit/component coverage: lines/functions/statements >= 82%, branches >= 78%.
- E2E flow for home+leaderboard must pass with 0 failures.
- Smoke route checks must pass for `/`, `/leaderboard`, `/rules`.

## CI Merge Gates

Required checks:

- `website-lint`
- `website-unit`
- `website-e2e-home-leaderboard`
- `website-smoke-routes`

## Accessibility Checks

```bash
cd ks-home
npm run test:a11y -- --routes=/,/leaderboard
```

- 0 critical axe violations; 0 serious color-contrast violations.

## Visual Regression

```bash
cd ks-home
npm run test:visual -- --suite=marketing-core
```

- Snapshot diffs require review and explicit approval label in PR.
