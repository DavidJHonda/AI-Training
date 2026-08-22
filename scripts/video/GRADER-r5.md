# r5 video grader

Read this file completely before grading. It is the canonical grading authority
for one course lesson video. `videos/video-rubric.csv` is a synchronized tracker
summary, not a second source of rules.

The course is for 16-year-olds. The video's primary job is to replace the lesson
reading without losing essential understanding.

## 1. Required inputs

Your assignment names the lesson slug, lesson source, and grading bundle.

1. Read the lesson as an editor and a grader. It is the grounding source, but it
   is not presumed infallible.
2. Read the complete bundle:
   - `transcript.txt`: timestamped narration and the teaching spine.
   - `sections.txt`: video time per teaching beat compared with lesson weighting.
   - `holds.txt`: long no-cut spans paired with their narration.
   - `scenes.txt`: scene-cut times.
   - every image in `sheets/`: the complete sampled visual record.
3. Identify the exact current lesson boards from the lesson's references in
   `index.html`, including assets in `illustrations/` and `lessons/`. Do not use
   an older board merely because it appears in the video bundle.

A grade that skips the transcript, lesson, or any contact sheet is not valid.

## 2. Anti-anchoring

Grade the video fresh. Do not read its previous grade, tracker row, memory files,
git history, commit messages, generation prompt, or the sitting catalog video.
If you already know an old score, ignore it. Comparisons between two rolls are
valid only when both are graded in the same sitting.

Per-lesson prompts steer generation. They are deliberately more restrictive than
the grading rules and are not grading authority. A prompt violation affects the
grade only when it also violates this file. A challenger intake may separately
report prompt compliance under `SPEC` without changing the numeric score.

## 3. Scoring priority

Score six dimensions independently. Do not compute a total; totals are assembled
centrally. The dimensions add to 100, but the ship gates remain non-compensable.

Accuracy and complete teaching come first. A useful extra sentence is preferable
to an elegant omission, and complete, slightly overlong raw material is preferable
to a concise roll that lacks essential narration. Excess can usually be cut.
Missing or inadequate teaching normally requires a re-roll.

| Field | Max | What it measures |
|---|---:|---|
| `TEACHING_COVERAGE` | 20 | Every major teaching beat reaches the viewer with enough substance to preserve its meaning. A paragraph reduced to a passing clause is partial coverage. |
| `TEACHING_LESSON_MATERIAL` | 15 | The narration is grounded in the lesson's strongest model, examples, numbers, analogies, and sequence. Brief accurate additions or refreshers may earn full credit when they improve clarity or flow. Deduct only when outside material is weaker, distracting, inconsistent, or displaces a better explanation. If a new explanation is stronger, recommend updating the on-page lesson instead of penalizing the video. |
| `TEACHING_TEACHES_VS_RECITES` | 15 | The why lands well enough that a viewer could explain the idea in their own words. Correct recitation without explanatory work belongs in the middle of the band. |
| `TEACHING_BOARD_CONTENT` | 10 | The teaching carried by every lesson board, table, framework, or enumerated structure reaches the viewer. This score measures instruction, not asset fidelity. The separate ship gates enforce exact current boards and their visual treatment. |
| `CLEANLINESS` | 20 | Content-carrying visuals are legible, contained, and free of gibberish, pseudo-text, clipping, or white-on-light failures. Incidental prop text is forgiven. |
| `PACING` | 20 | Coverage comes first. Useful explanation, reinforcement, or a brief refresher is not penalized for adding runtime. Deduct for dead time, unnecessary repetition, confusing detours, or badly unbalanced structure that buries the central lesson. Prefer complete, slightly overlong material to a concise video that omits or compresses essential teaching. |

### Coverage, teaching, and pacing are different

- `TEACHING_COVERAGE` asks whether the complete lesson reached the learner.
- `TEACHING_TEACHES_VS_RECITES` asks whether the explanation creates understanding.
- `PACING` asks whether the completed teaching flows without waste or distortion.

Do not punish the same thin beat in all three dimensions automatically. If a beat
is too compressed to teach, charge Coverage or Teaches vs Recites and consider the
Substitute gate. Charge Pacing too only when the video's broader allocation or flow
creates a distinct problem.

