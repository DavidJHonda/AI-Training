# Embeddings v4 review

Output: videos/embeddings-v4.mp4 — 3:58.167, 7145 frames at 30 fps.

Requested changes:
- Restore embeddings-2 opening picture and narration through its original 18.7-second scene cut.
- Current student illustration begins at 18.7. Camera moves in from 22.73 to 24.13, holds both spoken IDs (1024 and 2048), and returns to full board from 29.27 to 30.17 for the remainder of the explanation.
- Remove the custom word-piece board. Continue the current embedding table briefly, then restore the original Notebook animation on its exact source cut (235.033 source seconds, 216.967 output seconds).

Other edits, pauses, board highlights, and approved closing retained. Source rolls, live video, index.html and lesson Markdown unchanged. Previous review versions retained.

Verification:
- Full decode passes; 7145/7145 frames.
- All 5296 board/camera frames match intended rendering within codec tolerance.
- Compared all 913 restored source frames against original frames; maximum mean pixel error 2.658.
- Audio after the opening is preserved from v3; only a five-millisecond room-tone join was recalculated. Encoded waveform correlation exceeds 0.9998.
- Four one-second pauses, 0.4-second join, and 2.533-second closing hold verified.
- All 21 actual splices pass transition guard and manual every-frame strip review.
- Four additional camera-keyframe guard windows flag the intentional continuous zoom. Inspected these separately; no unexpected visual source or cuts. Original flag report retained in transitions; actual splice report in transitions-splices.

The original Notebook token IDs and opening wording are restored as requested, including the numerical inconsistencies identified in the earlier evaluation. No substitute diagrams or narration were added to those original spans. This is a review video, not shipped.
