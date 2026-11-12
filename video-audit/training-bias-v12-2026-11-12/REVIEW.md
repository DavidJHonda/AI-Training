# Training Bias v12 · review candidate

[Play the candidate](../../Prompts/training-bias-v12.mp4) · [Timecoded transcript](qa/transcript/training-bias-v12.txt) · [Edit and source manifest](edit-manifest.json)

The full production cut is 2:35.83, 4,675 frames at 30 fps, 1280×720, with 48 kHz AAC narration. It uses version 2 as its audio base. The existing installed v11 is still in place.

| Candidate clock | Edit |
|---|---|
| 0:00–0:15.63 | Version 3’s student, teacher, mom and friend drawings, timed to version 2’s references to each speaker. Version 2’s accurate three-answer graphic follows. |
| 0:50.50–1:27.03 | Canonical Types of Training Bias board. Start unmarked, ring the whole purple card, cut to teacher-only training inputs, and return on the blue card. Removed the absolute claim that the AI will overlook an absent perspective. |
| 1:27.03–1:51.27 | Version 3’s student goes to the laptop. Version 1’s ten results appear, followed by the student’s reaction and typed follow-up. The shot cuts away before the raw visual labels the results “100% Tech Bias.” |
| 1:51.27–1:56.00 | Version 1’s complete evidence passage over its observed results. Version 2’s redundant instruction and data-cluster explanation are cut. |
| 1:56.00–2:15.70 | Canonical When You Suspect Training Bias board. All three cards remain in view as their outlines follow the spoken prompts. This is the longest uninterrupted teaching-board run, 19.70 s. |
| 2:15.70–2:28.50 | Version 2’s qualification about follow-up questions, illustrated with version 1’s broader-industries and missing-perspectives drawings. |
| 2:28.50–2:35.83 | The two spoken close lines over the canonical pill and sticky. The summary-graphic announcement and engine slate are cut. The close holds, pushes to 1.2× and settles. |

**Encoded-file verification.** Decoded every frame, checked sequential timestamps, tested every borrowed shot against the mapped frames from its original recording, and verified each of the five highlighted card states and the literal final frame. The [transition guard](qa/transitions/transition-guard.md) passed all 16 declared picture boundaries. Inspected the shots on both sides of each splice and the [board states](qa/board-states.jpg). The [audio/source checks](qa/output-checks.json) matched all five continuous narration spans with correlation above 0.99998. The final transcription contains all seven required spoken passages. Source hashes and the candidate fingerprint are in the manifest.

**Listening checkpoint.** The voice switches at 1:51.27 and returns at 1:56.00. The donor was matched by active-speech RMS (+1.41 dB). The measured quiet intervals across those joins were 0.81 s and 0.73 s; the other two narration edits retained 0.82 s and 0.93 s. No extra listening exercise or artificial pause was inserted. Direct human-speed audiovisual playback and a subjective listening pass were unavailable during this build. Wording, levels, timing and frame checks do not establish a natural voice match; listen from about 1:48 through 2:00 for cadence before shipping.

## Local shipment · 2026-11-12

Owner approved shipping v12 after disclosure of the listening limitation above. Installed the reviewed bytes locally in commit `eeb4f190` and verified the local HTTP response and committed MP4 against SHA-256 `dc4353cb70e954127fcd579f7c6007ed09cd043ebceee2e038b368e3c70fe614`. The release snapshot passed the full asset hash check. In the working tree only, concurrent Document Trap and Trust Trap image edits differ from their recorded hashes. Queued for batch deployment.
