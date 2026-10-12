# Vector Space v20 — lesson sentence card

User requested the actual lesson sentence format in place of v19’s plain text graphic. This authorizes the narrow visual revision; all prior narration/timing approval is reused.

Candidate: `Prompts/vector-space-v20.mp4`, 1280×720, 30 fps, 7,693 frames, **4:16.43**. Review player: `v20-review.html`.

## Change

Captured the current `index.html` element labeled **THE SENTENCE**, using the locally bundled Plus Jakarta Sans font. Preserved its purple left border, rounded outline, label, quotation marks, teal CAT circle, and blue IT badge. Captured at a 900 CSS-pixel card width and device scale 2, fitted to 1,160 pixels wide, centered on a white 1280×720 canvas. Same single-line sentence format as the supplied screenshot.

The complete card remains static from frames **6188–6533 inclusive (3:26.27–3:37.80)**. No new highlights, motion, pauses, or breaks. The existing map resumes at frame 6534. Original-source picture rendering preserves the rest of the approved treatment. V19’s AAC audio is stream-copied without re-encoding.

## Checks

- All 7,693 frames decoded; duration and dimensions unchanged.
- AAC packet SHA-256 matches v19 exactly: `5483a0f20904de65b75b774f370c802ceabf973883c0c3dcabe9a1f9f37e1291`.
- 249 unaffected picture samples compared with v19; maximum mean pixel difference 0.08494/255, consistent with encoding variation.
- 16 sentence-card samples match the source capture within the measured RGB/YUV conversion tolerance. First encoded card frame inspected at full size for legibility, complete content, shape, and positioning.
- Transition guard passed both changed visual boundaries. Every-frame strips inspected: direct cuts into the new card and back to the existing map; no stray intermediate frames.
- Protected hashes confirm v19, the live video, lesson page, source roll, and canonical boards unchanged.

This remains a review candidate. V19’s pending subjective voice-blend listening check remains pending; no new audio changes were introduced. Full-file real-time watching/listening and wider shipping checks were not repeated for this picture-only revision. Earlier approved 29.1-second context-board hold and supporting scenes remain unchanged. No installation, commit, push, or tracker update.

Reproduce with `capture_sentence_v20.cjs`, then `build_v20.py`; verification is in `verify_v20.py`, `v20-verification.json`, and `v20-transitions/`. `sentence-capture-v20.json` records the source element, capture bounds, and URL; `v20-manifest.json` records source hashes, changed frames, and candidate hash.

## Shipping — 2026-10-10

David accepted the reviewed candidate with “ship it.” Installed at the canonical lesson path and updated its cache key to `20261010ship-vector-space-v20`. Local HTTP checks verified the page reference and exact served file hash. Committed only the video and its one-line reference update as `12336bdbd4641d16dd2bffe9fd78c27f41a79580`; unrelated Your Choices edits in `index.html` remain uncommitted. Audit records remain local.

The final whole-timeline automated transition check passed all 47 inherited/new boundaries. Prior frame comparisons, card/transition inspection, audio packet identity, decoded-frame count, and encoded passage ASR support this narrow release. Owner acceptance is recorded separately from editor verification: no additional direct listening or full-file real-time watch was performed, and neither is represented as passed. The unchanged portions inherit the previously accepted edit.

**Shipped locally; queued for batch deployment.** No push or deployment. Removed seven regenerable scratch files (about 0.08 GB), retaining candidates, raw rolls, screenshots, transcripts, and records.
