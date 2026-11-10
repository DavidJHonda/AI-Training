# How AI Answers v21: assembled review candidate

**Release update:** Shipped locally by explicit user instruction. Commit `069e49c8` installs the approved 3:35.90 video, matching lesson explanations and canonical context board. Browser loading and asset-integrity checks passed. **Queued for batch deployment; no push or deployment performed.** The direct-listening limitation below remains accurately recorded. See `local-release.json`. The build-stage account below is retained as history.

Built from the approved donor plan and approved roll-8 insert. Candidate: `Prompts/how-ai-answers-v21.mp4`. Duration **3:35.90**, 1280×720, 30 fps, 6,477 frames. SHA-256: `d1509c90d2cc2d38c71a0e5efe7d93bcf2e3cdbd632bc1c74b77abebcdfe179e`.

## What changed

Roll 4 supplies the narration, starting at source 0:08.20 and ending after the closing hold at 3:20.61. Its generic introduction is removed. The 23.49-second roll-8 peanut-butter / salt example is inserted at source 1:39.26, after the first-token explanation. All other retained roll-4 teaching remains in order. No new pauses were added. Insert gain is +0.6283 dB; cut edges use the approved 5 ms ramps.

The pictures combine roll 5's question and evolving question-mark vector, the repaired roll-2 token reveal, roll 7's growing-answer connections and vector, roll 6's period arrival, and current canonical course boards. The complete blue demonstration was freshly captured from the current lesson, including the expanded question-plus-answer explanation. Probability highlights follow their spoken phrases. The end-of-answer signal stays separate from the displayed answer.

Preflight repairs widened the layer crop to retain both complete rows and moved the already-visible You vector forward to the beginning of its spoken explanation. The other growing-answer reveal anchors retain the approved proof timing. Technical donor headings and unspoken semantic boxes were removed.

## Output timeline

| Time | Picture / teaching |
| --- | --- |
| 0:00–0:16 | Dog question, empty answer, native token reveal |
| 0:16–0:36 | Before the Answer Begins, four spoken card outlines |
| 0:36–0:42 | Native token/layer connections |
| 0:42–1:05 | Question mark's starting numbers become contextual numbers |
| 1:05–1:25 | Current Same Token, Different Context board |
| 1:25–1:31 | Why the updated vector matters for prediction |
| 1:31–1:55 | Peanut butter / salt example; jelly and pepper appear as spoken |
| 1:55–2:03 | Prediction handoff |
| 2:03–2:22 | Full blue demonstration, first probabilities and You selection |
| 2:22–2:59 | Native question-plus-answer context animation |
| 2:59–3:16 | Full blue demonstration, name probabilities and Spot selection |
| 3:16–3:29 | Finished word sequence, period, separate stop signal |
| 3:29–3:36 | Canonical closing board with standard push |

## Verification

- Both complete media streams decode without errors; all 6,477 video frames were decoded sequentially.
- All 159 prepared frames match their encoded counterparts; maximum mean absolute pixel error 3.147/255.
- All 16 scene boundaries passed transition guard. Chronological encoded contact sheets, boundary pairs, and every-frame boundary strips were inspected. No stale-board flash was found.
- The assembled narration's 602-word ASR transcript retains the context explanation, learned-pattern example, both distributions, answer growth, stopping signal, and exact closing lines. The ASR spelling “U” is a transcription of the spoken token “You.”
- Decoded AAC compared with the assembled PCM: 45.59 dB signal-to-error ratio, peak 0.909, no clipping. Encoded audio padding is 704 samples (14.7 ms).
- Protected raw sources, canonical boards, installed video, and v20 remain unchanged. No installation, commit, push, or deployment was performed.

## Listening review still needed

Direct listening and uninterrupted audiovisual playback were not performed. Automated and still-frame checks do not certify voice continuity, cadence, or every phoneme at a splice. This is a completed review build, not shipping certification.

The six audio joins are at 1:31.06, 1:34.19, 1:39.83, 1:42.73, 1:51.47, and 1:54.55. `insert-joins.wav` provides 1:25–2:00 of the assembly for listening. The full video should receive an end-to-end listening/playback review before installation.

## Reproduction and evidence

- `scripts/video/build_how_ai_answers_v21.py`: pristine-source single-encode assembly and frame previews.
- `scripts/video/capture_how_ai_answers_full_demo.cjs`: current lesson panel captures; accepts output directory argument.
- `scripts/video/qa_how_ai_answers_v21.py`: sequential frame comparisons and complete media/audio checks.
- `edit-manifest.json`, `qa.json`, `transitions/transition-guard.json`, `transcripts/narration-check.json`: source hashes, timing, measurements, and assembled narration transcript.
