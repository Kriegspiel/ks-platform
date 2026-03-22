# Step 520 - Testing Plan

```bash
cd frontend && npm run test -- Game
cd frontend && npm run test -- api
cd frontend && npm run lint
cd frontend && npm run test:e2e -- --grep "game polling"
```

Expected: all commands PASS; e2e confirms log updates on poll tick and controls disable when completed.

If backend e2e dependency unavailable, run first three commands and document blocker explicitly.
