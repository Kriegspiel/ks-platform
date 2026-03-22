# Step 320 - GameService Lifecycle Operations

## Goal

Implement backend lifecycle behavior for create/join/list/resign/delete with strict state/ownership rules.

## Scope

- In scope: `src/app/services/game_service.py` lifecycle methods (`create_game`, `join_game`, `get_open_games`, `get_my_games`, `get_game`, `resign_game`, `delete_waiting_game`).
- In scope: domain exception mapping and deterministic validation branches.
- In scope: unit/service tests covering legal and illegal transitions.
- Out of scope: FastAPI route wiring and frontend wiring.

## Backend/Frontend/API/Data Model Impacts

Backend: central lifecycle orchestration lands in service layer. Frontend: none directly. API: downstream router contract is constrained by returned payload/error semantics. Data model: writes enforce state transitions and player slot assignment invariants.

## Rollout Order and Dependencies

Depends on 310 model + code generation completion. Must land before 330 and 350.

## Acceptance Criteria

- `create_game` writes `waiting` game with creator assigned chosen/randomized color.
- `join_game` enforces: exists, not creator, state is `waiting`, and transitions to `active`.
- `resign_game` only allowed for active participant and transitions to `completed` with winner + reason.
- `delete_waiting_game` allowed only for creator while game is still `waiting`.
- `get_open_games` returns only waiting games, newest first, bounded list size.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
