# Slice 610 - Testing (Automated + Gates)

## Exact Commands

```bash
cd src && pytest tests/test_user_routes.py -v
cd src && pytest tests/test_user_service.py -v
cd src && pytest tests/test_player_features.py -k "profile or leaderboard or settings" -v
cd src && pytest -q --maxfail=1 --disable-warnings
cd src && ruff check app tests
```

## Thresholds

- Route/service targeted tests: 100% pass
- No flaky retries allowed
- Lint: zero new violations in touched files
- API latency sanity (local): profile/leaderboard endpoints median < 250ms on fixture dataset

## CI Merge Gates

Must be green before merge:
- backend unit/integration workflow
- lint workflow
- branch up-to-date with `origin/main`

## Deterministic Fixtures

- Use fixed fixture users and archived games with fixed timestamps.
- Freeze ordering fields in fixture generation.
- No random username/game-code generation without seed.

## Regression Matrix

- Existing user profile -> 200
- Missing user profile -> 404
- History page 1 -> expected rows
- History page out of range -> empty rows + valid total
- `per_page > 100` -> clamped to 100
- Leaderboard filters out inactive/low-games users
- Leaderboard rank ordering stable for ELO ties
- Settings update authenticated -> 200 persisted
- Settings update unauthenticated -> 401

## Skip Policy

Skip only when environment dependency is absent (e.g. DB container unavailable).
Any skip must include:
1. exact skipped command,
2. root cause,
3. unblock command,
4. rollback risk note in progress log.

## Smoke / Rollback Checks

Smoke:
```bash
cd src && uvicorn app.main:app --host 0.0.0.0 --port 8000
# then curl key endpoints locally
```

Rollback:
- Revert router registration in `app/main.py`
- Revert `user.py` route additions
- Revert `user_service.py` method changes
- Re-run route tests to confirm baseline restored
