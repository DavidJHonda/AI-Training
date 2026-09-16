# Learn with AI v7: SHIPPED 2026-09-16 (board refresh; Which Study Tool dense)

**Candidate:** `Prompts/learn-with-ai-v7.mp4` (3:40.43, 6613 frames, 30 fps). v7 = v6 with Which Study Tool for the Job? treated as dense
(David: "It's dense enough for us to zoom and pan"): the full board for 3 s, a dive to the complete Focus card as its header rings, the
section rings (what it does, best use, the catch) following the narration inside the dive, a pan to the Exploration card at its header,
its four section rings, and a pull-back to the full board 0.6 s before the grafted takeaway line rings the banner. One leg now carries the
whole board (the roll 1 resume after the Focus graft addresses the leg with `video_from`, a small library addition, so the graft's picture
frames are not reused); v6's two compact legs are gone. v6 superseded. **Scope:** narrow visual repair of the shipped v5
(`course-assets/learn-with-ai/learn-with-ai.mp4`, sha256 9cdc8d5fd87d6190…): the three course boards are replaced by the current course-assets
versions, which carry the site URL at the bottom, and the close by the canonical closing JPG. Same pixel dimensions as the boards v5 used
(1600x1345, 1600x844, 1600x1507); every card rect, section rect, and ring onset is v5's, and the How Gemini Notebook Works and Your Four Moves
treatments are unchanged. No narration, pause, or
timing change. **Shipped 2026-09-16** as `course-assets/learn-with-ai/learn-with-ai.mp4` (cache key 20260916ship1); the v7 candidate removed from Prompts/. **Build:** `scripts/video/build_learn_with_ai_2_review.py` (the v5 assembly re-run from the pristine
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
2. `transition_guard.py` passed all 9 declared visual boundaries (1698, 1806, 3612, 3812, 4481, 4649, 4727, 5322, 6325); `boundary-pairs.jpg`
   inspected. (The audio-only graft seams inside the two board legs are camera moves by design and are not declared as visual cuts.)
3. No pause edits (audio untouched).
4. Ring states inspected (`states-1-study-tools.jpg`: each section ring inside the card dive, the pan to Exploration, the pull-back and
   banner; `states-2-how-it-works.jpg`, `states-3-four-moves.jpg` as v5); a 16-frame strip of the study-tool span inspected on the output. The
   URL line sits under each banner, clear of the banner ring.
5. Which Study Tool dense (new); the other two boards' density and every full-view open as v5.
6. Not auditioned by ear: nothing new to hear; the audio is bit-identical to the shipped file.
7. Nothing left undone in scope.

**At ship:** move to `course-assets/learn-with-ai/learn-with-ai.mp4`, new cache key on the `studying` entry (currently `20260914ship2`),
duration pill unchanged (4 min).
