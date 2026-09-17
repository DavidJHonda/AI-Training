# Transformer v8: SHIPPED 2026-09-17 (board refresh, visual-only retrofit of v7)

**Candidate:** `Prompts/transformer-v8.mp4` (4:18.30, 7749 frames, 30 fps, sha256 7d5edfa42ae5…). **Scope** (David: "run the same processing on
the Transformer video"): narrow visual repair of the shipped v7 (`course-assets/transformer/transformer.mp4`). The six course boards
are re-rendered from the current course-assets JPGs (`transformer-context-problems.jpg` 76dbe145…, `transformer-before-transformers.jpg`
a1114549…, `transformer-how-transformer-reads.jpg` 895ac201…, `transformer-attention-transformation.jpg` 84d228ef…,
`transformer-resolves-meaning.jpg` ece5c168…, `transformer-word-order.jpg` b6b48422…; same dimensions as the renders v5/v7 carried), and
the close is the canonical closing JPG (`transformer-close.jpg`, 1788x600) through `make_close_board.py --lesson attention` on the house
white stage at the house pill width (56% at the hold, 67% after the push; the live v7 close sat on the lavender stage at 58%/69%).
**Source limitation, disclosed:** the rolls behind v5 and the v5/v6 candidates no longer exist, so the build takes the finished v7 as its
picture source and muxes v7's audio stream back in untouched (`-c:a copy`). Outside the changed spans the picture is one more encoding
generation of v7 (mean per-pixel difference under 5, visually identical). **Build:** `scripts/video/build_transformer_v8_retrofit.py`.
**Manifest:** `edit-manifest.json` here.

## What was reproduced

v7 is v5's approved edit for its first 6339 frames plus the positional-encoding material and the word-order board. Both schedules are
reproduced verbatim on the current files: v5's edit timeline mapping output frames to the rolls' seconds, its board states and rings at
the same frames (every board a static full view, the board fit to 1210x660 on the stage; no dives, so there are no framing cuts to turn
into glides), the owner-requested attention-path overlay on How a Transformer Reads a Sentence (three backward paths from IT, the ring
on CAT from 4 s), and v7's two word-order rings at output frames 7226 and 7393. Spans on the output timeline: Two Problems Context Must
Solve 1128-2105, How Earlier AI Read Text 2815-3305, How a Transformer Reads a Sentence 3628-4413 (paths from 4125), How Context
Changes the Numbers 5115-5805, How the Transformer Resolves Meaning 5805-6369, How a Transformer Keeps Words in Order 7148-7519,
close from 7519. Every Notebook span and the earlier-live positional-encoding span (6369-7148) are v7's picture.

**One ring moved, and only because the board did.** How Earlier AI Read Text was restructured on 2026-09-15 (title-banner
standardization): "We know IT refers to CAT." now sits as plain text above the gold banner instead of inside it. v5's takeaway
rectangle (y 558-695) would have cut through that line, so the takeaway ring is re-anchored to the current banner, measured with
`banner_rect` (y 606-694; ring at 605-695). Every other takeaway ring still traces its banner within a pixel (checked on all six boards).
The site credit line is the only other board difference.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 7749 = plan = v7; duration 4:18.30 = v7; audio stream MD5 identical to v7 (5a4e98a130d779ffa57086dc449200d4).
2. `transition_guard.py` passed all 11 declared boundaries (1128, 2105, 2815, 3305, 3628, 4413, 5115, 5805, 6369, 7148, 7519); every
   strip inspected (`guard/`, `guard-sheet.jpg`): one cut per boundary, destination on the first frame.
3. No pause or audio edits.
4. Every ring state compared side by side with the live frame at the same output frame (`live-vs-new-0..3.jpg`), plus the overlay at
   2/4/7/9 s and the close: every ring, path, and camera position matches. Frame diff, every 10th frame: only the re-anchored takeaway
   span (3140-3300) and the close (white stage vs lavender) exceed re-encode noise. Final decoded checks in `final-checks.jpg`.
5. Board treatment as v5/v7 (approved 2026-09-10).
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope. Noted, not acted on: the two tall boards (Two Problems, 1341 px; Resolves Meaning, 1403 px) are shown
   at full view only, with half-board rings, as v5 approved them; their body text is small at that size if a dive is ever wanted.

**Shipped 2026-09-17** as `course-assets/transformer/transformer.mp4` (cache key 20260917ship1, pill 4 min); candidate removed from `Prompts/`. Ship recipe was: copy to `course-assets/transformer/transformer.mp4`, new cache key on the `attention` entry (currently `20260910repair1`),
duration pill unchanged (4 min), refresh the manifest `video_assets` hash and size, remove the candidate from `Prompts/`.
