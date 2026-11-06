# Does School Matter? video preparation

Prepared November 6, 2026 from the current local lesson in `index.html`, the approved boards, and `lessons/does-school-matter.md`. This is a full-lesson kit. The dated ending and skills pickup kits remain historical and are superseded for this generation.

## Lesson arc

The lesson moves from wondering why school matters when AI answers quickly, through a shared product-launch assignment that school-developed skills improve, to choosing knowledge and skills worth building now.

1. Ask the opening school question and establish the future job with the same AI.
2. Compare the same assignment and similar initial plans, row by row: sales projections, customer email, and market research. Each You example improves the work through skills learned in school.
3. Explain why similar AI answers became different finished work. Keep the approved combined paragraph linking writing, math, and research to the abilities developed in school.
4. Teach both Knowledge and Skills on What School Helps You Build, including critical thinking, questioning claims, weighing evidence, and informed decisions.
5. Encourage depth in an interest, explain that knowledge and skills remain yours as tools change, and finish with the exact two closing lines.

The source preserves the approved prose. The three school-skill sentences are separated into standalone paragraphs for verbatim delivery. “Here’s what school helps you build.” speaks the second board’s title as a short connective. The combined school paragraph remains intact.

## Upload and editing handoff

Upload only the four files staged in `upload/`: the full lesson Markdown, two faceless teaching boards, and the canonical close. Paste `PROMPT.txt` into video customization; do not upload this note or the prompt as source material.

| Upload board | Canonical replacement during editing | Handling |
| --- | --- | --- |
| `assets/does-school-matter-product-launch-faceless.jpg` | `course-assets/does-school-matter/does-school-matter-product-launch.jpg` | 1600 × 1639; both workplace portrait panels omitted, text and geometry retained. |
| `assets/what-school-helps-you-build-faceless.jpg` | `course-assets/does-school-matter/what-school-helps-you-build.jpg` | 1600 × 917; art panels omitted, including the sculpted face in Knowledge. Reused the verified existing faceless rendering because the canonical board is unchanged. |
| `course-assets/does-school-matter/does-school-matter-close.jpg` | Same canonical close | 1998 × 597; exact closing lines. |

Regenerate the first upload with `.video-venv/bin/python scripts/video/render_school_launch_comparison.py --upload-variant`. The second upload is an exact copy of `skills-2026-11-02/assets/what-school-helps-you-build-faceless.jpg`, made by `scripts/video/render_school_build_board.cjs --upload-variant`. That renderer still writes to the historical kit; copy its output into this kit only if the canonical board changes and the variant is reviewed again.

After generating, review the narration first. Preserve all three explicit connections to school and all three positive improvements. Do not restore THE RESULT, the removed character quotes, the redundant why-practice question, or the school-start-time example. Do not add product failures, invented costs, market statistics, or an activity segment. Restore the canonical illustrations during editing and plan board timing/highlighting under the current Edit Spec.

Save the first raw generation as `Prompts/does-school-matter-reroll.mp4`; use the next unused numbered name for further rolls. No generation, video installation, commit, or deployment is part of this preparation. The installed v13 video still needs revision to match the updated lesson. The external Video Tracker was not consulted; status here is based on local artifacts.

## Validation

Run `.video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson does-school-matter`, then repeat with `--check`. Check prompt length below 500 words, exact standalone required lines, ordered board uploads, matching board dimensions, and unchanged canonical assets. The registry owns the active upload list and post-production mappings.
