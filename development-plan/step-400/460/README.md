# Step 460 - Gameplay Integration + Regression Hardening

## Goal

Validate end-to-end gameplay core behavior across mutation, polling, hidden information, clock, and archive flows.

## Objective and Scope

- In scope: integration test suite covering full gameplay loop and security-sensitive edge cases.
- In scope: regression matrix for legal/illegal move handling, ask-any, timeout/resign completion, transcript visibility, and non-participant access.
- Out of scope: new product features or contract expansion.

## Dependencies and Order

- Depends on: 410, 420, 430, 440, 450 complete.
- Final slice for Step 400 signoff.

## Backend/Frontend/Data/API Impacts

- Backend: tests and (if needed) test fixtures/helpers only.
- Frontend: none directly; test evidence validates backend contracts consumed by Step 500 UI.
- Data: fixture coverage for active + archived games and clock state transitions.
- API: confirms end-to-end contract stability under realistic multi-user flows.

## Acceptance Criteria

- Integration tests cover complete game lifecycle from active play to completion/archival.
- Hidden-information guarantees verified for both players across polls.
- Timeout and resign terminal paths both validated.
- Unauthorized/non-participant access consistently rejected.
- Step 400 completion evidence captured with exact command outputs/outcome counts.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
