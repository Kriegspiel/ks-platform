# Step 250 - Auth Integration Verification and Regression Guardrails

## Goal

Prove end-to-end auth correctness and lock in Step 200 behavior with integration tests.

## Scope

- In scope: comprehensive backend auth integration tests, password unit tests, cookie/session regression assertions.
- In scope: explicit success and failure-path coverage matrix.
- Out of scope: introducing new auth features.

## Backend/Frontend/API/Data Model Impacts

Backend test suite expansion. Frontend indirect confidence only. API contracts become regression-guarded.

## Rollout Order and Dependencies

Depends on 210+220 complete. Can run parallel to 240 final polish once backend stable.

## Acceptance Criteria

- At least 12 auth integration scenarios implemented and passing.
- Tests cover missing email on register (422) and valid trio register success (201).
- Tests confirm login remains password-based (no accidental passwordless-only path).
- Session invalid/expired paths return 401 deterministically.
- All checks runnable non-interactively in CI-compatible mode.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
