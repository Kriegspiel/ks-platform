# Slice 740 - Implementation Plan
- `backup.sh`: timestamped compressed dump + 30-day retention.
- `restore.sh`: path validation + explicit confirmation/`--force` mode.
- `health-check.sh`: service status + API health + disk threshold check.
- All scripts: `set -euo pipefail`, usage docs, meaningful exit codes.
