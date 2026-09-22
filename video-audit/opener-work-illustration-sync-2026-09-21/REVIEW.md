# Work With AI opener v8: SHIPPED 2026-09-21 (illustration sync over a camera walk, narrow visual repair)

**Scope.** David, 2026-09-21: "opener-work. From :47 to :58. There is a zoom in and zoom out." The Same Tool. Different Results.
board is the lesson's illustration (`index.html` line 8698, `?v=20260921cast1`); the cast refresh replaced it in place — same
board, same 1600x1150 dimensions, same title, photograph rect, the two phone panels inside it and the takeaway banner, new cast in
the photograph. Only that span changes. Narration, timing, FPS, frame count and the audio stream are untouched. Sixth of the day's
illustration syncs, and the first over a camera walk.

**Span and structure.** The board is on screen from output frame 1410 (0:47.00) to 1779 (0:59.30) — 369 frames in the three pieces
the shipped build created: the 339-frame photo walk's first 332 frames (1410–1742), a 30-frame pause that freezes walk frame 331
(1742–1772), and the walk's last 7 frames under the tail (1772–1779). This build renders one 339-frame leg and re-times it the same
way, so the freeze lands on the frame it always did.

**The walk is the shipped one, verbatim.** `leg-same-tool.json` reused unchanged: establish with a small push
(2044 → 1982.68 over 57 frames), 36-frame move to the two phone photos [1032, 505.4375, 1342], 112-frame hold, 45-frame pull back
to the full illustration, 89-frame hold. No rings. The composition did not move in the refreshed art — the zoom window frames the
same two phone panels, checked by drawing it on both canvases — so every beat lands where it did before.

Verified before building: the OLD JPG rendered through the shipped spec and re-timed the same way reproduces the live video frame
for frame across all 369 output frames at 2.42 mean per-pixel difference (max 2.67, re-encode noise). That fixes the span, the
beats, the pause hold and its freeze frame in one test. On the candidate, the per-frame motion profile inside the span correlates
0.9997 with the baseline's, maximum difference 0.8 — the camera moves on the same frames at the same speed.

**Build.** `scripts/video/build_opener_work_same_tool_sync.py`. The pristine roll no longer exists, so the baseline is the shipped
file itself, frozen here as `baseline-live-2026-09-16.mp4` (sha256 34a4e9ef4233…, 4737 frames, gitignored). Geometry comes from the
same code that built the shipped leg, `editspec_build.Build.compose` with `tall_margin=False`: a 2044x1150 canvas at offset
(222, 0). One `ken_burns_path.py` leg, one re-timing pass into a lossless intermediate, one concat pass, audio packet-copied.

- Asset: `course-assets/work-with-ai-opener/work-with-ai-opener-same-tool.jpg` (09a706b94854…, 1600x1150). Previous: 4ffd451900dc….
- Candidate: `Prompts/work-with-ai-opener-v8.mp4` (48c90ec93194…), shipped to
  `course-assets/work-with-ai-opener/work-with-ai-opener.mp4` and removed.
- Cache key `20260916ship1` → `20260921ship14` on the `openerworkwith` entry. Pill unchanged and correct (3 min; 2:37.90).

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 4737 frames at 30 fps, matching the baseline exactly. Leg decoded its 339 frames; the re-timed intermediate, 369.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed all six declared boundaries — the two splices and the four beat changes; both splice strips were
   inspected frame by frame (the Notebook blurry-vs-crisp sandwich drawing into the board at 1410, the board into the section map
   at 1779), one clean cut each way, no stale frames, no board-render leak.
4. Frame diff against the baseline every 10th frame: inside the span mean 6.99 (the new cast); outside it mean 0.27, max 0.80 —
   re-encode noise. Nothing outside 1410–1779 changed visually.
5. Walk states inspected (`state-001410-establish-open.jpg`, `state-001503-zoom-arrive.jpg`, `state-001614-zoom-hold-end.jpg`,
   `state-001659-pullback-arrive.jpg`, `state-001771-freeze-end.jpg`): the zoom arrives on the two phone panels with both fully in
   frame, the pull-back settles on the whole board with title and banner readable, and the freeze holds a settled frame.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch, and no check of the lesson's other boards (the refrain and the section map), which
   this repair does not touch and the cast refresh did not change.
