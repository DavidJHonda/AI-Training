# Where AI Works Best — v10 review

Built October 23, 2026. **Review candidate only; not shipped.**

- Candidate: `Prompts/where-ai-works-best-v10.mp4`
- Duration: 173.8 seconds (2:53.8), down from 233.9 seconds (3:53.9). Saves 60.1 seconds.
- Format: 1280 × 720, 30 fps, 5,214 frames, H.264 with AAC audio.
- [Local review player](review.html) · [Encoded-video transcript](transcript/where-ai-works-best-v10.txt)

## Changes

The opening, course-building comparison, shared training explanation, and original closing remain. The four repeated per-strength training explanations and spoken strength-board banners are removed. Each strength retains two examples, eight in total.

The two exact simplified lesson boards replace the old strength boards and generated example graphics. Each board appears in full, then the camera moves toward the card being discussed and reframes to show both examples.

The fundraiser phrase comes from existing roll 1, with a −1.5 dB gain adjustment. The problem examples now run experiment first, budget trip second, matching the new board. No new narration was generated. This edit uses the installed v9 video plus the existing donor, with one additional video encode.

## Review points

- **1:31:** fundraiser phrase from roll 1. The player includes a button starting at 1:27 for context.
- **2:02–2:06:** experiment-to-trip sequence. The player includes a button starting at 1:59 for context.

## Verification

All 5,214 encoded frames were compared to the intended source frame or board-camera frame. Maximum mean absolute pixel error was 3.43/255, consistent with encoding differences. Frame timestamps are continuous at 30 fps. Encoded audio correlates 0.999988 with the assembled PCM; decoded peak is 0.824, below clipping. Cut edges were checked for low-energy gaps and use 5 ms ramps at discontinuous audio joins.

A fresh transcription of the encoded MP4 confirms the eight selected examples, complete fundraiser phrase, reordered problem examples, and retained ending. Direct listening was not performed; cadence and voice continuity still need listening review.

The generic transition guard flagged seven intentional camera moves as possible brief visual islands. All 16 boundary strips were visually inspected. The seven flagged sequences show continuous zooms of the correct new board, with no intervening old graphic or flash. The raw automatic FAIL is preserved in `transitions/transition-guard.json`; its flags are resolved by this visual review and the every-frame comparison, not by changing the detector threshold.

Hashes confirm the installed course video, lesson source, index, and new board assets remained unchanged during this build. Nothing was installed, committed, or pushed.

## Reproduction and evidence

- Build: `scripts/video/build_where_ai_works_best_v10.py`
- QA: `scripts/video/qa_where_ai_works_best_v10.py` (exits nonzero on the preserved generic transition-guard alerts)
- Exact source/output intervals and hashes: `edit-manifest.json`
- Frame/audio measurements: `qa.json`
- Visual overview: `overview-1.jpg`, `overview-2.jpg`, `overview-3.jpg`
- Boundary strips and raw alerts: `transitions/`
