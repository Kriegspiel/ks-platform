# Step 420 - Move/Ask-Any/Resign Gameplay Execution API - Implementation Plan

## Objective

Wire mutation endpoints to adapter/service logic with strict state/turn/participant validation and stable persistence updates.

## Delivery Sequence

1. Define request/response DTOs for move and ask-any contract in router layer.
2. Implement guard rail checks (auth, participant, active state, turn ownership).
3. Add service methods to apply adapter outcomes to persistent game records.
4. Integrate resign completion path with shared completion helper.
5. Add focused API tests for legal, illegal, forbidden, and terminal transitions.
6. Run mandatory checks and update `step-400/PROGRESS.md`.

## Engineering Notes

- Keep validation ordering deterministic to avoid ambiguous error responses.
- Persist engine state atomically with move append where possible.
- Ensure route errors preserve standardized API error shape from earlier steps.

## Definition of Done

- Acceptance criteria in `README.md` satisfied.
- Required tests/lint/format checks pass.
- Evidence documented in step progress file.
