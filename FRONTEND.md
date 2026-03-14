# Frontend Specification

## Design Philosophy

Server-rendered pages with minimal JavaScript. The owner reads Python, not TypeScript — so the frontend is **Jinja2 templates + HTMX + vanilla JS**, not a React/Vue SPA. The only significant JS is the chessboard interaction and WebSocket handling.

## Tech Stack

| Component | Library | Purpose |
|---|---|---|
| Templates | **Jinja2** (FastAPI built-in) | Server-rendered HTML |
| Dynamic updates | **HTMX 2.x** | Lobby refresh, partial page updates without full reload |
| Chess board | **chessboard.js 1.0** | Drag-and-drop board UI, piece rendering |
| Chess validation | **chess.js** | Client-side move format validation (UCI generation) |
| Styling | **Custom `kriegspiel.css`** | Design system from [DESIGN.md](./DESIGN.md) — no CSS framework |
| Icons | **Lucide** | Lightweight icon set |
| WebSocket | **Native browser API** | Game communication |

Total JS payload: < 100 KB gzipped.

> **Note:** [DESIGN.md](./DESIGN.md) is authoritative for all visual and styling decisions. Any styling mentions in this document are informational — if they conflict with DESIGN.md, DESIGN.md wins.

## Page Map

```
/                          → Home (landing + login prompt)
/auth/login                → Login form
/auth/register             → Registration form
/lobby                     → Game lobby (create/join/open games)
/join/{game_code}          → Direct join link (redirects to lobby or game)
/game/{game_id}            → Active game (chessboard + referee panel)
/game/{game_id}/review     → Post-game review (full board replay)
/user/{username}           → Public profile + game history
/user/{username}/games     → Paginated game history
/leaderboard               → ELO rankings
/settings                  → User preferences (board theme, sounds, etc.)
/rules                     → Kriegspiel rules reference
```

## Page Specifications

### Home (`/`)

```
┌─────────────────────────────────────────┐
│  ♞ Kriegspiel                    Login  │
├─────────────────────────────────────────┤
│                                         │
│       Welcome to Kriegspiel             │
│                                         │
│  The chess variant of imperfect         │
│  information. You can't see your        │
│  opponent's pieces — only the           │
│  referee's announcements.               │
│                                         │
│  [ Play Now ]    [ Learn the Rules ]    │
│                                         │
│  ─── Recent Games ───────────────────   │
│  alexfil vs opponent1 — White wins      │
│  player2 vs player3 — Draw              │
│                                         │
└─────────────────────────────────────────┘
```

- If logged in: "Play Now" goes to `/lobby`
- If not logged in: "Play Now" goes to `/auth/login`
- Recent games list: `<div id="recent-games" hx-get="/api/game/recent" hx-trigger="load, every 30s" hx-swap="innerHTML">`

### Lobby (`/lobby`)

```
┌─────────────────────────────────────────┐
│  ♞ Kriegspiel    alexfil    ⚙ Logout   │
├─────────────────────────────────────────┤
│                                         │
│  ┌─── Create Game ────────────────────┐ │
│  │ Rules: [Berkeley+Any ▾]            │ │
│  │ Play as: (●) Random (○) White (○) Black │
│  │ [ Create & Wait for Opponent ]     │ │
│  └────────────────────────────────────────┘ │
│                                         │
│  ┌─── Join by Code ──────────────────┐  │
│  │ Code: [______]  [ Join ]          │  │
│  └────────────────────────────────────────┘ │
│                                         │
│  ─── Open Games ─────────────────────   │
│  ┌──────────────────────────────────┐   │
│  │ grandmaster42 │ Berkeley+Any │ ▶ │   │
│  │ newplayer1    │ Berkeley     │ ▶ │   │
│  │ chessbot9000  │ Berkeley+Any │ ▶ │   │
│  └──────────────────────────────────┘   │
│  (refreshes via HTMX every 5s)         │
│                                         │
│  ─── My Active Games ───────────────    │
│  alexfil vs opponent1 — your turn  ▶   │
│                                         │
└─────────────────────────────────────────┘
```

