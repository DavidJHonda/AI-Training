# Your Home Base v4: SHIPPED 2026-09-21 (illustration sync over a camera walk, narrow visual repair)

**Scope.** David, 2026-09-21: "Your Home Base. Need the new illustration starting at 2:35." The Pick a Home Base board is the
lesson's middle illustration (`index.html` line 7823, `?v=20260921cast3`); the cast refresh replaced it in place — same board,
same 1600x1150 dimensions, same title, photograph rect with the three labelled workstations and the takeaway banner, new cast in
the photograph. Only that span changes. Narration, timing, FPS, frame count and the audio stream are untouched. Eighth of the
day's illustration syncs.

**Span.** Output frames 4651–5017 (2:35.03–2:47.23), 366 frames — the whole board leg, which is where 2:35 leads. Verified by
decoding: re-rendering the OLD JPG through the shipped leg spec reproduces the live video frame for frame across all 366 frames at
2.48 mean per-pixel difference (max 2.87, nothing over 6). The old asset's sha256 also matches the one recorded in the 09-16 v3
manifest, so the baseline and the spec belong to each other.

**The walk is the shipped one, verbatim.** `leg-home-base.json` reused unchanged: 100-frame establish with a small push
(2208 → 2141.76), 36-frame dive to the ChatGPT workstation [665, 696, 638], 67-frame hold, 45-frame pull back to the full
illustration, 118-frame hold. No rings on this board, so no stroke question arises. The composition did not move in the refreshed
art — the dive window frames the same ChatGPT sign and laptop, checked by drawing it on both canvases — so every beat lands where
it did before.

**Build.** `scripts/video/build_your_home_base_sync.py`. The rolls this video was assembled from no longer exist, so the baseline
is the shipped v3 itself, frozen here as `baseline-live-2026-09-16.mp4` (sha256 8ce89dfb5807…, 7168 frames, gitignored). Geometry
comes from the same code that built the shipped leg, `editspec_build.Build.compose` at its default tall margin: a 2208x1242 canvas
at offset (304, 46), matching the offset recorded in the 09-16 v3 manifest. One `ken_burns_path.py` leg, one concat pass, audio
packet-copied.

- Asset: `course-assets/your-home-base/your-home-base-home-base.jpg` (80315f17c4f3…, 1600x1150). Previous: 4e095acef2ff…, the sha
  the shipped build recorded.
- Candidate: `Prompts/your-home-base-v4.mp4` (c3a337dd9844…), shipped to `course-assets/your-home-base/your-home-base.mp4` and
  removed.
- Cache key `20260916ship1` → `20260921ship16` on the `modelselection` entry. Pill unchanged and correct (4 min; 3:58.93).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 7168 frames at 30 fps, matching the baseline exactly. Leg decoded its 366 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` on six declared boundaries: both splices pass and their strips were inspected (the Notebook
   choice/age-restriction drawing into the board at 4651, the board into the verifier drawing at 5017), one clean cut each way.
   The four beat boundaries flag one-frame islands, which are the camera easing in and out of its move: running the same guard on
   the **baseline** flags three of the same four at the same frames with the same counts, and the fourth strip
   (`beat-hold-full-illustration`) shows the pull-back's deltas decaying 13.6 → 0.0 with no stale frame. Detector noise from
   motion, not a defect introduced here.
4. Frame diff against the baseline every 10th frame: inside the span mean 4.96 (the new cast); outside it mean 0.28, max 0.96 —
   re-encode noise. Nothing outside 4651–5017 changed visually.
5. Per-frame motion profile inside the span correlates 0.9999 with the baseline's, maximum difference 1.09: the camera dives,
   holds and pulls back on the same frames at the same speed.
6. Walk states inspected (`state-004651-board-open.jpg`, `state-004787-dive-arrive.jpg`, `state-004853-dive-hold-end.jpg`,
   `state-004899-pullback-arrive.jpg`, `state-005016-board-last.jpg`): the dive lands on the ChatGPT sign with the sign and its
   laptop fully in frame, the pull-back settles on the whole board with title and banner readable.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
8. Not performed: a full end-to-end rewatch, and no check of the lesson's other two boards (The Big Three, How We Used Them),
   which this repair does not touch and the cast refresh did not change.
