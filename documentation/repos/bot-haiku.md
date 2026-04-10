# bot-haiku

`bot-haiku` is the Anthropic-driven conversational model bot.

It mirrors the overall shape of `bot-gpt-nano`, but targets the Anthropic Messages API.

## Runtime role

- systemd unit: `kriegspiel-haiku-bot.service`
- single Python process
- serial poll loop
- per-game conversation state

## Main file

### `bot.py`

Important function groups:

- env and token restore
- lobby policy
- rules-text and scoresheet digestion
- prompt construction
- Anthropic request/response handling
- ranked-action parsing
- gameplay loop

Key functions:

- `load_rules_text`
- `build_system_prompt`
- `build_initial_user_prompt`
- `build_followup_user_prompt`
- `call_anthropic_messages`
- `conversation_messages`
- `persistable_conversation_messages`
- `normalize_ranked_decisions`
- `choose_ranked_actions`
- `maybe_play_game`
- `run_loop`

## Current prompting design

Like `gptnano`, it uses:

- stable system prompt
- incremental follow-up prompts
- ordered top-N move batches
- compact state representation

## Operational policy

- no self-created waiting games by default
- join sampling only once per minute
- very low bot-vs-bot join probability
- intentionally low concurrency

## Practical difference from `bot-gpt-nano`

- Anthropic API integration instead of OpenAI
- Anthropic-specific cache and output-token settings
- otherwise the same overall control flow and orchestration philosophy

For the exhaustive file list, use [`../module-index.md`](../module-index.md).