Runtime and prompt minute ranges are never scored. Use `sections.txt` as evidence,
not a verdict. Worked examples and board walkthroughs legitimately take more spoken
time than their source word count.

### Dead time

A still frame costs nothing while narration is teaching from it. A board held while
its rows are explained is working as designed. Dead time begins only after narration
moves beyond the displayed content, or when repetition adds no understanding. Check
`holds.txt` and adjacent scenes before deducting.

## 4. Source QA

Evaluate the lesson before treating it as authoritative.

`SOURCE_QA` passes only when the lesson's major claims and distinctions are accurate
and internally consistent. Fail it for a material error, contradiction, or example
that undermines its rule. Cite exact lesson lines and identify the source correction.
Then fix the lesson and generation materials before repairing or re-rolling the video.

Do not fail Source QA for taste, wording preference, harmless compression, or because
the video found a clearer accurate explanation. A better video explanation should be
flagged in `NOTES` as a candidate lesson improvement.

## 5. Visual evidence discipline

Contact sheets sample motion and can create false defects. Before reporting one:

1. If the apparent problem could be a pan, build, counter, transition, or animation,
   check frames on both sides using `scenes.txt` and `holds.txt`. Do not judge a moving
   state from one sampled frame.
2. Read multi-column boards down each column. Do not horizontally interleave separate
   columns and call the result scrambled text.

Treat claims accordingly:

- Gibberish on a static, content-carrying visual is reliable evidence.
- Cropping may be real, but state whether a nearby pan resolves it.
- Collision, duplication, and scrambled-layer claims require adjacent-frame proof.

Narration findings do not have this sampling problem.

### What cleanliness does not score

- Incidental b-roll text is forgiven when the narration is not teaching from it.
- Animation is not graded. Never deduct for stills, static boards, limited motion,
  or a missed opportunity to be more dynamic.
- Visual style is not graded. Dotted paper, paper craft, live-action hands,
  photoreal spans, and off-palette colors may receive at most one brief note.

## 6. Instructional and ship gates

Evaluate every gate after assigning the six scores. A high numeric score cannot
compensate for a failed Source QA, Accuracy, Substitute, or Spine gate.

- `SOURCE_QA`: The grounding lesson is accurate and internally consistent.
- `GATE_ACCURACY`: The video's teaching is accurate and internally consistent,
  with no material contradiction, reversal, or misleading distinction. If the
  video inherited the problem from the lesson, fail Source QA too.
- `GATE_SUBSTITUTE`: A student can watch instead of reading and lose no essential
  understanding. Every major beat is meaningfully taught; essential examples,
  frameworks, distinctions, and explanatory links survive; and the central idea
  is understandable and usable without opening the lesson. Minor optional detail
  may be compressed.
- `GATE_SPINE`: The narration includes every hard lesson requirement, including
  required full terms or verbatim lines. For example, Document Trap must say
  "Retrieval-Augmented Generation" in full. A missing hard requirement
  disqualifies the narration spine.
- `GATE_RESTRAINT`: No legible profanity, prohibited depiction of a real person,
  or banned imagery such as self-harm, restricted medical imagery, or red-staining
  appears. The course is for 16-year-olds.
- `GATE_STOCK`: No Getty, watermark, or unlicensed stock asset appears. Cropping a
  watermark is not a repair. Engine-generated photoreal imagery is a style choice,
  not stock. Course assets from `illustrations/` and `lessons/` are always allowed.
- `GATE_ENDING`: The close board is the literal final frame. No outro or engine-drawn
  sign follows it.
- `GATE_SYNC`: Narration and visuals agree in timing. Elements appear as they are
  mentioned; narration leads and visuals follow.
- `GATE_BOARD_WALK`: Every teaching board is the exact current lesson board and uses
  the correct treatment:
  - Compact or lighter-text board: keep the entire board visible; begin unmarked,
    then highlight the active card, row, or component in spoken order. A restrained
    whole-board push is allowed. Do not dive or pan between items.
  - Dense or text-heavy board: establish the full unmarked board, dive to the complete
    active card or section, and pan smoothly to the next complete area in spoken order.
    Never crop inside a card. Pull back when timing permits.
  - A board discussed only as a whole receives an unmarked restrained push.
  Numeric Board Content credit does not waive this ship requirement. A redraw may
  teach the right content and still fail this gate.
