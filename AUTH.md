# Authentication & Authorization

## Overview

Two auth mechanisms serve different clients:

| Mechanism | Client | Storage | Lifetime |
|---|---|---|---|
| **Session cookie** | Browser (web UI) | MongoDB `sessions` collection | 30 days (sliding) |
| **API token** | Bots, scripts, external clients | Included in token (JWT) | 90 days |

## Session-Based Auth (Web UI)

### Flow

```
1. POST /auth/register  or  POST /auth/login
   └─ Server validates credentials
   └─ Creates session document in MongoDB
   └─ Returns Set-Cookie: session_id=<random_id>; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000

2. Subsequent requests include cookie automatically
   └─ Middleware looks up session_id in MongoDB
   └─ Populates request.state.user with user data
   └─ If expired/missing → 401

3. POST /auth/logout
   └─ Deletes session from MongoDB
   └─ Clears cookie
```

### Session Document

```json
{
  "_id": "sess_a1b2c3d4e5f6...",    // 32-byte random hex
  "user_id": ObjectId("664a1b..."),
  "username": "alexfil",
  "created_at": ISODate,
  "expires_at": ISODate,             // TTL index auto-deletes
  "ip": "192.168.1.1",
  "user_agent": "Mozilla/5.0..."
}
```

### Session Middleware (FastAPI)

```python
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException


class SessionMiddleware(BaseHTTPMiddleware):
    """Look up session cookie and populate request.state.user."""

    EXEMPT_PATHS = {"/auth/login", "/auth/register", "/", "/static"}

    async def dispatch(self, request: Request, call_next):
        # Skip auth for public routes
        if any(request.url.path.startswith(p) for p in self.EXEMPT_PATHS):
            return await call_next(request)

        session_id = request.cookies.get("session_id")
        if not session_id:
            raise HTTPException(401, "Not authenticated")

        session = await request.app.state.db.sessions.find_one(
            {"_id": session_id}
        )
        if not session:
            raise HTTPException(401, "Session expired")

        # Populate user context
        request.state.user = {
            "user_id": session["user_id"],
            "username": session["username"],
        }

        # Sliding expiry: extend session on activity
        await request.app.state.db.sessions.update_one(
            {"_id": session_id},
            {"$set": {"expires_at": datetime.now(timezone.utc) + timedelta(days=30)}}
        )

        return await call_next(request)
```

### Password Handling

```python
import bcrypt

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())
```

- Bcrypt with default cost factor (12).
- Max password length enforced at 72 bytes (bcrypt limitation).
- No password complexity rules beyond minimum 8 chars + 1 letter + 1 digit. Complexity rules hurt more than they help.

### CSRF Token Implementation

CSRF protection prevents cross-site form submissions:

1. **Generation**: A random 32-byte hex CSRF token is generated per session and stored in the session document:
   ```json
   { "_id": "sess_...", "csrf_token": "a1b2c3d4..." }
   ```
2. **Form embedding**: Jinja2 templates include a hidden field in all forms:
   ```html
   <input type="hidden" name="_csrf" value="{{ csrf_token }}">
   ```
3. **HTMX headers**: For HTMX requests, include the CSRF token in headers:
   ```html
   <body hx-headers='{"X-CSRF-Token": "{{ csrf_token }}"}'>
   ```
4. **Middleware validation**: On all POST/PATCH/DELETE requests (except API token auth), the middleware checks `_csrf` form field or `X-CSRF-Token` header against the session's `csrf_token`. Mismatch → 403.
5. **WebSocket connections are exempt** from CSRF (they use token-based auth).

### Session Cleanup

- MongoDB TTL index on `expires_at` handles expired session deletion automatically.
- On explicit logout (`POST /auth/logout`), the session document is **immediately deleted** from MongoDB — do not rely solely on TTL.
- On login, any existing sessions for the same user are preserved (allow multi-device login).

## API Token Auth (Programmatic Access)

For bots and analysis tools that play via the API.

### Token Generation

```
POST /api/auth/token
Cookie: session_id=...  (must be logged in)

Response:
{
  "token": "ks_live_a1b2c3...",
  "expires_at": "2026-06-13T00:00:00Z"
}
```

