# Slice 750 - Testing (Automated + Gates)
## Exact Commands
```bash
cd src && pytest tests/test_logging.py -v
cd src && pytest tests/test_auth.py -k "login or register" -v
cd src && pytest tests/test_game_service.py -k "create or join or resign or complete" -v
cd src && ENV=production pytest tests/test_logging.py -k json -v
cd src && pytest -q
docker compose logs app | tail -n 500 > /tmp/app.log
rg -n "password|session_id|token=" /tmp/app.log && exit 1 || true
```
## Thresholds / Coverage Gates
- logging/auth/game test subsets all pass.
- production logs are valid JSON lines.
- sensitive-data grep guard returns zero forbidden hits.
## CI Merge Gates
- backend tests + log scan guard required.
## Deterministic Fixtures/Seeding
- fixed IDs and frozen timestamps in logging assertions.
## Regression Matrix
- dev log renderer readable; prod renderer json; auth/game/move events emitted; sensitive terms absent.
## Skip Policy + Prereqs
- log tail scan may be skipped only if app container unavailable; unit tests remain mandatory.
## Post-Deploy Smoke + Rollback
```bash
docker compose up -d app
curl -fsS http://localhost/api/health
docker compose logs app | tail -n 100
# rollback
git checkout -- src/app/main.py src/app/routers/auth.py src/app/services/game_service.py
```
