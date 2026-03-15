# Step 200 - Auth and Sessions

## Goal

Implement secure user authentication, session handling, and the basic account entry pages.

## Read First

- [AUTH.md](../../AUTH.md)
- [DATA_MODEL.md](../../DATA_MODEL.md)
- [API_SPEC.md](../../API_SPEC.md)

## Depends On

- `step-100`

## Task Slices

### 210 — User and Session Pydantic Models

**Create these files:**

- `src/app/models/user.py` — `UserDocument`, `UserStats`, `UserSettings`, `UserProfile` models exactly as defined in DATA_MODEL.md
- `src/app/models/session.py` — `SessionDocument` model matching DATA_MODEL.md sessions collection schema (fields: `_id`, `user_id`, `username`, `csrf_token`, `ip`, `user_agent`, `created_at`, `expires_at`)
- `src/app/models/auth.py` — `RegisterRequest`, `RegisterResponse`, `LoginRequest`, `LoginResponse` models exactly as defined in API_SPEC.md

**Acceptance criteria:**
- All models instantiate with valid data and reject invalid data (e.g., username regex `^[a-zA-Z0-9_]+$`, min/max lengths)
- Models match DATA_MODEL.md and API_SPEC.md schemas exactly
- `cd src && python -c "from app.models.user import UserDocument; print('ok')"` works

---

### 220 — Password Hashing and UserService

**Create these files:**

- `src/app/services/auth_helpers.py` — `hash_password(plain) -> str` and `verify_password(plain, hashed) -> bool` using bcrypt as specified in AUTH.md
- `src/app/services/user_service.py` — `UserService` class with methods:
  - `create_user(username, password, email=None) -> dict` — validates uniqueness, stores `username` (lowercase) + `username_display` (original case), hashes password, inserts into `users` collection, returns user doc
  - `authenticate(username, password) -> dict | None` — looks up user by lowercase username, verifies password, returns user doc or None
  - `get_by_id(user_id) -> dict | None`
  - `get_by_username(username) -> dict | None`

**Acceptance criteria:**
- `hash_password` produces a bcrypt hash, `verify_password` matches it
- `UserService.create_user` inserts a user matching the DATA_MODEL.md schema
- `UserService.authenticate` returns None on wrong password, returns user on correct password
- Duplicate username raises a handled error (409-style)

---

### 230 — Session Service and Auth Router

**Create these files:**

- `src/app/services/session_service.py` — `SessionService` class with methods:
  - `create_session(user_id, username, ip, user_agent) -> str` — generates 32-byte random hex session ID, generates CSRF token, inserts session doc with 30-day expiry, returns session_id
  - `get_session(session_id) -> dict | None` — looks up session, returns None if expired/missing
  - `delete_session(session_id)` — removes session doc
  - `extend_session(session_id)` — updates `expires_at` to now + 30 days (sliding window)
- `src/app/routers/auth.py` — FastAPI router with prefix `/auth`:
  - `POST /auth/register` — validate `RegisterRequest`, call `UserService.create_user`, create session, set `session_id` cookie (HttpOnly, Secure in prod, SameSite=Lax, Max-Age=30 days), return `RegisterResponse`
  - `POST /auth/login` — validate `LoginRequest`, call `UserService.authenticate`, create session, set cookie, return `LoginResponse`. Return 401 on bad credentials.
  - `POST /auth/logout` — delete session, clear cookie, return `{"message": "Logged out"}`
  - `GET /auth/me` — return current user info (user_id, username, email, stats, settings) or 401
- Wire the auth router into `src/app/main.py`

**Acceptance criteria:**
- `POST /auth/register` with valid data returns 201 + sets `session_id` cookie
- `POST /auth/register` with duplicate username returns 409
- `POST /auth/login` with valid credentials returns 200 + sets cookie
- `POST /auth/login` with bad password returns 401
- `POST /auth/logout` clears the session
- `GET /auth/me` with valid session returns user data, without session returns 401

---

### 240 — Session Middleware, CSRF, and Route Protection

