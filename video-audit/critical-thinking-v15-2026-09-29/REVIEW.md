# Critical Thinking v15 — review candidate

Built September 29, 2026 from the approved evaluation. David authorized the three visual repairs with “Build it.” **Shipped locally September 29, 2026, with David’s “ship it” approval; queued for batch deployment.**

Candidate: [critical-thinking-v15.mp4](../../Prompts/critical-thinking-v15.mp4), 3:06.43, 1280×720, 30 fps, 5,593 decoded frames.

SHA-256: `10ad9dd4b723533e31269826c2cf6c743134a8b98d43058da359983647636488`.

## Completed repairs

| Output span (end exclusive) | Change |
|---|---|
| 1:11.80–1:29.90; frames 2154–2696 | Revised the data diagram with a staged reveal of 15 participants, 18 measurements per person, one outcome that appears to stand out, and the conclusion “A chance result can look like a discovery.” Removed “inevitable,” “270 Data Streams,” and the single-person correlation annotation. The diagram uses the original paper background and follows the existing narrated progression. |
| 1:36.77–1:42.40; frames 2903–3071 | Replaced only the heading with “DELIBERATELY FLAWED STUDY.” Its opacity follows the original heading's fade. The journalist, panel, data symbols and subsequent headline-spread animation remain. |
| 1:46.60–1:55.60; frames 3198–3467 | Replaced the article's gibberish with three legible evidence-checking questions. The imagegen edit preserves the annotated-paper/red-pen composition; a restrained 2.5% pullback keeps the text in view. |

The narration, pauses, opening, canonical boards, existing board-camera treatment, callbacks, and close retain their v14 timeline positions. No audio splice or new narration was introduced. The approved optional opening improvement was not part of this build.

## Source and asset provenance

The installed v14 file has source SHA-256 `194681a637a4b39c50aa7edcb6bb543cfad53c9febe301a2fc87eb6bdbeaead4`. Original Critical Thinking rolls are absent from `Prompts`, so this is one additional video encode from the finished source, with compressed audio copied rather than re-encoded.

An active-build snapshot is retained at `/private/tmp/critical-thinking-v15-source-194681a637a4.mp4`; the build checks its hash. Source frame 2154 supplies the blank diagram background. The heading mask uses the recorded source frame 3030. Their extraction was sequential, never a timestamp seek.

The project-owned generated image and its exact built-in imagegen prompt are in [the asset directory](../../scripts/video/assets/critical-thinking-v15/README.md). The diagram and heading graphics are reproducible code in [the build script](../../scripts/video/build_critical_thinking_v15.py).

## Verification on the actual encoded candidate

- OpenCV and FFmpeg each decoded all **5,593 frames**. Every video presentation timestamp advances exactly 512 ticks at a 15,360 Hz timescale: 30 fps without internal timing gaps.
- **Audio stream is bit-identical** to v14. Both compressed-stream SHA-256 hashes are `7951957d2b583306f1b274a7f3bb902532a99408a1272b1a44c47a19dc50c5c4`.
- All unedited frames remain aligned to their same source frame. Mean thumbnail pixel difference is 2.55/255, maximum 2.75/255, consistent with the additional encode. During the title patch, the rest of the frame remains aligned to the original animation.
- All six declared repair boundaries passed `transition_guard.py`. All six every-frame strips were visually inspected; no stale graphic or intermediate-shot flash was found. Full-resolution repaired endpoints and destination frames were also inspected.
- Four encoded-frame sheets cover every second of the repairs. The staged quantities, corrected heading fade, paper questions, and last repaired paper frame are legible and unclipped. The source's supporting drawings resume at the intended boundaries.
- The paper pullback has continuous small frame differences, with eased near-stationary endpoints. No extra cuts were introduced inside it.
- Build/QA scripts compile. `git diff --check` passed.
- The installed Critical Thinking video and board files remain unchanged. No tracker rows were edited.

Evidence: `edit-manifest.json`, `verification/verification.json`, `verification/ffmpeg-decode.log`, `verification/repaired-sequence-*.jpg`, `verification/transitions/`, and full-resolution endpoint frames.

Commands:

```sh
.video-venv/bin/python scripts/video/build_critical_thinking_v15.py --preview
.video-venv/bin/python scripts/video/build_critical_thinking_v15.py
.video-venv/bin/python scripts/video/qa_critical_thinking_v15.py
```

The builder refuses to overwrite an existing candidate. Use a new version for any later rebuild.

## Remaining review limits

No direct full-duration audiovisual playback or new auditory judgment is claimed. Encoded audio identity proves that this visual repair did not change v14's sound; it does not certify v14's earlier audio repairs. The prior transcript-based narration assessment remains provisional KEEP, with the previous owner-approved “explanations” repair retained exactly in the compressed audio stream.

The 35.23-second opening-board span, abrupt “Look at the left side” opening, and older board-ring treatment are retained under this narrow scope. The preceding evaluation identifies these limitations. This candidate is ready to review, not represented as newly certified for shipping. Public-site bytes were not verified.

## Local shipping — September 29, 2026

David explicitly approved v15 with “ship it.” Installed the exact verified candidate bytes at `course-assets/critical-thinking/critical-thinking.mp4`, updated the lesson cache key to `20260929critical15`, and refreshed only this video’s manifest hash/size. The displayed runtime remains “3 min.”

Local release commit: `317b89509ac24f1b6b72f91c32fdff6208df2215` (`Ship approved Critical Thinking v15 locally`). Exactly three release files are included. The committed video and installed file both match SHA-256 `10ad9dd4b723533e31269826c2cf6c743134a8b98d43058da359983647636488`. Audit/build records remain local.

Scoped scratch cleanup completed with no matching intermediates to remove. No push or deployment was performed. Status: **shipped locally; queued for batch deployment**. Earlier listening limitations and retained legacy treatment remain documented; shipping approval does not imply a newly performed auditory check.
