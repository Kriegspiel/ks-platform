# Slice 950 - Implementation Plan

## Files / Areas

- CI workflow definitions (preview + production)
- Smoke and regression automation scripts
- Visual regression baseline config
- Ops runbook and ownership docs
- Deploy failure handling and rollback automation

## Tasks

1. Implement ephemeral preview environment workflow per PR for both `ks-home` and `Kriegspiel/content` changes.
2. Add required gates: markdown lint, frontmatter validation, link check, build, sitemap check, feed check, unit, E2E, accessibility, visual regression, SEO validation.
3. Ensure content PR previews use regenerated static output from content branch artifacts.
4. Add production smoke suite for required routes and critical assets.
5. Implement rollback mechanism (redeploy previous artifact/tag) and automated validation command.
6. Define failed-deploy behavior: block rollout, auto-trigger rollback, run rollback smoke checks, and page release owner.
7. Publish runbook with owner matrix (content owner, engineering owner, release owner, approver).
8. Define incident triggers and freeze criteria for content-site releases.

## Acceptance Criteria

- PR previews spin up automatically and are attached to website and content pull requests.
- Content PR previews prove static regeneration output prior to merge.
- Production deploy is blocked unless all required checks pass.
- Failed deploy executes rollback path with successful smoke validation.
- Rollback drill is documented and validated with command evidence.
- Required-route regression matrix reports PASS before launch approval.
