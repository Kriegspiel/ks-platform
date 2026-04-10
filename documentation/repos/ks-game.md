# ks-game

`ks-game` is the Python engine library that implements the Berkeley-style Kriegspiel referee.

It is the game-rules core used by `ks-backend`.

## Runtime role

- no public HTTP surface by itself
- imported by `ks-backend`
- acts as the authoritative hidden-information referee

## Main modules

### `kriegspiel/berkeley.py`

Contains `BerkeleyGame`.

Responsibilities:

- own the hidden full board
- accept move questions and `ask any` questions
- validate/referee them
- mutate the underlying chess board
- produce `KriegspielAnswer` objects
- maintain white and black scoresheets

### `kriegspiel/move.py`

Defines the core move/answer types:

- `QuestionAnnouncement`
- `KriegspielMove`
- `MainAnnouncement`
- `SpecialCaseAnnouncement`
- `KriegspielAnswer`
- `KriegspielScoresheet`

These are the most important shared engine-side structures for the backend.

### `kriegspiel/serialization.py`

Serialization helpers used by the backend engine adapter.

Responsibilities:

- save/load game state
- translate engine objects into persisted form

## Important engine behavior

- supports Berkeley with or without the `Any` rule
- understands illegal move attempts from the player’s perspective
- distinguishes:
  - impossible-to-ask
  - illegal-but-informative
  - regular move
  - capture
  - `ask any`
- emits special announcements for check, mate, and draw conditions

## How the backend uses it

The backend does not expose raw engine objects directly.

Instead it:

1. stores serialized engine state
2. uses `engine_adapter.py` to call into `ks-game`
3. uses `state_projection.py` to build player-visible payloads

This separation is important:

- `ks-game` owns referee truth
- `ks-backend` owns persistence and API projection

## Tests and scope

`ks-game` is a library repo, not a deployment/orchestration repo.

Changes here usually require:

- engine-level tests in `ks-game`
- backend integration verification in `ks-backend`

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
