# Step 200 Progress

Status: IN PROGRESS
Last Updated: 2026-03-23

## Slice Checklist

- [x] `210` User model, auth DTOs, password hashing, UserService
- [x] `220` Session service, auth dependency, backend auth routes
- [ ] `230` React auth context + login/register pages
- [ ] `240` Navigation/auth UX integration and styling pass
- [ ] `250` Backend auth integration + regression tests

## Planning Packet Checklist

- [x] Slice folders `210/220/230/240/250` created
- [x] Per-slice `README.md`, `IMPLEMENTATION.md`, `TESTING.md`, `CHECKLIST.md` created
- [x] Auth decision (username+email+password now, passwordless later) embedded in step + slice docs
- [x] Testing expectations include exact commands + expected pass/fail/skip semantics
- [x] Integration prerequisites + smoke checks documented per slice

## Test Evidence

### Slice 210 (ks-v2 PR #10, merged)

- Branch: `step-200-slice-210`
- PR: https://github.com/Kriegspiel/ks-v2/pull/10
- Merge commit: `b65efa0852f98346e62575de1dec486394e323a5`

Commands executed against `ks-v2` branch worktree (`/tmp/ksv2-step210`):

```bash
cd backend && uv run pytest src/tests/test_user_models.py src/tests/test_user_service.py -v
# result: PASS (8 passed, 0 skipped)

cd backend && uv run pytest src/tests/test_user_models.py src/tests/test_user_service.py --cov=app.models.auth --cov=app.models.user --cov=app.services.user_service --cov-fail-under=90 -v
# result: PASS (8 passed, 0 skipped), total coverage 93.92%

cd backend/src && ../.venv/bin/ruff check app tests
# result: PASS

cd backend/src && ../.venv/bin/black --check app tests
# result: PASS
```

Slice 210 acceptance delivered:
- register DTO enforces required `username` + `email` + `password`
- username format and password length/complexity rules validated
- `create_user()` stores canonical lowercase username, `username_display`, bcrypt `password_hash`, and verification-ready email fields (`email_verified`, `email_verification_sent_at`, `email_verified_at`)
- `authenticate()` returns user on valid credentials and `None` otherwise
- duplicate username/email collisions raise deterministic typed domain conflicts for 409 mapping

### Slice 220 (ks-v2 PR #11 + fix PR #14, merged)

- Branches: `step-200-slice-220`, `step-200-slice-220-fix-tz`
- PRs:
  - https://github.com/Kriegspiel/ks-v2/pull/11
  - https://github.com/Kriegspiel/ks-v2/pull/14
- Merge commits:
  - `5e27ca1b57fe78cd39d0de831ffd65a34e55204e`
  - `4133e05eb579eb27bec108718c2130c7a0ac663d`

Commands executed against `ks-v2` worktrees (`/tmp/ksv2-step220`, `/tmp/ksv2-step220-fix/backend/src`):

```bash
cd backend/src && uv run pytest tests/test_auth_routes.py tests/test_session_service.py tests/test_dependencies.py -v
# result: PASS (13 passed, 4 skipped)

cd backend/src && uv run pytest tests/test_auth_routes.py tests/test_session_service.py tests/test_dependencies.py --cov=app.routers.auth --cov=app.services.session_service --cov=app.dependencies --cov-fail-under=90 -v
# result: PASS (13 passed, 4 skipped), total coverage 98.18%

cd backend/src && uv run python -m compileall app tests
# result: PASS

cd backend/src && uv run ruff check app tests
# result: PASS

cd backend/src && uv run black --check app tests
# result: PASS
```

Runtime smoke check on deployed stack (`http://localhost:18000`):
- `POST /auth/register` => 201 and session cookie issued
- `GET /auth/me` (with cookie) => 200 user payload
- `POST /auth/logout` => 200 and cookie cleared
- `GET /auth/me` after logout => 401

Slice 220 acceptance delivered:
- Added `SessionService` with create/read/delete lifecycle and expiry extension
- Added `get_current_user` dependency for cookie/session-based auth checks
- Added `/auth/register`, `/auth/login`, `/auth/logout`, `/auth/me` router and wired into app factory
- Enforced required `username` + `email` + `password` registration contract from Slice 210
- Added tests for route behavior, dependency behavior, and session service expiry handling (including naive Mongo datetime normalization)

## Blockers

- None for slice 210 or 220.

## Notes

- Next slices: `230` then `240`, followed by `250` backend auth regression hardening.
- Keep backend/frontend sequencing aligned with packet dependencies.