- "Open Games" list: `<div id="open-games" hx-get="/api/game/open" hx-trigger="every 5s" hx-swap="innerHTML" hx-target="#open-games">`
- "My Active Games": `<div id="my-games" hx-get="/api/game/mine" hx-trigger="every 10s" hx-swap="innerHTML">`
- "Join by Code" form: `<form hx-post="/api/game/join/{code}" hx-target="#join-result" hx-swap="innerHTML">`
- Shows games where user is a participant and state is "active" or "paused"

### Game (`/game/{game_id}`)

This is the core gameplay screen.

```
┌─────────────────────────────────────────────────────────────┐
│  ♞ Kriegspiel    alexfil (white) vs opponent1 (black)       │
├──────────────────────────────────┬────────────────────────┤
│                                  │  ─── Referee ─────────── │
│     8 │ . . . . . . . .         │                          │
│     7 │ . . . . . . . .         │  Move 12. White's turn.  │
│     6 │ . . . . . . . .         │                          │
│     5 │ . . . . . . . .         │  > "Capture on d4."      │
│     4 │ . . . . P . . .         │  > "Check on a rank."    │
│     3 │ . . . . . . . .         │  > "No."                 │
│     2 │ P P P P . P P P         │  > "Yes."                │
│     1 │ R N B Q K B N R         │                          │
│       └─────────────────         │  ─── Actions ────────── │
│         a b c d e f g h          │  [ Ask "Any?" ]          │
│                                  │  [ Resign ]              │
│                                  │  ─── Clock ──────────── │
│                                  │  White: 24:58            │
│                                  │  Black: 25:00  ●         │
│                                  │                          │
│  opponent1 ● connected           │                          │
│                                  │  ─── Captured ────────── │
│                                  │  You lost: ♟             │
│                                  │  Captures: d4, f6        │
│                                  │                          │
└──────────────────────────────────┴────────────────────────┘
```

#### Board Panel (left)

- `chessboard.js` renders the board
- Only the player's own pieces are shown (opponent squares empty)
- Drag-and-drop to make moves
- Board orientation matches player color (black sees board flipped)
- Highlighted squares: last move origin/destination (own moves only)

#### Referee Panel (right)

- Scrollable log of all referee announcements in chronological order
- New announcements appear at the bottom with a brief highlight animation
- Announcements use the human-readable format from GAME_ENGINE.md
- Both players see the same announcements (per Berkeley rules)

#### Action Buttons

- **"Ask Any?"** — visible only when ASK_ANY is in possible_actions
- **"Resign"** — always visible; requires confirmation dialog
- **"Offer Draw"** — Phase 2

#### Status Indicators

- Opponent connection status (green dot = connected, gray = disconnected)
- Turn indicator (whose turn, visually emphasized)
- Move counter

### Phantom Pieces (Opponent Tracking)

Since players cannot see their opponent's pieces, the UI provides a set of **phantom pieces** — opponent-colored pieces that the player can freely place, move, and remove on the board as personal memory aids for tracking where they believe opponent pieces are.

Phantom pieces are **entirely client-side**. They are never sent to the server and never affect the game state.

#### Behavior

- On game start, a **phantom tray** appears below the board containing 16 opponent-colored pieces: 1 King, 1 Queen, 2 Rooks, 2 Bishops, 2 Knights, 8 Pawns.
- **Place**: Player drags a phantom piece from the tray onto any empty board square.
- **Move**: Player drags an existing phantom piece on the board to a different square.
- **Remove**: Player right-clicks (desktop) or long-presses (mobile) a phantom piece to return it to the tray.
- Phantom pieces are rendered at **50% opacity** with a **dashed outline** to visually distinguish them from the player's real pieces.
- Phantom pieces do **not** block or interact with real piece movement. The player can place a real piece on a square that has a phantom — the phantom is automatically returned to the tray.
- When a capture is announced ("Capture on d4"), the player may choose to remove a phantom from that square (manual, not automatic — the player decides which piece they think was captured).

#### Storage

- Phantom positions are stored in `localStorage` keyed by game ID.
- Key: `phantoms_{game_id}` → JSON array of `{"piece": "bQ", "square": "d8"}`.
- On page reload or WebSocket reconnect, phantom positions are restored from `localStorage`.
- On game end, phantom data is cleared from `localStorage`.

