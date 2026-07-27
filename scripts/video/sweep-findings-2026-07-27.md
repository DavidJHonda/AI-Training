# Full contact-sheet sweep — 2026-07-27
Method: frames.py --sheet (480x270 every 4s). Findings are LEADS until confirmed
at full resolution. Detector result (validated, separate pass):
  NotebookLM watermark: ai-is-math 66% of runtime; why-learn-ai ~2:05;
  one-more-thing ~0:33; all other 34 videos clean (max score <=0.205 vs 1.000).

## Per-video visual notes

## HEADLINE: NotebookLM watermark on 31 of 37 videos (CORRECTED)

First scan was WRONG. Its template came from a light-mark-on-dark-chalkboard frame
and matched a high-passed ROI with TM_CCOEFF_NORMED, which is sign-sensitive; the
mark is dark-on-light on pale scenes, so the signal inverted and scored ~0. It
reported art-of-prompting 0.019 while the mark is plainly visible at full res.
Fixed by matching on GRADIENT MAGNITUDE (polarity-free). Revalidated:
  ai-is-math dark bg 0.992 | art-of-prompting pale bg 0.994 | layers f900 0.000

MARKED (31): evaluate-the-results 98%, how-ai-answers 98%, training 97%,
what-you-can-control 96%, opener-work 93%, document-trap 91%, opener-avoid 91%,
transformers-quiz 90%, one-more-thing 90%, art-of-prompting 87%, which-app 85%,
why-learn-ai 84%, questions-matter 84%, does-ai-think 84%, embeddings 83%,
tokens 83%, welcome 83%, learn-with-ai 83%, training-bias 82%,
critical-thinking 79%, what-is-ai 76%, ai-is-math 75%, opener-understand 73%,
flattery-trap 73%, vector-space 70%, context-window 63%, engagement-trap 60%,
where-ai-works-best 56%, mind-trap 54%, support-trap 39%, transformer 11%.

CLEAN (6), each confirmed by eye at its max-scoring frame:
  ai-is-different, does-school-matter, fake-trap, hallucination,
  how-an-llm-works, layers

PATTERN: the 6 clean ones are the most recent rolls (fake-trap 7/24, the rest
re-rolled 7/26). The engine appears to have stopped burning the mark in around
late July. transformer at 11% from 0:24 is consistent with a composite of an
older marked roll and a newer clean one.

FIX: ffmpeg `delogo` at the fixed box (~x1130-1275, y680-715). Test one span first.

## ENDINGS: all clear
Last frame of all 37 dumped to one montage. 36/36 teaching videos end on their
close board, all legible. transformers-quiz ends on a CPU render, but it is the
TRY IT quiz video, not a teaching lesson - no close board expected. No GATE_ENDING
failures anywhere.

## Videos read clean (visual sheets, apart from the watermark)
ai-is-math, art-of-prompting, context-window, critical-thinking, document-trap,
does-ai-think, embeddings, engagement-trap, evaluate-the-results, fake-trap

Notes on things deliberately NOT flagged:
- context-window 0:28 and engagement-trap 2:08: photoreal composites of Luke/Nate
  in Anthropic "Claude" / Google hoodies. These are David's own commissioned
  illustrations, same family as the does-school-matter Google-stage one. Deliberate.
- ai-is-math 2:28-2:36 "wrong" chart numbers (24/71, 26/74) are mid-animation
  states of counters resting on 50/50. The known false-positive class.
- engagement-trap 3:04-3:16 revenue chart carries no invented data - it resolves
  to a sticky note reading "Objective: Make Line Go Up!". Wordless background,
  which the narrowed rule 5 allows.

## Leads still to confirm at full res
- critical-thinking 0:44-0:48 handwritten red annotations (pseudo-text density)
- document-trap 0:28 rulebook spread (dense pseudo-text; profanity check)
- art-of-prompting 3:24 crate lettering
- flattery-trap 0:08 "THOUGHTS" heading may render as "THOUGIITS"

## CONFIRMED DEFECT: style-prompt leakage (rule 7), 2 instances, both verified at full res
- how-an-llm-works 0:24-0:28 -- peanut-butter jar annotated "heavy felt-tip
  fineliner lines", "heavy cardstock shadow washer", "Alcohol... peanut standard",
  "tinged card". The artist's own material notes lettered INTO the artwork.
  NOTE: this is a video I repaired today; the span was never inspected.
- flattery-trap 2:12-2:16 -- gag-gift display annotated "paper cutut" (sic),
  "fineliner ink glass", "alcohol-marker wash", arrows pointing at the drawing.
This is the SAME class named in the training-bias kit ("FINELINER WITH
ALCOHOL-MARKER", "ANALOG TEXTURE AND ANNOTATINES"). So it is not a one-off; it
recurs across rolls and is worth a catalogue-wide named ban, not per-video patching.

## Lead NOT confirmed as a defect
- hallucination 2:56 "Hallucinations Drop But Persist" chart plots a Frequency
  axis 0-125 over Early Models/Pre-RAG/RAG Intro/Refinement/Today. Invented
  quantitative data. Flagging as a JUDGEMENT CALL for David, not a clear
  violation: how-ai-answers solves the same problem honestly by printing "The
  exact numbers are illustrative" on its own probability board.

## Videos read clean so far (visual, apart from watermark)
ai-is-math, art-of-prompting, context-window, critical-thinking, document-trap,
does-ai-think, embeddings, engagement-trap, evaluate-the-results, fake-trap,
hallucination (bar the chart call), how-ai-answers, how-an-llm-works (bar 0:26),
flattery-trap (bar 2:12), + ai-is-different & does-school-matter (repaired today)

## STYLE LEAKAGE -- 3rd and worst instance: training-bias (still shipped)
0:20  "hand-drawn video linings to quick thumbs", "draw logic activator"
2:24-2:32  "alcohol-marker fineliner washes", "felt-tip fineliner workstation inks",
           "realistic alcohol-marker drop shows"
3:28  "FINELINER WITH ALCOHOL-MARKER AND WORKS", "ANALOG TEXTURE & ANNOTATIONS",
      "FELT-TIP FILE-TIPS FINELINER", "DUSCLY ROADS IN CARDSTOCK"
This matches the defect already NAMED in memory for this video at exactly 0:20,
2:24 and 3:28. It was known, a hardened prompt was written for it, and the fix
never shipped -- the roll on disk is still the defective one.

So: 3 of 22 videos read carry style leakage (how-an-llm-works, flattery-trap,
training-bias). It is systemic, not incidental.

## COVERAGE (honest)
CATALOGUE-WIDE, COMPLETE (all 37 videos):
  - NotebookLM watermark scan (validated detector, polarity-invariant)
  - Endings check (last frame of every video)

FULL SHEET READ (18): ai-is-math, art-of-prompting, context-window,
critical-thinking, document-trap, does-ai-think, embeddings, engagement-trap,
evaluate-the-results, fake-trap, flattery-trap, hallucination, how-ai-answers,
how-an-llm-works (4/6), layers, learn-with-ai (5/6), ai-is-different,
does-school-matter

PARTIAL (6): training-bias 3/5 (defect found), mind-trap 2/5, support-trap 1/6,
training 1/7, one-more-thing 1/6, which-app 1/7 -- all clean in what was read

NOT READ (13): opener-avoid, opener-understand, opener-work, questions-matter,
tokens, transformer, transformers-quiz, vector-space, welcome, what-is-ai,
what-you-can-control, where-ai-works-best, why-learn-ai

Roughly 110 of 192 sheets read. Sheets remain on disk at scratchpad/sweep/ so
the rest can be picked up without regenerating anything.
