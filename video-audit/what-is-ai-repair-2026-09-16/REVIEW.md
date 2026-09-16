# What Is AI? v5: SHIPPED 2026-09-16 (board refresh, one approved cut)

**Candidate:** `Prompts/what-is-ai-v5.mp4` (2:56.6, 5298 frames, 30 fps). v5 = v4 plus David's two notes (2026-09-16): (1) output
0:56–1:01 cut = source 54.8–59.2, "To use it well, we need to understand the different ways this tool is applied." (troughs 54.62–54.94
/ 59.0–59.4); the existing pause now sits between "…that once required a person." and "Different AI systems are built for different
jobs."; the picture after the pause starts on Notebook's own cut to its number-2 drawing (source 1784), so none of the cut sentence's
scene shows (seam frames inspected: the pyramids-laptop drawing holds through the pause, then the number-2 drawing); (2) the THE JOB
rings on the Two Ways board cut through their label (ring top 640 vs label rows 642–656); top raised to 622 on both cards. v4 superseded.
**Scope of v4:** narrow visual repair of the shipped v3
(`course-assets/what-is-ai/what-is-ai.mp4`, sha256 7ce725b5c60bb686…): the two course boards that got new versions, Two Ways You
Already Use AI and One Picks. One Creates., are replaced by the current course-assets versions, which carry the site URL at the bottom.
Same pixel dimensions as the boards v3 used (1600x1302 and 1600x1550), so every card rectangle, section rectangle, and ring onset is
unchanged. Ask the Desk is byte-identical to v3's. The close uses the current canonical closing JPG. No narration, pause, or timing
change beyond the one cut above. **Shipped 2026-09-16** as `course-assets/what-is-ai/what-is-ai.mp4` (cache key 20260916ship1, pill 3 min); the v5 candidate removed from Prompts/. **Build:** `scripts/video/build_what_is_ai_3_review.py` (the v3 assembly re-run with the new boards,
`tall_margin` off for v3-parity framing). **Manifest:** `edit-manifest.json` here.

## Sources (hash-verified before and after the render)

- Base roll `Prompts/what-is-ai-1.mp4` (no grafts, no donors).
- Boards: `course-assets/what-is-ai/what-is-ai-types.jpg` (840212b1e5…, 1600x1302, URL line; v3 used 52e16011ff…),
  `what-is-ai-same-goal.jpg` (8e8c3401ea…, 1600x1550, URL line; v3 used e9e5694ad9…), `what-is-ai-ask-the-desk.jpg` (905c385909…, unchanged).
- Close: `course-assets/what-is-ai/what-is-ai-close.jpg` (ba151205b7…, 1464x597, bottom rows pure white) via `make_close_board.py --lesson llms`.

## What changed against the live v3 (frame diff of v4, every 10th frame; v5 adds the cut and the ring fix)

- Board spans 2079–3744 (both boards): the URL line at the bottom edge only; mean per-pixel difference under 0.5.
- Output 5080–5429 (the close): the canonical closing JPG on a white stage at the house pill size, where v3 had the legacy rendered pill
  on the lavender stage.
- Everywhere else re-encode noise only. Audio stream MD5 identical to v3 (1722112ab7ba39d2b4e0a2f85f54c375); duration and frame count identical.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 5298 = plan (v3 5430 minus the 132-frame cut); audio 176.619 s; each leg decoded its span exactly.
2. `transition_guard.py` passed all 6 declared boundaries (370, 574, 1704, 1947, 3612, 4941); `boundary-pairs.jpg` inspected: 1704 is
   Notebook's number-2 drawing on its own first frame, no stale scene tail.
3. Pauses on the final file (silencedetect −35 dB): 21.26–22.73, 55.58–57.02 (the cut's seam), 118.93–120.45, 163.31–164.89; close hold
   171.71–176.62. The join re-transcribed: "…tasks that once required a person." 55.00 → pause → "Different AI systems are built for
   different jobs." 57.00; floor −73 dB in the gap, no cliff.
4. Ring states inspected (`states-types.jpg`, `states-picks.jpg`): the THE JOB rings now clear their labels on both cards
   (`state-types-0178.jpg`, `state-types-0755.jpg`); every other ring, color, and onset as v3; the URL line sits under the banner, clear of
   the banner ring.
5. Density (all compact, still) and full-view opens unchanged from v3.
6. Not auditioned by ear: David should listen to 0:54–0:58 (the cut's seam).
7. Nothing left undone in scope.

**At ship:** move to `course-assets/what-is-ai/what-is-ai.mp4`, new cache key on the `llms` entry (currently `20260913ship1`), duration
pill: 2:57 → 3 min.
