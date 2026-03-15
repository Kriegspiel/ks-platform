# Step 700 - Infra and Operations

## Goal

Finish the operational layer: containers, proxying, CI, deployment, backup, logging, and runtime readiness.

## Read First

- [INFRA.md](../../INFRA.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [AUTH.md](../../AUTH.md)
- [MILESTONES.md](../../MILESTONES.md)

## Depends On

- `step-600`

## Task Slices

- `700.1` Finalize Docker, Compose, and NGINX configuration for the implemented app.
- `700.2` Finalize GitHub Actions for lint, tests, and deployment flow.
- `700.3` Implement backup/restore scripts, environment handling, and runtime logging/health hooks.
- `700.4` Validate VPS/deploy docs and operator workflow end-to-end.

## Required Tests Before Done

- `docker compose` boot test.
- CI workflow dry run or equivalent local reproduction.
- Backup script dry run.
- Health endpoint and logging checks under containerized startup.

## Exit Criteria

- The app runs correctly via Docker Compose.
- CI can lint and test the repo.
- Backup and health mechanisms exist and are documented.
- The deployment path is documented well enough to execute without guesswork.

## Out of Scope

- Final production launch decision
- Community/Phase 2 features
