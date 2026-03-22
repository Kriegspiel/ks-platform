# Step 440 - Clock Service + Timeout Adjudication

## Goal

Implement server-side time accounting and timeout completion behavior that integrates with move/poll flows.

## Objective and Scope

- In scope: clock domain/service methods for remaining-time calculation, move-time deduction/increment, timeout detection.
- In scope: wiring clock state into mutation + polling payloads.
- Out of scope: transcript/archive retrieval APIs (450), broad regression suite (460).

## Dependencies and Order

- Depends on: 420 mutation path and 430 polling payload.
- Blocks: 460 final verification.

## Backend/Frontend/Data/API Impacts

- Backend: new clock service and integration points in move + state routes/services.
- Frontend: receives authoritative clock values from polling payload (no client clock authority).
- Data: stores per-color remaining time + last timestamp/active color metadata.
- API: expands move/state responses with normalized `clock` object and timeout terminal reason.

## Acceptance Criteria

- Remaining time is computed server-side using persisted baseline + elapsed wall time.
- Successful move deducts mover elapsed time and applies increment atomically.
- Timeout detection transitions game to `completed` with deterministic winner/reason.
- Polling endpoint reflects current remaining values and active color.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
