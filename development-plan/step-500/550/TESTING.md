# Step 550 - Testing Plan

```bash
cd frontend && npm run test -- Home
cd frontend && npm run test -- Nav
cd frontend && npm run lint
cd frontend && npm run test:e2e -- --grep "home to active game navigation"
```

Expected: PASS; e2e verifies Play Now path and active-game entry visibility.
