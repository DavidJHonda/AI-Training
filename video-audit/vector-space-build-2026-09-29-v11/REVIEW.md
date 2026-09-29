# Vector Space v11 — opening and neighborhood highlights

[Candidate](/Users/davidobrien/Developer/AI-Training/Prompts/vector-space-v11.mp4) · [Neighborhood preview](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-29-v11/preview-neighborhoods.mp4) · [Opening preview](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-29-v11/preview-opening.mp4)

Narrow visual repair requested by the user: remove the yellow opening highlight and match the drink-map highlights to the shapes representing the neighborhoods. This is a review candidate; no shipping or publication is performed.

## Changes

- **0:05.80–0:23.23:** Removed the yellow marker stroke behind “The layers change the numbers.” The text, its placement, paper background, number tiles, and other opening reveals remain.
- **1:49.63–1:55.87:** The blue outline follows the soft-drinks neighborhood's tall oval.
- **1:55.87–2:04.97:** The purple outline follows the hot-drinks neighborhood's wider oval.

The outlines are fitted to the shaded silhouettes in the current canonical JPG. Text and dotted comparison lines interrupt the pale fill, so the extraction uses each shape's outside convex boundary for a smooth ellipse fit. This avoids a rough contour that would duck into the labels or follow the dotted lines. The resulting paths are retained in `neighborhood-contours.json`. Outlines are rendered after framing, at a fixed four-pixel stroke with antialiasing. No fill or tint is added.

## Board treatment

| Visual | Highlighting | Camera and timing |
|---|---|---|
| Opening number schematic | Plain “The layers change the numbers”; yellow stroke removed | Existing fixed framing and 0:00–0:23.23 duration |
| A Map of Drink Similarities | Initial unmarked view; blue soft-drinks silhouette, then purple hot-drinks silhouette at the existing cues | Existing fixed complete-board framing; 1:46.23–2:04.97 |

The source board image is unchanged. The mystery-drink board's existing number comparisons remain. The stable map-to-map framing remains intact. V10's dimensions graphic, larger context board, revised narration, and close are preserved.

## Assembly and verification

Pictures are reconstructed from the same canonical JPGs, code-native graphics, and retained lossless source excerpts as v10. The finished v10 MP4 supplies only its copied compressed AAC track; the repair does not re-encode the narration. Expected runtime remains 3:29.27, 6,278 frames at 30 fps, 1280 × 720.

Native previews of the clean opening and both outlined neighborhoods were inspected at full resolution before rendering. Encoded checks and audio identity are recorded in `qa.json`; affected transition strips are in `guard/`. The prior full-file transcript remains applicable when compressed-audio identity passes.

Direct listening was not repeated for this visual-only change. V10's disclosed listening limitation on the narration graft remains; this repair does not claim new audio certification. Source candidates, installed lesson video, raw rolls, lesson Markdown, and canonical JPGs are protected by hash checks. No lesson/index change, commit, push, or deployment.

Build: `.video-venv/bin/python scripts/video/build_vector_space_v11.py`. QA: `.video-venv/bin/python scripts/video/qa_vector_space_v11.py`.

Final checks passed: 6,278 decoded frames; 209.2667 seconds; exact compressed-audio identity with v10 (`99cf0d65f9b0982327aaaf760e222944274516ef1a4067aa7dfc0f4962bca825`). All six affected transition checks passed. Encoded opening and both neighborhood states were visually inspected, along with the every-frame strips for soft-drinks onset, the switch to hot drinks, and the transition to the mystery board. All protected hashes remained unchanged. One-second samples outside the changed spans have mean absolute pixel difference 0.0010/255 versus v10 (maximum sampled mean 0.0307/255), consistent with only negligible encoding variation elsewhere.

Candidate SHA-256: `91fc722c8173cd7903a11ac6e9bfb16de44a3188912ffcd02ac9632963f6b280`.


## Local shipping — September 29, 2026

David approved v11: “ship it.” Installed the exact approved candidate at `course-assets/vector-space/vector-space.mp4`, updated its manifest hash/size, and selected cache key `20260929ship1` in `index.html`. Duration remains 3:29.27, displayed as 3 min under the existing rounded-minute convention. Local release commit: `9ac45fba23aefeec3228d5407b3913ece190ebde`. Only those three release files are committed.

**Shipped locally; queued for batch deployment.** No push or deployment was performed. The installed SHA-256 matches the candidate (`91fc722c8173cd7903a11ac6e9bfb16de44a3188912ffcd02ac9632963f6b280`). The global asset checker has 131 pre-existing diagnostics; its before/after output is identical, so this release introduced no new diagnostic. Owner approval follows the previously disclosed listening limitations; no new perceptual-listening claim is made.

Post-commit scratch cleanup removed 21 regenerable files (0.17 GB) from the v10/v11 build folders only. Candidates, raw sources, retained donor excerpts, reports, transcripts, previews, and QA evidence remain.
