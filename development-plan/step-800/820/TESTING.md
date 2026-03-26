# Slice 820 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail

# Security-focused backend tests
cd src
PYTHONHASHSEED=0 TEST_RANDOM_SEED=820 pytest tests/security -q --maxfail=1

# Targeted auth + authorization regression
PYTHONHASHSEED=0 TEST_RANDOM_SEED=820 pytest tests -q -k "auth or session or permission or forbidden" --maxfail=1

# Static dependency audit (non-blocking medium, blocking high/critical)
cd ../frontend
npm audit --audit-level=high
cd ../src
pip-audit --strict

# Runtime header/cookie verification (compose env assumed up)
curl -si http://localhost/api/auth/session | tee /tmp/ks-auth-session-headers.txt
grep -Ei "set-cookie|httponly|samesite" /tmp/ks-auth-session-headers.txt
```

## Thresholds / Coverage Gates

- 0 failures in `tests/security` lane.
- High/Critical dependency vulnerabilities: **0 allowed** at merge.
- Auth + authorization focused regression subset must pass fully.
- Security-labeled test coverage target: **>= 90% of listed security requirements** in matrix.

## CI Merge Gates

Required checks:

- `security-tests`
- `dependency-audit`
- `authz-regression`

Any failing high/critical audit or failing security test blocks merge.

## Deterministic Fixtures / Seeding

- Fixed seed `TEST_RANDOM_SEED=820` and deterministic test users/game IDs.
- Use stable fixture payload corpus (`fixtures/security/*.json`) with version pinning.
- Rate-limit tests run serially to avoid cross-test contamination.

## Regression Matrix

- Cookie flags (`HttpOnly`, `SameSite`, secure-mode behavior)
- Expired/invalid session -> `401`
- Non-participant poll/review -> `403`
- Hidden-piece leakage absent from opponent payloads
- Malformed input rejected with `4xx`, not `500`
- Error payloads omit stack traces in production profile
- Logs redact secrets/tokens/password-like fields
- Rate-limit on login/abuse endpoints enforced

## Skip Policy + Prereqs

- Prereqs: compose stack up, test accounts seeded, edge proxy enabled for rate-limit verification.
- Skip only for infra unavailability (e.g., proxy lane unavailable) and must include mitigation + rerun deadline.
- Cannot skip auth/session/authz core lanes for release branch.

## Post-Deploy Smoke + Rollback

```bash
# smoke: verify security baseline still active
curl -fsS http://localhost/api/health
curl -si http://localhost/api/auth/session | grep -Ei "set-cookie|httponly|samesite"

# rollback check
git revert --no-edit HEAD
cd src && PYTHONHASHSEED=0 TEST_RANDOM_SEED=820 pytest tests/security -q --maxfail=1
```
