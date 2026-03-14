# Design System

Visual design specification for the Kriegspiel platform at **kriegspiel.org**. Informed by analysis of [claude.ai](https://claude.ai) and [chatgpt.com](https://chatgpt.com) — two best-in-class conversational interfaces — adapted to the context of a chess-variant game platform.

> This document is prescriptive. Implementing agents should follow these specs exactly. Every color, size, and spacing value is intentional.

---

## Design Philosophy

**Warm minimalism with heraldic authority.**

The platform should feel like a refined chess club — serious enough for competitive play, warm enough to invite newcomers. We take the editorial warmth of Claude.ai (serif headings, cream backgrounds, generous spacing) and the functional clarity of ChatGPT (monochrome core, content-first layout, pill-shaped interactive elements). The result is a design that is:

- **Warm, not cold** — cream/ivory backgrounds instead of pure white or cool gray
- **Authoritative, not flashy** — serif headings and heraldic gold accents, no gradients or bright colors
- **Content-first** — the chessboard and referee announcements are the stars; chrome is minimal
- **Responsive, not busy** — generous whitespace, simple layouts, fast transitions
- **Themed** — full light/dark mode, toggled via the double-headed knight logo

---

## Color Palette

### Light Theme (Default)

| Token | Hex | Usage |
|---|---|---|
| `--bg-primary` | `#F5F0EB` | Page background — warm ivory, similar to Claude's `#F5F3F0` |
| `--bg-surface` | `#FFFFFF` | Cards, modals, input backgrounds |
| `--bg-subtle` | `#FAF8F5` | Sidebar, secondary panels, hover states |
| `--bg-hover` | `#F0EDE8` | Hover state for sidebar items, ghost buttons |
| `--text-primary` | `#1A1A2E` | Headings, primary body text — matches logo navy-black |
| `--text-body` | `#4A4A5A` | Regular body text — warm dark gray |
| `--text-secondary` | `#78716C` | Labels, captions, timestamps — warm stone |
| `--text-placeholder` | `#A8A29E` | Input placeholders, disabled text |
| `--border-default` | `#E7E5E2` | Card borders, dividers — barely visible |
| `--border-input` | `#D6D3D0` | Input field borders |
| `--border-focus` | `#1A1A2E` | Focused input border — navy-black |
| `--accent-gold` | `#C9A84C` | Heraldic gold — active indicators, links, highlights |
| `--accent-gold-hover` | `#B8963E` | Gold on hover (darkened 10%) |
| `--accent-error` | `#C45A3C` | Error states, illegal move feedback |
| `--accent-success` | `#4A8C5C` | Success states, legal move confirmation |
| `--shadow-subtle` | `rgba(0, 0, 0, 0.04)` | Minimal lift |
| `--shadow-card` | `rgba(0, 0, 0, 0.06)` | Card elevation |
| `--shadow-modal` | `rgba(0, 0, 0, 0.10)` | Modal/dialog elevation |

### Dark Theme

| Token | Hex | Usage |
|---|---|---|
| `--bg-primary` | `#0F0F1A` | Page background — deep navy-black |
| `--bg-surface` | `#1A1A2E` | Cards, modals — the logo's navy |
| `--bg-subtle` | `#16162A` | Sidebar, secondary panels |
| `--bg-hover` | `#222240` | Hover state for interactive elements |
| `--text-primary` | `#F5F0EB` | Headings, primary text — warm off-white |
| `--text-body` | `#C8C4BE` | Body text — muted cream |
| `--text-secondary` | `#8A8680` | Labels, captions — dimmed warm gray |
| `--text-placeholder` | `#5A5856` | Placeholders, disabled |
| `--border-default` | `#2A2A44` | Subtle card edges |
| `--border-input` | `#3A3A54` | Input borders |
| `--border-focus` | `#C9A84C` | Focus ring — heraldic gold (more visible on dark) |
| `--accent-gold` | `#C9A84C` | Same gold — consistent across themes |
| `--accent-gold-hover` | `#D4B65E` | Gold on hover (lightened 10%) |
| `--accent-error` | `#E87759` | Error — warmer, more visible on dark |
| `--accent-success` | `#5CA86C` | Success — brighter on dark |
| `--shadow-subtle` | `rgba(0, 0, 0, 0.20)` | Stronger shadows on dark |
| `--shadow-card` | `rgba(0, 0, 0, 0.30)` | Card elevation |
| `--shadow-modal` | `rgba(0, 0, 0, 0.40)` | Modal elevation |

### Color Principles

1. **No blue or bright accent colors in the core UI.** The palette is warm neutrals + heraldic gold + navy-black. Color accents are reserved for semantic states only (error, success).
2. **Gold (`#C9A84C`) is the only brand accent.** Used for active nav items, links on hover, focused states (dark mode), and sparingly for emphasis.
3. **Warm undertones everywhere.** Backgrounds lean toward cream/ivory (light) or warm navy (dark), never cool gray.
4. **Both themes use the same gold.** The gold reads well on both ivory and navy.

### CSS Custom Properties

```css
:root {
  /* Light theme (default) */
  --bg-primary: #F5F0EB;
  --bg-surface: #FFFFFF;
  --bg-subtle: #FAF8F5;
  --bg-hover: #F0EDE8;
  --text-primary: #1A1A2E;
  --text-body: #4A4A5A;
  --text-secondary: #78716C;
  --text-placeholder: #A8A29E;
  --border-default: #E7E5E2;
  --border-input: #D6D3D0;
  --border-focus: #1A1A2E;
  --accent-gold: #C9A84C;
  --accent-gold-hover: #B8963E;
  --accent-error: #C45A3C;
  --accent-success: #4A8C5C;
  --shadow-subtle: rgba(0, 0, 0, 0.04);
  --shadow-card: rgba(0, 0, 0, 0.06);
  --shadow-modal: rgba(0, 0, 0, 0.10);
  --logo-fill: #1A1A2E;
  --logo-bg: #F5F0EB;
}

[data-theme="dark"] {
  --bg-primary: #0F0F1A;
  --bg-surface: #1A1A2E;
  --bg-subtle: #16162A;
  --bg-hover: #222240;
  --text-primary: #F5F0EB;
  --text-body: #C8C4BE;
  --text-secondary: #8A8680;
  --text-placeholder: #5A5856;
  --border-default: #2A2A44;
  --border-input: #3A3A54;
  --border-focus: #C9A84C;
  --accent-gold: #C9A84C;
  --accent-gold-hover: #D4B65E;
  --accent-error: #E87759;
  --accent-success: #5CA86C;
  --shadow-subtle: rgba(0, 0, 0, 0.20);
  --shadow-card: rgba(0, 0, 0, 0.30);
  --shadow-modal: rgba(0, 0, 0, 0.40);
  --logo-fill: #F5F0EB;
  --logo-bg: #0F0F1A;
}
```

---

## Typography

### Font Stack

| Role | Font | Fallback | Source |
|---|---|---|---|
| **Headings** | Playfair Display | Georgia, "Times New Roman", serif | Google Fonts (free) |
| **Body / UI** | Inter | system-ui, -apple-system, "Segoe UI", Roboto, sans-serif | Google Fonts (free) |
| **Monospace** | JetBrains Mono | "Fira Code", "Courier New", monospace | Google Fonts (free) |

### Why This Pairing

- **Playfair Display** for headings follows Claude.ai's editorial serif approach (Tiempos Text). It has high stroke contrast and classical proportions that evoke the heraldic, 19th-century chess-club atmosphere. It pairs naturally with the double-headed knight logo.
- **Inter** for body follows ChatGPT's approach of a clean, highly-legible sans-serif (Söhne). Inter is free, has excellent screen rendering, and supports all weights needed.
- **No custom/proprietary fonts.** Everything from Google Fonts — easy for agents to implement, no licensing.

### Type Scale

| Token | Size | Weight | Line Height | Letter Spacing | Usage |
|---|---|---|---|---|---|
| `--font-hero` | 48px | 700 | 1.1 | -0.02em | Landing page hero heading |
| `--font-h1` | 32px | 700 | 1.15 | -0.02em | Page titles ("Lobby", "Game Review") |
| `--font-h2` | 24px | 600 | 1.2 | -0.01em | Section headings within a page |
| `--font-h3` | 20px | 600 | 1.25 | -0.01em | Card titles, panel headers |
| `--font-h4` | 16px | 600 | 1.3 | 0 | Sub-section labels |
| `--font-body` | 15px | 400 | 1.6 | 0 | Paragraph text, referee announcements |
| `--font-body-sm` | 14px | 400 | 1.5 | 0 | Secondary text, table cells |
| `--font-caption` | 13px | 400 | 1.4 | 0 | Timestamps, metadata, footnotes |
| `--font-small` | 12px | 500 | 1.3 | 0.01em | Badges, labels, keyboard shortcuts |
| `--font-mono` | 14px | 400 | 1.5 | 0 | Game codes, UCI moves, technical data |

### Typography Rules

1. **Headings are always Playfair Display (serif).** Never use Inter for headings.
2. **Body and UI are always Inter (sans-serif).** Buttons, inputs, labels, navigation — all Inter.
3. **Headings use `--text-primary`**, body uses `--text-body`**, captions use `--text-secondary`**.
4. **Heading weights**: hero and h1 use Bold (700), h2-h4 use SemiBold (600). Never use Regular for headings.
5. **No all-caps** except for tiny labels/badges (12px) which may use `text-transform: uppercase` with `letter-spacing: 0.05em`.
6. **Link style**: `--text-body` color by default, `--accent-gold` on hover, with a 200ms color transition. No underline by default; underline on hover.

### Font Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&family=JetBrains+Mono:wght@400&display=swap" rel="stylesheet">
```

Load only the weights used: Inter 400/500/600, Playfair Display 600/700, JetBrains Mono 400. Use `font-display: swap` to prevent FOIT.

---

## Spacing System

### Base Unit: 8px

All spacing values are multiples of 8px (with 4px for micro adjustments). Inspired by Claude.ai's 8px grid.

| Token | Value | Usage |
|---|---|---|
| `--space-0` | 0 | Reset |
| `--space-1` | 4px | Micro — icon-to-text gap, inline element spacing |
| `--space-2` | 8px | Small — between tightly related items (list items, badges) |
| `--space-3` | 12px | Medium-small — sidebar item padding, button internal gap |
| `--space-4` | 16px | Default — standard padding, paragraph spacing |
| `--space-5` | 20px | Medium — form field gaps |
| `--space-6` | 24px | Large — card padding, section sub-spacing |
| `--space-8` | 32px | XL — between major groups within a section |
| `--space-10` | 40px | 2XL — page top padding |
| `--space-12` | 48px | 3XL — between page sections |
| `--space-16` | 64px | 4XL — major vertical rhythm (hero to content) |
| `--space-20` | 80px | 5XL — hero section padding |

### Spacing Principles

1. **Generous whitespace.** Follow Claude.ai's airy approach — sections should breathe. Use 48-64px between page sections, not 24-32px.
2. **Consistent card padding:** 24px on all sides.
3. **Form field gap:** 20px between fields.
4. **Button padding:** 12px vertical, 24px horizontal (primary); 10px vertical, 20px horizontal (secondary).

---

## Layout

### Container

```css
.container {
  max-width: 880px;            /* ChatGPT-inspired content width */
  margin: 0 auto;
  padding: 0 var(--space-6);  /* 24px horizontal padding */
}

.container--wide {
  max-width: 1080px;           /* For lobby, leaderboard (tables) */
}
```

### Page Layout Structure

```
┌────────────────────────────────────────────────────────────┐
│  Header (56px height, sticky, full-width)                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│     ┌──── Content Container (max-width: 880px) ────┐      │
│     │                                               │      │
│     │  Page content, centered horizontally           │      │
│     │                                               │      │
│     └───────────────────────────────────────────────┘      │
│                                                            │
│  Footer (minimal — copyright + links)                      │
└────────────────────────────────────────────────────────────┘
```

- **No sidebar.** Unlike ChatGPT, Kriegspiel has no conversation history sidebar. Pages are single-column, centered.
- **Exception: Game page** — uses a two-column layout (board left, referee panel right) within the container, collapsing to stacked on mobile.

### Header

```css
.header {
  height: 56px;
  padding: 0 var(--space-6);
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

Header layout:

```
[♞♞ Kriegspiel]     [Lobby]  [Leaderboard]  [Rules]     alexfil  [⚙]
 ↑                    ↑                                    ↑       ↑
 Logo + wordmark      Nav links (Inter 14px/500)           Username  Settings
 (click = theme)      Gold underline on active             link      icon button
```

- Logo + "Kriegspiel" wordmark (Playfair Display 600, 18px) on the left.
- Navigation links centered or right-aligned.
- Active nav link: `--accent-gold` color with a 2px bottom border.
- User controls on the far right.

### Game Page Layout

Two-column layout specific to the gameplay screen:

```css
.game-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: var(--space-6);
  max-width: 1080px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .game-layout {
    grid-template-columns: 1fr;
  }
}
```

- **Left column:** Chessboard (scales to fill available width, max 560px)
- **Right column:** Referee panel (fixed 320px on desktop), stacks below board on mobile

### Responsive Breakpoints

| Breakpoint | Width | Layout Changes |
|---|---|---|
| Desktop | > 1024px | Full layout, 880px container |
| Tablet | 768–1024px | Container fills width with 24px padding; game columns compress |
| Mobile | < 768px | Single column; game stacks vertically; board scales to viewport |

---

## Components

### Buttons

Blend Claude.ai's solid rounded buttons with ChatGPT's pill-shaped style. The result: rounded rectangle (not full pill) with warm colors.

#### Primary Button

```css
.btn-primary {
  background: var(--text-primary);       /* Navy-black (light) or off-white (dark) */
  color: var(--bg-primary);              /* Inverted text */
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 600;
  padding: 12px 24px;
  height: 44px;
  border: none;
  border-radius: 12px;                   /* Rounded but not pill (Claude-style) */
  cursor: pointer;
  transition: background-color 200ms ease, transform 100ms ease;
}

.btn-primary:hover {
  opacity: 0.88;
}

.btn-primary:active {
  transform: scale(0.98);
}
```

#### Secondary Button

```css
.btn-secondary {
  background: var(--bg-surface);
  color: var(--text-primary);
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 500;
  padding: 10px 20px;
  height: 40px;
  border: 1px solid var(--border-input);
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 200ms ease, border-color 200ms ease;
}

.btn-secondary:hover {
  background: var(--bg-subtle);
  border-color: var(--text-secondary);
}
```

#### Ghost Button (icon buttons, compact actions)

```css
.btn-ghost {
  background: transparent;
  color: var(--text-body);
  padding: 8px 12px;
  height: 36px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 150ms ease;
}

.btn-ghost:hover {
  background: var(--bg-hover);
}
```

#### Game Action Button (Ask "Any?", Resign)

```css
.btn-game-action {
  background: transparent;
  color: var(--accent-gold);
  font-weight: 600;
  padding: 10px 20px;
  height: 40px;
  border: 2px solid var(--accent-gold);
  border-radius: 12px;
  cursor: pointer;
  transition: all 200ms ease;
}

.btn-game-action:hover {
  background: var(--accent-gold);
  color: var(--bg-surface);
}

.btn-game-action--danger {
  color: var(--accent-error);
  border-color: var(--accent-error);
}

.btn-game-action--danger:hover {
  background: var(--accent-error);
  color: var(--bg-surface);
}
```

### Inputs

#### Text Input

```css
.input {
  background: var(--bg-surface);
  color: var(--text-primary);
  font-family: "Inter", sans-serif;
  font-size: 15px;
  padding: 12px 16px;
  height: 48px;
  border: 1px solid var(--border-input);
  border-radius: 12px;
  width: 100%;
  transition: border-color 150ms ease, box-shadow 150ms ease;
}

.input::placeholder {
  color: var(--text-placeholder);
}

.input:hover {
  border-color: var(--text-secondary);
}

.input:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(26, 26, 46, 0.08);   /* light theme */
}

[data-theme="dark"] .input:focus {
  box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.20);  /* gold glow on dark */
}
```

#### Select / Dropdown

Same dimensions and border style as text input. Arrow icon from Lucide (`chevron-down`), positioned right. Opens a native `<select>` on mobile, custom dropdown on desktop if needed.

### Cards

```css
.card {
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  padding: var(--space-6);               /* 24px */
  box-shadow: 0 1px 3px var(--shadow-subtle);
  transition: box-shadow 200ms ease, transform 200ms ease;
}

.card--interactive:hover {
  box-shadow: 0 4px 12px var(--shadow-card);
  transform: translateY(-1px);
}
```

- **Lobby game cards** (open games list): `.card--interactive` with hover lift.
- **Stats cards** (profile page): static `.card`.
- **Form cards** (login, register): `.card` with `max-width: 420px`, centered.

### Modal / Dialog

```css
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.40);
  backdrop-filter: blur(4px);
  z-index: 200;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--bg-surface);
  border-radius: 20px;
  padding: var(--space-8);               /* 32px */
  max-width: 440px;
  width: 90%;
  box-shadow: 0 8px 32px var(--shadow-modal);
  z-index: 201;
}
```

Used for: resign confirmation, game-over summary, settings sub-dialogs.

### Referee Panel

The referee announcement log during gameplay:

```css
.referee-panel {
  background: var(--bg-subtle);
  border: 1px solid var(--border-default);
  border-radius: 16px;
  padding: var(--space-4);               /* 16px */
  max-height: 500px;
  overflow-y: auto;
}

.referee-message {
  font-family: "Inter", sans-serif;
  font-size: 14px;
  color: var(--text-body);
  padding: 8px 12px;
  border-radius: 8px;
  margin-bottom: 4px;
  animation: referee-appear 300ms ease-out;
}

.referee-message--announcement {
  /* Referee voice: italic, slightly muted */
  font-style: italic;
  color: var(--text-secondary);
}

.referee-message--capture {
  /* Captures get gold emphasis */
  border-left: 3px solid var(--accent-gold);
  padding-left: 12px;
}

.referee-message--check {
  /* Checks get error/warning emphasis */
  border-left: 3px solid var(--accent-error);
  padding-left: 12px;
}

.referee-message--game-over {
  font-weight: 600;
  color: var(--text-primary);
  background: var(--bg-hover);
  text-align: center;
  padding: 16px;
}

@keyframes referee-appear {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### Chessboard Styling

The board uses `chessboard.js` with custom theming to match:

```css
/* Board square colors */
.board-light-square {
  background: #F0E6D6;    /* Warm cream — lighter than page bg */
}

.board-dark-square {
  background: #B8A080;    /* Warm brown — muted, not harsh */
}

[data-theme="dark"] .board-light-square {
  background: #4A4460;    /* Muted purple-gray */
}

[data-theme="dark"] .board-dark-square {
  background: #2E2A44;    /* Deep navy-purple */
}

/* Highlight: last move */
.board-highlight {
  background: rgba(201, 168, 76, 0.35);   /* Gold overlay */
}

/* Board border */
.board-container {
  border: 2px solid var(--border-default);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px var(--shadow-card);
}
```

Board coordinate labels (a-h, 1-8): Inter 11px/500, `--text-secondary`.

### Phantom Piece Styling

Phantom pieces are client-side opponent tracking aids (see [FRONTEND.md](./FRONTEND.md)).

```css
/* Phantom pieces (opponent tracking aids) */
.phantom-piece {
  opacity: 0.45;
  filter: grayscale(20%);
  pointer-events: all;
  cursor: grab;
  position: relative;
}

.phantom-piece::after {
  content: '';
  position: absolute;
  inset: 2px;
  border: 2px dashed var(--accent-gold);
  border-radius: 4px;
  opacity: 0;
  transition: opacity 150ms;
}

.phantom-piece:hover {
  opacity: 0.65;
}

.phantom-piece:hover::after {
  opacity: 1;
}

.phantom-tray {
  background: var(--bg-subtle);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  padding: var(--space-2);
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  margin-top: var(--space-3);
}

.phantom-tray-piece {
  width: 32px;
  height: 32px;
  opacity: 0.5;
  cursor: grab;
  transition: opacity 150ms;
}

.phantom-tray-piece:hover {
  opacity: 0.8;
}
```

### Pawn Promotion Modal

```css
.promotion-modal {
  /* Inherits from .modal base styles */
  max-width: 240px;
  padding: var(--space-4);
  display: flex;
  gap: var(--space-3);
  justify-content: center;
}

.promotion-option {
  width: 48px;
  height: 48px;
  cursor: pointer;
  border-radius: var(--radius-md);
  border: 2px solid transparent;
  transition: border-color 150ms ease;
  background: transparent;
  padding: 4px;
}

.promotion-option:hover {
  border-color: var(--accent-gold);
  background: var(--bg-hover);
}
```

### Connection Status Indicator

```css
.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot--connected {
  background: var(--accent-success);
}

.status-dot--disconnected {
  background: var(--text-placeholder);
}
```

### Toast Notifications

Transient feedback messages (illegal move, connection status, etc.):

```css
.toast {
  position: fixed;
  bottom: var(--space-6);
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  border-radius: var(--radius-lg);
  font-family: "Inter", sans-serif;
  font-size: 14px;
  font-weight: 500;
  z-index: 300;
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  box-shadow: 0 4px 16px var(--shadow-card);
  animation: toast-in 300ms ease-out, toast-out 300ms ease-in 2.7s forwards;
}

.toast--error {
  border-color: var(--accent-error);
  color: var(--accent-error);
}

.toast--success {
  border-color: var(--accent-success);
  color: var(--accent-success);
}

@keyframes toast-in {
  from { opacity: 0; transform: translateX(-50%) translateY(8px); }
  to   { opacity: 1; transform: translateX(-50%) translateY(0); }
}

@keyframes toast-out {
  from { opacity: 1; }
  to   { opacity: 0; }
}
```

### Chess Clock (Timer Display)

```css
.clock {
  font-family: "JetBrains Mono", monospace;
  font-size: 24px;
  font-weight: 400;
  padding: 8px 16px;
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  border: 1px solid var(--border-default);
  min-width: 100px;
  text-align: center;
}

.clock--active {
  color: var(--text-primary);
  border-color: var(--accent-gold);
}

.clock--inactive {
  color: var(--text-secondary);
}

.clock--low {
  color: var(--accent-error);
  animation: clock-pulse 1s ease-in-out infinite;
}

@keyframes clock-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
```

---

## Shadows

Minimal, subtle, multi-layered shadows — following Claude.ai's "almost flat" approach.

| Level | Value | Usage |
|---|---|---|
| Level 0 | none | Default state for most elements |
| Level 1 | `0 1px 2px var(--shadow-subtle)` | Subtle lift — cards at rest, header |
| Level 2 | `0 1px 3px var(--shadow-subtle), 0 4px 12px var(--shadow-card)` | Interactive card on hover |
| Level 3 | `0 4px 16px var(--shadow-card)` | Dropdowns, popovers |
| Level 4 | `0 8px 32px var(--shadow-modal)` | Modals, dialogs |

Never use `drop-shadow` or strongly-colored shadows. Always use `rgba(0,0,0,…)`.

---

## Border Radius

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | 6px | Small interactive elements (badges, tags, chips) |
| `--radius-md` | 8px | Ghost buttons, sidebar items, referee messages |
| `--radius-lg` | 12px | Primary/secondary buttons, inputs, form elements |
| `--radius-xl` | 16px | Cards, referee panel |
| `--radius-2xl` | 20px | Modals, dialogs |

Note: We use 12px for interactive elements (buttons, inputs) — a middle ground between Claude's 10px rounded rectangles and ChatGPT's 20-28px pills. This is rounded enough to feel modern, but rectangular enough to feel structured/heraldic.

---

## Animation & Transitions

### Timing

| Token | Duration | Usage |
|---|---|---|
| `--duration-instant` | 100ms | Active/press states |
| `--duration-fast` | 150ms | Focus rings, ghost button hovers |
| `--duration-normal` | 200ms | Button hovers, link color changes |
| `--duration-slow` | 300ms | Modal appear, theme toggle, referee message appear |
| `--duration-slower` | 400ms | Page-level transitions (rare) |

### Easing

```css
--ease-default: ease-in-out;
--ease-smooth: cubic-bezier(0.16, 1, 0.3, 1);    /* Claude-style smooth */
--ease-natural: cubic-bezier(0.7, 0, 0.84, 0);
```

### Hover States

- **Buttons**: background-color shift, 200ms
- **Links**: color change to `--accent-gold`, 200ms
- **Cards (interactive)**: translateY(-1px) + shadow increase, 200ms
- **Ghost buttons**: background to `--bg-hover`, 150ms

### Focus States

- **Inputs**: border-color to `--border-focus`, box-shadow glow ring, 150ms
- **Buttons**: visible outline ring, 2px offset
- **All**: respect `prefers-reduced-motion: reduce` — disable transforms and reduce transitions to opacity/color only

### Theme Toggle

See [LOGO.md](./LOGO.md) for the full theme toggle specification. Summary:

- Logo fill crossfades (300ms)
- Page background, text, borders all transition (300ms)
- `transition: background-color 300ms, color 300ms, border-color 300ms`

### Referee Message Animation

New referee announcements slide up and fade in (300ms, `ease-out`). The most recent message briefly has a subtle gold left-border flash (fades after 1s).

---

## Icons

**Icon set:** [Lucide](https://lucide.dev/) — lightweight, consistent, MIT-licensed.

| Context | Icon | Size |
|---|---|---|
| Settings | `settings` (gear) | 20px |
| Login | `log-in` | 20px |
| Logout | `log-out` | 20px |
| Resign | `flag` | 20px |
| Connected | `circle` (filled green) | 8px |
| Disconnected | `circle` (filled gray) | 8px |
| Turn indicator | `clock` | 16px |
| Copy game code | `copy` | 16px |
| Leaderboard | `trophy` | 20px |
| Profile | `user` | 20px |
| Expand/Collapse | `chevron-down` / `chevron-up` | 16px |
| External link | `external-link` | 14px |

Icon style: outline (stroke-width 1.5px), inherits parent color. No filled icons except status dots.

---

## Page-Specific Design Notes

### Home / Landing (`/`)

- Hero section: Playfair Display 48px heading ("The Chess You Can't See"), Inter 16px body, centered layout
- Primary CTA button: "Play Now" (`.btn-primary`, 48px tall, min-width 200px)
- Secondary CTA: "Learn the Rules" (`.btn-secondary`)
- Recent games: subtle card list below hero, auto-refreshing via HTMX
- Background: `--bg-primary` (warm ivory/dark navy)

### Login / Register (`/auth/*`)

- Centered form card (max-width 420px, `.card`, 32px padding)
- Logo + "Kriegspiel" above the form (stacked layout from LOGO.md)
- Input fields at 48px height, 12px radius
- "Log in" / "Create account" primary button full-width
- "Or sign in with Google" divider + OAuth button below (Phase 2)
- Link between login↔register at bottom: "Don't have an account? Sign up" — `--text-secondary`, gold on hover

### Lobby (`/lobby`)

- Create Game card: bordered card at top with rule selector, color selector, CTA button
- Join by Code: inline form — text input + "Join" button in a row
- Open Games: table or card list, with `.card--interactive` hover
- My Active Games: separate section with "Your turn" gold indicator

### Game (`/game/{game_id}`)

- Two-column layout (board + referee)
- Board: maximum 560px width, centered in left column
- Referee panel: 320px right column, scrollable, `--bg-subtle` background
- Action buttons below referee: "Ask Any?" (gold outline), "Resign" (error outline)
- Player info bar above board: names, colors, connection status

### Game Review (`/game/{game_id}/review`)

- Full board (referee view) in left column
- Move log in right column — clickable moves, current move highlighted with gold background
- Perspective toggles: radio buttons (Referee / White / Black)
- Step controls: `◀ ▶` buttons, arrow key support

### Profile (`/user/{username}`)

- Stats cards: wins/losses/draws/ELO in a 2×2 or 4-across grid
- Recent games: table with result, opponent, method, date
- Clean, information-dense layout — no hero, just data

### Leaderboard (`/leaderboard`)

- Full-width table within `.container--wide`
- Columns: Rank, Username, ELO, Games, Win Rate
- Top 3 get `--accent-gold` rank numbers
- Alternating row backgrounds: `--bg-surface` / `--bg-subtle`

---

## Accessibility

| Requirement | Implementation |
|---|---|
| Color contrast | All text meets WCAG AA (4.5:1 for body, 3:1 for large text). Test both themes. |
| Focus visibility | Visible focus ring on all interactive elements. Never `outline: none` without replacement. |
| Reduced motion | `@media (prefers-reduced-motion: reduce)` disables transforms, reduces transitions to opacity only. |
| Semantic HTML | `<nav>`, `<main>`, `<article>`, `<aside>`, `<header>`, `<footer>`. |
| ARIA | `role="log"` + `aria-live="polite"` on referee panel. Labels on all inputs. Buttons have accessible names. |
| Keyboard | Tab navigation through all controls. Arrow keys for game review. Escape closes modals. |
| Screen reader | Referee announcements readable. Board position described textually (not just visual). |

---

## CSS Framework

**Do not use Pico CSS, Simple.css, or any classless CSS framework.** Instead, build a minimal custom stylesheet following this design system exactly.

The CSS should be:

1. **A single `kriegspiel.css` file** (< 15 KB minified)
2. **CSS custom properties** for all colors, spacing, radii, shadows (as defined above)
3. **Component classes** (`.btn-primary`, `.card`, `.input`, etc.) — not utility classes
4. **Mobile-first** media queries
5. **No CSS preprocessor needed** — modern CSS custom properties are sufficient

Load order:

```html
<link rel="stylesheet" href="/static/css/kriegspiel.css">      <!-- Design system -->
<link rel="stylesheet" href="/static/css/chessboard.css">       <!-- chessboard.js styles -->
```

---

## CSS Class Inventory

Complete list of all CSS classes defined in this design system:

| Category | Classes |
|---|---|
| Layout | `.container`, `.container--wide`, `.game-layout`, `.header` |
| Buttons | `.btn-primary`, `.btn-secondary`, `.btn-ghost`, `.btn-game-action`, `.btn-game-action--danger` |
| Inputs | `.input` |
| Cards | `.card`, `.card--interactive` |
| Modal | `.modal-backdrop`, `.modal`, `.promotion-modal`, `.promotion-option` |
| Referee | `.referee-panel`, `.referee-message`, `.referee-message--announcement`, `.referee-message--capture`, `.referee-message--check`, `.referee-message--game-over` |
| Board | `.board-container`, `.board-light-square`, `.board-dark-square`, `.board-highlight` |
| Phantom | `.phantom-piece`, `.phantom-tray`, `.phantom-tray-piece` |
| Status | `.status-dot`, `.status-dot--connected`, `.status-dot--disconnected` |
| Toast | `.toast`, `.toast--error`, `.toast--success` |
| Clock | `.clock`, `.clock--active`, `.clock--inactive`, `.clock--low` |

---

## Reference: Design Influences

| Source | What We Took | What We Didn't Take |
|---|---|---|
| [Claude.ai](https://claude.ai) | Warm palette (cream/beige), serif+sans pairing, editorial feel, generous spacing, 8px grid, subtle shadows, rounded-rectangle buttons (10-12px radius), warm border colors | Brand orange, specific font (Tiempos), massive hero sizes (78px), 12-column grid (overkill for single-column layout) |
| [ChatGPT](https://chatgpt.com) | Content-first layout, narrow centered container (768-880px), sticky header, 56px header height, functional minimalism, fast transitions, pill-shaped influence on border radius, modal styling, monochrome discipline | Pure black/white (too cold), Söhne font (proprietary), sidebar, pill buttons (too round for heraldic feel), 15px body (we use 15px too) |
| **Kriegspiel identity** | Double-headed knight logo, heraldic gold `#C9A84C`, navy-black `#1A1A2E`, Playfair Display serif, light/dark theme via logo toggle | — |