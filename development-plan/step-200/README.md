# Step 200 - Auth and Sessions

## Goal

Implement user registration, login, logout, and session handling. Build React auth pages.

## Read First

- [AUTH.md](../../AUTH.md) — password hashing, session model (ignore CSRF/middleware sections — we use a simpler approach)
- [DATA_MODEL.md](../../DATA_MODEL.md) — users and sessions collections
- [API_SPEC.md](../../API_SPEC.md) — auth endpoint contracts
- [development-plan/PLAN.md](../PLAN.md) — architecture decisions

## Depends On

- `step-100`

## Auth Approach (Simplified vs. Spec)

The spec describes session middleware + CSRF middleware. We use a simpler approach:

- **Server-side sessions** in MongoDB (same as spec)
- **HttpOnly cookie** with `SameSite=Lax` (same as spec)
- **No CSRF middleware** — SameSite=Lax + API-only (no form submissions from server-rendered pages) is sufficient
- **No session middleware** — use a FastAPI dependency (`get_current_user`) instead
- **No sliding session expiry** — sessions last 30 days, period

## Task Slices

### 210 — User Model, Password Hashing, UserService

**Create these files:**

- `src/app/models/user.py` — Pydantic models from DATA_MODEL.md:
  - `UserDocument` (username, username_display, email, password_hash, profile, stats, settings, role, status, timestamps)
  - `UserStats`, `UserSettings`, `UserProfile` embedded models
- `src/app/models/auth.py` — API request/response models from API_SPEC.md:
  - `RegisterRequest` (username: 3-20 chars `[a-zA-Z0-9_]+`, password: 8-72 chars, email: optional)
  - `RegisterResponse` (user_id, username, message)
  - `LoginRequest` (username, password)
  - `LoginResponse` (user_id, username)
- `src/app/services/user_service.py` — `UserService` class:
  - `hash_password(plain) -> str` — bcrypt with default cost
  - `verify_password(plain, hashed) -> bool` — bcrypt check
  - `create_user(db, username, password, email=None) -> dict` — lowercase username, store display case, hash password, insert into `users`, return user doc. Raise 409 on duplicate.
  - `authenticate(db, username, password) -> dict | None` — lookup by lowercase username, verify password, return user or None
  - `get_by_id(db, user_id) -> dict | None`

**Acceptance criteria:**
- `RegisterRequest` rejects usernames with spaces, passwords under 8 chars
- `hash_password` / `verify_password` round-trip works
- `create_user` inserts a user matching DATA_MODEL.md schema
- `create_user` raises on duplicate username
- `authenticate` returns None on wrong password

---

### 220 — Session Service and Auth API Endpoints

**Create these files:**

- `src/app/services/session_service.py` — `SessionService`:
  - `create_session(db, user_id, username, ip, user_agent) -> str` — generate 32-byte random hex ID, insert session doc (user_id, username, ip, user_agent, created_at, expires_at=now+30days), return session_id
  - `get_session(db, session_id) -> dict | None` — lookup session, return None if missing/expired
  - `delete_session(db, session_id)` — remove session doc
- `src/app/dependencies.py`:
  - `get_current_user(request) -> dict` — read `session_id` cookie, lookup session via SessionService, return `{user_id, username}` or raise 401. This is a FastAPI `Depends()` function, not middleware.
- `src/app/routers/auth.py` — FastAPI router, prefix `/auth`:
  - `POST /auth/register` — validate `RegisterRequest`, create user, create session, set `session_id` cookie (HttpOnly, SameSite=Lax, Max-Age=30 days, Secure=True only in production), return 201 `RegisterResponse`
  - `POST /auth/login` — validate `LoginRequest`, authenticate, create session, set cookie, return 200 `LoginResponse`. Return 401 on bad credentials.
  - `POST /auth/logout` — delete session, clear cookie, return `{"message": "Logged out"}`
  - `GET /auth/me` — uses `get_current_user` dependency, returns user info (user_id, username, email, stats, settings). Returns 401 if not authenticated.
- Wire auth router into `src/app/main.py`

