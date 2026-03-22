# Step 310 - Game Domain Models and Code Generator

## Goal

Establish authoritative game/lobby data contracts and deterministic join-code generation primitives used by all later Step 300 slices.

## Scope

- In scope: `src/app/models/game.py` model definitions for game document + lobby DTOs.
- In scope: `src/app/services/code_generator.py` with collision-aware `generate_game_code(db)`.
- In scope: tests for model validation boundaries and code generator uniqueness/collision retry behavior.
- Out of scope: lifecycle orchestration (`GameService`), router wiring, frontend lobby UX.

## Backend/Frontend/API/Data Model Impacts

Backend: adds core game models and join-code service. Frontend: none in this slice. API: DTO schemas become the source of truth for create/join/list responses. Data model: `games` document shape stabilized for lifecycle states and player embeds.

## Rollout Order and Dependencies

Must land before 320/330/340/350. Depends on Step 200 auth user identity contract (user id + username available per request).

## Acceptance Criteria

- `GameDocument.state` accepts only `waiting`, `active`, `completed`.
- DTOs serialize to API contract fields expected by Step 300 endpoints.
- `generate_game_code()` returns 6-char uppercase safe-alphanumeric code and retries on collision.
- Code generation unit tests cover at least one forced collision then success case.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