**Create/modify these files:**

- `src/app/middleware/session.py` — `SessionMiddleware` (BaseHTTPMiddleware) that reads `session_id` cookie, looks up session, populates `request.state.user` with `{user_id, username}` or sets to None. Extends session expiry on activity (sliding window). Exactly as specified in AUTH.md.
- `src/app/middleware/csrf.py` — CSRF middleware that on POST/PATCH/DELETE requests (except API-token-authenticated requests): checks `_csrf` form field or `X-CSRF-Token` header against session's `csrf_token`. Returns 403 on mismatch.
- `src/app/dependencies.py` — `require_auth` dependency (FastAPI `Depends`) that checks `request.state.user` and raises 401 if None. `require_admin` dependency that additionally checks user role.
- Wire both middlewares into `src/app/main.py` (session middleware must run before CSRF middleware)

**Acceptance criteria:**
- Requests with valid session cookie get `request.state.user` populated
- Requests without session cookie get `request.state.user = None`
- POST requests without valid CSRF token return 403
- POST requests with valid CSRF token succeed
- `require_auth` raises 401 for unauthenticated requests
- Session sliding window works (expires_at gets extended on each request)

---

### 250 — Login and Register Pages

**Create these files:**

- `src/app/templates/base.html` — base Jinja2 layout with `<head>` (meta, CSS link), `<nav>` (logo, login/logout links based on user state), `<main>` block, HTMX script tag, CSRF token in `hx-headers`
- `src/app/templates/login.html` — extends base, login form with username + password fields, error display area, link to register page. Form posts to `/auth/login`.
- `src/app/templates/register.html` — extends base, registration form with username + password + optional email fields, validation error display, link to login page. Form posts to `/auth/register`.
- `src/app/routers/pages.py` — FastAPI router for server-rendered pages:
  - `GET /auth/login` — render login.html (redirect to /lobby if already logged in)
  - `GET /auth/register` — render register.html (redirect to /lobby if already logged in)
  - Modify auth router POST handlers to handle form submissions (redirect on success, re-render with errors on failure)
- Wire pages router into `src/app/main.py`, configure Jinja2 templates directory

**Acceptance criteria:**
- `GET /auth/login` renders an HTML page with a login form
- `GET /auth/register` renders an HTML page with a registration form
- Submitting the login form with valid credentials redirects to `/lobby` (or `/` for now)
- Submitting with invalid credentials re-renders the form with an error message
- Forms include hidden `_csrf` field
- Nav shows login/register links when logged out, username + logout when logged in

---

### 260 — Auth Integration Tests

**Create these files:**

- `src/tests/test_auth.py` — integration tests covering:
  - Register with valid data → 201 + session cookie set
  - Register with duplicate username → 409
  - Register with invalid username (too short, bad chars) → 422
  - Register with short password → 422
  - Login with valid credentials → 200 + session cookie
  - Login with wrong password → 401
  - Login with nonexistent user → 401
  - Logout → session deleted, cookie cleared
  - `GET /auth/me` with valid session → 200 + user data
  - `GET /auth/me` without session → 401
  - CSRF: POST without token → 403
  - CSRF: POST with valid token → success
  - Session sliding: session `expires_at` is extended on request
- `src/tests/test_password.py` — unit tests for `hash_password`/`verify_password`

**Acceptance criteria:**
- `cd src && pytest tests/test_auth.py tests/test_password.py -v` — all pass
- Tests use the test database and clean up after themselves
- At least 15 test cases covering happy paths and error cases

---

## Required Tests Before Done

- Unit tests for password hashing and auth service behavior
- Integration tests for register/login/logout/session flows
- CSRF/session tests for protected POST routes

## Exit Criteria

- Users can register, log in, log out, and fetch current session state
- Sessions are stored server-side and hydrated correctly
- CSRF protection is present on form-based writes
- Login and registration pages work end-to-end

## Out of Scope

- Lobby/game APIs
- OAuth
- WebSocket gameplay
- API token auth (JWT) — added later when WebSocket needs it
