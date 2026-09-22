# Training: roll 1 (2026-09-22) against the live video

Narration review under `scripts/video/NARRATION-REVIEW.md`. Lesson authority: `index.html` TrainingSection (line 6383) and
`lessons/training.md` (2026-09-21 recipe, eight required-verbatim lines in `Prompts/training-video-prompt.txt`, board-coverage
pass applied). Bundles in this folder: `training-1/` (roll, 5:18.63, 39 cuts) and `training/` (live v4 of 2026-09-16, 4:37.57,
a visual retrofit of a 2026-09-09 roll on the old materials). Uncertain spans re-heard with small.en (`training-1-words-small.txt`).

## Teaching points (page order)

1. Hook: AI can explain chemistry, write code, improve an essay; how did it learn?
2. Basketball: shoot, check where it goes, adjust aim or force.
3. "AI training follows a similar pattern: guess, check, and adjust." (verbatim); training adjusts the numbers inside the model.
4. Board 1, The Training Loop: peanut butter and jelly; guess cloud; check against jelly; adjust so jelly is more likely; repeat; "Repeat with more examples. The patterns build." (verbatim)
5. Board 2, Before Training Starts: set up the system (design the model, starting values, training adjusts them); gather the data: books, websites, conversations, code, images, audio, video; the curriculum.
6. Bridge: training also teaches following instructions and useful answers; one basketball question through three phases.
7. Board 3, Three Phases: "How do I shoot a basketball?" (verbatim); Pretraining learns patterns from data; Instruction Tuning learns to follow instructions; Preference Tuning improves responses through feedback.
8. Board 4, Pretraining: vast data, more than 1,000 lifetimes of reading; guesses what comes next, checks against the example; "Training adjusts its internal numbers, called weights." (verbatim); learns to write sentences, explain ideas, produce code; sample answer in full; still needs work: fluent, does not reliably follow instructions.
9. Board 5, Instruction Tuning: questions paired with example answers; practices, compares, weights adjusted toward the examples; sample answer in full; still needs work: unclear, incomplete, unhelpful.
10. Board 6, Preference Tuning: several answers, people pick the best (clear, useful, accurate); weights adjusted; sample answer in full to its last sentence; "Feedback helps improve the answers, but AI can still give a wrong answer that sounds right." (verbatim)
11. Training ends, model ready to use; a normal chat uses the trained weights; "It can work with new information you give it, but your conversation does not change those weights." (verbatim)
12. Close: "AI learns from examples and feedback." / "Guess. Check. Adjust. Repeat." Nothing after.

