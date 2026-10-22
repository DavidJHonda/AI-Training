# Transformer v15 — requested highlight adjustments

Candidate `Prompts/transformer-v15.mp4`, 3:58.767, 7,163 frames at 30 fps.
Shipped locally on 2026-10-22 after David’s “Ship it.” Queued for batch deployment.

[Play v15](http://127.0.0.1:8765/video-audit/transformer-build-v15-2026-10-22/review.html).

- The full CAT sentence section remains outlined through its spoken answer
  (40.733–42.733), instead of switching to the top line.
- The full MILK sentence section remains outlined through its spoken answer
  (43.100–47.100), instead of switching to the top line.
- Removed the highlight on the unspoken “We know IT refers to CAT” line
  (70.000–73.800). Existing token and spoken takeaway highlights remain.

Only highlight specifications changed. Cameras, boards, supporting scenes and
timing retain the approved v14 plan. Reassembled from the same retained v12 visual
source and canonical boards to avoid an extra finished-video encode. The v14 AAC
stream was copied without re-encoding and its extracted payload hash is identical.

## Verification

- Full sequential decode: 7,163 frames at 30 fps, 238.766667 seconds, unchanged.
- Encoded changed-section frame sheets inspected, including highlight transitions.
- Prepared-to-encoded visual checks pass (maximum mean RGB error 2.749/255).
- Transition guard: five boundaries pass automatically; the sixth flags the
  unchanged pullback near 47.1 seconds. Its every-frame strip was inspected: smooth
  planned camera movement, no stray intermediate graphic.
- Browser playback and both new jump buttons (0:40, 1:08) pass with no page errors.
- Existing lesson, assets, installed video and prior candidates are unchanged.
- No new listening claim: audio is byte-identical to v14, whose continuous
  perceptual review remains pending. No ship-checklist pass is claimed.

Source/build details and hashes: `edit-manifest.json`, `verification.json`.
Rebuild script: `scripts/video/build_transformer_v15.py` (refuses to overwrite).
Earlier complete narration/board review: `../transformer-build-v14-2026-10-22/REVIEW.md`.

Candidate SHA-256: `b62c896073195493b5078684d097d4e2187b3d7c89ed3b9916caedd7d3024ff1`.
Copied AAC payload SHA-256: `b6da39ae4133aafc4bc523e8b8bca3533f3069ca721b4e91660f907c510720cf`.

## Local release

Installed the exact candidate at `course-assets/transformer/transformer.mp4`.
Updated the course cache key to `20261022ship-transformer-v15`; displayed runtime
remains 4 min. Installed and HTTP-served hashes match the approved candidate.
Local commit: `394b916744c7c1d64edb6c574cc60c75d0332382`. No GitHub push or deployment.
Assistant perceptual listening remains unclaimed; owner shipping approval followed
the delivered review. See `shipping.json`.
