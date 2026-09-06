# Training Bias repaired review candidate

Output: `Prompts/training-bias-patched.mp4`, 7488 frames at 30 fps, 4:09.60.
Shipped September 5, 2026 to `videos/training-bias.mp4`. Live file SHA-256 matches the approved candidate: `a4ceb6c48229065c8f31158e62c87d51aa14254fe5f74f59ae1468adceab856d`.
Previous live version preserved in `Archive/video-candidates/training-bias-pre-ship-2026-09-05/training-bias.mp4`. Prompt candidates retained. Lesson watch-bar duration updated to 4 min; no teaching content changed.

## Approved edits

- Source 2:31.167–2:36.433: removed the guarantee of revealing actual reality.
- Source 3:01.067–3:12.900: removed the asserted internal diagnosis of Claude's error. Preserved the complete sentence ending in Mavericks and the following practical correction.
- Source 3:24.200–3:29.867: continued the current lesson conversation board and its full current-source takeaway over the unsupported 18-month-cutoff graphic. Narration retained.
- Source 4:18.200–4:26.000: removed the philosophical reflection passage, going directly to the exact lesson closing.
- Inserted the five current lesson boards. Preserved native opening and between-board footage outside the replacement intervals. Three-card walkthroughs use full-board introductions, zooms, pans, and complete outer-card highlights; conversation highlights trace whole bubbles; takeaway highlights trace the entire banner.

## Final-output verification

- Exact frame count and source/live hash preservation assertions passed.
- Transition guard passed all 12 boundaries. Every-frame strips inspected for all boundaries.
- An initial one-frame old conversation-board flash was caught and repaired before delivery.
- All highlight states and the literal final frame inspected using QA frame sheets.
- Cut points checked with word-level source alignment, final-output splice transcription, and audio measurements. These are computational checks, not a claimed human listening pass.
- Final cut-point 20 ms audio levels: -64.6, -63.0, -67.1 dBFS. Cut points were moved out of breath tails during QA.
- Final-output audio joins: 2:31.167, 2:55.800, 4:01.100.

Rebuild: `.video-venv/bin/python scripts/video/build_training_bias_review.py`

QA: `.video-venv/bin/python scripts/video/qa_training_bias_review.py`

`manifest.json` contains exact board, highlight, and source/output timing details. `transitions/transition-guard.json` lists the current boundary strips; older iteration strips in the audit folder are not additional video candidates.
