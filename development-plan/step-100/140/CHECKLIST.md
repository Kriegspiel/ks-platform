# Step 140 Checklist

Use this as the execution checklist when implementing slice `140`.

## Planning And Context

- [ ] Re-read [development-plan/README.md](../../README.md)
- [ ] Re-read [development-plan/PLAN.md](../../PLAN.md)
- [ ] Re-read [step-100 README](../README.md)
- [ ] Re-read [INFRA.md](../../../INFRA.md)
- [ ] Claim slice `140` in [step-100/PROGRESS.md](../PROGRESS.md)

## Files To Create

- [ ] `.env.example`
- [ ] `src/app/requirements.txt`
- [ ] `src/app/requirements-dev.txt`
- [ ] `src/app/Dockerfile`
- [ ] `docker-compose.yml`
- [ ] `src/nginx/nginx.conf`
- [ ] `src/nginx/conf.d/kriegspiel-dev.conf`
- [ ] `src/mongo/init-replica.sh`
- [ ] optional thin validation helper scripts, if needed

## Implementation Tasks

- [ ] Define the repo env contract, including `SITE_ORIGIN`
- [ ] Add pinned Python dependency files
- [ ] Add backend Dockerfile
- [ ] Add Compose services and profiles
- [ ] Add NGINX rate-limit zones in the top-level config
- [ ] Add dev proxy config for `/api/` and `/auth/`
- [ ] Add Mongo replica-set bootstrap script

## Automated Verification Tasks

- [ ] Run `docker compose config`
- [ ] Build the backend image
- [ ] Syntax-check the replica-init script
- [ ] Syntax-check NGINX config
- [ ] Bring up the dev stack automatically
- [ ] Probe `/health`
- [ ] Verify the Mongo replica set is initialized
- [ ] Tear the stack down cleanly

## Required Commands

- [ ] `docker compose config`
- [ ] `docker build -f src/app/Dockerfile src`
- [ ] `bash -n src/mongo/init-replica.sh`
- [ ] `docker run --rm -v "$PWD/src/nginx/nginx.conf:/etc/nginx/nginx.conf:ro" -v "$PWD/src/nginx/conf.d:/etc/nginx/conf.d:ro" nginx:1.27-alpine nginx -t`
- [ ] `docker compose --profile dev up -d --build`
- [ ] `curl --fail http://localhost:8000/health`
- [ ] `docker compose exec -T mongo mongosh --quiet --eval 'rs.status().ok'`
- [ ] `docker compose down -v`

## Before Marking Done

- [ ] Record exact command results in [step-100/PROGRESS.md](../PROGRESS.md)
- [ ] Confirm the stack comes up from a clean repo state
- [ ] Confirm no validation step depended on manual intervention
- [ ] Leave handoff notes for slice `150` and later infra work
