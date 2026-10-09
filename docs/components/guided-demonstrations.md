# Guided Demonstrations

Use this format for an in-lesson explanation that becomes clearer when the learner
reveals a change, compares positions, or follows a process. The two Vector Space
maps are the reference implementation. The consistent experience is: read a short
setup, activate one control, see what changed, and connect the result to the idea.

This is the default for new guided demonstrations across lessons. Quizzes, open
explorations, games, and labs retain controls appropriate to their purpose. A static
illustration is preferable when showing the complete relationship teaches it more
clearly; interaction should earn its place.

## Standard layout

1. **Introduction outside the box.** Explain the concept and the learner’s goal in
   ordinary lesson body text. Use a section heading only for a genuine topic turn.
2. **Blue outer box.** Contains one instruction card above one visual panel. No
   repeated title, activity eyebrow, numbered step list, or takeaway banner.
3. **White instruction card.** Explain the current situation and what the next
   action will reveal. Put the control below the text, aligned left.
4. **White visual panel.** Show the diagram, example, or process. Keep the important
   labels and values with the objects they describe.
5. **Conclusion in the same instruction card.** Explain what the finished example
   demonstrates. Replace the advance control with a completion indicator and Replay.

“See It” is the action label, not a new SEE IT activity type or heading. Do not
route this pattern through the existing TRY IT instruction list merely to obtain
an outer container.

## Appearance

Use the course tokens and typography. The blue shell is the deliberate exception
to the usual lavender narrative containers and their border treatment.

| Element | Standard |
| --- | --- |
| Outer surface | `--info` at 8% mixed with `--card` |
| Outer outline | 1.5 px, `--info` at 30% |
| Outer corners and padding | 20 px radius; 24 px padding |
| Instruction card | White `--card`; 1 px outline using `--info` at 22%; 16 px radius; 20 px vertical and 24 px horizontal padding |
| Instruction accent | 4 px `--primary` rule at the left, inset 12 px from the top and bottom |
| Instruction text | `BodyP`: 17 px, 1.65 line height, `--inkSoft`, course sans font; normal body weight |
| Separate ideas | One blank line, approximately one line of body text; no blank line within a single idea |
| Text to controls | 14 px minimum after the longest instruction; no extra empty paragraph |
| Card to visual | 20 px gap |
| Visual panel | White `--card`, 16 px radius; default 24 px inner padding |
| Main control | Existing `ActivityButton`: dark fill, white label, bold text, 8 px radius |
| Completion | Green check plus neutral “Complete” text, weight 600; never color alone |
| Replay | Secondary button using `--primaryFaint` and `--primaryDeep` |

At widths of 540 px or less, use 12 px outer padding, 16 px instruction padding,
12 px inner-card corners and card-to-visual gap, and 16 px vertical / 12 px
horizontal visual padding. Preserve readable body text and labels rather than
shrinking the entire experience to fit. Controls may wrap within their reserved
area. Interactive targets must remain comfortable to tap.

## Instruction writing

Give the learner enough information to understand the next reveal before asking
for it. Prefer concrete objects, values, and short sentences. Define unfamiliar
dimensions where they are first used; do not depend on a distant legend.

A prompt may contain an observation about the previous result, followed by a new
task. Separate those ideas with a blank line. Keep the new task and its coordinates
or values together. For example:

> Hot coffee’s scores differ more from Coke’s and Pepsi’s, so it sits farther away
> in the Coffee and tea neighborhood.
>
> Now you get numbers that don’t match any of our existing drinks. Your goal is to
> find the closest drink. Mystery Drink A’s coordinates are sweetness 9, bitterness
> 1, fizz 10, heat 2, caffeine 3, darkness 8, and citrus 9. Add Mystery Drink A to the map.

Use selective emphasis for the conclusion or a key distinction. Do not bold the
whole prompt, add technical implementation details, or repeat every sentence in
the visual. A generic button label works because the adjacent instruction names
the specific action.

## Controls and progression

| Situation | Control and result |
| --- | --- |
| Add, change, or reveal something | **See It**. One activation advances one authored reveal. |
| A separate explanation needs reading before the next idea | **Continue**, only if that additional state is necessary. Do not use See It when nothing will be shown or changed. |
| Ask the learner to compare | Ask in the card while the candidates are visible; **See It** reveals the answer and its explanation. No answer highlight beforehand. |
| Demonstration finished | Show the conclusion, green check with **Complete**, and **Replay**. No disabled See It button. |
| Replay | Reset this demonstration to its initial prompt and visual state, ready for the first action. |

Default to See It. Do not alternate among “Do It,” “Next,” “Show,” and custom
action names for equivalent reveals. Do not display step numbers, a step counter,
or a list of future steps. These sequences may contain both actions and
explanations, so counting clicks is not a useful measure of progress.

Keep progression learner-controlled. Do not automatically advance the instruction
or reveal an answer on a timer. A learner may think about a question without
submitting a response; this does not make the demonstration a scored quiz.

## Stable layout and visual behavior

- Size the instruction text area to its longest authored state at the current
  width and font size. Anchor controls beneath that area so they remain at the
  same height throughout this demonstration. Different demonstrations may need
  different heights. Reflow on resize or zoom; never crop text to keep a fixed height.
- Remove surplus space below the longest instruction. A reserve for genuinely
  needed copy is acceptable, but do not add a standard empty line after every prompt.
- Keep the visual frame stable while revealing new elements. Preserve earlier
  objects and their positions when continuity is part of the teaching. Remove or
  move an object only when that change is the lesson’s point.
- Use brief, purposeful reveal animation. Animate the new information, not every
  previously visible object again. Respect reduced-motion preferences and keep the
  same information available without animation.
