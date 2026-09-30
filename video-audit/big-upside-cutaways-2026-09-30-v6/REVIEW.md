# Big Upside v6 visual repair

Status: built and visually verified; ready for candidate review. Authorized by “Agree. Build it please.” after the live-video evaluation. Not shipped.

The four new cutaways make the six-example section more concrete. The brief unfinished “Documented AI Milestones” scene is replaced by the existing everyday-life takeaway. Narration and the 4:17.30 timeline are preserved.

## Changes

| Output time | Treatment |
|---|---|
| 2:03–2:11 | Doctor reviewing an AI-flagged possible scan finding. |
| 2:25–2:30 | Researcher testing a computational candidate in the laboratory. |
| 2:51–2:57 | Student using a phone to read a menu aloud. |
| 3:17–3:22 | One camera-guided nozzle spraying a weed between healthy crops. |
| 3:29.93–3:31.63 | Hold the everyday board's final takeaway instead of showing nearly empty milestone cards. |

Both affected boards use their exact canonical JPGs, original full-view openings, existing card-name highlight timing, and original restrained camera paths. Their rings are now fixed 4px at 720p. Each new supporting scene has a gentle 2.5% push. All other source visuals, including the standard close, retain their original timeline.

The health board's longest continuous exposure is now 21.37 seconds; the everyday board's is 20 seconds, down from 55.23 and 53.07. Across consecutive boards, the longest run is 36.83 seconds, down from 123.77. The unchanged timeline board still has its previously approved 24-second first span. No silence or pauses were added.

## Sources and implementation

- Candidate: `Prompts/big-upside-v6.mp4`.
- Source: `course-assets/big-upside/big-upside.mp4`, SHA-256 `a7d56ee3a5a5f4e4968c125719077130c7317f31872fc1c52d3ce22ecffb4c06`, verified against the public file during the preceding evaluation.
- Source limitation: raw rolls and lossless intermediates are absent. This build uses one picture encode from the verified v5 file and copies its AAC stream, avoiding a new audio encode.
- Build: `scripts/video/build_big_upside_v6.py`.
- QA: `scripts/video/qa_big_upside_v6.py`.
- Generated assets and exact prompts: [supporting scenes](../../scripts/video/assets/big-upside-cutaways-2026-09-30/README.md) and [PROMPTS.txt](../../scripts/video/assets/big-upside-cutaways-2026-09-30/PROMPTS.txt). Built-in image_gen was used. The menu scene received a targeted correction so the rear camera points toward the menu.
- Frame ranges, source/asset hashes and all edit boundaries: `edit-manifest.json`.

The new pictures are illustrative scenes, not records of particular patients or experiments. The scan's alert calls for review; the lab image represents research rather than a clinical cure. The approved narration retains those qualifications.

## Verification

Source images and rendered start/end previews inspected: intended action visible, readable scan alert, plausible menu-camera orientation, targeted spraying, crop-safe framing, complete board cards and takeaway rings.

The finished MP4 passes the encoded checks in [verification.json](verification.json):

- 7,719 decoded frames, 30 fps, 1280×720, 257.30 seconds.
- Both the compressed AAC payload and decoded PCM match the source exactly.
- All 33 encoded preview comparisons pass; maximum mean absolute channel error is 3.44 on the 0–255 scale.
- All 4,419 frames outside the repaired region match the source within the compression tolerance: mean error 2.43, maximum 2.88. This is one additional picture encode, not a lossless copy.
- Source video, lesson text, canonical JPGs and generated source PNGs retain their protected hashes.
- All 27 [transition checks](guard/transition-guard.md) pass, with zero flagged short visual islands.

Visually inspected all 11 affected every-frame transition strips: eight cutaway entry/exit points, the two rebuilt board starts, and the final board-to-question cut. Also inspected the four encoded scene starts, replacement takeaway hold and literal final frame. The joins contain the intended images, the unfinished milestone cards are gone, and the original close remains intact. These checks do not constitute continuous audiovisual playback.

Candidate SHA-256: `19002f4eaef7fa1a8bc984acec41fc682c164bf8a206870cedae2cf2fe91aae7`.

## Listening and release status

This is a narrow visual repair. Direct listening and continuous audiovisual playback have not been completed. Existing pronunciation questions for Hassabis and abaucin, and the older donor narration at 3:31.63–3:38.43, carry forward. The repair introduces no new audio join. Do not interpret automated checks or unchanged audio as a new listening certification.

The canonical video, lesson, website reference and deployment are not replaced by this build. Shipping is not requested or performed.
