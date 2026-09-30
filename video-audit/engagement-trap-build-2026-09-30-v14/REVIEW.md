# Engagement Trap v14 — first-board camera revision

Built September 30, 2026 for David's request: “The board at :31. We should do the zoom and pan for this board.” This is a narrow visual repair of v13.

Candidate: `Prompts/engagement-trap-v14.mp4`, 1280×720, 30 fps, 7,832 frames, 4:21.07. Shipped locally on September 30, 2026; queued for batch deployment.

| Board | Highlight sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| One Answer. Two Endings. | Question bubble → AI bubble → YOU STOP → THE TRAP → takeaway | Full unmarked opening for 3.2 seconds; one-second eased dive and pans; complete active bubbles/cards; full-view takeaway | 30.27–48.50, 58.90–70.70, 76.97–86.47; existing follow-up animation and timer preserved | Explicit owner request for zoom and pan overrides the general compact AI-chat treatment for this board |

The camera dives at 33.47, pans to the answer at 38.17, returns from the cutaway on YOU STOP at 58.90, and pans to THE TRAP at 65.23. After the timer, it pulls back from THE TRAP at 76.97 and reaches full view at 77.97. Rings on the answer, trap, and takeaway appear after the camera lands, avoiding clipped outlines during movement. All outlines are drawn after cropping at the fixed four-pixel output width. Both lower cards retain their title, body, and bottom section.

## Verification

- Fully decoded 7,832 frames, 30 fps, matching v13's runtime and dimensions.
- Copied v13's AAC stream without re-encoding; audio packet SHA-256 matches exactly: `e9c6ebbb714c87774aff89fe740b4e25458ffeb8161dc54f411d082afde457f0`.
- Compared every one of the 6,646 unaffected decoded frames against v13 at 320×180. Maximum mean absolute channel difference: 0.0157/255, consistent with encoding differences. The builder reuses the same v12 source and visual assembly outside the three changed board spans.
- Transition guard passed 17/17 declared boundaries. Manually inspected all six strips bordering the changed board, all settled highlight states in the contact sheet, and full-size question, answer, trap, and takeaway frames. Other boundaries retain their prior visual treatment; their older manual review is recorded with v13.
- Every highlighted frame passed complete-ring bounds assertions. Canonical board, live video, and protected lesson files retain their hashes.
- Candidate SHA-256: `88f2f67a4958bd2aa7dc135307f8c4150fc4dd94518fb6cc6c1a50932949e42e`.

## Provenance and limits

Builder: `scripts/video/build_engagement_trap_v14.py`; QA: `scripts/video/qa_engagement_trap_v14.py`. Geometry, timing, and source hashes are in `edit-manifest.json`; decoded frames, contact sheet, and transition strips accompany this review.

The original raw rolls remain absent. Video was assembled once from a verified snapshot of the same finished source used for v12, with the exact canonical comparison JPG for the new camera treatment. It was not re-encoded from v13's video. Audio was copied directly from v13.

No continuous playback or listening was performed. v13's prior listening-review needs and pre-existing spoken slope-definition gap remain; see its review. This candidate is ready for owner review, not a whole-file ship-ready sign-off.

## Local shipping — September 30, 2026

David approved this exact candidate with “ship it” after the recorded review. Installed v14 at the canonical video path, verified its SHA-256 against the candidate, and updated only Engagement Trap’s lesson cache key to `20260930ship14`. The displayed runtime remains `4 min` for the 4:21.07 video.

Local commit: `3a23dfa0e87374d510400bc5563f2f9a1ea2fef1` (`Ship Engagement Trap v14 locally`). The commit contains only the video and its one-line lesson reference update. Audit/build records remain local. No push or deployment was performed; **shipped locally, queued for batch deployment**.

Shipping follows the owner’s explicit approval of the reviewed candidate. The earlier listening and narration-review limitations are retained; this action does not claim new end-to-end listening or a formal KEEP assessment.

After the commit, scoped render-scratch cleanup removed 10 untracked WAV intermediates (0.19 GB) from Engagement Trap build folders only. Kept review evidence, candidates, and the verified source snapshot needed to reproduce the visual assembly.
