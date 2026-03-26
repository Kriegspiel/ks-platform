# Slice 730 - Implementation Plan
- Trigger workflow on push/PR to `main`.
- Backend job: Python 3.12 + Mongo service + black/ruff + pytest with coverage gate.
- Frontend job: Node 20 + npm ci + lint + build.
- Deploy job: depends on backend+frontend and runs only on push to main.
