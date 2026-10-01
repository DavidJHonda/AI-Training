# Make Your Move — title revision, October 1, 2026

Final candidate: `Prompts/make-your-move-v9.mp4`, 4:54.17, 8,825 frames at 30 fps, 1280×720.
SHA-256: `b0093c677628a758faf67e5388ffd30f8d95f4e2543ca28a7b572bc20cbd1cfc`.

David requested changing the Four Skills to Build card title from “Create and Solve Problems” to “Create and Solve,” on one line, and updating the video. Completed as a narrow visual repair of the approved v6 build. The canonical skills JPG, its renderer title, lesson HTML text/alt description, and lesson Markdown now match. Body copy and board dimensions (1600×1379) are unchanged.

The video preserves v6's narration, duration, card camera movements, rings, supporting scenes, opening trim, career edits, and closing board. Audio is packet-copied from v6; encoded audio payload SHA-256 `621fc409f325cca2ffcd914c3fbebba92b022e0b4d76daa9b52a920d88f699cc` matches exactly. Narration and the independent Notebook drawing's wording are outside this card-title repair and remain unchanged.

## Method and spans

Built once from v6's retained finished source, `/Users/davidobrien/Developer/AI-Training/video-audit/make-your-move-note-cut/make-your-move-without-note.mp4`, hash `d2aeeba98a33c91657fe75368d46502671af1c47a35e51f2e32cd5b663951d60`, reproducing the existing v6 assembly. The raw generation is unavailable. Audio comes from `/Users/davidobrien/Developer/AI-Training/Prompts/make-your-move-v6.mp4`, hash `3162a39fa46d8fe2bca309a3af0bb905c34db439b111e22791a72a8aeb4949bd`.

Feature matches against the original canonical board recovered its existing scale and translation for all 1,144 board frames, with no gaps inside its three runs. Maximum fit residual was 0.644 pixels. The removed title suffix is filled with the adjacent encoded card background directly in Y/U/V planes; other source samples are unchanged before the final encode. This avoids shifting near-white card colors through an RGB round trip.

Source spans: [[4999, 5180], [5389, 5935], [6220, 6637]].
Output spans: [[4779, 4960], [5169, 5715], [6000, 6417]] (half-open frame intervals).
Output times: 2:39.30–2:45.33; 2:52.30–3:10.50; 3:20.00–3:33.90.

## Verification

- Full decode: 8,825 frames, constant 30 fps, continuous timestamps; exact v6 duration.
- Audio packet hashes identical to v6; no new audio joins.
- Transition guard: all six affected boundaries pass, zero failures.
- Inspected actual encoded full-board views, moving camera samples, focused card view, returning board, and before/at/after boundary sheets. New title stays on one line, no old suffix remains, background blends cleanly, and surrounding body copy/rings remain intact.
- Literal final frame remains the existing closing board.
- No new direct listening or continuous motion-with-sound review; this visual-only revision carries v6's audio byte-for-byte. Broader shipping checks were not repeated.

v7 and v8 are superseded internal attempts: sampled visual review caught near-white background shifts. Use v9 only.

Build: `.video-venv/bin/python scripts/video/build_make_your_move_v9.py`.
QA: `.video-venv/bin/python scripts/video/qa_make_your_move_v9.py`.
Records: `edit-manifest-v9.json`, `tracking.json`, `v9-qa/verification.json`, `v9-qa/transitions/`, and encoded frame/contact sheets in `v9-qa/`.

Candidate provided for review. This task did not install a canonical MP4 or publish a deployment.

## Local shipping — October 1, 2026

Owner approved with “ship it.” Installed v9 at `course-assets/make-your-move/make-your-move.mp4`; installed SHA-256 matches the candidate above. Updated `LESSON_VIDEOS.makeyourmove` to cache key `20261001v9`. The displayed duration remains “5 min” for the 4:54.17 video.

Local commit: `02d6f42f8b805c3b665abcaa4c7cc118a8e9f785`. Only the canonical MP4 and video reference were included; the board and matching title text were already in repository HEAD. Shipped locally; queued for batch deployment. No push or deployment performed. Prior technical/visual verification and the owner’s acceptance support this release; no additional direct listening is claimed.
