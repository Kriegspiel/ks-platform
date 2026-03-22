# Step 510 - Chess Board Component and Visual-State Primitives

## Goal

Build reusable board rendering and click semantics that all gameplay UI depends on.

## Objective and Scope

- In scope: `ChessBoard` component, FEN parsing, orientation flip, highlight rendering, disabled click guard.
- In scope: board CSS for piece/square/highlight/phantom visuals and responsive sizing.
- Out of scope: polling logic, API calls, promotion flow.

## Dependencies and Order

- Depends on Step 400 payload conventions.
- Blocks slices 520/530/540.

## Acceptance Criteria

- Board renders from FEN correctly.
- Black orientation flips board and coordinates.
- Square clicks emit algebraic names.
- Highlight + phantom overlays are visually distinct.
