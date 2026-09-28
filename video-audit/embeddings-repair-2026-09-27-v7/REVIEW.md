# Embeddings v7 — review candidate

Built September 27, 2026 from the published Embeddings video. Not published.

Candidate: [embeddings-v7.mp4](../../Prompts/embeddings-v7.mp4), 4:26.567, 7,997 frames, 30 fps, 1280 × 720.

## Approved repairs

| Repair | Published-source interval | Candidate location |
| --- | --- | --- |
| Remove the redundant structured-grid recap; keep the definitions and proceed directly to Pepsi | 1:46.500–1:56.867 | Join at 1:46.500 |
| Remove “individual syllables”; retain the subword example and animation | Picture: 4:21.233–4:22.633; audio: 4:21.228–4:22.628 | Audio join at 4:10.861 |
| Render highlight outlines at 4 px after camera transforms | All five lesson-board sections | Throughout |

The repaired sentence reads: “Every one of those gets its own dedicated row of learned numbers in the table.” Full-candidate transcription confirms this wording. The two audio joins use 5 ms edge ramps, with no added silence or gain change.

Original illustrations, animations, camera paths, framing decisions, useful worked examples, and the closing card are retained outside the approved cuts. Student ID and Inside a Real Model retain the approved full-view framing. Canonical lesson boards, lesson text, prompt, and published MP4 remain unchanged.

## Continuous board durations

These intervals include zooms, pans, and pauses; camera movement does not restart the duration.

| Board | Candidate interval | Continuous duration |
| --- | --- | --- |
| Student ID | 0:18.367–0:34.633 | 16.267 s |
| Meaning in a Row | 1:04.333–1:46.500 | 42.167 s |
| A New Dimension | 1:46.500–2:17.200 | 30.700 s |
| Taste / AI | 2:23.433–3:12.367 | 48.933 s |
| Inside a Real Model | 3:17.567–3:58.600 | 41.033 s |
| Closing card | 4:14.500–4:26.567 | 12.067 s |

The adjacent Meaning in a Row / A New Dimension sequence is 72.867 seconds, down from 83.233 seconds. The longest single lesson board remains 48.933 seconds. These longer worked examples remain under the approved plan; no filler breaks were inserted.

## Verification

- Decoded the entire candidate: 7,997 frames at 30 fps.
- Compared all 2,624 retained original-graphics/closing frames and 562 board frames with their expected source or render. Maximum mean absolute pixel error was 3.006 on the 0–255 scale, consistent with encoding differences.
- Transition guard passed 19/19 boundaries. Inspected all 19 frame strips across seven contact sheets; no stale-frame flashes or unintended transition frames observed.
- Inspected five encoded contact sheets covering board states, both edits, and the ending.
- Measured 480 highlight sides across five boards. Effective encoded widths ranged from 3.784 to 4.432 px around the 4 px render target, including antialiasing and compression. Zooms do not enlarge the outlines.
- Edited PCM matches the source exactly outside the two cuts and 5 ms ramps. Encoded-audio comparison: 40.546 dB SNR, correlation 0.999958.
- Full edited-audio transcription confirms removal of both passages and retention of the required teaching statements.
- Protected source, lesson, prompt, and canonical board hashes are unchanged.

Evidence: `edit-manifest.json`, `verification.json`, `manual-review.json`, `guard/transition-guard.json`, encoded and guard contact sheets, and `audio-check/edited.json`.

## Check still required

No end-to-end listening or perceptual audio audition was performed. Signal measurements and transcription cannot certify natural cadence or an inaudible splice. Listen particularly at **1:46.5** and **4:10.9**. Short encoded-candidate excerpts are provided as `recap-join.mp3` and `phrase-join.mp3`. No deployment or live-player check applies yet because this is an unpublished review candidate.

## Identity

- Published source SHA-256: `a47d96f332712cba24a26bf7483eaaaf184bbac72327cd2499c20ebf5825237e`
- Candidate SHA-256: `14d9ba4b66ee5a698eaa5845e7ec08b931d5de33f93a5d798c92a486637dca94`
- Build script: `scripts/video/build_embeddings_v7.py`

## Shipping authorization

David approved shipping this exact candidate ("ship it") after the listening limitation was disclosed. Installed at `course-assets/embeddings/embeddings.mp4`, cache key `20260927ship1`; manifest hash and byte count updated. Existing technical and visual evidence applies to the identical installed file. Unperformed listening checks remain unperformed. Deployment is not awaited.
