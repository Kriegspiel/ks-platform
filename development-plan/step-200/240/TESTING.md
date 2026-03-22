# Step 240 - Auth UX Styling and Navigation Integration - Testing Plan

## Integration Prerequisites

- Slice 230 merged in working tree.
- CSS files imported and scoped predictably to avoid global bleed.

## Required Commands

```bash
cd frontend && npm run test -- --run
cd frontend && npm run lint
cd frontend && npm run build
```

## Expected Outcomes

- Frontend regression tests: PASS.
- Lint/build: PASS.

## Runtime Smoke Checks

- Visual pass for narrow/mobile and desktop widths.
- Keyboard-only tab flow through login/register/nav without focus trap.

## Fail/Skip Handling Rules

- If a command fails: stop and record exact failure output + suspected root cause in `step-200/PROGRESS.md`.
- If a command is intentionally skipped: record the explicit skip gate (env var or prerequisite) and confirm remaining mandatory coverage still passed.
- Do not mark this slice complete on manual smoke checks alone.
