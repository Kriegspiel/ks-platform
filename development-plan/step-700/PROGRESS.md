# Step 700 Progress

Status: IN PROGRESS
Last Updated: 2026-03-26

## Slice Checklist

- [x] `710` Container runtime and Compose finalization
- [ ] `720` NGINX production and dev routing policy
- [ ] `730` CI/CD workflow gates
- [ ] `740` Backup/restore/health operations scripts
- [ ] `750` Structured logging and operational telemetry

## Test Evidence

### 710 Evidence (rpi-server-02)
- `docker compose config -q` ✅
- BuildKit path failed on host (`client version 1.52 too new; daemon max 1.41`), fallback executed:
  - `DOCKER_BUILDKIT=0 docker compose build app frontend nginx` ✅
  - `DOCKER_BUILDKIT=0 docker compose build --no-cache app frontend` ✅
- Runtime + ordering checks:
  - `docker compose up -d mongo app frontend nginx` ✅
  - `docker compose exec -T app sh -lc 'id && test "$(id -u)" != "0"'` ✅ (uid 999)
  - `curl -fsS http://localhost:18080/` + `curl -fsS http://localhost:18080/api/health` repeated 3x ✅
  - `docker compose --profile dev up -d mongo-express` ✅
  - `docker compose --profile dev ps` ✅
  - `docker compose --profile dev down -v --remove-orphans` ✅
- Impacted project gates:
  - backend: `./.venv/bin/pytest -q` → `149 passed, 22 skipped, 1 warning`
  - frontend: `npm run lint` ✅
  - frontend: `npm run test -- --run` → `23 passed`
  - frontend: `npm run build` ✅

## Blockers

- Slice 720 should account for host port occupancy on this node (port `80` unavailable during 710 validation; mapped `18080` used for local verification).

## Discovery Notes

- Slice 710 implemented in ks-v2 PR #35 and merged to `main`.
- Compose startup ordering validated with `service_completed_successfully` and `service_healthy` dependencies.
- Frontend artifact handoff now uses named volume contract (`frontend_dist`) consumed by nginx.

## Handoff

- Proceed to `step-700/720` packet.
- Preserve 710 evidence references in subsequent slice PR(s).
