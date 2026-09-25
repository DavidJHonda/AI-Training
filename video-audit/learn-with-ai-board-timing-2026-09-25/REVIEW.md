# Learn with AI v9: pause cut, earlier boards, tighter card dives (2026-09-25). SHIPPED 2026-09-25.

**Scope.** David, 2026-09-25: cut the one-second pause at about 0:22; show Which Study Tool at "As you can see…" (0:57); on the
1:02 dive, and the pan to the other card, zoom further so the illustration at the top of the card is out of frame; show Your Four
Moves at "To get the most…" (David said 2:23; the line is at 2:35.2 in v8, 2:34.2 in v9).

**Candidate:** `Prompts/learn-with-ai-v9.mp4`, 6583 frames (3:39.43), 30 fps. Baseline is the shipped v8
(`baseline-live-20260921ship13.mp4`, sha256 521b271f…). The pristine rolls are gone. Build:
`scripts/video/build_learn_with_ai_board_timing.py`. Manifest: `edit-manifest.json`.

| Change | v8 | v9 |
|---|---|---|
| Pause into "Used correctly" | inserted 30 frames of room tone, frozen picture, 0:21.9–22.9 | removed; source joins source (about 0.4 s natural gap remains) |
| Which Study Tool arrives | 1:00.2 (over the gibberish chat sketch) | 0:55.33, as "As you can see here" starts (0:55.4) |
| Card dive window | whole card incl. illustration (2129 canvas px) | white text section only (1278 px), same card centres, same onsets (dive 1:02.3, pan 1:28.3) |
| Rings | shipped | shipped rects, colours, and onsets, verbatim (shifted with the earlier arrival) |
| Your Four Moves arrives | 2:37.6 (2:36.6 after the cut) | 2:34.07, 0.2 s before "To get the most" |

## Verification
1. Decoded 6583 frames at 30 fps (v8 minus 30). The new leg decoded its 1922 frames.
2. Audio: the cut-out segment peaks at -64 dBFS (room tone only). Seam RMS -61.5 dBFS. After the cut, the audio matches v8 shifted by
   1.000 s (correlation 0.99998). Audio re-encoded once, AAC 192k mono.
3. `transition_guard.py`, 7 declared boundaries: 6 pass. The flag on "dive-focus" is the zoom itself (the frame-to-frame change builds
   up smoothly with no stale frame; strip inspected). Strips for the chat-sketch-to-board cut, the files-to-Four-Moves cut, and the
   held-to-shipped-leg join inspected: one clean cut each, no jump at the join.
4. Dive framing inspected (`preview/kb3-*`, `kb5-*`): no illustration visible, every section ring fully in frame, all text readable.
5. Not done: listening to the pause join by ear (it is a source-to-source rejoin, measured above); an end-to-end rewatch.

**Shipped 2026-09-25** on David's "ship it": installed as `course-assets/learn-with-ai/learn-with-ai.mp4` (sha256 61997998…, decoded 6583 frames at 30 fps after install), cache key `20260921ship13` → `20260925ship14` on the `studying` entry, duration pill unchanged (4 min). Candidate removed from Prompts/.
