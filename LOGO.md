# Logo Specification

## Concept

The Kriegspiel platform logo is a **double-headed chess knight** — inspired by the double-headed eagle of heraldry. Two knight heads face opposite directions (left and right) on a shared neck/base, forming a symmetrical silhouette. The form is bold, heraldic, and immediately recognizable as chess-related.

The logo exists in two variants — **white** and **black** — representing the two sides of a Kriegspiel game. These variants also serve as a **light/dark theme toggle** in the UI: clicking the logo switches between day (white knight on dark ground) and night (black knight on light ground) modes.

## Why a Double-Headed Knight

- **The knight** is the most recognizable chess piece in silhouette. Unlike a pawn, rook, or bishop, it is unambiguous even at small sizes.
- **Double-headed** references heraldic tradition (Byzantine/Russian double-headed eagle), giving the mark a sense of history and authority — fitting for a game rooted in 19th-century military chess.
- **Two heads facing away** symbolize Kriegspiel's core mechanic: two players who cannot see each other's position, each looking into their own fog of war.
- **White ↔ Black duality** is chess itself, and the theme toggle makes the brand feel alive.

## Form Description

### Silhouette

```
        ╱◠╲           ╱◠╲
       ╱   ╲         ╱   ╲
      │  ◉  ╲       ╱  ◉  │
      │     ╱╲     ╱╲     │
       ╲   ╱  ╲   ╱  ╲   ╱
        ╲ ╱    ╲ ╱    ╲ ╱
         │      V      │
         │     ╱ ╲     │
         │    ╱   ╲    │
         └───╱─────╲───┘
            ╱  BASE  ╲
           ╱───────────╲
```

This ASCII is a rough guide. The actual form should follow these principles:

### Geometry

1. **Bilateral symmetry** — the left knight head is a mirror of the right knight head, reflected on the vertical center axis.
2. **Knight head shape** — follows the classic Staunton chess knight profile: curved forehead, pointed ears, open or closed mouth, strong jaw. The silhouette should be instantly readable as a chess knight at 16×16 px (favicon) through 512×512 px (social sharing).
3. **Shared neck** — the two heads merge into a single neck/body that widens into a stable base. The merge point is roughly at the throat line.
4. **Base** — a flat or slightly curved pedestal (like the base of a chess piece). Provides visual weight and grounding.
5. **Negative space** — the gap between the two heads (where they face away from each other) forms a distinctive void — this is the most recognizable feature at small sizes.
6. **No fine detail** — the logo must work as a flat single-color silhouette. No gradients, no thin lines, no textures. Every feature must survive reduction to 16×16 px.

### Proportions

- **Aspect ratio**: approximately 1:1 (square bounding box), or slightly taller (e.g., 5:6).
- **Head-to-base ratio**: the two heads occupy roughly the top 60% of the height; the neck and base occupy the bottom 40%.
- **Head width**: each head extends to about 40% of total width from center, so the full span of both heads fills ~80% of the bounding box width.
- **Negative space gap**: the opening between the two heads (at the top) is approximately 15-20% of total width.

### Eyes

- Each knight head has a single visible eye (the outward-facing eye).
- The eye is a simple circle or dot — no pupil detail. It reads as a cutout in the silhouette.
- The eye is the only interior detail in the silhouette form.

## Color Variants

### White Knight (Light Theme Default)

| Element | Value |
|---|---|
| Knight silhouette | `#F5F5F5` (off-white) |
| Eye cutout | Background color shows through |
| Background / ground | `#1A1A2E` (deep navy-black) |
| Usage | Dark theme, dark page backgrounds |

### Black Knight (Dark Theme Default)

| Element | Value |
|---|---|
| Knight silhouette | `#1A1A2E` (deep navy-black) |
| Eye cutout | Background color shows through |
| Background / ground | `#F5F5F5` (off-white) |
| Usage | Light theme, light page backgrounds |

### Monochrome

For contexts where only one color is available (favicon, watermark, stamp):

- **Black on transparent** — the primary monochrome form.
- **White on transparent** — for dark backgrounds.

### Accent Color (Optional)

If a single accent is ever needed (error states, active indicators):

- `#C9A84C` — muted heraldic gold. Used sparingly, never on the logo itself.

## Theme Toggle Behavior

The logo doubles as the **light/dark theme switch** in the site header:

