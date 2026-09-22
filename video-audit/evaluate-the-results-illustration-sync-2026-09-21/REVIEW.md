# Evaluate the Results v6: SHIPPED 2026-09-21 (illustration sync with a camera walk and rings, narrow visual repair)

**Scope.** David, 2026-09-21: "Evaluate the Results. Use the new illustration at 3:38 to 4:05. Including zooms and highlights."
The Check Before You Use board is the lesson's closing illustration (`index.html` line 9388, `?v=20260921cast3`); the cast refresh
replaced it in place — same board, same 1600x1394 dimensions, same title, photograph, the CLAIM / SOURCES / DECISION row and the
takeaway banner, new cast in the photograph. Only that span changes. Narration, timing, FPS, frame count and the audio stream are
untouched. Tenth of the day's illustration syncs.

**Span.** Output frames 6549–7372 (3:38.30–4:05.73), 823 frames — the whole board leg. Verified by decoding: the OLD JPG rendered
through the shipped leg spec (stroke forced to the old constant 5 for the comparison) reproduces the live video at 2.70 mean
per-pixel difference, sampled every 20 frames and at every beat and ring onset, nothing over 6. The old asset's sha256 also
matches the one recorded in the 09-16 manifest, so baseline and spec belong to each other.

**Zooms and highlights, both the shipped ones.** `leg-example.json` reused unchanged: 86-frame establish at full view, 24-frame
dive to the CLAIM / SOURCES / DECISION row, 88-frame hold with the CLAIM ring, move and 184-frame hold with SOURCES, move and
180-frame hold with DECISION, 30-frame pull back, 183-frame full hold with the banner ring. The row did not move in the refreshed
art — all four rectangles and the dive window drawn on the new canvas land exactly as before.

Stroke follows the artwork-scaled rule (owner, 2026-09-21, and his instruction today that a synced video takes the current
highlighting). At this dive the rule gives 5 px, the weight the video already carried, so the three card rings are unchanged;
only the banner ring, which lives at the pull-back and full view, comes out finer at 3 px.

**Build.** `scripts/video/build_evaluate_the_results_example_sync.py`. The rolls this video was assembled from no longer exist, so
the baseline is the shipped file itself, frozen here as `baseline-live-2026-09-16.mp4` (sha256 0e138f738161…, 7708 frames,
gitignored). Geometry comes from the same code that built the shipped leg, `editspec_build.Build.compose` at its default tall
margin: a 2678x1508 canvas at offset (539, 57), matching the 09-16 manifest. One `ken_burns_path.py` leg, one concat pass, audio
packet-copied.

- Asset: `course-assets/evaluate-the-results/evaluate-the-results-check-before-use.jpg` (60a6c2dd8ffe…, 1600x1394). Previous:
  cb719bb0048581b3…, the sha the shipped build recorded.
- Candidate: `Prompts/evaluate-the-results-v6.mp4` (50b463848f73…), shipped to
  `course-assets/evaluate-the-results/evaluate-the-results.mp4` and removed.
- Cache key `20260916ship1` → `20260921ship18` on the `evaluating` entry. Pill unchanged and correct (4 min; 4:16.93).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 7708 frames at 30 fps, matching the baseline exactly. Leg decoded its 823 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` on eleven declared boundaries: both splices pass and their strips were inspected (the Make Your Move
   board into this one at 6549, this one into the close at 7372), one clean cut each way. Five beat/ring boundaries flag
   one-frame islands; running the same guard on the **baseline** flags the same five at the same frames, so it is the detector
   reacting to the shipped camera motion. The pull-back strip was inspected: deltas decay smoothly from 17.0 to 1.3 while the
   DECISION ring hands over to the banner, with no stale frame.
4. Frame diff against the baseline every 10th frame: inside the span mean 6.16 (the new cast); outside it mean 0.24, max 0.92 —
   re-encode noise. Nothing outside 6549–7372 changed visually.
5. Per-frame motion profile inside the span correlates 0.9999 with the baseline's, maximum difference 0.81: the camera dives,
   holds and pulls back on the same frames at the same speed.
6. States inspected (`state-006549-board-open.jpg`, the three ring states, `state-007176-banner.jpg`,
   `state-007371-board-last.jpg`): correct card ringed in each, card text readable at the dive, banner readable at full view,
   nothing clipped.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
8. Not performed: a full end-to-end rewatch, and no check of the lesson's other four boards (Quick Pass, Dig Decision, Dig
   Deeper, Make Your Move), which this repair does not touch and the cast refresh did not change.
