# Icon and logo system

This directory is the authoritative production asset set for the course. The live
call sites are in `index.html`; do not infer current usage from old handoff or design
files in Git history.

## Live favicon and app-icon family

The current browser and device treatment is the bold cream-and-gold “Ai” mark on a
navy rounded square. Keep this family visually synchronized when changing it:

| File | Dimensions | Current use |
|---|---:|---|
| `favicon-16x16.png` | 16×16 | Browser tab |
| `favicon-32x32.png` | 32×32 | Browser tab and bookmarks |
| `favicon-48x48.png` | 48×48 | High-density and legacy browser contexts |
| `apple-touch-icon.png` | 180×180 | Apple touch icon |
| `icon-192.png` | 192×192 | Web-app manifest |
| `icon-512.png` | 512×512 | Web-app manifest |
| `site.webmanifest` | — | App name, icon paths, colors, and display mode |

`index.html` links the three favicon sizes, the Apple touch icon, and the manifest.
The manifest’s icon paths are relative to the manifest itself and therefore do not
begin with `/icons/`. Its theme and background color are the brand navy `#15315a`,
matching the page’s `theme-color` metadata.

## Course logo assets

- `logo-disc.png` is the live circular mark used in the course-header plate and on
  the name gate, including its watermark treatment.
- `logo-lockup.png` is the full AI Leadership Society lockup. It is retained as the
  production brand asset but is not currently rendered by `index.html`.

When changing the favicon family, regenerate and inspect every size together,
especially the 16px result. When changing a logo filename or role, update and verify
all `index.html` call sites. Browsers cache favicons aggressively, so use a hard refresh
or cleared cache during verification.
