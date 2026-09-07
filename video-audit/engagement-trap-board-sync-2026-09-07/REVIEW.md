# Engagement Trap: board and illustration sync

Review candidate: `Prompts/engagement-trap-patched-v3.mp4`. Not shipped.

- 0:16.700–0:40.233: exact upper chat portion of the current lesson board. Both turns remain fully visible; the complete neutral AI bubble receives the standard purple ring at 0:19.400. The outcomes are omitted from this crop, not rewritten.
- 0:58.300–1:16.733: complete updated board establishes, then both outcome cards stay visible. Measured outer bounds are (40,740,784,1340) and (816,740,1560,1340), blue and amber respectively.
- 3:31.633–3:54.600: corrected current Nate/Luke illustration, including the right boy's inward gaze. Full title and banner remain visible.
- All other approved cuts, visuals and standard closing are retained.

Rebuilt visuals from the pristine roll, not a recompressed patched video. Audio stream-copied from the approved candidate. Both compressed-audio SHA256 and decoded PCM SHA256 match exactly; see `qa/integrity.json`. Runtime remains 7,265 frames / 30 fps = 4:02.167.

`transitions/transition-guard.json`: PASS, 14 boundaries, zero transient failures. All boundary before/after pairs visually checked, plus every-frame strips at the six changed-asset boundaries. Settled chat, outcome highlights, and illustration frames visually checked in `qa/changed-states.jpg`. Source and live hashes unchanged. No HTML edits.

The preliminary v2 render had an overly tight chat crop; retained as `initial-framing-v2.mp4` in this audit folder, not a review deliverable. The v3 chat framing avoids partial neighboring bubbles.
