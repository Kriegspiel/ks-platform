# Documentation

This folder is the human-facing documentation layer for the active Kriegspiel.org repos.

## Files

- [`data-structures.md`](./data-structures.md)
  - shared models, payloads, identifiers, and persisted shapes
- [`runtime-flows.md`](./runtime-flows.md)
  - auth flow, game flow, replay flow, bot flow, static-site flow
- [`module-index.md`](./module-index.md)
  - exhaustive generated snapshot of modules/files across the active repos
- [`repos/`](./repos)
  - one repo note per active repo

## Repo notes

- [`repos/ks-backend.md`](./repos/ks-backend.md)
- [`repos/ks-web-app.md`](./repos/ks-web-app.md)
- [`repos/ks-home.md`](./repos/ks-home.md)
- [`repos/content.md`](./repos/content.md)
- [`repos/ks-game.md`](./repos/ks-game.md)
- [`repos/bot-random.md`](./repos/bot-random.md)
- [`repos/bot-random-any.md`](./repos/bot-random-any.md)
- [`repos/bot-gpt-nano.md`](./repos/bot-gpt-nano.md)
- [`repos/bot-haiku.md`](./repos/bot-haiku.md)
- [`repos/ks-platform.md`](./repos/ks-platform.md)

## How to keep it current

When repo layout or public behavior changes:

1. update the affected repo note(s)
2. update shared docs if a contract changed
3. regenerate [`module-index.md`](./module-index.md)

Command:

```bash
python scripts/generate_inventory.py
```
