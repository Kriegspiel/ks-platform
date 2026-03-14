# Documentation

Additional implementation details, research notes, and architectural decision records.

## Contents

| Path | Purpose |
|---|---|
| `adr/` | Architecture Decision Records — document significant design choices with context and rationale |

## Adding Documents

Agents implementing features should add detailed notes here when a spec document in the root doesn't cover enough detail. Use Markdown. Name files descriptively (e.g., `websocket-reconnection-strategy.md`, `elo-calculation-research.md`).

## ADR Format

Architecture Decision Records in `adr/` should follow this template:

```markdown
# ADR-NNN: Title

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Date:** YYYY-MM-DD

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?
```
