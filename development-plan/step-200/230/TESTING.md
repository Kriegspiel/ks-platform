# Step 230 - Frontend Auth Context and Core Pages - Testing Plan

## Integration Prerequisites

- Node/npm versions satisfy frontend toolchain.
- Mocked API layer or MSW fixtures available for deterministic unit tests.
- Backend dev server running only if smoke checks hit real endpoints.

## Required Commands

```bash
cd frontend && npm install
cd frontend && npm run test -- --run
cd frontend && npm run lint
cd frontend && npm run build
```

## Expected Outcomes

- Unit/component tests: PASS; no skip unless clearly documented for env mismatch.
- Lint/build: PASS.

## Runtime Smoke Checks

- Run frontend dev server and complete register->lobby and logout loop.
- Hard-refresh on lobby keeps auth state; deleting cookie then refresh returns logged-out state.

## Fail/Skip Handling Rules

- If a command fails: stop and record exact failure output + suspected root cause in `step-200/PROGRESS.md`.
- If a command is intentionally skipped: record the explicit skip gate (env var or prerequisite) and confirm remaining mandatory coverage still passed.
- Do not mark this slice complete on manual smoke checks alone.
