# Handoff: Logo lockup in the top nav + browser tab favicon

## Overview
Two related brand changes for the **"Be Smarter Than the Tool"** course (the AI Leadership Society):

1. **Header logo lockup** — place the AI Leadership Society mark to the left of the course title in the navy top-nav header.
2. **Browser tab favicon** — replace the current faint tab icon with the navy "app-tile" badge of the same mark, in all the sizes browsers/devices need.

Both use the same source mark (a serif **A** + gold swoosh + stylized **i**, i.e. "Aɩ").

## About the design files
The files in `reference/` are **design references created in HTML** — prototypes that show the intended look, not production code to paste in. The job is to **recreate these in the course's real `index.html`** using its existing structure and CSS. The header in the live course is rendered by React (`React.createElement`) inside one large `index.html`; match that pattern. Image assets in `assets/` ARE final and should be copied into the codebase as-is.

> Note: the design was prototyped against a slightly older copy of `index.html`. Implement against the **current** `index.html` in the repo — the specs below are written to be applied to whatever the current header markup is.

## Fidelity
**High-fidelity.** Exact colors, fonts, sizes, and spacing are given below. Recreate pixel-for-pixel using the course's existing fonts and CSS conventions.

---

## Part 1 — Header logo lockup

### What changes
In the navy header (`.course-header` → `.course-topbar`), the left side currently holds only the title lockup (`.course-title-lockup`: the H1 "Be Smarter *Than the Tool*" + gold subtitle "AI Predicts. You Decide."). **Add the logo mark immediately to its left**, grouped with the title in a flex row.

### Recommended treatment — "white circle plate" (Option A)
The mark sits on a white circular plate so it reads at high contrast against the navy bar.

**Structure**
```
.lockup-zone            (display:flex; align-items:center; gap:17px; min-width:0)
├── .logo-plate         (the white circle holding the mark)
│   └── img             (logo-disc.png)
└── .course-title-lockup (existing H1 + subtitle, unchanged)
```

**`.logo-plate` (white circle)**
- width / height: **66px**
- border-radius: **50%**
- background: **#ffffff**
- display:flex; align-items:center; justify-content:center
- box-shadow: **0 6px 18px -6px rgba(0,0,0,0.45)**
- flex: 0 0 auto (never shrink)

**`.logo-plate img`** — source `assets/logo-disc.png`
- width / height: **58px**
- border-radius: **50%** (the source is already a navy disc; rounding guards against edge fringe)
- display:block

**Spacing:** `gap: 17px` between the plate and the title lockup. The whole `.lockup-zone` is the left child of `.course-topbar`; the existing right-side cluster (user name / progress bar / "Continue" button) is unchanged.

**Responsive (≤760px):** keep the plate at 66px (or step to 56px if space is tight) and keep it inline to the left of the title; do not stack the logo above the title.

### Alternatives (shown in `reference/Header Logo Options.html`)
- **B — gold ring:** same disc, no white plate; wrap in a 3px ring of **#ffd24a** (68px outer, 3px padding, disc fills remainder). Use if a lighter, more "on-navy" look is wanted.
- **C — app tile:** disc on a 64px white **rounded-square** (radius 17px) instead of a circle.
- **D — full lockup plaque:** the entire "AI Leadership Society" lockup (`assets/logo-lockup.png`) in a white rounded panel. Trade-off: it's tall and pushes the title to wrap — only use if showing the org name in the header is a hard requirement.

Default to **Option A** unless told otherwise.

---

## Part 2 — Browser tab favicon

### What changes
Add favicon `<link>` tags to the `<head>` of `index.html` (there are currently none) and ship the icon PNGs alongside it.

### Chosen treatment — "app tile" (rounded square)
A self-contained badge: the "Aɩ" mark centered on a navy rounded square. Chosen over a circle because it fills more of the 16px tab box, so the mark reads larger; it also matches favicon convention and holds up on both light and dark browser tabs. (The full "Leadership Society" lockup is intentionally NOT used here — its small-caps lines turn illegible below ~64px. Keep that lockup for the header/footer/print only.)

### Assets (in `assets/`, already final — copy into the codebase)
| File | Size | Use |
|---|---|---|
| `favicon-16x16.png` | 16×16 | tab icon |
| `favicon-32x32.png` | 32×32 | tab icon (retina) / bookmarks |
| `favicon-48x48.png` | 48×48 | Windows / high-DPI |
| `apple-touch-icon.png` | 180×180 | iOS "Add to Home Screen" |
| `icon-512.png` | 512×512 | PWA / Android maskable-safe |

### Markup — add inside `<head>`, right after `<title>`
Adjust the `href` paths to wherever the icons live relative to `index.html` (in the prototype they sit next to it, so paths are bare filenames):
```html
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
<link rel="icon" type="image/png" sizes="48x48" href="favicon-48x48.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
```

### Regenerating the badge (if a vector/source is later available)
The badge is the navy disc mark recropped onto a rounded square:
- background navy: **#00245a** (rgb 0,36,90) — the logo's own disc navy
- corner radius: **22%** of the icon side
- the "Aɩ" mark is centered and scaled to ~1.16× of its size within an inscribed circle, so it nearly fills the square with a small margin

---

## Design tokens
| Token | Value | Where |
|---|---|---|
| Brand navy (header bar) | `#0f2e7a` | `.course-header` background |
| Logo disc navy | `#00245a` | inside the logo mark + favicon background |
| Gold | `#ffd24a` | "Continue" button, gold ring option, progress fill |
| Soft gold | `#ffe08a` | header subtitle "AI Predicts. You Decide." |
| White | `#ffffff` | logo plate, title |
| Header radius | `22px` | `.course-header` |
| Header padding | `26px 30px` | `.course-header` |
| Logo plate shadow | `0 6px 18px -6px rgba(0,0,0,0.45)` | `.logo-plate` |

### Typography (already in the course; listed for completeness)
- Sans / UI / title: **Plus Jakarta Sans** (weights 400–800)
- Title italic span "Than the Tool": **Libre Baskerville**, italic, weight 400
- Title `.course-title-main`: 800, ~31–34px, letter-spacing −0.035em, color #fff
- Subtitle `.course-title-subtitle`: 500, ~16–17px, color #ffe08a

## Assets
- `assets/logo-disc.png` — circular navy disc mark with transparent corners (for the header plate / ring / tile). Cleaned and cropped from the client's supplied logo JPEG.
- `assets/logo-lockup.png` — full "Aɪ Leadership Society" lockup on white (header/footer/print, NOT the favicon).
- `assets/favicon-*.png`, `apple-touch-icon.png`, `icon-512.png` — final favicon set (app-tile badge).
- Source artwork was a client-supplied logo image; the disc was background-removed and re-cropped programmatically. No external/licensed assets.

## Files
- `reference/Header Logo Options.html` — all four header treatments (A–D) on a faithful replica of the real nav, plus the recommended one shown in context with the section tabs.
- `reference/Favicon Preview.html` — circle vs app-tile favicon compared in real dark/light Chrome tabs, with a size ramp.
- Target file in the repo: `index.html` (the course is a single large HTML file; header is built with `React.createElement` under the `.course-header` / `.course-topbar` classes).