```text
LESSON: training
CANDIDATE: Prompts/training-1.mp4 (5:18.63)
VERDICT: REPAIR (one judgment call for David on the data list; see below)
TEACHING POINTS:
  1 hook               — TAUGHT — 0:00–0:09 "AI can explain complex chemistry, write computer code, and help you improve an essay. How did it actually acquire these skills?"
  2 basketball         — RICH   — 0:09–0:18
  3 pattern / numbers  — RICH   — 0:18 verbatim; 0:23 "Instead of physical force, the training process modifies the internal numbers that determine the model's output." (paraphrase; meaning intact)
  4 Training Loop      — RICH   — 0:32–1:09: cloud, jelly, adjust "to make the word jelly more likely in this exact situation", "The loop runs again on the next example.", banner verbatim. 1:01 "Dualness once is not enough." is garbled on both decoders (probably "Doing this once is not enough."): cut it.
  5 Before Training    — THIN   — 1:14 set-up RICH; 1:20 gather the data names "books, websites, conversations, and code" only: images, audio, and video are not spoken (the board lists all seven; the prompt asked for all seven). No roll or live donor says them.
  6 bridge             — TAUGHT — 1:28 "Building the system and running this basic loop establishes the foundation. To reach the level of a helpful assistant, the AI must undergo three specific training phases." (the "follow instructions and give more useful answers" idea is compressed to "helpful assistant"); 1:38 "This panel shows the specific process of teaching a model to follow instructions." mislabels the Three Phases board: cut.
  7 Three Phases       — RICH   — 1:43–2:03: the question verbatim, three phases with their one-line roles, orientation only as asked
  8 Pretraining        — RICH   — 2:03–2:49; verbatim weights line at 2:16 inside "Every time it checks a guess against an actual example, training adjusts its internal numbers, called weights."; sample answer complete; still-needs-work TAUGHT ("completely fails to reliably answer the direct instruction" overstates "doesn't reliably follow your instructions yet"); "Across billions of examples" adds a count the prompt banned; "produce code" not spoken (writes sentences, explains ideas only)
  9 Instruction Tuning — TAUGHT — 2:49–3:36; questions paired with examples, practices, compares, adjusts weights "so its output matches that specific format" (narrows "more like those examples" to format); sample answer verbatim; still-needs-work RICH. Additions: "the objective shifts entirely to teaching the model how to format its knowledge", "It requires a final layer of refinement based on human taste."
 10 Preference Tuning  — RICH   — 3:36–4:27; several answers, humans pick "the one that is clearest and most accurate" ("useful" dropped); weights adjusted; sample answer read to its last sentence but with one wrong word at 4:07 "and the other to STUDY the ball" (heard on both decoders; the board says steady); verbatim feedback line at 4:22
 11 ready / weights    — TAUGHT — 4:42 "When these three training phases conclude, the model's architecture is locked, and it is deployed for everyday use." ("architecture is locked" is an invented claim; weights are what is fixed); 4:49 "During a normal chat, it relies entirely on the final weights that training produced." RICH; verbatim line at 4:54; 5:00 "Chatting with the AI does not train the model in real time." accurate addition
 12 close              — RICH   — 5:09 / 5:12, nothing after
HARD REQUIREMENTS:
  "AI training follows a similar pattern: guess, check, and adjust."        — MET — 0:18
  "Repeat with more examples. The patterns build."                          — MET — 1:06
  "How do I shoot a basketball?"                                            — MET — 1:47
  "Training adjusts its internal numbers, called weights."                  — MET — 2:16 (intact as the second clause of a longer sentence)
  "Feedback helps improve the answers, but AI can still give a wrong answer that sounds right." — MET — 4:22
  "It can work with new information you give it, but your conversation does not change those weights." — MET — 4:54
  "AI learns from examples and feedback."                                   — MET — 5:09
  "Guess. Check. Adjust. Repeat."                                           — MET — 5:12 (cadence to hear)
  Third sample answer read to its final sentence                            — MET as a read, MISSED on one word ("study")
ERRORS: 4:07 "study the ball" — board and Markdown say "steady the ball". 4:42 "the model's architecture is locked" — the lesson says the model is ready to use and its weights do not change; architecture is not what training fixes.
SOURCE_QA: PASS
ADDITIONS: "Chatting with the AI does not train the model in real time." (5:00) is accurate and reinforces the prompt's guardrail; keep. "Across billions of examples" (2:22) is true but an unapproved count; David's call, cuttable only with its sentence.
REPAIR PLAN:
  a. Cut 0:29.0–0:32.0 "This diagram shows the core training framework." (banned word, production talk; own gap each side).
  b. Cut 1:01.3–1:02.6 "Dualness once is not enough." (garbled; whole sentence between silences 59.72→61.32 and 62.58→63.50).
  c. Cut 1:38.7–1:43.0 "This panel shows the specific process of teaching a model to follow instructions." (mislabel).
  d. Graft the live video's "Use one hand to shoot, and the other to steady the ball." (live 3:34.1–3:38.0, a whole sentence between gaps) over roll 1's 4:05.3–4:07.7 "Use one hand to shoot, and the other to study the ball." Under Board 6, our picture. Level-match at build.
  e. Cut 4:27.0–4:42.3 "Through pre-training, instruction tuning, and preference tuning, the guess check adjust loop builds upon itself. The result is a model that no longer just predicts the next word, but accurately follows instructions and answers questions in a helpful way." (summary the prompt banned; "accurately follows instructions" overclaims; own Notebook scene 4:27.6–4:42.3 with two invented diagrams).
  f. Replace 4:42.3–4:48.4 "When these three training phases conclude, the model's architecture is locked, and it is deployed for everyday use." with the live video's "When those three phases of training conclude, the heavy lifting is done. The model is packaged up and ready for public use." (live 3:55.2–4:02.2, a whole beat). Picture under it: a held drawn frame (the FROZEN WEIGHTS drawing at 4:52 or the preference board), since roll 1's own picture there is the paper-craft phone photograph (rule 8c). Alternative: cut the sentence and let "During a normal chat…" carry the beat; "ready to use" is then implied only.
  g. Cut 5:04.2–5:08.5 "This graphic summarizes the entire development journey down to its foundational elements." (production talk before the close).
  h. Judgment call, not repairable from audio: the data list names four kinds, not seven. Accept (the canonical board on screen lists all seven, and the point is "many kinds, this becomes the curriculum") or reroll for the list. Recommend accept; flagging because the rule says a THIN essential does not pass on mention alone.
  About 35 s out; projected runtime about 4:45, pill 5 min.
EDITING NOTES:
  Notebook renders of all six boards (0:32–1:08, 1:12–1:28, 1:40–2:00, 2:03–2:49, 2:49–3:36, 3:36–4:27) replaced by the canonical JPGs. Boards 4–6 run back to back for 2:24 with no Notebook drawing between them, because the boards themselves carry the teaching (Edit Spec 8b: report the longest unbroken run; roll 1 drew nothing for those beats, so there is nothing to interleave without inventing filler).
  Invented diagrams: 0:20 "Universal Training Loop" and 0:24–0:31 "Internal Weights" neural net under the numbers sentence (drawn; keep or cover with the Loop board arriving at "Instead of physical force"); 1:32 "FOUNDATIONAL TRAINING LOOP" and 1:36 "THREE CURRICULUM PHASES" (under the bridge; 1:36 goes with cut c); 4:28–4:40 "AI TRAINING CURRICULUM" / "TRANSFORMATION" (inside cut e); 4:52–5:04 "FROZEN WEIGHTS" prompt→weights→response drawing (drawn, labels invented but harmless; keep under the weights lines).
  Photograph: 4:44–4:52 paper-craft phone (photographed collage) under "deployed for everyday use / During a normal chat": cover (rule 8c).
  5:16 Notebook's loading spinner after the close: outside the close audio, never rendered.
  Corner mark throughout; the build removes it. Frame 0 is a drawn molecule sketch, no stock image.
LISTENING: small.en confirms "Dualness" (garble), "study", the four-kind list, "billions", "architecture is locked". Not heard by ear: all joins above; David should listen to the two grafts (d, f) and the seven cuts.
```

