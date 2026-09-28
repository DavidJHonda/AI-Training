# How AI Answers v8 — candidate review

Built for owner review on 2026-09-28. Not published.

Candidate: `Prompts/how-ai-answers-v8.mp4` — 1280×720, 30 fps, 7,617 frames, 253.9 seconds.
SHA-256: `018b61457cc0e3de27accab369ab171b171922149c0683e58db8b5255af05dda`.

## Approved repairs implemented

- 0:13.333–0:49.067: full-board opening, then complete-column framing and pans. Highlights remain a nominal 4 output pixels at 720p through camera changes.
- 0:49.067–1:23.900: compact final-token board stays fully framed; existing question drawing interrupts it at 0:54–0:58.
- 1:28.300–1:33.967: replace the invalid probability chart with the existing dog/question/token drawing. Preserve the following Once upon a time loop.
- 1:43.533–2:46.933: frame complete Prediction 1 and Prediction 5 groups, including their context and selected tokens. Reuse the animated You could name him sequence at 2:05.700–2:13.900 without revealing Spot early. The Reply so far outline encloses the heading and token row without crossing the heading.
- 2:54.933–3:03.933: extend the existing dog sketch over the conflicting You probability chart.
- 3:24.033–4:03.967: keep Rank/Pick/Add/Repeat fully framed with individual highlights; reuse the completed answer drawing at 3:48.500–3:52.500.
- Preserve original narration, useful remaining drawings, and the 4:03.967–4:13.900 close.

## Continuous board exposure

Zooms, pans, and highlight changes do not reset these durations. Actual drawing inserts do.

| Board | Continuous runs |
| --- | --- |
| Before the Answer Begins | 35.733 seconds |
| Why the Final Token Matters | 4.933 and 25.900 seconds |
| The Answer, Token by Token | 22.167 and 33.033 seconds |
| Inference: How AI Builds an Answer | 24.467 and 11.467 seconds |

The longest continuous individual board remains 35.733 seconds, an intentional approved exception. Longest uninterrupted board-to-board chain is 40.667 seconds (previously 70.567). The final inference board plus close lasts 21.400 seconds after the drawing insert.

## Verification

- Full candidate decoded successfully: 7,617 frames, unchanged duration.
- AAC stream and decoded PCM audio both exactly match the source by SHA-256.
- Compared 1,960 retained-source frames, 926 reused-drawing frames, and 544 repaired-board frames against their expected images. Maximum pixel MAE 3.194/255, within the encoding tolerance of 5.
- All complete-group camera checks passed. Ring bounds were checked throughout rendering. Measured 368 encoded ring sides: median 4.181 pixels, range 4.048–4.455 including antialiasing/compression.
- Automated transition guard passed all 17 boundaries with 20-frame handles.
- Manually inspected all nine encoded contact sheets and all six transition contact sheets, plus the corrected Reply so far preview. No unexpected frames, cut-off active groups, or outline/text collisions found in the inspected evidence. Original short animation fade-ins at 1:33.967 and 3:03.933 remain intact.
- Source video, lesson, current prompt, index, and canonical board images passed protected-file hash checks.

## Review limits

This is an encoded-frame, transcript/timing, and technical review. Actual listening, continuous real-time playback, physical-phone readability, and a newly published player were not checked. Audio identity verifies preservation, not a new listening assessment. Existing narration simplifications and previously approved omissions remain; this was a visual repair, not a narration rewrite. Owner review remains pending.
