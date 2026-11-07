# Your Home Base v10 — review candidate

Completed November 7, 2026. Narrow visual repair under the approved chat plan.

## Result

- Three purpose-generated photographic scenes show one of the existing students planning Art Night with ChatGPT, comparing two plans with Claude, and organizing documents/email with Gemini. Their style follows Questions Matter at 0:40.
- Replaced the abstract comparison from 46.800–68.133 seconds and the three matching monitor cutaways at 79.100–83.200, 94.967–98.800 and 113.000–118.133 seconds.
- Revised the existing two-student board: CLAUDE on the left, CHATGPT in the center, GEMINI on the right. The 150.233–162.433-second camera move now focuses on the center workstation, keeping both students' faces and the sign visible.
- The detailed side-by-side board retains its original teaching copy, camera and highlights. The longest uninterrupted board run is 18.467 seconds. Other source visuals and the closing board are preserved.

## Deliverables

- Full candidate: `../../Prompts/your-home-base-v10.mp4` (1280×720, 30 fps, 190.1 s).
- Interactive before/after review: `review.html`, with contextual excerpt buttons and original/candidate versions. Served locally at `http://127.0.0.1:8878/video-audit/your-home-base-scenes-v10-2026-11-07/review.html` during review.
- Staged revised lesson board: `../../scripts/video/assets/your-home-base-scenes-2026-11-07/your-home-base-home-base-v10.jpg`.
- Source images and full built-in image_gen prompts: `../../scripts/video/assets/your-home-base-scenes-2026-11-07/` and `generation-record.json`.
- Reproducible builder: `../../scripts/video/build_your_home_base_v10.py`.

## Verification

The source is retained finished v9 with SHA-256 `27fd288d9c1dc240ee3e34cc4d57223bdd26d42c4dbb2d8453ed181974428145`. It matches the installed source. Earlier raw rolls are unavailable; this is one additional picture encode from v9.

- Decoded all 5,703 candidate frames. Runtime and FPS match the source.
- AAC audio packet payload matches the source exactly. No audio edits, new pauses or timing changes.
- Compared every decoded output frame with its expected source or replacement at 320-pixel analysis width: 4,305 unaffected frames (maximum mean absolute difference 3.155/255) and 1,398 replaced frames (maximum 2.671/255). Differences are consistent with encoding; no stale visual frames detected.
- All 12 actual visual splices passed `transitions-cuts/transition-guard.json`. Every-frame strips were inspected. Each destination begins at its planned boundary.
- An initial diagnostic also treated continuous camera beat changes as cuts and flagged two portions of the intentional zoom. Those strips show continuous motion; all 366 board frames independently match the planned camera render. The original diagnostic is retained under `transitions/`, and the actual-splice report is under `transitions-cuts/`.
- Inspected final encoded 720p frames for all three scenes and the center-sign camera hold: text is readable; center sign and both students are visible. Full board opens for over three seconds before the closer view.
- Verified browser playback: 190.1-second duration, ready state 4, no media error, full seekable range, and playback at the selected Claude and Gemini excerpt timestamps. The browser tab is retained for review.
- Source video, installed canonical boards, current lesson Markdown and `index.html` remain unchanged by this video pass. The earlier requested TRY IT copy edit remains in the working tree.

## Scope limits and status

Shipped locally on November 7, 2026 after explicit owner approval. Commit `a2d6bbed7e84040de9cea700305ae2fd87425c74`. The approved board and video are installed together; image/video cache keys and all corresponding manifest rows are updated. Queued for batch deployment. See SHIP.md and install-verification.json.

No direct audio listening audition is claimed. Audio identity is established by packet hash; browser playback and visual inspection are separate checks. This narrow pass did not repeat the full-course narration audit or whole-file shipping checklist. Previously approved text-focused teaching-board zooms remain unchanged. Video Tracker was not accessed and no tracker status is inferred.
