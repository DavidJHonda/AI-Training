# Video repair batch 2

## Shipped outputs

- `videos/mind-trap.mp4`
- `videos/flattery-trap.mp4`
- `videos/support-trap.mp4`

The approved v3 review files were promoted byte for byte to the canonical
lesson filenames on 2026-08-22. The versioned review files remain available for
comparison, and the previous tracked versions remain recoverable through Git
history.

## Treatments

### Mind Trap

- Replaced the retired illustration sequence with the current “Why AI feels
  like somebody” board.
- Kept the full board visible and highlighted the two complete columns as the
  narration moved from the brain’s mind detector to AI’s generated language.
- Rebuilt the closing message from `CLOSE_BOARDS[mindtrap]` and began it at the
  preceding scene cut so the standard 48-frame prehold, 150-frame push, and
  fixed 1.2x endpoint all fit without cutting narration.
- Removed the 14-frame stray face graphic at 1:54 by advancing the following
  ELIZA-era illustration to the preceding scene cut.

### Flattery Trap

- Replaced the retired training animation with the current “How the praise got
  baked in” board.
- Highlighted People rank answers, The numbers move, Support often wins, and
  the result in narration order.
- Highlighted the board title when the narrator says that praise gets baked
  into the system, beginning at 1:34 instead of returning to the final panel.
- Rebuilt the closing message from `CLOSE_BOARDS[flattery]` with the standard
  close treatment.

### Support Trap

- Replaced the retired “Why AI feels like real support” sequence with the
  current “Use AI to get ready for people, not instead of people” board.
- Kept the full board visible and highlighted the complete What can be real and
  What is missing columns as spoken.
- Moved the right-column highlight to 1:37.13, exactly when the narrator begins
  “And on the right.”
- Reused the board near the lesson’s conclusion so the main title is visible
  and highlighted exactly when the narrator says it.
- Rebuilt the closing message from `CLOSE_BOARDS[supporttrap]` with the standard
  fixed endpoint and a longer final hold for the longer narration.

## Integrity results

All three review videos pass:

- exact decoded frame count;
- nominal 30 fps cadence;
- bit-identical source audio;
- no changed frames outside authorized visual spans;
- no one-to-five-frame source islands inside replacements.

Boundary strips and machine-readable reports are in
`video-audit/batch2/splice/`.

## Audio review

The between-word acoustic scan produced no `BLIP_CANDIDATE` results in any of
the three source videos. The remaining detections are longer breath or room
sound candidates, so no audio was changed.
