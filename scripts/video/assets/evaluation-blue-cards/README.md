# Evaluation Matters blue full-bleed cards

Built-in imagegen created the five text-free illustrations on 2026-10-23. `prompts.json` records every prompt; `boards.json` preserves the approved teaching copy. Artwork is local so the render is reproducible.

Render with `node scripts/video/render_evaluation_cards.cjs` (optional `--board decide` or `--board dig`). Canonical outputs are `course-assets/evaluation-matters/evaluation-matters-decide.jpg` (EE-2FB) and `evaluation-matters-dig.jpg` (EE-3FB). Blue #1652f0 intentionally matches the middle overview step across both boards. No mini maps or sequence indicators. Typography is deterministic Plus Jakarta Sans, 56/40/29 px, with original banners retained.

Dig Deeper now includes an assignment-style introduction above the cards, with two small task-and-stakes headings and original explanations. Its copy is in `boards.json` under `intro`.

The active middle board is titled Take a Closer Look with a blue step-2 marker; the two introduction headings use the same 40 px / 48 px bold styling as the three checking cards. Make Your Move is restored with three text-only cards, teal #0e8f86, and step-3 marker. The previous `decide` asset is retained for reference, not displayed in the lesson.
