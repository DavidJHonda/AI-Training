# How an LLM Works — comparison of the two-part generations

Recommendation: **REPAIR using how-the-model-learns-1 as Part 1 and how-the-model-answers-2 as Part 2, with two short additions from their alternate versions. No further reroll is needed on the evidence available.** This is a narration/edit recommendation, not a shipping certification. Voice continuity remains unauditioned.

The split has improved the explanatory structure. The training example now gets a sustained explanation: an example supplies a target, a guess is compared with it, internal numbers change, and repetition produces patterns. The answering section follows context → probabilities → selection → updated context. This addresses the earlier v9 problem more directly than changing pictures or inserting pauses. Some formal wording remains, but the selected versions preserve a comprehensible chain of cause and effect.

## Scope and evidence

Evaluation and a proposed production plan only. No source video, live lesson, canonical board, existing candidate, or deployed file was changed. The full course closing message applies to Part 2; Part 1 is assessed against its approved handoff, not penalized for lacking the final close. The omission of the early four-concept overview is intentional and previously agreed.

Read the current `AIHistorySection` in `index.html`, `lessons/how-an-llm-works.md`, both split-source Markdown files, and the shared video review/edit instructions. Reviewed all four complete base.en timestamped transcripts, all 18 contact sheets (samples every four seconds), and all six canonical JPGs used by this kit. Used small.en for independent checks of uncertain words, proposed donors, and opening/closing passages. Inspected measured low-level audio gaps around the two recommended additions and the part boundary.

**Listening limitation:** no audio was literally auditioned, and no video was watched in continuous real-time playback. ASR agreement and waveform gaps are not listening. Pronunciation, prosody, voice identity, perceived pace, and actual splice quality remain unverified. These are raw generations, not a finished joined candidate. The full tracker was not accessed; no workflow status is inferred from it.

ASR corrections: learns-2's guessed word at about 1:11 is rendered “Claude” by base.en but “cloud” by small.en; do not label this a confirmed spoken error. In answers-2 at 0:26, small.en identifies “Answering a prompt,” not base.en's “Comparing a prompt.” “Four” in the prediction examples is the recognizer's homophone spelling of “for,” not evidence of a wrong number. Full-length base.en timestamps are approximate; targeted word-level checks and measured gaps supersede them for proposed cuts.

| File in Prompts | Duration | Format | SHA-256 |
|---|---:|---|---|
| how-the-model-learns-1.mp4 | 2:51.70 | 1280×720, 30 fps | `09da1a9e263bc5fa8890caea3374c1df27f99d63459fcf38bdbc818b03d5a9b1` |
| how-the-model-learns-2.mp4 | 3:04.43 | 1280×720, 30 fps | `d621adc32f86a9a0e5ebdcd531fc438bdd5972202724378d49070919cf57b262` |
| how-the-model-answers-1.mp4 | 3:50.03 | 1280×720, 30 fps | `b1d9ba5a486b021f231ff2ca6cdcf8fe1e446ca56991595a889ace02a6eb3984` |
| how-the-model-answers-2.mp4 | 3:21.17 | 1280×720, 30 fps | `f2c38a594b458759a73fb2f2e425993ef7f2dcd11e1dd2d87420aba730497279` |

## Narration verdicts

### LESSON: how-an-llm-works / learning section

**CANDIDATE: how-the-model-learns-1.mp4 (2:51.70)**

**VERDICT: REPAIR.** It teaches the mechanism clearly enough to use as the base, but never says the full term Large Language Model.

TEACHING POINTS:

- Hook/learning before use — TAUGHT, 0:00–0:08: asks how jelly fits before a user prompts it, then answers “It learns from examples.”
- App versus engine — TAUGHT, 0:13.50–0:17.50: “ChatGPT is the app. The LLM is the engine.”
- Large, Language, Model — TAUGHT, 0:17.50–0:38: scale and extensive text/code, all five language functions, numerical prediction. Full expansion of LLM is MISSING.
- Read and guess — RICH, 0:50.50–1:13.50: target already included, prompt fragment, wrong guess cloud, prediction rather than fact lookup.
- Check and adjust — RICH, 1:13.50–1:37: compares with jelly, changes internal numbers, makes jelly more likely in that situation.
- Repetition — RICH, 1:37–1:55: one correction is insufficient; repeats the complete cycle over billions of examples.
- Familiar patterns — RICH, 1:55–2:18: jelly, star, time, never all supplied.
- Broader patterns — TAUGHT, 2:18–2:31: explanations, logical problem solving, misspellings. “Asking questions” is not separately named, but the generalization beyond stock phrases is taught.
- Training/pattern relationship — RICH, 2:31–2:42: explicitly rejects a separate later pattern-learning step.
- Handoff — TAUGHT, approximately 2:42–2:48.34 in the targeted check: learned patterns → use them to build an answer.

