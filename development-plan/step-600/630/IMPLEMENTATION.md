# Slice 630 - Implementation Plan

## Files

- `frontend/src/pages/Profile.jsx` + `.css`
- `frontend/src/pages/GameHistory.jsx` + `.css`
- `frontend/src/pages/Leaderboard.jsx` + `.css`
- `frontend/src/pages/Settings.jsx` + `.css`
- `frontend/src/services/api.js`
- `frontend/src/App.jsx`

## Required Behaviors

- Profile page shows stats and links to last 5 reviewable games
- Game history table paginates and links to review route
- Leaderboard paginates and links username to profile
- Settings form supports load/edit/save with success/error feedback
- Routes: `/user/:username`, `/user/:username/games`, `/leaderboard`, `/settings`

## UX Constraints

- Must remain usable on narrow/mobile width
- Empty states and API error states must render informative text
