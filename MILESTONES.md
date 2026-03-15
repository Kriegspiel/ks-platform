# Milestones & Delivery Plan

## Phase 1: Foundation (MVP)

**Goal:** Two players can create a game, join via code, and play Kriegspiel (Berkeley + Any) with a **Rapid 25+10** Fischer clock to completion through a web browser.

### Milestone 0 — Design System

| Task | Details | Acceptance Criteria |
|---|---|---|
| Create `kriegspiel.css` | Implement [DESIGN.md](./DESIGN.md) as a single CSS file | All CSS custom properties defined; all component classes implemented |
| Light/dark theme | `[data-theme="dark"]` toggles all colors | Both themes render correctly; toggle via logo click works |
| Responsive breakpoints | Desktop / tablet / mobile layouts | Container width, game layout, and mobile stacking verified at all breakpoints |
| Font loading | Google Fonts: Playfair Display, Inter, JetBrains Mono | Fonts load with `font-display: swap`; correct weights used |

**Testing:** Visual inspection at all breakpoints. Both themes. All component classes render correctly.

### Milestone 1.1 — Project Scaffold

| Task | Details | Acceptance Criteria |
|---|---|---|
| Init FastAPI project | `main.py`, router stubs, Pydantic settings | `cd src && uvicorn app.main:app` starts, `/health` returns 200 |
| MongoDB connection | Motor async client, connection pooling | App connects to MongoDB replica set on startup |
| Docker Compose | App + MongoDB + NGINX containers | `docker compose up` starts all services; app accessible at localhost |
| Project structure | See below | All directories and `__init__.py` files in place |

**Project structure:**

