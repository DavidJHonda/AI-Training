# How AI Answers v11 — two visual repairs

Approved scope: David requested the two visual fixes from the live evaluation and explicitly excluded the optional narration tightening. Review candidate only; no local shipping or public deployment authorized by this build request.

Candidate: `Prompts/how-ai-answers-v11.mp4`.

## Changes

- **2:48.967–3:05.967:** place “You” and the smaller “First reply token” caption inside the existing red square beside the dog. Preserve the artwork, camera, span, and narration. The label is centered using the square's measured colored bounds.
- **Approximately 3:20–3:25.933:** brighten both existing `<EOS>` labels in the stopping-token illustration. Recolor the original letter shapes rather than covering the moving boxes. The change follows their existing opacity/fades and leaves borders, percentages, sequence, and timing intact.

The picture is rebuilt from the same retained pre-v8 source and canonical board composition used for v10, with all v10 timing, rings, question reprise, shorter ending, and closing treatment carried forward. No lossy v10 picture is used as a new picture source. The **v10 AAC audio stream is copied unchanged**.

Sources: original source `c0e56437479d467ffaea26ff6ca51e93019e7cb18a041f3b980b038f7ff3f1fa`; v10/audio source `451fa414b0e0fbc971e71b6ccb7ae8d1663e001b1a1ed25c297466e373d73b3e`. Paths, protected asset hashes, and frame spans are recorded in `edit-manifest.json`.

Board/camera treatment: no course-board changes. Preserve the board table in `../how-ai-answers-live-review-2026-09-29/REVIEW.md`, including its previously approved long-run exception. No narration cuts, grafts, or added pauses.

## Verification

- Complete decode: 6,590 frames at 30 fps, 1280×720, 219.667 seconds; identical runtime and frame count to v10.
- Compressed AAC payload SHA-256 matches v10 exactly: `306733fb5c6920244c6d31d5e06bedea918980bdbe4e85e75fb1d7568618ef2c`.
- Compared 397 frames outside the repair windows with v10: maximum mean absolute pixel difference 0.761/255. Compared all 708 frames in the two repair windows outside their small patch regions: maximum 0.533/255. Differences are consistent with the independent encode, with no timing shift or unrelated visual change detected.
- Dog-label tracking is stable across all 510 affected frames (one measured bounding box). Both EOS glyph masks remain present through their fully visible intervals; fading samples were inspected.
- All 21 declared boundaries passed the automated transition guard. Visually inspected the four repair-edge strips, all three encoded contact sheets, delivery-resolution repaired frames, the next Inference frame, and the literal final closing frame. No leaked labels or new transition islands found. The original paper-only opening to the next animation at 3:05.967 is retained from v10.
- Original source, v10 candidate/audio, canonical video, lesson, index, and protected JPG hashes remained unchanged through this build.
- Candidate SHA-256: `e38783730880f2a64d578670a8715e1a2c7b05881e2dc19fd3b27273ff286ce4`.

Evidence: `qa.json`, `tracking.json`, `encoded/`, `encoded-sheet-*.jpg`, and `guard/`. Build: `scripts/video/build_how_ai_answers_v11.py`; verification: `scripts/video/qa_how_ai_answers_v11.py`.

**Ready for owner review.** No installation, commit, or publication performed.

## Limits

No new perceptual audio listening or uninterrupted whole-file playback is claimed. The original v10 listening checkpoints and accepted narration simplifications remain as disclosed in the live review. This is a narrow visual repair for review, not a new whole-file shipping certification.

## Local shipping — September 29, 2026

David approved the exact candidate with “ship it” after the disclosed review limits. Installed v11 at the canonical course path, verified the installed and committed video hash, updated the cache key to `20260929ship1`, and synchronized the asset manifest. The displayed runtime remains “4 min.”

Commit: `fd4f58327672fc24cf7ff2505e9f352302e22475`. Installed SHA-256: `e38783730880f2a64d578670a8715e1a2c7b05881e2dc19fd3b27273ff286ce4`.

**Shipped locally; queued for batch deployment.** No push or deployment was performed. This approval does not turn unperformed perceptual listening into a completed check. See `shipping-receipt.json`.

Post-commit cleanup removed only the four regenerable board canvases in this v11 audit folder. Candidate, sources, review evidence, and other active builds were retained.
