# Vector Space v9 — stable mystery-drink transition

[Candidate](/Users/davidobrien/Developer/AI-Training/Prompts/vector-space-v9.mp4) · [12-second transition preview](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-28-v9/transition-preview.mp4)

The neighborhood board in v8 pushed from a camera width of 1668 to 1626.337 pixels, enlarging the board by approximately 2.56%. At 2:04.967 the mystery board returned to the original width, making the map jump smaller.

V9 removes that push. Both canonical boards now use the same fixed camera `[834, 470, 1668]`, with their existing highlights and full-board introductions. Only the neighborhood-board framing at frames `[3187, 3749)` is changed. The map's stable features align: 2,691 feature correspondences yield an effectively identity transform (see `alignment-check.json`). The source JPGs are unchanged.

The output remains 3:25.13, 6,154 frames at 30 fps, 1280 × 720. V8's AAC audio is copied, and its compressed-audio hash matches exactly. No narration, pause, or timing change was made. Source videos, canonical JPGs, lesson Markdown, live video, and v8 retain their protected hashes.

Verification: complete sequential video decode; transition guard passed at both affected boundaries (frames 3187 and 3749); their every-frame strips and the encoded mystery-board arrival were visually inspected. The before/after framing comparison is in `transition-before-after.jpg`. This narrow repair does not repeat v8's narration review or claim new listening verification; its outstanding listening review remains applicable.

Build: `scripts/video/build_vector_space_v9.py`. Manifest: `edit-manifest.json`. Evidence: `qa.json`, `alignment-check.json`, `encoded/`, and `guard/`.

Candidate SHA-256: `53a9bb18646f9160e91291c9957a00751edf15285fd548919c9d7a6ab7b4dd25`.

## Shipping approval — September 28, 2026

David approved v9: “ship it.” The exact reviewed bytes are installed at the canonical live path with cache key `20260928ship1`. Duration remains 3:25.13, shown as “3 min” under the course's existing rounded-minute convention. The source lesson and canonical boards are unchanged. The owner authorized shipping after the disclosed listening limitations; no additional perceptual-listening claim is made.

The repository-wide asset verifier reports existing unrelated discrepancies; its output is identical before and after this replacement. Vector Space's installed hash, manifest hash/size, and course reference match. See `shipping-receipt.json` and `shipping-verification.json`. Remote verification will be recorded in `published-verification.json` after deployment.
