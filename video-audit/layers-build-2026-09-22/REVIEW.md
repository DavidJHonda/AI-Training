# Layers v1: review candidate, built 2026-09-22

**Candidate:** `Prompts/layers-v1.mp4` — 3:48.67, 6860 frames, 30 fps, sha256 f4ab7f86b31387a4….
**Base:** `Prompts/layers-2.mp4` (roll 2), which earned KEEP in `video-audit/layers-comparison-2026-09-22/REVIEW.md`.
**Scope:** full production pass, picture only. The narration ships **uncut and ungrafted** — no cuts, no grafts, no reordering.
Build: `scripts/video/build_layers_v1.py`.

## What was built

Three boards, each replacing Notebook's own rendering at the roll's own visual cut (`scenes.py`):

| Board | Output span | Treatment |
|---|---|---|
| B1 "The Horse Raced Past the Barn Fell" | 146–1519 | Compact, still. Rings: First Read 12.72, More Reads 24.56, Meaning Clicks 36.56, banner 47.60. The three reads are columns inside one shared white box, so each ring runs the **full height of that box** (owner rule, 2026-09-21). |
| B2 How Layers Update the Numbers | 2144–3808 | Full view for the diagram beats — the whole diagram ringed at 73.60, the front layer's Attention/Transformation card at 81.28, both without diving — then a dive to each number card: Starting 97.84, After One Layer 103.44, After Many Layers 107.52, Final 111.84 (held through "the values shift at every layer"), pull back at 121.00 and the banner ringed at 121.92. |
| B3 How AI Connects 'IT' to 'CAT' | 3994–5432 | Compact, still. Rings: the sentence 136.00, START 144.00, LAYER 1 151.76, LAYER 2 160.48, REPEAT 169.28, RESULT 174.40 held through "AI works out that IT refers to CAT". No banner on this board. |

Board 1 holds through 1519 so its banner ring lands on our board rather than on Notebook's check-mark flourish; Board 2 holds
through 3808 so its banner is not spoken over Notebook's own hand-drawn number grid.

**Four pauses of one second**, at idea boundaries: after Board 1 into the pivot (1519), after Board 2 into "follow one word, IT"
(3808), after Board 3 into the scale beat (5432), and before the closing message (6518). **No pause after the horse sentence** —
roll 2 speaks its own 0.63 s beat there, which is what David asked for at v6. Standard close from Notebook's own close cut
(source 6428), canonical `layers-close.jpg`.

## Verification

1. Decoded 6860 frames at 30 fps, 3:48.67, matching the prepared plan exactly.
2. `transition_guard.py` on all twelve declared boundaries: **PASS, none failed**.
3. Pause audit (`silencedetect -35 dB`, ≥1 s): four gaps, at 50.31, 126.24, 180.70 and 217.26 — the four planned boundaries and
   no others. The roll's own 0.63 s beat after the horse sentence is untouched and below this threshold, as intended.
4. Corner mark: 1,366 frames cloned, 587 inpainted, **0 declined**.
5. Protected files unchanged (roll 2, the live `layers.mp4`, `lessons/layers.md`, all three board JPGs).
6. Board states inspected on every ring and camera state (`states-*.jpg`): correct component ringed in each, the number cards
   large and readable at their dives, board text readable at full view, nothing clipped at a frame edge.
7. The canonical close is the literal final frame, carrying both closing lines (`check-last-frame.jpg`).
8. **Stock-photograph sweep, whole file** (the v5/v6 reviews found two photograph spans in the old roll): 458 samples at every
   15th frame, none below the paper-background threshold; and of the Notebook-sourced frames ranked most photo-like, the top
   eight are all hand-drawn — the layer-stack sketch and the data-centre drawing around 3:35–3:37 (`photo-sweep` contact sheet
   inspected). No stock photograph in this roll.

## Not done / for David

- **Not watched end to end by me, and not auditioned by ear.**
- **Two page changes belong with the ship:** the pill goes **3 min → 4 min** (3:48.67 against the live 2:39.90), and
  `LESSON_VIDEOS.layers.title` still reads "Meaning builds up, layer by layer — and one box stays blank." David resolved on
  2026-09-21 that the cliffhanger is retired; the proposal is **"Meaning builds up, layer by layer."**
- Nothing has been shipped. The live `course-assets/layers/layers.mp4` and `index.html` are untouched.
