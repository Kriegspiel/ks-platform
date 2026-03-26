# Slice 740 - Testing (Automated + Gates)
## Exact Commands
```bash
chmod +x scripts/backup.sh scripts/restore.sh scripts/health-check.sh
shellcheck scripts/backup.sh scripts/restore.sh scripts/health-check.sh
./scripts/backup.sh --help
./scripts/restore.sh --help
./scripts/backup.sh
LATEST_BACKUP=$(find backups -type f | sort | tail -n 1)
./scripts/restore.sh "$LATEST_BACKUP" --force
./scripts/health-check.sh
```
## Thresholds / Coverage Gates
- shellcheck zero errors.
- backup artifact exists and >0 bytes.
- restore completes with latest artifact.
- health script exits 0 in healthy environment.
## CI Merge Gates
- shell lint + script smoke jobs required.
## Deterministic Fixtures/Seeding
- fixed backup name prefix/UTC format; restore against seeded dataset snapshot.
## Regression Matrix
- executability bits set; usage output present; backup ok; retention pruning works; invalid restore path fails safely; health report complete.
## Skip Policy + Prereqs
- Skip restore only if no Mongo runtime; still validate argument and failure paths.
## Post-Deploy Smoke + Rollback
```bash
./scripts/health-check.sh && ./scripts/backup.sh
# rollback
git checkout -- scripts/backup.sh scripts/restore.sh scripts/health-check.sh
```
