# Step 310 - Game Domain Models and Code Generator - Implementation Plan

## Objective

Create stable game/lobby schema primitives and join-code generation utility.

## Delivery Sequence

1. Reconcile model fields with `DATA_MODEL.md` and `API_SPEC.md` (no speculative extras).
2. Implement `game.py` document + DTO models with explicit literals/enums for lifecycle states.
3. Implement `generate_game_code(db)` with configurable retry cap and collision lookup.
4. Add tests for schema validation, state restriction, and generator collision handling.
5. Execute all required testing commands and log outcomes in `step-300/PROGRESS.md`.

## Engineering Notes

- Normalize naming to existing backend conventions (`snake_case` in persistence where applicable).
- Exclude ambiguous characters (`0,O,1,I,L`) in game code alphabet.
- Keep generator deterministic-testable by allowing RNG stub/seed injection if needed.
- Do not overreach into service/router layers in this slice.

## Definition of Done

- Acceptance criteria from `README.md` all satisfied.
- Test commands in `TESTING.md` run with expected outcomes.
- Slice evidence added to `step-300/PROGRESS.md`.
