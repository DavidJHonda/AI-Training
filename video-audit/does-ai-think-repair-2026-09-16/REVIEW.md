# Does AI Think? v4: board refresh candidate (2026-09-16, visual-only retrofit of the shipped v3)

**Candidate:** `Prompts/does-ai-think-v4.mp4` (3:40.00, 6600 frames, 30 fps). **Scope:** narrow visual repair of the shipped v3
(`course-assets/does-ai-think/does-ai-think.mp4`, sha256 e71f1b610fc45e59…): the two course boards are replaced by the current course-assets
versions and the close by the canonical closing JPG. **Source limitation, disclosed:** the raw rolls (`Prompts/does-ai-think-1.mp4`, `-2.mp4`)
no longer exist, so the v3 assembly could not be re-run from pristine sources. This build takes the finished v3 as its picture source,
replaces the board and close spans with new legs, and muxes v3's original audio stream back in untouched. The picture outside the changed
spans is therefore one more encoding generation of v3 (mean per-pixel difference about 2.6, visually identical; frame pairs inspected).
**Live video unchanged.** **Build:** `scripts/video/build_does_ai_think_3_retrofit.py`. **Manifest:** `edit-manifest.json` here.

## Boards and geometry

- **The Chinese Room** is a NEW asset: `does-ai-think-chinese-room.jpg` (6a3159d52a…, 1600x1310, with a title, banner, and URL line); v3
  used the bare 1536x1024 illustration (b6154b3b87…). The illustration sits inside the new board scaled 0.990 x 0.988 at offset (40, 128),
  confirmed by measuring the "To anyone outside" panel at both sizes (v3 [20,743,427,999] → new [60,862,463,1115]). The four step-callout
  rects are v3's mapped through that transform: [60,158,466,410], [60,415,466,627], [60,637,466,850], [60,859,466,1116]. Purple for
  steps 1–3, neutral for "To anyone outside", as v3.
- **When You Think / What AI Does**: `does-ai-think-side-by-side.jpg` (c9ff37bef3…, 1600x1556, URL line); v3 used 8475f2729c… at the same
  size. Text rows and separator rules measured identical, so the five row rects and the banner are v3's.
- **Close:** `does-ai-think-close.jpg` (c49e10885e…, 1434x597, bottom rows are the sticky's shadow) via `make_close_board.py --lesson doesaithink`.
- Spans on the output timeline (v3's cut list, confirmed by frame-difference cut detection on the live file): Chinese Room [1389, 2876),
  comparison [3669, 5847), close from 6312. Ring onsets are v3's roll-2 onsets shifted onto the output timeline (B1 −7.7 s, B2 −5.7 s);
  re-heard on the finished file: "Step one" 57.68, "Step two" 64.20, "When it comes to meaning" 129.90, "The outputs might look" 184.58.
- Framing at v3 parity (`tall_margin` off). Corner cleaning off (v3's Notebook frames were already cleaned).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 6600 = plan = v3; duration 3:40.00 = v3; audio stream MD5 identical to v3 (5f0479ae23637b7f24240f229dfe4e0f).
2. `transition_guard.py` passed all 5 declared boundaries (1389, 2876, 3669, 5847, 6312); `boundary-pairs.jpg` inspected.
3. No pause or audio edits (the audio is v3's stream, copied).
4. Ring states inspected (`states-1-chinese-room.jpg`, `states-2-side-by-side.jpg`): each Chinese Room ring traces its callout on the new
   board; the five row rings and the banner as v3; the URL line under each banner, clear of the banner ring.
5. Density (both compact, still) and full-view opens as v3.
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope. Pre-existing: v3's own narration and drawings are unchanged.

**At ship:** move to `course-assets/does-ai-think/does-ai-think.mp4`, new cache key on the `doesaithink` entry (currently `20260913ship1`),
duration pill unchanged (3 min).
