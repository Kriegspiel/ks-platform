# Step 540 - Testing Plan

```bash
cd frontend && npm run test -- PromotionModal
cd frontend && npm run test -- Game --runInBand
cd frontend && npm run lint
cd frontend && npm run test:e2e -- --grep "promotion flow"
```

Expected: PASS; promotion e2e verifies modal selection and UCI suffix behavior.
