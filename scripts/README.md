# Scripts

Operational and utility scripts for the Kriegspiel platform.

## Expected Scripts

| Script | Purpose | Reference |
|---|---|---|
| `backup.sh` | Daily MongoDB backup via `mongodump` (run via cron) | [INFRA.md](../INFRA.md) |
| `setup-vps.sh` | Initial VPS provisioning (UFW, Docker, certbot) | [INFRA.md](../INFRA.md) |
| `deploy.sh` | Manual deploy script (pull, build, restart) | [INFRA.md](../INFRA.md) |
| `seed-db.py` | Seed MongoDB with test data (dev only) | [DATA_MODEL.md](../DATA_MODEL.md) |
| `generate-secret.py` | Generate a random SECRET_KEY for `.env` | [AUTH.md](../AUTH.md) |

## Notes

- All Bash scripts should use `#!/usr/bin/env bash` and `set -euo pipefail`.
- Python scripts should use the same Python 3.12+ as the main app.
- Scripts that interact with Docker should assume they run on the VPS host (not inside a container).
