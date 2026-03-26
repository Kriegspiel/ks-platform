# Slice 710 - Testing (Automated + Gates)
## Exact Commands
```bash
docker compose config -q
DOCKER_BUILDKIT=1 docker compose build --pull app frontend nginx
DOCKER_BUILDKIT=1 docker compose build --pull --no-cache app frontend

docker compose up -d mongo app frontend nginx
docker compose ps
docker compose exec -T app sh -lc 'id && test "$(id -u)" != "0"'
curl -fsS http://localhost/ >/dev/null
curl -fsS http://localhost/api/health
docker compose --profile dev up -d mongo-express
docker compose --profile dev ps
docker compose down -v
```
## Thresholds / Coverage Gates
- Compose config parse passes.
- Clean no-cache build succeeds.
- App runs non-root.
- Root and API health checks pass 3x consecutively.
## CI Merge Gates
- Compose validation + backend + frontend jobs required green.
## Deterministic Fixtures/Seeding
- Fixed env values, pinned tags/digests, no `latest` for prod.
## Regression Matrix
- config valid; builds pass; non-root enforced; root serves UI; API proxy works; dev profile adds mongo-express.
## Skip Policy + Prereqs
- Skip only if Docker daemon unavailable; log command, reason, unblock step, risk.
## Post-Deploy Smoke + Rollback
```bash
docker compose up -d && docker compose ps
curl -fsS http://localhost/
curl -fsS http://localhost/api/health
# rollback
git checkout -- docker-compose.yml src/app/Dockerfile frontend/Dockerfile && docker compose up -d
```
