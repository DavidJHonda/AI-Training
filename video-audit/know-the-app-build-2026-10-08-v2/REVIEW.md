# Know the App — production candidate v2

Built 2026-10-08 from roll 6 using the October 1 edit plan. Review candidate; not installed or shipped.

- Runtime: 4:23.63, 7,909 frames at 30 fps, 1280×720.
- Roll 6 audio is copied unchanged; compressed audio stream hashes match.
- Current canonical Which Model?, How Much Thinking?, and How Much Research? boards, with narration-timed card highlights using the established nominal 4 px renderer.
- Drawn camera examples from roll 4; engine, project-planning and university-comparison drawings from rolls 4 and 5.
- Useful source animation retained. Repaired settled answer labels to say Proposed answer / Review before using, removing claims that the answer has been verified.
- Canonical closing: 48-frame hold, 150-frame push, 26-frame settle.
- Canonical boards and protected source files remain unchanged.

## Validation

Decoded all 7,909 output frames. Automated transition guard passed all 27 declared boundaries. Reviewed contact sheets across the full video, before/at/after frames for every declared join, full-size board previews, label repairs, and final frame. Audio identity: SHA256=83b2ea2a3724ecbb2fde7d28b80c77c7c72ef98ff9f24f4722a7f36e3304e342.

Candidate SHA-256: `5895213badbd7e9d74d9cab225407f3c210150e53398937f6a32a0be8324386d`.

Continuous audiovisual listening has not been completed. Roll 6's existing narration KEEP review is retained, but the candidate still needs a full listening pass, including the Dallas/College Station example around 3:34–3:39. No new narration correctness or readiness-to-ship certification is claimed.

v1 is superseded by v2's tighter label patches. Build script: `scripts/video/build_know_the_app_v2.py`. Exact timeline and asset hashes: `edit-manifest.json`. QA: `qa.json` and `transitions/`.

Browser playback verified: picture visible, readyState 4, time advanced to 26.36 seconds. Ring audit found 32 samples across nine runs, measuring 4–5 solid pixels after encoding with the established nominal 4 px anti-aliased renderer. Teaching boards have no camera zoom.
