# Step 230 - Frontend Auth Context and Core Pages

## Goal

Deliver working login/register flows and persistent auth state in the React app.

## Scope

- In scope: `AuthContext`, Login/Register pages, API client auth helpers, route integration.
- In scope: required register form fields include username/email/password.
- Out of scope: final visual polish (slice 240), non-auth gameplay views.

## Backend/Frontend/API/Data Model Impacts

Frontend: auth state orchestration + page routes. Backend/API: consumes 220 endpoints. Data model: none direct.

## Rollout Order and Dependencies

Depends on 220 backend APIs. Enables 240 UX polish and 250 full-path tests.

## Acceptance Criteria

- App bootstraps auth state via `/auth/me`.
- Login success redirects to `/lobby`; failure surfaces actionable error.
- Register requires username/email/password and handles 422/409 API errors.
- Logout clears UI state and returns user to unauthenticated navigation.
- Refresh preserves logged-in state when valid cookie exists.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
