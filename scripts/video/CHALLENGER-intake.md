# Challenger intake — read fully before scoring

You are evaluating a NEW roll of a lesson video that already has a sitting
version in the catalog. Your job has two parts: grade this roll on its own
merits, and find what could be harvested from it.

## Part 1 — grade it

Follow `scripts/video/GRADER-r4.md`
exactly, including the two false-positive traps and the cite-or-don't-deduct
discipline. Produce the standard output block.

**Anti-anchoring, same as always:** do NOT look up the sitting version's score.
Do not read the tracker sheet, memory files, git log, or `videos/<slug>.mp4`.
Grade what is in front of you. The comparison is done centrally.

## Part 2 — did it hit the spec?

This roll was generated from a prompt written to fix specific defects. Read
`Prompts/<slug>-video-prompt.txt` and check its "Required narration" rule
line by line against `transcript.txt`.

Report each requirement as MET or MISSED with a timestamp or the quote that
settles it. This is the single most decision-relevant thing you produce — the
whole point of the re-roll was those lines.

Also check, from the same prompt:
- did it end on the close board as the literal final frame?
- did each qualifying multi-point board use the exact current lesson board,
  held fully visible with narration-synced item highlights?
- did it letter style words into the artwork ("fineliner", "analog texture")?

## Part 3 — harvest

Whatever the verdict, this roll may contain spans worth grafting into the
sitting version. List every span you would nominate, with:
- `start–end` timestamps (from `scenes.txt`, so they land on real scene cuts)
- what it contains
- whether it is AUDIO-worthy, VISUAL-worthy, or BOTH
- one line on why it beats what a typical roll does here

Be selective. A nomination that isn't clearly excellent wastes an edit.

## Output — exactly this, nothing before or after

```
SLUG: <slug>
RUNTIME: <m:ss>
TEACHING_COVERAGE: <n>/20 — <evidence>
TEACHING_LESSON_MATERIAL: <n>/15 — <evidence>
TEACHING_TEACHES_VS_RECITES: <n>/15 — <evidence>
TEACHING_BOARD_CONTENT: <n>/10 — <evidence>
CLEANLINESS: <n>/20 — <evidence>
PACING: <n>/20 — <evidence>
SOURCE_QA: PASS|FAIL — <lesson-line evidence>
GATE_ACCURACY: PASS|FAIL — <timestamp or quote>
GATE_SUBSTITUTE: PASS|FAIL — <could a student watch instead of reading and lose no essential understanding?>
GATE_SPINE: PASS|FAIL — <evidence>
GATE_RESTRAINT: PASS|FAIL — <evidence>
GATE_STOCK: PASS|FAIL — <evidence>
GATE_ENDING: PASS|FAIL — <evidence>
GATE_SYNC: PASS|FAIL — <evidence>
GATE_BOARD_WALK: PASS|FAIL|N/A — <evidence>
SPEC:
  <requirement> — MET|MISSED — <timestamp or quote>
  ...
  canonical-board-walk: PASS|FAIL|N/A — <evidence>
  style-leakage: YES|NO — <evidence>
HARVEST:
  <m:ss>–<m:ss> — AUDIO|VISUAL|BOTH — <what it is, and why it's worth taking>
  ...  (or "none worth taking")
NOTES: <at most two lines, or "none">
```

Your final message is the return value and must be that block alone.
