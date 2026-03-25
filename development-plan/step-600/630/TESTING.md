# Slice 630 - Testing (Automated + Gates)

## Exact Commands

```bash
cd frontend && npm run test -- Profile GameHistory Leaderboard Settings
cd frontend && npm run test -- --coverage src/pages/Profile.jsx src/pages/GameHistory.jsx src/pages/Leaderboard.jsx src/pages/Settings.jsx
cd frontend && npm run lint
cd frontend && npm run build
```

## Thresholds

- Page test suites: 100% pass
- Combined page coverage: >= 80% lines, >= 75% branches
- Build succeeds with zero TypeScript/ESLint blocking errors
- Pagination tests include first/last/out-of-range interactions

## CI Merge Gates

Must be green:
- frontend unit tests
- frontend lint/build
- e2e smoke (if configured)

## Deterministic Fixtures

- Mock API responses with static payloads and stable ordering.
- Use fixed dates in fixtures; avoid timezone-dependent assertions.
- Use seeded mock leaderboard for rank consistency.

## Regression Matrix

- Profile happy path render
- Profile 404 render
- History pagination next/prev
- History empty state
- Leaderboard rank order and links
- Settings load existing values
- Settings save success toast/message
- Settings API failure path handling
- Route navigation from table/list links

## Skip Policy

No voluntary skip. If environment prevents run (e.g. node_modules missing), install deps then rerun.
Any unavoidable skip requires explicit blocker entry in `step-600/PROGRESS.md`.

## Smoke / Rollback Checks

Smoke:
```bash
cd frontend && npm run dev -- --host 0.0.0.0 --port 4173
# manually hit /user/<name>, /leaderboard, /settings
```

Rollback:
- Revert page routes in `App.jsx`
- Revert API client additions in `services/api.js`
- Re-run page tests to verify pre-change baseline
