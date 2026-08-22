# Board Review — First Four Sections

This folder is the review workspace. Proposed boards stay here; once approved, the
canonical copy is placed in `illustrations/` and wired into the live course. Video
changes remain pending until the tracker marks them complete.

## What is here

- `current-contact-sheets/` — 20 contact sheets covering 163 current JPG/PNG boards
  from the first four completed sections.
- `current-selected/` — copies of the current boards selected for redesign.
- `alternatives/` — 66 active review JPG entries representing 58 distinct board
  designs. The extra entries are compatibility aliases or intentional cross-lesson
  reuse, including the shared Embeddings / Vector Space taste-profile board.
- `.retired/` — recoverable superseded boards, including the removed Embeddings
  “Meaning as Numbers” photo treatment and its pre-simplification taste-profile
  board.
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

The alternative boards use the finalized illustration-first component: fixed
lavender canvas, title-only header, one open white body panel, thin dividers, and a
purpose-built graphic for each concept. Subtitle-free one-line titles use the compact
132 px header so more of the frame belongs to the teaching content. Nested cards and gold takeaway bands are
exceptions rather than defaults; sequence numbers appear only when order matters.
The batch readability floor is 44 px for board titles, 28–30 px for essential labels
and explanatory copy, and 24 px only for genuinely secondary text. When the standard
564 px body would force smaller type, use the 688 px dense body and omit the takeaway.
Rebuild the original set from the preserved pre-spec snapshot with
`scripts/video/normalize_alternative_board_titles.sh`; rebuild the Welcome roadmap
with `scripts/video/build_welcome_course_arc_board.sh`.

Rebuild the approved Start Smarter component-normalized set with
`scripts/video/standardize_start_smarter_boards.sh`.

Rebuild the 2026-08-21 illustration-first refresh of the recent Avoid Traps and
Embrace the Future boards with
`scripts/video/render_editorial_board_refresh.py`. Run this after older batch board
renderers; it owns the canonical outputs listed in its `save_all` calls.

After running any legacy board renderer, run
`scripts/video/compact_single_line_board_headers.py --apply`. This idempotent final
pass gives every detected one-line board title the 132 px compact header while
leaving wrapped titles and sequence-marker headers unchanged.

## Review rule

An alternative should be approved only if it improves comprehension, not merely
decoration. If approved, the same board should become canonical in both experiences:

1. place it in the on-page lesson at the matching teaching beat;
2. place that exact JPG into the existing video's matching narration span;
3. preserve the original narration and duration whenever possible;
4. highlight the active card or stage during multi-point walkthroughs.

Approved on-page changes are listed in `VIDEO-EDIT-TRACKER.md`; shipped videos are not
changed until their tracker row is completed.
