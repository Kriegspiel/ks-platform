# Step 200 - Auth and Sessions

## Goal

Deliver production-shaped username/email/password authentication and Mongo-backed sessions across backend and frontend, with deterministic automated tests for each slice.

## Read First

- [AUTH.md](../../AUTH.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [API_SPEC.md](../../API_SPEC.md)
- [development-plan/README.md](../README.md)
- [development-plan/PLAN.md](../PLAN.md)

## Depends On

- `step-100` (DONE)

## Product/Auth Decision (Locked)

Step 200 must implement the approved decision exactly:

- **Required now:** `username` + `email` + `password` for registration
- **Auth mode now:** password-based login + server-side session cookie
- **Migration later:** passwordless introduced in later phases as additive, then optional default, with password fallback preserved until explicit deprecation sign-off

This decision is mandatory scope and must stay reflected in API contracts, validation, UI copy, and tests.

## Slice Packets

Each slice has a detailed implementation packet:

- [210 - Domain models + UserService](./210/README.md)
- [220 - Session service + auth API](./220/README.md)
- [230 - Frontend auth state + pages](./230/README.md)
- [240 - Auth UX polish + navigation integration](./240/README.md)
- [250 - End-to-end auth verification and hardening checks](./250/README.md)

Every slice folder contains:

- `README.md` (scope contract)
- `IMPLEMENTATION.md` (execution-level build plan)
- `TESTING.md` (exact commands + expected outcomes)
- `CHECKLIST.md` (operator checklist)

## Exit Criteria

- Backend supports register/login/logout/me with session cookies and no middleware-based auth hydration.
- Registration enforces **username+email+password required**.
- Frontend auth flow is usable and stateful across refresh.
- Automated tests cover success/failure auth paths and session lifecycle.
- Step-200 progress docs include exact executed commands and outcomes for each completed slice.

## Out of Scope

- Passwordless login implementation (planning hooks only)
- OAuth/social auth
- Email verification enforcement gate
- Lobby/game feature work (Step 300+)
