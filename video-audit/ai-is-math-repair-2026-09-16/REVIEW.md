# AI Is Math v4: board refresh candidate (2026-09-16, visual-only retrofit of the shipped v3)

**Candidate:** `Prompts/ai-is-math-v4.mp4` (3:30.33, 6310 frames, 30 fps). **Scope** (David: "use the new boards into the video, including
the closing message"): narrow visual repair of the shipped v3 (`course-assets/ai-is-math/ai-is-math.mp4`, sha256 50092ad96ef22b7f…). The
four course boards are re-rendered from the current course-assets JPGs (`ai-is-math-the-math.jpg` c72ef3725e…, `-two-coins.jpg`
98d0119744…, `-conditional-probability.jpg` 48b3381642…, `-what-comes-next.jpg` 75e29c0cee…; white cards with the site URL line, where
v3 carried the pre-attribution renders with mint-tinted cards), and the close is the canonical closing JPG (`ai-is-math-close.jpg`,
0376001ccd…, 1494x600). **Source limitation, disclosed:** the roll behind v3 no longer exists, so the build takes the finished v3 as its
picture source and muxes v3's audio stream back in untouched. Outside the changed spans the picture is one more encoding generation of v3
(mean per-pixel difference under 2.7, visually identical). **Live video unchanged.** **Build:** `scripts/video/build_ai_is_math_v4_retrofit.py`.
**Manifest:** `edit-manifest.json` here.

## What was reproduced

The shipped v3 is the v2 board build (`build_ai_is_math_review_repair.py`, 2026-09-09) with two Notebook spans restored
(`restore_ai_is_math_notebook.py`). v2's layout (each board scaled to fit 1220x680, centered on the house stage), its ring rectangles and
colors, and its event timing are reused verbatim on the new files, which share the old files' dimensions. Board spans on the output timeline,
confirmed against the live file's scene cuts: Standard Probability 1336–1834, Counting the Possibilities 1834–2597, A Clue Changes the Odds
3549–4480, What Comes Next? 5025–5760, close from 6070. The one-second pauses inside those spans hold the frame before them, as v3 did.
Everything else, Notebook's drawings and the two restored Notebook spans, is v3's picture.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 6310 = plan = v3; duration 3:30.33 = v3; audio stream MD5 identical to v3 (9ab394dffb731ff45281087fc2f3559b).
2. `transition_guard.py` passed all 8 declared boundaries (1336, 1834, 2597, 3549, 4480, 5025, 5760, 6070); `boundary-pairs.jpg` inspected.
3. No pause or audio edits.
4. Ring states inspected (`states/*.jpg`, 21 states) and a side-by-side of nine frames against the live file at ring events: every ring on the
   same component at the same frame; the only differences are the white cards and the URL line. Frame diff, every 10th frame: only the close
   span exceeds re-encode noise.
5. Board treatment as v3 (compact, still, rings).
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope.

**At ship:** move to `course-assets/ai-is-math/ai-is-math.mp4`, new cache key on the `aiismath` entry (currently `20260909repair1`), duration
pill unchanged (4 min).
