# Current board and video audit

Read-only audit. No MP4 was modified.

- Main lesson videos: 36
- Teaching boards inventoried: 58
- Explicit course-native highlight plans: 39
- Missing video files: 0

## Executive result

- Current board pixels differ from the rendered planned walk: 30 boards across 19 videos
- Current boards with no course-native highlight plan: 19 boards across 12 videos
- Videos requiring board repair: 29 of 36
- Planned board walks already pixel-matched to the current source: 9
- Closing treatments to normalize to the new fixed endpoint: 36

The planned-walk comparison renders the current board through the production camera and ring engine, then compares that expected frame with the MP4. It therefore distinguishes a harmless file date change from an actual stale video frame.

## Findings

- BOARD_NEWER_THAN_PLAN: 33
- BOARD_NEWER_THAN_VIDEO: 48
- CURRENT_BOARD_NOT_VISUALLY_FOUND: 2
- MISSING_HIGHLIGHT_PLAN: 19
- COURSE_NATIVE_HIGHLIGHT_PLAN: 39
- PLAN_RENDER_DIFFERS_FROM_VIDEO: 30
- VISUAL_MATCH_WEAK: 39

## Highlight and close review rules

Every board comparison includes an active-state frame when a plan exists. The planned walks use the course-native ring-and-chip renderer. Boards without a native plan are replacement-required; no Gemini Notebook highlighting may be carried into the repair.

Every final frame is included in the closing contact sheets. Standard closes must share the same final visible size and centering; longer narration may only extend the hold.

## Artifacts

- `board-audit.csv`: sortable board-level ledger
- `board-comparisons/`: 20 current-board/video comparison sheets
- `closing-frames/`: 4 final-frame contact sheets

## Board ledger

