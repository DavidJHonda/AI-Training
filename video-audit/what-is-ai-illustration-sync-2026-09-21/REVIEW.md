# What Is AI? v2: SHIPPED 2026-09-21 (illustration sync, narrow visual repair)

**Scope.** David, 2026-09-21: "Do the same thing for What is AI? From :12 to :18 the illustration needs to be updated. No other
changes should be made to the video." The Ask the Desk board is the lesson's illustration (`index.html` line 3913,
`?v=20260921cast2`); the 09-21 cast refresh replaced it in place — same board, same 1600x1150 dimensions, same title, photo rect,
speech bubbles and takeaway banner, new cast in the photograph. Only that span changes. Narration, timing, FPS, frame count and the
audio stream are untouched. Same pass as the Why Learn AI illustration sync earlier today.

**Span.** Output frames 370–574 (0:12.33–0:19.13), 204 frames: the board leg, still and whole, no rings, no pause hold after it —
the treatment the shipped video already used. Boundaries verified by decoding, not by seeking: re-rendering the OLD JPG through the
same code and diffing against the live file put the board's first frame at 370 and its last at 573 (mean per-pixel difference 2.69
across the span, re-encode noise; 77.0 at frame 369 and 83.8 at 574). They match `edit-manifest.json` in the 09-16 repair audit.

**Build.** `scripts/video/build_what_is_ai_desk_sync.py`. The pristine roll this video was assembled from no longer exists, so the
baseline is the shipped file itself, frozen here as `baseline-live-2026-09-16.mp4` (sha256 640a8d915399…, 5298 frames, gitignored).
Geometry comes from the same code that built the shipped leg — `editspec_build.Build.compose` with `tall_margin=False` — which on a
1600x1150 board yields a 2044x1150 canvas at offset (222, 0) and the full-view camera window [1022, 575, 2044], identical to
`leg-desk.json` in the 09-16 audit. One `ken_burns_path.py` leg, one concat pass (baseline head, new leg, baseline tail), audio
packet-copied.

- Asset: `course-assets/what-is-ai/what-is-ai-ask-the-desk.jpg` (19ba95765a87…, 1600x1150). Previous: 905c3859092b…, same dimensions.
- Candidate: `Prompts/what-is-ai-v2.mp4` (954c22da0e59…), shipped to `course-assets/what-is-ai/what-is-ai.mp4` and removed.
- Cache key `20260916ship1` → `20260921ship9` on the `llms` entry. Duration pill unchanged (3 min; 2:56.6).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 5298 frames at 30 fps, matching the baseline exactly. Leg decoded its 204 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed both declared boundaries (370 source-to-desk, 574 desk-to-source); strips inspected — one clean cut
   each way, from the Notebook desk drawing into the board and out of the board into the Ancient Egypt / Berlin Wall timeline, with
   no stale frames and no board-render leak.
4. Frame diff against the baseline every 10th frame: inside the span mean 5.49 (the new cast); outside it mean 0.27, max 0.85 —
   re-encode noise. Nothing outside 370–574 changed visually.
5. Settled frames inspected (`state-000370-desk-open.jpg`, `state-000470-desk-mid.jpg`, `state-000573-desk-last.jpg`) against the
   baseline's own frames: identical framing, board whole and edge-to-edge, both speech bubbles and the laptop list readable, banner
   clear of the frame edge.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch of the rest of the video, which this repair does not touch.