- `GATE_NO_NOTEBOOK_HIGHLIGHT`: All teaching-board emphasis uses the course-native
  ring-and-chip treatment. Gemini Notebook highlighting is forbidden. Highlights
  replace one another unless narration explicitly combines points. Use the item's
  accent color when available, otherwise course purple.
- `GATE_STANDARD_CLOSE`: The exact current app close is inserted in post, unmarked,
  on the standard canvas with standard centering, start framing, easing, fixed zoom
  endpoint, final visible size, and settled hold. Longer narration adds hold time,
  never zoom distance. Quiz videos are exempt only when explicitly designated.
- `GATE_EDIT_INTEGRITY`: Every edit is seamless. No one-frame or brief remnants of
  deleted visuals appear; no spoken sentence is cut short; and no click, blip, or
  abrupt noise-floor dropout is audible. Visual-only repairs preserve identical
  source audio. Natural breaths are not defects by default. A reviewed breath may
  be kept, attenuated, or replaced with equal-duration matched room tone. Do not
  ripple-delete breaths or substitute digital silence when it creates an audible gap.

### Repair meaning

- A failed Accuracy, Substitute, or Spine gate normally requires a re-roll. Use a
  donor audio graft only when it restores the complete beat coherently.
- Visual gate failures normally require a repair over untouched narration.
- A Source QA failure requires fixing the lesson and generation materials first.
- Specific owner waivers are allowed only when recorded in the report and tracker.

## 7. Scoring discipline

- Cite or do not deduct. Every deduction requires a timestamp or direct quote.
- Every full mark states what would have cost a point. A dimension with neither
  supporting evidence nor a deduction threshold has not been graded.
- Use the middle of the range when evidence warrants it. A catalog in which every
  roll scores near 90 is not discriminating.
- The numeric score ranks raw-material quality. It never overrides a failed gate.
- When new material improves the explanation, do not deduct merely because it is
  absent from the lesson. Note the stronger explanation as a possible lesson edit.

## 8. Output format

Return exactly this block and nothing before or after it:

```text
SLUG: <slug>
RUNTIME: <m:ss>
TEACHING_COVERAGE: <n>/20 — <evidence with timestamp or quote>
TEACHING_LESSON_MATERIAL: <n>/15 — <evidence>
TEACHING_TEACHES_VS_RECITES: <n>/15 — <evidence>
TEACHING_BOARD_CONTENT: <n>/10 — <evidence; identify the current board source or say none exists>
CLEANLINESS: <n>/20 — <evidence>
PACING: <n>/20 — <evidence>
SOURCE_QA: PASS|FAIL — <lesson-line evidence; if failed, identify the source fix>
GATE_ACCURACY: PASS|FAIL — <timestamp or quote>
GATE_SUBSTITUTE: PASS|FAIL — <decisive evidence about instructional equivalence>
GATE_SPINE: PASS|FAIL — <evidence>
GATE_RESTRAINT: PASS|FAIL — <evidence>
GATE_STOCK: PASS|FAIL — <evidence>
GATE_ENDING: PASS|FAIL — <evidence>
GATE_SYNC: PASS|FAIL — <evidence>
GATE_BOARD_WALK: PASS|FAIL|N/A — <evidence; N/A only when no teaching board appears>
GATE_NO_NOTEBOOK_HIGHLIGHT: PASS|FAIL|N/A — <evidence; N/A only when no teaching board appears>
GATE_STANDARD_CLOSE: PASS|FAIL|N/A — <evidence; N/A only for an explicitly exempt quiz>
GATE_EDIT_INTEGRITY: PASS|FAIL — <boundary-frame, sentence-completion, and audio-continuity evidence>
BIGGEST_LEVER: <single highest-value fix and whether it requires RE-ROLL or REPAIR>
NOTES: <at most two lines, including any candidate lesson improvement, or "none">
```

The final message is the return value and must contain that block alone.
