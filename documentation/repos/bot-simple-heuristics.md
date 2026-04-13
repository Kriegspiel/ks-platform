# bot-simple-heuristics

`bot-simple-heuristics` is the lightweight heuristic bot between the random bots and the model bots.

It is useful as:

- a stronger non-model baseline
- a reference bot with explicit tactical rules
- a moderate-load bot that still stays cheap to run

## Runtime role

- systemd unit: `kriegspiel-simple-heuristics-bot.service`
- single Python process
- serial poll loop
- current production host uses a user-level systemd service

## Main file

### `bot.py`

This repo is intentionally centered on one runtime script.

Important function groups:

- env and token restore:
  - `load_env_file`
  - `load_state`
  - `save_state`
  - `save_token`
  - `maybe_restore_token`
- registration/auth:
  - `register_bot`
  - `auth_headers`
  - `bot_username`
- lobby policy:
  - `open_bot_lobby_candidates`
  - `has_own_waiting_game`
  - `can_attempt_bot_join`
  - `record_bot_join_attempt`
  - `choose_bot_game_to_join`
  - `maybe_join_bot_lobby_game`
  - `maybe_create_lobby_game`
- gameplay heuristics:
  - capture parsing / last-capture detection
  - recapture selection
  - promotion preference
  - weighted piece selection
  - move ordering by distance
  - `maybe_play_game`
  - `run_loop`

## Behavior

- if the opponent just captured, it first tries to recapture on that square
- if promotion is available, it prefers queen promotion
- otherwise it selects one action source using geometric weights:
  - `ask-any` gets `50%` when available
  - else the remaining weight starts from the piece with the longest available move
  - next pieces receive halving weights
- once a piece is chosen, it tries that piece's moves from longest to shortest
- if all moves for that piece fail, it chooses again from the remaining pieces

## Operational policy

- auto-creates a human-joinable waiting game when it can
- allows up to `5` active games
- samples bot-vs-bot joins at most once per minute
- bot-vs-bot join probability is `10%`

## Practical difference from other bots

- stronger than the random bots because it reacts to captures and promotions
- much cheaper than the model bots because it does not call an external LLM
- higher allowed concurrency than the model bots

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
