# Video grader changelog

The current grading authority is `GRADER-r5.md`. Historical grader files remain
unchanged so prior decisions can be reconstructed.

## r5, 2026-08-22

r5 consolidates the accumulated r4 rules into one workflow-ordered document.
The numeric dimensions and their weights remain unchanged.

Intentional scoring changes:

- `TEACHING_LESSON_MATERIAL` no longer penalizes accurate outside material merely
  because it is absent from the lesson. Brief refreshers and stronger explanations
  may earn full credit when they improve clarity or flow. A stronger explanation
  becomes a candidate on-page lesson edit.
- `PACING` now explicitly prioritizes complete teaching over concision. Useful
  explanation is not padding. Deduct for dead time, needless repetition, confusing
  detours, or structure that buries the central lesson. Slightly overlong complete
  material is preferred because it can be cut; missing narration usually requires
  a re-roll.

Structural changes:

- `GRADER-r5.md` is the single grading authority.
- `videos/video-rubric.csv` is a synchronized tracker summary.
- Current-board fidelity is clearly separated from Board Content scoring: a redraw
  may teach the content and earn numeric credit while still failing the ship gate.
- The compact-board and dense-board treatments are stated together.
- Gemini Notebook highlighting is explicitly prohibited.
- Standard closing size, endpoint, and hold behavior are included in one close gate.
- Edit Integrity now blocks one-frame visual remnants, truncated speech, audio blips,
  and abrupt noise-floor dropouts. Breath cleanup preserves duration and uses keep,
  attenuation, or matched-room-tone replacement rather than ripple deletion.
- Historical explanations were removed from the live grader and retained here or
  in Git history.

## r4, 2026-08-14 through 2026-08-21

r4 retained the six r3 numeric dimensions and added non-compensable Source QA,
Accuracy, Substitute, Spine, canonical board-walk, Notebook-highlight, and standard
close gates. Several rules were appended after the output schema as they were
discovered, which eventually made precedence unclear and prompted the r5 consolidation.

## r3

r3 removed animation as a scored dimension, retained its legitimate dead-time
concern under Pacing, split Teaching into four reported sub-scores, and treated
visual style as ungraded.
