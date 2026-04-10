# bot-random-any

`bot-random-any` is a slightly smarter random bot that asks `any pawn captures?` before choosing random moves.

It is useful as:

- a Berkeley + Any example bot
- a simple stronger baseline than pure random

## Runtime role

- systemd unit: `kriegspiel-random-any-bot.service`
- single Python process
- serial poll loop

## Main file

### `bot.py`

Like `bot-random`, this repo is mostly one runtime script.

Important function groups:

- env and state handling
- registration/auth
- API wrappers
- lobby join/create policy
- gameplay loop

Key gameplay functions:

- `choose_random_moves`
- `maybe_play_game`

The main difference from `bot-random` is that it uses the `ask any` path before random move selection where appropriate.

## Behavior

- favors the `Any` rule flow when the variant supports it
- samples bot-vs-bot joins at most once per minute
- handles games sequentially in one process

## Operational notes

- useful for generating lots of Berkeley + Any games
- still intentionally simple enough to serve as a public example repo

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
