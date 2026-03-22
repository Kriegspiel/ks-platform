# Step 430 - Polling Game-State API + Hidden-Information Projection - Implementation Plan

## Objective

Implement gameplay polling endpoint with strict visibility boundaries and stable DTO responses.

## Delivery Sequence

1. Define polling response DTO based on `API_SPEC.md` and Step 400 contract.
2. Implement participant authz and fetch path for active/completed games.
3. Build projection helpers for board visibility, possible actions, and referee log shaping.
4. Add API tests for white-view/black-view/non-participant and announcement filtering.
5. Record outcomes in `step-400/PROGRESS.md`.

## Engineering Notes

- Never expose raw move UCI in opponent-visible feed unless explicitly allowed by spec.
- Keep projection logic unit-testable (pure functions where possible).
- Ensure endpoint remains efficient for 2-second polling cadence.

## Definition of Done

- Acceptance criteria met.
- All commands in `TESTING.md` pass.
- Evidence captured in progress doc.
