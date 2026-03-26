# Slice 750 - Implementation Plan
- Configure structlog in app bootstrap (JSON in prod, console in dev).
- Instrument auth events (register/login success/failure + source IP).
- Instrument game lifecycle and move-submit events with safe metadata (`game_id`, `user_id`, side).
- Ensure no passwords/session IDs/tokens are emitted.
