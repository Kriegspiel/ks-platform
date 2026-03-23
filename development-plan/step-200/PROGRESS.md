# Step 200 Progress

Status: IN PROGRESS
Last Updated: 2026-03-22

## Slice Checklist

- [x] `210` User model, auth DTOs, password hashing, UserService
- [ ] `220` Session service, auth dependency, backend auth routes
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

## Blockers

- None for slice 210.

## Notes

- Next slice remains `220` (session service + auth routes).
- Keep backend-first order: `220 -> 250` before frontend hardening signoff.
