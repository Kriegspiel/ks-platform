# Step 530 - Testing Plan

```bash
cd frontend && npm run test -- usePhantoms
cd frontend && npm run test -- PhantomTray
cd frontend && npm run lint
cd frontend && npm run test:e2e -- --grep "phantom persistence"
```

Expected: test/lint PASS; e2e verifies phantom placement survives reload for same game id.