HARD REQUIREMENTS: app/engine line MET; full Large Language Model term MISSED; approved handoff words MET. Final course close not required in this part.

ERRORS: no confirmed substantive incorrect teaching identified; missing expansion requires repair. The causal explanation “It makes this error because it is calculating a prediction rather than looking up a fact” is compressed, but the following comparison/correction supplies the actual teaching.

SOURCE_QA: PASS for the intended beginner model; approved sources contain the full term that this generation omitted. The board's training-data description of Large is shorthand; this roll's “refers to scale” avoids making corpus size the sole definition.

ADDITIONS: useful explanation of prediction versus fact lookup. No additional technical material needed.

REPAIR PLAN: insert learns-2 0:19.65–0:24.15 at learns-1 0:17.55; complete sentence and measured boundary details below.

EDITING NOTES: extensive re-rendered, cropped, and duplicated board text requires canonical-board replacement. The narration itself does not need to be reorganized.

LISTENING: transcript/targeted ASR only; literal listening outstanding.

### LESSON: how-an-llm-works / learning section

**CANDIDATE: how-the-model-learns-2.mp4 (3:04.43)**

**VERDICT: REPAIR.** Usable as a donor, but the first version is the better base. This version introduces unnecessary technical language and an overstatement about every update improving the model.

TEACHING POINTS:

- Hook and learning before use — TAUGHT, 0:00–0:09.76.
- App/engine and full term — TAUGHT, 0:09.76–0:24.24; full term is present at approximately 0:20.02–0:23.76.
- Large, Language, Model — TAUGHT with wording concern for Large, 0:24.24–0:43.12. “Called large because they are trained on huge amounts” is less precise than learns-1's scale wording.
- Read, guess, check, adjust — RICH, 0:48.72–1:31.36. The fragment after “known answer” is incomplete, but the surrounding narration explicitly states that the example contains the target and later supplies jelly. The uncertain cloud/Claude transcription is not a verified error.
- Repetition and small changes — RICH, 1:31.36–1:51.24: no hard-coded rulebook; one correction makes a small change; move to the next example.
- Familiar patterns — RICH, 2:02.12–2:25.60: jelly, star, time, never.
- Broader patterns — TAUGHT, 2:25.60–2:43.32: communication, arguments, code, explanation. It loses the source's misspelling example, which learns-1 retains.
- Patterns arise through changed numbers — TAUGHT, but contains WRONG overgeneralization at approximately 2:46.84–2:50.58: “With every adjustment, the internal map of language becomes more precise.”
- Handoff — TAUGHT, 2:54.72–3:01.52.

HARD REQUIREMENTS: full term MET; app/engine line MET; handoff MET.

