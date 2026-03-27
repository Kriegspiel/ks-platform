# Slice 960 - Implementation Plan

## Files / Areas

- `Kriegspiel/content` directory structure docs and enforcement scripts
- `CODEOWNERS` and contributor workflow docs
- Content lifecycle metadata validators
- CI workflow definitions for repository-policy checks

## Tasks

1. Define canonical repository structure (e.g., `blog/`, `changelog/`, `rules/`, `authors/`, `assets/`, `schemas/`).
2. Define slug/filename policy and path conventions for each content type.
3. Add lifecycle metadata policy (`draft`, `reviewStatus`, `publishedAt`, `archivedAt`) and schema enforcement.
4. Configure CODEOWNERS/reviewer routing by content area.
5. Add policy-check script that fails on invalid structure, missing ownership, or lifecycle conflicts.
6. Integrate policy checks into content and website CI paths that consume content artifacts.
7. Document contributor workflow for proposing, previewing, publishing, and archiving content.

## Acceptance Criteria

- Repository structure and naming policy are documented and machine-validated.
- Ownership policy is enforceable and wired to review routing.
- Lifecycle metadata policy is enforced with automated checks.
- CI blocks merges on organization-policy violations.
- Documentation enables new contributors to follow workflow without tribal knowledge.
