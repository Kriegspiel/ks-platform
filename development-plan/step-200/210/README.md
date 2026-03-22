# Step 210 - User Domain Models and UserService

## Goal

Create authoritative backend auth data contracts and user persistence helpers.

## Scope

- In scope: `src/app/models/user.py`, `src/app/models/auth.py`, `src/app/services/user_service.py`, tests for model validation and password hashing behavior.
- In scope: required register inputs (username/email/password) and duplicate username/email collision handling.
- Out of scope: HTTP route wiring, session cookie logic, frontend auth flows.

## Backend/Frontend/API/Data Model Impacts

Backend: new models/services. Frontend: none. API: request/response DTO contract established. Data model: users collection write/read shape aligned with DATA_MODEL.md + verification-ready fields.

## Rollout Order and Dependencies

Must land before slice 220. Dependencies: Step 100 test harness + Mongo index setup from step-120.

## Acceptance Criteria

- Register DTO rejects missing `email`, missing `username`, missing `password` with 422.
- Username format and password length rules enforced per packet.
- `create_user()` stores bcrypt hash, lowercase canonical username, display username, and verification-ready email fields.
- `authenticate()` returns user for valid creds, `None` otherwise.
- Duplicate username/email produces deterministic 409-domain exception path.

## Required Reading Order

1. `README.md`
2. `IMPLEMENTATION.md`
3. `TESTING.md`
4. `CHECKLIST.md`
