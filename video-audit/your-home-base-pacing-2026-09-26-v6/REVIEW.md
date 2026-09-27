# Your Home Base v6 — Big Three zoom-and-pan, 2026-09-26

**Review candidate:** `Prompts/your-home-base-v6.mp4` (sha256 `5e73454b5b7f…`, 3:53.20, 6,996 frames). Live video and lesson page unchanged. v5 is kept for comparison.

**Change from v5 (David: "The board at 1:13. Let's do a zoom and pan highlight."):** The Big Three, Side by Side now gets the dense treatment (Edit Spec 4):
- Full view from 1:12.93 through "This board breaks down the big three side by side."
- At 1:16.20 ("We can think of ChatGPT…") the camera dives in 24 frames to one uniform window that holds the complete ChatGPT card.
- It pans to Claude at 1:35.44 and to Gemini at 1:52.28 (24 frames each).
- It pulls back to the full board for the overlap summary at 2:10.00 (30 frames).
- Each cut back from a monitor cutaway lands on the settled window.
- Everything else is exactly v5: rings and their timings, the three cutaways, the narration trim, How We Used, and the close.

**Framing:**
- Each card is 931 px tall on an 1,100 px board. Keeping the whole card in frame limits the window to 1773x998 canvas px, a **1.19x zoom**, so text is about 19% larger than at full view.
- The window's top edge sits in the gap between the title and the cards, so the title is never sliced.
- Neighbouring cards can be partly cropped at the frame edges; the active card is always whole.
- A stronger zoom would need a crop inside the card (section-level dives), which Edit Spec 4 forbids without an owner exception.

**Checks:**
- Frame count matches the plan.
- `transition_guard.py` passed all 13 boundaries.
- `ring_stroke.py` read 4 px on all 146 samples.
- Dive frames were checked in `dive-check.jpg` and `walk-sheet.jpg`.
- Board holds are unchanged from v5: longest single board and longest run are both 19.9 s (`measure/board-spans.txt`).

**Not performed:** listening (the 3:16.70 join, as in v5) and real-time playback of the camera moves.

Build: `.video-venv/bin/python scripts/video/build_your_home_base_v6.py`.

## Shipped 2026-09-26 (David: "ship it")

- Installed at `course-assets/your-home-base/your-home-base.mp4` (sha256 `5e73454b…de018`, 31,336,806 bytes); cache key `20260926ship7`; `manifest.json` video_assets row updated. Pill stays "4 min" (3:53).
- The ship-checklist listening pass was not done by the editor (no audio playback available); David approved after review.
