# Make Your Move — actions introduction correction

User-directed narrow visual repair, October 23, 2026: show the course board when narration introduces it (the “Here is a…” line near 1:41, continuing through 1:44).

| Board | Highlights | Camera | On screen / breaks | Reason |
|---|---|---|---|---|
| Moves to Make | Complete unmarked board during the introduction; existing item highlights resume unchanged | Full canonical JPG, fitted to 720px height with the existing full-board horizontal placement | Replace city illustration at frames [3011,3341), 1:40.367–1:51.367. Existing action treatment continues afterward; its conversation cutaway remains at 1:59.4 | The narration explicitly introduces this four-action board, so the city illustration is mismatched. |

Audio, timing, and all other pictures remain unchanged. Encode only the replacement span, which starts and ends at existing closed GOP boundaries. Copy original audio packets and every unaffected video packet. Verify exact decoded-frame identity outside the repair, constant timestamps and frame count, and both visual transitions.

This extends the first actions-board run to about 19 seconds, before the existing conversation cutaway. No new pause, ring, zoom, narration, or teaching is added. V11 remains available for comparison. New candidate: `Prompts/make-your-move-v12.mp4`; no installation/publication.
