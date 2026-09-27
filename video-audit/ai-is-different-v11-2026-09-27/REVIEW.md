# AI Is Different v11: review candidate, 2026-09-27

**Candidate:** `Prompts/ai-is-different-v11.mp4` (4:37.6, 8328 frames). This is not shipped, and the live video is unchanged.
**Build:** `scripts/video/build_ai_is_different_v11.py`, which is v10 (`video-audit/ai-is-different-v10-2026-09-27/REVIEW.md`) plus David's two review notes:

1. **v10 2:03 flash removed.** The roll 3 AI-network break inside Rules vs. Patterns ran into the first frames of roll 3's next scene (a code window fading in, 2:03.1–2:03.5). The break is gone and the board stays on screen, per David. As a result, Rules vs. Patterns is now an unbroken ~29 s board run (1:45.5–2:14.8). That is over the 20 s guideline, and David chose it.
2. **N4 cut** (v10 3:10–3:18, roll 2's "AI is flexible... like a PDF or a photo... summary, table, or image"). It repeated the two drawings before it and set up the "flexible / flexibility" echo. "Pictures, table, image" are now shown on the card and in the drawing but not spoken. The roll 3 inputs-to-outputs drawing hands back to the board 0.76 s before the app-line ring.

## Verification
- `transition_guard.py`: all boundaries PASS (`guard/`). Corner mark: 0 frames declined.
- Transcript: both edited spots read cleanly. The join is "…a clean first draft." → "While the available inputs…", with a 0.90 s gap.
- Frames 1:58–2:04 are board only. Frames 3:02–3:07 run from the drawings to the board with no stray frames.

## Not done
- No listening pass. The remaining joins to listen to are the roll 3 grafts at 1:20 and 1:54, the roll 2 legal-pad graft at 2:35, the N5 cut near 3:24, and the new N4 cut at ~3:09.
