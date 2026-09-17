# AI Is Different — v8 review handoff

## Recommendation

**Deployed to the canonical lesson path on 2026-09-16 at David's direction.** v8 preserves the approved v7 narration repair and replaces only the second lesson board with the newly revised `Two Ideas Behind Every Answer` artwork.

## Candidate

- File: `Prompts/ai-is-different-v8.mp4`
- Duration: 5:22.47
- Format: 1280x720, 30 fps
- Decoded frames: 9,674 of 9,674 expected
- SHA-256: `68d18890805cedea44b9fa19e1b9597de99dc14c4aaa12c13f0a6a080769c24b`
- Status: live at `course-assets/ai-is-different/ai-is-different.mp4`
- Website cache key: `?v=20260916ship1`

## Revised second board

- Board asset: `course-assets/ai-is-different/ai-is-different-learn-once.jpg`
- Asset SHA-256: `d621ca4329e7fa78f7d077b59c69c8a0a7b070b336f8f8ba0f80dd16e8fcb8fc`
- Output span: 1:01.53–1:37.13
- Complete-board opening: 210 frames / 7.00 seconds
- Highlight structure:
  - 1:08.53 — Training
  - 1:13.47 — Patterns
  - 1:20.83 — Patterns power every answer
  - 1:26.10 — Probability
  - 1:30.57 — Prediction

The rings were repositioned for the new two-card layout while preserving the original narration-synced sequence and purple/neutral/amber color logic. Each ring encloses the complete concept block, and the board remains readable before highlighting begins.

## Verification

- Full decode: PASS, 9,674/9,674 frames
- Transition guard: PASS, 22/22 declared boundaries
- Second-board entry at frame 1,846: visually inspected, clean
- Second-board exit at frame 2,914: visually inspected, clean
- Second-board state sheet: visually inspected, all five rings correctly placed
- Full 4-second timeline around the revised board: visually inspected
- Protected inputs, lesson Markdown, and live video unchanged: PASS
- Narration transcript: unchanged from the approved v7 repair
- Audio correlation with the planned edit: `0.9999129`

This environment cannot perform perceptual audio listening. No audio, narration timing, or audio splice changed in v8. David explicitly directed promotion of this reviewed candidate; the limitation remains recorded here rather than being represented as an audio pass.

Supporting artifacts:

- `states-learn.jpg` — revised board's full-view and five highlight states
- `final-sheet-1.jpg` — revised board in the finished timeline
- `guard/transition-guard.md` — all 22 splice checks
- `boundary-pairs.jpg` — finished before/after boundary comparisons
- `bundle/ai-is-different-v8/transcript.txt` — complete timestamped narration transcript
- `verification.json` — decode, audio, hash, pause, and protected-file checks

Build with `scripts/video/build_ai_is_different_v8.py` and verify with `scripts/video/qa_ai_is_different_v8.py`.
