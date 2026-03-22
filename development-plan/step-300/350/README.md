# Step 350 - Lifecycle Integration Verification and Hardening

## Goal

Provide final Step 300 confidence through integration tests and runtime validation spanning backend lifecycle rules and lobby flows.

## Scope

- In scope: end-to-end/integration tests for create/join/open/mine/resign/delete flows and error conditions.
- In scope: regression checks that Step 200 auth/session behavior still holds under Step 300 routes.
- In scope: final progress evidence collation and completion recommendation.
- Out of scope: Step 400 gameplay-move validation.

## Backend/Frontend/API/Data Model Impacts

Backend: test additions and possibly minor bugfixes discovered by integrated checks. Frontend: smoke-level validation, optional targeted bugfixes. API: confirms contract stability across the full Step 300 surface. Data model: verifies transition correctness over real persistence lifecycle.

## Rollout Order and Dependencies

Must run after 310/320/330/340 are functionally complete. This is the final gate before marking Step 300 DONE.

## Acceptance Criteria

- Integration suite verifies lifecycle transitions and denial paths end to end.
- Auth-required protections and standardized errors remain intact.
- Smoke checks confirm practical multi-user create/join/active/resign loop.
- `step-300/PROGRESS.md` contains exact command evidence and final status recommendation.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
