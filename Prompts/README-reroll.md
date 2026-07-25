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

11 of the 26 have kit boards; the other 15 are written board-free on purpose —
`vector-space` (90), `one-more-thing` (85), `context-window` (83) and
`what-you-can-control` (83) all score well with no staged boards, because their
`.md` carries the structured content and the engine renders it.

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
