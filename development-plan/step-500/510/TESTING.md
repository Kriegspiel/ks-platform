# Step 510 - Testing Plan

## Required Commands

```bash
cd frontend && npm run test -- ChessBoard
cd frontend && npm run lint
cd frontend && npm run test -- --coverage --runInBand ChessBoard
```

## Expected Outcomes

- ChessBoard tests PASS with zero unexpected skips.
- Lint PASS.
- Coverage command PASS for the target component path.

## Runtime Smoke Check

```bash
cd frontend && npm run dev -- --host 0.0.0.0 --port 4173
```

Expected: board renders and flips when orientation prop changes.

## Fail/Skip Rules

- If `frontend/` missing/toolchain unavailable, mark BLOCKED with exact missing dependency.
