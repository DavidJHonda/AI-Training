# Engagement Trap: flat Editorial frame

Shipped 2026-09-07 on owner approval to `videos/engagement-trap.mp4`.
Approved candidate `Prompts/engagement-trap-patched-v4.mp4` was moved to the live filename.
SHA256: `dbb4cbeb2b0f6dea8a28902b128d655278d3fd46e9d86340d10f03cbccb603bf`.
Previous live video retained locally as `live-before-ship.mp4` in this audit folder.

Rebuilt the illustration's outer frame with the standard Editorial feature-board renderer and exact #eae7fd lavender, matching the video canvas. The approved inner scene was extracted pixel-identically from the previous gaze-corrected lesson image; no generated background-edit trials were installed. Canonical title and takeaway retain the exact wording. Page image and preparation JPG were updated together.

Changed video interval: 3:31.633–3:54.600 only. The updated AI Chat board from v3 remains unchanged. Visuals rebuilt from the pristine roll, approved narration stream-copied.

Verification: 7,265 decoded frames at 30 fps, 4:02.167 runtime. Compressed AAC and decoded PCM hashes match the approved audio exactly (`qa/integrity.json`). All 14 boundaries passed the transition guard. Both illustration-boundary every-frame strips and the settled full-resolution illustration frame were visually checked: no old-board flashes, no visible inner frame. Approved inner artwork crop verified pixel-identical before placement by the native renderer.

No index.html edits. Live video replacement hash verified against the approved candidate.
Earlier review candidates remain; no broader cleanup was requested for this ship.
