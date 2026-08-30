# Current board and video audit

Read-only audit. No MP4 was modified.

- Main lesson videos: 46
- Teaching boards inventoried: 105
- Explicit course-native highlight plans: 78
- Missing video files: 0

## Executive result

- Current board pixels differ from the rendered planned walk: 25 boards across 16 videos
- Current boards with no course-native highlight plan: 27 boards across 10 videos
- Videos requiring board repair: 26 of 46
- Planned board walks already pixel-matched to the current source: 53
- Closing treatments to normalize to the new fixed endpoint: 46

The planned-walk comparison renders the current board through the production camera and ring engine, then compares that expected frame with the MP4. It therefore distinguishes a harmless file date change from an actual stale video frame.

## Findings

- BOARD_NEWER_THAN_PLAN: 12
- BOARD_NEWER_THAN_VIDEO: 30
- COURSE_NATIVE_HIGHLIGHT_PLAN: 78
- CURRENT_BOARD_NOT_VISUALLY_FOUND: 21
- MISSING_HIGHLIGHT_PLAN: 27
- PLAN_RENDER_DIFFERS_FROM_VIDEO: 25
- VISUAL_MATCH_WEAK: 9

## Highlight and close review rules

Every board comparison includes an active-state frame when a plan exists. The planned walks use the course-native ring-and-chip renderer. Boards without a native plan are replacement-required; no Gemini Notebook highlighting may be carried into the repair.

Every final frame is included in the closing contact sheets. Standard closes must share the same final visible size and centering; longer narration may only extend the hold.

## Artifacts

- `board-audit.csv`: sortable board-level ledger
- `board-comparisons/`: 35 current-board/video comparison sheets
- `closing-frames/`: 6 final-frame contact sheets

## Board ledger

