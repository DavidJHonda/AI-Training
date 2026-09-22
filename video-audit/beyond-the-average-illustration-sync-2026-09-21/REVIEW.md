# Beyond the Average v8: SHIPPED 2026-09-21 (illustration sync, narrow visual repair)

**Scope.** David, 2026-09-21: "Beyond-the-average. From :50 to 1:00 we need to use the new illustration. It's straight-forward. No
highlighting or zoom and pans." The Same Tool board is the lesson's first illustration (`index.html` line 4884,
`?v=20260921batch5`); the cast refresh replaced it in place — same board, same 1600x1150 dimensions, same title, photograph rect
and takeaway banner, new cast in the photograph. Only that span changes. Narration, timing, FPS, frame count and the audio stream
are untouched. Fourth of the day's illustration syncs, after Why Learn AI, What Is AI and Does AI Think.

**Span.** Output frames 1521–1818 (0:50.70–1:00.60), 297 frames: the board leg, still and whole at full view, no rings and no
camera move — the treatment the shipped video already used. Boundaries verified by decoding, not by seeking: rendering the OLD JPG
at the shipped camera and scanning the whole live file matched frames 1521 through 1817 and nothing else, one contiguous run, every
frame at 2.81–2.82 mean per-pixel difference (re-encode noise), which also confirms the leg is a still with no push.

**Build.** `scripts/video/build_beyond_the_average_same_tool_sync.py`. The pristine roll this video was assembled from no longer
exists, so the baseline is the shipped file itself — the v7 ship of 2026-09-16, whose recorded sha256 (1472549cc38c…) matches the
live file — frozen here as `baseline-live-2026-09-16.mp4` (4984 frames, gitignored). Geometry comes from the same code that built
the shipped leg, `editspec_build.Build.compose` at its default tall margin (the 4% stage margin added on 09-14 for this very
lesson): a 2208x1242 canvas at offset (304, 46) and the full-view camera window [1104, 621, 2208], identical to
`leg-same-tool.json` in the 09-14 audit. One `ken_burns_path.py` leg, one concat pass (baseline head, new leg, baseline tail),
audio packet-copied.

- Asset: `course-assets/beyond-the-average/beyond-the-average-same-tool.jpg` (7ba7a831e37d…, 1600x1150). Previous: eeada8445f7b….
- Candidate: `Prompts/beyond-the-average-v8.mp4` (b50c3baa71e0…), shipped to `course-assets/beyond-the-average/beyond-the-average.mp4`
  and removed.
- Cache key `20260916ship1` → `20260921ship12` on the `whybother` entry. Duration pill unchanged and correct (3 min; 2:46.13).

**Note for whoever reads the history.** At build time the refreshed JPG was still uncommitted in the working tree — it belongs to
the cast-refresh session running in parallel, which commits its own assets and `index.html` alt text. This ship staged only the
video, this script, this audit directory and the one `LESSON_VIDEOS` line.

## Verification (narrow-repair checks, Edit Spec section 10)

1. Decoded 4984 frames at 30 fps, matching the baseline exactly. Leg decoded its 297 frames.
2. Audio packet payload sha256 identical to the baseline (`-c copy -f data`); the audio stream was never re-encoded.
3. `transition_guard.py` passed both declared boundaries (1521 source-to-same-tool, 1818 same-tool-to-source); strips inspected —
   one clean cut each way, from the Notebook server-aisle drawing into the board and out of the board into the Student A / Student B
   diagram, no stale frames, no board-render leak.
4. Frame diff against the baseline every 10th frame: inside the span mean 5.90 (the new cast); outside it mean 0.49, max 1.32 —
   re-encode noise. Nothing outside 1521–1818 changed visually.
5. Settled frames inspected (`state-001521-board-open.jpg`, `state-001670-board-mid.jpg`, `state-001817-board-last.jpg`) against the
   baseline's own frame: identical framing on the house stage, board whole, banner text readable, nothing clipped, no ring or motion
   introduced.
6. Not re-auditioned by ear: the audio is bit-identical to the shipped file, so there is nothing new to hear.
7. Not performed: a full end-to-end rewatch, and no check of the lesson's other board (What to Start Building Today), which this
   repair does not touch and the cast refresh did not change.