- Keep a label and its values together. In the Vector Space maps, the values are
  centered beneath the name at 75% of the name size. Other diagrams may need a
  different arrangement, but spacing must be consistent and labels must not collide.
- Distinguish an object’s label connector from an answer or relationship line.
  Show an answer ring or connection only when the learner requests the answer.
- Keep essential text selectable where practical. If diagram text becomes too
  small on narrow screens, use a responsive layout or a readable companion
  description; do not rely on color, hover, or tiny labels alone.

## Completion and access

The final instruction explains the result and the concept it demonstrates. Put a
distinct concluding idea on a second paragraph and emphasize it when useful.
Keep the finished visual in place for inspection. The green check means the
demonstration is complete; it does not claim the learner passed an assessment.
Replay appears only here and is optional.

Use native buttons, visible keyboard focus, and a meaningful accessible name for
the demonstration. Announce the current instruction and results politely. Describe
the visible diagram separately from the instruction for the next action. Hidden
content used to measure height must not be focusable or read by assistive technology.
Do not shift focus into decorative visual content when the learner advances.
When the final action disappears, keep focus on a sensible completion target or
Replay. Replay returns focus to the first action.

For print, show the complete explanatory visual and enough accompanying text to
understand it without controls. For video, use the same visual states and data;
narration replaces the instruction card. Omit buttons, completion UI, and outer
lesson prose. Measure reveal timing against the recorded narration, following the
[video storyboard](../../gemini-notebook/vector-space/STORYBOARD.md).

## Authoring and implementation

For each demonstration, prepare the introduction, initial visual, instruction for
each state, change caused by its action, answer reveal where needed, and final
conclusion. Keep a single set of visual states and data usable by the lesson and
video capture. Validate the longest prompt, narrow layout, answer timing, final
state, Replay, keyboard behavior, and reduced motion.

The shared implementation in `index.html` is `GuidedDemoShell`,
`GuidedDemoControls`, and `GuidedDemonstration`, with `.guided-demo-*` styles.
The shell measures all authored instructions at the current width, and the
controls reserve room for Complete and Replay even when they wrap. Completion
focuses Replay; Replay focuses the first action. Measurement content is hidden
from assistive technology and inert.

`GuidedDemonstration` accepts a label, an array of states with instructions
(a string or an array of paragraph nodes for selective emphasis), optional action
labels, and a separate `renderScene` function. It owns linear
progression, Replay, and the completed print state. `VectorMapBox` and
`VectorMapControls` are adapters to the same shell and controls; the existing
map data, geometry, and capture interface remain separate.

Keep subject data and diagram geometry outside that shell. Do not duplicate
the shared CSS per lesson or force
quizzes and labs into a linear reveal component. Existing activities should adopt
the pattern when their lesson is revised, not through an automatic course-wide
conversion.

### Embeddings: adding a dimension

`EMBEDDING_DIMENSION_DATA`, `EMBEDDING_DIMENSION_STATES`, and
`EmbeddingDimensionScene` begin with the ratings scale and six dimension headings visible,
and a prompt about rating Coffee. The first action fills Coffee’s row; the second
fills Coke’s. Row order is Coffee, Coke, Pepsi, keeping Coke and Pepsi adjacent.
Then ask which drink has Sweet 9, Bitter 1, and Fizz 10, then highlight Coke’s
three values and define vector, dimension, and value. The next action adds Pepsi.
Pause for a comparison before highlighting Coke and Pepsi’s six matching values.
The next action adds the Citrus heading and empty rating tiles. A separate final
action fills the Citrus values: Coffee 0, Coke 1, and Pepsi 10.

The visual follows the original drink board: shared colored column headings,
colored number tiles, and outlined drink rows. Reserve space for Pepsi and Citrus
so earlier values stay in place. On narrow screens, transpose the table to keep
drink values side by side, with dimensions down the left. Use native table headers
and hide unrevealed values from assistive technology. The finished view retains
all three drinks. Replay returns to the headings and Coffee prompt, with drink names and values hidden.

This replaces both static taste-profile boards and their repeated explanation.
The ratings are illustrative taste-test scores, not measured product claims.
Print shows the completed comparison and explanation.

Run `node scripts/video/preview_embedding_dimension.cjs` to regenerate the preview
from the live components. `previews/embedding-dimension.html?capture=1&step=7`
shows only the finished scene; `window.setEmbeddingDimensionScene(step)` selects
any of its eight states. This does not update the recorded lesson video.

### How AI Answers pilot

`ANSWER_BUILD_STATES` and `AnswerBuildScene` supply a second reference. Introduce
the bolded question in the opening instruction. Keep guidance in the instruction
card and show the growing reply directly in the visual panel, without an internal
context card. Reveal initial possibilities, then highlight one selected token
with a 2 px border and add it to the reply in the same action. Preserve the chart
for inspection. The next action updates the next-token probabilities. Pause with
the dog names visible before selecting and adding Spot. Select and add the period next,
then reveal the special end-of-answer token and explain inference.

The authored probability distributions are illustrative and include the combined
remainder of the vocabulary. The live instructions omit the probability disclaimer;
the print explanation retains that context. Words stand in for tokens in this teaching
example. Selection is one possible run, not a claim that the model always picks
the highest probability. The chart follows One More Thing’s probability rows:
rounded outlines, purple bars, bold percentages, and a striped Other (combined)
bar. Candidates remain neutral until the selected result is revealed.
The guided demonstration replaces the static answer-build
board and its repeated explanation; the separate prediction-loop practice stays.

Run `node scripts/video/preview_how_ai_answers.cjs` to generate a preview from the
live components. `previews/how-ai-answers.html?capture=1&step=10` renders only the
scene for video; `window.setAnswerScene(step)` selects any authored state.
The existing recorded video is not regenerated by this preview. New narration
timings must be measured before producing a replacement video.
