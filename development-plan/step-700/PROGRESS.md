# Step 700 Progress

Status: DONE
Last Updated: 2026-03-26

## Slice Checklist

- [x] `710` Container runtime and Compose finalization
- [x] `720` NGINX production and dev routing policy
- [x] `730` CI/CD workflow gates
- [x] `740` Backup and restore and health operations scripts
- [x] `750` Structured logging and operational telemetry

## Test Evidence

### 710 Evidence (rpi-server-02)
- `docker compose config -q` ✅
- BuildKit path failed on host (`client version 1.52 too new; daemon max 1.41`), fallback executed:
  - `DOCKER_BUILDKIT=0 docker compose build app frontend nginx` ✅
  - `DOCKER_BUILDKIT=0 docker compose build --no-cache app frontend` ✅
- Runtime and ordering checks:
  - `docker compose up -d mongo app frontend nginx` ✅
  - `docker compose exec -T app sh -lc id` ✅ (uid 999)
  - `curl -fsS http://localhost:18080/` and `curl -fsS http://localhost:18080/api/health` repeated 3x ✅
  - `docker compose --profile dev up -d mongo-express` ✅
  - `docker compose --profile dev ps` ✅
  - `docker compose --profile dev down -v --remove-orphans` ✅
- Impacted project gates:
  - backend: `./.venv/bin/pytest -q` -> `149 passed, 22 skipped, 1 warning`
  - frontend: `npm run lint` ✅
  - frontend: `npm run test -- --run` -> `23 passed`
  - frontend: `npm run build` ✅

### 720 Evidence (rpi-server-02)
- ks-v2 PR merged: https://github.com/Kriegspiel/ks-v2/pull/36
- Merge commit: `80201205181a698e960ad55874de4aa4337205ff`
- Config artifacts:
  - `backend/src/nginx/nginx.conf` (hardening baseline and gzip and limit zones)
  - `backend/src/nginx/conf.d/kriegspiel.conf` (prod TLS and ACME plus route map and headers)
  - `backend/src/nginx/conf.d/kriegspiel-dev.conf` (dev parity route map)
  - `backend/src/nginx/tests/slice720_smoke.sh` (deterministic smoke)
- Validation gates:
  - `docker compose exec -T nginx nginx -t` ✅
  - SPA deep-link checks (`/`, `/lobby`, `/game/abc123`) -> HTTP 200 ✅
  - `curl http://localhost:18080/api/health` -> HTTP 200 ✅
  - Auth burst (20x POST `/auth/login`) -> `429` observed (9/20) ✅
  - Asset cache header present (`Cache-Control: public, max-age=3600, immutable`) ✅
- Impacted project gates:
  - backend: `./.venv/bin/pytest -q` -> `149 passed, 22 skipped, 1 warning` ✅
  - frontend: `npm run lint` ✅
  - frontend: `npm run test -- --run` -> `23 passed` ✅
  - frontend: `npm run build` ✅

### 730 Evidence (rpi-server-02)
### 740 Evidence (rpi-server-02)
- ks-v2 PR merged: https://github.com/Kriegspiel/ks-v2/pull/38
- Merge commit: `23e9059e000f9c0d4c3e14adf544c78c583f60cf`
- Script artifacts:
  - `scripts/backup.sh` (UTC timestamped compressed dump + 30-day retention pruning)
  - `scripts/restore.sh` (path validation + explicit confirmation / `--force`)
  - `scripts/health-check.sh` (service checks + API health + disk threshold)
  - `scripts/test-step-740.sh` (deterministic scripted validation)
- CI gate updates:
  - `.github/workflows/ci.yml` adds `ops-scripts-quality` required job
  - `deploy-main` now needs `[backend, frontend, ops-scripts]`
- Local packet/gate validation:
  - `docker run --rm -v "$PWD:/mnt" -w /mnt koalaman/shellcheck:stable scripts/backup.sh scripts/restore.sh scripts/health-check.sh` ✅
  - `./scripts/backup.sh --help`, `./scripts/restore.sh --help`, `./scripts/health-check.sh --help` ✅
  - `./scripts/backup.sh` -> non-empty artifact (`backups/ks-backup-20260326T220922Z.archive.gz`, 854 bytes) ✅
  - `./scripts/restore.sh "$LATEST_BACKUP" --force` ✅
  - `./scripts/health-check.sh` ✅
  - Regression checks: invalid restore path fails safely; retention pruning verified ✅
