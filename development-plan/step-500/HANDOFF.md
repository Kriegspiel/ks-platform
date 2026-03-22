# Step 500 Handoff Notes

## Purpose

Operator handoff companion for Step 500 game-UI execution.

## Current State

- Detailed planning packet exists for slices 510-550.
- No implementation code changed in this planning commit.

## Next Action

1. Start with `510/README.md`, then `510/IMPLEMENTATION.md`, then `510/TESTING.md`.
2. Lock square-selection semantics/orientation before wiring poll actions.
3. Keep phantom state strictly client-side.

## Guardrails

- Never expose hidden opponent state not returned by API.
- Never send phantom state to backend routes.
- Promotion selection must gate move submission.
- Poll interval must be cleaned on unmount/completion.