**Acceptance criteria:**
- `POST /auth/register` returns 201 + sets `session_id` cookie
- `POST /auth/register` with duplicate username returns 409
- `POST /auth/login` with correct password returns 200 + sets cookie
- `POST /auth/login` with wrong password returns 401
- `POST /auth/logout` clears session and cookie
- `GET /auth/me` with valid cookie returns user data
- `GET /auth/me` without cookie returns 401

---

### 230 — React Auth Pages

**Create these files:**

- `frontend/src/context/AuthContext.jsx` — React context for auth state:
  - `AuthProvider` wraps app, provides `{user, loading, login, register, logout}`
  - On mount: call `GET /auth/me` to check if already logged in
  - `login(username, password)` — call `POST /auth/login`, update state
  - `register(username, password, email)` — call `POST /auth/register`, update state
  - `logout()` — call `POST /auth/logout`, clear state
- `frontend/src/pages/Login.jsx` — login form:
  - Username + password inputs
  - Submit calls `login()` from AuthContext
  - Error display for invalid credentials
  - Link to register page
  - Redirect to `/lobby` on success
- `frontend/src/pages/Register.jsx` — registration form:
  - Username + password + optional email inputs
  - Client-side validation (username 3-20 chars, password 8+ chars)
  - Submit calls `register()` from AuthContext
  - Error display for duplicates/validation
  - Link to login page
  - Redirect to `/lobby` on success
- `frontend/src/services/api.js` — add auth API functions:
  - `authApi.register(username, password, email)`
  - `authApi.login(username, password)`
  - `authApi.logout()`
  - `authApi.me()`
- `frontend/src/App.jsx` — wrap with `AuthProvider`, add Login/Register routes, add nav bar showing user state (logged in → username + logout, logged out → login/register links)

**Acceptance criteria:**
- Login page renders with form
- Registration page renders with form
- Successful login redirects to /lobby
- Failed login shows error message
- Nav bar reflects auth state
- Page refresh preserves login state (cookie persists)

---

### 240 — React Auth Styles

**Create/modify these files:**

- `frontend/src/pages/Login.css` — login form styling (centered card, input fields, button, error area)
- `frontend/src/pages/Register.css` — registration form styling (same pattern)
- `frontend/src/components/Nav.jsx` — navigation bar component:
  - Logo (♞ Kriegspiel) linking to /
  - Auth area: login/register links when logged out, username + logout button when logged in
  - Active game indicator (placeholder for step 300)
- `frontend/src/components/Nav.css` — nav styling
- `frontend/src/App.jsx` — use Nav component in layout

**Acceptance criteria:**
- Auth pages are styled and usable
- Nav bar shows on all pages
- Nav reflects auth state correctly
- Forms have basic visual feedback (loading state, errors)

---

### 250 — Auth Integration Tests

**Create this file:**

- `src/tests/test_auth.py` — integration tests:
  - Register with valid data → 201 + cookie set
  - Register with duplicate username → 409
  - Register with invalid username (too short, bad chars) → 422
  - Register with short password → 422
  - Login with valid credentials → 200 + cookie
  - Login with wrong password → 401
  - Login with nonexistent user → 401
  - Logout → session deleted, cookie cleared
  - `GET /auth/me` with valid session → 200 + user data
  - `GET /auth/me` without session → 401
  - `GET /auth/me` with expired/invalid session → 401
- `src/tests/test_password.py` — unit tests:
  - `hash_password` produces bcrypt hash
  - `verify_password` matches correct password
  - `verify_password` rejects wrong password

**Acceptance criteria:**
- `cd src && pytest tests/test_auth.py tests/test_password.py -v` — all pass
- At least 12 test cases
- Tests use test database and clean up

---

## Exit Criteria

- Users can register, log in, log out, and check session
- React auth pages work end-to-end
- Session cookies are set correctly (HttpOnly, SameSite=Lax)

## Out of Scope

- CSRF middleware (not needed with SameSite + API-only)
- OAuth
- Game logic
- API token auth (JWT)
