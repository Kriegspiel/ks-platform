# Step 410 - Engine Adapter + Deterministic Serialization - Implementation Plan

## Objective

Create a minimal, reusable gameplay engine boundary layer with deterministic behavior and robust unit coverage.

## Delivery Sequence

1. Reconcile function contract with `GAME_ENGINE.md` and existing ks-v2 wrapper patterns.
2. Implement adapter module (new game, move, ask-any, FEN projection, serialization).
3. Normalize adapter response payload keys to stable names reused by route handlers.
4. Add unit tests covering positive/negative move paths and projection correctness.
5. Run required checks and record outcomes in `step-400/PROGRESS.md`.

## Engineering Notes

- Keep engine-specific objects contained in service layer; routers should only consume plain dict/DTO output.
- Ensure projection functions are pure and side-effect free.
- Avoid speculative helpers not required by 420-440 dependencies.

## Definition of Done

- All acceptance criteria in `README.md` met.
- All commands in `TESTING.md` pass.
- Evidence recorded in `step-400/PROGRESS.md`.
