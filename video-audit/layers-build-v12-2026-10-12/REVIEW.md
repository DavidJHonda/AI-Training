# Layers v12 — revised context build

Built 2026-10-12; approved for shipping 2026-10-22 with **“ship it.”** Shipped locally in `d03987ea`; queued for batch deployment. Installed file matches the reviewed candidate SHA-256; lesson cache key is `20261022ship-layers-v12`. No push or public deployment performed.

## Candidate

- `Prompts/layers-v12.mp4`
- SHA-256: `42fb10fd979dd5567d8a9ae2105507a87b7f7cc0610ff20e1095fbd7ce5bcbb6`
- 6,183 frames, 30 fps, 1280 × 720; **3:26.10**. H.264 picture and AAC mono 48 kHz.
- [Local review player](http://127.0.0.1:8765/video-audit/layers-build-v12-2026-10-12/review.html)

## Changes

The approved two whole passages from roll 6 replace the obsolete example and conclusion. All other narration is retained without speech stretching or added teaching pauses.

| Passage | Output span | Donor span | Words |
|---|---|---|---|
| Example | 112.533–117.667 | 85.767–90.900 | The tired cat sat on the mat during the May rainstorm. It soon fell asleep. |
| Conclusion | 154.833–159.333 | 112.567–117.067 | Its updated numbers carry information about its connection to cat. |

Gain +4.495 dB, donor-only peak limiter ceiling .96, compensated latency, and 5 ms seam ramps inside the selected quiet boundaries. Existing starting, intermediate, and final-number explanations remain in place.

| Visual | Output span | Treatment |
|---|---|---|
| Lesson sentence card | 107.200–112.567 | The exact captured card approved for Vector Space v20, centered and fully visible, replaces another obsolete handwritten example found during encoded QA. No timing change. |
| Current CAT/IT board | 112.567–140.767; 148.200–159.767 | Canonical current lesson JPG, full view, complete-card highlights. Sentence → Start → Layer 1 → Layer 2 → Repeat → Result. |
| Successive IT updates illustration | 140.767–148.200 | Corrected sentence; sleeping cat, four IT tiles, arrows and bar groups retained. Existing 7.43-second duration and 1% push retained. |

Highlights begin at 112.733, 117.967, 126.967, 132.800, 140.167, and 149.900 seconds. The first sentence begins immediately after board entry; its ring follows the spoken onset. The compact board remains fully visible throughout. No unrelated camera treatment changed.

The complete existing horse introduction, neural-network explanation, numeric walkthrough, late scale/cost animations, and standard close are retained. The extra 2.733 seconds come only from the two longer donor passages.

## Verification

- Decoded all 6,183 frames with expected dimensions and rate.
- Compared 156 retained-picture samples with their mapped v10 frames: maximum mean pixel difference 0.003550/255.
- Unchanged audio portions are exactly identical before encoding; after AAC encoding, all three retained spans correlate above .99998 with the base. No global normalization or limiter was applied.
- Encoded donor peaks are .96127 and .96145, with zero samples over full scale. The base contains eight small AAC reconstruction overshoots (peak 1.00465); float assembly preserves these rather than introducing int16 clipping. This inherited characteristic is outside the two-passage repair.
- ASR of the assembled encoded context confirms both replacement sentences and the retained neighboring explanations. V12 AAC is byte-identical to the transcribed v11 AAC; `qa.json` records the audio hash and provenance.
- Inspected the encoded full-board and supporting-illustration frames, three scene contact sheets for v11, all affected v11 transition neighborhoods, v12 introduction/board-entry strips, and a v12 whole-video contact sheet sampled every five seconds. V12's other 47 transition strips are pixel-identical to v11.
- Transition guard checked 51 boundaries. All revised-region boundaries pass. Its sole flag, inherited f302, is a continuous horse-board camera zoom; manual every-frame inspection shows no stale intermediate shot. The raw automatic FAIL is preserved in `guard/`, with the adjudication in `transition-review.json`.
- Encoded result-ring spot check measures four solid pixels on the left and top edges using the shared color-distance threshold. Rings enclose complete cards and do not cut through text.
- V11 was superseded internally because its inherited introduction still showed the old sentence. V12 fixes that span; v11 remains available as an audit artifact.

The local browser review page passed its final smoke check: video metadata, all three seek/play controls, and no page errors. The existing preview server lacks byte-range support; the review page loads the video as a local Blob so seeking works reliably. See `browser-check.json` and `review-browser.png`.

## Limits and remaining review

No direct listening, continuous real-time viewing, or subjective voice-match judgment is claimed. **Listen to both grafts with their surrounding narration before shipping.** Automated wording, waveform and similarity checks do not certify a natural voice blend.

The reconstruction reuses the retained original-source pipeline where available. Its earliest surviving snapshot is itself an earlier published edit; earlier raw footage is unavailable. V12 is not a lossy transcode of v11. Original source identity checks remain in place, with only the intentionally updated CAT/IT board hash exception made in memory.

The new raster asset is `scripts/video/assets/layers-visual-variety/it-successive-updates-v11.png`; its creation prompt and built-in imagegen provenance are in `image-edit.md`. The card source and all protected-file hashes, frame mappings, rings and donor boundaries are in `edit-manifest.json`.

No tracker rows were written. Candidate build approval was used; shipping remains a separate action.

## Local release — 2026-10-22

Commit: `d03987ea8f1a2c4488f43c92ca6d45e8dc0cd4b5`. Candidate identity and current board/illustration hashes reverified before installation. Installed MP4 hash and lesson reference verified after installation; final encoded frame inspected. User approved the delivered review candidate after the disclosed listening limitation. This records approval without claiming that the assistant performed direct listening or that the user explicitly reported listening. The approved candidate was installed unchanged. Unrelated course-planning documents and local audit records were left outside the release commit.

Post-commit cleanup removed 13 regenerable files (about 0.08 GB) from only the v11/v12 build and original donor-review folders. Source rolls, review MP4 candidates, transcripts, manifests, image assets and transition evidence were retained.
