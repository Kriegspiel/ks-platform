# Step 140 - Dev Environment Files

This folder is the detailed execution packet for slice `140` from [step-100](../README.md).

Canonical status for this slice still lives in [step-100/PROGRESS.md](../PROGRESS.md). This folder expands the slice into implementation-ready planning docs; it does not create a new top-level rollup step.

## Goal

Create the local development and containerization files that make the backend stack reproducible: environment variables, Python dependency files, Dockerfile, Docker Compose, NGINX config, and MongoDB replica-set bootstrap.

## Why This Slice Exists

Slices `110` through `130` define application code structure, but they do not make the stack reproducible for other developers or CI. This slice establishes:

- the canonical environment variable contract,
- the Python dependency installation path,
- the container build for the backend,
- the multi-service dev stack,
- the NGINX and MongoDB bootstrap files needed by local and hosted deployment.

## Read First

- [development-plan/README.md](../../README.md)
- [development-plan/PLAN.md](../../PLAN.md)
- [step-100 README](../README.md)
- [INFRA.md](../../../INFRA.md)
- [README.md](../../../README.md)

## Scope

In scope:

- `.env.example`
- Python requirements files
- backend Dockerfile
- `docker-compose.yml`
- NGINX base and dev configs
- MongoDB replica-set init script
- automated validation of Docker, NGINX, and Compose configuration

Out of scope:

- CI workflow files
- backup scripts
- production TLS issuance flow beyond placeholder `certbot` service wiring
- advanced image optimization

## Deliverables

The implementing agent should leave behind at least these files:

- `.env.example`
- `src/app/requirements.txt`
- `src/app/requirements-dev.txt`
- `src/app/Dockerfile`
- `docker-compose.yml`
- `src/nginx/nginx.conf`
- `src/nginx/conf.d/kriegspiel-dev.conf`
- `src/mongo/init-replica.sh`

The implementing agent may also add the smallest validation helper scripts needed to make signoff non-interactive.

## Contract For This Slice

The finished files must satisfy all of the following:

- `docker compose config` succeeds,
- the backend Docker image builds from `src/app/Dockerfile`,
- the Compose stack includes `app`, `mongo`, `nginx`, `mongo-express`, and `certbot`,
- `mongo-express` is restricted to the `dev` profile,
- `certbot` is restricted to the `production` profile,
- NGINX config places rate-limit zones in the top-level `http` block,
- the dev NGINX config proxies `/api/` and `/auth/` to the app container,
- the Mongo init script can bootstrap a single-node replica set non-interactively.

## Required Reading Order For The Implementing Agent

1. Read [IMPLEMENTATION.md](./IMPLEMENTATION.md)
2. Read [TESTING.md](./TESTING.md)
3. Read [CHECKLIST.md](./CHECKLIST.md)
4. Claim slice `140` in [step-100/PROGRESS.md](../PROGRESS.md) before writing code

## Definition Of Done

This slice is done only when:

- the implementation matches [IMPLEMENTATION.md](./IMPLEMENTATION.md),
- every automated validation step in [TESTING.md](./TESTING.md) passes,
- exact commands and results are recorded in [step-100/PROGRESS.md](../PROGRESS.md), and
- stack bring-up is proven by automated commands rather than a manual “it seems to work” check.

## Handoff To The Next Slices

- Slice `150` can rely on `requirements-dev.txt` and the dev stack to run automated tests.
- Step `700` can refine these files later, but should treat them as the baseline rather than recreate them from scratch.
