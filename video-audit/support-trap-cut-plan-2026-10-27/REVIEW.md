# Support Trap v15 — approved recap cut

Built October 27, 2026 following “Build it please.” Review candidate: `Prompts/support-trap-v15.mp4`. Runtime **4:27.700**, 8,031 frames, 30 fps, 1280 × 720. Approved and shipped locally; queued for batch deployment. See the release record below.

## Change

Removed v14 frames [1721, 1849), **0:57.367–1:01.633**, totaling 4.267 seconds:
“but only one of these replies alters your day. The other cannot act.”

At output 0:57.367, the shortened empty-chair illustration cuts directly to the existing comparison board. The retained narration is “The AI’s words might even sound kinder in the moment.” followed by “Support Trap is mistaking supportive words for support.” The encoded join transcript measures approximately 0.62 seconds between those sentences. No silence was inserted. Five-millisecond fades touch only quiet join edges.

All other source frames/audio are retained in order. The approved opening and closing omissions were already present in v14. The complete lunch comparison, all three boards, existing highlights/camera, v14 preparation illustration, warning and story, safety guidance, and canonical closing motion/final frame remain. The source/output visual timeline is recorded in `v15-edit-manifest.json`; the longest unchanged board run is 23.80 seconds.

## Verification

- Decoded all 8,031 frames with uniform timing and the planned duration.
- All 30 declared boundary checks pass. Inspected the new cut strip, board return/highlight sequence, and literal final frame.
- Sampled source/output images match within encode error, including the final frame.
- Before encoding, retained audio is sample-identical except for the five-millisecond seam fades. Encoded correlation with the planned audio is 0.999996762.
- Cut handles measure −58.17 and −81.03 dBFS. Encoded join transcription preserves both intended sentences and excludes the deleted recap.
- Installed MP4, lesson page, source v14 and canonical boards remain unchanged.

## Limitations and review

Perceptual listening and continuous full-video playback were not performed. Please listen around **0:57**, or use `v15-qa/join-review.wav` (starts at video 0:53). Waveform and transcript checks are not a listening verdict. This is a narrow review candidate, not whole-file shipping certification.

The pristine assembled PCM was removed during earlier shipping cleanup. The hash-verified finished v14 is the approved fallback source, encoded once more at H.264 CRF 16/AAC 192k. Raw generations remain available; no claim is made that they were lost. The inherited story wording still omits the lesson qualifier “sometimes,” as disclosed in the v13 review; this narrow cut does not alter it.

Source SHA-256: `a465ed033c1139dbf61fb5404826d3f0d9c955c58b295ef1abe4977d7151d88e`.
Candidate SHA-256: `70e787efac28dff7efa2fd5b439f30e4883eeb8e8edb59a34a4d955edd562b0a`.

Build: `.video-venv/bin/python scripts/video/build_support_trap_v15.py`
QA: `.video-venv/bin/python scripts/video/qa_support_trap_v15.py`

Local installation and publishing remain separate from this build approval.

## Local release — October 27, 2026

Owner approval: “Looks good. Ship it please.” Installed v15 at `course-assets/support-trap/support-trap.mp4`, updated its cache key to `20261027ship15`, and refreshed its asset manifest hash/size/version. Runtime is 4:27.700; the existing whole-minute ceiling remains 5 min.

Commit: `30e3069df5395fc0dfc39e4bd926d477ec0b5a10`. Exactly three release files committed; unrelated staged/working lesson edits were preserved. Candidate, installed, and committed MP4 SHA-256 match `70e787efac28dff7efa2fd5b439f30e4883eeb8e8edb59a34a4d955edd562b0a`.

Two inline JavaScript blocks parse. Support Trap references and manifest metadata match the installed file. The broader asset verifier reports pre-existing retired In Your Hands image filenames; those unrelated files were left untouched. Owner approval follows the disclosed listening/full-playback limitations; it is not represented as agent listening.

No push or deployment performed. **Shipped locally; queued for batch deployment.** Removed regenerable join WAV and 49.0 MiB of raw audio scratch, preserving candidates, source videos, scripts, transcripts, QA images and records.
