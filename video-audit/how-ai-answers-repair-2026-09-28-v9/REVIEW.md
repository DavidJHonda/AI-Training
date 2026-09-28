# How AI Answers v9 — review candidate

Narrow repair approved by David: correct the banner highlight and abbreviate the ending to match the revised lesson. Built for review only; not published.

Candidate: `Prompts/how-ai-answers-v9.mp4`. Duration 217.633 seconds (3:37.6), 6,529 frames, 30 fps, 1280×720.
SHA-256: `273f4524b23c4e94e8605e110c9ea966862bfec5005dac91a6b5a27b76cd9cc0`.

Source: retained original published file, SHA-256 `c0e56437479d467ffaea26ff6ca51e93019e7cb18a041f3b980b038f7ff3f1fa`. Reconstructed the approved v8 visuals from the same original and lossless board rendering, so this is not a second lossy pass over v8. v8 remains unchanged.

## Changes

- 1:15.067–1:23.900: corrected banner ring to canonical JPG bounds x40–1560, y725–813 (plus the 23-pixel padded-canvas offset). The top edge moves down 5.6 delivery pixels. Nominal output stroke stays 4 pixels. Full-resolution encoded frame inspected at 1:20.
- 3:23.900–3:27.367: replace the removed inference board with an Inference title over the existing completed-answer token drawing. Preserve the spoken sentence: “This repeating cycle has a formal name, inference.” The title is an overlay on reused source artwork, not a new course board.
- Cut source 3:27.367–4:03.633 (frames [6221,7309)), removing 36.267 seconds: the Rank/Pick/Add/Repeat walkthrough and “Pulling back…” transition.
- At output 3:27.367, cut to the canonical closing visual. Hold its first frame for 10 extra frames to cover the source gap before the original close appears; then preserve its existing motion and final frame. Both closing lines remain.

## Narration and join

The lesson’s new summary is already taught at 1:34–1:43: selecting a token, adding it, and using expanded context to predict again. Changing likely continuations is explained at 3:03.84–3:14.18. The stopping token remains, followed by the retained inference definition and the two closing lines. The new lesson paragraph is not read verbatim, as approved.

Mapped the complete source transcript through the cut and ran fresh local ASR on the encoded ending (see `ending-asr.json`). It retains the stopping-token explanation, the complete inference naming sentence, “Every answer is built one token at a time,” and “The whole run is called inference.” ASR timestamps are approximate and do not determine the cuts.

Cut points were selected with decoded PCM measurements. Audio before and after the join is approximately −65 dBFS in adjacent 50-ms windows. The last audible tail ends around 3:27.25 and the closing sentence begins around 3:27.87, leaving about 0.62 seconds including the source breath/room tone. No new pause was added. Five-millisecond fades occur only on the quiet edges to avoid a discontinuity. Audio was encoded to AAC at 192 kb/s; correlation with the intended PCM assembly is 0.999915, SNR 37.66 dB.

**Listening still required at 3:23–3:30, especially the join at 3:27.367.** ASR and waveform measurements are not an auditory assessment.

## Visual and technical checks

- Full decode matches planned frame count, frame rate, dimensions, and duration.
- Compared all 265 corrected-banner frames, all 104 title frames, and 949 retained frames (including the complete closing sequence and transition handles) against the expected render or aligned v8 frames. Maximum mean absolute pixel error 2.940/255, within encoding tolerance.
- Transition guard passed 16/16 boundaries with 20-frame handles. Inspected all six every-frame contact sheets and three encoded-frame sheets. No unexpected visual islands or leaked inference-board frames found.
- Inspected corrected banner at full resolution and the title composition preview. Original short fade-ins in the preserved drawings remain.
- Protected source, v8, lesson, index, and canonical JPG hashes unchanged by this build.

## Continuous board durations

Camera movement and ring changes do not reset these durations. Existing drawing inserts do.

| Board | Continuous runs |
| --- | --- |
| Before the Answer Begins | 35.733 seconds |
| Why the Final Token Matters | 4.933 and 25.900 seconds |
| The Answer, Token by Token | 22.167 and 33.033 seconds |
| Former inference board | Removed |
| Standard close | 10.267 seconds |

The longest single board remains the approved 35.733-second exception. Longest board-to-board chain remains 40.667 seconds. The new Inference drawing lasts 3.467 seconds.

Reused source drawings retained from v8: question-token drawing at 0:54–0:58 and 1:28.300–1:33.967; intermediate tokens at 2:05.700–2:13.900; dog sketch extension at 2:54.933–3:03.933. The new title uses the completed five-token row from source 3:15.500. The old 3:48.500–3:52.500 drawing insert is inside the deleted walkthrough.

## Limits and status

No actual listening, continuous real-time playback, physical-phone test, or published-player check was performed. Unaffected narration retains the previously accepted simplifications (including early use of “word” and the abbreviated layers recap). This narrow repair does not claim a fresh full-production approval. Current lesson and video-prep files were not edited in this build; generation materials may still describe the removed board and should be reconciled before any future reroll.

Ready for owner review. No commit, publication, or deployment performed.
