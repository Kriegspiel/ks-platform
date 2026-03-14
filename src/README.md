# Source Code

Implementation source code for the Kriegspiel platform. This directory mirrors the project structure defined in [MILESTONES.md](../MILESTONES.md) (Milestone 1.1).

## Directory Layout

```
src/
├── app/                        # FastAPI application
│   ├── main.py                 # App factory, startup/shutdown hooks
│   ├── config.py               # Pydantic settings (env vars → typed config)
│   ├── database.py             # Motor async MongoDB client setup
│   ├── dependencies.py         # FastAPI dependency injection (get_db, get_current_user)
│   │
│   ├── routers/                # URL route handlers
│   │   ├── auth.py             # /auth/* — login, register, logout
│   │   ├── game.py             # /api/game/* — create, join, list, resign
│   │   ├── user.py             # /api/user/* — profile, stats, game history
│   │   ├── pages.py            # /* — server-rendered Jinja2 pages
│   │   └── ws.py               # /ws/* — WebSocket gameplay handlers
│   │
│   ├── services/               # Business logic (framework-agnostic, testable)
│   │   ├── user_service.py     # Registration, auth, profile CRUD
│   │   ├── game_service.py     # Game lifecycle, wraps kriegspiel.BerkeleyGame
│   │   └── matchmaking_service.py  # Open game listings, pairing
│   │
│   ├── models/                 # Pydantic models (request/response schemas)
│   │   ├── auth.py             # LoginRequest, RegisterRequest, SessionInfo
│   │   ├── game.py             # CreateGameRequest, GameState, MoveResult
│   │   └── user.py             # UserProfile, UserStats, GameHistoryItem
│   │
│   ├── ws/                     # WebSocket management
│   │   ├── manager.py          # ConnectionManager — tracks active connections
│   │   └── handlers.py         # Message handlers (move, ask_any, resign)
│   │
│   ├── templates/              # Jinja2 HTML templates
│   │   ├── base.html           # Base layout (header, footer, theme toggle)
│   │   ├── home.html           # Landing page
│   │   ├── login.html          # Login form
│   │   ├── register.html       # Registration form
│   │   ├── lobby.html          # Game lobby (create/join/list)
│   │   ├── game.html           # Active gameplay (board + referee)
│   │   ├── review.html         # Post-game review
│   │   ├── profile.html        # User profile + stats
│   │   └── leaderboard.html    # ELO rankings
│   │
│   ├── static/                 # Static assets (served by NGINX in production)
│   │   ├── css/                # kriegspiel.css (design system from DESIGN.md)
│   │   ├── js/                 # game.js (WebSocket client), review.js
│   │   ├── img/pieces/         # Chess piece SVGs (Staunton set)
│   │   └── sounds/             # Optional move/capture/check sounds
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── mongo/
│   └── init-replica.sh         # Single-node replica set initialization
│
├── nginx/
│   ├── nginx.conf              # Global NGINX config
│   └── conf.d/
│       └── kriegspiel.conf     # Site config (TLS, proxying, rate limits)
│
└── tests/
    ├── conftest.py             # Shared fixtures (test DB, test client, mock game)
    ├── test_auth.py            # Registration, login, logout, sessions
    ├── test_game_service.py    # Game lifecycle unit tests
    ├── test_game_api.py        # REST API integration tests
    ├── test_websocket.py       # WebSocket gameplay tests
    └── test_user.py            # Profile and stats tests
```

## Implementation References

Each file should be implemented according to the corresponding spec document:

| Component | Spec Document |
|---|---|
| App structure, services, routers | [ARCHITECTURE.md](../ARCHITECTURE.md) |
| MongoDB collections, indexes | [DATA_MODEL.md](../DATA_MODEL.md) |
| REST + WebSocket endpoints | [API_SPEC.md](../API_SPEC.md) |
| Game engine integration | [GAME_ENGINE.md](../GAME_ENGINE.md) |
| Auth flow, sessions, OAuth | [AUTH.md](../AUTH.md) |
| Templates, pages, JS | [FRONTEND.md](../FRONTEND.md) |
| CSS, colors, typography | [DESIGN.md](../DESIGN.md) |
| Docker, NGINX, CI/CD | [INFRA.md](../INFRA.md) |
| Logo SVG assets | [LOGO.md](../LOGO.md) |

## Key Dependencies

```
# requirements.txt (expected)
fastapi>=0.110
uvicorn[standard]>=0.30
motor>=3.4                     # Async MongoDB driver
pydantic>=2.7
pydantic-settings>=2.3
kriegspiel>=X.Y                # PyPI game engine
python-multipart>=0.0.9        # Form parsing
jinja2>=3.1
bcrypt>=4.1
itsdangerous>=2.2              # Session signing
httpx>=0.27                    # OAuth HTTP client (Phase 2)
structlog>=24.1                # Structured logging
```
