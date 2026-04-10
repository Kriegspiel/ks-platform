# ks-web-app

`ks-web-app` is the authenticated React frontend at `app.kriegspiel.org`.

It owns:

- auth pages
- lobby
- active game UI
- completed-game review UI
- profile pages
- live leaderboard
- settings
- technical reports such as `/tech/bots-report`

## Runtime role

- public host: `app.kriegspiel.org`
- framework: React + Vite
- API pattern: same-origin relative `/api/...`

## Main layout

### `frontend/src/App.jsx`

Top-level route composition.

Current route map includes:

- `/`
- `/auth/login`
- `/auth/register`
- `/lobby`
- `/join/:gameCode`
- `/game/:gameCode`
- `/game/:gameCode/review`
- `/user/:username`
- `/user/:username/games`
- `/leaderboard`
- `/tech/bots-report`
- `/settings`

### `frontend/src/services/api.js`

Central browser API client.

Responsibilities:

- Axios instance
- auth error normalization
- game APIs
- user APIs
- tech report APIs

Important rule:

- base URL stays empty so browser traffic uses same-origin `/api/...`

### `frontend/src/pages/`

Main page-level route components.

Important pages:

- `HomePage.jsx`
- `LobbyPage.jsx`
- `GamePage.jsx`
- `Review.jsx`
- `Profile.jsx`
- `GameHistory.jsx`
- `Leaderboard.jsx`
- `BotsReport.jsx`
- `SettingsPage.jsx`
- auth pages

### `frontend/src/components/`

Shared UI pieces.

Important components include:

- board rendering
- Elo chart
- navigation/header
- reusable stat cards

### `frontend/src/context/`

Cross-page state such as auth and theme.

## Important behaviors

### Active game UI

`GamePage.jsx` is responsible for:

- loading game metadata and active state
- move submission
- `ask any pawn captures?`
- phantom-piece board interactions
- referee log rendering
- status card and game code display

Important rule:

- this page must never gain access to opponent hidden pieces during active play

### Review UI

`Review.jsx` handles:

- referee / white / black perspective toggle
- ply-based move log
- grouped white/black ply rows
- board overlays for illegal attempts, completed moves, and captures
- review metadata and stats

Important review semantics already implemented:

- navigation moves by ply, not raw attempts
- white/black views hide the opponent’s attempt arrows
- capture highlights remain visible in both private views

### Profile and stats

`Profile.jsx` and `HomePage.jsx` display:

- exact backend-owned track stats
- aggregated rating-history charts
- three rating tracks:
  - overall
  - vs humans
  - vs bots

The frontend should render backend summaries, not recompute lifetime stats from history slices.

### Bots report

`BotsReport.jsx` renders:

- one table per listed bot
- last 10 days
- grouped columns:
  - overall
  - vs humans
  - vs bots
- subcolumns:
  - total games
  - win rate

## Styling conventions already in use

- light/dark mode is theme-aware
- user-visible version footer appears across app pages
- header controls should stay flat without hover shadows
- replay selected ply uses warm app accent styling rather than bright blue

## Testing

Vitest tests in `frontend/src/__tests__/` cover:

- route-level page behavior
- review and board UX
- API wrappers
- leaderboard
- bots report

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
