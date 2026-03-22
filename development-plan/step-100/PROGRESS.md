# Step 100 Progress

Status: IN PROGRESS
Last Updated: 2026-03-22

## Slice Checklist

- [x] `110` Backend: App factory, settings, health endpoint
- [x] `120` MongoDB Motor wiring
- [ ] `130` React frontend scaffold
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

## Blockers

- No blockers for slices `110` and `120`.
- Remaining slices (`130`–`150`) pending implementation.

## Notes

- Slice `110` moved runtime entrypoint to scaffolded `app.main` path while preserving backward compatibility via `backend/main.py` shim.
- Slice `120` keeps app import-time free of network I/O and degrades `/health` to `503` when DB is unavailable.
- Keep recording exact test commands/outcomes here for every subsequent slice.

## Handoff

- Start slice `130` (frontend scaffold) next.
