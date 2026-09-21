# Why Learn AI? v7: SHIPPED 2026-09-21 (illustration sync, narrow visual repair)

**Scope.** David, 2026-09-21: "the live video for Why Learn AI? From :13 to :24, we show the lesson's illustration. We updated the
illustration. So, use the current illustration in that place." The AI Is the Press board is the lesson's illustration
(`index.html` line 4685, `?v=20260921cast2`); the 09-21 cast refresh replaced it in place — same board, same 1600x1150 dimensions,
same title, photo rect and takeaway banner, new cast in the photograph (the printer is now a young woman; the scribe is unchanged).
Only that span changes. Narration, timing, FPS, frame count and the audio stream are untouched.

**Span.** Output frames 417–757 (0:13.90–0:25.23), 340 frames: the 310-frame board leg plus the 30-frame pause hold that follows it,
every frame identical (compact, still, full view, no rings — the shipped v6 treatment, unchanged). Boundaries verified by decoding,
not by seeking: re-rendering the OLD JPG through the same code and diffing against the live file put the board's first frame at 417
and its last at 756 (mean per-pixel difference 2.63 across the whole span, re-encode noise; 94.6 at frame 416).

**Build.** `scripts/video/build_why_learn_ai_press_sync.py`. The pristine rolls the video was assembled from
(`Prompts/why-learn-ai-1.mp4`, `-2.mp4`) no longer exist, so the baseline is the shipped file itself, frozen here as
`baseline-live-2026-09-16.mp4` (sha256 d3759d7ff1dcf315…, 7117 frames, gitignored). Geometry comes from the same code that built the
shipped leg — `editspec_build.Build.compose` with `tall_margin=False` — which on a 1600x1150 board yields a 2044x1150 canvas at offset
(222, 0) and the full-view camera window [1022, 575, 2044], identical to `leg-1-press.json` in the 09-16 audit. One
`ken_burns_path.py` leg, one concat pass (baseline head, new leg, baseline tail), audio packet-copied.

- Asset: `course-assets/why-learn-ai/why-learn-ai-press.jpg` (93733fd2ad01…, 1600x1150). Previous: 43a9730c99f6…, same dimensions.
- Candidate: `Prompts/why-learn-ai-v7.mp4` (6628a10f654e…), shipped to `course-assets/why-learn-ai/why-learn-ai.mp4` and removed.
- Cache key `20260916ship1` → `20260921ship8` on the `whydeeper` entry. Duration pill unchanged (4 min; 3:57.23).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 7117 frames at 30 fps, matching the baseline exactly. Leg decoded its 340 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed both declared boundaries (417 source-to-press, 757 press-to-source); strips inspected — one clean cut
   each way, no stale frames, no board-render leak.
4. Frame diff against the baseline every 10th frame: inside the span mean 6.29 (the new cast); outside it mean 0.36, max 1.49 —
   re-encode noise, in line with the v6 pass. Nothing outside 417–757 changed visually.
5. Settled frames inspected (`state-000417-press-open.jpg`, `state-000560-press-mid.jpg`, `state-000756-press-last.jpg`) against the
   baseline's own frames: identical framing, board whole and edge-to-edge, banner clear of the frame edge, title and takeaway readable.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch of the other 96% of the video, which this repair does not touch.
