# bot-gpt-nano

`bot-gpt-nano` is the OpenAI-driven conversational model bot.

It is the main reference implementation for a model-based Kriegspiel bot on the OpenAI stack.

## Runtime role

- systemd unit: `kriegspiel-gpt-nano-bot.service`
- single Python process
- serial poll loop
- per-game conversation state in local files/state

## Main file

### `bot.py`

Important function groups:

- env/state/token restore
- lobby policy
- rules-text loading
- scoresheet digestion and recent-item extraction
- prompt construction
- OpenAI calling
- ranked-action parsing
- gameplay loop

Key functions:

- `load_rules_text`
- `build_system_prompt`
- `build_initial_user_prompt`
- `build_followup_user_prompt`
- `call_openai`
- `normalize_ranked_decisions`
- `choose_ranked_actions`
- `maybe_play_game`
- `run_loop`

## Current prompting design

- stable system prompt
- compact initial user prompt with state, scoresheet, and possible moves
- follow-up prompts carry only new referee items, rejected candidates, and refreshed move options
- model returns ordered best-to-worst candidate batches

This was shaped specifically to be:

- more cache-friendly
- easier to continue turn by turn
- more conversational without resending the whole history every call

## Operational policy

- no self-created waiting games by default
- bot-vs-bot join sampling only once per minute
- very low join probability
- voluntary active-game cap is intentionally tiny

Why:

- model calls are slower than random bots
- per-game context is heavier
- serial handling makes long model calls block other games

## Important caveat

Concurrency is still one process, one loop.
The difference from random bots is context and latency, not multiprocessing.

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
