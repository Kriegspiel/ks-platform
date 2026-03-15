# Step 200 - Auth and Sessions

## Goal

Implement secure user authentication, session handling, and the basic account entry pages.

## Read First

- [AUTH.md](../../AUTH.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [API_SPEC.md](../../API_SPEC.md)
- [MILESTONES.md](../../MILESTONES.md)

## Depends On

- `step-100`

## Task Slices

- `200.1` Implement `users` and `sessions` data access, indexes, and password hashing helpers.
- `200.2` Implement register/login/logout/session-me endpoints and request validation.
- `200.3` Implement session hydration middleware, route protection helpers, and CSRF handling.
- `200.4` Build the login/register pages and server-rendered validation flow.

## Required Tests Before Done

- Unit tests for password hashing and auth service behavior.
- Integration tests for register/login/logout/session flows.
- CSRF/session tests for protected POST routes.

## Exit Criteria

- Users can register, log in, log out, and fetch current session state.
- Sessions are stored server-side and hydrated correctly.
- CSRF protection is present on form-based writes.
- Login and registration pages work end-to-end.

## Out of Scope

- Lobby/game APIs
- OAuth
- WebSocket gameplay