ERRORS: the “every adjustment” promise is too strong. Training can have noisy steps with increased loss, so individual updates do not guarantee overall improvement. This correction is supported by [Google's explanation of noisy stochastic-gradient training](https://developers.google.com/machine-learning/crash-course/linear-regression/hyperparameters). “Brute force repetition” at 1:56.20–2:02.12 is also a less helpful explanation than the already-described directed adjustments.

SOURCE_QA: PASS for the approved split source; it does not claim improvement at every update. The stronger Large wording and guaranteed-improvement wording are generation additions.

ADDITIONS: the small-change explanation is useful, but does not warrant replacing learns-1's already complete repetition beat. Program syntax and “math stabilizes” increase abstraction without helping the peanut-butter explanation.

REPAIR PLAN if this alternate were chosen: replace 0:24.24–0:29.40 with learns-1 0:17.50–0:25.50 (scale and extensive training data); replace 2:25.60–2:54.72 with learns-1 2:18–2:42 (broader patterns and the explicit training relationship). Both are complete runs of sentences. These alternate-plan ranges are semantic selection ranges, not measured final splice frames. They are not proposed for the preferred assembly.

EDITING NOTES: strong app/engine drawings and a possible handoff drawing. Other scenes introduce weights, invented training counts and 96% prediction confidence, matrix labels, and decorative diagrams. Do not treat those as required teaching.

LISTENING: targeted secondary ASR on full-term, wrong-guess, and “every adjustment” passages; literal listening outstanding.

### LESSON: how-an-llm-works / answering section

**CANDIDATE: how-the-model-answers-1.mp4 (3:50.03)**

**VERDICT: REPAIR.** The explanation is substantive and has a useful qualifier, but its second probability example omits toast at 9%.

TEACHING POINTS:

- Uses trained patterns; generates incrementally — RICH, 0:02.64–0:22.80.
- Word/token distinction — TAUGHT, 0:22.80–0:33.60.
- Calculate possibilities, choose, continue — TAUGHT, 0:33.60–0:44.
- First full prompt and values — RICH, 0:44–1:00.80: jelly 41, bread 27, bananas 16, honey 5 percent.
- Illustrative values — TAUGHT, 1:00.80–1:09.28. Remaining probability assigned to other words is MISSING.
- Most likely is not compulsory — TAUGHT, 1:09.28–1:20.08.
- Second prompt and values — THIN/incomplete, 1:20.08–1:34.24: sandwich 54, smoothie 16, jelly 2; toast 9 is MISSING.
- Why context changes odds — RICH, 1:34.24–2:09.04: explicitly compares 41 with 2 and explains why banana makes sandwich a better fit.
- Phone analogy — TAUGHT, 2:09.76–2:24.16.
- Growing sentence and recalculation — RICH, 2:24.80–3:04.32: jelly → for → lunch, with updated text explained at each stage.
- Paragraph-scale repetition, training versus answering, close — TAUGHT, 3:04.88–3:46.88. The core idea is complete; “hundreds of times” and hardware wording are unnecessary elaborations.

HARD REQUIREMENTS: both closing lines MET; all worked-example values MISSED (toast 9%).

ERRORS: omissions rather than contradictory spoken values. Neither the chart nor a subtitle can supply the missing spoken value.

SOURCE_QA: PASS; both omitted items are explicit in the Part 2 source.

ADDITIONS: explicit non-greedy choice is useful. The long technical restatement after the worked example is less direct than answers-2.

REPAIR PLAN if chosen: replace 1:20.08–1:34.24 with answers-2 1:04.28–1:25.48, the complete new-context/example beat including toast. Insert answers-2 0:48.68–0:53.64 (“The remaining probability is split among all other possible words to reach 100%”) after the first table. Alternate-plan timing is a semantic selection, not final measured cuts. Preferred assembly instead uses answers-2 and borrows only this roll's qualifier.

EDITING NOTES: several generated charts invent extra values, and the 41-to-2 chart labels the change “−39%” rather than 39 percentage points. Do not reuse those charts. Close appears too early, leaves, and returns; replace with the single final course close.

LISTENING: secondary ASR confirms omission of toast in 1:20–1:35 and the qualifier's wording; literal listening outstanding.

### LESSON: how-an-llm-works / answering section

**CANDIDATE: how-the-model-answers-2.mp4 (3:21.17)**

**VERDICT: REPAIR.** Best answering base. The full example and its causal explanation are intact; restore the source's essential qualification that the percentages are illustrative.

TEACHING POINTS:

- Uses trained patterns; builds incrementally — RICH, 0:00–0:17.04.
- Word/token distinction — TAUGHT, 0:17.04–0:26.20.
- First prompt and values — RICH, 0:33–0:48.68: jelly 41, bread 27, bananas 16, honey 5 percent.
- Remaining probability — TAUGHT, 0:48.68–0:53.64.
- Most likely is not compulsory — TAUGHT, 0:53.64–1:04.28.
- Illustrative values — MISSING; “Let's look at the exact numbers” is unqualified in the current narration.
- Second prompt and all values — RICH, 1:04.28–1:25.48: sandwich 54, smoothie 16, toast 9, jelly 2 percent.
- Context changes the odds — RICH, 1:25.48–1:41.36: explains the changed subject and explicitly compares jelly at 41 and 2 percent.
- Phone analogy — TAUGHT, 1:48.44–2:02.80.
- Growing sentence — RICH, 2:02.80–2:38: jelly → for → lunch; final context is shortened to “and jelly for,” but it follows the already spoken full sentence and preserves the mechanism.
- Repeated loop and why it looks thought-like — TAUGHT, 2:38–2:57.28.
- Training versus answering and conclusion — TAUGHT, 2:57.28–3:18. Both closing lines present; targeted ASR puts their actual speech at about 3:11.76–3:17.90.

HARD REQUIREMENTS: every listed value MET; both closing lines MET; illustrative-value qualifier MISSED.

ERRORS: no confirmed wrong number; missing qualifier needs repair. “Primary variables that dynamically dictate” at 1:41–1:48 is unnecessarily formal, but the preceding concrete explanation already teaches the point.

SOURCE_QA: PASS; the qualification is present in the supplied Markdown and prompt.

ADDITIONS: “not a forced choice” is a useful explanation of possible continuations.

REPAIR PLAN: insert answers-1 1:00.65–1:09.15 at answers-2 0:48.40, after honey's percentage and before the remaining-probability sentence. Complete words and measured gaps below.

EDITING NOTES: the generated boards contain repeated/malformed text, cropped cards, and unwanted fills/arrows. Canonical replacements needed. Preserve the useful loop concept while excluding unspoken or misleading labels such as “FLUID THOUGHT EMERGENCE.”

LISTENING: targeted secondary ASR on the opening, “Answering a prompt,” and final close; literal listening outstanding.

## BEST-OF PLAN: learning

BASE: **how-the-model-learns-1.mp4**. It explicitly connects the results to the training process and covers the source's broader-pattern examples with less technical excess. RICH/TAUGHT are teaching judgments from text, not voice-quality judgments.

| Teaching point | Learns 1 evidence | Learns 2 evidence | Selection |
|---|---|---|---|
| Learning before use | TAUGHT, 0:00–0:08, “before a user ever prompts it… It learns from examples.” | TAUGHT, 0:00–0:09.76, “It learns this from examples long before a user ever prompts it.” | Keep 1; both establish the right question. |
| App / engine | TAUGHT, 0:13.50–0:17.50, “ChatGPT is the app. The LLM is the engine.” | TAUGHT, 0:15.74–0:19.70, same line, with app examples beforehand. | Keep 1. |
| Full term | MISSING; only “LLM” | TAUGHT, 0:19.70–0:24.24, “Under the hood, a large language model, or LLM, does the work.” | **Take 2, under the LLM board.** |
| Large | TAUGHT, 0:17.50–0:25.50, “refers to scale… massive amounts of text and computer code.” | TAUGHT with wording concern, 0:24.24–0:29.40, “called large because… huge amounts of text and code.” | Keep 1's more careful scale wording. |
| Language and Model | TAUGHT, 0:25.50–0:38, “reading, writing, summarizing, translating, and explaining… learned numerical patterns.” | TAUGHT, 0:29.56–0:43.12, “read, write, summarize, translate, and explain… learned numerical patterns.” | Keep 1; equivalent coverage. |
| Target and wrong guess | RICH, 0:50.50–1:13.50, “correct answer is already included… guesses cloud.” | RICH, 0:48.72–1:13.40, “already contain the correct answers… might guess cloud.” | Keep 1; clearer complete setup. |
| Compare and adjust | RICH, 1:13.50–1:37, “compares that incorrect guess against… jelly… changes its internal numbers.” | RICH, 1:13.40–1:31.36, “compares its guess… jelly… alters… numerical weights.” | Keep 1's plain “internal numbers.” |
| Repeat | RICH, 1:37–1:55, “One correction doesn't teach the model everything… across billions of different examples.” | RICH, 1:31.36–1:51.24, “One adjustment only makes a slight change… moves to the next example.” | Keep 1. Roll 2 adds a useful small-change detail, but 1 already explains why repetition is necessary; no extra graft. |
| Familiar completions | RICH, 2:00–2:18, “jelly… star… time… never.” | RICH, 2:06.20–2:25.60, “jelly… star… time… never.” | Keep 1. |
| Broader patterns | TAUGHT, 2:18–2:31, “explain ideas, solve logical problems, and even… misspell words.” | TAUGHT, 2:25.60–2:43.32, “build arguments, write code, or explain ideas.” | Keep 1; retains misspellings and avoids a coding detour. |
| Patterns during training | RICH, 2:31–2:42, “not a separate step that happens after training is over.” | TAUGHT with WRONG overgeneralization, 2:43.32–2:54.72, “With every adjustment… more precise.” | Keep 1. |
| Handoff | TAUGHT, final spoken sentences, “Training has built patterns… Now let's see…” | TAUGHT, 2:54.72–3:01.52, same handoff. | Keep 1. |

GRAFTS: one complete sentence, under a canonical board.

## BEST-OF PLAN: answering

BASE: **how-the-model-answers-2.mp4**. Both context examples retain every number; explanation of updating the input is intact; recap is more direct.

| Teaching point | Answers 1 evidence | Answers 2 evidence | Selection |
|---|---|---|---|
| Use trained patterns | RICH, 0:02.64–0:22.80, “patterns it learned during training… one single piece at a time.” | RICH, 0:00–0:17.04, “patterns… learned during training… one piece at a time.” | Keep 2's direct handoff. |
| Tokens versus words | TAUGHT, 0:22.80–0:33.60, “tokens… full words or… fragments of words.” | TAUGHT, 0:17.04–0:26.20, same distinction. | Keep 2. |
| Score then choose | TAUGHT, 0:33.60–0:44, “first calculating the odds… then choosing one.” | TAUGHT across 0:33–1:04.28 and 2:08–2:12, “calculates… not a forced choice… adds… jelly.” | Keep 2; concrete sequence teaches the connection. |
| First example | RICH, 0:44–1:00.80, “jelly at 41%, bread at 27%, bananas at 16%, and honey at 5%.” | RICH, 0:33–0:48.68, same sentence and values. | Keep 2. |
| Probability beyond listed choices | MISSING; goes directly from values to qualifier. | TAUGHT, 0:48.68–0:53.64, “remaining probability… all other possible words… 100%.” | Keep 2. |
| Illustrative values | TAUGHT, 1:00.80–1:09.28, “illustrative examples… aren't fixed mathematical constants.” | MISSING; “exact numbers” at 0:30.84–0:32.04 is unqualified. | **Take 1, under the probability board.** |
| Choice need not be top option | TAUGHT, 1:09.28–1:20.08, “doesn't always automatically select the number one option.” | TAUGHT, 0:53.64–1:04.28, “not a forced choice.” | Keep 2; adequate and brief. |
| Second example | THIN/incomplete, 1:20.08–1:34.24, “sandwich… 54%, smoothie… 16%, and jelly… 2%.” | RICH, 1:04.28–1:25.48, adds “toast 9%” in the complete run. | Keep 2. |
| Why context changes odds | RICH, 1:34.24–1:55.44, “41%… 2%… item made with peanut butter and banana together.” | RICH, 1:25.48–1:41.36, “something made with peanut butter and banana… 41%… 2%.” | Keep 2; both supply the reason. |
| Phone analogy | TAUGHT, 2:13.28–2:24.16, “suggests a word, you tap it… next.” | TAUGHT, 1:48.44–2:02.80, same analogy and automatic continuation. | Keep 2. |
| Growing sentence | RICH, 2:24.80–3:04.32, “updated string… jelly… for… lunch.” | RICH, 2:02.80–2:38, “entire updated string… each chosen word… input.” | Keep 2; the shorter last-context quote does not lose the mechanism. |
| Paragraph and training link | TAUGHT, 3:04.88–3:39.76, “loop hundreds of times… modern hardware… strictly separate step.” | TAUGHT, 2:38–3:12.04, “many times… training changes the internal numbers… answering uses… patterns.” | Keep 2's clearer summary. |
| Close | TAUGHT, 3:40.40–3:46.88, both exact lines. | TAUGHT, approximately 3:11.76–3:17.90, both exact lines. | Keep 2. |

GRAFTS: one coherent two-sentence beat, under a canonical board. Total selected-plan grafts: two.

## Proposed exact narration changes

These are proposals for the next build. They do not authorize publication and have not been applied. The cut positions below lie in measured gaps; final splice sound still requires auditioning.

1. **Learning: expand LLM.** At learns-1 **0:17.55**, after “The LLM is the engine,” insert learns-2 **0:19.65–0:24.15**:

   > Under the hood, a large language model, or LLM, does the work.

   Resume learns-1 at 0:17.55 with “The large part of that engine refers to scale.” This is a whole sentence, not a synthetic word splice. Hold the current LLM board over it. A source-only listening excerpt is saved as `donor-llm-expansion.wav` beside this review; it is not an assembled join.

2. **Answering: qualify the numbers.** At answers-2 **0:48.40**, after “honey 5%,” insert answers-1 **1:00.65–1:09.15**:

   > Keep in mind, these percentages are illustrative examples to show how the concept works. They aren't fixed mathematical constants shared by every AI model.

   Resume answers-2 at 0:48.40 with “The remaining probability is split among all other possible words to reach 100%.” Keep the probability board visible; do not bring along the donor's unrelated extra chart. A source-only listening excerpt is saved as `donor-illustrative-values.wav`; it is not an assembled join.

3. **Join the parts.** Keep learns-1 through **2:48.70**, after its complete “Now let's see how the model uses those patterns to build an answer.” This removes only its remaining silent tail, not narration. Then start answers-2 at 0:00 with its existing leading gap and “Suppose you type…” Do not add a welcome, recap, map, or intermediate closing card. The final close comes only from answers-2.

Expected joined runtime is roughly **6:23 plus any required final close settle**, based on current durations, the 13 seconds of donor audio, and trimming the learning tail. A final frame count is a build output, not yet verified.

### Measured gaps and selective pauses

Using −35 dB and a 0.12-second minimum for boundary diagnosis:

| Location | Existing measured low-level interval | Proposed treatment |
|---|---|---|
| Learns-1 insertion | 0:17.357–0:17.782, about 0.425 s | Split at 17.55; preserve surrounding room tone. |
| Learns-2 donor entrance | 0:19.335–0:19.912 | Start at 19.65, before the complete sentence. |
| Learns-2 donor exit | 0:23.839–0:24.504 | End at 24.15, after the complete sentence. |
| Answers-2 insertion | 0:48.189–0:48.620, about 0.431 s | Split at 48.40. |
| Answers-1 donor entrance | 1:00.364–1:00.942 | Start at 60.65. |
| Answers-1 donor exit | 1:08.918–1:09.383 | End at 69.15. |
| Part boundary | Learns-1 speech ends into low level at 2:48.430; answers-2 begins with 0.301 s low level | Keep learns-1 to 168.70 and answers-2 from 0; combined gap about 0.571 s. |

No added teaching pause is proposed. With the selected donor margins, the two learning joins have approximately 0.46/0.54-second total gaps and the two answering joins approximately 0.50/0.45-second gaps. These are measured construction estimates, not a judgment of how the transition sounds. There is no automatic one-second rule. No pacing conclusion is being made from elapsed seconds alone.

## Visual and production proposal

Scope: a future full production pass using the new pair. The exact current JPGs remain authoritative. Keep the coherent example visible as it develops; do not cycle back to the four-concept map or insert unrelated drawings simply to make another cut. Board changes follow teaching changes, and highlights follow the spoken sections.

| Board | Highlighting sequence | Camera | Reason / exception |
|---|---|---|---|
| What's an LLM? (`how-an-llm-works-llm.jpg`) | Full view, app/engine banner as spoken, unmarked full board during expansion donor, then whole Large → Language → Model cards | Compact; full board throughout | Simple definitions, no need to crop or dive. |
| How Training Works (`how-an-llm-works-training.jpg`) | Full view; Read → Guess → Check → Adjust as meaningful complete sections; return unmarked for overall repetition | Compact; full board | All four steps remain spatially related. Rings include illustration, label and explanation, not just a keyword. |
| How AI Learns Patterns (`how-an-llm-works-patterns.jpg`) | Whole One Familiar Pattern card → whole Patterns Are Everywhere card; do not create a new ring for every nursery phrase | Compact; full board | Each card supports one idea. Broader-pattern explanation can remain on an unmarked full view. |
| Same Word. Different Odds. (`how-an-llm-works-same-word-different-odds.jpg`) | Full view first; introduce whole left card, then prompt section as the sentence is read, then probability table as the choices are explained; same sequence on right; pull back for the explicit jelly 41%/2% comparison; banner | Dense; full view → complete left card → complete right card → full comparison | Keep every active card complete. The donor qualification stays under this board. No separate row-level ring for each number. |
| One Word at a Time (`how-an-llm-works-one-word-at-a-time.jpg`) | Full view; whole first → second → third cards as the sentence grows; full-width takeaway banner | Compact; full board | The accumulation of text is the mechanism; don't hide the previous step with a tight crop. |
| Close (`how-an-llm-works-close.jpg`) | Unmarked canonical close, only at the final two lines | Standard 48-frame hold, 150-frame push to 1.2×, settled final hold at 30 fps | Only one course close in the joined lesson. |

The overview board is omitted per the accepted two-part plan. Component bounds and spoken onsets will be finalized against the assembled narration. All outlines follow the constant 5 px specification and use card accents.

Useful drawing candidates, with source times provisional until exact retained frame boundaries are inspected during preparation:

- Learns-1 opening, 0:00–0:08.47: peanut-butter setup.
- Learns-1, 0:42.17–0:50.73: read/guess/check/adjust loop. Keep in place; consider reusing it during the repetition explanation around 1:37–1:46 to break the long board run without changing the example.
- Learns-2 handoff drawing, roughly 2:54.7–3:01.5: model's internal patterns then application input. Potential cover for learns-1's handoff, with audio still from learns-1. Exclude the Notebook end card. Exact visible labels need a full-resolution check before retaining.
- Answers-1 at about 0:20: incremental pieces; at about 0:28: whole words versus word fragments. These can support answers-2 0:12.8–0:26.2. The 0:28 state is useful; exclude later fabricated token IDs. No extra spoken example is needed.
- Answers-2, about 2:37.87–2:57.17: generation loop. Useful mechanism, but the later “FLUID THOUGHT EMERGENCE” label must be excluded or covered; do not imply that actual thought has been demonstrated.
- Answers-2, about 2:57.17–3:11.63: training/answering distinction drawings, subject to legibility and boundary checks.

**Longest board runs:** replacing the chosen raw board scenes without any other treatment would leave about 118 seconds of continuous training/patterns boards in learns-1 and about 101 seconds of probability board in answers-2. The proposed repetition-loop and handoff drawings reduce the learning runs to approximately 56 seconds or less. Using the short incremental/token scenes early in Part 2 still leaves about **84 seconds** for the continuous probability explanation after the qualifier graft.

**Proposed exception for owner review:** keep that probability comparison together, despite the usual roughly-60-second board-run trigger. The source offers no verified, directly useful drawing in its middle; the alternate's charts introduce different values and would weaken the example. Full view/complete-card camera changes and spoken highlights can guide attention while preserving the same comparison. Do not treat the exception as approved yet. This is preferable as a proposal to padding the explanation with unrelated visuals.

Production defects observed separately from narration:

- All four rolls re-render course boards, with clipped edges, shifting or duplicated words, stray highlights, and partial-card views. For example, answers-2 around 2:12–2:28 duplicates and corrupts the growing sentence. These are replaceable picture defects, not reasons to discard its narration.
- Learns-2 introduces a purported 10-billion training-cycle count and 96% confidence picture around 1:52–2:00. These are not source facts; exclude them.
- Answers-1 around 1:04–1:20 and 1:48–2:08 introduces new percentages and unrelated contexts; exclude these donor pictures. Its 41-to-2 comparison around 1:36–1:44 labels the difference as −39%, which confuses percent with percentage points.
- Answers-2's “SHAPING THE ODDS” card at approximately 1:41–1:48 adds a title rather than an explanation. The existing probability comparison can carry that sentence more coherently.
- Notebook marks and final logo cards are visible. Apply the shared production treatment to retained scenes and end only on the canonical course close.
- No standalone stock photograph was identified in the four-second samples. This is not a frame-by-frame photo clearance; course-board imagery is a separate approved asset category.

## Reproduction and next step

The full review bundles are adjacent to this file, one directory per source. Each contains its complete timestamped transcript, scene estimates, holds, and all contact sheets.

Commands used:

```sh
.video-venv/bin/python scripts/video/grade_bundle.py video-audit/how-an-llm-works-split-comparison-2026-09-17 Prompts/how-the-model-learns-1.mp4 Prompts/how-the-model-learns-2.mp4
.video-venv/bin/python scripts/video/grade_bundle.py video-audit/how-an-llm-works-split-comparison-2026-09-17 Prompts/how-the-model-answers-1.mp4 Prompts/how-the-model-answers-2.mp4
```

Secondary checks used cached faster-whisper small.en with `beam_size=5`, word timestamps, and targeted clips. Boundary measurements decoded the original MP4 audio with ffmpeg `silencedetect=noise=-35dB:d=0.12`. The runtime warnings emitted by Whisper's feature extractor did not prevent transcription; uncertain words were rechecked and are disclosed above. Automatic scene counts include motion-induced detections and are not literal editorial cut counts.

Next step is approval of this concrete two-addition plan and its long-probability-board exception, followed by a new review build from the pristine sources. The reviewed pair is approximately 6:23 before final close timing; it has not been assembled. The two donor joins and the learning-to-answering boundary require literal listening, and the eventual finished video requires the full end-to-end watch/listen check before shipping.
