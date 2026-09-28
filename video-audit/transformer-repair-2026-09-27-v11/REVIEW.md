# Transformer v11 — review candidate

Built from the approved repair plan. **Unpublished.** Candidate: [transformer-v11.mp4](../../Prompts/transformer-v11.mp4).

Runtime **3:53.567**, 7,007 frames at 30 fps, 1280 × 720. This adds **7.300 seconds** to the published 3:46.267 video.

## What changed

At **2:25.47–2:54.23**, each example sentence is read in full before its existing clue explanation. The board highlights that sentence and then the corresponding clue paragraph, with one outline at a time. The rereads use the existing narrator from the opening. The fourth full sentence combines “The cat drank the milk” with “because it was fresh.”

| Reread | Inserted output interval | Published-source interval |
| --- | --- | --- |
| Please turn on the light. | 2:26.533–2:27.800 | 0:30.267–0:31.533 |
| The suitcase is light enough to carry. | 2:31.067–2:33.067 | 0:34.433–0:36.433 |
| The cat drank the milk because it was thirsty. | 2:37.567–2:40.033 | 0:41.533–0:44.000 |
| The cat drank the milk because it was fresh. | 2:43.333–2:45.800 | Prefix 0:41.533–0:42.833 + ending 0:47.700–0:48.867 |

The fourth sentence's internal join is at **2:44.633**. All times are half-open edit intervals including retained source lead/tail, not claimed exact speech onsets.

The brief “In the second” bridge at source **2:29.800–2:30.700** is removed so the second reread flows directly into “Carry indicates light means not heavy.” Existing “In our examples,” “It's the same for pronouns,” and the explanations are retained. No other narration is changed.

All rebuilt generated outlines use a fixed **4 px** width after camera transforms. Current canonical boards, full-view framing, illustrations, animation, existing surrounding gaps, and the standard closing sequence remain. The embedded IT border is not doubled. No new silence or automatic pauses were added; 5 ms edge ramps suppress discontinuities at audio joins.

## Continuous board durations

Durations include the entire board exposure, all changed highlights, camera movement, and held silence. New highlights do not reset a board's duration.

| Board | Candidate interval | Duration |
| --- | --- | --- |
| Two Problems Context Must Solve, first visit | 0:23.567–0:39.033 | 15.467 s |
| Two Problems Context Must Solve, second visit | 0:42.867–0:53.667 | 10.800 s |
| How Earlier AI Read Text | 1:01.600–1:21.967 | 20.367 s |
| How a Transformer Reads a Sentence | 1:32.100–1:42.600 | 10.500 s |
| How Context Changes the Numbers | 1:51.900–2:13.500 | 21.600 s |
| How the Transformer Resolves Meaning | 2:25.467–2:54.233 | **28.767 s** |
| How a Transformer Keeps Words in Order | 3:20.000–3:43.567 | 23.567 s |
| Standard close | 3:43.567–3:53.567 | 10.000 s |

Longest single teaching-board exposure: **28.767 s**, the approved expanded worked example, versus 21.467 s for this board previously. Longest adjacent teaching-board-plus-close chain: **33.567 s**. Actual added time was below the planning estimate; no filler was added to reach that estimate.

All original drawing breaks remain, including cat/IT/glass at 0:39.03–0:42.87 and 1:42.60–1:51.90; brain/monitor at 0:53.67–1:01.60; 2017/Transformer introduction at 1:21.97–1:32.10; active-data bars at 2:13.50–2:25.47; and the LIGHT/brightness, sarcasm, placeholder-IT and word-order drawings at 2:54.23–3:20.00. No donor graphics or replacement illustration was needed.

## Verification

- Full sequential decode: **7,007 frames**, correct dimensions and 30 fps.
- Compared **all 3,075 retained original-graphics/closing frames** with the source, plus **578 board frames** against the expected render. Maximum pixel MAE 2.977 / 255; mean 2.457 / 255, consistent with video encoding differences.
- Transition guard passed **26/26 boundaries**. Inspected every boundary strip across nine contact sheets: no stale frames or unintended transition flashes observed. The original 2017 illustration's fade-in remains intact.
- Inspected five prepared and seven encoded contact sheets, covering board/ring states, edited joins, original drawings, and literal final frame. Inspected a new clue-highlight frame at full output resolution.
- Measured **392 outline sides** across all seven rendered board legs. Median effective coverage is 4.14–4.20 px by leg; total range 4.09–4.47 px, including antialiasing/compression around the 4 px render target.
- Edited PCM exactly matches its source mapping outside the nine 5 ms join ramps. No gain change. Encoded AAC versus edited PCM: **42.512 dB SNR**, correlation **0.999973**. No audio truncation detected.
- Read the complete **612-word** candidate transcript. All four rereads and existing explanations are present. Both the isolated assembled sentence and the repaired passage transcribe correctly. Existing introductory, attention/transformation, fixed-weights, sarcasm/idiom, order and closing teaching remains.
- Measured encoded quiet intervals at −35 dB / ≥0.10 s; retained in `pause-measurements.json`. These measurements do not certify perceptual pacing.
- Protected source MP4, current lesson Markdown, video prompt, and all seven canonical JPG hashes remain unchanged. No page, prep-material, or publication edit was made.

## Listening still required

No real-time end-to-end watching/listening or perceptual audition of the splices was performed. Transcription, PCM identity, waveforms, and AAC correlation do not certify natural cadence, pronunciation, breath/noise-floor continuity, or invisible audio joins. The current status is **ready for owner review**, not a fully auditioned shipping certification.

Listen through **2:25–2:54**, especially **2:43–2:46**. The nine new join times are: 2:26.533, 2:27.800, 2:31.067, 2:33.067, 2:37.567, 2:40.033, 2:43.333, 2:44.633, and 2:45.800. An exact encoded audio excerpt is saved as `repaired-section.mp3`.

Phone readability and public-player playback were not checked. Original raw rolls are unavailable; the existing published MP4 is the only audio/video source, so preserved drawings receive one additional video encode. No tracker or deployment action occurred.

## Identity and evidence

- Source SHA-256: `d55f0000452087fb4b7993b2e79e06759ef263e147362cbd744a3c44883d9eb6`
- Candidate SHA-256: `557ba04f54762ffdec07d4d952be6545bac733c5abb8bd01127d8b45d229263a`
- Build: `scripts/video/build_transformer_v11.py` (uses the shared Renderer from committed `build_embeddings_v7.py`).
- Exact source/output mapping, board geometry, onsets, boundaries, and protected hashes: `edit-manifest.json`.
- Encoded verification: `verification.json`, `manual-review.json`, `audio-seams.json`, `pause-measurements.json`, `guard/transition-guard.json`, contact sheets, and `audio-check/edited.json`.