### Token Format

Signed JWT with the following claims:

```json
{
  "sub": "664a1b...",            // user_id
  "username": "alexfil",
  "iat": 1710374400,
  "exp": 1718150400,             // 90 days
  "scope": "play"                // "play" | "admin"
}
```

Signed with HS256 using the app's `SECRET_KEY`.

### Token Usage

```
Authorization: Bearer ks_live_a1b2c3...
```

Or for WebSocket:
```
wss://kriegspiel.org/ws/game/{game_id}?token=ks_live_a1b2c3...
```

### Auth Priority

Request handling checks in order:
1. `Authorization: Bearer` header → JWT validation
2. `session_id` cookie → MongoDB lookup
3. `?token=` query param (WebSocket only) → JWT validation
4. None found → 401

### WebSocket Authentication Detail

WebSocket connections authenticate during the initial handshake:

1. Extract `?token=` from the WebSocket URL query params.
2. If the token starts with `ks_live_`, validate it as a JWT (API token auth).
3. Otherwise, treat it as a `session_id` and look it up in MongoDB.
4. If auth fails, close the WebSocket with code **1008** (policy violation).
5. If the user is not a participant in the requested game, close with code **4002**.
6. If the game is not in `active` or `paused` state, close with code **4003**.
7. On successful auth, **do not extend session expiry** — WebSocket connections are long-lived and sliding expiry on every message would be wasteful.

## OAuth (Phase 2)

Optional social login via Google. Implementation:

1. `GET /auth/oauth/google` → Redirect to Google consent screen
2. Google callback → `GET /auth/oauth/google/callback`
3. Exchange code for tokens, extract email + name
4. Find or create user by email
5. Link `auth_providers: ["google"]`
6. Create session, redirect to home

Library: **`authlib`** (supports OAuth2 with minimal code).

```python
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)
```

## Authorization

### Role Model

Simple two-role system:

| Role | Capabilities |
|---|---|
| `user` | Play games, view profiles, manage own account |
| `admin` | All user capabilities + suspend users, delete games, view audit log |

Role is stored on the user document:

```json
{
  "role": "user"    // "user" | "admin"
}
```

### Route Protection

```python
from functools import wraps
from fastapi import HTTPException, Request


def require_auth(func):
    """Ensure request has valid session/token."""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if not hasattr(request.state, "user"):
            raise HTTPException(401, "Authentication required")
        return await func(request, *args, **kwargs)
    return wrapper


def require_admin(func):
    """Ensure request is from admin user."""
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if not hasattr(request.state, "user"):
            raise HTTPException(401)
        user = await request.app.state.db.users.find_one(
            {"_id": request.state.user["user_id"]}
        )
        if user.get("role") != "admin":
            raise HTTPException(403, "Admin access required")
        return await func(request, *args, **kwargs)
    return wrapper
```

### Game-Level Authorization

```python
async def require_game_player(game_id: str, user_id: str, db) -> str:
    """
    Verify user is a participant in this game.
    Returns the player's color ("white" or "black").
    Raises 403 if user is not a player.
    """
    game = await db.games.find_one({"_id": game_id})
    if game["white"]["user_id"] == user_id:
        return "white"
    elif game["black"]["user_id"] == user_id:
        return "black"
    raise HTTPException(403, "You are not a player in this game")
```

## Security Measures

| Threat | Mitigation |
|---|---|
| Brute-force login | NGINX rate limit: 5 req/min on `/auth/login` |
| Brute-force registration | NGINX rate limit: 3 req/min on `/auth/register` |
| Session fixation | New session ID generated on every login |
| Session hijacking | `HttpOnly`, `Secure`, `SameSite=Lax` flags |
| CSRF | `SameSite=Lax` + CSRF token in forms (Jinja2 generates) |
| Timing attacks on password | `bcrypt.checkpw` is constant-time |
| Credential stuffing | Rate limiting + optional CAPTCHA (Phase 2) |
| Token leakage | Short-lived JWTs, token revocation via deny-list (Phase 2) |

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://kriegspiel.org",
        "https://www.kriegspiel.org",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)
```

Local development adds `http://localhost:8000` to origins.
