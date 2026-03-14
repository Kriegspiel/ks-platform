# Kriegspiel Platform — Implementation Plan

A modern web platform for playing **Kriegspiel chess** (Berkeley + Any rules) online.

> Kriegspiel is a chess variant of imperfect information: players cannot see their opponent's pieces. A referee announces legality of moves, captures (by square), checks (by direction), and game endings. The "Any?" rule allows players to ask if pawn captures exist before committing.

## What This Repo Contains

This repository is the **blueprint** for building the Kriegspiel platform. It contains no application code — only detailed specifications that a development team (human or AI agents) can follow to build each component.

| Document | Description |
|---|---|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System architecture, service boundaries, deployment topology |
| [DATA_MODEL.md](./DATA_MODEL.md) | MongoDB collections, document schemas, indexes |
| [API_SPEC.md](./API_SPEC.md) | REST + WebSocket API contracts |
| [GAME_ENGINE.md](./GAME_ENGINE.md) | Game logic integration with `kriegspiel` PyPI package |
| [AUTH.md](./AUTH.md) | Authentication & authorization design |
| [FRONTEND.md](./FRONTEND.md) | Web client architecture and UI specifications |
| [INFRA.md](./INFRA.md) | Docker, CI/CD, deployment, monitoring |
| [MILESTONES.md](./MILESTONES.md) | Phased delivery plan with acceptance criteria |
| [LOGO.md](./LOGO.md) | Logo design spec — double-headed knight, light/dark theme toggle |
| [DESIGN.md](./DESIGN.md) | Visual design system — colors, typography, spacing, components |

## Repository Structure

Beyond the plan documents above, this repo contains scaffold directories for implementation. Agents building the platform should place code and assets in these locations:

```
ks-platform/
├── README.md                   # This file
├── ARCHITECTURE.md             # System architecture
├── DATA_MODEL.md               # MongoDB schemas
├── API_SPEC.md                 # REST + WebSocket API
├── GAME_ENGINE.md              # Game engine integration
├── AUTH.md                     # Authentication design
├── FRONTEND.md                 # Frontend spec
├── DESIGN.md                   # Visual design system
├── INFRA.md                    # Infrastructure & deployment
├── MILESTONES.md               # Delivery plan
├── LOGO.md                     # Logo specification
│
├── docs/                       # Additional implementation docs
│   └── adr/                    # Architecture Decision Records
│
├── src/                        # Source code (implementation)
│   ├── app/                    # FastAPI application
│   │   ├── routers/            # Route handlers
│   │   ├── services/           # Business logic
│   │   ├── models/             # Pydantic schemas
│   │   ├── ws/                 # WebSocket management
│   │   ├── templates/          # Jinja2 HTML templates
│   │   └── static/             # CSS, JS, images, sounds
│   ├── mongo/                  # MongoDB init scripts
│   ├── nginx/                  # NGINX config
│   └── tests/                  # Test suite
│
├── assets/                     # Design assets
│   ├── logo/                   # SVG logo, favicon, icons
│   └── og-images/              # Social sharing images
│
└── scripts/                    # Ops scripts (backup, deploy, seed)
```

Each directory contains a `README.md` explaining what belongs there and which spec document to follow.

## Domain

**Production URL:** [https://kriegspiel.org](https://kriegspiel.org)

The domain is owned by the project. See [INFRA.md](./INFRA.md) for DNS, TLS, and deployment configuration.

## Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Language | **Python 3.12+** | Owner fluency; ecosystem maturity |
| Web framework | **FastAPI** | Native async/await, WebSocket support, Pydantic validation, auto-generated OpenAPI docs |
| Database | **MongoDB 7+** | Document structure fits game state naturally; Change Streams for real-time |
| Game engine | **`kriegspiel` PyPI package** ([ks-game](https://github.com/kriegspiel/ks-game)) | Already battle-tested, serializable, covers Berkeley + Any rules |
| Real-time | **WebSocket** (FastAPI native) | Low-latency move delivery; replaces old 3-second polling |
| Frontend | **Jinja2 templates + HTMX + chessboard.js** | Python-centric stack; minimal JS; server-rendered |
| Auth | **Session-based + optional OAuth** | Simple for users; JWT available for API clients |
| Deployment | **Docker Compose → single VPS** | Minimal ops overhead for a niche game; 1 Uvicorn worker (no Redis needed for Phase 1) |

## Existing Ecosystem

This platform builds on top of existing repos in the [kriegspiel](https://github.com/kriegspiel) org:

- **[ks-game](https://github.com/kriegspiel/ks-game)** — Python game engine (PyPI: `kriegspiel`). Berkeley + Any rules. JSON serialization. This is the core dependency.
- **[old-ks-flask-app](https://github.com/kriegspiel/old-ks-flask-app)** — Prior Flask prototype. Informs the new design but is fully superseded.
- **[content](https://github.com/kriegspiel/content)** — Rules documentation (Berkeley, Wild 16).
- **[ks-home](https://github.com/kriegspiel/ks-home)** — Static site at kriegspiel.org.

## Quick Reference: Berkeley + Any Rules

From [content/rules/berkeley.md](https://github.com/kriegspiel/content/blob/master/rules/berkeley.md):

- **Imperfect information**: Each player sees only their own pieces. The referee has the true board.
- **Move attempts**: Player tries a move → Referee says "Yes" (legal), "No" (illegal), or "Nonsense" (not a valid attempt).
- **Captures**: Referee announces square only (e.g., "Capture at d4"). Captured piece identity is hidden.
- **Checks**: Referee announces direction — Rank / File / Long diagonal / Short diagonal / Knight / Double check.
- **Not announced**: Castling, en passant, pawn promotions happen silently.
- **"Any?" rule**: Player may ask "Any pawn captures?" → Referee says "Try" (must then capture with pawn) or "No" (count added to illegal tries visible to opponent).
- **Opponent piece tracking (phantom pieces)**: Since players cannot see opponent pieces, the UI provides a full set of opponent-colored "phantom" pieces that the player can freely place, move, and remove on the board as personal memory aids. Phantom pieces are entirely client-side — they never affect the game state and are never sent to the server. Players use them to track where they believe opponent pieces are.
- **Game end**: Checkmate or stalemate announced. No 3-fold repetition or 50-move draw rules.
- **Material stalemate**: Standard chess insufficient-material rules apply.

## Document Authority

When specs overlap, the following precedence applies:

| Topic | Authoritative Document | Notes |
|---|---|---|
| Visual design & styling | [DESIGN.md](./DESIGN.md) | Overrides any styling mentions in FRONTEND.md |
| Database schemas | [DATA_MODEL.md](./DATA_MODEL.md) | Overrides inline schemas in other docs |
| API contracts | [API_SPEC.md](./API_SPEC.md) | Overrides inline examples in ARCHITECTURE.md |
| Engine integration | [GAME_ENGINE.md](./GAME_ENGINE.md) | Code in ARCHITECTURE.md is illustrative only |
| Game state transitions | [ARCHITECTURE.md](./ARCHITECTURE.md) | State machine is defined here |

**Recommended reading order:** README → ARCHITECTURE → GAME_ENGINE → DATA_MODEL → API_SPEC → AUTH → FRONTEND → DESIGN → INFRA → MILESTONES
