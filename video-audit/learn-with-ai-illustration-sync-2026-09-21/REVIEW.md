# Learn with AI v8: SHIPPED 2026-09-21 (illustration sync with rings, narrow visual repair)

**Scope.** David, 2026-09-21: "learn-with-ai. From 2:07 to about 2:28. We have a new illustration. There is highlighting." The How
Gemini Notebook Works board is the lesson's middle illustration (`index.html` line 9200, `?v=20260921cast3`); the cast refresh
replaced it in place — same board, same 1600x844 dimensions, same title, two cards and takeaway banner, new cast in the two
photographs. Only that span changes. Narration, timing, FPS, frame count and the audio stream are untouched. Fifth of the day's
illustration syncs.

**Span.** Output frames 3812–4481 (2:07.07–2:29.37), 669 frames: the board leg, still at full view, the You Upload card ring, the
You Get card ring, and the banner ring. Verified by decoding, not by seeking: re-rendering the OLD JPG through the shipped leg spec
reproduced the live video across the whole leg at 3.04 mean per-pixel difference (re-encode noise), sampled every 25 frames and at
each ring onset and hand-off — which fixes the span, the camera, every ring rectangle, its color, its onset and its stroke.

**Highlights.** Ring rectangles, colors, radii and onsets are the shipped `leg-2-how-it-works.json` reused verbatim; the cards did
not move in the refreshed art, so they land on the same components (checked by overlaying the shipped rects on both JPGs). Stroke
needs no special handling here: this wide board fills the frame at full view, so the artwork-scaled rule (owner, 2026-09-21) gives
5 px — the weight the video already carries. Measured on the candidate against the baseline, all three rings match run for run.

**Build.** `scripts/video/build_learn_with_ai_how_it_works_sync.py`. The pristine roll this video was assembled from no longer
exists, so the baseline is the shipped file itself, frozen here as `baseline-live-2026-09-16.mp4` (sha256 e4d265738706…, 6613
frames, gitignored). Geometry comes from the same code that built the shipped leg, `editspec_build.Build.compose`: a 1600x900
canvas at offset (0, 28) and the full-view camera window [800, 450, 1600], identical to the 09-16 audit's leg spec. One
`ken_burns_path.py` leg, one concat pass (baseline head, new leg, baseline tail), audio packet-copied.

- Asset: `course-assets/learn-with-ai/learn-with-ai-how-it-works.jpg` (5099c3d1e07f…, 1600x844). Previous: 72a3b9b6ae23…, same size.
- Candidate: `Prompts/learn-with-ai-v8.mp4` (521b271f1491…), shipped to `course-assets/learn-with-ai/learn-with-ai.mp4` and removed.
- Cache key `20260916ship1` → `20260921ship13` on the `studying` entry. Duration pill unchanged and correct (4 min; 3:40.43).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 6613 frames at 30 fps, matching the baseline exactly. Leg decoded its 669 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed all five declared boundaries — the two splices and the three ring onsets; both splice strips were
   inspected frame by frame (the Notebook source-grounded diagram into the board at 3812, the board into the files-to-mind-map
   drawing at 4481), one clean cut each way, no stale frames, no board-render leak.
4. Frame diff against the baseline every 10th frame: inside the span mean 7.22 (the new cast); outside it mean 0.40, max 1.44 —
   re-encode noise. Nothing outside 3812–4481 changed visually.
5. Ring states inspected against the baseline's own frames (`state-003902-ring1-you-upload.jpg`, `state-004132-ring2-you-get.jpg`,
   `state-004391-banner.jpg`): same component ringed, same color, same onset, same stroke, card text readable, nothing clipped.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch, and no check of the lesson's other two boards (Which Study Tool, Four Moves), which
   this repair does not touch and the cast refresh did not change.
