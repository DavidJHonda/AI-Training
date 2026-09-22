# Honesty & Privacy v2: SHIPPED 2026-09-21 (illustration sync with rings, narrow visual repair)

**Scope.** David, 2026-09-21: "Honesty & Privacy. The illustration starts at 1:05." The When AI Help Is Allowed board is the
lesson's second illustration (`index.html` line 11262, `?v=20260921batch6`); the cast refresh replaced it in place — same board,
same 1706x922 dimensions, same title, three numbered cards and takeaway banner, new cast in the photographs. Only that span
changes. Narration, timing, FPS, frame count and the audio stream are untouched. Eighteenth of the day's illustration syncs.

**Span and structure.** The board is on screen from output frame 1959 (1:05.30) to 2880 (1:36.00), 921 frames, in the three
pieces the 09-12 build created: a single arrival frame, a 30-frame pause that freezes it, then the leg's remaining 890 frames.
This build renders the 891-frame leg and re-times it the same way, so the freeze lands on the frame it always did. Verified by
decoding: the pre-refresh JPG rendered through the shipped leg spec and re-timed identically reproduces the live video at 2.89
mean per-pixel difference across samples at every ring onset and the freeze boundary, nothing over 6.

**A note on which old asset matched.** The 09-12 manifest records sha a0c881ef… for `lessons/honesty-and-privacy-best-practices.jpg`,
while the pre-refresh course-asset is f8be2aed…. They are different bytes but the same picture — the 09-15 consolidation re-saved
the file — and the frame diff above confirms the live board is visually that asset. No hidden board revision is being carried in.

**Highlights.** The shipped four rings reused verbatim: card 1 Understand It, card 2 Show Your Process, card 3 Explain AI's Role,
then the banner. Same rectangles, colors, radii and onsets; the cards did not move in the refreshed art, checked by drawing all
four on the new canvas. Stroke needed no decision: the artwork-scaled rule gives 5 px at this camera (a 1706 px board across the
1280 px frame sits near the rule's reference framing), which is exactly what the shipped video carries. Measured on the candidate
against the baseline at the card 1 ring: identical run widths.

**Build.** `scripts/video/build_honesty_privacy_best_practices_sync.py`. Baseline: the shipped file itself, frozen here as
`baseline-live-2026-09-12.mp4` (sha256 99604cf032d3…, 7200 frames, gitignored); the 09-12 manifest's `render_sha256` matches it,
which the build asserts. Canvas from `editspec_build.Build.compose`: 1706x960 at offset (0, 19), matching that manifest. One
`ken_burns_path.py` leg, one re-timing pass into a lossless intermediate, one concat pass, audio packet-copied.

- Asset: `course-assets/honesty-and-privacy/honesty-and-privacy-best-practices.jpg` (f1358054816c…, 1706x922). Previous:
  f8be2aedcb8feff0…. The refresh is committed (cc7e16e4).
- Candidate: `Prompts/honesty-and-privacy-v2.mp4` (4207c924c8e9…), shipped to
  `course-assets/honesty-and-privacy/honesty-and-privacy.mp4` and removed.
- Cache key `20260912ship1` → `20260921ship26` on the `integrity` entry. Pill unchanged and correct (4 min; 4:00.00).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 7200 frames at 30 fps, matching the baseline exactly. Leg decoded its 891 frames; the re-timed intermediate, 921.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed all six declared boundaries — the two splices and the four ring onsets. The board is still at
   full view, so there is no camera motion to trip the detector. Both splice strips inspected: the Notebook shortcut-addition
   drawing into the board at 1959, the board into the claim-vs-reveal drawing at 2880.
4. Frame diff against the baseline every 10th frame: inside the span mean 6.47 (the new cast); outside it mean 0.30, max 1.13 —
   re-encode noise. Nothing outside 1959–2880 changed visually.
5. States inspected (`state-001959-board-arrives.jpg`, `state-001989-freeze-end.jpg`, the three card rings,
   `state-002762-banner.jpg`, `state-002879-board-last.jpg`): the freeze holds a settled frame, the correct card is ringed in
   each state, card text readable, banner clear of the frame edge, nothing clipped.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch, and no check of the lesson's other three boards (the school board, the privacy
   tiers and Share Only), which this repair does not touch and the refresh did not change.

**Housekeeping.** The lossless legs were deleted as soon as the candidate verified.
