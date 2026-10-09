#!/usr/bin/env python3
"""Build the Prompting Matters v6 review candidate (2026-09-26).

v5 plus David's note on it: "at 1:29, zoom in to the right side of the board like
you did for the left side. at 2:44, do the right side of the board the same zoom
in as you did on the left side."

- 1:26 is Four Moves, Move 2 (live leg frames 2753-3290): the same text-panel
  window as Move 1 (1.52x), diving at the 09-16 leg's frame 60.
- 2:43 is Four Moves, Continued, Move 4 (live leg frames 5057-5392): the same
  text-panel window as the Continued intro (1.47x), diving at frame 60.

As on Move 1, the whole-card ring becomes a ring around the move's text panel on
its Include rails (the illustration is out of frame); Include/Weak rects and all
ring times are the 09-16 leg's. Every other frame is v5's.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_art_of_prompting_v5 as v5  # noqa: E402

v5.DEST = v5.ROOT / "Prompts/art-of-prompting-v6.mp4"
M12, M34 = v5.M12, v5.M34

v5.LEGS["moves12-move2"] = dict(
    board=M12,
    live=(2753, 3290),
    beats=[("establish", 60, "full"), ("dive-text", 24, "text"), ("hold", 453, "text")],
    text=v5.M12_TEXT,
    rings=[
        # Move 2 text panel, same geometry as Move 1's on the right card's rails.
        (21, 98, [1444, 526 + 16, 720, 1493 - 12 - 542], "#1652f0", 18),
        (98, 410, [1444, 780, 720, 216], "#1652f0", 18),  # Include (09-16 rect)
        (410, 537, [1444, 1005, 720, 160], "#1652f0", 18),  # Weak (09-16 rect)
    ],
)
v5.LEGS["moves34-move4"] = dict(
    board=M34,
    live=(5057, 5392),
    beats=[("establish", 60, "full"), ("dive-text", 24, "text"), ("hold", 251, "text")],
    text=v5.M34_TEXT,
    rings=[
        # Move 4 text panel: 16 px below the illustration edge (canvas 535), 12 px
        # above the card bottom (canvas 1615), on the Include rails.
        (18, 102, [1556, 535 + 16, 720, 1615 - 12 - 551], "#a9760c", 18),
        (102, 335, [1556, 809, 720, 210], "#a9760c", 18),  # Include (09-16 rect)
    ],
)

if __name__ == "__main__":
    v5.main()