| Video | Board | Plan | Best match | Findings |
|---|---|---:|---:|---|
| `videos/ai-is-different.mp4` | `illustrations/ai-is-different-kryptonite.jpg` | yes | 180.50s / MAD 2.4 | BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-different.mp4` | `illustrations/ai-is-different-side-by-side.jpg` | yes | 142.00s / MAD 2.2 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-1-formula.jpg` | yes | 28.50s / MAD 2.5 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-2-one-coin.jpg` | yes | 46.00s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-3-two-coins.jpg` | yes | 60.00s / MAD 2.4 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-4-update.jpg` | yes | 98.00s / MAD 2.5 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/ai-is-math.mp4` | `illustrations/ai-is-math-5-autoregressive.jpg` | yes | 146.00s / MAD 2.5 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/big-downside.mp4` | `illustrations/big-downside-goal-test-v2.jpg` | no | 126.50s / MAD 19.0 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/big-downside.mp4` | `illustrations/big-downside-guardrails-v3.jpg` | no | 75.00s / MAD 35.6 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/big-downside.mp4` | `illustrations/big-downside-jailbreak-v2.jpg` | no | 179.50s / MAD 73.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/big-downside.mp4` | `illustrations/big-downside-policy-puppetry-v2.jpg` | no | 122.00s / MAD 16.4 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/big-downside.mp4` | `illustrations/big-downside-safety-timeline-v2.jpg` | no | 124.00s / MAD 17.8 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/big-downside.mp4` | `illustrations/big-downside-voice-clone-v2.jpg` | no | 160.50s / MAD 27.1 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/big-upside.mp4` | `illustrations/big-upside-discovery-v3.jpg` | no | 195.00s / MAD 35.4 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/big-upside.mp4` | `illustrations/big-upside-hassabis-timeline.jpg` | no | 220.50s / MAD 17.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/big-upside.mp4` | `illustrations/big-upside-help-v3.jpg` | no | 211.50s / MAD 34.9 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/context-window.mp4` | `illustrations/context-window-luke-nate-ai.jpg` | yes | 23.50s / MAD 2.3 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/context-window.mp4` | `illustrations/context-window-outside.jpg` | yes | 145.50s / MAD 3.1 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/critical-thinking.mp4` | `illustrations/critical-thinking-1-equation.jpg` | yes | 6.00s / MAD 1.7 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/critical-thinking.mp4` | `illustrations/critical-thinking-2-one-more.jpg` | yes | 52.00s / MAD 1.7 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/critical-thinking.mp4` | `illustrations/critical-thinking-3-two-reactions.jpg` | yes | 94.00s / MAD 1.4 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/data-centers.mp4` | `illustrations/data-centers-footprint-v2.jpg` | no | 120.00s / MAD 47.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/does-ai-think.mp4` | `illustrations/does-ai-think-rulebook.jpg` | yes | 67.50s / MAD 2.8 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/does-school-matter.mp4` | `illustrations/does-school-matter-two-skills.jpg` | yes | 66.50s / MAD 2.4 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/embeddings.mp4` | `illustrations/embeddings-taste-three.jpg` | yes | 83.50s / MAD 1.6 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/embeddings.mp4` | `illustrations/embeddings-taste-two.jpg` | yes | 49.00s / MAD 1.6 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/evaluate-the-results.mp4` | `illustrations/evaluate-the-results-1-quick-pass.jpg` | yes | 54.50s / MAD 2.0 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/evaluate-the-results.mp4` | `illustrations/evaluate-the-results-2-decide.jpg` | yes | 101.00s / MAD 2.0 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/evaluate-the-results.mp4` | `illustrations/evaluate-the-results-3-dig.jpg` | yes | 156.00s / MAD 2.0 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/evaluate-the-results.mp4` | `illustrations/evaluate-the-results-4-move.jpg` | yes | 235.50s / MAD 1.9 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/fake-trap.mp4` | `illustrations/fake-trap-four-reasons.jpg` | yes | 102.00s / MAD 2.3 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/fake-trap.mp4` | `illustrations/fake-trap-three-checks.jpg` | yes | 163.50s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/flattery-trap.mp4` | `illustrations/flattery-trap-praise-loop.jpg` | yes | 67.00s / MAD 2.3 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/hallucination.mp4` | `illustrations/hallucination-types.jpg` | yes | 102.48s / MAD 2.3 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/hallucination.mp4` | `illustrations/hallucination-why.jpg` | yes | 21.50s / MAD 2.8 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/how-ai-answers.mp4` | `illustrations/how-ai-answers-last-token.jpg` | yes | 105.50s / MAD 2.1 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/layers.mp4` | `illustrations/layers-inside.jpg` | yes | 83.00s / MAD 2.9 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/layers.mp4` | `illustrations/layers-resolves-it.jpg` | no | 100.50s / MAD 14.3 | MISSING_HIGHLIGHT_PLAN, VISUAL_MATCH_WEAK |
| `videos/layers.mp4` | `illustrations/layers-three-reads.jpg` | yes | 0.00s / MAD 3.0 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/layers.mp4` | `illustrations/layers-why-dozens.jpg` | yes | 96.50s / MAD 2.1 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/learn-with-ai.mp4` | `illustrations/learn-with-ai-study-tools.jpg` | yes | 17.00s / MAD 3.1 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/loudest-voices.mp4` | `illustrations/loudest-voices-experts-v2.jpg` | no | 4.00s / MAD 32.1 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/loudest-voices.mp4` | `illustrations/loudest-voices-missed-predictions-v2.jpg` | no | 230.00s / MAD 45.4 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/mind-trap.mp4` | `illustrations/mind-trap-eliza-effect.jpg` | yes | 154.50s / MAD 1.8 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/opener-avoid.mp4` | `illustrations/opener-avoid-section-map.jpg` | yes | 124.98s / MAD 14.2 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/opener-embrace.mp4` | `illustrations/opener-embrace-section-map.jpg` | no | 122.50s / MAD 2.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO |
| `videos/opener-understand.mp4` | `illustrations/opener-understand-section-map.jpg` | yes | 73.50s / MAD 19.0 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/opener-work.mp4` | `illustrations/opener-work-section-map.jpg` | yes | 96.00s / MAD 13.7 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, VISUAL_MATCH_WEAK, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/pace-of-change.mp4` | `illustrations/pace-of-change-accelerants-v5.jpg` | no | 106.50s / MAD 37.1 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/pace-of-change.mp4` | `illustrations/pace-of-change-future-capability-v5.jpg` | no | 241.50s / MAD 40.2 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/pace-of-change.mp4` | `illustrations/pace-of-change-future-research-v5.jpg` | no | 187.50s / MAD 36.7 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/pace-of-change.mp4` | `illustrations/pace-of-change-three-years-v2.jpg` | no | 27.50s / MAD 16.4 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, VISUAL_MATCH_WEAK |
| `videos/questions-matter.mp4` | `illustrations/questions-matter-answers-cheap.jpg` | yes | 45.00s / MAD 2.3 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/questions-matter.mp4` | `illustrations/questions-matter-value-shift.jpg` | yes | 47.00s / MAD 2.1 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/rise-of-agents.mp4` | `illustrations/rise-of-agents-chatbot-agent-v2.jpg` | no | 242.50s / MAD 34.9 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/rise-of-agents.mp4` | `illustrations/rise-of-agents-flow-v2.jpg` | no | 132.00s / MAD 27.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/rise-of-agents.mp4` | `illustrations/rise-of-agents-gps-agent-v2.jpg` | no | 4.00s / MAD 88.6 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/rise-of-agents.mp4` | `illustrations/rise-of-agents-rogue-v2.jpg` | no | 133.50s / MAD 46.2 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/support-trap.mp4` | `illustrations/support-trap-real-vs-missing.jpg` | yes | 90.00s / MAD 2.2 | BOARD_NEWER_THAN_PLAN, PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/tokens.mp4` | `illustrations/tokens-3-cat.jpg` | yes | 138.50s / MAD 2.3 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/training-bias.mp4` | `illustrations/training-bias-mechanisms.jpg` | yes | 84.00s / MAD 2.3 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/training-bias.mp4` | `illustrations/training-bias-questions.jpg` | yes | 120.50s / MAD 7.0 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/training.mp4` | `illustrations/training-loop.jpg` | yes | 13.00s / MAD 2.0 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/transformer.mp4` | `illustrations/transformer-1-before.jpg` | yes | 69.99s / MAD 7.0 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/transformer.mp4` | `illustrations/transformer-2-now.jpg` | yes | 77.49s / MAD 64.6 | PLAN_RENDER_DIFFERS_FROM_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/transformer.mp4` | `illustrations/transformer-attention-transformation-video.png` | yes | 135.48s / MAD 5.9 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/transformer.mp4` | `illustrations/transformer-reading-comparison.jpg` | yes | 114.99s / MAD 8.9 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/transformer.mp4` | `illustrations/transformer-solutions-video.png` | yes | 191.98s / MAD 7.4 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/unexpected-results.mp4` | `illustrations/unexpected-results-plans-v2.jpg` | no | 213.00s / MAD 38.9 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/vector-space.mp4` | `illustrations/vector-space-cities.jpg` | yes | 29.00s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/vector-space.mp4` | `illustrations/vector-space-taste-profile.jpg` | yes | 64.00s / MAD 2.0 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-is-ai.mp4` | `illustrations/what-is-ai-llm.jpg` | yes | 190.50s / MAD 2.8 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-you-can-control.mp4` | `illustrations/what-you-can-control-hands.jpg` | yes | 97.98s / MAD 1.5 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-you-can-control.mp4` | `illustrations/what-you-can-control-three-moves.jpg` | yes | 155.97s / MAD 2.0 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/where-ai-works-best.mp4` | `illustrations/where-ai-works-best-1-transform.jpg` | yes | 71.00s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/where-ai-works-best.mp4` | `illustrations/where-ai-works-best-2-variation.jpg` | yes | 93.00s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/where-ai-works-best.mp4` | `illustrations/where-ai-works-best-3-compression.jpg` | yes | 107.00s / MAD 2.3 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/where-ai-works-best.mp4` | `illustrations/where-ai-works-best-4-reasoning.jpg` | yes | 139.00s / MAD 2.2 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/why-learn-ai.mp4` | `illustrations/why-learn-ai-thrive.jpg` | yes | 103.00s / MAD 1.7 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/work-changes.mp4` | `illustrations/work-changes-assignment-v2.jpg` | no | 328.00s / MAD 42.3 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/work-changes.mp4` | `illustrations/work-changes-automate-augment-v3.jpg` | no | 207.00s / MAD 30.2 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/work-changes.mp4` | `illustrations/work-changes-strengths-v2.jpg` | no | 169.50s / MAD 35.8 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/work-changes.mp4` | `illustrations/work-changes-what-changes-v3.jpg` | no | 229.50s / MAD 28.5 | MISSING_HIGHLIGHT_PLAN, BOARD_NEWER_THAN_VIDEO, CURRENT_BOARD_NOT_VISUALLY_FOUND |
| `videos/art-of-prompting.mp4` | `lessons/art-of-prompting-1-qualities.jpg` | yes | 60.50s / MAD 1.9 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/document-trap.mp4` | `lessons/document-trap-1-chunks.jpg` | yes | 118.00s / MAD 2.3 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/document-trap.mp4` | `lessons/document-trap-2-moves.jpg` | yes | 201.50s / MAD 2.2 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/how-an-llm-works.mp4` | `lessons/how-an-llm-works-1-map.jpg` | yes | 31.50s / MAD 2.1 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/how-an-llm-works.mp4` | `lessons/how-an-llm-works-3-patterns.jpg` | yes | 89.00s / MAD 2.6 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/learn-with-ai.mp4` | `lessons/learn-with-ai-2-feed-in.jpg` | yes | 101.00s / MAD 2.3 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/learn-with-ai.mp4` | `lessons/learn-with-ai-3-habits.jpg` | yes | 111.00s / MAD 2.0 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/one-more-thing.mp4` | `lessons/one-more-thing-1-draws.jpg` | yes | 87.99s / MAD 1.9 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/one-more-thing.mp4` | `lessons/one-more-thing-2-two-sides.jpg` | yes | 125.48s / MAD 1.9 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/one-more-thing.mp4` | `lessons/one-more-thing-3-bill.jpg` | yes | 196.47s / MAD 2.1 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/opener-avoid.mp4` | `lessons/opener-avoid-1-traps.jpg` | yes | 46.99s / MAD 1.5 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/opener-understand.mp4` | `lessons/opener-understand-1-kind.jpg` | yes | 0.00s / MAD 1.8 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/opener-work.mp4` | `lessons/opener-work-1-refrain.jpg` | yes | 7.00s / MAD 3.4 | BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/vector-space.mp4` | `lessons/vector-space-neighborhoods.jpg` | yes | 90.50s / MAD 1.9 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/welcome.mp4` | `lessons/welcome-2-how-to-take-course-page.jpg` | yes | 18.50s / MAD 2.7 | BOARD_NEWER_THAN_VIDEO, BOARD_NEWER_THAN_PLAN, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/welcome.mp4` | `lessons/welcome-2-your-path.jpg` | yes | 93.00s / MAD 2.4 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-is-ai.mp4` | `lessons/what-is-ai-1-types.jpg` | yes | 40.50s / MAD 2.9 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-is-ai.mp4` | `lessons/what-is-ai-2-movie-task.jpg` | yes | 99.50s / MAD 3.4 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/what-you-can-control.mp4` | `lessons/what-you-can-control-3-close.png` | yes | 162.97s / MAD 1.6 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/why-learn-ai.mp4` | `lessons/why-learn-ai-1-everyday.jpg` | yes | 40.00s / MAD 1.9 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/does-ai-think.mp4` | `scripts/video/assets/does-ai-think-compare-clean.png` | yes | 172.00s / MAD 1.7 | COURSE_NATIVE_HIGHLIGHT_PLAN |
| `videos/vector-space.mp4` | `video-audit/review-31/assets/vector-space-map-16x9.jpg` | yes | 130.00s / MAD 2.2 | PLAN_RENDER_DIFFERS_FROM_VIDEO, COURSE_NATIVE_HIGHLIGHT_PLAN |
