# Make Your Move 2 — shipped

Published file: `videos/make-your-move.mp4`

Approved candidate `Prompts/make-your-move-2-patched.mp4` was moved to the published path without re-encoding on 2026-09-05. The lesson's video entry now points to it instead of showing Coming Soon. Published SHA-256 matches the reviewed file below.

Runtime: **4:47.30** (8,619 decoded frames at 30 fps).
SHA-256: `8e27e4aa39a314724ff6fe02ee5135dc172a5feec6b9bc95445b8ee755114a63`

## Approved treatment

- Exact current career-board assets, including the Nate and Luke illustrations.
- Full-board orientation once per career group, then complete active-card views.
- Restore the established full-board → zoom → pan treatment. Keep complete board pixels under the camera, not isolated-card cutouts. Eleven one-second eased moves cover the first career in each group, designer-to-entrepreneur, and the skills/action cards.
- Return from native cutaways directly to the appropriate settled card, without repeating the full-board introduction.
- Add the approved Nate-and-Luke note illustration for the complete original shot at 0:29.23–0:37.30. Hold the entire note still and readable. Replace the corresponding visible kicker and body paragraph in the lesson; preserve the text in alt text and the Markdown export source.
- Full-card horizontal highlight rails; vertical bounds measured separately for each text block with 18 source pixels above and below its ink.
- Purple, blue, and teal accents inherited from each career card.
- Five native-graphic cutaways; the lawyer stays on the board.
- Preserve source 3:04–3:15 narration and graphics as a breather.
- Remove only the approved broad summary at source 2:06.30–2:18.80 and the redundant closing introductions.
- Replace skills and action boards with current assets and full-card accent highlights.
- Exact course closing board; 48-frame hold, 150-frame push to 1.2x, settled ending. No Notebook logo.

## Finished-output review map

| Output time | Picture |
|---|---|
| 0:29.23–0:37.30 | A Note from Nate and Luke |
| 1:15.17–1:29.73 | Doctor board |
| 1:29.73–1:33.57 | Original doctor–patient graphic |
| 1:33.57–1:43.03 | Teacher board |
| 1:43.03–1:47.20 | Original classroom graphic |
| 1:47.20–1:59.20 | Lawyer board |
| 1:59.20–2:06.30 | Original hands-on/creative transition |
| 2:06.30–2:18.23 | Electrician board |
| 2:18.23–2:23.57 | Original electrician graphic |
| 2:23.57–2:26.80 | Original design-variations graphic |
| 2:26.80–2:37.70 | Designer board |
| 2:37.70–2:48.57 | Entrepreneur board |
| 2:48.57–2:52.07 | Original founder/team graphic |
| 2:52.07–3:02.87 | Preserved source 3:04–3:15 breather |
| 3:13.10–3:34.17 | Four Skills to Build |
| 3:55.37–4:39.80 | Moves to Make |
| 4:39.80–4:47.30 | Standard close |

## Verification

- Source unchanged; its hash and all six asset hashes are recorded in `edit-manifest.json`.
- Encoded picture once from the pristine source; no stacked MP4 repairs.
- 8,619 / 8,619 decoded output frames verified.
- Current hard-transition guard: **28 / 28 pass**, zero short intermediate visual islands detected.
- All 28 current every-frame boundary strips visually inspected (`qa-current/transitions-current-*`). No discarded graphic visible at a restored-picture boundary.
- The 11 deliberate camera moves are reviewed separately: the generic cut detector flags their continuous frame differences. Review sheets cover the boundary frame sequence and samples throughout each complete move (`qa-current/motion-review-*`, `qa-current/complete-moves-*`). These are intentional pans/zooms on the same source board, not discarded-graphic flashes. Global detector sensitivity was not reduced.
- Every highlight state inspected; the shorter electrician responsibility block receives its own shorter ring.
- Prior output transcript verifies intact transition into “Think about an electrician,” retained responsibility breather, and both closing lines. This visual-only revision retains exactly the same audio assembly, source cuts, and runtime.
- Audio cut shoulders measured on the final encoded candidate: -62.54, -71.19, and -70.15 dB RMS; peak adjacent-sample changes below 0.00045. Cuts fall in measured quiet shoulders, not inside words. This is a signal/transcript check, not a claim of human listening review.
- Lesson HTML and lesson Markdown now contain the approved personal note. Inline JavaScript syntax verified. Published video, source upload, and existing teaching-board assets unchanged.

Illustration: `illustrations/make-your-move-note-v1.png`. Generated with the built-in image-generation tool; exact generation prompt and reference roles are recorded in `illustrations/make-your-move-note-v1.prompt.md`.

Previous `transitions/` and `qa-sheets/` reports describe the earlier static-card candidate, not this revision. Use `transitions-current/`, `motion-review/`, and `qa-current/` for this output.

Rebuild: first restore `make-your-move-2.mp4` to `Prompts/`, then run `.video-venv/bin/python scripts/video/build_make_your_move_2_review.py`. The build still produces a review candidate, never overwrites the published file.

## Cleanup

Two unused uploads were moved to `/Users/davidobrien/.Trash/make-your-move-unused-2026-09-05/` and remain recoverable:

- `make-your-move.mp4` — SHA-256 `00891989224ead74d1312c57412e8d98397b4d9eb0c6a2e1a6ae10d7b7ce4ebe`
- `make-your-move-2.mp4` — SHA-256 `332ed152cbc3bf783135367021d7942b5c74f23cceafd5bb23f736615f8a5366`

No Make Your Move MP4 candidates remain in Prompts. Lesson JPGs, Markdown, PDF, prompt, illustration, and editing/audit records were retained. No other lessons' candidates were touched.

Status: **Shipped with owner approval on 2026-09-05.**
