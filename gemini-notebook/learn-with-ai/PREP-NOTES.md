# Learn with AI video preparation

Prepared November 6, 2026 from the current local lesson in `index.html`, its four canonical boards, and `lessons/learn-with-ai.md`. This is a fresh full-lesson kit under `scripts/video/PREPARATION.md`.

## Lesson arc

The lesson moves from not having enough time to study, through choosing a source-based study tool or a learning coach, to practicing with class materials and working through difficult ideas yourself.

1. Open on the crowded student schedule, the four-extra-hours joke, and the patient tutor. Keep the approved “makes you genuinely sharper” and “try another explanation when you’re stuck” wording.
2. Compare **Your Study Tool** with **Your Learning Coach**. Gemini Notebook uses supplied materials for study and exam preparation; ChatGPT Study mode and Gemini Guided Learning guide understanding through questions, hints, and explanations. Speak both best-use paragraphs and the shared class-materials/teacher-check banner.
3. Develop the study-tool side with the original class-materials paragraph and **How Gemini Notebook Works**. Name every upload type and every output type, then speak its banner.
4. Teach **Your Four Moves for Gemini Notebook** in order: one subject per notebook, give it the full picture, quiz yourself blind, and trace it back. Keep the history/math example, the complete ten-question quiz quotation, withheld answers and grading, and checking the original material through citations.
5. Return to the learning-coach side with “Sometimes you don’t need another study guide.” Explain stating what you are learning and where you are stuck, trying answers, asking for hints, and requesting a different explanation. Keep the student doing the thinking. Use drawn scenes for this prose rather than extending the four-moves board hold.
6. End with the exact current close: “Use AI to learn, not to skip the learning.” followed by “Practice. Ask questions. Explain it yourself.”

The narration source preserves every live prose paragraph. Board headings and labels are turned into short spoken sentences; no new teaching examples or claims are added. Required audio lines stand alone. The LAB, Discussion Questions, Group Exercise, Study-mode navigation, and LLM-training question are excluded from the video source. The removed “The Catch” sections and four-moves banner stay removed.

## Upload and editing handoff

Upload only the **five files in `upload/`**: one narration Markdown file and four JPGs. Paste `PROMPT.txt` into the video customization field; do not upload it, these notes, the registry, or the course packet as source material.

| Order | Upload board | Editing treatment |
| --- | --- | --- |
| 1 | `learn-with-ai-study-toolkit.jpg` | Exact canonical first board, 1600 × 1127. Current role labels, shared check banner, gray credit, and revised typography. |
| 2 | `learn-with-ai-how-it-works-faceless.jpg` | 1600 × 844 upload-only variant with both student-photo panels blank. Replace with `course-assets/learn-with-ai/learn-with-ai-how-it-works.jpg` during editing. |
| 3 | `learn-with-ai-four-moves-faceless.jpg` | 1600 × 1378 upload-only variant with the top-left history illustration blank because it contains a small sculpted face. Other three illustrations and all teaching text remain. Replace with `course-assets/learn-with-ai/learn-with-ai-four-moves.jpg` during editing. |
| 4 | `learn-with-ai-close.jpg` | Exact canonical closing board, 1578 × 600. Final frame and two spoken lines. |

The two temporary variants were made with the built-in image generator and exported as quality-95 JPEGs at the canonical dimensions. Their edit prompts and selected outputs are recorded in `assets/UPLOAD-VARIANTS.txt`. They are upload stand-ins, not replacements for the canonical page assets. Use the exact canonical boards in the video edit; do not retain blank panels or Notebook recreations. Board timing, highlights, and selective pauses belong to the later edit plan.

Save the first raw generation as `Prompts/learn-with-ai-reroll.mp4`, or the next unused numbered reroll name. Preserve existing raw generations and finished videos.

## Status and validation

The live lesson currently references `course-assets/learn-with-ai/learn-with-ai.mp4?v=20261008ship13`. That installed video predates this revised lesson and is not updated by preparation. No video generation, narration review, installation, commit, or deployment is included here. The external Video Tracker was not consulted; this status is based on verified local files.

Validation covers: the four ordered prompt blocks and a prompt below 500 words; standalone exact required lines; all live prose retained in order; current board copy and closing lines; no activity material in the narration source; matching upload-variant dimensions; exact hashes for canonical upload copies; registry mappings; and `sync_gemini_notebook.py --lesson learn-with-ai --check`.

Refresh the bundle after any source change:

```sh
.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson learn-with-ai
.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson learn-with-ai --check
```
