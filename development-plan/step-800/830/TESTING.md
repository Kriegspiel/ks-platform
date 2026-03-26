# Slice 830 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

# Bring stack up for failure-path tests
cd /home/fil/dev/kriegspiel/ks-platform
docker compose up -d mongo app frontend nginx

# Backend failure-path + race tests
cd src
PYTHONHASHSEED=0 TEST_RANDOM_SEED=830 pytest tests -q -k "race or timeout or outage or resilience or recovery" --maxfail=1

# Frontend failure UX tests
cd ../frontend
CI=1 npm run test -- --runInBand -t "error boundary|api failure|retry"

# Induced outage smoke (manual scripted)
cd ..
docker compose stop mongo
curl -s -o /tmp/ks-outage-health.txt -w "%{http_code}" http://localhost/api/health
cat /tmp/ks-outage-health.txt
docker compose start mongo
sleep 5
curl -fsS http://localhost/api/health
```

## Thresholds / Coverage Gates

- Failure/race test subset pass rate: **100%** (no flaky allowance in required lane).
- Frontend error UX suite pass rate: **100%**.
- Outage health transition: unhealthy during outage, healthy within **60s** after dependency recovery.
- No data corruption assertions failing in post-recovery consistency checks.

## CI Merge Gates

Required checks:

- `resilience-tests`
- `frontend-error-ux`
- `recovery-smoke`

Merge blocked on any failure in these checks.

## Deterministic Fixtures / Seeding

- Use fixed seed `TEST_RANDOM_SEED=830` and deterministic game fixture set.
- Concurrency tests use controlled parallelism (`pytest -n 2` only where explicitly deterministic).
- DB fixture reset before each resilience suite run.

## Regression Matrix

- DB outage -> health degrade + graceful API behavior
- Simultaneous join -> single winner + deterministic loser code (`409`)
- Duplicate completion action (double resign/move on completed game) -> idempotent/guarded response
- Invalid session under load -> `401` without server crash
- Long transcript/review fetch -> bounded latency and no frontend crash

## Skip Policy + Prereqs

- Prereqs: Docker available, compose services healthy before fault injection, test fixture seed job succeeds.
- Skip allowed only for unavailable Docker host/CI runner limitations; must include risk + rerun ticket.
- Concurrency/failure lanes are required for release candidate tags.

## Post-Deploy Smoke + Rollback

```bash
# smoke after deployment
curl -fsS http://localhost/api/health
curl -fsS http://localhost/ >/dev/null

# basic rollback drill after intentionally bad deploy candidate
git revert --no-edit HEAD
docker compose up -d --build
curl -fsS http://localhost/api/health
```
