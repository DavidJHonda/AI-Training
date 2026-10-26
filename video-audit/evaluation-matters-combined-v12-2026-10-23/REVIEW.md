# Evaluation Matters v12: Quick Review transition

Shipped locally on 2026-10-23; queued for batch deployment. User explicitly approved v12 with “Ship Evaluation Matters.”

Added “Let's focus on the quick review process shown here.” before the existing “Step one is to read.” The introduction plays over the full, stationary Quick Review board.

- Candidate: `Prompts/evaluation-matters-v12.mp4`
- Duration: 3:51.27; 6,938 frames at 30 fps.
- Inserted at 1:18.17; 2.90 seconds long. Existing Read instruction follows at 1:21.07, with speech beginning at approximately 1:21.46.
- Donor: `Prompts/evaluation-matters-1.mp4`, frames 2391–2478 (end exclusive), 1:19.70–1:22.60.
- Source audio endpoints measured at approximately −77 and −81.8 dBFS.

The rest of the edit is preserved. Assembled PCM before and after the insertion matches v11 sample for sample. Later chapters move forward by 2.9 seconds. Sources and installed video remain unchanged.

## Verification

Full decode completed with constant frame timing. Fresh transcription confirms the complete new transition and the following Read instruction. Both insertion boundaries were inspected using every-frame contact strips. Encoded audio correlates with the assembled audio at all joins (minimum 0.999969).

The automatic transition guard passed 24 of 29 boundaries. Its five flags are the previously reviewed camera transitions, shifted by 87 frames. All 125 frames in those neighborhoods are pixel-identical to the corresponding decoded v11 frames. The raw guard result is retained; this is a manual disposition, not an automatic pass.

Direct listening and continuous audiovisual playback have not been performed. Please listen around 1:18–1:23 for voice continuity and pacing.

Evidence: `qa.json`, `repair-preservation.json`, `transition-review.json`, `transitions/`, and `transcripts/evaluation-matters-v12.txt`.

## Local release

- Commit: `acee3d7e` (`Ship Evaluation Matters v12 with revised evaluation boards`).
- Installed: `course-assets/evaluation-matters/evaluation-matters.mp4`.
- SHA-256: `1d861ec8762e9756f17da06eef4f4505edd14de9f22b76039d29369ea7f2095d`.
- Lesson cache key: `20261023ship12`; displayed runtime remains 4 min (actual 3:51.27).
- Confirmed candidate identity, unchanged source/board/lesson hashes before installation, and local HTTP lesson reference and served MP4 hash after installation.
- Owner ship approval followed the disclosed listening limitation. No agent listening or continuous playback is claimed.
- Only the canonical video and its index reference were committed. No push or deployment performed.
- Removed six regenerable WAV scratch files (0.11 GB); retained candidate, raw donors, build scripts and QA evidence.
