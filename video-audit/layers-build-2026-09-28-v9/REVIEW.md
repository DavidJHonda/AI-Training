# Layers v9 — visual variety

Shipping authorized by David: “ship it.” Exact candidate installed at `course-assets/layers/layers.mp4`, cache key `20260928ship1`. David approved v8's narration and lesson progression, then agreed to replace two repeated layer-stack breaks with new relevant illustrations.

Candidate: `Prompts/layers-v9.mp4` — 3:23.367, 6,101 frames, 30 fps, 1280×720.

## Changes

| Output span | Illustration | Purpose |
| --- | --- | --- |
| 1:19.867–1:24.867; frames 2396–2545 | Many numbers, two shown | A long row with the board's .42 and −1.15 brought forward. |
| 2:19.767–2:27.200; frames 4193–4415 | Successive updates to “it” | The same token follows a continuous path; fixed-size schematic bar groups change height at each stage. The full cat sentence stays in view. |

Each drawing uses a restrained 1% camera push. Narration, pauses, lesson order, board timings, annotations, other drawings and the close retain v8's approved treatment. Existing stack imagery remains at the other placements.

The original retained source and canonical boards were rendered again using v8's reconstruction, with only these two picture spans replaced. The approved v8 AAC stream was copied without re-encoding. Assets were created with built-in imagegen; final PNGs and all prompts are in `scripts/video/assets/layers-visual-variety/`.

## Verification

- All 6,101 frames decoded at 30 fps and 1280×720.
- Compressed AAC bytes and decoded PCM both exactly match v8. No new listening judgment was needed for this visual-only change; David's narration approval is retained.
- 389 retained-picture comparisons against v8: maximum mean absolute pixel difference 0.024/255 (encoding variation).
- 16 encoded-state comparisons against render previews: maximum mean absolute difference 2.845/255.
- All four changed cut boundaries pass the transition guard. Every-frame strips inspected: direct board → illustration → board cuts, no stale stack frames or flashes.
- First, middle and final encoded illustration frames inspected: sentence and number labels remain readable and uncropped throughout the push. Each of the four schematic bar groups has the same five positions and color order.
- Protected source media, canonical boards, lesson and website files match their pre-build hashes.

The first render's final check used an obsolete index.html hash from the v8 manifest and stopped. No media source differed. The final build protects the current page state instead; all checks pass. No website or published video changes were made by this task.

Machine results: `qa.json`, `edit-manifest.json`, and `guard/`. Encoded review frames: `encoded/`; context contact sheets: `contact-0.jpg` through `contact-3.jpg`.

## Shipping verification — 2026-09-28

Owner approved the narration, lesson progression and final visual candidate. Agent has not claimed fresh perceptual listening. The exact reviewed file hash is `40b88ef892c5bf0c72490e96544c5f2f31b88dfc1f24a208a3d705bbb952b2ca`. All canonical board hashes still match. The literal final frame was reinspected and is the standard close. The whole-file transition guard checked 31 declared boundaries: 30 automatic passes; inherited frame 302 was reinspected and cleared as continuous camera motion, with the automated flag retained in the record. See `shipping-guard/manual-review.json` and `shipping-receipt.json`. Publication verification follows the push.
