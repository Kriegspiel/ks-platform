# Step 300 Handoff Notes

## Purpose

Operator handoff companion for Step 300 implementation execution.

## Current State

- Detailed planning packet exists for slices 310-350.
- No implementation code changed in this planning commit.

## Next Action

1. Begin with `310/README.md`, then `310/IMPLEMENTATION.md`, then `310/TESTING.md`.
2. Keep state machine constrained to `waiting -> active -> completed` everywhere.
3. Use auth dependency from Step 200 and avoid middleware/session architecture drift.

## Guardrails

- Join codes must be unique, human-shareable, and collision-tested.
- `join` must reject creator self-join and non-waiting states deterministically.
- Lobby API responses must preserve standardized error shape.
- Polling intervals should remain bounded (no sub-second loops) and cancellable in React cleanup.

## Evidence Protocol

For each slice, append:

- Branch/PR pointer (if applicable)
- Exact commands executed
- Outcome counts (pass/fail/skip)
- Any justified deviation from packet docs
