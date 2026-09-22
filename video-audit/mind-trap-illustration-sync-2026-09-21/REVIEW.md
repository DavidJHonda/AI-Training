# Mind Trap v4: SHIPPED 2026-09-21 (illustration sync with rings, narrow visual repair)

**Scope.** David, 2026-09-21: "Mind Trap needs the new illustration from :27 to 1:07. Includes highlights." The Same Question.
Different Answers. board is the lesson's comparison illustration (`index.html` line 10337, `?v=20260921batch8`); the cast refresh
replaced it in place — same board, same 1600x1424 dimensions, same title, the YOU strip, the Your Mom and The Chatbot columns
with their KNOWS/SEES, NOTICES/MATCHES and STAKE rows, new cast in the two photographs. Narration, timing, FPS, frame count and
the audio stream are untouched. Fifteenth of the day's illustration syncs.

**Both appearances were replaced, not just the named one.** The same asset is on screen twice:

| Leg | Output frames | Time | Treatment |
|---|---|---|---|
| compare | 804–2030 | 0:26.80–1:07.67 | still full view, nine rings — the span David named |
| define | 2296–2450 | 1:16.53–1:21.67 | the same board held unmarked under the definition |

Replacing only the first would leave the same board showing a different cast nine seconds later, so both take the new artwork.
The second is separable: drop `'define'` from `PIECES` in the build script and rebuild.

**Highlights.** The shipped nine rings reused verbatim — the YOU strip, the whole Your Mom card, its KNOWS, NOTICES and STAKE
rows, the whole The Chatbot card, then its SEES, MATCHES and STAKE rows — same rectangles, colors, radii and onsets. The columns
did not move in the refreshed art, checked by drawing all nine rectangles on the new canvas. Stroke follows the artwork-scaled
rule: 3 px at this camera where the shipped video carried 5 px. Measured on the candidate against the baseline at the Your Mom
card ring: 4 px of coloured run against 6 (3 px and 5 px cores plus antialiasing).

**Build.** `scripts/video/build_mind_trap_comparison_sync.py`. Baseline: the shipped v3 itself, frozen here as
`baseline-live-2026-09-21-v3.mp4` (sha256 63c12abcb023…, 7213 frames, gitignored); build-v3's `render_sha256` matches it, which
the build asserts. One canvas from `editspec_build.Build.compose` at its default tall margin (2736x1540 at offset 568, 58) feeds
both legs. Two `ken_burns_path.py` legs, one concat pass over five pieces, audio packet-copied.

- Asset: `course-assets/mind-trap/mind-trap-comparison.jpg` (cd56225aeac5…, 1600x1424). Previous: 3685146309497c27…, the sha v3
  recorded. The refresh is committed (cc7e16e4, the parallel session's batches 4–9).
- Candidate: `Prompts/mind-trap-v4.mp4` (0b7f49264e5b…), shipped to `course-assets/mind-trap/mind-trap.mp4` and removed.
- Cache key `20260921ship4` → `20260921ship23` on the `mindtrap` entry. Pill unchanged and correct (4 min; 4:00.43).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 7213 frames at 30 fps, matching the baseline exactly. Legs decoded 1226 and 154 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. Spans proven before building: the OLD JPG rendered through both shipped specs with the stroke forced to 5 reproduces the live
   video at 2.66 mean per-pixel difference (max 2.70) across every sample and all nine ring onsets, nothing over 6.
4. `transition_guard.py` passed all thirteen declared boundaries — the four splices and the nine ring onsets. This board is
   still at full view, so there is no camera motion for the detector to trip on, and nothing was flagged. Splice strips
   inspected: one clean cut each way at 804, 2030, 2296 and 2450.
5. Frame diff against the baseline every 10th frame: inside the two spans mean 4.77 (the new cast and the finer stroke); outside
   them mean 0.38, max 1.37 — re-encode noise. Nothing outside the two legs changed visually.
6. Ring states inspected (`state-000931-ring1-you.jpg`, `state-001054-ring2-mom-card.jpg`, `state-001522-ring6-chatbot-card.jpg`,
   `state-001904-ring9-chatbot-stake.jpg`) and the unmarked hold (`state-002296-define-open.jpg`): correct component ringed in
   each, no ring on the hold, card text readable, nothing clipped.
7. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
8. Not performed: a full end-to-end rewatch, and no check of the lesson's other board (Why AI Feels Like Somebody), which this
   repair does not touch and the refresh did not change.
