# Evaluate the Results v8 (2026-09-27)

Candidate: `Prompts/evaluate-the-results-v8.mp4` (4:15.37, 7661 frames). SHIPPED 2026-09-28 on David's "ship it" (cache key 20260928ship2, pill 3 -> 4 min). Build script: `scripts/video/build_evaluate_the_results_v8.py`.
Scope: v7 plus the new opening board "How to Evaluate an AI Answer", plus the four stage boards retrofitted to their 2026-09-27 layouts. David said "Build it" on 9/27 after the recommendation in `../evaluate-the-results-process-rolls-2026-09-27/process-board-comparison.csv`.

## What changed
- **New span, output 0:34.10 to 1:20.10 (46.0 s).** Roll 4 audio from 41.80 to 87.80 s, running from "This flowchart maps out the entire evaluation process." to "...evaluate the revised version." It sits between "And is it good enough for what I need?" and "Start with the quick pass."
  - Both cut points fall in roll 4 silences.
  - Loudness: roll 4 measures -20.3 LUFS against roll 3's -20.2 and -19.8, so the span gets +0.3 dB.
- **Process board treatment.** The camera moves stage by stage and there are no cutaways, because the prompt asked for one uninterrupted walkthrough. Rings follow roll 4's word onsets.

  | Cue | Camera | Ring |
  |---|---|---|
  | "This flowchart…" | full view (4.2 s) | none |
  | "You start…quick pass" | Quick Pass + diamond | Quick Pass |
  | "you reach the diamond" | same | diamond |
  | "If you choose the yes path" | top route (diamond tip, Dig Deeper, Your Move, No line) | Dig Deeper |
  | "you take the no path" | same | "No" label (inside the line's gap) |
  | "your move" | same | Your Move |
  | "Use it, fix it, or walk away" | Your Move + pills | all three pills |
  | "Notice the return arrow" | full view | "Check the fix" (inside the line's gap) |
  | "If you choose to fix" | full view | Fix It |
  | "back to the quick pass" | full view | Quick Pass |

  - The longest stretch without camera motion is about 16 s.
  - The windows were chosen so no text is sliced. The return loop spans the whole board, so its beats use the full view.
- **Stage boards.** Rects were re-measured on the new JPGs:
  - Quick Pass, Dig Deeper? and Your Move: compact.
  - Dig Deeper: dense, and now laid out 3 + 2 on a 1600x1032 board.
  - Every roll 3 onset, cut, cutaway, pause, and the close are unchanged from v7.

## Verified on the encoded file
- Frame count is 7661, matching the plan.
- transition_guard passed 32/32 (strips in `transition-guard/`).
- Transcript: v7's words are unchanged, with the roll 4 walkthrough inserted at 0:34.8.
  - Whisper also "heard" an ad line at 4:13.7. That span is the settled close hold, and its RMS is identical to v7's room tone, so it's a Whisper hallucination, not audio.
- Ring states on all five boards were checked on the leg sheets (`states-*.jpg`, `preview/process-states.jpg`, `preview/p2.jpg`). Each ring lands on the right card or shape, and no card is clipped.
- Corner mark: 0 frames declined. Protected hashes unchanged.

## Not done / needs David
- **Ear test** of the two new joins:
  - 0:34.1: roll 3 "…what I need?" into roll 4 "This flowchart…"
  - 1:20.1: roll 4 "…revised version." into roll 3 "Start with the quick pass."
  - The voice match is by pitch estimate only.
- Earlier ear-test items from v7 still stand: "riding"/"writing" at about 2:31, the roll 2 close line, and the reused "Read. Understand. Validate."
- ring_stroke.py was not run.
- Known narration weakness: the Yes path is spoken as "before moving forward" and never names Your Move. The top-route camera shows the arrow into Your Move.
- Shipped without the ear test above; the joins are still unheard.
