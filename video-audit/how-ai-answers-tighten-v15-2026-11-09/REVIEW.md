# How AI Answers v15 review

Candidate: `/Users/davidobrien/Developer/AI-Training/Prompts/how-ai-answers-v15.mp4`

SHA-256: `868053d29e39724862a544b44af9438faccdaf62bd2510536f05b7fbc9b88964`

Duration: 2:49.433, 5,083 frames at 30 fps, 1280x720. Removes 45.500 seconds from the accepted v12.

## Authorized scope and result

David approved the proposed redundancy cuts and wider token graphic with “Agree. Build it please.” This is a review candidate, not a local shipment or publication. No course content, canonical image, canonical video, manifest, or lesson reference was changed by this build.

The initial final-token preview and repeated reading-to-writing introduction were consolidated into the explanation at 0:39-0:55. The other final-token teaching moment is the switch to “him” at 1:38-1:43. The launching-pad restatement, second probability calculation, repeated question-mark explanation including “solely,” and first inference definition are removed. The dog-name/“You” explanation, end-of-answer token explanation, and complete canonical closing narration remain.

| Removed passage | Original v12 seconds | Output join seconds |
|---|---|---|
| Repeated reading-to-writing setup and initial final-token preview | 39.200-58.867 | 39.200 |
| Launching-pad restatement | 74.900-83.000 | 55.233 |
| Repeated final-token probability calculation | 85.900-93.433 | 58.133 |
| Repeated question-mark explanation, including solely | 107.333-113.600 | 72.033 |
| First inference definition; retain the closing definition | 200.767-204.700 | 159.200 |

All five joins were placed in measured quiet. Only 5ms fades at the new seams change the retained PCM. No new pauses, generated voice, donor voice, or time stretching.

## Picture

The new landscape scene runs from 1:08.233 to 2:02.667. The question stays across the top, the growing answer is large on the left, and three compact probability rows appear on the right. The combined remainder is a smaller line. The latest token is highlighted; each selected token moves from its probability row to its position in the answer. The existing lesson probabilities are unchanged and identified as illustrative. Content ends above y=610, leaving the bottom 110 pixels clear for player controls.

A fixed layout keeps earlier words in place. Punctuation uses the same baseline as the words; highlight backgrounds are drawn before reply text. Six token arrivals follow the spoken demonstration, including punctuation before the completed answer is read.

Before the Answer Begins retains its canonical asset, original dense-board camera, and highlights through the layers explanation. Why the Final Token Matters opens as the full unmarked canonical board for approximately three seconds, then highlights the question and final-token cards with their narrated explanation. The longest retained canonical-board run is approximately 25.9 seconds; the new animated demonstration is 54.4 seconds. The existing dog illustration, loop drawing, EOS drawing, and close are preserved.

The loop entrance holds the preceding keyboard image for 16 frames after the new audio cut, removing a short leftover question graphic before the original loop animation starts. This changes picture only.

## Source reconstruction

The original source snapshot had been removed from temporary storage. Its exact bytes were recovered from `git ec30a9f5:course-assets/how-ai-answers/how-ai-answers.mp4` into `/private/tmp/how-ai-answers-v13-source.mp4` and verified against SHA-256 `c0e56437479d467ffaea26ff6ca51e93019e7cb18a041f3b980b038f7ff3f1fa`. Retained picture was rebuilt through the original v8-v12 treatments and encoded once. Original PCM reconstruction was checked sample-for-sample against the accepted v12 assembly. The previous candidates were not used as lossy picture inputs.

The build scripts, renderers, manifests, source hashes, PCM, frame samples, and code snapshots are retained in this audit directory. v13 and v14 are intermediate review builds; v15 is the candidate to review.

## Completed verification

- Full encoded audio/video decode passed; exact planned count and duration verified.
- All 37 declared boundaries passed the transition guard, with no flagged short scene islands.
- 60 encoded frames compared to render references: maximum absolute mean error 3.035/255, maximum detail error after the measured color-conversion offset 1.139/255.
- 100 retained-picture samples compared against accepted v12: maximum mean difference 0.392/255.
- Encoded PCM correlation 0.99988310; signal-to-noise ratio 36.26 dB. Protected lesson/source/canonical assets passed their hash checks.
- Fresh small.en transcription of the tightened narration confirms intact retained wording, both probability lists, no clipped-word fragments at the five cuts, and one inference definition. The final v15 encoded AAC stream is byte-identical to that transcribed audio; `audio-identity.json` records the check. ASR renders spoken “You” as “U” in some lines; the graphic correctly reads “You.”
- Inspected encoded join and flight contact sheets, settled token states, the final period at full size, and the final close. Verified the review player in Chrome, including jump controls, metadata duration, and no horizontal overflow at desktop or 390px widths.

## Limits and review

No perceptual listening or uninterrupted whole-file playback was performed. Automated transcription, frame checks, and PCM correlation do not certify natural sound. Listen to the five joins at 0:39.200, 0:55.233, 0:58.133, 1:12.033, and 2:39.200. `review.html` has buttons that begin playback three seconds before each join; contextual WAVs are in `join-audio/`. No fresh phone-device playback or public-player verification is claimed. This candidate is ready for owner review, not declared ready to ship.

## Commands

```sh
.video-venv/bin/python scripts/video/build_how_ai_answers_v15.py
.video-venv/bin/python scripts/video/qa_how_ai_answers_v15.py
NODE_PATH=/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules node video-audit/how-ai-answers-tighten-v15-2026-11-09/check-review.cjs
```
