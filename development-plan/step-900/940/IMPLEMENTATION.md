# Slice 940 - Implementation Plan

## Files / Areas

- Rules page template and rules data source
- SEO metadata helpers and route-level tag definitions
- Analytics/event instrumentation wrappers
- Legal page templates and policy docs

## Tasks

1. Build rules page from versioned source with `lastUpdated`, semantic sections, and revision ID.
2. Link rules revisions to changelog entries where policy/gameplay changes are introduced.
3. Implement per-route metadata: title/description/canonical/OG/Twitter tags.
4. Add JSON-LD structured data for website/organization/article routes where applicable.
5. Define analytics event dictionary and privacy boundaries (no PII in events, consent-aware toggles).
6. Add legal surfaces: privacy page + terms page shell and review ownership metadata.

## Acceptance Criteria

- `/rules` is versioned and traceable to changelog/revision source.
- Metadata and structured data validate on required routes.
- Analytics implementation follows documented privacy constraints.
- Legal pages are reachable and included in nav/footer.