| Video | Board | Plan | Best match | Findings |
|---|---|---:|---:|---|
| `videos/ai-is-different.mp4` | `illustrations/ai-is-different-kryptonite.jpg` | yes | 180.50s / MAD 16.2 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-different.mp4` | `illustrations/ai-is-different-side-by-side.jpg` | yes | 11.00s / MAD 20.5 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-1-formula.jpg` | yes | 30.50s / MAD 9.9 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-2-one-coin.jpg` | yes | 47.00s / MAD 12.8 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-3-two-coins.jpg` | yes | 60.00s / MAD 2.4 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-4-update.jpg` | yes | 98.00s / MAD 2.5 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-5-autoregressive.jpg` | yes | 30.00s / MAD 17.4 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/context-window.mp4` | `illustrations/context-window-outside.jpg` | yes | 147.00s / MAD 2.1 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/critical-thinking.mp4` | `illustrations/critical-thinking-1-equation.jpg` | yes | 7.00s / MAD 10.7 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/critical-thinking.mp4` | `illustrations/critical-thinking-2-one-more.jpg` | yes | 52.00s / MAD 9.7 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/critical-thinking.mp4` | `illustrations/critical-thinking-3-two-reactions.jpg` | yes | 94.00s / MAD 12.1 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/does-ai-think.mp4` | `illustrations/does-ai-think-rulebook.jpg` | yes | 71.50s / MAD 17.1 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/does-school-matter.mp4` | `illustrations/does-school-matter-two-skills.jpg` | yes | 69.50s / MAD 20.5 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/embeddings.mp4` | `illustrations/embeddings-taste-three.jpg` | yes | 51.00s / MAD 12.5 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/embeddings.mp4` | `illustrations/embeddings-taste-two.jpg` | yes | 51.00s / MAD 10.7 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/evaluate-the-results.mp4` | `illustrations/evaluate-the-results-1-quick-pass.jpg` | yes | 55.50s / MAD 13.3 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/evaluate-the-results.mp4` | `illustrations/evaluate-the-results-2-decide.jpg` | yes | 235.00s / MAD 14.2 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/evaluate-the-results.mp4` | `illustrations/evaluate-the-results-3-dig.jpg` | yes | 235.00s / MAD 15.1 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/evaluate-the-results.mp4` | `illustrations/evaluate-the-results-4-move.jpg` | yes | 235.00s / MAD 12.9 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/fake-trap.mp4` | `illustrations/fake-trap-four-reasons.jpg` | no | 102.00s / MAD 14.8 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/fake-trap.mp4` | `illustrations/fake-trap-three-checks.jpg` | no | 102.00s / MAD 13.4 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/flattery-trap.mp4` | `illustrations/flattery-trap-praise-loop.jpg` | no | 137.50s / MAD 12.7 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/hallucination.mp4` | `illustrations/hallucination-types.jpg` | no | 41.00s / MAD 14.6 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/hallucination.mp4` | `illustrations/hallucination-why.jpg` | no | 70.50s / MAD 23.5 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/how-ai-answers.mp4` | `illustrations/how-ai-answers-last-token.jpg` | no | 10.00s / MAD 16.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/layers.mp4` | `illustrations/layers-inside.jpg` | no | 96.98s / MAD 20.8 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/layers.mp4` | `illustrations/layers-three-reads.jpg` | no | 97.98s / MAD 15.6 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/layers.mp4` | `illustrations/layers-why-dozens.jpg` | no | 10.00s / MAD 17.1 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/learn-with-ai.mp4` | `illustrations/learn-with-ai-study-tools.jpg` | yes | 6.50s / MAD 15.6 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/mind-trap.mp4` | `illustrations/mind-trap-eliza-effect.jpg` | no | 102.00s / MAD 16.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/opener-avoid.mp4` | `illustrations/opener-avoid-section-map.jpg` | yes | 126.50s / MAD 15.3 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/opener-understand.mp4` | `illustrations/opener-understand-section-map.jpg` | yes | 71.00s / MAD 18.3 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/opener-work.mp4` | `illustrations/opener-work-section-map.jpg` | yes | 93.50s / MAD 14.3 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/questions-matter.mp4` | `illustrations/questions-matter-answers-cheap.jpg` | yes | 44.00s / MAD 17.9 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/questions-matter.mp4` | `illustrations/questions-matter-value-shift.jpg` | yes | 94.00s / MAD 17.2 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/support-trap.mp4` | `illustrations/support-trap-real-vs-missing.jpg` | no | 90.00s / MAD 15.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/tokens.mp4` | `illustrations/tokens-3-cat.jpg` | yes | 142.50s / MAD 13.7 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/training-bias.mp4` | `illustrations/training-bias-mechanisms.jpg` | no | 85.00s / MAD 15.0 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/training-bias.mp4` | `illustrations/training-bias-questions.jpg` | no | 85.00s / MAD 15.6 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/training.mp4` | `illustrations/training-loop.jpg` | yes | 13.50s / MAD 8.3 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/transformer.mp4` | `illustrations/transformer-1-before.jpg` | no | 73.99s / MAD 16.1 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/transformer.mp4` | `illustrations/transformer-2-now.jpg` | no | 103.49s / MAD 64.7 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/vector-space.mp4` | `illustrations/vector-space-cities.jpg` | no | 95.00s / MAD 13.8 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/vector-space.mp4` | `illustrations/vector-space-taste-profile.jpg` | yes | 95.50s / MAD 11.6 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-is-ai.mp4` | `illustrations/what-is-ai-llm.jpg` | yes | 191.50s / MAD 9.9 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-you-can-control.mp4` | `illustrations/what-you-can-control-hands.jpg` | yes | 56.50s / MAD 20.3 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-you-can-control.mp4` | `illustrations/what-you-can-control-three-moves.jpg` | yes | 159.00s / MAD 15.4 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/where-ai-works-best.mp4` | `illustrations/where-ai-works-best-1-transform.jpg` | yes | 71.00s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/where-ai-works-best.mp4` | `illustrations/where-ai-works-best-2-variation.jpg` | yes | 92.50s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/where-ai-works-best.mp4` | `illustrations/where-ai-works-best-3-compression.jpg` | yes | 106.50s / MAD 2.3 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/where-ai-works-best.mp4` | `illustrations/where-ai-works-best-4-reasoning.jpg` | yes | 123.00s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/why-learn-ai.mp4` | `illustrations/why-learn-ai-thrive.jpg` | yes | 104.00s / MAD 18.7 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/document-trap.mp4` | `lessons/document-trap-1-chunks.jpg` | no | 195.00s / MAD 19.0 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/document-trap.mp4` | `lessons/document-trap-2-moves.jpg` | no | 118.00s / MAD 15.4 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/opener-work.mp4` | `lessons/opener-work-1-refrain.jpg` | yes | 7.00s / MAD 3.4 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/welcome.mp4` | `lessons/welcome-2-how-to-take-course-page.jpg` | no | 18.50s / MAD 2.1 | MISSING_HIGHLIGHT_PLAN |
| `videos/welcome.mp4` | `lessons/welcome-2-your-path.jpg` | yes | 93.00s / MAD 17.2 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/why-learn-ai.mp4` | `lessons/why-learn-ai-1-everyday.jpg` | yes | 40.00s / MAD 2.0 | COURSE_NATIVE_HIGHLIGHT_PLAN |
