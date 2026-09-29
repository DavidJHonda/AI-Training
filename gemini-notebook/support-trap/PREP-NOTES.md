# Support Trap full-video reroll — September 29, 2026

David requested a **full-video generation**, then selection of its narration for the edit. This replaces the earlier suggestion to generate an isolated role passage. Generate the entire lesson, not a patch or summary. The current published v4 remains the baseline and possible donor; neither its audio nor its useful visuals should be discarded automatically.

## Teaching progression

Caring language raises the question of what actually changes → the same lunch disclosure gets an actionable invitation from a sister and words from a chatbot → separate real benefits from missing human presence and responsibility → distinguish venting, preparation followed by action, and danger requiring a person → give the content warning before the attributed Sophie story → explain what the black box concealed from people → teach urgent human-help actions → close on knowing when to leave the chat.

The Markdown carries the full current page/board teaching, with production-only Scene/Takeaway labels removed. Prose between boards has its own headings so it does not all become one board hold. The three roles retain the established prep's application of the page activity. The finals example now also uses the current activity's plan-then-start teaching; it is a concrete application of organizing thoughts, not a new lesson claim or a spoken quiz.

## What must land this time

- Require the complete benefits sentence verbatim: naming a feeling, **organizing your thoughts**, and preparing for a hard conversation. Then develop the practical examples.
- Require all four limitations together: notice what changed, show up, take responsibility, check tomorrow. The prior video does teach showing up elsewhere; do not misreport it as globally absent.
- The three jobs are **Ordinary Venting, Preparation, Danger**. The published graphic's Task Execution / System Collaboration / Multi-Agent Workflow labels are wrong. Both narration and visuals must keep the actual distinction. Orientation names the three once; examples develop them afterward.
- Preserve both lunch replies and the outcome comparison, including the possibility that the chatbot's words sound kinder.
- Keep the exact content note before the story, visible warning, 2025 attribution to Laura Reiley, Sophie Rottenberg's age of 29, Harry, “sometimes” encouraging help, “died by suicide,” and the mother's black-box account. Never invent a causal explanation, diagnosis, motive, or details of the death.
- Keep the two distinct 988 and 911 sentences, telling despite a promise, and both closing lines. Required sentences stand alone in the Markdown.
- Keep drafting versus doing without adding the previous roll's blanket claim that an AI bot cannot send email. Preserve the lesson's concrete requirement that the message reach the teacher and the real conversation happen.

## Uploads and generation

Upload every file in `upload/`: **one Markdown and four JPGs, five files total**. Paste `PROMPT.txt` into video customization; do not upload it or these notes. Save the full generation to the next unused `Prompts/support-trap-reroll.mp4` / `support-trap-reroll-N.mp4` name.

- Comparison: render a text-only source at the canonical 1600×1511 dimensions, keeping the scenario, both replies, all six comparison sections, and takeaway. Remove all photo panels from this upload variant.
- Role: upload the canonical 1600×885 board; it has no people or faces.
- Danger: render a text-only source at the canonical 1600×901 dimensions, preserving all three actions and the complete safety text. Conservatively omit all photos, including the small person in the first panel.
- Close: upload the canonical 1590×600 image.

The deterministic text-only renderer is `scripts/video/render_support_trap_uploads.py`. It uses text/layout primitives and canonical image dimensions; it does not alter or redraw canonical artwork. The illustrated comparison and danger boards remain post-only and replace their upload stand-ins during editing. The registry records both `covers` mappings.

## Review and editing handoff

Reference evaluation: `video-audit/support-trap-live-review-2026-09-29/REVIEW.md`. Baseline public cache key: `20260921ship28`; SHA-256: `3bf1658e980395f5d688b1c58cd39550c92378e2421644740611c7aaec3c23ab`; duration: 4:23.667. Earlier review used the exact-file transcript and sampled frames, not an audio audition.

Review the new full transcript against the current lesson, listen to the complete roll, and compare teaching beats with v4. Select narration only after that comparison; no donor word timings or joins are pre-approved. Protect the attributed story from the earlier generation's invented “because she relied on the bot” explanation. If using passages from different rolls, audition each join in context.

Preserve useful new or existing drawings and animations; correct faulty labels rather than replacing useful motion automatically. Keep boards in the upload set. The old 60.1-second comparison, 81.5-second board-to-board chain, and 52.47-second danger board call for relevant breaks during editing, not omission of teaching during generation. Use current canonical boards, spoken-onset highlighting, complete-card framing, and fixed four-pixel outlines at 720p in the next build. Retain a clear warning card and review its breathing room; choose any new pauses after listening, not from a fixed minimum. Final timings and board/camera plan depend on the selected narration.

This update prepares sources only. It does not generate a video, approve a production build or splice plan, replace the published lesson/video, or update the external tracker. Bundle checks establish consistency, not a teaching verdict.

## Preparation checks completed

- Prompt: 468 words, four required blocks in order; all ten verbatim sentences appear as standalone Markdown lines.
- Upload bundle: five files, all Markdown image references resolve, and lesson-specific sync `--check` reports OK.
- Both rendered upload variants visually inspected: full teaching text readable, no clipped text or photo panels, canonical dimensions retained.
- `index.html` and the canonical finished MP4 hashes remain unchanged from the start of this prep update.
