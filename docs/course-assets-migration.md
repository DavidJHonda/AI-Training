# Course asset migration

Completed locally on September 15, 2026. No deployment or image regeneration was performed.

## What changed

- Moved all 662 image/PDF assets from `lessons/` and `illustrations/` into `course-assets/`, grouped by lesson.
- Preserved every filename and every byte, including 146 website-attributed/original pairs.
- Preserved all 12 same-filename collisions. The original illustrations-folder copies are under `source-illustrations/` within the appropriate lesson. Eleven collision pairs have identical bytes; the two `critical-thinking-1-equation.jpg` files differ and remain distinct.
- Kept lesson Markdown and illustration documentation in their existing folders.
- Updated the website, image enlargement detection, download links, generators, video scripts, and active source/configuration references.
- Added a manifest-backed path resolver for computed filenames. It preserves the distinction between each original folder’s copy.
- Moved transient lesson PDF exports to `tmp/lesson-pdfs/`; the Start Smarter packet still publishes to `packets/start-smarter.pdf`.
- Left historical archive and generated audit snapshots as historical records.

## Verification

- SHA-256 verification passed for all 662 relocated assets.
- All 187 current website image/PDF references resolve, including computed Training board paths.
- Every manifest resolver entry and all 146 attribution generator input/output pairs resolve.
- Python, JavaScript, shell, inline application JavaScript, and script JSON checks passed for the applicable updated files.
- Browser comparison: Training, Your Home Base, Critical Thinking, Finish Smarter Opener, and Learn with AI retained identical image positions and dimensions.
- The enlarged-image viewer opens migrated assets.
- Five Big Ideas image and PDF downloads match the preserved source bytes.
- Video renders were not rerun. Existing video files were not changed.

## File map and maintenance

See `course-assets/manifest.json` for every old path, new path, original SHA-256, and reference-file inventory. Those hashes describe the migration baseline; later intentional edits may change them.

Run `python3 scripts/verify-course-assets.py` to validate files and website references. Use `--migration-hashes` when checking against the original migration baseline.

## Lesson folders

| Folder | Assets |
| --- | ---: |
| `ai-is-different` | 19 |
| `ai-is-math` | 15 |
| `art-of-prompting` | 7 |
| `avoid-traps-opener` | 7 |
| `beyond-the-average` | 8 |
| `big-downside` | 20 |
| `big-upside` | 12 |
| `build-your-skills-opener` | 4 |
| `context-window` | 14 |
| `creative-thinking` | 9 |
| `critical-thinking` | 17 |
| `curious-and-flexible` | 9 |
| `data-centers` | 7 |
| `document-trap` | 14 |
| `does-ai-think` | 7 |
| `embeddings` | 14 |
| `embrace-the-future-opener` | 5 |
| `engagement-trap` | 11 |
| `evaluate-the-results` | 17 |
| `fake-trap` | 16 |
| `finish-smarter-opener` | 4 |
| `flattery-trap` | 14 |
| `hallucination` | 21 |
| `honesty-and-privacy` | 18 |
| `how-ai-answers` | 15 |
| `how-an-llm-works` | 14 |
| `layers` | 11 |
| `learn-with-ai` | 12 |
| `loudest-voices` | 8 |
| `make-your-move` | 15 |
| `mind-trap` | 12 |
| `next-level-moves` | 13 |
| `one-more-thing` | 11 |
| `pace-of-change` | 17 |
| `people-skills` | 9 |
| `questions-matter` | 13 |
| `rise-of-agents` | 15 |
| `shared` | 2 |
| `support-trap` | 12 |
| `the-final` | 2 |
| `tokens` | 13 |
| `training` | 12 |
| `training-bias` | 18 |
| `transformer` | 20 |
| `understand-ai-opener` | 7 |
| `unexpected-results` | 5 |
| `vector-space` | 18 |
| `welcome` | 12 |
| `what-is-ai` | 8 |
| `what-you-can-control` | 10 |
| `where-ai-works-best` | 15 |
| `why-learn-ai` | 9 |
| `work-changes` | 17 |
| `work-with-ai-opener` | 6 |
| `your-choices` | 12 |
| `your-home-base` | 10 |

## Preserved filename collisions

- `course-assets/critical-thinking/source-illustrations/critical-thinking-1-equation.jpg`
- `course-assets/evaluate-the-results/source-illustrations/evaluate-the-results-1-quick-pass.jpg`
- `course-assets/evaluate-the-results/source-illustrations/evaluate-the-results-2-decide.jpg`
- `course-assets/evaluate-the-results/source-illustrations/evaluate-the-results-3-dig.jpg`
- `course-assets/evaluate-the-results/source-illustrations/evaluate-the-results-4-move.jpg`
- `course-assets/how-ai-answers/source-illustrations/how-ai-answers-before-answer-begins-v2.jpg`
- `course-assets/how-ai-answers/source-illustrations/how-ai-answers-token-by-token.jpg`
- `course-assets/how-ai-answers/source-illustrations/how-ai-answers-where-answer-begins-v2.jpg`
- `course-assets/how-an-llm-works/source-illustrations/how-ai-learns-patterns.jpg`
- `course-assets/how-an-llm-works/source-illustrations/how-an-llm-training-flow.jpg`
- `course-assets/vector-space/source-illustrations/vector-space-closest-drink.jpg`
- `course-assets/vector-space/source-illustrations/vector-space-neighborhoods.jpg`
