# Flattery Trap v7: SHIPPED 2026-09-21 (illustration sync with rings, narrow visual repair)

**Scope.** David, 2026-09-21: "Do this for Flattery Trap now. The new board starts about :23." The Flattery vs. Useful Feedback
board is the lesson's comparison illustration (`index.html` line 10480, `?v=20260921batch8`); the cast refresh replaced it in
place — same board, same 1600x1582 dimensions, same title, THE SCENARIO strip, the Flattery and Useful Feedback columns with
their response quotes and PRAISED / COULD FIT / NAMED / RESULT rows, and the takeaway banner, new cast in the two photographs.
Only that span changes. Narration, timing, FPS, frame count and the audio stream are untouched. Sixteenth of the day's
illustration syncs.

**Span.** Output frames 690–2487 (0:23.00–1:22.90), 1797 frames — the whole board leg, still at full view. This is the only leg
built from this asset; the video's other seven legs use the cycle-of-praise, sycophancy and five-moves boards, none of which the
refresh touched. Verified by decoding: the OLD JPG rendered through the shipped leg spec reproduces the live video at 2.78 mean
per-pixel difference, sampled every 25 frames and at all eight ring onsets, nothing over 6. The old asset's sha256 matches the
one build-v6 recorded, and build-v6's `render_sha256` matches the live file; the build asserts the latter.

**Highlights — nothing to decide.** The shipped eight rings reused verbatim: THE SCENARIO strip, the Flattery response quote,
its PRAISED and COULD FIT rows, the Useful Feedback response quote, its NAMED and RESULT rows, then the banner. Same rectangles,
colors, radii and onsets; the columns did not move in the refreshed art, checked by drawing all eight on the new canvas. Unlike
the other syncs today, no stroke question arose: v6 was the **first build under the artwork-scaled rule**, so its rings already
carry that weight (3 px at this camera) and re-rendering under the same default reproduces them. Measured on the candidate
against the baseline at the banner ring: identical run widths.

**Build.** `scripts/video/build_flattery_trap_comparison_sync.py`. Baseline: the shipped v6 itself, frozen here as
`baseline-live-2026-09-21-v6.mp4` (sha256 2449fbb325ec…, 9881 frames, gitignored). Canvas from
`editspec_build.Build.compose` at its default tall margin: 3040x1710 at offset (720, 64), matching build-v6. One
`ken_burns_path.py` leg, one concat pass, audio packet-copied.

- Asset: `course-assets/flattery-trap/flattery-trap-comparison.jpg` (acc368d0445a…, 1600x1582). Previous: 69cbe3f89b73ec20…,
  the sha v6 recorded. The refresh is committed (cc7e16e4, the parallel session's batches 4–9).
- Candidate: `Prompts/flattery-trap-v7.mp4` (9c926d2868c1…), shipped to `course-assets/flattery-trap/flattery-trap.mp4` and
  removed.
- Cache key `20260921ship5` → `20260921ship24` on the `flattery` entry. Pill unchanged and correct (5 min; 5:29.37).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 9881 frames at 30 fps, matching the baseline exactly. Leg decoded its 1797 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded. (The v6
   build's audio carries the roll-2 graft and three roll-3 drawings' beats; none of that is touched.)
3. `transition_guard.py` passed all ten declared boundaries — the two splices and the eight ring onsets. The board is still at
   full view, so there is no camera motion for the detector to trip on, and nothing was flagged. Both splice strips inspected:
   the Notebook marked-up-essay drawing into the board at 690, the board into How the Praise Got Baked In at 2487.
4. Frame diff against the baseline every 10th frame: inside the span mean 4.47 (the new cast only — the rings are unchanged);
   outside it mean 0.30, max 1.30 — re-encode noise. Nothing outside 690–2487 changed visually.
5. Ring states inspected (`state-000867-ring1-scenario.jpg`, `state-001210-ring2-flattery-response.jpg`,
   `state-001700-ring5-useful-response.jpg`, `state-002119-banner.jpg`): correct component ringed in each, same weight as the
   baseline's own frames, card text readable, nothing clipped.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch, and no check of the lesson's other three boards, which this repair does not touch
   and the refresh did not change.