```text
LESSON: training
CANDIDATE: course-assets/training/training.mp4 (4:37.57, live v4 of 2026-09-16)
VERDICT: superseded by roll 1 (REPAIR-at-best against the current materials)
TEACHING POINTS: coverage complete and mostly TAUGHT, in the old formal register: "Artificial intelligence uses a remarkably similar pattern" (0:18), "strictly involves tweaking a set of internal numbers", "which engineers formally call weights", "the model can still hallucinate" (3:45, a banned word), "This brings up a common misconception". Data list names five kinds (adds images; no audio, video). Third sample answer read only to "steady the ball" (3:32–3:38), then paraphrased, which is why the prompt now demands the last sentence. Board order differs from the page (Before Training Starts before the Loop).
HARD REQUIREMENTS: 3 of 8 MET ("How do I shoot a basketball?" 1:36; "AI learns from examples and feedback." 4:27; "Guess, check, adjust, repeat." 4:29). The other five are paraphrased.
ERRORS: none factual.
ADDITIONS: "The model is packaged up and ready for public use." (3:59) is the donor for roll 1's repair f. "Use one hand to shoot, and the other to steady the ball." (3:34) is the donor for repair d.
```

```text
BEST-OF PLAN: training
BASE: Prompts/training-1.mp4 (8 of 8 verbatim lines, all three sample answers complete, the page's order and voice)
  Sample answer 3, "steady the ball" — roll 1 WRONG word @4:05 | live MET @3:34 — TAKE live (under Board 6)
  Ready to use — roll 1 WRONG-wording @4:42 "architecture is locked" | live TAUGHT @3:55 "heavy lifting is done… packaged up and ready for public use" — TAKE live (under a held drawn frame; the roll's own picture there is a photograph)
  Everything else — KEEP roll 1
GRAFTS: 2, both audio-only; one under a board, one under a held drawing. Plus cuts a, b, c, e, g.
```

## Proposed edit plan (for David's approval before the first build; Edit Spec 1b; timing provisional until the cut list is approved)

| Board | Highlighting sequence | Camera | Reason or exception |
|---|---|---|---|
| The Training Loop | whole board in at "Let's look at one baseline training example" (0:32); card rings Guess 0:36, Check 0:45, Adjust 0:52; banner ring at "Repeat with more examples" 1:06 | full board (compact) | three illustrated cards read at full view |
| Before Training Starts | card rings Set Up the System 1:14, Gather the Data 1:20 | full board (compact) | |
| Three Phases of Training | question ring at 1:47; card rings Pretraining 1:49, Instruction Tuning ~1:53, Preference Tuning 1:57 | full board (compact) | orientation only |
| 1 · Pretraining | section rings: Learn from Vast Amounts of Data 2:03, What an Answer Might Look Like 2:29, What Still Needs Work 2:39 | dense: dive to each stacked section | body text is small at full view |
| 2 · Instruction Tuning | same three sections at 2:49, 3:13, 3:23 | dense | |
| 3 · Preference Tuning | same three sections at 3:36, 3:58, 4:18; banner none | dense | graft d lands inside the answer section |
| Standard close | none | full | from "AI learns from examples and feedback." |

Pauses (Edit Spec 6): propose three, each adding about 0.6 s over the natural gap: before "Think about learning to shoot a basketball" (0:09), before the Three Phases question (1:47), before the close. No pause between a board's sections.
