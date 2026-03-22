# Step 530 - Phantom Tray and Client Persistence

## Goal

Implement client-only phantom placement/removal/persistence per game.

## Objective and Scope

- In scope: `PhantomTray`, `usePhantoms` hook, placement/move/remove/displace/clear operations.
- In scope: localStorage key `phantoms_{gameId}` with restore on load.
- Out of scope: any backend persistence or network payload changes.

## Dependencies and Order

- Depends on 510 + 520.
- Blocks 540.

## Acceptance Criteria

- Full opponent tray initializes when absent.
- Transitions preserve tray+board piece counts.
- Reload restores phantom placement for game id.
- Phantom state never sent over API requests.
