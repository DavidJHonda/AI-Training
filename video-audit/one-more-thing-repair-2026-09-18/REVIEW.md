# One More Thing v5 — current boards + canonical close (visual-only retrofit, 2026-09-18)

Status: **SHIPPED 2026-09-18** on David's approval ("ship it"): v5 copied to `course-assets/one-more-thing/one-more-thing.mp4` (SHA-256 verified before and after the copy, `062049ad…`), the v5 candidate removed, `index.html` video src given cache key `?v=20260918ship1`, `course-assets/manifest.json` entry updated. See `shipping-receipt.json`.

- Candidate (now live): `Prompts/one-more-thing-v5.mp4`, 3:36.73, 6502 frames at 30 fps (same as live).
- SHA-256: see `edit-manifest.json` → `render_sha256`.
- Base: the shipped v4 (`course-assets/one-more-thing/one-more-thing.mp4`, sha `8ab2b181…`, the 2026-09-09 "engaging visuals" build), taken as the picture source because the raw roll (`Prompts/one-more-thing-2.mp4`) no longer exists. Same shape as the Vector Space v5 and How AI Answers v6 retrofits.
- Build: `.video-venv/bin/python scripts/video/build_one_more_thing_v5_retrofit.py` (`--prepare-only` = states, sheets, close, manifest). The shipped v4 edit manifest recovered from git is beside it as `shipped-v4-edit-manifest.json`; the build asserts its 37-state schedule matches it frame for frame.
- Audio: the shipped AAC stream muxed back with `-c:a copy`. Verified byte-identical (stream sha `09cc564a…` on both files). Nothing to audition.

## What changed

All three boards changed since the 2026-09-09 ship, each by the website credit line only, at the same pixel dimensions (draws 1600×910, temperature 1600×1033, bill 1600×890). Every shipped ring rect was drawn on the current files and frames its component exactly, so the event list is used verbatim.

| Span (output frames) | Picture |
|---|---|
| 0–1034 | Notebook opening and dog-prompt animation (shipped picture) |
| 1034–2977 | Same Probabilities, Different Choices: 17 ring states at the shipped onsets (answer so far, list, Spot 22 %, banner, five tries one by one, other choices…), pause held |
| 2977–3227 | Notebook temperature dial (shipped picture) |
| 3227–4502 | How Temperature Changes the Odds: 6 ring states (Starting vs Low, Spot comparison, High, Other row, banner), pause held |
| 4502–5110 | Notebook weights and computation animation (shipped picture) |
| 5110–6262 | The Math Adds Up Fast: One Token (blue), A Short Answer (purple), A Longer Conversation (teal), join and pause held |
| 6262–6502 | Canonical close `one-more-thing-close.jpg` via `make_close_board.py --lesson inference`; 48-frame hold, 150-frame push to 1.2×, settled hold |

Treatment is the shipped one: static board canvases (1220×680 fit on the `#f6f5fb` stage) with 5 px outline rings in the locked accents (purple `#4f2fc4`, blue `#1652f0`, red `#c41f28`, teal `#0e8f86`; neutral titles/banners `#6e51ff`). No camera moves, as shipped.

## Checks

- Decoded frames 6502 = live; close starts at 6262 as shipped.
- Frame-by-frame vs live: Notebook spans mean |diff| 2.7 (re-encode at crf 17 only); probability and temperature boards 0.3; math board 2.8 (title banner styling); close 8.6 (canonical board replaces the archived capture).
- `transition_guard.py`: 10 boundaries, 0 failures. Strips inspected: every first frame after a boundary is the destination shot; pauses hold the board with its current ring; the close is the literal final frame.
- All 37 ring states inspected (`states-sheet-*.jpg`): complete component inside each ring.
- Protected files (live video, lesson, close JPG, three boards) unchanged through the render.

## Still open

- (done) David approved 2026-09-18.
- (done) shipped 2026-09-18; see above.
