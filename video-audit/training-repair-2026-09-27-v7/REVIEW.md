# Training v7 — repair candidate, not published

**Lesson changed after this candidate was built (2026-09-27):** The current lesson places preparation and the phase overview first, then presents the loop as a pattern shared across all three phases, followed by the phase walkthrough. The Pretraining board and bridging text were revised. v7 retains the earlier sequence and board; its original KEEP assessment predates those edits. The current-flow feasibility review recommends a provisional narration repair: [review](/Users/davidobrien/Developer/AI-Training/video-audit/training-current-flow-review-2026-09-27/REVIEW.md).

Built after David approved the Training repair plan with “Build it please”. This is a narrow visual repair of the existing v6. Narration KEEP; candidate ready for owner review, not certified for shipping.

[Play candidate](/Users/davidobrien/Developer/AI-Training/Prompts/training-v7.mp4)

## Completed changes

| Output time | Change | Donor picture from current source |
|---|---|---|
| 0:49.000–0:56.000 | Internal-weights drawing replaces part of the adjustment explanation. | 0:25.000–0:28.900; play once, hold last frame for 3.1s. |
| 2:20.000–2:28.000 | Basketball drawing during the pretraining answer. | 0:10.900–0:18.567; hold last frame for 0.333s. |
| 3:03.000–3:12.000 | Basketball drawing during the instruction-tuning answer. | Same 7.667s donor, then 1.333s hold. |
| 3:52.000–4:05.000 | Basketball drawing during the preference-tuning answer. | Same donor, then 5.333s hold. |

The basketball donor ends on frame 556, before its exit dissolve. No loop restart or speed change was introduced. Each new drawing cut returns to the board at its current explanation state.

All six course boards were rebuilt from their unchanged canonical JPGs with fixed 4px highlights. Compact boards remain at full view; the tiny legacy push on Before Training Starts was removed. Dense phase boards preserve the existing complete-active-section camera paths and full-board openings. Source ring onsets and colors remain mapped to the published timeline; rings are naturally hidden during drawing breaks. The loop’s repeat line remains unmarked, preserving the previous removal of its banner-reading sentence.

Original narration, pauses, both existing voice grafts, opening pictures, frozen-weight handoff and closing picture are preserved. The video was re-encoded once from the published source because raw rolls are unavailable; AAC audio was copied without re-encoding.

## Continuous board durations

Counts include zooms, pans and inherited picture holds. Changing cards or camera position does not restart the board clock.

| Board | Runs after repair |
|---|---|
| The Training Loop | 19.900s + 5.333s |
| Before Training Starts | 19.300s |
| Three Phases of Training | 20.633s |
| 1 · Pretraining | 28.867s + 9.533s |
| 2 · Instruction Tuning | 25.467s + 12.200s |
| 3 · Preference Tuning | 27.800s + 11.900s |
| Standard close | 9.800s |

**Longest single teaching-board run: 28.867s. Longest adjacent-board chain: 49.500s**, previously 166.400s. Including the close does not increase the maximum because it is separated by the frozen-weights drawing. Residual 20–29s explanation spans are the approved pacing exceptions.

## Verification

- Exactly 8,696 frames, 30fps, 1280 × 720; runtime 4:49.867, unchanged.
- Original AAC packet hashes and decoded PCM hashes match exactly. This preserves existing joins; it does not certify their audible quality.
- All 18 settled highlight states, plus 6 camera-motion samples, measured 4px on all four straight sides in the encoded candidate. Background-relative measurement excludes canonical accent pixels with insufficient color contrast, which otherwise create false extra stroke pixels.
- All 33 automated transition checks passed; sequential strips for all 33 were manually inspected. This includes the eight new picture cuts and the old audio-edit boundaries.
- Every reused drawing frame was compared against its decoded donor; retained source picture frames and selected board states were checked for encoding differences.
- Canonical video, lesson Markdown and all seven current board JPG hashes remain unchanged. Index and asset registry were not edited.

## Remaining limitations and pre-existing issues

- Real-time full playback/listening, audible quality of the two existing voice grafts, phone/player readability and manual scrutiny of every encoded frame were not performed. Listen especially at 3:53.30–3:57.30 and 4:16.90–4:24.87.
- The opening’s photographed-paper-craft appearance remains flagged; no opening replacement was approved or built.
- Original Notebook loop diagrams remain outside this narrow repair. The reused weights drawing retains illustrative numeric labels and its “Optimal Output” label; these are source artwork, not verified model measurements.
- Dense camera views can crop inactive sections and the overall board heading, while retaining the complete active section and its ring.
- The original raw rolls are unavailable. The source snapshot is retained at the path in source-snapshot.json for this active repair; no permanent live-copy dependency was introduced.

## Evidence

- [Edit manifest](/Users/davidobrien/Developer/AI-Training/video-audit/training-repair-2026-09-27-v7/edit-manifest.json)
- [Verification results](/Users/davidobrien/Developer/AI-Training/video-audit/training-repair-2026-09-27-v7/verification.json)
- [Transition report](/Users/davidobrien/Developer/AI-Training/video-audit/training-repair-2026-09-27-v7/guard/transition-guard.md)
- [Builder](/Users/davidobrien/Developer/AI-Training/scripts/video/build_training_v7.py)
- [Verification script](/Users/davidobrien/Developer/AI-Training/video-audit/training-repair-2026-09-27-v7/verify-candidate.py)

Build command: `.video-venv/bin/python scripts/video/build_training_v7.py`. Existing candidates are protected from overwrite.

Source SHA-256: `01a8b51a707a59d6c29288ee9d86c5500aa5546882dc45c26b307f80d1755ebe`.
Candidate SHA-256: `f11f12ecc8a46594de330ed4725c5d83c06628691951442aa20a7ffd56126c13`.
