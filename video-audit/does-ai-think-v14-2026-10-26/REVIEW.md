# Does AI Think? v14 — different students on the right

Updated 2026-10-26 for the request to use different people on the right of “When You Think. What AI Does.”

## Change

The right-hand photo now shows a red-haired student and a dark-haired student with glasses. The existing left image, board title, three comparison rows, typography, layout, and takeaway are preserved. Pixel comparisons of the title, left scene, and text/banner regions passed; see `board-preservation.json`.

Edited the right-hand source with the built-in image generation tool (`image_gen.imagegen`). The exact prompt is saved in `image-prompt.txt`; source paths and hashes are in `image-source-record.json`. Rebuilt the canonical board with the existing renderer, refreshed its cache key in `index.html`, and updated the cast inventory.

- Board: `course-assets/does-ai-think/does-ai-think-side-by-side.jpg`
- Right-panel source: `scripts/video/assets/does-ai-think-unified/what-ai-does.png`
- Candidate: `Prompts/does-ai-think-v14.mp4`
- Build: `scripts/video/build_does_ai_think_v14.py`
- QA: `scripts/video/qa_does_ai_think_v14.py`

## Video preservation and validation

The candidate retains v13’s shortened setup, wall-chart treatment, three-row board, camera movements, highlighting, cutaways, and narration. It is 5,272 frames at 30 fps, 175.7333 seconds (about 2:56), 1280×720. The changed board appears at 106.8–149.0 seconds, with the existing cutaways retained.

All 8,239 AAC packets, timestamps, and durations are identical to v13: audio was copied without re-encoding. Timeline and highlight specifications also match v13. See `audio-stream-preservation.json` and `timeline-preservation.json`.

Automated checks passed: uniform frame timestamps, protected source hashes unchanged, and 155 encoded frame samples compared with the intended renderer (minimum PSNR 33.88 dB). The full board and encoded full-board/three-row highlight samples were visually inspected. Eight encoded transition strips were inspected at frames 3204, 3654, 3744, 4164, 4254, 4314, 4344, and 4470; these show the intended cuts and continuous camera motion without a stray frame.

The transition guard flags 9 of 31 boundaries. The two affected comparison-board flags (4314 and 4344) are expected camera pullback/highlight changes, confirmed in their strips. The other seven flags are in the unchanged Chinese Room sequence and were previously reviewed in v13; they were not manually re-reviewed here.

No direct listening or continuous playback was performed for v14. The pending v13 listening review remains applicable because audio is bit-for-bit identical. This is a visual repair candidate, not a new full audiovisual approval.

Candidate SHA-256: `5683aea0573ffc5fbe8fddaf2c6f3c2f2acfec1e8ee46913299d876c5d6f5049`.

## Delivery state

Owner authorized shipping with “ship v14” on 2026-10-26. Installed v14 at `course-assets/does-ai-think/does-ai-think.mp4`; both the installed file and committed blob match the candidate SHA-256 above. Updated the lesson video cache key to `20261026ship-doesaithink-v14` and runtime label to `3 min`. Local commit: `7cf497656bef70d6e076d555ec66d9a453a7e7b2`. Shipped locally; queued for batch deployment. No push or publication performed. The disclosed listening limitation remains; owner shipping approval is recorded separately from technical review. See `shipping-receipt.json`.
