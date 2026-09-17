# Layers v6: candidate 2026-09-17 (v5 + one-second pause after "The horse raced past the barn fell.")

**Candidate:** `Prompts/layers-v6.mp4` (2:39.90, 4797 frames, 30 fps, sha256 fbe3017d9037…). **Scope:** v5
(`../layers-repair-2026-09-17/REVIEW.md`: the three current boards and the canonical close re-rendered into the shipped v4) plus one
change David asked for after eye-testing v5 ("Add a one second pause at :12 after the sentence 'The horse raced past the barn fell.'").
This is an audio-changing build: 30 frames of matched room tone are spliced into v4's audio at output frame 383 (12.77 s) and encoded
AAC 192k; everything before the insert is v5 frame for frame, everything after is v5 30 frames later. **Build:**
`scripts/video/build_layers_v6_retrofit.py` (imports v5). **Manifest:** `edit-manifest.json` here.

## The pause

| | |
|---|---|
| "fell." ends / "At first" begins (v5) | 12.22 s / 12.96 s, a natural gap of 0.74 s |
| Insert point | 12.77 s (frame 383), inside the quietest part of that gap (RMS about 20, the file's own floor) |
| Inserted | 30 frames = 1.00 s of room tone seeded from the same gap (12.70-12.80 s), house 240-sample crossfades at both joins |
| Resulting gap | 1.74 s between "fell." and "At first" (silencedetect at -45 dB: 12.59-13.99 s, 1.39 s under the threshold) |
| Picture during the pause | The Horse Raced Past the Barn Fell holds with its spoken-title ring; the First Read ring still pops on "At first" (now frame 417) |

David's instruction was a one-second pause, so a full second is added on top of the natural gap, as v4's own pauses were. If the
total should be one second instead, the insert shrinks to 8 frames; say so and it is a one-line change.

## Verification (Edit Spec section 10, audio-changing build)

1. Decoded frames 4797 = plan (v5's 4767 + 30); duration 2:39.90; close starts at 4541.
2. `transition_guard.py` passed all 9 declared boundaries (223, 383 hold start, 413 hold end, 796, 1073, 1860, 2367, 3101, 4541);
   every strip inspected (`guard/`, `guard-sheet.jpg`): one cut per boundary, the hold is a single still frame, destination on the
   first frame after it.
3. The edited pause measured in the finished file (table above). Audio outside the insert is sample-identical to v4's stream before
   the cut and after it (offset by one second); the decoded output correlates 0.9999 with the edit; the insert peaks at -52 dBFS, no
   noise-floor cliff (the bed matches the surrounding floor at RMS about 20).
4. Picture compared with v5 offset-aware at every 10th frame and every frame from 370 to 420: zero mismatches.
5. Board treatment as v4/v5.
6. **Not auditioned by ear** (no playback in this runtime): David should listen through 12.0-14.5 s for the pause and the two joins.
7. Nothing left undone in scope. Pre-existing items from the v5 review stand (two photograph spans, Why Dozens not in the video).

**At ship:** copy to `course-assets/layers/layers.mp4`, new cache key on the `layers` entry (currently `20260910repair1`), duration pill
unchanged (3 min), refresh the manifest `video_assets` hash and size, remove both candidates from `Prompts/`.