- Impacted project gates:
  - backend: black + ruff + pytest/cov -> `149 passed, 22 skipped, 1 warning`; coverage `95.62%` ✅
  - frontend: lint + test + build -> `23 passed`; build succeeded ✅
- Evidence log: `ks-v2/.evidence/step700-slice740-20260326T220912Z.log`

- ks-v2 PR merged: https://github.com/Kriegspiel/ks-v2/pull/37
- Merge commit: `cc657ccac19bd8590a95e3b873e1d18654190cec`
- Workflow artifact: `.github/workflows/ci.yml`
  - jobs: `backend-quality`, `frontend-quality`, `deploy-main`
  - deterministic controls: `concurrency`, `PYTHONHASHSEED=0`, `TZ=UTC`, service health check, job timeouts
  - deploy gate: `if github.event_name == push && github.ref == refs/heads/main` with `needs: [backend, frontend]`
  - triage artifacts: backend JUnit + coverage XML upload, frontend dist upload
- Local verification gates:
  - `backend/.venv/bin/python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('ci.yml parse ok')"` ✅
  - `cd backend/src && ../.venv/bin/black --check app tests` ✅
  - `cd backend/src && ../.venv/bin/ruff check app tests` ✅
  - `cd backend/src && ../.venv/bin/pytest tests -v --cov=app --cov-report=term-missing --cov-fail-under=80 --cov-report=xml --junitxml=pytest-junit.xml` ✅
    - Result: `149 passed, 22 skipped, 1 warning`; coverage `95.62%`
  - `cd frontend && npm ci && npm run lint && npm run test -- --run && npm run build` ✅
    - Result: lint pass, `23 passed`, production build succeeded
- GitHub Actions evidence (PR #37):
  - `backend-quality` ✅
  - `frontend-quality` ✅
  - `deploy-main` skipped on PR by policy ✅

## Blockers

- BuildKit API mismatch persists on host (`client 1.52`, daemon max `1.41`); keep `DOCKER_BUILDKIT=0` fallback for compose-heavy validations.

## Discovery Notes

- Slice 710 implemented in ks-v2 PR #35 and merged to `main`.
- Slice 720 implemented in ks-v2 PR #36 and merged to `main`.
- Slice 730 implemented in ks-v2 PR #37 and merged to `main`.
- Compose startup ordering validated with `service_completed_successfully` and `service_healthy` dependencies.
- Frontend artifact handoff uses named volume contract (`frontend_dist`) consumed by nginx.

## Handoff

- Step 700 complete through Slice 750; transition execution focus to Step 800 packet.
- Preserve Step 700 evidence references for hardening and launch-readiness audit trails.

### 750 Evidence (rpi-server-02)
- ks-v2 PR merged: https://github.com/Kriegspiel/ks-v2/pull/39
- Merge commit: `ac95f7885e29ff76d077186fdae1d26561dda6a5`
- Logging artifacts:
  - `backend/src/app/logging_config.py` (env-aware structlog renderer: JSON prod, console dev/test)
  - `backend/src/app/routers/auth.py` (auth register/login/logout telemetry)
  - `backend/src/app/services/game_service.py` (game create/join/move/ask-any/resign telemetry)
  - `backend/src/tests/test_logging.py` (renderer contract)
  - `backend/src/tests/test_telemetry_contracts.py` (field consistency + no secret leakage contract)
- Validation gates:
  - `backend/.venv/bin/ruff check backend/src/app backend/src/tests` ✅
  - `cd backend/src && ../.venv/bin/python -m pytest tests/test_logging.py -v` ✅
  - `cd backend/src && ../.venv/bin/python -m pytest tests/test_auth.py -k "login or register" -v` ✅ (known skips)
  - `cd backend/src && ../.venv/bin/python -m pytest tests/test_game_service.py -k "create or join or resign or complete" -v` ✅
  - `cd backend/src && ENV=production ../.venv/bin/python -m pytest tests/test_logging.py -k json -v` ✅
  - `cd backend/src && ../.venv/bin/python -m pytest -q` -> `153 passed, 22 skipped, 1 warning` ✅
  - `docker compose logs app | tail -n 500 > /tmp/app.log` + `grep -En "password|session_id|token=" /tmp/app.log` -> no hits ✅
- Evidence logs:
  - `ks-v2/.evidence/step700-slice750-20260326T230009Z.log`
  - `ks-v2/.evidence/step700-slice750-lint-20260326T232137Z.log`
