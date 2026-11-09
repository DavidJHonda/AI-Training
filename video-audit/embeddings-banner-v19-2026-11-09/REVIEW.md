# Embeddings v19: banner border repair

User request: at 2:47, match the highlight to the banner border.

| Board | Highlight | Camera | Changed span |
|---|---|---|---|
| From Taste Ratings to AI Embeddings | Outline the full yellow takeaway banner at source-image bounds (40, 901)–(1560, 989), following its 12px corner radius. Keep the 4px output stroke. | Existing full-board framing. | 2:46.500–2:49.033 |

The previous outline was inset at (54, 912)–(1544, 979). Measured the canonical JPG’s yellow boundary to place the corrected outline. The repaired span uses the same highlight onset and ending.

Pictures are rebuilt from the original roll using the established v18 renderer. Audio is stream-copied from approved v18. No narration or timing changes. Candidate: Prompts/embeddings-v19.mp4. Approved v19 is now installed locally.

Verification passed: all 5,722 frames decoded; all 76 repaired frames match the corrected border coordinates; all other frames match v18 within encoding tolerance (maximum mean pixel error 0.000115). Encoded audio payload is identical to v18. Both transition guards pass. The actual encoded 2:47 frame was visually inspected.

Local release: 646f6bbf6c7e1b64b97df76c24075a9aef77a11f. Cache key: 20261109ship19. Served video bytes match the approved candidate; asset integrity and browser checks pass. Shipped locally; queued for batch deployment. No push or public deployment performed.
