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

## Build: v5 review candidate (2026-09-22, David: approved plan a–h + best-of, "build it")

**Candidate:** `Prompts/training-v5.mp4` (8790 frames, 4:53.00, 30 fps, sha256 def32dc7366fe6d3…). Built by
`scripts/video/build_training_v5.py` from `Prompts/training-1.mp4`; build folder `build-v5/` (edit-manifest.json, legs,
state sheets, guard strips in `guard/`, `kept-notebook-spans.jpg`, `output-frame-0000.jpg`, `qa-report.json`, output
transcript and word stamps). Review only: live video, raw roll, lesson, six boards and the close JPG unchanged (manifest
`protected_files_unchanged` all true); index.html and the registry not touched. Not committed.

**Timeline (source frames of roll 1 → output frames):**
- 0–263 Notebook opening (paper-craft molecule, code monitor, essay; chemistry question mark) → 0–263; pause 18 (holds the question mark)
- 263–855 question mark, basketball shots, Notebook's invented "Universal Training Loop" and "Internal Weights" drawings → 281–873
- cut a (855→948): "This diagram shows the core training framework." removed; the roll's cut into its Loop render (866) is inside it
- 948–1825 The Training Loop, canonical (rings Guess 36.76, Check 45.22, Adjust 52.54) → 873–1750; cut b (1825→1899) "Dualness once is not enough." removed, camera still
- 1899–2083 The Training Loop, banner ring 66.34 → 1750–1934
- 2083–2662 Before Training Starts, canonical (card rings 74.30, 80.56) → 1934–2513
- 2662–2795 Notebook FOUNDATIONAL TRAINING LOOP drawing → 2513–2646; 2795–2958 frame 2794 held (the drawing starts morphing into "THREE CURRICULUM PHASES" at 2795, 1:33.2, not 1:36 as the sheets suggested) → 2646–2809
- cut c (2958→3089): "This panel shows the specific process of teaching a model to follow instructions." removed; the roll's Three Phases render cut (2962) is inside it
- 3089–3210 Three Phases of Training, canonical → 2809–2930; pause 18; 3210–3690 question ring 107.18, cards 110.16 / 113.48 / 118.16 → 2948–3428
- 3690–5082 1 · Pretraining (dense; sections 126.86, 149.50, 159.36) → 3428–4820; 5082–6482 2 · Instruction Tuning (172.68, 193.58, 204.00) → 4820–6220
- 6482–7355 3 · Preference Tuning (218.92, 238.64) → 6220–7093; 6 f roll-1 tone; graft d = live v4 6411–6525 "Use one hand to shoot, and the other to steady the ball." (−0.57 dB) → 7099–7213; 7446–8028 rest of the board (258.50 ring) → 7213–7795. The donor is 23 frames longer than the roll-1 sentence, so the board leg runs 23 frames ahead of source time from the graft on; the camera is holding the answer section throughout and the third onset is entered in leg time, so nothing moves.
- cut e (8028→8676): summary + "architecture is locked" sentence removed; 6 f tone; graft f = live v4 7055–7290 "When those three phases of training conclude, the heavy lifting is done. The model is packaged up and ready for public use." (−2.56 dB) under the held FROZEN WEIGHTS frame 8750 → 7801–8036; 4 f tone
- 8676–8750 "During a normal chat…" under the same held frame (covers the photograph's last 8 frames and the box fade-in) → 8040–8114; 8750–9114 FROZEN WEIGHTS drawing live, build-up in sync → 8114–8478; pause 18
- cut g (9114→9285): "This graphic summarizes the entire development journey…" removed (the roll's close render cut 9124 inside it)
- 9285–9459 "AI learns from examples and feedback. Guess. Check. Adjust. Repeat." under the standard close → 8496–8670 (audio ends 315.30 source, after the final /t/ release and before the file's digital zeros at 315.48); settled hold 120 → 8790. Notebook's spinner (9469) never rendered.

**Board rects (measured on the JPGs):** Loop columns [65,236,552,790] / [556,236,1043,790] / [1047,236,1534,790] (tile x-extent ±16, tile top −16, shared text-bottom rail +16), banner [40,967,1560,1055]; Before cards [41,128,782,715] / [817,128,1558,715]; Three Phases question [40,112,1560,244], cards [40,272,530,558] / [555,272,1045,558] / [1070,272,1560,558]; phase sections x 74–1526 at rows Pre 165–467 / 499–664 / 696–861, Inst 165–412 / 444–650 / 682–847, Pref 165–412 / 444–691 / 723–888. Colors: Guess/Pretraining purple, Check/Instruction blue, Adjust teal (the board's chip is #0e8f86), Preference green, question card and banner neutral.
Judgment on the Loop board: its three columns share one white box with a caption row above and the REPEAT bracket below, so a full-height box ring (the Hallucination v10 rule) would slice the caption text at x≈547 and cross the bracket; the rings are component blocks around each column's tile, number, title and text instead. Easy to switch if David prefers the full-height rule.

**Checks (Edit Spec section 10):**
1. Decoded 8790 frames = plan; each leg decoded its span exactly (render_legs assert).
2. `transition_guard.py` passed all 24 declared boundaries; strips inspected at 873 (weights drawing → Loop board, destination from the first frame), 1934, 2513 (Before → Notebook's own blank-in of the bridge drawing), 2646 (hold start, seamless), 2809 (held drawing → Three Phases board), 3428, 4820, 6220 (board → board), 7093/7099/7213 (graft d: static answer section throughout), 7795/7801 (board → held FROZEN WEIGHTS frame), 8036/8040/8114 (hold → live drawing, seamless), 8478/8496 (drawing → close), 8670.
3. Pauses on the finished file (silencedetect −35 dB): 8.44–9.71 (1.27 s, plan ~1.26); 97.61–98.49 (0.88 s at −35 dB, plan ~1.04; the narrator's exhale tail after "phases." sits at −35 to −40 dB, so word-to-word the gap is ~1.05 s); 282.25–283.46 (1.21 s, plan ~1.22). Splice gaps at the grafts were filled with 6/6/4 frames of roll-1 room tone so each join keeps the roll's own ~0.6 s inter-sentence gap (the live's floor is ~6–8 dB quieter than roll 1's, so the donors are kept tight and the gap is roll-1 tone).
4. Ring states inspected (`states-*.jpg`): Loop column and banner rings, Before card rings, Three Phases question and card rings, and each phase section ring at its spoken onset; artwork-scaled stroke.
5. Density: Loop compact still; Before compact (2.6 % push); Three Phases compact still; the three phase boards dense with per-target camera arriving on each onset (the tall canvas clamps the camera, so sections 2 and 3 share a frame and only the ring moves). Every board opens whole and unmarked ≥ 2 s before its first ring (Loop 5.2 s, Before 4.9, Three Phases 4.2, Pre 3.9, Inst 3.3, Pref 2.9).
6. Corner mark: 1638 kept Notebook frames cloned, 186 inpainted, 0 declined. Kept spans sampled every 30 frames (`kept-notebook-spans.jpg`): no board renders, no diagrams beyond the two invented drawings the plan keeps. Frame 0 is the paper-craft molecule.
7. Transcript of the finished file (small.en): all five cut sentences gone, "study the ball", "architecture is locked", "deployed for everyday use" absent; "steady the ball" and the live "heavy lifting is done… packaged up and ready for public use" present; all eight verbatim lines exact ("Guess, check, adjust, repeat." confirmed on a close-clip pass with small.en and base.en; the whole-file pass dropped the isolated "Guess," as it did on the source roll); nothing after "Repeat."
8. Levels (volumedetect mean): graft d −16.7 dB against −18.5 before / −16.8 after; graft f −18.1 dB against −16.8 before / −17.8 after. Gains from an active-speech match to roll 1's neighbouring sentences (gaps excluded): d −0.57 dB, f −2.56 dB (raw sentence RMS would have given −0.31 / −3.40).

**Photographs and covers:** the paper-craft phone photograph (source 8468–8684) is inside cut e/f except its last 8 frames, which the held FROZEN WEIGHTS frame covers; the AI TRAINING CURRICULUM / TRANSFORMATION diagrams are inside cut e; the THREE CURRICULUM PHASES morph is under the bridge hold.
**Kept Notebook spans David may pull:** 0:00–0:06.2 of the output is the same photographed-paper-craft style as the covered phone (molecule, code monitor, highlighted essay; no people, no logos, they illustrate the chemistry/code/essay line and no drawing exists for it); 0:20–0:29 (output) Notebook's invented "Universal Training Loop" and "Internal Weights" drawings under "Instead of physical force…".
**Longest unbroken board run:** Three Phases → Pretraining → Instruction Tuning → Preference Tuning, output 2809–7789 (2:46.0). Roll 1 drew nothing between these boards (its renders cut straight into one another), so there is no Notebook scene to interleave without inventing filler. Boards 1–2 run 873–2513 (54.7 s).

**Not auditioned by ear (David):** the cut joins at 0:29.1 (into the Loop board), 0:58.3 (inside the Loop board), 1:33.6 (into Three Phases), the two pauses at 0:08.8 and 1:37.7, graft d at 3:56.4–4:00.4, graft f at 4:19.8–4:28.0 (both its joins), the join before the close at 4:43.2, and the close's last word. Transcript and level checks do not certify them.

**At ship (not authorized yet):** copy to `course-assets/training/training.mp4`, cache key `?v=20260922ship1` on `training` (currently 20260916ship1; if the Understand AI opener ships the same day, this becomes ship2), pill stays 5 min (4:53), manifest video_assets hash + bytes, then commit; David maintains the tracker.

## v6 (2026-09-22, same day): the banner read comes out

David, after watching v5: "we read the banner word-for-word at about 1:02 … the banner as written doesn't work as read
word-by-word … it might be easier to delete the word-by-word reading." `Prompts/training-v6.mp4` (4:49.87, 8696 frames,
sha256 01a8b51a707a59d6…) = v5 plus cut h: roll 1 66.07–69.20 ("Repeat with more examples. The patterns build."), out after
"example." (tail 65.85), in inside the 68.89–69.46 gap before "This illustration shows"; 0.44 s of natural gap remains. The
Loop board's banner ring goes with it; the Adjust ring now ends at "The loop runs again" (63.50) and the board sits unmarked
until Before Training Starts arrives. Script `scripts/video/build_training_v6.py`, folder `build-v6/`. Guard 24/24, decoded
8696 = plan, corner mark 0 declined, protected files unchanged; pauses unchanged (1.27 / ~1.05 / 1.21 s). Transcript across
the cut: "The loop runs again on the next example. This illustration shows what has to happen before that loop can even
begin." v5 stays in Prompts/ until David says which to keep. The banner line is removed from the prompt's verbatim list so a
future reroll does not read it either. Listen: 1:01.5 (cut h) plus the v5 list.
