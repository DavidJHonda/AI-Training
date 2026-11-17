# Where Will AI Land? — v13 narrow visual repair

User request: remove the brief highlight of the second part of the GPS box at about 2:13 in v12.

- Keep the whole GPS card outlined through frames 3995–4000 (2:13.167–2:13.367), replacing the six-frame Unexpected Result highlight before the satellite cutaway.
- The later GPS Unexpected Result outline begins at frame 4188 (2:19.600), when the board returns, and remains as in v12.
- All other visual choices, narration, and timing remain as in v12. Video rebuilt from the pristine sources and current canonical assets; AAC audio stream copied from v12 without re-encoding.
- New review candidate: `Prompts/where-will-ai-land-v13.mp4`. Installed lesson video untouched.

Verification completed:

- Every frame decoded and compared with v12: 7,829 frames at 30 fps, unchanged 4:20.967 duration.
- All six requested frames show the whole-card outline consistently until the satellite cutaway. The frame-by-frame contact sheet was inspected.
- Outside frames 3959–4000, every decoded frame is pixel-identical to v12. The 36 preceding frames have only nearby compression differences (maximum frame-mean absolute difference 0.2693 on an 8-bit scale). The later GPS result highlight is pixel-identical.
- Compressed AAC packets, timestamps, durations, and stream time base are exactly identical to v12. No audio re-encoding or timing change.
- Targeted transition guard passes all three checks, with no transient-frame flags.
- Source videos and canonical graphics retain their hashes. Installed video unchanged.

Prior direct-listening/continuous-playback limitations remain; this is a visual-only repair.

Output SHA-256: `52a57be4f6eaa794039e2e714c8ac46c57dba9279ceec49b4afa0db954c7eb1f`.

## Local release

Owner approved v13 with “Ship it.” Installed at `course-assets/where-will-ai-land/where-will-ai-land.mp4` with cache key `20261117ship13`. Local commit `a057208cf1ddfa560823513b7d7a2b55824f72f2` includes only the video, its manifest entry, and the lesson video reference. Installed SHA-256 and size match the approved candidate. Staged-release asset hash verification passed for all 346 unique assets. The working-tree hash check has unrelated Big Downside image mismatches from work in progress; those edits were preserved and excluded from this commit. Direct-listening limitations were disclosed before owner approval and are not represented as performed.

Shipped locally; queued for batch deployment. No push or deployment performed. Render scratch cleaned; review records and candidates retained.
