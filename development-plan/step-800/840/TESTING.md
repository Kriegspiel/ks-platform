# Slice 840 - Testing (Automated + Gates)

## Exact Commands

```bash
set -euo pipefail
cd /home/fil/dev/kriegspiel/ks-platform

# Markdown/link quality checks (tool choice depends on repo)
markdownlint "**/*.md"
lychee --no-progress "**/*.md"

# Fresh-clone style command verification (sampled)
cp .env.example .env

docker compose config -q

docker compose up -d mongo app frontend nginx
curl -fsS http://localhost/api/health
curl -fsS http://localhost/ >/dev/null

docker compose down -v
```

## Thresholds / Coverage Gates

- Markdown lint: 0 blocking errors.
- Link check: 0 broken internal links, 0 broken required external docs links.
- Quickstart validation: stack reaches healthy state within **120s**.
- Command samples in README/runbook must execute without undocumented prerequisites.

## CI Merge Gates

Required checks:

- `docs-lint`
- `docs-link-check`
- `docs-quickstart-verify`

Any failure blocks merge when docs or ops files are changed.

## Deterministic Fixtures / Seeding

- Use `.env.example` baseline and documented defaults.
- Run doc command verification in clean workspace/CI container.
- Pin doc examples to actual scripts/paths in repo (no placeholder commands).

## Regression Matrix

- README quickstart path valid
- Local dev backend/frontend commands valid
- Test command documentation valid
- Deployment runbook path valid
- Backup/restore/health script references valid
- Architecture divergence notes present and accurate

## Skip Policy + Prereqs

- Prereqs: markdownlint/lychee available (install step documented).
- Skip only for transient external link failures; rerun required and must record URL + timestamp.
- Internal-link and command-validation checks are non-skippable.

## Post-Deploy Smoke + Rollback

```bash
# smoke
curl -fsS http://localhost/api/health
curl -fsS http://localhost/ >/dev/null

# rollback docs change if operator confusion/regression is discovered
git revert --no-edit HEAD
```
