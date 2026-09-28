# How AI Answers v10 — review candidate

Narrow repair requested by David: fit the first-board banner correctly and repeat the question before the Prediction 1 explanation, highlighting the question as spoken. Not published.

Candidate: `Prompts/how-ai-answers-v10.mp4`, 219.667 seconds (3:39.7), 6,590 frames at 30 fps, 1280×720.
SHA-256: `451fa414b0e0fbc971e71b6ccb7ae8d1663e001b1a1ed25c297466e373d73b3e`.

Rebuilt from the original published source (SHA-256 `c0e56437479d467ffaea26ff6ca51e93019e7cb18a041f3b980b038f7ff3f1fa`) plus lossless board composition; v8 and v9 remain unchanged. All v9 treatment, including its shorter ending, is retained outside these changes.

## Changes and exact timing

- **0:42.933–0:49.067:** fix the banner on **Before the Answer Begins**, the board in David's screenshot. Measured actual canonical JPG bounds x40–1560, y911–999. Previous bounds were y905–992. Applied both padded-canvas offsets (x198, y42). The purple outline now follows all four yellow edges, with the existing 4-pixel delivery stroke.
- **1:43.600–1:45.633:** insert the existing question recording from original source 0:11.000–0:13.033, retaining its complete spoken line and quiet margins: “What should I name my new dog?” No new voice or synthesized words.
- **1:43.767–1:45.633:** purple whole-question outline, including the YOU label, around canonical box x40–1560, y127–250 with padded-canvas offsets x281, y46. The board stays full-frame. The question begins audibly around 1:43.75; fresh ASR reports 1:43.74. The highlight clears before “Let's look at prediction one on the left.”
- Board entry remains 1:43.533, unmarked. The first item starts inside the initial two seconds, so its ring appears in the full view; the dive waits. Prediction 1 introduction now begins approximately 1:45.70; the existing dive starts 1:47.567. Later narration, highlights, drawings, and ending shift together by 2.033 seconds.

## Verification

- Full decode matches planned frame count, dimensions, frame rate and duration.
- Compared all 184 corrected-banner frames and all 61 inserted-question frames to expected render; compared 1,039 retained frames to aligned v9 frames. Maximum pixel MAE 2.972/255, within encoding tolerance.
- Measured encoded fixed-stroke widths: first banner 4.06–4.23 pixels; three measurable question sides 4.14–4.19 pixels including antialiasing. The left question accent shares the ring color, preventing independent color-based measurement there; its geometry was inspected at full resolution.
- All 20 transition boundaries passed the automated guard. Inspected all seven boundary contact sheets and three encoded contact sheets, plus full-resolution encoded banner and question frames. No unexpected frames or outline/text collisions found.
- Fresh ASR of the encoded join confirms the complete question followed by the complete Prediction 1 introduction. Source waveform measurements determined the cuts, since ASR timing misses quiet word tails.
- Audio assembled from original PCM with 5-ms fades only at quiet join edges, then encoded AAC 192k. Correlation with the intended assembly: 0.999867; SNR 35.64 dB. Existing closing join remains with the timeline shift.
- Protected hashes for source, v8, v9, lesson, index and canonical JPGs passed. No lesson edits or publication in this task.

## Board exposure

Durations include zooms, pans, and ring changes; these do not reset a board run. The question reprise adds to the first token-by-token run.

| Board | Continuous runs |
| --- | --- |
| Before the Answer Begins | 35.733 seconds |
| Why the Final Token Matters | 4.933 and 25.900 seconds |
| The Answer, Token by Token | 24.200 and 33.033 seconds |
| Inference title over drawing | 3.467 seconds |
| Standard close | 10.267 seconds |

Longest board remains 35.733 seconds, previously approved. Longest board-to-board chain remains 40.667 seconds. Reused drawing breaks: question at 0:54–0:58 and 1:28.300–1:33.967; intermediate tokens at 2:07.733–2:15.933; dog sketch extension at 2:56.967–3:05.967; inference title over completed tokens at 3:25.933–3:29.400.

## Limits and owner review

Actual listening, continuous real-time playback, phone playback, and published-player checks were not performed. Listen to the new question joins at **1:43.600 and 1:45.633**, in context from 1:40–1:50. The retained closing join is now **3:29.400**. Waveforms, ASR, and correlations do not certify natural cadence or absence of audible artifacts.

Unaffected narration retains the previously accepted simplifications and abbreviated layers recap. This is a narrow repair for owner review, not a new full-production or publishing approval. Video-prep materials may still describe the removed inference board; reconcile before any future reroll.

## Shipping approval

David approved shipping with “ship it.” Installed the exact v10 candidate and updated the course cache key to `20260928ship1`. Owner authorization follows the disclosed listening limits. See `shipping-receipt.json` and `shipping-verification.json`. Deployment is not being awaited.
