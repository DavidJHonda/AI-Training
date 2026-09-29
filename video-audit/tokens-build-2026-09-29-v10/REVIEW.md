# Tokens hybrid — review candidate v10c

Built from Version 1 with three Version 2 narration grafts and the complete approved short examples block from live v9. This implements the corrected, owner-approved plan in `../tokens-comparison-2026-09-29/REVIEW.md`.

Candidate: `Prompts/tokens-v10c.mp4`. Runtime **3:31.23**, 6,337 frames at 30 fps, 1280 × 720. Review candidate only; publication and direct listening are not certified. The earlier render was superseded to extend the Send outlines to the full shared white card; it is retained here as `first-render-superseded.mp4`. A second render was superseded after full-frame QA exposed three inconsistent incidental IDs in the early token-splitting diagram; `second-render-superseded.mp4` records that intermediate, and v10c corrects just its labels while preserving the animation.

## The shortened examples stay shortened

The examples occupy **2:31.80–3:04.77 (32.97 seconds / 989 frames)**. They preserve v9's source frames 6198–7186, including its existing framing, motion, and outlines:

- Basketball → basket + ball.
- Spaces and symbols: I, space + heart, space + AI; SP and the three-token count.
- The URL's eight-token count, without reciting its fragments.

All five rows appear in the full-board introduction. There is no second unbelievable walkthrough, no ChatGPT walkthrough, and no added recap. The later return-to-text illustration remains, as approved.

## Narration changes and listening locations

| Output | Change |
|---|---|
| 1:02.00–1:04.80 | Version 2: “A token can be a whole word or just part of one.” |
| At 1:52.13 | Remove the optional vocabulary-size aside, including the unsupported Claude comparison. Training/chat consistency leads directly into Send. |
| 2:04.03–2:14.77 | Version 2: complete 359 / 32898 / 24694 walkthrough and “Tokenization turns text into token IDs the model can use.” |
| 2:27.93–2:31.80 | Version 2: “A token ID identifies the token. Meaning comes later.” |
| 2:31.80–3:04.77 | The approved v9 examples, replacing Version 1's longer sequence. |
| 3:04.77 onward | Resume Version 1's return-to-text explanation and exact closing lines. |

Version 2 measured -19.91 LUFS against the base's -19.84 LUFS; its grafts receive +0.07 dB. The v9 examples measured -15.03 LUFS and receive -4.81 dB. This is level matching, not a new dynamic-normalization pass. Five-millisecond ramps occur only at actual audio splices. No internal explanatory pauses were added. The canonical closing motion uses source room tone through its settled tail.

The assembled-waveform detector places the edited gaps at 61.733–62.256, 64.418–65.181, 111.674–112.377, 123.727–124.296, 134.424–135.376, 147.629–148.180, 151.373–151.915, and 184.291–185.197 seconds. Final encoded measurements are in `encoded-check/silences.txt`. Detector boundaries and ASR timestamps are not proof of inaudible seams.

## Visual treatment

Current canonical JPGs replace actual course-board recreations. The chat stays at full view. Building Blocks retains its complete illustrated composition and receives a whole-card outline; the reuse drawing breaks the board before its brief banner return. Send and Cat remain complete and legible, with fixed 4 px outlines drawn after framing. Send's three column outlines span the full height of their shared white container. The short examples retain the approved complete-row camera treatment from v9.

The dictionary, reuse, vocabulary-building, training/chat, and return-to-text animations are retained. The exaggerated dictionary heading is replaced with “Whole-word lookup cannot cover every input,” preserving the surrounding animated scene. The early token-splitting diagram at about 0:57–0:59.57 now consistently labels un / belie / vable as 359 / 32898 / 24694; its original 482 / 15324 / 8912 labels conflicted with the lesson. This is a targeted visual correction discovered during final QA. The return diagram's source frame 6540 is brought forward over the outgoing URL fade, then its original motion continues. Native corner marks are cleaned on every retained Version 1 frame.

The close uses the current canonical JPG, a 48-frame hold, 150-frame push to 1.2×, and 120-frame settled hold. It is the literal final frame; no generated logo outro follows it.

Approved exceptions: the continuous Send → Cat → examples board run is **72.63 seconds**. Send alone lasts 22.63 seconds; the approved moving examples block lasts 32.97 seconds. No filler scene or extra example was inserted to break that run. The chat question, brief returning banner, and Send's first item begin within two seconds of arrival; the board is initially complete and unmarked, and rings follow the first spoken item under EDIT-SPEC rule 3's exception.

## Verification and limits

Build provenance, hashes, source/output frame mappings, gains, geometry, and source protection checks are recorded in `edit-manifest.json`. Fresh assembled narration transcription is in `audio-check/edited.txt`. A fresh transcript of the second encoded render is in `final-transcript/tokens-v10b.txt`; the final visual-only label correction uses identical assembled PCM audio. It recognizes all nine protected passages and the corrected token IDs, and confirms only the three approved examples.

Final decode, encoded-audio correlation, boundary checks, frame samples, and source-protection results are in `encoded-check/`. Final checks passed: all 6,337 frames decoded; all 16 declared boundaries passed the transition guard and their frame strips were visually inspected; encoded-to-assembled audio correlation is 0.9999868, with a -1.68 dBFS decoded peak. All seven protected live assets retain their hashes. The final AAC audio stream is byte-identical to the freshly transcribed second render (`audio-stream-identity.json`). See `encoded-check/results.json` for actual measurements. Canonical frames, outline states, sampled supporting visuals, transitions, and the closing frame are reviewed visually.

**Not directly auditioned:** the complete narration and donor joins still need listening review, particularly around 1:02, 1:05, 1:52, 2:04, 2:15, 2:28, 2:32, and 3:05. ASR, level measurements, and waveform correlation do not certify pronunciation, vocal continuity, or seamless audio. The examples also inherit v9's prior encoding generation. This file is a built review candidate, not a listening-certified shipping verdict.

The live video and canonical board assets remain unchanged. No commit, installation, deployment, or publication was performed.
