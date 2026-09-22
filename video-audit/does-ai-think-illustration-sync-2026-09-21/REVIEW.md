# Does AI Think? v7: SHIPPED 2026-09-21 (illustration sync with rings, narrow visual repair)

**v7 supersedes v6, shipped an hour earlier.** David, after reading the v6 report: "Change the lesson pill. Also, we want the new
highlighting for the video to be consistent." So v7 is the same build with the ring stroke taken off its pin and left to the
artwork-scaled rule (3 px at this camera instead of the shipped 5 px); the rectangles, colors, radii and onsets are untouched, and
the artwork is the same refreshed JPG. The `ring_stroke_px` escape hatch added for v6 is reverted out of `ken_burns_path.py` and
Edit Spec section 5 — the scaled rule is the only rule again. v7 was assembled from the same frozen baseline as v6, not from v6, so
the file still carries exactly one re-encode. The lesson's duration pill is corrected 3 min -> 4 min (the file is 3:40). Cache key
`20260921ship10` -> `20260921ship11`; candidate `Prompts/does-ai-think-v7.mp4` (c6321f91964d…). Everything below describes the
build both versions share, with the stroke note updated.

**Scope.** David, 2026-09-21: "2:02 to 3:14 in Does AI Think? has a new illustration. This one has highlights. We need to keep
those same highlights in the same place at the same time. We just need the new illustration." The When You Think / What AI Does
comparison board is the lesson's second illustration (`index.html` line 4824, `?v=20260921batch3`); the 09-21 cast refresh replaced
it in place — same board, same 1600x1556 dimensions, same title, column headings, five rows, takeaway banner and URL line, new cast
in the two photographs. Only that span changes. Narration, timing, FPS, frame count and the audio stream are untouched. Third of
the day's illustration syncs, after Why Learn AI and What Is AI, and the first with rings.

**Span.** Output frames 3669–5847 (2:02.30–3:14.90), 2178 frames: the board leg, still at full view, five green row rings and the
purple banner ring. Boundaries and highlights verified by decoding, not by seeking: re-rendering the OLD JPG through the shipped
leg spec reproduced the live video across the whole leg at a mean per-pixel difference of 2.86 (re-encode noise), sampled every 50
frames and at each ring onset — proof that the span, the camera, the ring rectangles, their colors, their onsets and the stroke
weight are all as shipped.

**Highlights: same rings, current stroke.** Ring rectangles, colors, radii and onsets are the shipped `leg-2-side-by-side.json`
reused verbatim; the rows did not move in the refreshed art, so they land on the same components. Confirmed by overlaying the
shipped rects on both JPGs. The stroke follows the artwork-scaled rule (owner, 2026-09-21), which draws 3 px at this camera because
the tall board is letterboxed at full view; measured on the candidate, the green row ring and the purple banner ring are 3 px
against the baseline's 5 px, in the same place at the same time. v6 pinned 5 px to leave the artwork as the only change; David then
asked for the current highlighting here too, which is what v7 carries.

**Build.** `scripts/video/build_does_ai_think_sbs_sync.py`. The pristine roll this video was assembled from no longer exists, so the
baseline is the shipped file itself, frozen here as `baseline-live-2026-09-16.mp4` (sha256 7982de8a668b…, 6600 frames, gitignored).
Geometry comes from the same code that built the shipped leg — `editspec_build.Build.compose` with `tall_margin=False` — which on a
1600x1556 board yields a 2766x1556 canvas at offset (583, 0) and the full-view camera window [1383, 778, 2766], identical to the
09-16 audit's leg spec. One `ken_burns_path.py` leg, one concat pass (baseline head, new leg, baseline tail), audio packet-copied.

- Asset: `course-assets/does-ai-think/does-ai-think-side-by-side.jpg` (a6d776ab594e…, 1600x1556). Previous: c9ff37bef301…, same size.
- Candidate: `Prompts/does-ai-think-v7.mp4` (c6321f91964d…), shipped to `course-assets/does-ai-think/does-ai-think.mp4` and removed.
  (v6, bcd585e1651a…, was the same build with the stroke pinned at 5 px; it was live for about an hour.)
- Cache key `20260916ship1` → `20260921ship10` (v6) → `20260921ship11` (v7). Duration pill corrected 3 min → 4 min (file is 3:40).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 6600 frames at 30 fps, matching the baseline exactly. Leg decoded its 2178 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed all eight declared boundaries — the two splices and all six ring onsets; the two splice strips were
   inspected frame by frame (OUTPUT / COMPREHENSION into the board at 3669, board into the gears drawing at 5847), one clean cut
   each way, no stale frames, no board-render leak.
4. Frame diff against the baseline every 10th frame: inside the span mean 6.55 (the new cast and the finer stroke); outside it
   mean 0.49, max 1.10 — re-encode noise. Nothing outside 3669–5847 changed visually.
5. Ring states inspected against the baseline's own frames (`state-003898-ring1-meaning.jpg` … `state-005538-banner.jpg`): same
   component ringed, same color, same onset, stroke at the current standard, text readable, nothing clipped.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch, and no check of the lesson's other board (The Chinese Room), which this repair does
   not touch and the cast refresh did not change.
