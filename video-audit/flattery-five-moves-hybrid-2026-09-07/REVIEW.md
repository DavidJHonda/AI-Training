# Flattery Trap: complete five-move hybrid

Status: ready for owner review, not shipped.

## Playback repair

The first export was H.264 High 4:4:4 Predictive / yuv444p. FFmpeg decoding succeeded, but that did not establish browser/macOS playback compatibility. After the owner reported the failure, the video was re-encoded as H.264 High Level 3.1 / yuv420p with fast-start metadata. Audio was stream-copied unchanged. The corrected file replaces the candidate at the same Prompts path; the original is retained as `playback-incompatible-yuv444p.mp4` in this audit folder.

Verified all 11,445 frames, unchanged 381.5-second duration, and identical AAC stream (SHA256 `bb9e0d07e78270ac75bf6b89a1c5c1bb9fe3ccd4e27166a198c5514edef74bc4`). Apple's AVFoundation reports playable and successfully decodes a frame using the native decoder. New candidate SHA256: `d9d61d0d2dc3a44d9f514d7ed40166b926ec8b0610b3821afe4abec8cd4c6f2b`.

The builder now explicitly sets yuv420p / High / Level 3.1 and checks the exported pixel format before completion. Existing visual QA below describes the same unchanged frame sequence before the compatibility re-encode.

Candidate: `Prompts/flattery-trap-five-moves-patched.mp4`

Length: 381.5 seconds, 11,445 frames at 30fps (6:21.5).

Builder: `scripts/video/build_flattery_five_moves_hybrid.py`.

## Content and pacing

The existing approved first section is reconstructed from `Prompts/flattery-trap.mp4`. Its earlier narration cuts are retained. The old abbreviated practical section and its duplicate caveat/takeaway are replaced by the approved donor `Prompts/flattery-trap-5-moves.mp4`.

All five weak comparisons and better prompts remain spoken, with explanations. The counterargument and saved-instruction caveats remain. The optional donor 1:23–1:30 explanation was retained for this complete first review, as communicated during the build. Owner can request further tightening after review.

Final-timeline landmarks:

- 3:05.9: new five-move introduction.
- 3:11.8: Ask, Don't Tell.
- 3:34.1: Ask for the Gaps.
- 4:01.4: Use a Rubric.
- 4:45.0: Argue the Other Side.
- 5:22.7: Set a Standing Instruction.
- 6:09.4: board takeaway.
- 6:13.1: exact current lesson closing, with narration from the original take.

## Visual repairs

- Correct FLATTERY TRAP title during precisely the original title-shot span (source frames 598–686). Code-native typography uses the existing paper surround and matching coral/cream/dark palette.
- Gatsby card sections highlighted separately on complete column-width rails.
- Three-part training board: establish, zoom, pan through complete components. Ring widths include the actual text, not just the narrower illustrations.
- Sycophancy: narrated phrases highlighted in the actual quote.
- Exactly 30 extra frames before OpenAI in the rollback transition; quote view held throughout.
- Full better-prompt bubble boundaries, full weak-prompt region with additional clearance, full rows for introductions, and the full takeaway banner.
- Retained native donor artwork at exact scene boundaries, interspersed with current board views.

## QA

`manifest.json` records all final-timeline chunks, states and 49 edit/highlight boundaries. `transitions/` contains every-frame strips for all 49. All strips were visually reviewed. No leaked old-graphic islands were found.

The generic transition guard reports nine alerts, at frames 984, 1275, 1563, 1788, 2010, 2898, 4869, 5755 and 6422. Each was inspected and is continuous intentional pan/zoom motion within the same current board, not an intermediate graphic. The raw automated report is retained unchanged; manual visual QA passes.

All settled highlight states were reviewed. The first render exposed a too-narrow training-flow ring and weak-prompt padding; both were corrected and inspected again before handoff.

The complete assembled audio was freshly transcribed and checked across the joins. The final visual correction preserves that reviewed audio bit-for-bit after PCM decoding: SHA256 `e8683ea5741c7297592862cc1f5e1156d59ac9628052e002fab261450136cecb`. Whole examples and sentence endings remain in the transcript. This is transcript/signal QA, not a claim of human listening review.

`integrity.json` verifies all 11,445 frames decode, no decoder errors, the inserted 30-frame pause has a silent interior, and the final frame matches the current closing image within normal encoding error (mean pixel error 0.48/255).

Both source videos and the live video are unchanged. This task did not write `index.html`. Its hash changed between rendering and final QA during concurrent work, which is recorded honestly in `integrity.json`; no attempt was made to revert or overwrite it.

No videos were deleted and no commit was created.
