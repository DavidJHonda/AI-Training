# Flattery Trap v9 — approved targeted repair

Candidate: `Prompts/flattery-trap-v9.mp4`.

Authorization: David's “Agree to all. Build it please.” approves the three-part plan in `video-audit/flattery-trap-live-review-2026-09-29/REVIEW.md`. This is a review candidate; shipping and publication were not requested.

## Result

- Remove the complete “Because sycophancy…ensure we get honest answers” sentence, source 2:40.933–2:49.333.
- Remove the complete “By giving the AI…prevent it from simply agreeing with us” sentence, source 2:53.000–2:59.600.
- Enlarge the complete active Gatsby comparison card by approximately 47%. Keep the full-board introduction, scenario and takeaway; introduce each card with its whole-card outline before highlighting its spoken sections. Ring width uses the current shared 4 px at 720p renderer. The whole-card outline follows the white card edge, excluding its shadow.
- Correct the opening diagram label to “Training can reward agreeable answers.” The correction follows the original slide-in and fade. The rest of the diagram's animation is retained.
- Preserve all five moves, their limitations, the existing illustration cutaways, and the standard close.

Planned output: **9,431 frames at 30 fps, 5:14.367**, exactly 15 seconds shorter. No extra teaching pauses.

The original raw rolls no longer exist in `Prompts/`. The build therefore uses the verified live v7 MP4 as its source and the canonical comparison JPG for the rebuilt board. It performs one new video encode at CRF 16. It does not stack the repair on the intermediate v8 candidate. V8 was an internal first encode; v9 tightens the whole-card outlines to exclude shadows.

## Sources and implementation

- Source MP4 SHA-256: `9c926d2868c198ec14ef3b3cec206f4c00a2f0549e8fa2e74b1505e7cec6fb31`.
- Comparison JPG SHA-256: `acc368d0445a88c73253f6c17b6c417e091893013f87d08717c7933d290ebe2d`.
- Builder: `scripts/video/build_flattery_trap_v8.py --version 9`.
- QA: `scripts/video/qa_flattery_trap_v8.py --version 9`.
- Exact timeline, camera path, ring targets, source identities and output hash: `edit-manifest.json` and `comparison-spec.json`.
- Label translation and reveal opacity for every affected frame: `label-tracking.json`.

The source and board hashes are checked before and after rendering. Neither the source MP4, JPG, lesson nor site reference is overwritten.

## Audio and picture joins

Audio cut boundaries are the approved frame boundaries inside measured silences. PCM slices retain their exact sample count; 5 ms fades inside the silence smooth the two joins without adding time or overlapping spoken words. Audio is then encoded once to AAC.

| Output join | Kept words around the join | Planned retained gap |
|---|---|---|
| **2:40.933** | “…it has not disappeared.” → “This table outlines five ways to fight the flattery trap.” | About 0.571 s |
| **2:44.600** | “…five ways to fight the flattery trap.” → “The first move is ask, don't tell.” | About 0.416 s |

Two necessary picture adjustments avoid flashes at the first join:

- Hold source frame 4821 over source frames 4822–4827, preserving the training-model scene for the final six frames before the cut. Without this, the cut would strand six frames of the removed speech-bubble scene.
- Show the Five Ways opening frame over source frames 5080–5082. Its original visual cut was three frames later than the approved audio cut. The complete board is visible immediately on the new side of the splice.

These short holds change no audio and add no time. The board still has over three seconds of unmarked introduction before the first strategy ring.

## Board plan as built

| Board | Output span | Treatment |
|---|---|---|
| Flattery vs. Useful Feedback | 0:23–1:22.90 | Full view and scenario; whole Flattery card then its spoken sections; return to full view; whole Useful Feedback card then its sections; full-view takeaway. Complete active card visible throughout camera moves. |
| How the Praise Got Baked In | 1:22.90–1:52.83 | Preserve original readable full view and sequence. |
| Sycophancy | 2:13.33–2:23.90 | Preserve original short excerpt and framing. |
| Five Ways to Fight the Flattery Trap | Begins 2:40.933 after the cuts | Preserve existing complete-row zooms, highlights and supporting cutaways. |
| Closing message | 5:04.60–5:14.367 | Preserve original canonical closing graphic, push and final settled hold. |

The longest uninterrupted **single-board** span remains the 59.9-second Gatsby comparison. It is actively taught throughout and now has complete-card camera movement, as approved. It runs directly into the 29.93-second training board, so the longest consecutive sequence of course boards is 89.83 seconds. The Five Ways section retains its existing breaks; its longest single leg is 42 seconds. No custom filler illustration was added.

## Verification and limits

Final encoded verification is recorded in `qa.json`, `transitions/transition-guard.md`, the native-size `encoded-frames/` folder and the measured `encoded-audio-silences.txt`. No preview alone is treated as proof of the final encode.

Completed checks on the actual v9 MP4:

- Decoded **9,431 frames at 30 fps**, matching the 5:14.367 plan exactly.
- Both source and canonical board retain their original hashes. Candidate SHA-256: `26a48f97db2ece2374d2849ac7730d39c68d19fe083f6cb709bc450d0ce5f4f0`.
- Inspected all ten new ring states at native delivery size, the label during its fade and settled state, and the literal final frame. Complete active cards and text remain visible.
- Compared 124 samples from unchanged scenes against their mapped source frames: mean absolute pixel difference 2.29/255, maximum 2.72/255. These are re-encoded source scenes, not claimed to be bit-identical.
- Encoded audio correlates **0.999988** with the planned PCM; RMS error 0.000649. Exact intended output audio length is 15,089,600 samples at 48 kHz.
- Measured retained gaps are **0.571396 s** and **0.416208 s**, matching the plan. Sample jumps at the joins are 0.00000370 and 0.00001182 of full scale. These measurements do not replace listening.
- All five actual edited scene/splice boundaries pass the transition guard. The broader 19-boundary diagnostic flags the ongoing camera dive near frame 1640: consecutive moving frames 1628–1630 cross its frame-difference threshold. Inspection of the every-frame strip shows continuous movement into the right card, not a stale visual. The original automated FAIL result is retained; `manual-transition-review.json` records this specific false-positive disposition and the inspected strips. No threshold was relaxed to hide it.
- Ring rendering uses the shared fixed **4 px** parameter throughout both wide and zoomed views. Color-threshold measurements of encoded JPEG samples read 3–5 solid pixels depending on color, antialiasing and encoding; those threshold readings are not represented as ten exact 4.0 px measurements.

The original lesson coverage review remains applicable because the only narration removed is the two identified overclaims. All essential teaching remains in order; the remaining summary explains the role of a concrete standard. The words at the edited joins receive a local speech-recognition check; this is not a listening pass.

**Listening remains required at 2:41 and 2:45.** Direct audio audition and continuous playback with sound were not available through the tools used. No claim of an end-to-end audiovisual sign-off is made. The inherited donor-voice join at 2:37–2:41 also remains an ear-check item from the previous review.

This narrow repair preserves older ring weights on unaffected boards, as explicitly allowed by the current Edit Spec. Other inherited limitations include the small peripheral prop writing in the Notebook sketches and the lack of a fresh continuous-motion review of every unchanged scene. These are not represented as new defects or as completed ship checks.

Status: built for review; live site unchanged. Not shipped locally, committed or published. The owner's Video Tracker was not changed.
