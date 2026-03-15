# Step 500 - Game UI

## Goal

Build the React game page with chess board, referee log, polling client, phantom pieces, and promotion modal.

## Read First

- [FRONTEND.md](../../FRONTEND.md) — phantom pieces spec, game page layout (adapt for React, not Jinja2)
- [API_SPEC.md](../../API_SPEC.md) — game state response shape
- [development-plan/PLAN.md](../PLAN.md) — React + click-based board + component CSS

## Depends On

- `step-400`

## UI Approach

Follows ks-v2 patterns: custom React board component with click-to-select-square interaction and Unicode chess pieces. No chessboard.js, no drag-and-drop. Component-level CSS files.

## Task Slices

### 510 — Chess Board Component

**Create these files:**

- `frontend/src/components/ChessBoard.jsx` — board rendering component (based on ks-v2 pattern, enhanced):
  - Props: `fen`, `orientation` ("white"/"black"), `onSquareClick(square)`, `highlightedSquares[]`, `phantomPieces` (Map of square→piece for overlay), `disabled` (bool)
  - Renders 8x8 grid with file/rank labels
  - Parses FEN to place pieces
  - Color-coded squares (light/dark)
  - Unicode chess piece symbols (♔♕♖♗♘♙ for white, ♚♛♜♝♞♟ for black)
  - Piece color styling (white pieces vs black pieces)
  - Square highlighting for selected squares
  - Board orientation flips based on player color
  - Phantom pieces rendered at 50% opacity with dashed outline
  - `disabled` prop prevents clicks during opponent's turn
- `frontend/src/components/ChessBoard.css` — board styles:
  - Grid layout, square colors, piece sizing
  - Highlighted square styling
  - Phantom piece styling (opacity: 0.5, dashed border)
  - Responsive sizing (board scales to fit viewport)

**Acceptance criteria:**
- Board renders from FEN string correctly
- Clicking a square calls `onSquareClick` with square name (e.g., "e2")
- Board flips when orientation is "black"
- Highlighted squares are visually distinct
- Phantom pieces render at 50% opacity
- Board is responsive

---

### 520 — Game Page with Polling

**Create these files:**

- `frontend/src/pages/Game.jsx` — main game page:
  - Two-column layout: board (left) + referee panel (right)
  - **Board panel**: ChessBoard component with player's FEN
  - **Move interaction**: click source square → click target square → send move. Show selected from/to squares as highlighted.
  - **Referee log**: scrollable list of announcements from `referee_log` in polled state
  - **Action buttons**: "Ask Any?" (visible when `possible_actions` includes "ask_any"), "Resign" (with confirm dialog)
  - **Clock display**: white remaining / black remaining, active player indicated
  - **Turn indicator**: whose turn it is
  - **Opponent info**: opponent username
  - **Game over overlay**: when `is_game_over`, show result + link to review
  - **Polling**: `useEffect` with `setInterval` every 2 seconds, calls `GET /api/game/{gameId}/state?player={color}`, updates board + referee log + clock + turn
  - **Move submission**: `POST /api/game/{gameId}/move` with UCI string, then re-poll
- `frontend/src/pages/Game.css` — game page styles:
  - Two-column layout (board left, panel right)
  - Stacked on mobile (<768px)
  - Referee log scrollable panel
  - Clock styling
  - Game over overlay
- `frontend/src/services/api.js` — add:
  - `gameApi.getState(gameId, player)` — polls game state
  - `gameApi.makeMove(gameId, uci)` — submit move
  - `gameApi.askAny(gameId)` — ask any question
- `frontend/src/App.jsx` — add `/game/:gameId` route with auth guard

**Acceptance criteria:**
- Game page renders board with player's pieces only
- Clicking two squares sends a move
- Referee log updates on each poll
- Clock ticks down (based on polled data)
- Ask Any button works when available
- Resign with confirmation works
- Game over shows result
- Polling stops when game is completed

---

### 530 — Phantom Pieces

**Create these files:**

- `frontend/src/components/PhantomTray.jsx` — tray of unplaced opponent pieces:
  - Shows 16 opponent pieces (1K, 1Q, 2R, 2B, 2N, 8P) not yet placed on board
  - Click a tray piece to select it, then click a board square to place it
  - Pieces in tray shown at 50% opacity
