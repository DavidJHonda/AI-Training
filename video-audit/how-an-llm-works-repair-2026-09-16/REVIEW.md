# How an LLM Works v5: board refresh candidate (2026-09-16, narrow visual repair)

**Candidate:** `Prompts/how-an-llm-works-v5.mp4` (4:22.70, 7881 frames, 30 fps). **Scope:** narrow visual repair of the shipped v4
(`course-assets/how-an-llm-works/how-an-llm-works.mp4`, sha256 6e307af634624fab…): all four course boards are replaced by the current
course-assets versions, which carry the site URL at the bottom. Same pixel dimensions as the boards v4 used (1600x856, 1600x868,
1600x1012, 1600x1032), so every card rectangle, step rectangle, and ring onset is unchanged. The close uses the current canonical closing
JPG. No narration, pause, or timing change. **Live video unchanged.** **Build:** `scripts/video/build_how_an_llm_works_2_review.py`
(the v4 assembly re-run with the new boards, `tall_margin` off for v4-parity framing of the two tall boards). **Manifest:** `edit-manifest.json` here.

## Sources (hash-verified before and after the render)

- Base roll `Prompts/how-an-llm-works-2.mp4`; graft roll `Prompts/how-an-llm-works-1.mp4` (the "Over billions of examples…" line, as in v4).
- Boards (`course-assets/how-an-llm-works/`): `how-an-llm-works-llm.jpg` (61fc5bbdd1…; v4 used 17ff30c4fe…), `-learn-once.jpg`
  (5587e85f43…; v4 283c0e345b…), `-training.jpg` (b4b05b41f6…; v4 0e1279fa41…), `-patterns.jpg` (83cc11b5f6…; v4 b58c1be8cc…).
- Close: `how-an-llm-works-close.jpg` (e527b3cb4d…, 1854x597; its bottom rows are the sticky's soft shadow fading to white, no hairline)
  via `make_close_board.py --lesson aihistory`.

## What changed against the live v4 (frame diff, every 10th frame)

- Board spans: the URL line at the bottom edge only; mean per-pixel difference under 0.7.
- Output 7580–7880 (the close): the canonical closing JPG on a white stage at the house pill size, where v4 had the legacy rendered pill
  on the lavender stage.
- Everywhere else re-encode noise only. Audio stream MD5 identical to v4 (355fa4b3a35151c4927b9ae0634b9448); duration and frame count identical.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 7881 = plan = v4; audio 262.72 s; each leg decoded its span exactly.
2. `transition_guard.py` passed all 7 declared boundaries (1126, 1438, 2598, 3963, 4596, 4948, 7575); `boundary-pairs.jpg` inspected.
3. No pause edits (audio untouched).
4. Ring states inspected (`states-1-llm.jpg`, `states-2-learn-once.jpg`, `states-3-training.jpg`, `states-4-patterns.jpg`): same rings,
   colors, and onsets as v4; the URL line sits under each banner, clear of the banner ring.
5. Density (all compact) and full-view opens unchanged from v4.
6. Not auditioned by ear: nothing new to hear; the audio is bit-identical to the shipped file.
7. Nothing left undone in scope.

**At ship:** move to `course-assets/how-an-llm-works/how-an-llm-works.mp4`, new cache key on the `aihistory` entry (currently
`20260913ship1`), duration pill unchanged (4 min).
