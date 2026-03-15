# Step 500 - Core Game UI

## Goal

Build the main player-facing web experience for landing, lobby polish, the live game board, phantom pieces, promotion, and referee presentation.

## Read First

- [FRONTEND.md](../../FRONTEND.md)
- [DESIGN.md](../../DESIGN.md)
- [API_SPEC.md](../../API_SPEC.md)

## Depends On

- `step-400`

## Task Slices

### 510 — Design System and Base Layout

**Create/modify these files:**

- `src/app/static/css/kriegspiel.css` — full CSS design system from DESIGN.md: CSS custom properties (colors, spacing, typography), base element styles, utility classes, nav styles, form styles, button styles, responsive breakpoints
- `src/app/templates/base.html` — update/finalize the base layout template:
  - Semantic HTML (`<nav>`, `<main>`, `<footer>`)
  - Nav with logo (♞ Kriegspiel), user area (login/register or username/logout)
  - HTMX script, CSRF headers in `hx-headers`
  - Meta tags, favicon reference, CSS link
  - Mobile viewport meta tag
- Download and place static assets:
  - Chess piece SVGs in `src/app/static/img/pieces/` (cburnett set — use standard filenames: `wK.svg`, `wQ.svg`, `bP.svg`, etc.)

**Acceptance criteria:**
- `kriegspiel.css` defines all custom properties from DESIGN.md
- `base.html` renders a clean page with nav and content area
- CSS works at desktop and mobile widths
- Chess piece SVGs are in place for chessboard.js

---

### 520 — Home Page and Rules Page

**Create these files:**

- `src/app/templates/home.html` — extends base.html:
  - Welcome hero section with description of Kriegspiel
  - "Play Now" button (links to /lobby if logged in, /auth/login if not)
  - "Learn the Rules" button (links to /rules)
  - Recent games section with HTMX auto-refresh (`hx-get="/api/game/recent" hx-trigger="load, every 30s"`)
- `src/app/templates/rules.html` — extends base.html:
  - Kriegspiel rules explanation (Berkeley variant with "Any?" rule)
  - What the referee announces, what players can see
  - How phantom pieces work
- `src/app/templates/partials/recent_games.html` — HTMX partial for recent completed games
- `src/app/routers/pages.py` — add routes:
  - `GET /` → render home.html
  - `GET /rules` → render rules.html
- `src/app/routers/game.py` — add `GET /api/game/recent` endpoint (returns last 10 completed games from `game_archives`)

**Acceptance criteria:**
- Home page renders with correct content and CTAs
- Rules page explains Kriegspiel clearly
- Recent games section loads and refreshes via HTMX
- Pages look correct on desktop and mobile

---

### 530 — Lobby Page Polish

**Modify these files:**

- `src/app/templates/lobby.html` — polish the lobby page from slice 350:
  - Apply DESIGN.md styles to create game form, join by code form, open games list, my active games
  - Add waiting-for-opponent state: when user creates a game, show game code prominently with a "Share this code" instruction and auto-poll for opponent joining
  - Add direct join URL display (`/join/{code}`)
  - Error/success feedback for create and join actions
  - Empty state messages ("No open games" / "No active games")
- `src/app/templates/partials/open_games.html` — polish with player username, rule variant, join button, time since creation
- `src/app/templates/partials/my_games.html` — polish with opponent name, game state, "your turn" indicator, resume link
- `src/app/routers/pages.py` — add `GET /join/{game_code}` route: if game exists and is waiting, redirect to lobby with auto-join; if game is active and user is participant, redirect to game page

**Acceptance criteria:**
- Lobby looks polished with consistent design system
- Create game shows waiting state with shareable code
- Open games auto-refresh and are joinable with one click
- My games show turn indicator and link to game page
- Direct join URLs (`/join/A7K2M9`) work correctly

---

### 540 — Game Page Template and Board

**Create these files:**

- `src/app/templates/game.html` — extends base.html, the core gameplay screen:
  - Two-column layout: board panel (left) + referee/actions panel (right)
  - Board container `<div id="board">` for chessboard.js
  - Referee log panel `<div id="referee-log" role="log" aria-live="polite">` — scrollable
  - Action buttons: "Ask Any?" and "Resign" (with confirmation dialog)
  - Clock display for both players
  - Opponent connection status indicator
  - Captured pieces summary
  - Phantom piece tray below the board
  - Responsive: stacks vertically on mobile (<768px)
  - Script tags for chessboard.js, chess.js, and game.js
  - Inline JS to initialize `KriegspielClient` with game_id and player_color from template context
- `src/app/routers/pages.py` — add `GET /game/{game_id}` route:
  - Requires auth
  - Loads game from DB, verifies user is a participant
  - Passes game_id, player_color, opponent_username, game state to template
  - If game is completed, redirect to review page

