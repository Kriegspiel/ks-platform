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
```css
.logo {
  content: url('/static/logo-light.png');
}

@media (prefers-color-scheme: dark) {
  .logo {
    content: url('/static/logo-dark.png');
  }
}
```

### Don'ts
- Do not add drop shadows, glows, or 3D effects
- Do not rotate or skew the mark
- Do not change the navy/ivory color values
- Do not place on busy or patterned backgrounds
- Do not add text inside or overlapping the mark

## SVG (Future)
An SVG version should be traced from these PNGs for resolution independence and CSS fill control. The SVG should use a single `<path>` with `fill: currentColor` so the site's CSS custom properties handle theme switching automatically.

## File Manifest
```
assets/logo/
├── logo-dark.png      # 1024×1024, dark theme
├── logo-light.png     # 1024×1024, light theme
└── README.md          # This spec (symlinked from LOGO.md)
```