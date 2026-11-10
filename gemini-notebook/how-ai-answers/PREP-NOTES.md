# How AI Answers — current video preparation

The continuous narration clarity draft is in [NARRATION-DRAFT.md](NARRATION-DRAFT.md),
with its shot and pause plan in [NARRATION-VISUAL-MAP.md](NARRATION-VISUAL-MAP.md).
These are review materials, separate from the current upload source. They make
the transitions audible and explain the context at the question mark, You, and
him stages. No new recording or video has been generated from the draft.

Updated 2026-11-10 after the approved lesson review. These notes and the active
registry supersede the historical board lists in the section kit.

## Teaching progression

Move from the question's contextualized vectors to the first prediction, then show
how each added token changes the context used to predict what comes next.

1. Establish the question plus the answer so far as the context. Keep the explicit
   simplification that words are shown as single tokens.
2. Briefly recap the four preparation steps on Before the Answer Begins. Its old
   prediction banner is removed; do not recreate or highlight it.
3. Explain the question mark's updated vector, then compare the dog and dinner
   questions on Same Token, Different Context. Keep “reflects the context”; avoid
   a perfect compressed copy, a unique encoding of the whole question, a funnel,
   or the discarded essay/“end” analogy.
4. Under WHY IS THIS IMPORTANT?, explain the first prediction and the handoff to
   You. Once selected, You is the last token. The last token’s updated vector
   reflects both your question and everything AI has written so far. Teach the
   full paragraph here and only the shorter
   reminder during the demonstration.
5. Cover the complete demonstration in the video. The on-page version stays inside
   Read the lesson because the video provides this teaching too. Introduce the
   initial choices, select You, add could/name/him one at a time, show the name
   probabilities, then select Spot. Add a period and the end-of-answer token.
6. End with the existing two closing lines, including inference.

## Uploads and reproducibility

The active bundle contains the narration Markdown and seven JPGs: two current
lesson boards, four stills from the shared demonstration renderer, and the close.
The registry and generated README give the exact filenames. No face variants are
needed. The stacked phone layouts are page adaptations; use the original desktop
boards in the video.

Refresh the four demonstration stills with:

```sh
node scripts/video/render_how_ai_answers_prep.cjs
python3 scripts/video/sync_gemini_notebook.py --lesson how-ai-answers
python3 scripts/video/sync_gemini_notebook.py --lesson how-ai-answers --check
```

The renderer requires Playwright in Node's module search path and Chrome. It
regenerates the demonstration preview from index.html and uses an isolated local
HTTP server. Upload stills are 1280×720 with the shared scene enlarged for reading;
no controls or instructional UI are burned into the stills. Their selection borders
and new-token colors are part of the lesson state, not added narration highlights.

The old token-by-token and building-an-answer JPGs are excluded from the active
bundle. Do not use them to restore Rank/Pick/Add/Repeat or old final-token wording.
Keep each required verbatim sentence on its own source line. The first and name
prediction snapshots contain the complete probability distributions; do not repeat
all the percentages when the selected-token frame follows.

## Editing and narration review

- Before a selection, the chart heading is Possible next tokens. After a selection,
  it is AI selected You or AI selected Spot. The retained choices are the previous
  distribution, not another prediction. Keep the chosen row visibly selected.
- As choices are spoken, emphasize the corresponding whole row, including its
  percentage, using the shared editing specification. Never highlight an unspoken
  banner. Semantic selection borders remain distinct from spoken-choice emphasis.
- Leave a short natural pause before the demonstration repeats the dog-name
  question. Determine the actual gap from the new narration; do not reuse the
  earlier candidate's 1:08 timestamp or add silence mechanically.
- Animate could, name, and him separately. When the reply reaches You could name
  him, show the name probabilities before selecting and adding Spot.
- After the period and end-of-answer token, remove the probability panel. Do not
  restore the redundant End of answer badge or final empty white box.
- No “Illustrative numbers and probabilities” banner, added quiz, narration of
  matching or discussion activities, or early teaching of sampling/temperature.
- Verify the transcript contains the updated context explanation and the handoff;
  correct visuals alone cannot replace missing narration. Retain the qualification
  that another run could select a different name, without promising that it will.

## Status

Preparation only. No new narration or video has been generated, installed, or
published by this update. The installed course asset remains the October v12 video;
v16 is a separate November review candidate and predates the settled explanation.
Assess any future roll against this source and the current prompt, not historical
required-line lists.

## Approved narration clarification — 2026-11-10

Replace “Its updated vector reflects your question and the reply so far.” with:

“The last token’s updated vector reflects both your question and everything AI has written so far.”

This wording is now in the lesson and the required verbatim narration prompt.
The existing v20 review candidate still has the earlier audio at approximately
1:28–1:32. None of the three reviewed rolls contains the new sentence verbatim;
a new recording is needed to carry this exact wording into the video. Preserve
v20’s approved visual treatment when replacing that sentence.

## Explicit context at each stage

The Same Token board explains that each question mark’s updated vector reflects
the context of its whole question. At You, name the question plus the one-word
answer. At You could name him, identify him as the last token and name the
question plus all four answer words as the context. Use the current source
wording without em dashes. These revisions require fresh narration; v20 is unchanged.

## Familiar continuation example

Under WHY IS THIS IMPORTANT?, the lesson now compares “Peanut butter and”
with “Salt and” to connect learned patterns, contextualized vectors, and likely
continuations. It follows the first-token explanation and precedes the transition
to a longer answer. The upload source, prompt, and continuous narration draft
include it. Existing video recordings do not contain this new passage.