#### UI Layout

```
┌──────────────────────────────────────┐
│          Chessboard                   │
│       (player's real pieces)          │
│                                       │
│   (phantom pieces shown at 50%        │
│    opacity with dashed outline)       │
│                                       │
├──────────────────────────────────────┤
│  Phantom Tray                         │
│  ♚ ♛ ♜ ♜ ♝ ♝ ♞ ♞ ♟♟♟♟♟♟♟♟          │
│  (pieces not yet placed on board)     │
└──────────────────────────────────────┘
```

- The tray uses `--bg-subtle` background, `--border-default` border, 8px padding.
- Tray pieces are 32px, shown at 50% opacity, with `cursor: grab`.
- See [DESIGN.md](./DESIGN.md) for exact CSS classes (`.phantom-piece`, `.phantom-tray`).

#### Implementation (game.js — PhantomManager class, ~80 lines)

```javascript
class PhantomManager {
    constructor(gameId, opponentColor) {
        this.gameId = gameId;
        this.color = opponentColor;      // "b" or "w"
        this.placed = new Map();         // square -> piece (e.g., "d8" -> "bQ")
        this.tray = [];                  // pieces not on the board
        this._loadFromStorage();
    }

    place(piece, square) {
        // Move piece from tray to board
        this.tray = this.tray.filter(p => p !== piece);
        this.placed.set(square, piece);
        this._save();
    }

    move(fromSquare, toSquare) {
        const piece = this.placed.get(fromSquare);
        if (!piece) return;
        this.placed.delete(fromSquare);
        this.placed.set(toSquare, piece);
        this._save();
    }

    remove(square) {
        const piece = this.placed.get(square);
        if (!piece) return;
        this.placed.delete(square);
        this.tray.push(piece);
        this._save();
    }

    displace(square) {
        // Called when a real piece lands on a phantom's square
        this.remove(square);
    }

    clear() {
        this.placed.clear();
        this.tray = [];
        localStorage.removeItem(`phantoms_${this.gameId}`);
    }

    render(boardElement) {
        // Overlay phantom pieces onto chessboard.js board using
        // absolutely-positioned elements at 50% opacity.
        // Implementation depends on chessboard.js API.
    }

    _save() {
        const data = [];
        for (const [square, piece] of this.placed) {
            data.push({ piece, square });
        }
        localStorage.setItem(`phantoms_${this.gameId}`, JSON.stringify({
            placed: data,
            tray: this.tray
        }));
    }

    _loadFromStorage() {
        const raw = localStorage.getItem(`phantoms_${this.gameId}`);
        if (raw) {
            const data = JSON.parse(raw);
            data.placed.forEach(({ piece, square }) => this.placed.set(square, piece));
            this.tray = data.tray;
        } else {
            this._initTray();
        }
    }

    _initTray() {
        // Full set of opponent pieces
        const c = this.color;
        this.tray = [
            `${c}K`, `${c}Q`, `${c}R`, `${c}R`,
            `${c}B`, `${c}B`, `${c}N`, `${c}N`,
            `${c}P`, `${c}P`, `${c}P`, `${c}P`,
            `${c}P`, `${c}P`, `${c}P`, `${c}P`
        ];
    }
}
```

### Pawn Promotion

When a pawn is dragged to the promotion rank (rank 8 for white, rank 1 for black):

1. A **promotion modal** appears centered over the board with 4 piece icons: Queen, Rook, Bishop, Knight.
2. Player clicks a piece to select the promotion. The move is then sent with the UCI promotion suffix (e.g., `"e7e8q"`, `"e7e8r"`, `"e7e8b"`, `"e7e8n"`).
3. If the player clicks outside the modal, the move is cancelled and the pawn returns to its source square.
4. The modal uses [DESIGN.md](./DESIGN.md) `.promotion-modal` styling.

```
┌─────────────────────────────┐
│     Choose promotion:       │
│                             │
│    ♛    ♜    ♝    ♞        │
│                             │
└─────────────────────────────┘
```

