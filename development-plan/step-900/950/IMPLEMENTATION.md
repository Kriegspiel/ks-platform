# Slice 950 - Implementation Plan

## Files / Areas

- CI workflow definitions (preview + production)
- Smoke and regression automation scripts
- Visual regression baseline config
- Ops runbook and ownership docs

## Tasks

1. Implement ephemeral preview environment workflow per PR (website + content integration).
2. Add required gates: lint, unit, E2E, accessibility, visual regression, link check, SEO validation.
3. Add production smoke suite for required routes and critical assets.
4. Implement rollback mechanism (redeploy previous artifact/tag) and automated validation command.
5. Publish runbook with owner matrix (content owner, engineering owner, release owner, approver).
6. Define incident triggers and freeze criteria for content-site releases.

## Acceptance Criteria

- PR previews spin up automatically and are attached to pull requests.
- Production deploy is blocked unless all required checks pass.
- Rollback drill is documented and validated with command evidence.
- Required-route regression matrix reports PASS before launch approval.
