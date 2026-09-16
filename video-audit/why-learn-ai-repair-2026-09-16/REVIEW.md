# Why Learn AI? v6: SHIPPED 2026-09-16 (board refresh, narrow visual repair)

**Candidate:** `Prompts/why-learn-ai-v6.mp4` (3:57.23, 7117 frames, 30 fps). v6 = v5 with the regenerated closing JPG (David, 2026-09-16 09:39; the hairline is gone); v5 superseded, otherwise identical (frame diff v5→v6: nothing outside the close, re-encode noise under 0.3 elsewhere). **Scope:** narrow visual repair of the shipped v4
(`course-assets/why-learn-ai/why-learn-ai.mp4`, sha256 210df1e1ac04c1ed…): the two boards David named, Where AI Already Lives and Why
You'll Thrive in the AI Future, are replaced by the current course-assets versions, which carry the site URL at the bottom. Same
pixel dimensions as the boards v4 used (1600x788 and 1600x958), so every card rectangle, camera window, and ring onset is unchanged.
No narration, pause, or timing change. **Shipped 2026-09-16** as `course-assets/why-learn-ai/why-learn-ai.mp4` (cache key 20260916ship1); v6 candidate removed from Prompts/. **Build:** `scripts/video/build_why_learn_ai_2_review.py` (the v4
assembly re-run from the pristine sources with the new boards). **Manifest:** `edit-manifest.json` here.

## Sources (hash-verified before and after the render)

- Base roll `Prompts/why-learn-ai-2.mp4`; graft roll `Prompts/why-learn-ai-1.mp4` (roll 1's Where AI Already Lives walk, as in v4).
- Drawings donor: the July live video, restored from git into this audit dir as `donor-live-before-2026-09-13.mp4`
  (`git show 13e9d84:videos/why-learn-ai.mp4`, sha256 75f8bb010119d51b…; gitignored, not an archive directory).
- Boards: `course-assets/why-learn-ai/why-learn-ai-everyday.jpg` (13648c4900…, 1600x788, URL line), `why-learn-ai-thrive.jpg`
  (ff2274fc18…, 1600x958, URL line), `why-learn-ai-press.jpg` (43a9730c99…, unchanged from v4).
- Close: `course-assets/why-learn-ai/why-learn-ai-close.jpg` (3266e6541e80…, 1203x597, regenerated 2026-09-16, bottom rows pure white) via `make_close_board.py --lesson whydeeper` (CLOSE_BOARD_ASSETS).

## What changed against the live v4 (frame diff, every 10th frame)

- Output 1150–1280 (Where AI Already Lives at full view, before and at the banner pull-back): the URL line. Dive frames are identical.
- Output 4060–4160 (Why You'll Thrive at full view): the URL line.
- Output 6850–7116 (the close): the current canonical closing JPG on a white stage, where v4 had the legacy rendered pill on the lavender
  stage. Pill size and motion match v4 (see below).
- Everywhere else the mean per-pixel difference is under 1.6 (re-encode noise). Audio stream MD5 identical to v4
  (7e6ac041f51a0eb8bbe9894e24a83f40); decoded PCM differs by 0.0. Duration and frame count identical.

## Two tool fixes made for this build (both committed)

1. `editspec_build.py`: `b.tall_margin = False` lets a build reproduce the pre-2026-09-14 framing of tall boards. Without it the press
   and thrive boards picked up the 4% stage margin added on 09-14 for Beyond the Average, which would have changed two spans David did
   not ask to change. Default behavior for new builds is unchanged.
2. `make_close_board.py --lesson`: the 09-15 rewrite placed the 1206x597 canonical closing JPG at native size on the 4K canvas, so the
   pill filled about a third of the frame (v4: 56%). It now scales the JPG so the pill spans the house fraction, proportions intact.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 7117 = plan = v4; audio 237.248 s; each leg decoded its span exactly.
2. `transition_guard.py` passed all 13 declared boundaries; `boundary-pairs.jpg` inspected.
3. No pause edits (audio untouched; silencedetect intervals identical to v4's).
4. Ring states inspected (`states-1-everyday.jpg`, `states-2-thrive.jpg`): same cards, colors, onsets, and dive windows as v4; the URL
   line is visible at every full view and clear of the banner ring.
5. Density and full-view opens unchanged from v4.
6. Not auditioned by ear: nothing new to hear; the audio is bit-identical to the shipped file.
7. The v5 close carried a faint hairline from the then-current closing JPG (a page-capture artifact); David regenerated the asset and v6
   uses it. Close frames inspected: pill at the house size, white stage, no line. Nothing left undone in scope.

**At ship:** move to `course-assets/why-learn-ai/why-learn-ai.mp4`, new cache key on the `whydeeper` entry (currently `20260914ship1`),
duration pill unchanged (4 min).
