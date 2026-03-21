# Step 140 Implementation Plan

## Implementation Sequence

Build this slice in the following order:

1. Define `.env.example`.
2. Add `requirements.txt` and `requirements-dev.txt`.
3. Add the backend Dockerfile.
4. Add `docker-compose.yml`.
5. Add NGINX base and dev configs.
6. Add the MongoDB replica-set init script.
7. Add any thin validation helpers needed for non-interactive verification.

## File-By-File Requirements

### `.env.example`

Required variables:

- `SECRET_KEY`
- `MONGO_URI`
- `ENVIRONMENT`
- `LOG_LEVEL`
- `SITE_ORIGIN`
- `ME_USERNAME`
- `ME_PASSWORD`

Implementation requirements:

- add short comments explaining intended values,
- keep production-sensitive values as placeholders,
- include `SITE_ORIGIN` because the backend config introduced it in slice `110`.

### `src/app/requirements.txt`

At minimum, include the packages already committed to the active plan:

- `fastapi`
- `uvicorn[standard]`
- `motor`
- `pydantic`
- `pydantic-settings`
- `bcrypt`
- `python-jose[cryptography]`
- `kriegspiel>=1.1.2`
- `structlog`
- `python-multipart`
- `httpx`

Pin versions consistently with the guidance in [INFRA.md](../../../INFRA.md).

Do not add frontend-only packages here.

### `src/app/requirements-dev.txt`

Required packages:

- reference `requirements.txt`
- `pytest`
- `pytest-asyncio`
- `pytest-cov`
- `black`
- `ruff`

If earlier slices introduced additional testing dependencies needed for automation, include them here rather than relying on ad-hoc local installs.

### `src/app/Dockerfile`

Required behavior:

- use `python:3.12-slim`,
- install minimal system packages needed by the app and health checks,
- copy and install Python requirements,
- copy the `src/` tree,
- expose port `8000`,
- start `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1`.

### `docker-compose.yml`

Required services:

- `nginx`
- `app`
- `mongo`
- `mongo-express`
- `certbot`

Required behavior:

- `app` builds from `./src` with `./app/Dockerfile`
- `app` gets environment variables from the repo env contract
- `app` depends on a healthy `mongo`
- `app` exposes port `8000` internally and has a `/health` healthcheck
- `mongo` runs `mongod --replSet rs0 --bind_ip_all`
- `mongo` mounts `src/mongo/init-replica.sh`
- `mongo-express` is on the `dev` profile only
- `certbot` is on the `production` profile only
- named volumes exist for MongoDB data and app static assets

### `src/nginx/nginx.conf`

Required behavior:

- define the `http` block,
- place rate-limit and connection-limit zones in the `http` block,
- include `/etc/nginx/conf.d/*.conf`.

### `src/nginx/conf.d/kriegspiel-dev.conf`

Required behavior:

- define a development HTTP server block,
- proxy `/api/` to `app:8000`,
- proxy `/auth/` to `app:8000`,
- serve the frontend build output at `/`,
- support SPA refreshes using `try_files` or equivalent fallback to `index.html`.

### `src/mongo/init-replica.sh`

Required behavior:

- bootstrap a single-node replica set,
- run non-interactively,
- be safe enough for repeated dev bring-up attempts,
- use a small startup delay or readiness loop before running `rs.initiate(...)`.

## Guardrails

- Do not require manual file editing after the slice is implemented.
- Do not hide validation assumptions in README prose only; the files themselves must be runnable.
- Do not place rate-limit directives in the wrong NGINX file.
- Do not make Compose depend on undeclared local paths outside the repo.

## Exact Handoff Expectations For Slice 150 And Later Infra Work

Later slices should be able to:

- install all Python tooling from the requirements files,
- bring up the local stack with Compose,
- run tests against the same env contract without inventing new variable names.
