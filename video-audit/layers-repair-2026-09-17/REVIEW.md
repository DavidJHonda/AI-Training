# Layers v5: candidate 2026-09-17 (board refresh, visual-only retrofit of v4)

**Candidate:** `Prompts/layers-v5.mp4` (2:38.90, 4767 frames, 30 fps, sha256 6c2d3ca62d10…). **Scope** (David: "run the same process with
Layers"): narrow visual repair of the shipped v4 (`course-assets/layers/layers.mp4`). The three course boards the video carries are
re-rendered from the current course-assets JPGs (`layers-horse-three-reads.jpg` 0311987d…, `layers-inside-layer.jpg` 7333020c…,
`layers-resolves-it.jpg` 9d75b63a…; same dimensions as the renders v4 used; the site credit line is the difference, plus the
2026-09-15 title-banner standardization on How Layers Update the Numbers, which left every ring target where it was), and the close is
the canonical closing JPG (`layers-close.jpg`, 1404x600) through `make_close_board.py --lesson layers` on the house white stage at the
house pill width (56% at the hold, 67% after the push; the live v4 close sat on the lavender stage at the same sizes). **Source
limitation, disclosed:** the rolls behind v4 and its audit folder (the generated tracing illustration, the composed close) no longer
exist, so the build takes the finished v4 as its picture source and muxes v4's audio stream back in untouched (`-c:a copy`). Outside the
changed spans the picture is one more encoding generation of v4 (mean per-pixel difference about 3, visually identical). **Build:**
`scripts/video/build_layers_v5_retrofit.py`. **Manifest:** `edit-manifest.json` here.

## What was reproduced

v4's schedule (`build_layers_v4.py`, 2026-09-10) verbatim on the current files: the edit timeline (roll 1 with two roll-2 donor spans
whose visual holds and maps drive the IT board's stage rings), the events, static full views (board fit to 1230x670), and the same
rings at the same frames. Spans on the output timeline: The Horse Raced Past the Barn Fell 223-766, How Layers Update the Numbers
1043-1830, How AI Connects IT to CAT 2337-3071, close from 4511. Every Notebook span, both roll-2 picture spans, and the generated
tracing illustration (2306-2337) are v4's picture. The page's fourth board, Why Dozens, was not in v4 (the layer-count narration,
3315-4481, runs over Notebook's own layer-stack drawings, not a rendering of the board), so it is not added here. No dives in v4, so
there are no framing cuts to turn into glides.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 4767 = plan = v4; duration 2:38.90 = v4; audio stream MD5 identical to v4 (ffb26e0857b2affab1c3f913096249dc).
2. `transition_guard.py` passed all 7 declared boundaries (223, 766, 1043, 1830, 2337, 3071, 4511); every strip inspected
   (`guard/`, `guard-sheet.jpg`): one cut per boundary, destination on the first frame.
3. No pause or audio edits.
4. Every ring state compared side by side with the live frame at the same output frame (`live-vs-new-0..2.jpg`), plus the close:
   every ring and camera position matches; the credit line is the only board difference. Frame diff, every 10th frame: only the close
   span (4520-4760, white stage vs lavender) exceeds re-encode noise.
5. Board treatment as v4 (approved 2026-09-10).
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope. **Pre-existing, outside scope (Edit Spec 8c, owner rule 2026-09-13, three days after v4 shipped):**
   two of v4's kept Notebook spans are photographs: a finger on a printed page under "rereading" (about 0:25-0:29, from output frame
   766) and an open book under "book rereading" (about 1:01-1:17, from 1830). A board refresh does not authorize replacing them; they
   are reported here for a separate decision.

**At ship:** copy to `course-assets/layers/layers.mp4`, new cache key on the `layers` entry (currently `20260910repair1`), duration pill
unchanged (3 min), refresh the manifest `video_assets` hash and size, remove the candidate from `Prompts/`.
