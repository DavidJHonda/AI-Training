# Work With AI opener v7: SHIPPED 2026-09-16 (the approved v5 assembly on the current boards, one more cut)

**Candidate:** `Prompts/work-with-ai-opener-v7.mp4` (2:37.90, 4737 frames, 30 fps). v7 = v6 plus a fourth cut approved by David
2026-09-16: source 95.25–102.23, "If you skip this phase, you risk using the wrong tool for the job, which leads to frustration before
the work even begins." (invented by roll 4; troughs 95.08–95.44 / 101.84–102.22). Notebook's tool-mismatch sketch, drawn for that
line, goes with it; the picture runs from the tool-selection sketch straight to the section map arriving at "Once you have the right
tool" on Notebook's own cut, as before. The join re-transcribed on the finished file: "…how its specific interface works." 86.74 →
"Once you have the right tool, we move to step two…" 87.80, floor −59 dB in the gap, no pause inserted. v6 superseded. **Scope of v6:** the v5 candidate of 2026-09-14
(`video-audit/opener-work-repair-2026-09-14b/REVIEW.md`: roll 4 base, three approved cuts, the two donor closing lines) rebuilt from the
same pristine sources with the current course-assets boards and the canonical closing JPG. No pause or timing change beyond the cut above.
**Shipped 2026-09-16** as `course-assets/work-with-ai-opener/work-with-ai-opener.mp4` (cache key 20260916ship1, pill 3 min); the July file it replaced was (`course-assets/work-with-ai-opener/work-with-ai-opener.mp4`, sha256 f78a30541f917913…, 2:10);
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
- Everywhere else re-encode noise only (measured on v6; v7 then removes 209 frames at the cut).

## Verification (Edit Spec section 10)

1. Decoded frames 4737 = plan (v5's 4946 minus the 209-frame cut); audio 157.909 s; each leg decoded its span exactly.
2. `transition_guard.py` passed all 11 declared boundaries (577, 794, 1410, 1779, 2027, 2632, 3004, 3489, 3865, 4214, 4414); `boundary-pairs.jpg`
   inspected: at 2632 the tool-selection sketch cuts to the section map's first frame, no stale frame.
3. Pauses on the final file (silencedetect −35 dB): 17.86–19.35, 25.32–26.69, 57.84–59.39, 145.97–147.33; close hold 153.73–157.91. The
   new join carries no inserted pause.
4. Ring states inspected (`states-refrain.jpg`, `states-map-1..4.jpg`): the refrain line rings, the three row rings, and the banner ring edge
   to edge on the wider banner; Same Tool walk keyframes as v5.
5. Density and full-view opens as v5.
6. Not auditioned by ear: David should listen to 1:26–1:29 (the new cut). v5's own list still applies if unheard: 24.5–27 (the first
   cut), 2:07–2:09 (the verify cut), 2:25–2:34 (the donor's two lines), 0–17 (the paraphrased refrain over the board).
7. Nothing left undone in scope.

**At ship:** move to `course-assets/work-with-ai-opener/work-with-ai-opener.mp4`, new cache key on the `openerworkwith` entry (currently `?v=2`),
duration pill 2 min → 3 min (2:38).
