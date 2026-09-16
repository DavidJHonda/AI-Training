# What Is AI? v4: board refresh candidate (2026-09-16, narrow visual repair)

**Candidate:** `Prompts/what-is-ai-v4.mp4` (3:01.00, 5430 frames, 30 fps). **Scope:** narrow visual repair of the shipped v3
(`course-assets/what-is-ai/what-is-ai.mp4`, sha256 7ce725b5c60bb686…): the two course boards that got new versions, Two Ways You
Already Use AI and One Picks. One Creates., are replaced by the current course-assets versions, which carry the site URL at the bottom.
Same pixel dimensions as the boards v3 used (1600x1302 and 1600x1550), so every card rectangle, section rectangle, and ring onset is
unchanged. Ask the Desk is byte-identical to v3's. The close uses the current canonical closing JPG. No narration, pause, or timing
change. **Live video unchanged.** **Build:** `scripts/video/build_what_is_ai_3_review.py` (the v3 assembly re-run with the new boards,
`tall_margin` off for v3-parity framing). **Manifest:** `edit-manifest.json` here.

## Sources (hash-verified before and after the render)

- Base roll `Prompts/what-is-ai-1.mp4` (no grafts, no donors).
- Boards: `course-assets/what-is-ai/what-is-ai-types.jpg` (840212b1e5…, 1600x1302, URL line; v3 used 52e16011ff…),
  `what-is-ai-same-goal.jpg` (8e8c3401ea…, 1600x1550, URL line; v3 used e9e5694ad9…), `what-is-ai-ask-the-desk.jpg` (905c385909…, unchanged).
- Close: `course-assets/what-is-ai/what-is-ai-close.jpg` (ba151205b7…, 1464x597, bottom rows pure white) via `make_close_board.py --lesson llms`.

## What changed against the live v3 (frame diff, every 10th frame)

- Board spans 2079–3744 (both boards): the URL line at the bottom edge only; mean per-pixel difference under 0.5.
- Output 5080–5429 (the close): the canonical closing JPG on a white stage at the house pill size, where v3 had the legacy rendered pill
  on the lavender stage.
- Everywhere else re-encode noise only. Audio stream MD5 identical to v3 (1722112ab7ba39d2b4e0a2f85f54c375); duration and frame count identical.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 5430 = plan = v3; audio 181.013 s; each leg decoded its span exactly.
2. `transition_guard.py` passed all 5 declared boundaries (370, 574, 2079, 3744, 5073); `boundary-pairs.jpg` inspected.
3. No pause edits (audio untouched).
4. Ring states inspected (`states-types.jpg`, `states-picks.jpg`): same section rings, colors, and onsets as v3; the URL line sits
   under the banner, clear of the banner ring.
5. Density (all compact, still) and full-view opens unchanged from v3.
6. Not auditioned by ear: nothing new to hear; the audio is bit-identical to the shipped file.
7. Nothing left undone in scope.

**At ship:** move to `course-assets/what-is-ai/what-is-ai.mp4`, new cache key on the `llms` entry (currently `20260913ship1`), duration
pill unchanged (4 min).
