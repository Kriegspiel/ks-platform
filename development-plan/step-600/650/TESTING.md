# Slice 650 - Testing (Automated + Gates)

## Exact Commands

```bash
cd src && pytest tests/test_player_features.py -v
cd src && pytest tests/test_player_features.py -q --maxfail=1
cd src && pytest tests/test_player_features.py --cov=app --cov-report=term-missing
cd src && pytest -q --maxfail=1
```

## Thresholds

- `test_player_features.py`: 100% pass
- Minimum 8 concrete test cases (target 10+)
- No xfail/skip in this file without explicit blocker note
- Coverage sanity for touched routes/services: >= 80% lines

## CI Merge Gates

Must be green:
- backend integration workflow
- backend coverage workflow (if separate)
- aggregate required checks on `main`

## Deterministic Fixtures

- Seed known users, games, archive rows with fixed values.
- Fix timestamps and ordering keys.
- Ensure per-test DB cleanup/reset to prevent cross-test bleed.

## Regression Matrix

- Profile existing/missing
- History default pagination
- History beyond-range pagination
- History per-page clamp
- Leaderboard filter + ordering
- Settings auth required
- Settings persist verified by follow-up read
- Moves endpoint transcript correctness

## Skip Policy

Do not skip this suite for convenience.
Only acceptable skip: infrastructure outage that blocks DB/test app startup; must log remediation and rerun before merge.

## Smoke / Rollback Checks

Smoke:
```bash
cd src && pytest tests/test_player_features.py -k "profile or leaderboard" -v
```

Rollback:
- Revert `test_player_features.py`
- Run baseline backend tests to ensure previous state is intact
- Re-apply tests in smaller commits if instability appears
