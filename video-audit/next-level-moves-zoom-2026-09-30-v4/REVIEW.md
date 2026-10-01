# Next Level Moves v4 — two-board zoom and pan

Scope: the user's request to add zoom and pan to the boards arriving at 0:55 and 4:12. This explicitly overrides the earlier full-view-only convention for these two AI-chat boards. All v3 supporting inserts are retained.

Candidate: `Prompts/next-level-moves-v4.mp4`. Runtime remains 5:06.867 at 1280×720, 30 fps, 9,206 frames. Not installed or published.

## Camera treatment

| Board | Span | Treatment |
|---|---|---|
| Starting a Summer Business | 0:55.033–1:35.633 | Establish the complete unmarked board for 2.07 seconds; zoom into the first complete student bubble, then pan between student and AI turns. Retain tutoring cutaway at 1:10–1:17 and return to the active student bubble. Pull back to the complete board for the takeaway. |
| From Idea to Business Plan | 4:11.467–4:56.067 | Establish the complete unmarked board for 2.57 seconds; zoom into the early request, pan to the early answer and then the later request and answer. Retain lawn-planning cutaway at 4:27–4:38 and return to the active later request before AI's pressure-test. Pull back for the takeaway. |

Both boards are redrawn directly from the current canonical JPGs. One uniform 1120-source-pixel camera width is used across each board's conversation turns. Every active speech bubble, speaker label and complete outline fits inside the settled view. Surrounding inactive material can run outside the frame during the close views; active bubbles are never cropped internally. The existing whole-board title remains visible at the beginning and takeaway.

The first dive lasts 0.8 seconds. Pans begin 0.8 seconds before the next turn and arrive at its existing ring cue. The outgoing ring is hidden during the pan so a clipped outline does not cross the frame. The new outline appears at the next turn's cue. The first dive retains its complete outline throughout. The takeaway pullback lasts one second. Outlines are drawn after camera motion at a constant 4 px in the delivered 720p frame.

`camera-plan.json` and the build manifest retain coordinates and exact cue frames. `preview/sb-sheet.jpg` and `preview/it-sheet.jpg` show the framing plan.

## The idea around 1:59

No narration was removed in this candidate. The user's question about whether the idea is needed was answered with an editorial recommendation and a scope question; it was not treated as authorization to remove an unspecified teaching beat.

Recommendation: remove only “and check whether you understand it” (approximately 1:57.32–1:58.92), which is redundant with the following instruction. Keep “Then explain the idea back in your own words and ask what you missed” (approximately 1:59.40–2:02.90), because it gives students a practical way to check their learning. Removing that whole idea would also remove a current lesson teaching point. Those are distinct choices; the audio remains intact pending the user's selection.

## Preservation and limitations

The v4 build reuses the same verified v2 baseline and original v3 assets/rendering code, avoiding another encode of the v3 candidate. Only the two board camera treatments differ creatively from v3. Narration, pauses, other boards, profit animation, generated scene inserts and closing motion are preserved. Audio is copied without re-encoding.

Build: `scripts/video/build_next_level_moves_v4.py`; camera renderer: `scripts/video/next_level_moves_zoom.py`; verification: `scripts/video/qa_next_level_moves_v4.py`.

Full-file listening and real-time audiovisual review remain unperformed. This is a review candidate, not a shipping sign-off. No lesson text, canonical JPG, course video or index reference was changed.

## Encoded verification

- All 9,206 frames decoded at the expected duration.
- Audio packet and decoded-PCM hashes match the original; no audio change.
- Compared 7,190 preserved frames with v3, including the retained cutaways. Mean sampled YUV error 0.0025/255; maximum frame mean 0.5151/255. No mismatches.
- Checked 103 changed-board frames against direct canonical-asset rendering, including settled states, pan midpoints and edit boundaries. No mismatch.
- Inspected all six encoded-state contact sheets: complete active bubbles and outlines, correct returns from cutaways, full-board takeaways, and canonical final frame.
- Candidate SHA-256: `e11bc8d471d161b922a39a7302ade3d7d9ac2be20f6cfcbc05cb90cdd9d7d4bb`.
- Shared transition guard passed all 12 declared boundaries, with zero failures. Inspected before/at/after strips for both board openings/exits and the retained cutaways' now-zoomed entrances/returns. No stale frames at the edited seams.

## Shipped locally — October 1, 2026

User approved v4 with “ship it” after the build report disclosed unchanged narration and the review limitations. Installed v4 unchanged; no learning-check narration cut.

Local commit: `b487d5c548698d5afb12166060df817970698d2b`. Installed SHA-256: `e11bc8d471d161b922a39a7302ade3d7d9ac2be20f6cfcbc05cb90cdd9d7d4bb`. Cache key: `20261001ship1`; displayed runtime remains 5 min. The commit contains only the canonical MP4, its manifest hash/size, and its index.html cache key. Unrelated edits in the shared index.html remain uncommitted.

Scoped installation checks passed. Broader `verify-course-assets.py` reported unrelated pre-existing In Your Hands retired filenames and malformed Training-prefixed Where’s the Line references; these were not changed. The prior frame/audio/transition checks remain valid because the installed bytes match the reviewed candidate exactly. Full-file listening was not newly performed or claimed.

Status: shipped locally; queued for batch deployment. No push or deployment performed.
