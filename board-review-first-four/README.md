# Board Review — First Four Sections

This folder is the review workspace. Proposed boards stay here; once approved, the
canonical copy is placed in `illustrations/` and wired into the live course. Video
changes remain pending until the tracker marks them complete.

## What is here

- `current-contact-sheets/` — 18 contact sheets covering 139 current JPG/PNG boards
  from the first four completed sections.
- `current-selected/` — copies of the current boards selected for redesign.
- `alternatives/` — 16 proposed replacement boards: seven in Start Smarter and three
  in each of the other completed sections.
- `standardized/start-smarter/` — the six approved Start Smarter boards rebuilt with
  the shared canvas, title, content, and takeaway components.
- `pre-standardization/start-smarter/` — recoverable copies of the six boards before
  component normalization.
- `selected-contact-sheets/` — one quick-view sheet per section containing its
  alternatives.
- `RECOMMENDATIONS.md` — lesson-by-lesson review of all 36 completed lessons.
- `VIDEO-FIT.md` — narration windows and drop-in treatment for every alternative.
- `VIDEO-EDIT-TRACKER.md` — approved on-page changes that still need to be carried
  into the shipped videos.
- `PROMPT-SPECS.md` — the reusable image-generation specifications.
- `assets/board-background.png` — the shared seamless lavender background field.
- `video-checks/` — transcripts, scene audits, holds, and frame sheets for the 15
  videos affected by the proposals.

All 16 `*-alternative.jpg` files use the finalized board component: fixed lavender
canvas, title zone, single white body panel, aligned content hierarchy, and gold
takeaway band. Rebuild the original 15 from the preserved pre-spec snapshot with
`scripts/video/normalize_alternative_board_titles.sh`; rebuild the Welcome roadmap
with `scripts/video/build_welcome_course_arc_board.sh`.

Rebuild the approved Start Smarter component-normalized set with
`scripts/video/standardize_start_smarter_boards.sh`.

## Review rule

An alternative should be approved only if it improves comprehension, not merely
decoration. If approved, the same board should become canonical in both experiences:

1. place it in the on-page lesson at the matching teaching beat;
2. place that exact JPG into the existing video's matching narration span;
3. preserve the original narration and duration whenever possible;
4. highlight the active card or stage during multi-point walkthroughs.

Approved on-page changes are listed in `VIDEO-EDIT-TRACKER.md`; shipped videos are not
changed until their tracker row is completed.
