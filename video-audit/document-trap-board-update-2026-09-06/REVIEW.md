# Document Trap: current lesson boards

Status: ready for user review, not shipped. September 6, 2026.

Candidate: `Prompts/document-trap-patched.mp4`.
Duration: 6,812 frames at 30 fps (3:47.067), unchanged.

## Updated visuals

- 0:57.800–1:05.533: the titled **An Incomplete Answer** illustration. The complete banner, “Uploading a file doesn’t mean AI has read it all,” is highlighted from 1:00.200.
- 1:05.533–2:02.900: **Split, Search, Load**, using the exact current lesson JPG. Step rings follow the illustration's horizontal edges and include the full step copy. Cameras are centered on the new target bounds. The takeaway ring follows the complete banner.
- 2:17.767–3:04.067: **Four Moves for Better Retrieval**, using the exact current lesson JPG. Full-card rings track the actual outer boundaries. The original accent colors, walkthrough timing, smooth pans, and full-banner highlight are retained.
- The regular-season/tournament opening, other retained source graphics, narration edits, and standard close are unchanged.

## Verification

- Rebuilt from the live opening and pristine reroll, not from the prior encoded candidate's video.
- Compared against the prior candidate: identical frame count, FPS, and encoded audio-stream MD5. No audio edits were introduced.
- `splice_integrity.py`: all checks passed; no unauthorized visual changes or short old-source islands in the replaced spans.
- `transition_guard.py`: all 10 declared output boundaries passed. Visually inspected the consecutive-frame strips for all 10; approved shots start immediately, without intermediate old graphics.
- Visually inspected all five final-output state sheets, including every settled highlight, complete card edges, all three takeaway banners, and the final frame.
- Geometry validation confirms all targets lie inside their actual v3 assets and active-card/step cameras use the target's vertical and horizontal center.
- Source reroll and live video hashes remain unchanged. Lesson page was not edited in this pass.

Reproduce: `scripts/video/build_document_trap_review.py`, then `scripts/video/qa_document_trap_review.py`.
Exact output boundaries and state geometry: `manifest.json`. Automated comparison: `integrity/`.
