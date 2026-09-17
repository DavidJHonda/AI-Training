# Vector Space v5: candidate 2026-09-17 (board refresh, visual-only retrofit of the shipped 2026-09-10 file)

**Candidate:** `Prompts/vector-space-v5.mp4` (3:52.90, 6987 frames, 30 fps, sha256 4873fac38f54…). **Scope** (David: "run the process with
the Vector Space video"): narrow visual repair of the shipped file (`course-assets/vector-space/vector-space.mp4`, the roll-4 candidate
of 2026-09-10/11 built by `build_vector_space_v4_review.py`). The six course boards are re-rendered from the current course-assets
JPGs (`vector-space-cities.jpg` c746dd66…, `vector-space-cities-closest.jpg` 5d24da88…, `vector-space-taste.jpg` 7f146cc4…,
`vector-space-neighborhoods.jpg` 1de4a9e8…, `vector-space-closest-drink.jpg` 3f693939…, `vector-space-meaning-map.jpg` 3c90cc2b…;
same dimensions as the renders the ship used; the site credit line is the difference), and the close is the canonical closing JPG
(`vector-space-close.jpg`, 1530x597) through `make_close_board.py --lesson vectorspace` on the house white stage at the house pill width
(56% at the hold, 67% after the push; the live close sat on the lavender stage at 54%/64%). **Source limitation, disclosed:** roll 4 no
longer exists, so the build takes the finished file as its picture source and muxes its audio stream back in untouched (`-c:a copy`).
Outside the changed spans the picture is one more encoding generation of the ship (mean per-pixel difference about 3, visually
identical). **Build:** `scripts/video/build_vector_space_v5_retrofit.py`. **Manifest:** `edit-manifest.json` here.

## What was reproduced

The shipped script's board definitions verbatim through the shared `Build.board` pipeline on the current files: the same source cuts,
compact density, ring targets, colors, radii and spoken onsets, banner rects re-measured on the current files (all six unchanged), and
`tall_margin = False` so the stage framing matches the pre-2026-09-14 library. **One library difference had to be undone for parity:**
on 2026-09-10 the compact whole-board push was `0.04 * n / 900` uncapped; on 2026-09-11 the library capped it at 4% and widened it to
keep rings clear of the frame edge. Under today's rule three legs pushed less than the live picture (cities 2.29% vs 2.60%, drink 2.55%
vs 4.10%, ctx 1.91% vs 2.22%) and drifted from it over their spans. The build re-applies the ship-time formula to every leg
(`push_rule` in the manifest), after which every state matches. Spans on the output timeline: Three Cities 795-1381, Closest City
1381-1969, Taste table 2551-3343, Neighborhoods 3610-4194, Closest drink 4509-5431, Context changes IT 6182-6681, close from 6711.
Every Notebook span is the shipped picture. No dives, so no framing cuts to turn into glides.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 6987 = plan = ship; duration 3:52.90; audio stream MD5 identical to the ship (cdae22279fb4573b825374c519bf747f).
2. `transition_guard.py` passed all 12 declared boundaries (795, 1381, 1969, 2551, 3343, 3610, 4194, 4509, 5431, 6182, 6681, 6711);
   every strip inspected (`guard/`, `guard-sheet-0/1.jpg`): one cut per boundary, destination on the first frame.
3. No pause or audio edits.
4. Every ring state from the re-rendered legs compared side by side with the live frame at the same output frame
   (`live-vs-new-0..3.jpg`): every ring, radius, and camera position matches; the credit line is the only board difference. Frame diff,
   every 10th frame: only the close span (6720-6980, white stage vs lavender) exceeds re-encode noise.
5. Board treatment as shipped 2026-09-10.
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope.

**At ship:** copy to `course-assets/vector-space/vector-space.mp4`, new cache key on the `vectorspace` entry (currently `20260911ship1`),
duration pill unchanged (3 min), refresh the manifest `video_assets` hash and size, remove the candidate from `Prompts/`.
