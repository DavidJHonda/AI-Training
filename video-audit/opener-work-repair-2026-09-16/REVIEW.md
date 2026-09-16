# Work With AI opener v6: review candidate (2026-09-16, the approved v5 assembly on the current boards)

**Candidate:** `Prompts/work-with-ai-opener-v6.mp4` (2:44.87, 4946 frames, 30 fps). **Scope:** the v5 candidate of 2026-09-14
(`video-audit/opener-work-repair-2026-09-14b/REVIEW.md`: roll 4 base, three approved cuts, the two donor closing lines) rebuilt from the
same pristine sources with the current course-assets boards and the canonical closing JPG. No narration, pause, or timing change.
**The live video is still the July file** (`course-assets/work-with-ai-opener/work-with-ai-opener.mp4`, sha256 f78a30541f917913…, 2:10);
v5 was never shipped, so this candidate replaces it. **Build:** `scripts/video/build_opener_work_4_review.py`. **Manifest:** `edit-manifest.json` here.

## Sources (hash-verified before and after the render)

- Base roll `Prompts/opener-work-4.mp4`; donor `Prompts/close-opener-work.mp4` (+1.0 dB), as in v5.
- Boards (`course-assets/work-with-ai-opener/`): `work-with-ai-opener-refrain.jpg` (9df6596f7d…, byte-identical to v5's),
  `work-with-ai-opener-same-tool.jpg` (4ffd451900…, byte-identical to v5's), `work-with-ai-opener-section-map.jpg` (77bb37bd52…, 1600x871;
  v5 used c440e26823…: the new render left-aligns the title and widens the gold banner to the board's edges; the three row panels and
  every text row measured identical, so the row rings are v5's and the banner ring, detected from the gold, follows the wider banner).
- Close: `work-with-ai-opener-close.jpg` (12fc5b06df…, 1302x597, bottom rows clean) via `make_close_board.py --lesson openerworkwith`.

## What changed against the v5 candidate (frame diff, every 10th frame, v5 restored from commit 30a9072)

- Section map legs: the title's position and the banner's width; mean per-pixel difference under 1.8.
- Output 4600–4945 (the close): the canonical closing JPG on a white stage at the house pill size, where v5 had the legacy rendered pill.
- Everywhere else re-encode noise only. Audio stream MD5 identical to v5 (ab7114a119407125f069f791167b41ea); duration and frame count identical.

## Verification (Edit Spec section 10)

1. Decoded frames 4946 = plan = v5; audio 164.885 s; each leg decoded its span exactly.
2. `transition_guard.py` passed all 11 declared boundaries (577, 794, 1410, 1779, 2027, 2841, 3213, 3698, 4074, 4423, 4623); `boundary-pairs.jpg` inspected.
3. No pause edits; the v5 pauses stand (v5 review, item 3).
4. Ring states inspected (`states-refrain.jpg`, `states-map-1..4.jpg`): the refrain line rings, the three row rings, and the banner ring edge
   to edge on the wider banner; Same Tool walk keyframes as v5.
5. Density and full-view opens as v5.
6. Not auditioned by ear: nothing new to hear; the audio is bit-identical to v5. v5's own listening list still applies if unheard: 24.5–27
   (the first cut), 134.5–136.5 (the verify cut), 152–161 (the donor's two lines), 0–17 (the paraphrased refrain over the board).
7. Nothing left undone in scope.

**At ship:** move to `course-assets/work-with-ai-opener/work-with-ai-opener.mp4`, new cache key on the `openerworkwith` entry (currently `?v=2`),
duration pill 2 min → 3 min (2:45).
