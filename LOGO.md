# Kriegspiel Logo — Final Specification

## Concept
Double-headed Staunton knight — two chess knight profiles facing away from each other (back-to-back), joined at the neck/back, sitting on a thin horizontal base line. The split between the two knights is visible as a narrow curved gap, making each profile distinct.

## Chosen Design
- **Style**: Flat vector silhouette, no gradients, no texture, no eyes/dots
- **Shape**: Wider-than-tall mark, two mirrored knight heads with a curved gap between them
- **Base**: Single thin horizontal line beneath the merged shape
- **Symmetry**: Near-perfect left-right mirror (slight organic variation from AI generation)

## Color Variants

### Dark Theme (Night Mode)
- **File**: `assets/logo/logo-dark.png`
- **Background**: Navy-black `#1A1A2E`
- **Mark fill**: Warm ivory `#F5F0EB`
- **Dimensions**: 1024 × 1024 px

### Light Theme (Day Mode)
- **File**: `assets/logo/logo-light.png`
- **Background**: Warm ivory `#F5F0EB`
- **Mark fill**: Navy-black `#1A1A2E`
- **Dimensions**: 1024 × 1024 px
- **Note**: Gap between knights is slightly narrower than dark variant (per design review)

## Usage Guidelines

### Minimum Size
- **Digital**: 32 × 32 px (favicon), 64 × 64 px (recommended minimum)
- **Print**: 12 mm × 12 mm

### Clear Space
- Maintain padding equal to ≥ 25% of mark width on all sides

### Theme Switching (CSS)

Uses the `data-theme` attribute (consistent with [DESIGN.md](./DESIGN.md)):

```css
.logo {
  content: url('/static/img/logo-light.png');
}

[data-theme="dark"] .logo {
  content: url('/static/img/logo-dark.png');
}
```

### Don'ts
- Do not add drop shadows, glows, or 3D effects
- Do not rotate or skew the mark
- Do not change the navy/ivory color values
- Do not place on busy or patterned backgrounds
- Do not add text inside or overlapping the mark

## SVG (Phase 1 Priority)

An SVG version should be traced from these PNGs for resolution independence and CSS fill control. This is a **Phase 1 priority** because the design system relies on `fill: currentColor` for seamless theme switching, and PNG swapping via CSS `content` property only works on replaced elements.

The SVG should use a single `<path>` with `fill: currentColor` so the site's CSS custom properties handle theme switching automatically.

## Favicon Specification

The following favicon files are needed for `base.html`:

| File | Format | Size | Purpose |
|---|---|---|---|
| `favicon.ico` | ICO | 32x32 | Browser tab icon |
| `favicon-192.png` | PNG | 192x192 | Android home screen |
| `apple-touch-icon.png` | PNG | 180x180 | iOS home screen |

Include these `<link>` tags in `base.html`:

```html
<link rel="icon" href="/static/img/favicon.ico" sizes="32x32">
<link rel="icon" href="/static/img/favicon-192.png" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="/static/img/apple-touch-icon.png">
```

## File Manifest
```
assets/logo/
├── logo-dark.png      # 1024×1024, dark theme
├── logo-light.png     # 1024×1024, light theme
└── README.md          # This spec (symlinked from LOGO.md)
```