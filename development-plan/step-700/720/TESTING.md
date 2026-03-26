# Slice 720 - Testing (Automated + Gates)
## Exact Commands
```bash
docker compose exec -T nginx nginx -t
docker compose up -d nginx app frontend
curl -I http://localhost/
curl -I http://localhost/lobby
curl -I http://localhost/game/abc123
curl -fsS http://localhost/api/health
for i in $(seq 1 20); do curl -s -o /dev/null -w "%{http_code}\n" -X POST http://localhost/auth/login; done
```
## Thresholds / Coverage Gates
- `nginx -t` passes.
- SPA deep-link routes return 200/304.
- API health proxy returns 200.
- Auth burst test demonstrates throttling (>=1 response 429).
## CI Merge Gates
- NGINX syntax job + integration smoke required.
## Deterministic Fixtures/Seeding
- Fixed upstream names/ports from compose; deterministic burst script.
## Regression Matrix
- prod/dev config syntax valid; SPA fallback works; API proxy works; rate limits active; assets cache headers present.
## Skip Policy + Prereqs
- Skip only if nginx container cannot start; document risk.
## Post-Deploy Smoke + Rollback
```bash
curl -fsS http://localhost/
curl -fsS http://localhost/api/health
# rollback
git checkout -- src/nginx/nginx.conf src/nginx/conf.d/kriegspiel.conf src/nginx/conf.d/kriegspiel-dev.conf && docker compose restart nginx
```