- `frontend/src/components/PhantomTray.css` — tray styling
- `frontend/src/hooks/usePhantoms.js` — custom hook for phantom state:
  - `placed`: Map of square → piece (e.g., "d8" → "bQ")
  - `tray`: array of unplaced pieces
  - `place(piece, square)` — move from tray to board
  - `move(fromSquare, toSquare)` — move phantom on board
  - `remove(square)` — return phantom to tray (triggered by right-click)
  - `displace(square)` — called when real piece moves to phantom square, returns phantom to tray
  - `clear()` — clear all phantoms (on game end)
  - Persists to `localStorage` keyed by game ID: `phantoms_{gameId}`
  - Loads from localStorage on mount
  - Initializes full tray on first load
- `frontend/src/pages/Game.jsx` — integrate phantoms:
  - Pass `phantomPieces` to ChessBoard for rendering
  - Show PhantomTray below the board
  - Right-click on phantom square removes it
  - When polling returns updated state and a capture was announced, don't auto-remove phantom (let player decide)

**Acceptance criteria:**
- Phantom tray shows 16 opponent pieces
- Clicking tray piece then board square places phantom
- Phantoms render at 50% opacity with dashed outline
- Right-click removes phantom back to tray
- Phantoms persist across page reloads (localStorage)
- Real piece displaces phantom on same square
- Phantoms are never sent to the server

---

### 540 — Promotion Modal and Interaction Polish

**Create these files:**

- `frontend/src/components/PromotionModal.jsx` — promotion chooser:
  - Appears when a pawn reaches the last rank (rank 8 for white, rank 1 for black)
  - Shows 4 piece options: Queen, Rook, Bishop, Knight (Unicode symbols)
  - Clicking a piece completes the move with UCI suffix (e.g., "e7e8q")
  - Clicking outside cancels (pawn returns to source)
- `frontend/src/components/PromotionModal.css` — centered overlay styling
- `frontend/src/pages/Game.jsx` — integrate promotion:
  - Detect pawn promotion before sending move
  - Show modal, wait for selection, then send move with suffix
- Polish:
  - Last move highlighting (source and target squares of the last move, own moves only)
  - Illegal move feedback: show "Illegal move" briefly in referee log when `move_done: false`
  - Turn indicator visual emphasis (bold/colored when it's your turn)
  - Empty state: "Waiting for opponent to move" message
  - Loading state during move submission

**Acceptance criteria:**
- Promotion modal appears for pawn reaching last rank
- Selecting a piece sends correct UCI (e.g., "e7e8q")
- Canceling returns pawn to source square
- Last move squares are highlighted
- Illegal move shows feedback
- Turn indicator clearly shows whose turn it is

---

### 550 — Home Page and Navigation Polish

**Create these files:**

- `frontend/src/pages/Home.jsx` — landing page:
  - Welcome message explaining Kriegspiel
  - "Play Now" button → /lobby (or /auth/login if not logged in)
  - "Learn the Rules" link → /rules
  - Recent completed games list (poll `/api/game/recent`)
- `frontend/src/pages/Home.css` — home page styling
- `frontend/src/pages/Rules.jsx` — static rules page:
  - Kriegspiel rules explanation (Berkeley variant)
  - What the referee announces
  - How phantom pieces work
- `frontend/src/pages/Rules.css` — rules page styling
- `frontend/src/components/Nav.jsx` — finalize nav:
  - Links: Home, Lobby (if logged in), Leaderboard
  - Active game indicator: if user has an active game where it's their turn, show notification dot
- Update `frontend/src/App.jsx` — add `/` and `/rules` routes

**Acceptance criteria:**
- Home page shows welcome + Play Now CTA
- Recent games display on home page
- Rules page explains the game clearly
- Nav links work and highlight active route
- Play Now redirects correctly based on auth state

---

## Exit Criteria

- The game page is playable end-to-end by a human player
- Board shows only the player's pieces
- Phantom pieces work and persist client-side
- Promotion modal works
- Referee log shows game events
- Clock displays correctly

## Out of Scope

- Profile/history/leaderboard (step 600)
- Deployment (step 700)
- Sound effects (nice-to-have, not MVP)
