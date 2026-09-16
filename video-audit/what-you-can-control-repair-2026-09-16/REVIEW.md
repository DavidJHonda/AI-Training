# What You Can Control v3: SHIPPED 2026-09-16 (board refresh, narrow visual repair)

**Candidate:** `Prompts/what-you-can-control-v3.mp4` (3:03.60, 5508 frames, 30 fps). **Scope:** narrow visual repair of the shipped v2
(`course-assets/what-you-can-control/what-you-can-control.mp4`, sha256 f6ccc2f3738f18d8…): both course boards are replaced by the current
course-assets versions, which carry the site URL at the bottom. Same pixel dimensions as the boards v2 used (1600x1340 and 1600x948),
so every row rectangle, card rectangle, and ring onset is unchanged. The close uses the current canonical closing JPG. No narration,
pause, or timing change. **Shipped 2026-09-16** as `course-assets/what-you-can-control/what-you-can-control.mp4` (cache key 20260916ship1); the v3 candidate removed from Prompts/. **Build:** `scripts/video/build_what_you_can_control_2_review.py` (the v2 assembly
re-run with the new boards, `tall_margin` off for v2-parity framing). **Manifest:** `edit-manifest.json` here.

## Sources (hash-verified before and after the render)

- Base roll `Prompts/what-you-can-control-1.mp4`; graft roll `Prompts/what-you-can-control-2.mp4` (the power/planet/trust line, as in v2).
- Boards (`course-assets/what-you-can-control/`): `what-you-can-control-in-your-hands.jpg` (d012614234…; v2 used 57d52f563e…),
  `what-you-can-control-three-choices.jpg` (593b4f81aa…; v2 used 4f855e742f…).
- Close: `what-you-can-control-close.jpg` (bd2ea0eb33…, 1686x597; bottom rows are the sticky's shadow fading to white, no hairline)
  via `make_close_board.py --lesson control`.

## What changed against the live v2 (frame diff, every 10th frame)

- Board spans: the URL line at the bottom edge only; mean per-pixel difference under 0.8.
- Output 5050–5507 (the close): the canonical closing JPG on a white stage at the house pill size, where v2 had the legacy rendered pill
  on the lavender stage.
- Everywhere else re-encode noise only. Audio stream MD5 identical to v2 (a5553376a993f263a7739c38decd975b); duration and frame count identical.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 5508 = plan = v2; audio 183.616 s; each leg decoded its span exactly.
2. `transition_guard.py`: the three visual boundaries (1059, 3504, 5046) pass; `boundary-pairs.jpg` inspected. The two audio-only graft
   seams (393, 768) report "possible stale visual" because the picture is roll 1's continuous drawing across them by design (as in v2).
3. No pause edits (audio untouched).
4. Ring states inspected (`states-1-hands.jpg`, `states-2-three-moves.jpg`): the ten row rings, the three card rings, and both banner rings
   as v2; the URL line sits under each banner, clear of the banner ring.
5. Density (both compact, still) and full-view opens unchanged from v2.
6. Not auditioned by ear: nothing new to hear; the audio is bit-identical to the shipped file.
7. Nothing left undone in scope.

**At ship:** move to `course-assets/what-you-can-control/what-you-can-control.mp4`, new cache key on the `control` entry (currently
`20260914ship1`), duration pill unchanged (3 min).