```
┌──────────────────────────────────────────────┐
│  [♞♞] Kriegspiel    alexfil    ⚙ Logout     │
│   ↑                                          │
│   Logo: click to toggle theme                │
└──────────────────────────────────────────────┘
```

### Transition

1. **Default state**: white knight on dark ground (dark theme) or black knight on light ground (light theme), matching current theme.
2. **On hover**: subtle scale-up (1.05×) and a faint glow or shadow shift.
3. **On click**: the knight silhouette **crossfades** from white→black or black→white over 300ms. Simultaneously, the page theme transitions (CSS `transition: background-color 300ms, color 300ms`).
4. **The two variants are not separate images** — they are the same SVG with `fill` color controlled by CSS custom properties (`--logo-fill`, `--logo-bg`), so the transition is smooth.

### Implementation

```css
:root {
  --logo-fill: #1A1A2E;         /* black knight for light theme */
  --logo-bg: #F5F5F5;
}

[data-theme="dark"] {
  --logo-fill: #F5F5F5;         /* white knight for dark theme */
  --logo-bg: #1A1A2E;
}

.logo svg {
  fill: var(--logo-fill);
  transition: fill 300ms ease;
  cursor: pointer;
}

.logo svg:hover {
  transform: scale(1.05);
}
```

```javascript
document.querySelector('.logo').addEventListener('click', () => {
  const current = document.documentElement.dataset.theme;
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  localStorage.setItem('theme', next);
});
```

## File Deliverables

The logo must be delivered as:

| File | Format | Purpose |
|---|---|---|
| `logo.svg` | SVG | Single SVG file. Fill color controlled by CSS. This is the primary logo used everywhere on the site. |
| `favicon.svg` | SVG | Simplified version optimized for 16×16. May drop the base or reduce head detail. |
| `favicon.ico` | ICO | Multi-resolution (16, 32, 48 px) generated from favicon.svg. |
| `og-image-dark.png` | PNG 1200×630 | Open Graph / social sharing image. White knight centered on dark background with "Kriegspiel" text. |
| `og-image-light.png` | PNG 1200×630 | Open Graph / social sharing image. Black knight centered on light background with "Kriegspiel" text. |
| `apple-touch-icon.png` | PNG 180×180 | iOS home screen icon. Knight silhouette centered with padding. |

All SVGs must be clean: no embedded raster images, no fonts (text converted to paths), no unnecessary groups or transforms. Optimized with SVGO.

## Typography Pairing

When the logo appears alongside the wordmark "Kriegspiel":

- **Font**: A serif with strong contrast and classical proportions. Candidates:
  - **Playfair Display** (Google Fonts, free) — high contrast, elegant, chess-appropriate.
  - **Cormorant Garamond** (Google Fonts, free) — lighter, more refined, heraldic feel.
  - **EB Garamond** (Google Fonts, free) — classic, excellent readability.
- **Weight**: Regular (400) or SemiBold (600) for the wordmark. Never bold or black.
- **Case**: Title case ("Kriegspiel"), never all-caps.
- **Spacing**: Standard letter-spacing. No tracking adjustments.
- **Color**: Matches `--logo-fill` (same color as the knight silhouette).

### Logo + Wordmark Layout

```
Horizontal (header):    [♞♞] Kriegspiel
                         ↑      ↑
                        logo   wordmark, vertically centered with logo

Stacked (splash/OG):      [♞♞]
                        Kriegspiel
                         ↑
                        centered below logo, with 8-12px gap
```

## References for the Agent

When generating or drawing the logo, use these as conceptual inputs:

- **Chess knight silhouette**: Staunton knight piece profile (the standard tournament chess piece shape).
- **Double-headed eagle**: Byzantine/Russian coat of arms — note the symmetry, the outward-facing heads, the shared body, and the heraldic simplicity.
- **Heraldic style**: Bold outlines, flat fills, no gradients. The form should look like it could be stamped on a wax seal or carved into stone.
- **NOT a realistic horse**: This is a chess piece, not an animal illustration. It should be stylized, geometric, and iconic — not anatomically accurate.

## Do Not

- Do not add a crown, scepter, or orb (unlike the heraldic eagle). The knight heads alone are sufficient.
- Do not add wings. This is a chess knight, not a pegasus.
- Do not use gradients, shadows, or 3D effects in the logo form itself.
- Do not use more than one color in the logo silhouette (the eye cutout is negative space, not a second color).
- Do not outline the logo. It is a filled silhouette, not a line drawing.
- Do not rotate or tilt the logo. It always sits upright on its base.
