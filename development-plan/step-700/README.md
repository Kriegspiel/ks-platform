# Step 700 - Infra and Operations

## Goal

Operationalize the platform for repeatable deploys, stable runtime behavior, and auditable production readiness.

This step turns feature-complete application behavior from Step 600 into deployable infrastructure with enforceable CI quality gates.

## Read First

- [INFRA.md](../../INFRA.md)
- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [development-plan/PLAN.md](../PLAN.md)
- [development-plan/step-600/HANDOFF.md](../step-600/HANDOFF.md)

## Depends On

- `step-600`

## Scope-Based Slices

### 710 — Container Runtime and Compose Finalization
- Hardened backend Dockerfile (non-root, healthcheck, deterministic copy/install)
- Multi-stage frontend Dockerfile producing immutable build artifacts
- Final `docker-compose.yml` layout with explicit profiles (`dev`, `prod`) and service dependencies
- Shared volume contract for frontend dist handoff to NGINX

### 720 — NGINX Production and Dev Routing Policy
- Base NGINX config with tuned worker/log/rate-limit/gzip settings
- Production TLS + ACME + SPA routing + cache headers config
- Dev HTTP-only config for local/CI runs
- Header/caching/rate-limit policy alignment with API/auth threat model

### 730 — CI/CD Workflow Gates
- GitHub Actions workflow with backend + frontend + deploy stages
- Required pass criteria for lint/tests/build
- Main-branch-only deploy gate
- Artifact/log visibility suitable for incident triage

### 740 — Backup, Restore, and Health Operations Scripts
- Backup script with retention enforcement
- Restore script with explicit operator confirmation and failure handling
- Health script for app/service/storage checks
- Script usage contract and failure exit code behavior

### 750 — Structured Logging and Operational Telemetry
- Environment-aware structured logger configuration
- Key auth + game lifecycle log events with safe metadata
- Sensitive-data redaction policy validation
- Compose-level log readability for production triage

## Exit Criteria

- Compose can build and run app stack in dev and production profiles
- NGINX config supports SPA routing, API proxying, and TLS flow
- CI blocks bad merges via lint/test/build gates
- Backup + restore + health scripts are executable, documented, and deterministic
- Structured logging is enabled with no sensitive-data leaks

## Out of Scope

- Step 800 hardening/regression campaign
- Multi-region or blue/green deployment
- Full SRE alerting platform rollout
