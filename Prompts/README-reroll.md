# Re-roll set — staged 2026-07-25

Every `*-video-prompt.txt` here is a video we want to re-roll. Nothing else.
Rejected challenger rolls kept as graft donors live in `donors/`.

## How to roll one

1. In NotebookLM, upload the lesson source: `lessons/<slug>.md`
   (openers use `Opener-Understand.md`, `Opener-Avoid.md`, `Opener-Work.md`).
2. If the prompt's first line lists attached boards, upload those too:
   `lessons/<slug>-*.jpg`, in their numbered order.
3. Make sure `Master Prompt.md` is still a source in the notebook.
4. Paste the prompt text into the video box and generate.

All 26 have kit boards — 98 jpgs total, 2 to 10 per lesson. 39 were captured on
2026-07-25 for the 12 lessons that had none; the specs are in
`scripts/video/board-specs.tsv` so they can be re-cut after a lesson edit.

Board capture gotcha: `capture-board.sh --find` matches the INNERMOST element
containing all the strings, so a single string usually grabs just the heading.
Always pass two or more strings from opposite ends of the board (a title plus a
value from the last row) to force the right ancestor, and eyeball the result —
a heading-only capture lands around 40KB, a real board 80-240KB.

## What changed in this set

Every prompt is generated from `scripts/video/build_prompts.py`, so the shared
rules are identical across all 26. Each carries:

- the fixed motion rule (a board may be held as long as the narration is walking
  it; the old "never hold a static frame longer than four seconds" rule fought r3
  and contradicted the no-marks-on-boards rule)
- the deck-referential ban ("this image shows…"), flagged by five graders as the
  tell for reciting rather than teaching
- the style-prompt-leakage ban (the engine lettering "fineliner", "analog
  texture" etc. into the artwork — found in two videos by two graders)
- per-lesson required narration aimed at that video's actual r3 deducts
- per-lesson bans, including a numbers-free chart ban wherever the lesson has no
  data

All 26 are under the 5,000-character prompt-box cap. `fake-trap` is the longest
at 4,930; trim it further if you edit it.
