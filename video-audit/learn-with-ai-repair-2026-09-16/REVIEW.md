# Learn with AI v6: board refresh candidate (2026-09-16, narrow visual repair)

**Candidate:** `Prompts/learn-with-ai-v6.mp4` (3:40.43, 6613 frames, 30 fps). **Scope:** narrow visual repair of the shipped v5
(`course-assets/learn-with-ai/learn-with-ai.mp4`, sha256 9cdc8d5fd87d6190…): the three course boards are replaced by the current course-assets
versions, which carry the site URL at the bottom, and the close by the canonical closing JPG. Same pixel dimensions as the boards v5 used
(1600x1345, 1600x844, 1600x1507), so every card rect, section rect, dive window, and ring onset is unchanged. No narration, pause, or
timing change. **Live video unchanged.** **Build:** `scripts/video/build_learn_with_ai_2_review.py` (the v5 assembly re-run from the pristine
rolls with the new boards, `tall_margin` off for v5-parity framing). **Manifest:** `edit-manifest.json` here.

## Sources (hash-verified before and after the render)

- Base roll `Prompts/learn-with-ai-1.mp4`; graft roll `Prompts/learn-with-ai-2.mp4` (the Focus list, the takeaway line, and move two, as in v5).
- Boards (`course-assets/learn-with-ai/`): `learn-with-ai-study-toolkit.jpg` (bb9152c9ee…; v5 used 3712c4ea82…), `learn-with-ai-how-it-works.jpg`
  (72a3b9b6ae…; v5 7b1e44a5a2…), `learn-with-ai-four-moves.jpg` (256ee9be3c…; v5 35476258d1…).
- Close: `learn-with-ai-close.jpg` (a897830ab0…, 1578x600, regenerated 2026-09-16, bottom rows clean) via `make_close_board.py --lesson studying`.

## What changed against the live v5 (frame diff, every 10th frame)

- Board spans: the URL line at the bottom edge only (largest on the Four Moves full views, output 4740–4830); mean per-pixel difference
  under 1.6 elsewhere in the board spans.
- Output 6330–6612 (the close): the canonical closing JPG on a white stage at the house pill size, where v5 had the legacy rendered pill on
  the lavender stage.
- Everywhere else re-encode noise only. Audio stream MD5 identical to v5 (0b3ec7cd91266bb429f37849ee6d0390); duration and frame count identical.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 6613 = plan = v5; audio 220.437 s; each leg decoded its span exactly.
2. `transition_guard.py`: 12 of 13 declared boundaries pass; the one flag (5130) is the start of the roll 2 move-two audio graft, where the
   Four Moves board is mid-pan from move one to move two by design (the dive follows the spoken onset); the strip shows the pan, not a
   splice, as in v5. `boundary-pairs.jpg` inspected.
3. No pause edits (audio untouched).
4. Ring states inspected (`states-1-study-tools.jpg`, `states-1-study-tools-b.jpg`, `states-2-how-it-works.jpg`, `states-3-four-moves.jpg`):
   section rings, card rings, dives, pull-back, and banners as v5; the URL line sits under each banner, clear of the banner ring.
5. Density and full-view opens unchanged from v5.
6. Not auditioned by ear: nothing new to hear; the audio is bit-identical to the shipped file.
7. Nothing left undone in scope.

**At ship:** move to `course-assets/learn-with-ai/learn-with-ai.mp4`, new cache key on the `studying` entry (currently `20260914ship2`),
duration pill unchanged (4 min).
