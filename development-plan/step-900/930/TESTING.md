# Slice 930 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

cd content
npm ci
npm run lint:markdown
npm run lint:links
npm run validate:frontmatter
npm run build:content-index

cd ../ks-home
npm ci
npm run test -- --runInBand --watch=false
npm run test:e2e -- --grep "blog|changelog"
npm run build
npm run content:trigger:simulate -- --from=../content --verify-static-regen
npm run sitemap:generate -- --check
npm run feeds:generate -- --check
```

## Thresholds / Coverage Gates

- Frontmatter validation: 0 errors, 0 warnings for required fields.
- Broken link checker: 0 broken internal links, 0 broken relative content links.
- Blog/changelog E2E tests pass with 0 failures.
- Static-regeneration simulation must report updated artifacts for changed content entries.

## CI Merge Gates

Required checks:

- `content-lint-markdown`
- `content-link-check`
- `content-frontmatter-check`
- `content-build-index`
- `website-e2e-blog-changelog`
- `website-static-regen-on-content`
- `website-sitemap-check`
- `website-feed-check`

## Accessibility / Smoke

```bash
cd ks-home
npm run test:a11y -- --routes=/blog,/changelog
npm run test:smoke -- --routes=/blog,/changelog
```

- 0 critical accessibility failures; route smoke checks pass.
