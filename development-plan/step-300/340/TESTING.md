# Step 340 - Frontend Lobby UX and Polling Flows - Testing Plan

## Integration Prerequisites

- Backend step slices 310-330 running and reachable from frontend dev server.
- Frontend dependencies installed (`frontend/package.json`).
- Auth flow from Step 200 functional for manual smoke sessions.

## Required Commands

```bash
cd frontend && npm run test -- Lobby
cd frontend && npm run test -- App
cd frontend && npm run lint
cd frontend && npm run build
```

## Expected Outcomes

- Lobby/App targeted tests: PASS (or explicit no-test harness note if command maps to Vitest/Jest pattern).
- Lint: PASS without new warnings promoted to errors.
- Build: PASS, proving route/component compile integrity.

## Runtime Smoke Checks

- Manual two-session run: user A creates game, user B joins by code, user A auto-redirects after polling detects active state.
- Verify open games panel drops joined game after activation.
- Verify my games panel shows active match with turn marker/source metadata as specified.

## Fail/Skip Handling Rules

- Capture frontend test or build failures with exact command output snippets in `step-300/PROGRESS.md`.
- If automated UI tests are skipped due to harness gaps, document gap and mandatory manual smoke evidence.
- Do not mark done if polling cleanup behavior remains unverified.
