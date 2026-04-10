# bot-random

`bot-random` is the baseline random-move bot.

It is intentionally simple and useful as:

- a sanity-check bot
- a load-generating bot
- an implementation example for external bot authors

## Runtime role

- systemd unit: `kriegspiel-random-bot.service`
- single Python process
- serial poll loop

## Main file

### `bot.py`

This repo is intentionally centered on one runtime script.

Important function groups:

- env and state:
  - `load_env_file`
  - `load_state`
  - `save_state`
  - `save_token`
  - `maybe_restore_token`
- registration/auth:
  - `register_bot`
  - `auth_headers`
  - `bot_username`
- API helpers:
  - `get_json`
  - `post_json`
  - `get_public_user`
- lobby policy:
  - `open_bot_lobby_candidates`
  - `has_own_waiting_game`
  - `can_attempt_bot_join`
  - `record_bot_join_attempt`
  - `choose_bot_game_to_join`
  - `maybe_join_bot_lobby_game`
  - `maybe_create_lobby_game`
- gameplay:
  - `choose_random_moves`
  - `maybe_play_game`
  - `run_loop`

## Behavior

- chooses random legal moves from the allowed move list
- can participate in bot-vs-bot games
- samples lobby bot joins at most once per minute
- now records the join attempt before the probability roll, so a miss still consumes the cooldown

## Operational notes

- one process, no worker pool
- multiple active games are handled sequentially, not truly in parallel
- first-move latency can grow if the bot has many active games

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
