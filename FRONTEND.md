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
| Styling | **Pico CSS** or **Simple.css** | Classless CSS framework — clean defaults, minimal markup |
| Icons | **Lucide** | Lightweight icon set |
| WebSocket | **Native browser API** | Game communication |

Total JS payload: < 100 KB gzipped.

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
- Recent games list: HTMX partial, auto-refreshes every 30s

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

- "Open Games" list uses `hx-get="/api/game/open" hx-trigger="every 5s"` for live updates
- "My Active Games" shows games where user is a participant and state is "active" or "paused"

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

The only significant JavaScript in the project. Approximately 150-200 lines.

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
