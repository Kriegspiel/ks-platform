# Step 330 - Authenticated Game API Surface

## Goal

Expose lifecycle operations as authenticated REST endpoints with stable request/response and error contracts.

## Scope

- In scope: `src/app/routers/game.py` and route registration in `src/app/main.py`.
- In scope: auth dependency enforcement on all game endpoints.
- In scope: API/integration tests for route behavior and standardized error shape.
- Out of scope: frontend lobby UX implementation details.

## Backend/Frontend/API/Data Model Impacts

Backend: new router and dependency wiring. Frontend: consumes these endpoints in 340. API: formalizes create/join/open/mine/get/resign/delete contracts. Data model: no new schema changes, only service-mediated mutations.

## Rollout Order and Dependencies

Depends on 310 + 320. Must land before 340 and 350 final integration gate.

## Acceptance Criteria

- All endpoints reject unauthenticated requests with 401.
- `POST /api/game/create` returns 201 + create payload with join code.
- `POST /api/game/join/{code}` returns assigned color and active state.
- `GET /api/game/open` and `GET /api/game/mine` return deterministic list payload shapes.
- Error responses conform to project-standard envelope for handled domain errors.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
