# Flattery Trap v12: restore the transition

2026-10-23. User requested restoring the live video's table transition with only the word “five” removed.

Candidate: `Prompts/flattery-trap-v12.mp4`, 4:25.133, 7,954 frames at 30 fps. SHA-256: `216955359bc279aca9097bd3792797c5512ce959ae246edbf78ddca173cc9c1c`.

The narration is now: “This table outlines ways to fight the flattery trap.” The full, unmarked three-tactic board is visible during the transition. All subsequent v11 editorial choices remain. This restores 101 frames (3.367 seconds) relative to v11.

## Source and edit

Rebuilt from verified `Prompts/flattery-trap-v10.mp4` using v11's builder, avoiding an additional encode generation from v11. Original source hash and canonical-board hash are enforced. First 4,712 video packets and decoded frames remain exact copies.

Source word removed: [162.333333, 162.700000), frames [4870, 4881). These boundaries are in quiet shoulders around “five,” with a 5 ms fade on each side. Measured 10 ms RMS around the edges is −48.71 and −42.88 dB. No other words are removed from the sentence. Original following sentence remains: “The first move is ask, don't tell.”

The full-board introduction begins at 160.867. Existing first-tactic highlight and camera timing follow after the restored sentence. No board layout or lesson changes.

## Verification

- Encoded transition re-transcribed using small.en: exact requested sentence, no “five,” neighboring “outlines” and “ways” intact. See `encoded-transition-transcript.json`.
- Complete decode: 7,954 frames, 30 fps, uniform 512-tick presentation-time increments.
- All 13 declared transition boundaries pass automated stale-frame checks. The three restored-introduction strips (4826, 4870, 4927) inspected: correct new board, no flash or picture jump at the word cut.
- Source cut-edge RMS and encoded audio comparison passed; correlation around the word splice is 0.999993 against assembled PCM.
- All assembled narration after v12 frame 4927 is sample-identical to v11 after frame 4826; the added transition is the only audio change from v11.
- A ten-second encoded excerpt at 2:37 is saved as `transition-preview.mp4` for listening in context.
- Direct listening was not performed. Automated transcription and waveform/codec checks do not establish perceptual smoothness; the preview is available for that review. V11's other documented review limitations remain.

No installation, Git commit, or deployment. The canonical course video remains unchanged pending review.

## Reproduction

`.video-venv/bin/python scripts/video/build_flattery_trap_v12.py`

`.video-venv/bin/python scripts/video/qa_flattery_trap_v12.py`

The builder refuses to overwrite a candidate. The earlier rejected trial word-cut WAV is explicitly named `rejected-cut-4858-4871.wav` and is not used in the candidate.

## Local release — 2026-10-23

David approved the candidate: “Looks good. Ship v12 locally.” This supersedes the pending-installation status above. The documented direct-listening limitations remain accurately recorded; no additional listening claim is made.

- Installed at `course-assets/flattery-trap/flattery-trap.mp4`; candidate, installed file, and committed blob SHA-256 all match `216955359bc279aca9097bd3792797c5512ce959ae246edbf78ddca173cc9c1c`.
- Local commit: `1054a860037282441d480ed0fd7e2c28a3ba5ffc`. Includes the approved three-tactic board, matching lesson text and accessibility content, and board renderer/metadata adjustments. Other lessons' working edits were left out of the commit.
- Course reference: `?v=20261023ship12`, displayed runtime `4 min`; exact runtime 4:25.133, 7,954 frames at 30 fps.
- Installed metadata, staged JavaScript syntax, asset metadata, and Git whitespace checks passed. Existing candidate decode/splice checks apply because the installed bytes match exactly.
- Shipped locally; queued for batch deployment. No push or deployment performed.
- Scoped v11/v12 render-scratch cleanup completed after commit: 10 regenerable files, 0.06 GB reclaimed. Candidates, review records, previews, manifests, transcripts, and transition strips retained.
