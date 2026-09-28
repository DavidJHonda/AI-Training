# Transformer v12 — review candidate

**Shipping approved by David: “ship it” (September 28).** Built from the unchanged published video, carrying forward the approved v11 repairs and adding David's September 28 requests. Candidate: `Prompts/transformer-v12.mp4`. Runtime **3:54.867**, 7,046 frames, 30 fps, 1280 × 720. Adds 1.300 s to v11 and 8.600 s to the published source. v11 is unchanged.

## Requested changes, with candidate timestamps

- **0:23.567–0:39.033:** full-board opening for 2 seconds; zoom toward the complete LIGHT card from 0:25.567–0:26.767; hold through the examples; pan right from 0:38.400–0:39.033. Preserve the original cat/IT/glass illustration at 0:39.033–0:42.867, then return to the complete pronoun card. Pull back at 0:51.700–0:52.500 for the full-board takeaway.
- **0:47.700–0:50.167:** narrate the complete “The cat drank the milk because it was fresh.” Reuse the existing 1.3-second prefix before the original “because” clause. The new joins are 0:47.700 and 0:49.000. The bridge remains “If we change the sentence to…”; no additional pause inserted. ASR confirms the full sentence and surrounding flow.
- **1:02.900–1:23.267:** replace the broad sequence highlight with individual word highlights aligned to the spoken examples: THE at 1:04.133, CAT at 1:05.133, SAT at 1:06.167, IT at 1:11.967, CAT again at 1:13.167. Only example-word mentions are marked; incidental uses of “the” are not. Inset outlines surround the text, preserving the existing chip borders and avoiding a second outline on the built-in purple IT chip border. The takeaway highlight remains.
- **2:26.767–2:55.533:** matching full-board → complete LIGHT card → pan to complete pronoun card → full-board takeaway treatment. Initial full view lasts 2 seconds; zoom 2:28.767–2:29.567; pan 2:37.267–2:38.867; pullback 2:50.433–2:51.233. Retain all four v11 full-sentence rereads followed by their clue explanations and synchronized sentence/clue highlights.

The opening uses a shorter pan in the existing gap after “not heavy”; the later board pans during the pronoun introduction. Each active card retains its photo, card title, sentences, and explanation. Board-level titles and bottom banners leave the viewport during zoomed card views and return with the whole-board view. No new audio padding, content rewrite, graphic replacement, or lesson edit. Fixed 4 px generated outlines are applied after camera transforms.

## Continuous board durations

Motion and highlight changes do not reset these durations.

| Board | Candidate interval | Continuous duration |
| --- | --- | --- |
| Two Problems Context Must Solve, first visit | 0:23.567–0:39.033 | 15.467 s |
| Two Problems Context Must Solve, second visit | 0:42.867–0:54.967 | 12.100 s |
| How Earlier AI Read Text | 1:02.900–1:23.267 | 20.367 s |
| How a Transformer Reads a Sentence | 1:33.400–1:43.900 | 10.500 s |
| How Context Changes the Numbers | 1:53.200–2:14.800 | 21.600 s |
| How the Transformer Resolves Meaning | 2:26.767–2:55.533 | 28.767 s |
| How a Transformer Keeps Words in Order | 3:21.300–3:44.867 | 23.567 s |
| Standard close | 3:44.867–3:54.867 | 10.000 s |

The longest teaching board remains the intentional 28.767-second worked example. The adjacent order-board/close chain remains 33.567 seconds. All original illustration breaks survive.

## Verification

- Sequential decode passed: all 7,046 frames at expected dimensions/rate.
- Compared all 3,075 retained illustration/closing frames with their source frames and 662 board frames with their expected render. Maximum pixel MAE 2.977/255, consistent with encoding. No removed illustration or stray source frame found.
- Inspected all ten encoded contact sheets, ten guard sheets covering all 28 boundaries, and the complete-card preview at output resolution.
- Automated transition guard passed 26/28 boundaries. Its two flags at frames 1171 and 4473 are expected continuous pan/zoom motion, confirmed by every-frame strips and comparison to expected render. Original automated failures remain recorded; manual disposition is in `manual-review.json`.
- Every frame of the three camera legs passed ring-bound checks. Full active cards fit during all holds, zooms, and pullbacks. Pan transitions briefly show portions of both cards, with the outgoing highlight cleared.
- 540 measured outline sides: median 4.179 px, range 4.094–4.455 px including antialiasing/compression, for the fixed 4 px target.
- Edited PCM is identical to its source mapping outside 5 ms join ramps. Encoded AAC SNR 42.005 dB, correlation 0.999969. No gain change or truncated audio detected. The opening excerpt ASR verifies the newly completed sentence. The approved v11 reread mapping is unchanged, shifted by 1.3 seconds.
- Protected published MP4, lesson Markdown, prompt and all canonical JPG hashes remain unchanged. The prior v11 candidate hash also remains unchanged.

## Checks not performed

No perceptual listening or real-time end-to-end playback was performed. ASR and signal comparisons cannot establish natural cadence or imperceptible audio splices. Listen especially to **0:46–0:52** for the new sentence, and **2:44–2:48** for the carried-forward assembled fresh reread (internal join now 2:45.933). Phone readability and public-player behavior were not checked. Original raw narration remains unavailable; the published video is the source, so retained graphics receive one additional encode.

Status: owner approved publication after the listening limitation was disclosed. Exact candidate installed for commit/push; see shipping-receipt.json. No new agent listening claim is made.

## Identity

Source SHA-256: `d55f0000452087fb4b7993b2e79e06759ef263e147362cbd744a3c44883d9eb6`.

Candidate SHA-256: `0a972235e9fcaf619d8db34715243a7812a87569091e87092f866666586376b5`.

Build script: `scripts/video/build_transformer_v12.py`. Evidence: `edit-manifest.json`, `verification.json`, `manual-review.json`, `camera-checks.json`, `complete-card-checks.json`, `audio-seams.json`, `opening-asr/opening-check.json`, and `guard/transition-guard.json`.
