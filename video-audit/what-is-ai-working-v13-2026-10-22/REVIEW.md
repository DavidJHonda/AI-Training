# What is AI? — working cut v13

Candidate: `Prompts/what-is-ai-v13.mp4` — 2:32.4, 1280 × 720, 30 fps. Review only; not installed or shipped.

Approved scope: preserve the existing opening/definition, graft AI Is Everywhere from Why Learn AI?, use the current Two Types of AI board, remove learned-patterns explanation and superhero comparison, and stop before the closing message. The new lesson close is intentionally absent.

## Assembly

All intervals are half-open source frames at 30 fps. Sources are the stable, hash-verified finished candidates `Prompts/what-is-ai-v11.mp4` and `Prompts/why-learn-ai-v10.mp4`. Their hashes match the installed videos at build time. This assembly incurs one additional encode; it does not reconstruct all earlier approved edits from raw generations.

| Output | Source | Retained source frames |
|---|---|---|
| 0:00–0:42.8 | What is AI? v11 | 0–1284 |
| 0:42.8–1:44.5 | Why Learn AI? v10 | 1197–3048 |
| 1:44.5–2:14.9 | What is AI? v11 | 1284–2196 |
| 2:14.9–2:32.4 | What is AI? v11 | 2313–2838 |

The donor starts at its exact robot/phone scene cut, within the speech gap, and ends after “AI was already part of your day before chatbots arrived.” The return starts on the types introduction graphic. Internal v12 briefly restored 12 frames of the previous keyboard scene; v13 moves that scene tail before the graft and removes the flash without changing the retained words or total duration.

Removed source narration at 1:13.2–1:17.1: “It uses learned patterns to create a new output from your prompt.” The retained narration proceeds from the generative AI job to the definition of a prompt, then examples. The updated mechanism is displayed on the board; its exact new sentence is not newly voiced. The candidate ends after “This course focuses on generative AI.”

## Boards and camera

The exact current `course-assets/what-is-ai/what-is-ai-types.jpg` replaces all retained appearances of the old types board and the generative explanation graphic. The canonical JPG is unmodified. Native size 1600 × 1302; padded stage 2500 × 1408, offset (450, 53). Complete cards stay visible during the modest zoom. Outlines are rendered at a fixed 4 pixels after the camera crop.

| Output board span | Treatment |
|---|---|
| 1:49.633–2:04.2 | Full board first; recommendation card, job, then mechanism, using its blue accent. |
| 2:10.2–2:26.8 | Full board first; complete generative card with job, prompt explanation, and examples highlighted in purple. |
| 2:26.8–2:32.4 | Full board return, then neutral purple takeaway-banner highlight. |

The donor retains its existing board treatment and illustrations. The opening and recommendation example animation are retained. No new pause was inserted. Audio is resampled to 48 kHz mono and uses 5 ms ramps within the measured quiet joins. No gain change was applied: active RMS is approximately −17.9/−18.2 dBFS for the base sections and −19.4 dBFS for the donor.

## Verification

See `qa.json`, `transitions/transition-guard.md`, and `transcripts/what-is-ai-v13.txt` for the actual encoded candidate. The reproducible builder and QA script are `scripts/video/build_what_is_ai_working_v13.py` and `scripts/video/qa_what_is_ai_working_v13.py`. `edit-manifest.json` records source/asset hashes, camera specifications, timeline, and protected files.

Checks passed: 4,572 frames, 30 fps, continuous timestamps, maximum per-frame mean absolute pixel error 3.081/255, audio correlation 0.999982, and all seven transition gates. All protected hashes match. Encoded board states and transition strips were visually inspected. Browser playback metadata confirms 152.4 seconds, 1280 × 720, and no media error.

Verification includes every encoded frame against its selected source/render, decoded frame count and continuous timestamps, audio correlation against the intended PCM assembly, quiet joins, fresh transcription, and every-frame transition strips. Source course videos, lesson text, index, and canonical boards are protected by hashes.

Direct listening was not available. Voice continuity and perceived pacing at the donor joins remain for owner listening review. This is a working body cut, not a complete final lesson video.