```
ks-platform/
├── src/
│   ├── app/
│   │   ├── main.py                 # FastAPI app factory
│   │   ├── config.py               # Pydantic settings (env vars)
│   │   ├── database.py             # Motor client setup
│   │   ├── dependencies.py         # FastAPI dependency injection
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py             # /auth/* endpoints
│   │   │   ├── game.py             # /api/game/* endpoints
│   │   │   ├── user.py             # /api/user/* endpoints
│   │   │   ├── pages.py            # / server-rendered pages
│   │   │   └── ws.py               # /ws/* WebSocket handlers
│   │   │
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── game_service.py
│   │   │   └── matchmaking_service.py
│   │   │
│   │   ├── models/                 # Pydantic models (request/response)
│   │   │   ├── auth.py
│   │   │   ├── game.py
│   │   │   └── user.py
│   │   │
│   │   ├── ws/
│   │   │   ├── manager.py          # ConnectionManager
│   │   │   └── handlers.py         # WebSocket message handlers
│   │   │
│   │   ├── templates/              # Jinja2 HTML templates
│   │   │   ├── base.html
│   │   │   ├── home.html
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── lobby.html
│   │   │   ├── game.html
│   │   │   ├── review.html
│   │   │   ├── profile.html
│   │   │   └── leaderboard.html
│   │   │
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   │   ├── game.js         # WebSocket client (~270 lines)
│   │   │   │   └── review.js       # Post-game replay
│   │   │   ├── img/
│   │   │   │   └── pieces/         # Chess piece SVGs
│   │   │   └── sounds/             # Optional sound effects
│   │   │
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── requirements-dev.txt
│   │
│   ├── mongo/
│   │   └── init-replica.sh
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── conf.d/
│   │       └── kriegspiel.conf
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_game_service.py
│       ├── test_game_api.py
│       ├── test_websocket.py
│       └── test_user.py
├── docker-compose.yml
├── .env.example
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

### Milestone 1.2 — Authentication

| Task | Details | Acceptance Criteria |
|---|---|---|
| Registration | `POST /auth/register` with validation | User created in DB with bcrypt hash; session cookie set |
| Login | `POST /auth/login` | Valid credentials → session cookie; invalid → 401 |
| Logout | `POST /auth/logout` | Session deleted from DB; cookie cleared |
| Session middleware | Check cookie on every request | Protected routes return 401 without valid session |
| Login/register pages | Jinja2 forms | Forms render, submit, show validation errors |

**Testing:** Unit tests for `UserService` (registration validation, password hashing, login). Integration tests for `/auth/*` endpoints. Minimum 80% coverage for `services/user_service.py`.

### Milestone 1.3 — Game Lifecycle (REST)

| Task | Details | Acceptance Criteria |
|---|---|---|
| Create game | `POST /api/game/create` | Game doc inserted with state=waiting; join code returned |
| Join game | `POST /api/game/join/{code}` | Second player added; state → active |
| List open games | `GET /api/game/open` | Returns games with state=waiting |
| Lobby page | Jinja2 + HTMX | Create form, join form, open games list (auto-refreshing) |

**Testing:** Unit tests for `GameService` (create, join, state transitions). Integration tests for `/api/game/*` endpoints. Minimum 80% coverage for `services/game_service.py`.

### Milestone 1.4 — Gameplay (WebSocket)

| Task | Details | Acceptance Criteria |
|---|---|---|
| WS connection | `/ws/game/{game_id}` | Browser handshake uses the session cookie; external clients may pass an API token query param. Player assigned to color, initial board sent |
| Regular moves | `{"action": "move", "uci": "e2e4"}` | Engine processes move; both players get appropriate messages |
| "Any?" question | `{"action": "ask_any"}` | HAS_ANY/NO_ANY handled; must_use_pawns enforced |
| Illegal moves | Engine returns ILLEGAL_MOVE | Moving player sees "No."; opponent sees attempt count increment |
| Check/capture | Engine announcements | Both players see capture square and check direction |
| Game over | Checkmate/stalemate/draw | Both players notified; full board revealed; stats updated |
| Resign | `{"action": "resign"}` | Game ends; opponent wins; both notified |
| Reconnection | Player reconnects after disconnect | Exponential backoff (1s-30s, 10 attempts); game state fully restored; opponent notified; phantom pieces restored from localStorage |
| Phantom pieces | Client-side opponent piece tracking | PhantomManager class works; pieces draggable from tray to board; stored in localStorage; visual distinction (50% opacity, dashed outline) |
| Pawn promotion | Promotion piece selector modal | When pawn reaches last rank, modal appears with Q/R/B/N; selected piece appended to UCI; promotion executes correctly |
| Time control | Fischer clock (25+10 rapid) | Countdown displayed for both players; flag on timeout; clock pauses on disconnect |
| Game page | `game.html` + `game.js` | Board renders; drag-and-drop works; referee panel updates; phantom tray visible; clock displays |

### Milestone 1.5 — Polish & Deploy

| Task | Details | Acceptance Criteria |
|---|---|---|
| User profile page | `/user/{username}` | Stats, recent games displayed |
| Game history | `/user/{username}/games` | Paginated list of completed games |
| Game review page | `/game/{game_id}/review` | Move-by-move replay with board |
| Leaderboard | `/leaderboard` | Sorted by ELO, paginated |
| Error handling | 404, 500 pages; WS error messages | Graceful handling of all error states |
| TLS setup | Let's Encrypt via certbot | HTTPS works; HTTP redirects to HTTPS |
| CI pipeline | GitHub Actions | Tests + lint run on PR; deploy on merge to main |
| Backup script | Daily mongodump | Cron job running; backups verified |
| First deploy | VPS provisioning + deploy | kriegspiel.org serves the platform |

---

## Phase 2: Enhanced Experience

**Goal:** Social features, better matchmaking, and quality-of-life improvements.

| Feature | Details |
|---|---|
| **Additional time controls** | Blitz (5+3), Classical (45+15) — extends the rapid (25+10) from Phase 1 |
| **ELO system** | Standard ELO calculation after each rated game; separate rated/casual queues |
| **OAuth login** | Google sign-in via `authlib` |
| **Draw offers** | In-game draw offer/accept/decline |
| **Spectator mode** | Watch live games; spectators see referee announcements only (not the board) |
| **Sound effects** | Move, capture, check, game-over sounds |
| **Board themes** | Multiple board colors and piece sets |
| **Game chat** | Optional text chat between players during/after game |
| **Rematch** | "Play again" button after game ends |

---

## Phase 3: Community & Scale

**Goal:** Build community features and prepare for growth.

| Feature | Details |
|---|---|
| **Tournaments** | Swiss-system tournament creation and management |
| **Bot opponents** | AI player using random legal moves (beginner) and heuristic play (intermediate) |
| **Game annotations** | Post-game comments and analysis by players |
| **Email notifications** | "It's your turn" and "New game invitation" emails |
| **Mobile optimization** | PWA with offline game review; touch-optimized board |
| **Redis pub/sub** | Cross-worker WebSocket routing for horizontal scaling |
| **CDN** | Static assets served via Cloudflare |
| **Monitoring** | Prometheus + Grafana for app metrics |
| **Additional rule variants** | Crazykrieg, Wild 16 (when ks-game adds support) |

---

## Estimated Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| Phase 1 (MVP) | 4-6 weeks | Playable Kriegspiel with accounts, lobby, game review |
| Phase 2 | 3-4 weeks | Time controls, ELO, OAuth, spectators, polish |
| Phase 3 | Ongoing | Community features, scaling, new variants |

These estimates assume a single developer (or AI agent) working full-time. The codebase is intentionally small (~2,000-3,000 lines of Python for Phase 1) to keep it manageable.

---

## Definition of Done (All Phases)

- [ ] All acceptance criteria met
- [ ] Tests passing (>80% coverage for services)
- [ ] No lint errors (`black` + `ruff`)
- [ ] Docker Compose starts cleanly from scratch
- [ ] README updated with any new setup steps
- [ ] No secrets committed to git
