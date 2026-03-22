# Step 100 Progress

Status: IN PROGRESS
Last Updated: 2026-03-22

## Slice Checklist

- [x] `110` Backend: App factory, settings, health endpoint
- [x] `120` MongoDB Motor wiring
- [x] `130` React frontend scaffold
- [ ] `140` Dev environment files
- [ ] `150` Test harness and smoke tests

## Test Evidence

### Slice 110 (implemented in `ks-v2`, merged)

Implementation branch: `feat/step-110-app-factory`  
PR: <https://github.com/Kriegspiel/ks-v2/pull/1>

Commands run from `ks-v2/backend`:

1. `cd src && pytest tests/test_config.py tests/test_app_factory.py tests/test_health.py -v`
   - Result: **13 passed**

2. `cd src && pytest tests/test_config.py tests/test_app_factory.py tests/test_health.py --cov=app.config --cov=app.main --cov-fail-under=90 -v`
   - Result: **13 passed**
   - Coverage:
     - `app/config.py` 100%
     - `app/main.py` 100%
     - total 100%

3. `cd src && python -m compileall app tests`
   - Result: success

4. `cd src && ruff check app tests`
   - Result: success

5. `cd src && black --check app tests`
   - Result: success

### Slice 120 (implemented in `ks-v2`, merged)

Implementation branch: `feat/step-120-mongo-motor`  
PR: <https://github.com/Kriegspiel/ks-v2/pull/2> (merged)

Scope delivered:
- Added Motor DB lifecycle module (`init_db`, `get_db`, `close_db`)
- Wired lifespan startup/shutdown to DB readiness state on `app.state`
- Added required indexes for `users`, `games`, `game_archives`, `audit_log`, `sessions`
- Upgraded `/health` to return connected/disconnected DB contracts
- Added unit + integration automation for DB lifecycle, indexes, and health behavior

Commands run from `ks-v2/backend`:

1. `cd src && pytest tests/test_db.py tests/test_health.py -v`
   - Result: **8 passed, 1 skipped** (integration test intentionally skipped in unit run)

2. `cd src && pytest tests/test_db.py tests/test_health.py --cov=app.db --cov=app.main --cov-fail-under=90 -v`
   - Result: **8 passed, 1 skipped**
   - Coverage:
     - `app/db.py` 96%
     - `app/main.py` 90%
     - total 93%

3. `cd src && python -m compileall app tests`
   - Result: success

4. `cd src && ruff check app tests`
   - Result: success

5. `cd src && black --check app tests`
   - Result: success

6. `./scripts/test-step-120.sh`
   - Result: **pass**
   - Disposable MongoDB mechanism: ephemeral `mongo:7` Docker container spun up and torn down by script.


### Slice 130 (implemented in ks-v2, PR open)

Implementation branch: feat/step-130-react-scaffold  
PR: <https://github.com/Kriegspiel/ks-v2/pull/3>

Scope delivered:
- Vite React scaffold route shell with deterministic placeholders for /, /auth/login, /auth/register, /lobby, /game/:gameId
- Shared Axios client configured for proxy-friendly relative baseURL and withCredentials enabled
- Vite dev proxy wiring for /api and /auth to http://localhost:8000
- Frontend smoke-test harness with Vitest + Testing Library

Commands run from ks-v2/frontend:

1. npm install
   - Result: pass (engine warnings only; host Node v18 while vite/react-router metadata prefers >=20)

2. npm run test -- --run
   - Result: 8 passed

3. npm run lint
   - Result: success

4. npm run build
   - Result: success

## Blockers

- No blockers for slices `110` and `120`.
- Slice `130` complete; remaining slices `140` and `150` pending implementation.

## Notes

- Slice `110` moved runtime entrypoint to scaffolded `app.main` path while preserving backward compatibility via `backend/main.py` shim.
- Slice `120` keeps app import-time free of network I/O and degrades `/health` to `503` when DB is unavailable.
- Keep recording exact test commands/outcomes here for every subsequent slice.

## Handoff

- Start slice `140` (dev environment files) next.

### Slice 140 (implemented in ks-v2, merged)

Implementation branch: feat/step-140-dev-environment-files
PR: https://github.com/Kriegspiel/ks-v2/pull/4 (merged)
Merge commit: 25ba37b17a4d0abdf06edaa29a29f94f4633626f

Test evidence (ks-v2 root):
- docker compose config -> pass
- docker build -f backend/src/app/Dockerfile backend/src -> pass
- bash -n backend/src/mongo/init-replica.sh -> pass
- nginx config test (nginx:1.27-alpine, nginx -t) -> pass
- DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 docker compose --profile dev up -d --build -> pass
- curl --fail --silent http://localhost:18000/health -> pass ({"status":"ok","db":"connected"})
- docker compose exec -T mongo mongosh --quiet --eval rs.status().ok -> pass (1)
- DOCKER_BUILDKIT=0 COMPOSE_DOCKER_CLI_BUILD=0 docker compose --profile dev down -v -> pass

Notes:
- Host ports 8000 and 8080 were already allocated on rpi-server-02; validation used 18000 (app) and 18080 (nginx).
- BuildKit API mismatch on this host required legacy compose build mode for validation.
