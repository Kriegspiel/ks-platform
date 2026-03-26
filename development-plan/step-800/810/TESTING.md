# Slice 810 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

# Backend regression + coverage gate
cd src
PYTHONHASHSEED=0 TEST_RANDOM_SEED=800 pytest tests -q \
  --maxfail=1 --disable-warnings \
  --cov=app --cov-report=term-missing --cov-fail-under=85

# Frontend regression + coverage gate
cd ../frontend
CI=1 npm ci
CI=1 npm run test -- --runInBand --coverage --watch=false
CI=1 npm run test:coverage:check -- --lines 80 --functions 80 --branches 75 --statements 80

# Integration/API smoke lane
cd ../src
PYTHONHASHSEED=0 TEST_RANDOM_SEED=800 pytest tests/integration -q -m "not slow" --maxfail=1
```

## Thresholds / Coverage Gates

- Backend line coverage **>= 85%** (`--cov-fail-under=85` hard fail).
- Frontend coverage minimums: lines/functions/statements **>= 80%**, branches **>= 75%**.
- Integration non-slow lane must pass with 0 failures.
- Flake budget: 0 tolerated on required checks.

## CI Merge Gates

Required checks on `main` protection:

- `backend-regression`
- `frontend-regression`
- `integration-smoke`
- `lint` (backend + frontend)

PR merge blocked unless all required checks pass.

## Deterministic Fixtures / Seeding

- `PYTHONHASHSEED=0` and `TEST_RANDOM_SEED=800` required for backend/integration lanes.
- Freeze test time via project time-freezing helper where available.
- Integration tests must use isolated ephemeral DB namespace per run.

## Regression Matrix

- Auth: register/login/logout/session-expiry
- Lobby: create/join/list game race-safe behavior
- Gameplay: legal move, illegal move, turn order, completion states
- Review: transcript retrieval and replay pagination
- Infra-adjacent: `/api/health`, startup readiness, static asset serve path

Each row marked PASS/WAIVED with command output evidence.

## Skip Policy + Prereqs

- Allowed skip reasons: missing Docker daemon (integration only), CI outage, third-party registry outage.
- Skips require: command attempted, failure output, owner, mitigation ETA, risk statement.
- Backend/frontend regression lanes cannot be skipped for `main` merges.

## Post-Deploy Smoke + Rollback

```bash
# smoke
curl -fsS http://localhost/api/health
curl -fsS http://localhost/ >/dev/null

# rollback validation (if regression introduced)
git revert --no-edit HEAD
# run minimum required lane to verify rollback stability
cd src && PYTHONHASHSEED=0 TEST_RANDOM_SEED=800 pytest tests/integration -q -m "not slow"
```
