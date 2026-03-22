# Step 520 - Game Page Polling Loop and Gameplay Actions

## Goal

Implement `/game/:gameId` orchestration against Step 400 APIs.

## Objective and Scope

- In scope: `Game.jsx` layout, 2s polling loop, move/ask-any/resign handlers, turn/clock/referee rendering.
- In scope: API helper methods + route wiring in `App.jsx`.
- Out of scope: phantom persistence internals and promotion modal.

## Dependencies and Order

- Depends on 510.
- Blocks 530/540/550.

## Acceptance Criteria

- Poll loop updates board/referee/clock.
- Two-click move submit posts UCI and re-polls.
- Ask-any/resign controls honor `possible_actions`.
- Poll timer clears on unmount and game completion.
