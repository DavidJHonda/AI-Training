# Video production handoff — September 10, 2026

This is a dated status snapshot for continuing in Claude or another assistant.
Read the current files and subsequent owner feedback before acting.

## Durable specifications

- `scripts/video/README.md`: production workflow and owner preferences. Read the
  current rules first; dated corrections supersede older repair recipes.
- `scripts/video/NARRATION-REVIEW.md`: the evaluation authority (narration-only,
  KEEP / REPAIR / REROLL). The r5 grader was retired later on 2026-09-10; visuals
  are verified by the ship checklist in the README.
- `Prompts/README.md`: Markdown, prompt TXT, upload boards, and cleanup workflow.
- `scripts/video/RETROFIT-PLAYBOOK.md` and `scripts/video/BOARD-SYNC-MANIFEST.md`:
  board replacement and timing/verification details.

The live lesson in `index.html` and its referenced assets define current content.
Do not infer current boards from old captures or raw videos. Preserve useful
Notebook graphics; use exact lesson boards only for spans that benefit from them.
New video-only replacement graphics should be Notebook-style illustrations.

## Pending: Vector Space review

David approved building a repair. It is built and linked for his review, **not
approved for shipping**. The existing live video and lesson registry are unchanged.

- Candidate: `videos/vector-space-v2.mp4`, 3:29.267, 6278 frames at 30 fps.
- SHA-256: `619a60cbcc7e6ad71721d4cca6f3f0935dbacf12449362bfb0f6d99e82ae3e04`.
- Base: `Prompts/vector-space-1.mp4`; Version 2 supplies the context-connection
  sentence. An existing course narration supplies “usually” in the close.
- Full changes and QA limits:
  `video-audit/vector-space-repair-2026-09-10/REVIEW.md`.
- Exact source spans, donor provenance, output timeline, assets, and boundaries:
  `video-audit/vector-space-repair-2026-09-10/edit-manifest.json`.
- Comparison: `video-audit/vector-space-comparison-2026-09-10/comparison.md`.
- Build: `.video-venv/bin/python scripts/video/build_vector_space_review.py`.
- QA: `.video-venv/bin/python scripts/video/qa_vector_space_review.py`.

The build preserves the full worked numerical comparison and CAT/IT sentence,
corrects inconsistent numbers/claims, retains useful Notebook scenes, uses current
boards and outline-only highlights, and ends with the current standard close.

Technical checks, complete edited transcript, contact sheets, settled highlights,
and every-frame splice strips were inspected. The transition guard passed all 27
boundaries. **Continuous listening/prosody certification was not performed.**
Review rendered audio joins, especially the donated “usually,” before treating
audio QA as complete. Seam clips are in the audit directory's `audio-seams/`.

Next step: address David's review feedback, or ship when he explicitly directs it.
Use the unsuffixed live filename on shipping, following the production spec.
Do not remove pending source rolls during unrelated cleanup.

## Working-directory caution

The shared workspace contains other lesson edits and prior video work. Do not
reset or replace unrelated changes. Transformer was shipped before this review;
its receipt is `video-audit/transformer-full-2026-09-10/v7/shipping-receipt.json`.
This note does not assert that an external tracker was updated or that a new web
deployment occurred.
