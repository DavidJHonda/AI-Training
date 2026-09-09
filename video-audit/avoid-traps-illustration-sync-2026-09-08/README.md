# Avoid Traps illustration-only sync — 2026-09-08

## Scope and status

Nine live videos were identified for illustration updates. Ten current lesson assets cover eleven mapped spans. Support Trap was approved and shipped on 2026-09-08. The seven other approved updates are now shipped: Opener, Hallucination, Training Bias, Document Trap, Mind Trap, Engagement Trap, and Fake Trap. Flattery Trap revision v3 is also approved and shipped. All nine Avoid Traps illustration updates are now live. Recoverable original videos and shipping receipts are retained in each final batch audit folder. See [REVIEW.md](REVIEW.md) for final deliverables. No lesson files were changed. The original mapping table below records the pre-build queue.

| Video | Mapped live-video interval | Status |
| --- | --- | --- |
| Opener | 1:48.100–1:53.667 | Queued |
| Hallucination | 2:04.133–2:12.467 | Queued; live uses v3, lesson uses v4 |
| Training Bias | 0:15.100–0:28.467 | Queued |
| Document Trap | 0:57.800–1:05.533 | Queued |
| Mind Trap | 0:24.633–0:35.900; 0:41.267–1:09.100 | Queued; preserve intervening native footage; Nate in both panels |
| Flattery Trap | 0:28.500–1:15.700 | Queued; remeasure all title, row, and banner targets |
| Engagement Trap | 3:31.633–3:54.600 | Queued |
| Support Trap | 0:13.500–1:02.800 | Approved and shipped |
| Fake Trap | 0:13.400–0:43.200; 1:59.367–2:20.100 | Queued; comparison and source illustration |

`replacement-map.json` stores live/asset hashes, integer half-open frame ranges, and timing sources. Midpoint contact sheets were inspected against the current lesson references. Before building each remaining video, inspect every boundary frame and check for additional cropped/repeated appearances. The broad SIFT scan in `inventory-scan.json` has false positives from shared fonts and is discovery evidence only, not an edit list. In particular, the Fake Trap source illustration must be located from its edit manifest and visual inspection, not that scan's peak match.

## Pilot QA

Shipping: verified the approved candidate SHA256 `48ad17d38fbeee9e0eb9cf521c86922d85d67c234ce61d5385885afc322289ec` matches `videos/support-trap.mp4`. Previous live video is recoverable at `support-trap-pilot/live-before-illustration-update.mp4`. The candidate and review reel were moved from Prompts to `support-trap-pilot/approved-shipped-candidate.mp4` and `support-trap-pilot/approved-review-reel.mp4`. The paths below describe pre-shipping QA. `index.html` was not modified.

- Candidate: `Prompts/support-trap-illustrations-patched.mp4`.
- Short review reel: `Prompts/support-trap-illustrations-review-reel.mp4`, 53.5 seconds. Reel starts at full-video 0:11.500, two seconds before the replacement; ends two seconds after it.
- Rebuilt from the pristine reroll and approved frame schedule. New artwork uses measured 1222×1287 coordinates; no old board coordinates reused.
- Final audio packet SHA256 exactly matches the shipped audio. The repaired complete word “secrecy”, all pauses, and narration are preserved.
- Exact decoded frame count: 6,312 / 6,312. Runtime 210.400 seconds, 30 fps.
- Sampled 163 corresponding frames outside the changed span; maximum mean absolute pixel difference 0.1743 on a 0–255 scale, attributable to encoder context. No outside visual content changes observed.
- Inspected all eight comparison entry/state/exit strips, including each frame within 12 frames of each boundary. No stale-graphic flashes found. The detector flagged the continuous pan at frame 810, not a stray graphic. Four remaining flags are inherited danger-board camera transitions at 4836, 5226, 5592, and 5964, outside this update.
- Native macOS playback and first-frame decode passed for both candidate and review reel.
- Live video and lesson assets unchanged. No writes to index.html.

## Repeatable procedure

1. Freeze the live baseline and current lesson asset hashes; abort if either changes.
2. Map every occurrence on the finished timeline using actual visual cuts, not narration timestamps alone.
3. Measure canonical full-box boundaries on the replacement image. Keep approved timing, accent colors, and shot intent; adapt camera geometry only as needed.
4. Rebuild once from pristine sources and the approved edit schedule. Stream-copy the approved live audio, never reconstruct it for an illustration-only pass.
5. Verify exact frame count, FPS, audio payload hash, unaffected shots, settled highlight states, and every-frame boundary strips.
6. Supply a short changed-segments reel with full-video time mapping plus the complete candidate.
7. Ship only after approval, retaining the existing live filename and recoverable backup. Archive the shipped candidate out of Prompts. Never edit index.html for this workflow.
