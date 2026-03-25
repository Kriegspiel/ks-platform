# Slice 640 - Testing (Automated + Gates)

## Exact Commands

```bash
cd frontend && npm run test -- Join Lobby
cd frontend && npm run test -- --coverage src/pages/Join.jsx src/pages/Lobby.jsx
cd frontend && npm run lint
cd src && pytest tests/test_game_routes.py -k join -v
```

## Thresholds

- Join/lobby tests: 100% pass
- Coverage on `Join.jsx`: >= 90% lines (critical routing page)
- Auth redirect path assertions included
- Lint clean for touched files

## CI Merge Gates

Must be green:
- frontend tests/lint
- backend join route tests

## Deterministic Fixtures

- Fixed game codes and game IDs in mocks
- Fixed API error payloads for full/not-found states
- No tests depending on random generated join codes

## Regression Matrix

- Valid join code -> redirect to game
- Invalid code -> error + lobby link
- Full game -> error + lobby link
- Unauthenticated path -> login redirect + return URL
- Duplicate mount/render does not double-post join request
- Lobby displays correct join URL format

## Skip Policy

No skip for join tests; this is release-critical navigation.
If backend fixtures missing, create deterministic test fixture and rerun.

## Smoke / Rollback Checks

Smoke:
```bash
cd frontend && npm run dev -- --host 0.0.0.0 --port 4173
# test /join/<valid>, /join/<invalid>, and logged-out flow
```

Rollback:
- Remove `/join/:gameCode` route
- Revert `Join.jsx` and lobby join-link changes
- Re-run join tests to validate baseline
