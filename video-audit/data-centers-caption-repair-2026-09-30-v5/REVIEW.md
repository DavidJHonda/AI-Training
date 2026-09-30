# Data Centers v5 — two caption clarifications

**SHIPPED LOCALLY 2026-09-30; queued for batch deployment.** David approved shipping with “ship it” after the v5 delivery and its disclosed listening limitation. Commit `8a6b4f5b` installs the verified candidate at `course-assets/data-centers/data-centers.mp4` and changes only its page cache key to `20260930ship5`; the displayed runtime remains `4 min`. Installed and committed bytes match SHA-256 `ce5dc2cf8d75bf50740dcf79476d4c5db022ab3bb7060f3e209187fd325dd284`. No push or deployment performed. This approval does not constitute an editor listening pass; the limitations below remain documented.

Release details: `release.json`. Retained candidate, scripts, manifest, QA, and visual evidence. Removed only this build's four temporary segment MP4s after commit; standard scoped scratch cleanup found no other eligible files. The previous source can be recovered from `8a6b4f5b^:course-assets/data-centers/data-centers.mp4` (original SHA-256 above in Source and method).

The following sections describe the build and pre-shipping review state.

**Scope:** User approved the evaluation's required caption corrections with “Build it please.” Narrow visual repair only. The optional facility-image replacement is excluded. Candidate: `Prompts/data-centers-v5.mp4`. Not installed, committed, or deployed.

## Changes

- Around 0:09.7–0:16.5, replace the universal-sounding subtitle beneath the trillion-weight example with **“In this example: one trillion weights used per token.”** Preserve the number, heading, plate, and surrounding arithmetic animation.
- Around 3:02.3–3:06.4, replace **“Single Request ~2 Quadrillion Ops”** with **“Our 1,000-token example: ~2 quadrillion calculations”**, on two lines within the existing plate. Preserve the phone, expanding user grid, and facility sequence.
- Replacement captions follow the plates' existing fades. No new narration, audio edits, pauses, camera treatment, boards, or closing changes.

## Source and method

Source: `course-assets/data-centers/data-centers.mp4`, SHA-256 `239d5a26ee58a5e28322eadc364a15af27f946324c4fe4563bb96d9a659c4130`, the file verified against the public stream in the September 30 evaluation.

The raw rolls are absent locally. This build uses the finished, hash-locked file and re-encodes only two complete H.264 GOPs: frames **250–499** and **5467–5716**. All other video packets and all audio packets are remuxed unchanged. Source and replacement decoder configuration must match exactly before assembly.

Actual caption processing windows are frame intervals **[290,494)** and **[5468,5591)**, including fades. Zero-opacity frames are left untouched. Current-frame plate colors are interpolated through the old text band, then the corrected text is composited with measured plate opacity. This avoids a static opaque patch during crossfades.

Build script: `scripts/video/build_data_centers_v5.py`.

QA script: `scripts/video/qa_data_centers_v5.py`.

Commands:

```sh
.video-venv/bin/python scripts/video/build_data_centers_v5.py --preview-only
.video-venv/bin/python scripts/video/build_data_centers_v5.py
.video-venv/bin/python scripts/video/qa_data_centers_v5.py
```

Source mapping and preview images are retained here. Sequential decoding was used for frame mapping. `edit-manifest.json` records exact spans, source/candidate hashes, and protected-file checks; `qa.json` records encoded-candidate checks; `guard/` records boundary strips and the transition result.

## Verification completed

- Candidate SHA-256: `ce5dc2cf8d75bf50740dcf79476d4c5db022ab3bb7060f3e209187fd325dd284`.
- All 6,694 frames decoded successfully; timestamps, 30 fps, and 3:43.13 runtime preserved.
- All 6,194 frames outside the two encoded GOPs are pixel-identical to the source. Their compressed packets and timestamps are also identical.
- Every AAC packet and timestamp is identical. Independently decoded PCM is byte-identical: 21,422,080 bytes, SHA-256 `8e7920462ca57c80057442cf9a07539af15b5c7a6a8f5c31d89a044d03a317a3`.
- The source and replacement H.264 decoder configurations match exactly. Final encoding uses the source's CRF 18 / medium settings for compatibility; an initial CRF 16 segment encode was rejected before any candidate assembly.
- All eight declared GOP/caption boundaries pass `transition_guard.py`. Inspected the every-frame boundary strips and three encoded contact sheets, plus full-size caption/fade frames. No stale caption, missing frame, or intermediate graphic was identified in those checks.
- The literal final frame remains the canonical close, pixel-identical to the source. Protected-file hashes passed at build completion.

**Result:** narrow caption repair is ready for user review. It is not a whole-file audiovisual sign-off or shipping authorization.

## Existing treatment preserved

Canonical boards, highlighting, and camera plan remain as reviewed in `../data-centers-live-review-2026-09-30/REVIEW.md`: full-view photograph; complete-card dives on the neighbors board, with two supporting cutaways; full-view demand board with its chip/pylon cutaway; standard canonical close. Longest board run remains 20 seconds. No course board is in either encoded GOP.

## Limits

This is a narrow repair candidate, not a new whole-video shipping sign-off. Full end-to-end listening and continuous-motion evaluation remain unperformed. The pre-existing narration cuts at 2:22.9 and 2:51.4 and close graft at 3:33.8 are unchanged and retain the previous listening limitation. The optional power-station-looking illustration around 1:12 and the unspoken GPU throughput label remain as evaluated. No new pauses are proposed.

The course page, canonical MP4, lesson text, canonical JPGs, and public deployment remain unchanged. Video Tracker was not accessed or modified.