Per Berkeley rules, pawn promotion is **silent** — the referee says nothing special about it beyond the normal move result ("Yes" or "No"). The opponent does not know a promotion occurred.

### Game Review (`/game/{game_id}/review`)

Post-game analysis page. Available after game ends.

```
┌─────────────────────────────────────────────────────────────┐
│  Game Review: alexfil vs opponent1                          │
├──────────────────────────────────┬────────────────────────┤
│                                  │  ─── Move Log ────────── │
│     Full board (referee view)    │                          │
│     showing all pieces           │  1. e2-e4  (Yes)         │
│                                  │     e7-e5  (Yes)         │
│     ◄ ►  move-by-move controls   │  2. d2-d4  (Yes)         │
│                                  │     e5xd4  Capture d4    │
│  ─── Perspective ─────────────── │  3. ...                  │
│  (○) Referee  (○) White  (○) Black                         │
│                                  │  Result: White wins by   │
│                                  │  checkmate (move 45)     │
└──────────────────────────────────┴────────────────────────┘
```

- Three view modes: Referee (full board), White's view, Black's view
- Step through moves with arrow keys or buttons
- Each move shows the announcement and board state at that point
- Click any move in the log to jump to that position

### User Profile (`/user/{username}`)

```
┌─────────────────────────────────────────┐
│  alexfil                                │
│  Member since Jan 2025                  │
│                                         │
│  Games: 47  W: 22  L: 20  D: 5         │
│  ELO: 1200 (peak: 1350)                │
│  Win rate: 47%                          │
│                                         │
│  ─── Recent Games ───────────────────   │
│  vs opponent1  │ W │ checkmate  │ 3/13  │
│  vs player2    │ L │ resign     │ 3/12  │
│  vs player3    │ D │ stalemate  │ 3/11  │
│  [ View all games → ]                   │
└─────────────────────────────────────────┘
```

## WebSocket Client (game.js)

The primary JavaScript in the project. Approximately **270 lines** (including PhantomManager).

```javascript
/**
 * game.js — WebSocket client for Kriegspiel gameplay.
 *
 * Handles:
 * 1. WebSocket connection lifecycle (connect, reconnect, disconnect)
 * 2. Translating board drag-and-drop into UCI moves
 * 3. Sending moves/actions to the server
 * 4. Receiving and rendering referee announcements
 * 5. Updating the board from server-provided FEN
 */

class KriegspielClient {
    constructor(gameId, sessionToken, playerColor) {
        this.gameId = gameId;
        this.token = sessionToken;
        this.color = playerColor;
        this.ws = null;
        this.board = null;       // chessboard.js instance
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
    }

    connect() {
        const url = `wss://${window.location.host}/ws/game/${this.gameId}?token=${this.token}`;
        this.ws = new WebSocket(url);

        this.ws.onopen = () => {
            this.reconnectAttempts = 0;
            this.updateConnectionStatus(true);
        };

        this.ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            this.handleMessage(msg);
        };

        this.ws.onclose = () => {
            this.updateConnectionStatus(false);
            this.scheduleReconnect();
        };
    }

    handleMessage(msg) {
        switch (msg.type) {
            case "connected":
                this.initBoard(msg);
                break;
            case "move_result":
                this.handleMoveResult(msg);
                break;
            case "opponent_moved":
                this.handleOpponentMoved(msg);
                break;
            case "any_result":
                this.handleAnyResult(msg);
                break;
            case "opponent_asked_any":
                this.appendReferee(`Opponent asked "Any?" — ${msg.result}`);
                break;
            case "game_over":
                this.handleGameOver(msg);
                break;
            case "opponent_status":
                this.updateOpponentStatus(msg);
                break;
            case "error":
                this.showError(msg.message);
                break;
        }
    }

    sendMove(source, target, piece) {
        // Convert chessboard.js square names to UCI
        const uci = source + target;
        // Handle pawn promotion (always promote to queen for now)
        const isPromotion = piece === "wP" && target[1] === "8"
                         || piece === "bP" && target[1] === "1";
        this.ws.send(JSON.stringify({
            action: "move",
            uci: isPromotion ? uci + "q" : uci
        }));
    }

    sendAskAny() {
        this.ws.send(JSON.stringify({ action: "ask_any" }));
    }

    sendResign() {
        this.ws.send(JSON.stringify({ action: "resign" }));
    }

    // ... board rendering, referee log, reconnection logic

    initBoard(msg) {
        // Configure chessboard.js
        this.board = Chessboard('board', {
            position: msg.your_fen,
            orientation: this.color,
            draggable: true,
            onDrop: (source, target, piece) => this.sendMove(source, target, piece),
            pieceTheme: '/static/img/pieces/{piece}.svg'
        });

        // Initialize phantom pieces for opponent tracking
        const opponentColor = this.color === 'white' ? 'b' : 'w';
        this.phantoms = new PhantomManager(this.gameId, opponentColor);
        this.phantoms.render(document.getElementById('board'));
    }
}

