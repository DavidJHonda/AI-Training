# Flattery Trap v13 — shortened Sycophancy board

2026-10-27. Review candidate completed for the request to match the edited lesson and identify any related narration cuts. Not installed, committed, or published.

Candidate: `Prompts/flattery-trap-v13.mp4`, 4:25.133, 7,954 frames at 30 fps.
SHA-256: `ffec02f6916c47d6226324894af8731a76a1c884cfc9d0922843dbb006bb7031`.
An 18-second excerpt, `board-preview.mp4`, begins at full-video 2:10.

## Lesson comparison and cuts

Compared current `index.html`, `lessons/flattery-trap.md`, their uncommitted diffs, the current board JPG, and the v12 release record. The installed course video and stable v12 candidate both hash to `216955359bc279aca9097bd3792797c5512ce959ae246edbf78ddca173cc9c1c`.

- The Sycophancy board now contains only the first paragraph. Replace the old two-paragraph board at frames [4000, 4317), 2:13.333–2:23.900.
- No quote narration cut is needed. The video reads only “Honestly, this is absolutely brilliant” and “It's not just smart, it's genius,” both retained in the current board. The deleted second paragraph was never spoken. The existing source transcript and v12's verified copied prefix establish this correspondence.
- The prose before the training board lost its repeated explanation of reviewers, agreeable answers, and training. These ideas remain in the current board. The video explains them once during the board walk at approximately 1:32–1:52, so removing them would remove the board's explanation rather than eliminate repetition.
- V12 already includes the three tactics and saved-instruction tip. Those changes require no further cuts. The new LAB checkbox UI has no corresponding video passage.

## Board treatment

| Board | Highlight | Camera | On screen / breaks |
|---|---|---|---|
| Sycophancy | Unmarked opening, then one editorial-purple outline around the complete shortened response card at existing frame 4152 (2:18.400) | Compact; complete board, static, same full-width fit as v12 | 10.567 seconds; existing gag-product illustration before, existing rollback illustration after |

Uses the exact current 1600×479 JPG on a 1600×900 temporary canvas, offset [0, 210]. Native card edges are [40, 127, 1560, 439]; the outline is fixed at 4 output pixels. No new narration, pause, zoom, or timeline change. This carries forward the established full-view and highlight timing, fitting the outline to the newly shortened card.

## Encoding and verification

Only the 317-frame board span is encoded. Its endpoints are existing keyframes and the replacement matches the source's codec configuration. Every other video packet and every audio packet is copied directly from stable v12. Original raw rolls are unavailable; unaffected material incurs no new encoding generation.

- Complete output decode: 7,954 frames, 30 fps, uniform 512-tick presentation intervals.
- All 7,637 unaffected frames are pixel-identical and their encoded packets/timestamps are identical to v12, including the ending.
- All 12,430 AAC packets, their timestamps, and the complete decoded audio are identical to v12.
- Current source, canonical board, and candidate hashes verified.
- Three transition boundaries pass the automated guard. All three every-frame boundary strips were visually inspected: clean board entrance, highlight appearance, and return to the original rollback illustration.
- Encoded full-size board frame inspected: correct shortened wording, readable full-width layout, complete card outline, no clipping.
- Direct listening and continuous audiovisual playback were not performed. This is a verified visual-only review candidate, not a new whole-video shipping certification; v12's previously documented listening limitations remain.

## Reproduction

Build: `.video-venv/bin/python scripts/video/build_flattery_trap_v13.py`

QA: `.video-venv/bin/python scripts/video/qa_flattery_trap_v13.py`

The builder refuses to overwrite the candidate. Retained `source-4000.jpg` supplies the existing video background color. `edit-manifest.json`, `qa.json`, encoded frames, and transition strips retain the verification evidence. No course asset or lesson source was changed by this task.

## Local release — 2026-10-27

David approved: “Looks good. Ship v13 locally.” This supersedes the review-only status above.

- Local commit: `9eb14c585cec205e2d236c96aec302caaa1a146d`.
- Installed and committed `course-assets/flattery-trap/flattery-trap.mp4` SHA-256: `ffec02f6916c47d6226324894af8731a76a1c884cfc9d0922843dbb006bb7031`, matching the verified candidate.
- Course reference updated to `?v=20261027ship13`; displayed runtime stays `4 min` (exact 4:25.133).
- Release includes the shortened canonical Sycophancy JPG, matching accessibility/lesson text, and its renderer. Unrelated edits, including LAB changes, remain uncommitted. Build and audit records retained locally.
- Staged inline JavaScript syntax, whitespace, video/board hashes, installed file, and committed blob checks passed. Existing candidate verification applies to the identical installed bytes. Previously disclosed listening limitations remain recorded; no new listening claim is made.
- Shipped locally; queued for batch deployment. No push or deployment performed.
- Scoped post-commit cleanup removed one regenerable canvas PNG. Candidate, source-frame reference, review excerpt, and QA evidence retained.
