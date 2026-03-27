# Slice 960 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

cd content
npm ci
npm run validate:repo-structure
npm run validate:file-naming
npm run validate:lifecycle-metadata
npm run validate:codeowners-coverage
npm run test:policy-snapshots

cd ../ks-home
npm ci
npm run content:policy:verify -- --from=../content
npm run build
```

## Thresholds / Coverage Gates

- Repository structure violations: 0.
- Filename/slug policy violations: 0.
- Lifecycle metadata violations: 0.
- CODEOWNERS coverage gaps for content paths: 0.

## CI Merge Gates

Required checks:

- `content-repo-structure-check`
- `content-file-naming-check`
- `content-lifecycle-metadata-check`
- `content-codeowners-coverage-check`
- `content-policy-snapshot-test`
- `website-content-policy-verify`

## Regression / Safety Notes

- Policy checks must run on both content-only and website-consuming pipelines.
- No bypasses on `main` for organization-policy checks.
- Any temporary waiver must include owner, expiry date, and remediation issue link.
