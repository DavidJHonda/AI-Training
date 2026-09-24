# Big Upside v5: review candidate (2026-09-24)

v5 is v4 (`video-audit/big-upside-v4-2026-09-24/REVIEW.md`) with one visual repair David flagged: "At 4:06, there's
a graphic flash." Build: `scripts/video/build_big_upside_v5.py` (v4's legs reused). Output: `Prompts/big-upside-v5.mp4`,
7719 frames, 4:17.3, sha256 `a7d56ee3a5a5f4e4...` (full hash in `build/edit-manifest.json`). Audio identical to v4.

## Cause and fix

The Nobel-medal cover under "You might not win the Nobel Prize" (4:02.4-4:06.2) used roll 4 frames 5100-5215. From
frame 5198 roll 4 cross-dissolves to its next card, so for the last half second the AlphaFold chip and structure
drawing ghosted in before the cut to the close. The donor now stops at 5196 and holds that clean frame; the output
goes from the still medal card straight to the close (frame 7387).

The roll 3 chess/simulation cover (3:43.8-3:54.6) had the same kind of tail, fainter: its title and controller card
start dissolving at roll 3 frame 5928. That donor now stops at 5925 and holds.

## Checks

- Decoded frames 7719. transition_guard 20/20. Every frame from 4:05.3 to the close inspected: medal card still, then the close.
- Largest frame-to-frame changes between 3:50 and 4:07 are the four planned cuts between covers and the cut to the close.
- index.html changed on disk at 18:19 during the render (not by this build, which does not read it), so the render's
  protected-file assertion fired after the video was written. The Big Upside section's text, boards and close lines
  were checked unchanged; all other protected files unchanged.

## Not auditioned

As listed for v4.
