# What Is AI? — closing update, v19

Review candidate: `Prompts/what-is-ai-v19.mp4`, 160.2 seconds, 4,806 frames at 30 fps. Closing begins at 152.000 seconds. Shipped locally in commit 3debb1e4; queued for batch deployment.

User approved take 8 and requested the closing question “What can it help you do?” The lesson, canonical closing artwork, Markdown, active generation prompt/upload set, and Start Smarter packet now use that wording. The earlier closing-only generation kit remains a historical record of the original request.

Both closing sentences come from `Prompts/what-is-ai-8.mp4`, source 266.666667–271.166667 seconds, placed at output 152.000–156.500 seconds with active-speech gain matching and 5 ms room-tone edge fades. The existing first 152 seconds retain the v17 source-frame map and all 7,296,000 pre-encode PCM samples exactly. The final board uses the current canonical JPG: 48-frame hold, 150-frame push to 1.2x, 48-frame settled hold.

The final voice gap is 1.596 seconds (150.663–152.260), preserving v17’s 1.604-second gap. V18 was superseded before delivery because its opening silence was longer. The final narration ends at about 155.464 seconds; the existing overall duration stays 160.2 seconds.

## Verification

- Decoded every actual frame: 4,806 frames, continuous 30 fps timestamps; maximum frame MAE 3.078 against expected composition.
- Encoded-audio correlation to assembled PCM: 0.99998483. Protected source and board hashes unchanged.
- Transition guard passed all nine declared boundaries; the replacement-close boundary and final frame were visually inspected. No stale old closing image appears.
- Final ending transcription contains both closing sentences and no former “Start with something you want to do” line.
- Asset verification and diff whitespace checks passed. Packet has seven pages; updated What Is AI page was rendered and visually checked.

## Listening limitation

No direct audio audition was performed. The owner reports “can”; small.en transcribes “could” in both the donor and encoded ending. The accepted take was preserved unchanged, without attempting a word splice. Exact can/could and perceived voice/transition quality still need owner listening; this is a review candidate, not a shipping verdict.

## Local shipment — 2026-11-02

Owner explicitly approved shipment with “ship it” after receiving the review candidate and the listening limitation. Installed exact v19 at `course-assets/what-is-ai/what-is-ai.mp4`; cache key `20261102ship19`. No independent listening is claimed.

Commit: `3debb1e49d070d9f62f4a3147b88a70be4aca3e1`. Installed SHA-256: `7fbdb27ea14176b3268b9d71a3c8a567ff1c80bf365d34cb76349f63d19e43aa`.

Asset migration-hash checks, staged JavaScript parse, targeted order/navigation checks, and installed/candidate byte identity passed. Commit includes the previously approved Probability & Prediction placement because the updated packet contains that lesson. Unrelated working edits remain uncommitted. No push or deployment performed. Render-scratch cleanup reclaimed 0.08 GB from this lesson’s November 2 review builds; raw takes, candidates, and review records retained.
