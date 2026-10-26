# Does AI Think? repaired video review

Built on October 24, 2026 from raw version 4, with the approved passages from versions 5 and 6. The current three-row comparison board, Chinese Room board, and established highlighting treatment are in place. This is a review candidate; the installed course video has not been replaced.

**Candidate:** [does-ai-think-v12.mp4](/Users/davidobrien/Developer/AI-Training/Prompts/does-ai-think-v12.mp4)

**Length:** 3:11.83; 5,755 frames at 30 fps; 1280 × 720, H.264/AAC.

**SHA-256:** `ca5ab988af051c90294e46dc0907f8fb25e290a01a741b5cfb2c6c857cd29150`

## Narration changes

| Output time | Source | Result |
|---|---|---|
| 0:32.900–0:38.100 | Version 6, 0:39.400–0:44.600 | Exact qualifier: “But sounding like a person doesn’t tell you whether it understands things the way a person does.” |
| Join at 1:54.533 | Version 4 | Removed source 1:54.633–2:06.833, including the unsupported most-probable-word and lack-of-comprehension explanation. Learned patterns now leads into the cautious fluency bridge. |
| 2:22.033–2:31.267 | Version 6, 2:30.533–2:39.767 | Complete word-choice comparison: selecting words to express intent versus predicting the next word, then repeating. |
| 2:45.100–2:56.067 | Version 5, 3:56.267–4:07.233 | Useful-work explanation, replacing the categorical lack-of-comprehension and “nothing like a human brain” claims. |

The rest of the narration remains from version 4, including the full Chinese Room exchange, experience and meaning, uncertainty, the comparison takeaway, final qualification, and the exact two closing lines. Donor levels were adjusted against the neighboring base speech. Splices use measured quiet intervals and 5 ms room-tone crossfades. There is no narration time stretching or added teaching pause. A 1.53-second room-tone tail completes the standard close.

## Boards and pictures

- Current canonical board images are unchanged. Each first appears complete and unmarked, then uses complete-card or complete-row outlines and camera moves. The comparison highlights span both columns in the order Experience and meaning, Word choice, Uncertainty.
- Outlines use the established 4-pixel screen-space renderer. All active highlight rectangles remain inside the camera frame. Full-board opening views last 3.8 seconds for Chinese Room and 4.53 seconds for the comparison. Longest uninterrupted board exposure is 15 seconds.
- Retained supporting drawings explain lookup, returning the reply, prompt input, and uncertainty. The useful-work passage carries the matching version 5 drawings. Version 4 supplies the remaining supporting scenes.
- Corrected the opening diagram’s categorical inequality label to “Fluency alone does not prove understanding.” Removed the discarded mechanism diagram tail, the later categorical utility graphic, and the engine end slate. Applied the standard corner-mark cleanup.
- The canonical close lasts eight seconds, with the established hold, push, and settled ending.

## Completed verification

The complete encoded file was decoded and freshly transcribed with local base.en. The entire transcript was reviewed: all required teaching points and approved replacements are present; the removed claims do not remain in the transcript. This checks wording, not delivery.

All four encoded contact sheets (four-second samples), all 31 every-frame transition strips, and full-resolution board/highlight, corrected-label, and final-frame samples were inspected. No stray frames were found in those reviewed boundaries. The transition detector flagged six boundaries: frames 2035, 2230, 2894, 2924, 4797, and 4827. Each shows a continuous intended board camera move, rather than a short island of discarded imagery. The original detector FAIL result is preserved alongside this manual disposition.

Frame count and presentation timestamps passed. The 158 sampled encoded frames matched the intended renderer with minimum PSNR 34.56 dB. Encoded audio matched the assembled master at 45.00 dB SNR, with peak −1.41 dBFS and no clipping. Measured quiet gaps at the seven joins range from 0.60 to 0.91 seconds. All protected source, board, lesson, prep, index, and installed-video hashes remained unchanged.

The ring detector measured 101 of 111 samples at 4 pixels, two at 3 pixels, and eight at 2 pixels. The narrower detections occur during the initial Chinese Room zoom and on its full-board purple takeaway outline; full-resolution inspection confirms the intended outline, and the renderer maintains a fixed screen-space stroke. These color-threshold measurements are not evidence of changing the board font or stroke specification.

Evidence: `edit-manifest.json`, `qa.json`, `encoded-transcript.txt`, `encoded-sheets/`, `encoded-frames/`, `transitions/transition-guard.md`, and `rings/ring-stroke.txt` in this audit folder. Build and QA scripts are `scripts/video/build_does_ai_think_v12.py` and `scripts/video/qa_does_ai_think_v12.py`.

## Listening and playback still required

**Content and inspected visual checks pass. Final KEEP remains pending direct listening and continuous playback.** No direct audio listening or end-to-end audiovisual playback occurred in this environment. ASR, waveform measurements, and still-frame inspection cannot certify voice compatibility, breaths, pronunciation, cadence, or animation quality in motion.

The seven audio joins are at **0:32.900, 0:38.100, 1:54.533, 2:22.033, 2:31.267, 2:45.100, and 2:56.067**. Contextual audio from the actual encoded candidate is saved as `join-1-encoded.wav` through `join-7-encoded.wav`, with three seconds before and four seconds after each join. Check these during the full playback, especially the two version 6 passages and the version 5 useful-work passage.

The candidate is built and available for review. No installation, commit, push, or publication was performed.