// PhantomManager class defined in the Phantom Pieces section above
```

### game.js Line Budget

| Concern | Lines |
|---|---|
| WebSocket lifecycle (connect, close, reconnect) | ~40 |
| Message handling (handleMessage, all cases) | ~60 |
| Board interaction (chessboard.js callbacks, promotion) | ~40 |
| Referee panel rendering | ~30 |
| PhantomManager class | ~80 |
| Reconnection logic (exponential backoff) | ~20 |
| **Total** | **~270** |

## Post-Game Replay (review.js)

The game review page (`/game/{game_id}/review`) uses a separate JavaScript file. Approximately **120 lines**.

```javascript
class GameReview {
    constructor(gameId) {
        this.gameId = gameId;
        this.moves = [];           // Loaded from API
        this.currentPly = 0;
        this.perspective = 'referee';  // "referee" | "white" | "black"
        this.board = null;
    }

    async load() {
        // Fetch full move transcript
        const resp = await fetch(`/api/game/${this.gameId}/moves`);
        const data = await resp.json();
        this.moves = data.moves;
        this.initBoard();
        this.bindControls();
    }

    initBoard() {
        this.board = Chessboard('review-board', {
            position: 'start',
            draggable: false,
            pieceTheme: '/static/img/pieces/{piece}.svg'
        });
    }

    bindControls() {
        // Arrow keys: Left = previous, Right = next
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'ArrowRight') this.next();
        });

        // Step buttons
        document.getElementById('btn-prev')?.addEventListener('click', () => this.prev());
        document.getElementById('btn-next')?.addEventListener('click', () => this.next());

        // Perspective radio buttons
        document.querySelectorAll('input[name="perspective"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.perspective = e.target.value;
                this.renderAtCurrentPly();
            });
        });

        // Click move in log to jump
        document.querySelectorAll('.move-entry').forEach((el, idx) => {
            el.addEventListener('click', () => this.goTo(idx));
        });
    }

    next() {
        if (this.currentPly < this.moves.length) {
            this.currentPly++;
            this.renderAtCurrentPly();
        }
    }

    prev() {
        if (this.currentPly > 0) {
            this.currentPly--;
            this.renderAtCurrentPly();
        }
    }

    goTo(ply) {
        this.currentPly = ply;
        this.renderAtCurrentPly();
    }

    renderAtCurrentPly() {
        // Rebuild board state by replaying moves up to currentPly
        // Use perspective to filter: "referee" = full FEN,
        // "white"/"black" = filter opponent pieces from FEN client-side
        // Highlight current move in the move log
    }
}
```

## Responsive Design

- **Desktop** (> 768px): Board + referee side by side (2-column)
- **Mobile** (< 768px): Board stacked above referee panel; board scales to viewport width
- Touch support via chessboard.js built-in touch handling

## Sound Effects (Optional)

- Move executed: soft click
- Capture: impact sound
- Check: alert chime
- Illegal move: error buzz
- Game over: fanfare / defeat sound

Sounds are opt-in via user settings. Loaded as small MP3 files (< 50 KB total).

## Accessibility

- Semantic HTML (`<nav>`, `<main>`, `<article>`, `<aside>`)
- ARIA labels on interactive elements
- Keyboard navigation for board (arrow keys in review mode)
- High-contrast text (WCAG AA)
- Referee log is a `<div role="log" aria-live="polite">` for screen readers
