# How AI Answers v6 — current boards + canonical close (visual-only retrofit, 2026-09-18)

Status: **SHIPPED 2026-09-18** on David's approval ("ship it"): v6 copied to `course-assets/how-ai-answers/how-ai-answers.mp4` (SHA-256 verified before and after the copy, `1d0216b5…`), the v6 candidate removed, `index.html` cache key bumped to `?v=20260918ship1`, `course-assets/manifest.json` entry updated. See `shipping-receipt.json`.

- Candidate (now live): `Prompts/how-ai-answers-v6.mp4`, 3:02.77, 5483 frames at 30 fps (same as live).
- SHA-256: see `edit-manifest.json` → `render_sha256`.
- Base: the shipped v5 (`course-assets/how-ai-answers/how-ai-answers.mp4`, sha `bca9561e…`), taken as the picture source because the raw roll (`Prompts/how-ai-answers.mp4`) no longer exists. Same shape as the Vector Space v5 retrofit of 2026-09-17.
- Build: `.video-venv/bin/python scripts/video/build_how_ai_answers_v6_retrofit.py` (`--prepare-only` = legs, state sheets, close, manifest).
- Audio: the shipped AAC stream muxed back with `-c:a copy`. Verified byte-identical (stream sha `4efd923b…` on both files). Nothing to audition.

## What changed

Every board JPG changed since the 2026-09-10 ship. Boards 1–3 changed only by the website credit line (their card and banner rects detect at the shipped coordinates to the pixel; B2's second card is 2 px different). Board 4 is a new layout: four bordered cards under "YOU ASK" / "ANSWER SO FAR" (1600×1000), replacing the photo strip (1600×1432).

| Board | Output span | Density | Treatment (unchanged from the ship) |
|---|---|---|---|
| B1 Before the Answer Begins | 400–1435, held through the pause, 1465–1472 | dense | dive Tokens 0:16 · Positions 0:21 · Starting Vectors 0:26 · Through Layers 0:32; pull back 0:39; banner ring 0:43 |
| B2 Why the Final Token Matters | 1472–2487, held, 2517–2527 | compact | ring The Question 0:58 · The Final Token 1:05 · banner 1:14 |
| B3a The Answer, Token by Token | 2527–3864 | dense | dive Prediction 1 1:30 · Three more predictions 1:41 · Prediction 5 1:47 |
| Notebook loop diagram | 3864–4134 | kept | shipped picture |
| B3b The Answer, Token by Token | 4134–4438, held, 4468–4479 | compact | banner ring 2:22 |
| B4 Inference: How AI Builds an Answer | 4479–5216, held to 5246 | compact | ring 1 · Rank 2:35 · 2 · Pick 2:38 · 3 · Add 2:40 · 4 · Repeat 2:42 (whole cards, locked accents) · banner 2:46 |
| Close | 5246–5483 | canonical | `how-ai-answers-close.jpg` via `make_close_board.py --lesson prediction`; 48-frame hold, 150-frame push to 1.2×, settled hold |

Accents: purple `#4f2fc4`, blue `#1652f0`, teal `#0e8f86`, green `#0f7a4a` per card title; banners `#6e51ff`. Rings post-crop at 5 px, pad 0, radius 14 (banner 22).

Framing: `tall_margin = False` and the ship-time compact push (0.04·n/900, uncapped) for parity with the 2026-09-10 ship, as Vector Space v5 did. The dense legs follow the current module (static full view before the first dive, owner rule 2026-09-14) where the ship had a 3 % push during the establish. Board 4's new JPG is 16:10, so at parity framing its title sits near the top edge and the credit line at the bottom edge, like B1 and B3 did in the ship; the 4 % stage margin is a one-flag change if wanted.

## Checks

- Decoded frames 5483 = live; every leg decodes its span exactly (1042 / 1025 / 1337 / 315 / 737).
- Notebook spans vs live: mean |diff| 3.1 (re-encode at crf 17 only). Board 2 / 3b spans: 0.5–0.8 (credit line only). Board 4: 86 (new board).
- `transition_guard.py`: 15 boundaries, 0 failures. Strips inspected: every first frame after a boundary is the destination shot; pauses hold the board with its current ring; the close is the literal final frame.
- Settled ring frames inspected (`states-*.jpg`, `state-*.jpg`): complete card inside each ring, arrows and dividers outside, banner rings edge to edge.
- Protected files: the shipped video, the lesson, the close JPG and all four boards unchanged. `index.html` changed during the render (another session shares the checkout); its `prediction` close copy and asset entries are untouched (git diff), which is all this build reads from it.

## Still open

- (done) David approved 2026-09-18.
- (done) shipped 2026-09-18; see above.