**Acceptance criteria:**
- `GET /game/{game_id}` renders the game page with correct layout
- Board container is present and sized correctly
- Referee log panel scrolls
- Action buttons are present (functional wiring in 550)
- Page is responsive (2-column desktop, stacked mobile)

---

### 550 — game.js WebSocket Client

**Create this file:**

- `src/app/static/js/game.js` — the `KriegspielClient` class as specified in FRONTEND.md (~190 lines without PhantomManager):
  - `connect()` — open WebSocket to `/ws/game/{game_id}`, set up onopen/onmessage/onclose handlers
  - `handleMessage(msg)` — switch on msg.type: connected, move_result, opponent_moved, any_result, opponent_asked_any, game_over, opponent_status, error, ping
  - `initBoard(msg)` — configure chessboard.js with player's FEN, orientation, drag-and-drop, piece theme
  - `sendMove(source, target, piece)` — convert to UCI, detect promotion (defer to 560)
  - `_sendUci(uci)` — send `{"action": "move", "uci": "..."}`
  - `sendAskAny()` — send `{"action": "ask_any"}`
  - `sendResign()` — send `{"action": "resign"}`
  - `handleMoveResult(msg)` — update board FEN, update referee log, update clock, update possible_actions (enable/disable Ask Any button)
  - `handleOpponentMoved(msg)` — update board FEN (opponent's move is invisible but FEN changes if captures occurred), append referee announcement, update clock, show illegal attempt count
  - `handleGameOver(msg)` — show result overlay, reveal full board, disable interactions, show link to review
  - `updateOpponentStatus(msg)` — update connection indicator
  - `appendReferee(text)` — add entry to referee log panel with scroll-to-bottom
  - `updateClock(clockData)` — update clock display, start/stop countdown timer
  - `scheduleReconnect()` — exponential backoff: 1s, 2s, 4s, 8s, 16s, 30s cap, max 10 attempts
  - `showError(message)` — display error in referee panel
  - Wire up "Ask Any?" button click → `sendAskAny()`
  - Wire up "Resign" button click → confirm dialog → `sendResign()`

**Acceptance criteria:**
- WebSocket connects and receives `connected` message
- Board renders with correct FEN and orientation
- Making a legal move sends UCI and updates board
- Referee log shows announcements
- Reconnection works with exponential backoff
- Clock ticks down for active player
- Game over shows result and disables board

---

### 560 — Phantom Pieces, Promotion Modal, Interaction Polish

**Create/modify these files:**

- `src/app/static/js/game.js` — add `PhantomManager` class (~80 lines) as specified in FRONTEND.md:
  - All methods: `place`, `move`, `remove`, `displace`, `clear`, `render`, `_save`, `_loadFromStorage`, `_initTray`
  - localStorage persistence keyed by game_id
  - Phantom pieces rendered at 50% opacity with dashed outline
  - Right-click/long-press to remove phantom
  - Phantom displaced when real piece moves to that square
- Add promotion modal to `game.js`:
  - Detect pawn reaching promotion rank
  - Show modal with 4 piece options (Queen, Rook, Bishop, Knight)
  - On selection: append promotion suffix to UCI (q/r/b/n) and send
  - On cancel (click outside): return pawn to source square
- `src/app/static/css/kriegspiel.css` — add CSS for:
  - `.phantom-piece` (50% opacity, dashed outline, cursor: grab)
  - `.phantom-tray` (bg-subtle, border, padding, piece sizing)
  - `.promotion-modal` (centered overlay, piece buttons, backdrop)
- Polish:
  - Highlighted squares for last move
  - Turn indicator visual emphasis
  - Sound effect hooks (optional, just the event emission — actual sounds can be added later)
  - Mobile touch support confirmation

**Acceptance criteria:**
- Phantom pieces can be dragged from tray to board
- Phantoms persist in localStorage across page reloads
- Right-click removes a phantom piece
- Real piece landing on phantom square displaces the phantom
- Promotion modal appears on pawn reaching last rank
- Selecting a promotion piece sends correct UCI suffix
- Canceling promotion returns pawn to source
- Phantoms render at 50% opacity and are visually distinct

---

## Required Tests Before Done

- Frontend smoke tests for primary pages (load without JS errors)
- Manual QA: create game, join, make moves, see referee log, use phantoms, promote pawn, resign
- Check responsive layout at desktop and mobile widths

## Exit Criteria

- The live game page is usable end-to-end by a human player
- Phantom pieces work and remain client-only
- Promotion uses an explicit chooser
- The core pages match the intended design system well enough for MVP use

## Out of Scope

- Profile/history/leaderboard features
- Deploy/VPS/TLS work
- Final launch QA
