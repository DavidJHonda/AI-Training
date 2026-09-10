# Retired video specs (2026-09-10)

These files are kept for reconstructing past decisions. None of them governs
current production.

| File | Original path | Replaced by |
| --- | --- | --- |
| `GRADER-r4.md` | `scripts/video/GRADER-r4.md` | `GRADER-r5.md` (below), then `scripts/video/NARRATION-REVIEW.md` |
| `GRADER-r5.md`, `GRADER-r5-MIGRATION.md` | `scripts/video/` | `scripts/video/NARRATION-REVIEW.md`. Owner rule 2026-09-10: no more scoring; evaluation is whether the narration teaches the content. The r5 ship gates survive as the editor's ship checklist in `scripts/video/README.md`. |
| `CHALLENGER-intake.md` | `scripts/video/CHALLENGER-intake.md` | `NARRATION-REVIEW.md` (compare rolls on narration completeness; its harvest idea lives in the EDITING NOTES field). |
| `video-rubric.csv` | `videos/video-rubric.csv` | Nothing. David maintains the external tracker himself. |
| `CLOSE-FIX-PLAYBOOK.md` | `scripts/video/CLOSE-FIX-PLAYBOOK.md` | The standard-close section of `scripts/video/README.md`: fixed 1.2x endpoint via `make_standard_close_plan.py`, and `make_close_board.py --lesson` for verbatim close copy. This playbook's span-scaled zoom and hand-passed pill/sticky text contradict r5. |
| `Master Prompt.md` | `Prompts/Master Prompt.md` | Nothing. Every per-lesson prompt is self-contained and it is never uploaded. Its narration rules (one narrator, never ask the viewer to pause or answer, open on the first scene, no photography, no invented data) live inside each prompt. |
