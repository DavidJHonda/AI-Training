# Trust Trap v6 — review candidate, October 27, 2026

## Shipped locally — October 27, 2026

The user approved the candidate with “Looks good. Ship it.” Installed the exact
reviewed v6 bytes and committed only the canonical MP4 and its cache-key/runtime
entry as `5961bd73` (`Ship shortened Trust Trap v6 locally`).

- Canonical SHA-256: `92ee469b00438c6e361b0267996e2e3c101e40856c33ec49504e6ca558c09f55`; installed file, candidate and committed blob match.
- Cache key: `20261027ship1`; runtime label: **3 min**.
- **Queued for batch deployment.** No push or deployment was performed.
- Other uncommitted lesson and course edits remain outside the release commit.
- Candidate, previous v5 candidate, approved word preview, listening clips and QA
  evidence retained. Scoped cleanup removed only regenerable `edited.wav` (17.1 MB).
- The owner reviewed and approved the candidate. Agent audio listening and
  uninterrupted playback remain unperformed; the approval does not change that
  disclosure. Encoded-file checks below apply to the byte-identical release.

The earlier review-only status below is superseded by this shipping record.

Built the user-approved same-sentence **Trust Trap** word splice and all five
recommended cuts. Candidate: `Prompts/trust-trap-v6.mp4`, **2:57.67**, 5,330 frames
at 30 fps, 1280×720. Saves **54.47 seconds** from the installed 3:52.13 version.

This is a review build. The canonical video, lesson, boards and course reference
were not changed. No installation, commit, push or deployment was performed.

## Implemented edits

| Edit | Installed-source interval | New-version location | Result |
|---|---|---|---|
| Opening | 0:00.000–0:26.800 | New start | Opens directly on the college example and full comparison board. Removes first old-name occurrence. |
| Name repair | 1:16.575–1:16.940 | 0:49.775–0:50.140 | Exact approved PCM patch copied from the auditioned preview. Uses “trust” from source 1:19.285–1:19.650; leaves “Trap” and the rest of the sentence intact. |
| Graphic introduction | 1:56.100–2:04.167 | Join 1:29.300 | Removes the announcement of the explanation. |
| Inner-life sentence | 2:14.467–2:19.233 | Join 1:39.600 | Removes the redundant sentence; keeps the generated-words explanation. |
| Repeated decision explanation | 3:16.733–3:23.633 | Join 2:37.100 | Connects the preparation examples directly to involving real people. |
| Second summary | 3:36.267–3:44.200 | Audio join 2:49.733 | Connects shared stakes directly to the standard close. |

The diagram's original boundary reveal is retimed continuously through
**2:36.567–2:38.467** in the output. It uses source 3:16.200–3:25.000,
preserving the full preparation list and allowing the human-card reveal to
continue on its retained narration. It does not jump over an unfinished reveal.
No new image or replacement diagram was introduced.

The complete 240-frame closing sequence starts at **2:49.667**. Its picture
arrival leads the final audio join by two frames, preserving the full original
hold, push and settled ending instead of shaving two opening frames. The
literal final frame is retained. No pauses were added.

## Encoded-file verification

- Sequential decode: **5,330 frames**, uniform 1/30-second presentation intervals.
- All **nine** declared transition checks pass. Every saved boundary strip was
  visually inspected; no stale intermediate shot was found.
- Three contact sheets covering the full candidate and the full-resolution last
  frame were inspected. Current boards and their inherited camera/highlight
  treatments remain intact. This narrow edit does not re-author their styling.
- Sampled decoded output frames agree with the planned source-frame mapping
  within normal re-encoding differences, including the initial and final frames.
- Fresh transcription of the encoded candidate contains **“Trust Trap is giving
  a human-sounding answer…”**, no “Mind Trap,” none of the deleted passages, the
  personal-context qualification, movie/college distinction, preparation steps,
  human involvement and both closing lines.
- Encoded audio correlation with planned edited PCM: **0.99998378**.
- Measured natural quiet gaps at the four new interior audio joins: **0.463 s,
  0.472 s, 0.380 s, 0.407 s**. All joins fall inside their quiet intervals. Five
  millisecond blends use quiet source audio; the approved word patch preserves
  its exact auditioned three-millisecond endpoint blends.
- Protected source-video, lesson, board and approved-preview hashes are unchanged.

## Review limits and listening clips

The user auditioned and approved the exact word-repair preview. The agent has
not perceptually listened to the newly assembled joins or watched the full
candidate in uninterrupted playback. Automated transcription, waveform checks
and frame strips do not certify natural cadence. This candidate is ready for
user review, not asserted to have completed the whole-file shipping checklist.

Focused clips, all extracted from the encoded candidate:

- `qa/word-repair.mp4` — includes the repaired definition at approximately 0:50.
- `qa/graphic-introduction.mp4` — join at 1:29.300.
- `qa/inner-life-cut.mp4` — join at 1:39.600.
- `qa/decision-diagram.mp4` — retimed reveal and join at 2:37.100.
- `qa/ending.mp4` — new closing join at 2:49.733 and full closing sequence.

The inherited ASR rendering “calling data patterns” remains uncertain and
unchanged, as in the preceding review. It was outside this approved repair.

## Reproducibility

- Source: `course-assets/trust-trap/trust-trap.mp4`, SHA-256
  `ec2084ebb4dc3d8485d59ae79476cf8f450dd2a574288dbbd81b19f73b24312e`.
- The original raw rolls are absent. This build uses the installed finished v5
  and applies one H.264 encode and one AAC encode.
- `approved-word-preview.wav` retains the auditioned preview; the build also
  records its original path and SHA-256 in `edit-manifest.json`.
- Build: `.video-venv/bin/python scripts/video/build_trust_trap_v6.py`.
- QA: `.video-venv/bin/python scripts/video/qa_trust_trap_v6.py`.
- Exact audio/picture source mappings, output hash, cuts and protected inputs:
  `edit-manifest.json` and the two `*-source-frames.npy` arrays.
- Verification: `qa/summary.json`, `qa/transcript.txt`, `qa/silences.txt`, and
  `qa/transitions/transition-guard.json`.
