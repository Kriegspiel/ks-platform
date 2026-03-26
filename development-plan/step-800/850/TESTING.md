# Slice 850 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail
cd /home/fil/dev/kriegspiel/ks-platform

# Pre-launch must-pass bundle
cd src
PYTHONHASHSEED=0 TEST_RANDOM_SEED=850 pytest tests -q --maxfail=1 --cov=app --cov-fail-under=85
cd ../frontend
CI=1 npm run test -- --runInBand --coverage --watch=false

# Deploy candidate and smoke
docker compose up -d --build mongo app frontend nginx
curl -fsS http://localhost/api/health
curl -fsS http://localhost/ >/dev/null

# Critical end-to-end API smoke (example script/commands)
cd ../src
PYTHONHASHSEED=0 TEST_RANDOM_SEED=850 pytest tests/e2e -q -m "launch_smoke" --maxfail=1

# Rollback drill
cd ..
ROLLBACK_START=$(date +%s)
git revert --no-edit HEAD
docker compose up -d --build
curl -fsS http://localhost/api/health
ROLLBACK_END=$(date +%s)
echo "RollbackSeconds=$((ROLLBACK_END-ROLLBACK_START))"
```

## Thresholds / Coverage Gates

- Backend coverage remains **>= 85%**.
- Launch-smoke E2E lane pass rate: **100%**.
- Post-deploy smoke endpoints return success 3 consecutive checks.
- Rollback drill completes within **<= 10 minutes** end-to-end.

## CI Merge Gates

Required checks:

- `release-regression`
- `release-security-gates`
- `release-smoke`
- `rollback-drill` (for release branch/tag workflow)

Release tag creation blocked unless all required checks are green.

## Deterministic Fixtures / Seeding

- Use fixed seed `TEST_RANDOM_SEED=850` across release verification lanes.
- Launch-smoke fixtures use immutable test users and deterministic game scripts.
- Use clean DB snapshot/fixture restore prior to smoke run.

## Regression Matrix

- Auth journey: register/login/logout/session expiry
- Core gameplay journey: create/join/play/resign/complete
- Review/leaderboard/settings journey: read and update paths
- Hidden-information enforcement journey
- Ops journey: health, backup status, structured logs present

## Skip Policy + Prereqs

- Prereqs: all prior slices complete, release candidate branch cut, deployment environment available.
- No skips allowed for launch-smoke, security, or rollback checks on go/no-go day.
- Any deferred item requires explicit risk acceptance from release owner.

## Post-Deploy Smoke + Rollback

- Post-deploy smoke is part of required commands above and must pass before launch signoff.
- Rollback drill output (`RollbackSeconds`) must be logged in launch evidence packet.
