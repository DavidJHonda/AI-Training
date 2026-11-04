# Work With AI opener v14

Built November 4, 2026 following the owner's “build it please” approval of the roll-5 cut-only plan. Shipped locally after the owner approved v14 with “ship it.” Queued for batch deployment; not pushed or published.

- Candidate: `Prompts/work-with-ai-opener-v14.mp4`
- Duration: **2:11.3**, 3,939 frames, 30 fps, 1280×720.
- Bytes: 15,573,500.
- SHA-256: `d4ebc011f34379f409e43e815a155ded5f8af847f6df0b7798b0f644776d2052`.
- Source: `Prompts/work-with-ai-opener-5.mp4`, SHA-256 `d307f2b4f61ce5b606160f9225a03a59a3f654d8e21b032745c776f7acd18f0c`.
- Builder: `scripts/video/build_work_with_ai_opener_v14.py`.
- Approved plan: `../work-with-ai-opener-rerolls-2026-11-04/REVIEW.md`.

## Edit

All narration comes from roll 5. No new voice or cross-roll narration. Removed the identical-server/only-variable passage, formal operational-method detour, overextended camera explanation, entirely-dependent assertion, redundant map elaborations, closing preamble, and post-closing paragraph/outro.

Exact removed source intervals: 22.600–43.300, 63.600–73.100, 80.533–84.200, 121.400–131.500, 161.467–173.600, 176.200–196.000. Closing narration ends at source 203.200. Each boundary falls in a measured quiet gap; see `audio-cut-measurements.json`. Standard 5 ms edge fades use matched room tone. No new instructional pauses; four seconds of final hold after closing audio.

The current Same Tool and Work With AI JPGs replace generated board recreations and misleading technical graphics. Full unmarked openings, static full view, one whole-image/row outline at a time, locked accent colors, 4 px stroke. Retained the animated draft and camera comparisons, goal/checking illustrations, app-choice drawing, and instruction drawing. The standard white closing board begins at output 2:00.1, holds 48 frames, pushes for 150 frames to 1.2×, and settles through the literal last frame. The first incoming source frame covers eight and four otherwise stale frames at the two early cuts; the source illustrations' own fade-ins remain.

## Verification and limits

- Complete assembled-audio ASR read in `transcripts/edited.txt`: 351 words. All intended sentences survive, including the qualified details statement, complete model/thinking/research options, map takeaway, and both exact closing lines. No fragments from the removed sentences appear.
- All 13 timeline boundaries passed `transition_guard.py`; all every-frame strips were visually inspected via four aggregate review sheets. No stale graphic islands found.
- Inspected all three finished-video contact sheets, every board highlight state, and the literal last frame. Canonical boards are legible and uncropped; close finishes correctly. The final frame is saved as `last-frame.jpg`.
- Full ffmpeg decode: no errors. Sequential count: 3,939 frames, 30 fps, 1280×720. Technical evidence in `technical-qa.json`.
- Corner cleanup processed all 1,830 retained source frames: 1,286 clone, 544 inpaint, zero declined. Sampled finished frames inspected.
- Hash checks confirm raw source, all canonical boards, and installed work opener remain unchanged.

**Direct listening and continuous playback with narration were not performed.** Waveform and transcript checks support cut placement and content completeness; they do not establish audible join quality, pronunciation, or delivery. This candidate is ready for the owner's evaluation, with listening review outstanding.

Reproduce with `.video-venv/bin/python scripts/video/build_work_with_ai_opener_v14.py` (choose a new candidate version if v14 already exists). `--prepare-only` assembles the audio and edit manifest before rendering. Source/output spans, board specifications, protected hashes, room-tone measurements, and rendering hash are in `edit-manifest.json`.

## Local shipping

- Owner approval: “ship it,” November 4, 2026, following disclosure of the listening-review limitation. Proceeded under that approval; direct listening and continuous playback remain unperformed, not represented as passed.
- Local commit: `0a0576822095c571b3232f2c82b348c3ebf9cbbc` (`Ship approved Work With AI opener v14`).
- Installed at `course-assets/work-with-ai-opener/work-with-ai-opener.mp4`; SHA-256 and bytes exactly match the approved candidate above.
- Course cache key: `20261104ship14`; displayed duration remains `2 min`. Manifest records version 14, updated bytes and hash; original migration fields preserved.
- `python3 scripts/verify-course-assets.py --migration-hashes`: PASS (248 assets, 519 mappings, 263 page references, 55 videos). Scoped staged diff check passed. Only the video, its manifest entry, and its course reference were committed; unrelated working changes preserved.
- No push or deployment requested or performed.
