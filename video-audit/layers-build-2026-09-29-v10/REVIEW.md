# Layers v10 — approved visual readability repair

David authorized this build with “Build it please,” following the September 29 live-video evaluation. David subsequently approved v10 with “ship it.” The approved narrow visual repair is now installed and committed locally; public deployment is pending the separately authorized batch workflow.

Candidate: `Prompts/layers-v10.mp4`. Verified duration: **3:23.367**, **6,101 frames**, 30 fps, 1280×720.

## Changes

| Output span | Change |
|---|---|
| 1:26.500–1:43.167 | Smoothly enlarge the complete four-card number row by 1.426× relative to the original framing. Hold all four cards in view; return to the full board before the takeaway. Preserve the original starting/final-value ring timings; rings are rendered at fixed 4 px after the camera transform. |
| 2:46.800–2:51.600 | Simplify the title to “Connecting words” / “Each layer adds information.” Remove the overlapping small stage label with clean pixels from the same original shot, before that label appeared. Preserve the growing arrow, layer stack, scientist example, and transition. |
| Approximately 2:51.600–3:00.167 | Simplify the next heading to “Working through harder meaning.” Replace the three box labels with “Sarcasm,” “Story twists,” and “Complicated reasoning.” Retain the source layer fill, connectors, box reveals, and dissolve. |
| Approximately 3:00–3:12.667 | Simplify the heading to “Why not keep adding layers?” and explain compute/time in plain language. Raise the balance by 140 pixels. Replace panel lettering with Benefit: Understanding / Reasoning and Cost: Computing power / Time. Change the center caption to “Benefit vs. cost.” |

The original tilted cost panel extended below the video canvas. Merely moving its decoded pixels upward revealed a missing bottom corner. The repaired panel uses the original tracked position, angle, size, and fade, restores the complete outline, and carries the simpler labels. Both panels are tracked from source image features. The beam, pivot, hanging lines, tilt, settling, and center-plaque reveal remain source animation.

Narration, audio joins, pauses, total duration, board exposures, number-row/cat supporting inserts, and closing sequence are unchanged. No new narration or silence was added. The longest board exposure remains the approved 27.2 seconds on IT/CAT; this repair does not add board holds.

## Sources and reproducibility

Base/audio: approved `Prompts/layers-v9.mp4`, SHA-256 `40b88ef892c5bf0c72490e96544c5f2f31b88dfc1f24a208a3d705bbb952b2ca`.

The picture pipeline reconstructs v9 using the retained original Layers snapshot, canonical board assets, original horse donor, and approved v9 illustration assets. The active-data donor is pinned to `Prompts/transformer-v12.mp4`, SHA-256 `0a972235e9fcaf619d8db34715243a7812a87569091e87092f866666586376b5`; another task replaced the canonical Transformer file during this build, so its moving path is not used. The pinned file exactly matches v9's donor identity.

Source limitation: the retained original Layers snapshot is itself an earlier published edit. Earlier pristine raw rolls are unavailable. This rebuild reuses the earliest retained reconstruction rather than layering the whole change onto v9's compressed picture.

Build: `.video-venv/bin/python scripts/video/build_layers_v10.py`  
QA: `.video-venv/bin/python scripts/video/qa_layers_v10.py`

The build refuses to overwrite an existing review candidate. `edit-manifest.json` records sources, protected hashes, frame ranges, camera specification, and output identity. `balance-tracking.json` records every fitted panel pose and fade. `panel-bounds.json` confirms every reconstructed panel corner remains inside the output frame.

## Verification status

**Approved and shipped locally; queued for batch deployment.** Candidate SHA-256: `67370834ca3117cb69bab6dbad99b2d1b5ed4fcee4344abeb92450268e952c1d`.

- Decoded all **6,101 frames** at 1280×720 and 30 fps; duration remains **203.3667 seconds**.
- Compressed AAC and decoded PCM are both exactly identical to v9. No new audio splice or pause exists.
- Compared **322 preserved-picture samples** with v9; largest mean pixel difference **0.412/255**, consistent with encoding variation.
- Compared **70 encoded states** with prepared render references; largest mean difference **2.999/255**.
- Inspected five encoded motion contact sheets across both changed spans, selected native-resolution frames, and the literal final frame. The number cards and balance panels remain complete. Layer fills, example reveals, balance tilt/settling and close are retained.
- Transition guard passed **all 17 checked boundaries**. Inspected all 17 every-frame strips in six review sheets: no stale-image flash or unexpected intermediate shot identified.
- Tracked **725 panel states**, with median feature-fit error **0.054 px** and maximum **0.366 px**. Every reconstructed panel corner remains inside the output frame; the lowest reaches about **607 px** in the 720 px frame, including the tilted poses.
- At build completion, protected v9, the then-installed Layers video, and canonical board assets retained their hashes. The approved shipping step subsequently installed v10 and updated only its lesson cache key.

Evidence: `qa.json`, `panel-bounds.json`, `balance-tracking.json`, `guard/`, `guard-review-*.jpg`, `encoded-motion-*.jpg`, and `encoded/`.

This is verification of the approved narrow visual repair. No continuous real-time whole-file viewing, fresh perceptual listening, public/mobile playback, or full remeasurement of inherited rings outside the changed number-board camera was performed. The previous review's generic ring-detector uncertainty outside this scope remains unadjudicated; it is not being converted into a new compliance pass.

No new perceptual audio claim will be made for this visual-only build. Final QA confirms both compressed AAC and decoded PCM identity to v9. Owner approval of the existing narration remains applicable; inherited audio joins are unchanged.

## Local shipping receipt

Owner approval: “ship it.” Installed `course-assets/layers/layers.mp4` from the verified v10 candidate. Installed and committed bytes match SHA-256 `67370834ca3117cb69bab6dbad99b2d1b5ed4fcee4344abeb92450268e952c1d`. The lesson reference is `course-assets/layers/layers.mp4?v=20260929ship1`; displayed duration remains 3 min.

Local commit: `d945bde7dd4cb791c958fa95fa11b12e8ce543da` (`Ship approved Layers v10 locally`). Only the canonical MP4 and the Layers lesson cache-key entry were included. Audit/build records remain local. No push or deployment was performed; **shipped locally; queued for batch deployment**.

After a scoped dry run, removed three regenerable render-scratch files from this v10 audit only. Candidate, QA evidence, and review records remain available. See `publication-status.json`.
