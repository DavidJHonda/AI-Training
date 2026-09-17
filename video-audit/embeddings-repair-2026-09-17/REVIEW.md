# Embeddings v5: candidate 2026-09-17, SUPERSEDED by v6 the same day (board refresh, visual-only retrofit of v4)

**Candidate:** `Prompts/embeddings-v5.mp4` (3:58.17, 7145 frames, 30 fps). **Scope** (David: "use the current boards in the lesson.
Replace the existing with those"): narrow visual repair of the shipped v4 (`course-assets/embeddings/embeddings.mp4`, sha256
adb23d034b23…). The five course boards are re-rendered from the current course-assets JPGs (`embeddings-student-id.jpg` 3620c271e8…,
`embeddings-meaning-row.jpg` 16fe24651f…, `embeddings-new-dimension.jpg` 68bb096b6b…, `embeddings-taste-test-to-ai.jpg` 94edafdce7…,
`embeddings-inside-real-model.jpg` b514833912…; the site credit line on the four content boards is the difference from the
pre-attribution renders v4 carried, and the student-ID illustration is byte-identical to what v4 used), and the close is the canonical
closing JPG (`embeddings-close.jpg`, 8b4f1ab749…, 1626x597) through `make_close_board.py --lesson embeddings`, which puts it on the
house white stage at the house pill width (56% at the hold, 67% at the end of the push; the live v4 close sat on the lavender stage at
the same sizes, and every close shipped on 2026-09-16 is on white). **Source limitation, disclosed:** the rolls behind v4
(`Prompts/embeddings-1.mp4`, `embeddings-2.mp4`) no longer exist, so the build takes the finished v4 as its picture source and muxes
v4's audio stream back in untouched (`-c:a copy`). Outside the changed spans the picture is one more encoding generation of v4 (mean
per-pixel difference under 3, visually identical). **Build:** `scripts/video/build_embeddings_v5_retrofit.py`. **Manifest:**
`edit-manifest.json` here.

## What was reproduced

v4's schedule (`build_embeddings_v4.py`, 2026-09-10) verbatim on the current files, which share the old files' dimensions
(1600x1308 / 848 / 1038 / 1029 / 1215): the same edit timeline mapping output frames to the rolls' seconds, the same events, the
student-ID camera move to the two spoken IDs (22.7-30.2 s) and back, the same static full views and the two Inside a Real Model crops,
and the same rings at the same frames. Spans on the output timeline: student 561-1171, Meaning Becomes an Ordered Row of Numbers
1518-2776, One New Dimension 2776-3741, From Taste Ratings to AI Embeddings 3881-5187, Inside a Real Model 5352-6509, close from 6891.
Every Notebook span is v4's picture. No board, ring, camera, pause, or narration decision was revisited: this is the approved v4
treatment on the current assets.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded frames 7145 = plan = v4; duration 3:58.17 = v4; audio stream MD5 identical to v4 (306b1d5ac0f635d0f651702a43b076d6).
2. `transition_guard.py` passed all 13 declared boundaries (561, 1171, 1518, 2776, 3741, 3881, 5187, 5352, 5516, 6015, 6194, 6509,
   6891); every strip inspected (`guard/`, contact sheets `guard-sheet-0/1.jpg`): one cut per boundary, destination on the first frame.
3. No pause or audio edits.
4. Every state compared side by side with the live frame at the same output frame (`live-vs-new-0..5.jpg`, `live-vs-new-close.jpg`):
   every ring and every camera position matches; the credit line is the only board difference. Frame diff, every 10th frame: only the
   close span (6900-7140, white stage vs lavender) exceeds re-encode noise; every board span is under it.
5. Board treatment as v4 (approved 2026-09-10).
6. Not auditioned by ear: nothing new to hear.
7. Nothing left undone in scope.

**At ship:** copy to `course-assets/embeddings/embeddings.mp4`, new cache key on the `embeddings` entry (currently `20260910repair1`),
duration pill unchanged (4 min), refresh the manifest `video_assets` hash and size, remove the candidate from `Prompts/`.
