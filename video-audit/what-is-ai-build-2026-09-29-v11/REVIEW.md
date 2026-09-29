# What Is AI? version 11

**Shipped locally; queued for batch deployment.** [Candidate](../../Prompts/what-is-ai-v11.mp4): **2:35.57**, 4,667 frames at 30 fps, 1280×720.

## Changes requested

- Removed v10/raw-roll-5 **0:21.00–0:48.00**, the complete repeated board explanation and ten-topic narration. This uses clean sentence boundaries around the user's approximate :22–:48 range. “A list in seconds” now leads directly into “AI is software built to do things that used to take a human brain.” Exactly 27 seconds removed.
- The takeaway banner on **One Picks. One Creates.** is highlighted on the first frame when the board returns: **new 2:19.37**, formerly 2:46.37. No two-second highlight delay. This is the owner's explicit exception to an unmarked return.
- Necessary cut dependency: the definition is now the first appearance of **Ask the Desk. Ask AI.** It opens complete and unmarked at 0:21.00, without the old list ring, then highlights its definition banner at the spoken onset around 0:21.38. No extra pause was inserted.
- Other v10 narration, corrected graphics, camera paths, rings and closing treatment preserved. Rebuilt from pristine raw version 5 to avoid stacking video encodes.

The user's explicit cut supersedes the earlier production requirement to enumerate all ten ideas. No lesson or prompt files were revised for this video-only request.

## Verification

- Complete sequential decode: 4,667 frames, 30 fps, 155.5667 seconds.
- Exact pre-encode PCM equals the two retained source spans at the original **44.1 kHz mono** format. AAC was necessarily re-encoded after the cut; no EQ, level processing, fades or added pauses. Encoded audio comparison SNR: **44.12 dB**.
- Both cut points are inside measured silence: 20.56805–21.461973 and 47.322404–48.356009 on the source. The final encoded join silence is **20.568–21.356**, a total **0.788 seconds**. No syllable lies at the splice according to the waveform/silence and existing transcript evidence.
- 178 prepared frame states compared to the encoded result. 38 sampled unchanged frames compared with v10: maximum mean pixel difference **0.456/255**.
- All 20 declared output boundaries pass [transition guard](guard/transition-guard.md). The affected cut and highlight-return strips, plus exact first frames, were visually inspected.
- First returned frame **4181** verified to contain the takeaway ring. The encoded image matches the ringed renderer substantially better than its unmarked baseline.
- Prior candidate, raw source, canonical boards and live video hashes unchanged.

**Listening limitation disclosed before approval:** the agent did not directly audition the new join at **0:21** or perform an end-to-end playback pass. Automated checks do not certify how the cut sounds. David subsequently explicitly authorized shipping with “ship it.” This records owner release approval, not an agent listening pass. No publication or tracker update performed.

## Reproduction and identity

[Plan](PLAN.md), [manifest](edit-manifest.json), [QA](qa.json).

Build: `.video-venv/bin/python scripts/video/build_what_is_ai_v11.py`

QA: `.video-venv/bin/python scripts/video/qa_what_is_ai_v11.py`

Source SHA-256: `085a13929d3df5715efb428edf49e7159c4710ddd419785cd92161c55bf4dd1e`

Candidate SHA-256: `e7713536d479f329277efacfd6d052efcdb66852c50eca83b26b6e5e44905785`

Previously approved supporting assets are reused from `video-audit/what-is-ai-build-2026-09-29-v10/assets/`; no new image generation was needed.

## Local shipping

Owner-approved version 11 installed at `course-assets/what-is-ai/what-is-ai.mp4`. Installed and committed bytes match the candidate SHA-256 above. The lesson uses cache key `20260929ship11`; its rounded runtime remains `3 min` for the actual 2:35.57 video.

Local release commit: `bd4f879d75398ef3d8aa7076282392b8d3bf868e`. Only the approved video and its lesson cache key were committed. Unrelated working changes remain intact. **Queued for batch deployment; no push or deployment performed.**

Removed nine regenerable v11 render-scratch files (0.05 GB), retaining review evidence, source generations, candidates and supporting assets. See [shipping receipt](shipping-receipt.json).
