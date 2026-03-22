# Step 340 - Frontend Lobby UX and Polling Flows

## Goal

Ship the authenticated lobby UI for create/join/open/mine flows with robust polling and clean navigation transitions into gameplay.

## Scope

- In scope: `frontend/src/pages/Lobby.jsx`, `Lobby.css`, API client additions, and `/lobby` route wiring.
- In scope: create game form, join by code form, open games list, my games list, waiting-state polling, and redirect-on-activation flow.
- In scope: frontend tests for key interactions/state transitions where harness exists.
- Out of scope: board/gameplay rendering and in-game move UI.

## Backend/Frontend/API/Data Model Impacts

Backend: none beyond consuming Step 330 contracts. Frontend: substantial new lobby page and service calls. API: consumes create/join/open/mine/get endpoints. Data model: no schema changes.

## Rollout Order and Dependencies

Depends on API stability from 330. Should complete before 350 integration verification so end-to-end checks include real UI behavior.

## Acceptance Criteria

- Lobby route is auth-guarded and inaccessible to anonymous users.
- Create flow displays generated join code and waiting status immediately.
- Waiting game poll redirects to game page when state transitions to `active`.
- Join-by-code success navigates to game view; common failures render actionable UI errors.
- Open/mine panels refresh on bounded intervals with proper cleanup on unmount.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
