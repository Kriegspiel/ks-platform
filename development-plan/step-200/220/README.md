# Step 220 - Session Service, Auth Dependency, and Auth Router

## Goal

Implement backend auth API endpoints and server-side session lifecycle.

## Scope

- In scope: `session_service.py`, `dependencies.py`, `routers/auth.py`, router wiring in `main.py`.
- In scope: register/login/logout/me endpoint behavior, cookie issuance/clearing, 401/409/422 path correctness.
- Out of scope: frontend auth UI integration and styling.

## Backend/Frontend/API/Data Model Impacts

Backend: auth routes + dependency injection. Frontend: API contracts consumed in slice 230. API: /auth/register/login/logout/me finalized for Step 200. Data model: sessions collection writes + expiry checks.

## Rollout Order and Dependencies

Depends on 210 models/services. Must be complete before 230 and 250 signoff.

## Acceptance Criteria

- `POST /auth/register` returns 201 and sets HttpOnly `session_id` cookie.
- `POST /auth/login` returns 200 and sets cookie on valid creds; returns 401 on invalid creds.
- `POST /auth/logout` invalidates session and clears cookie.
- `GET /auth/me` returns 200 with expected user fields when authenticated, else 401.
- Cookie flags follow env policy (`Secure` true in production, false in dev/test).

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
