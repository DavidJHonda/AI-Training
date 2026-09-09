# AI Is Math: two-roll evaluation

Recommendation: repair `Prompts/AI_is_Math__The_Secret_of_Conditional_Probability.mp4` (3:40.80). It has the stronger narration and the exact current closing. No reroll is needed if the removable claims below are cut and the visual errors replaced. Neither raw roll is ready to ship.

The other candidate is `Prompts/AI_is_Math.mp4` (4:11.73). These filenames identify the comparison; upload order does not establish version numbers.

## Evidence and scope

Narration intake and comparative visual review, not a finished-video ship certification. Read the current `lessons/ai-is-math.md` and matching `AIIsMathSection` in index.html. Read complete independent base.en and small.en transcripts for both candidates. Inspected all eleven four-second contact sheets, both scene/hold inventories, manually mapped teaching allocation, and additional adjacent frames for apparent animation defects and endings. ASR confirms wording; this report does not claim a complete human listening pass. Original videos and live course were not modified. Source hashes are in sources.json.

Current boards: `ai-is-math-the-math-editorial.jpg`, `ai-is-math-two-coins-editorial.jpg`, `ai-is-math-conditional-probability-editorial.jpg`, and `ai-is-math-what-comes-next-editorial.jpg`, all in lessons/. Reviewed the actual assets. Both rolls use them, but alter framing and add Notebook emphasis.

## Why the Conditional Probability version wins

- 0:43–0:59: states the equally-likely condition before explaining the counting formula.
- 1:07–1:39: explicitly enumerates HH, HT, TH, TT and explains why one of four gives 25%.
- 1:40–2:33: identifies the FIRST coin as heads, eliminates TH and TT, counts the two surviving possibilities, calculates 50%, and distinguishes changed knowledge from unchanged coins. This preserves the important distinction between “first coin heads” and merely “at least one heads.”
- 2:50–3:14: uses the approved dog question, the unfinished reply, and Spot 22%, Max 17%, Buddy 14% to explain conditional next-word prediction.
- 3:24–3:33: teaches the recursive connection: the chosen word joins the text and becomes evidence for the next prediction.
- 3:33–3:38: speaks the exact closing: “AI builds answers with probabilities. One prediction at a time.”

It is more direct and less abstract. Its shorter runtime does not cost any central teaching. In particular, its enumeration of the four coin outcomes is more explicit than the longer candidate's.

## Narration edits for the recommended version

Times are approximate source ranges, not frame-accurate edit instructions.

1. **0:59–1:07:** remove “This single ratio is the bedrock for predicting anything from a simple dice roll to a complex sequence of text.” The counting formula just introduced requires equally likely outcomes; connecting that exact ratio to text generation invites the wrong conclusion that AI obtains its word probabilities by counting equally likely words. The preceding explanation joins naturally to “Consider a basic scenario.”
2. **3:14–3:24:** remove the sentence describing the remaining 47% as other potential names “in the model's database.” The remainder includes possible next tokens, not exclusively names, and “database” suggests retrieval. The three example percentages remain spoken; the current board preserves the remaining-47% explanation visually. Then proceed directly to “Once a word is chosen…” If full spoken coverage of the remainder is desired, the other roll has a usable sentence at about 3:42–3:47, but a donor splice is unnecessary for the core lesson.
3. **Optional, 2:42–2:50:** remove the second coin-to-prompt comparison (“Every word you type … narrows down the possibilities…”). The preceding probability-update explanation and following dog example already teach the connection more precisely. It is less problematic than the other roll's explicit elimination claims, but expendable.

No extra narration is needed. Add one-second pauses between major ideas and before the closing. Preserve useful Notebook scenes around the boards.

## Visual repairs for the recommended version

- Restore complete current boards during their teaching spans: approximately 0:44–0:59, 1:07–1:32, 2:03–2:24, and 2:50–3:24. Replace temporary Notebook shading/arrows with the standard outline-only treatment. Retain the scenario and all relevant outcomes together.
- **2:24–2:33:** replace the generated four-panel animation. Adjacent frames at 2:31, 2:32.5 and 2:33 confirm that the fraction becomes 1/2 while the displayed percentage remains 25%. This is a real visual contradiction, not a sampled transition. Keep the current clue board visible or make a correct visual for the unchanged-coins/changed-knowledge explanation.
- **2:33–2:42:** the generated display appends Spot to the input while the same name probabilities remain. Repair the probability/context relationship before keeping this animation.
- **2:42–2:50:** replace the generated elimination/coin replay if retaining its narration. It adds a France example and displays 1/4 (25%) labels after evidence, muddying the bridge. An optional narration cut also removes this visual detour.
- **3:24–3:33:** the prediction-loop animation is useful, but inspect/correct its final state: the displayed context gains a period while the next-token list still offers punctuation from the preceding state. Preserve the useful progression where possible.
- Some apparently overlapping titles at 0:40 are an ordinary dissolve; adjacent 0:39, 0:41 and 0:42 frames resolve it. No static-collision deduction.
- Insert the exact standard closing board over the closing narration, retain a settled hold, and remove the Notebook outro after 3:37.8. Follow the established treatment for engine marks during repair.

## Why the longer AI_is_Math version is weaker

It still explains the coin calculation and knowledge change well (1:30–2:43), has the correct dog percentages (3:36–3:47), and teaches the repeating prediction loop (3:47–4:00). It is viable backup material.

However, it adds several avoidable problems:

- **1:21–1:27:** calls simple counting the building block for “all predictive math,” repeating the formula-overreach problem.
- **1:56–1:58:** calls the calculated 25% a “completely blind guess,” an unhelpful characterization after teaching the calculation.
- **3:02–3:24:** explicitly says context eliminates unlikely words and rules out unrelated dictionary words. This takes the coin analogy too literally. It is the more serious narration weakness, and the associated visuals reinforce it with crossed-out words.
- **4:00–4:09:** ends with “probabilistic tabulations” instead of the approved plain-language closing. The exact first closing line is missing.
- **3:47–4:00:** generated reply becomes “You could name him Spot is a…”; its diagram labels probability as outcomes divided by total vocabulary. Both are replaceable visual errors, but they compound the narration's misleading counting/filtering model.

## Accuracy basis and disposition

The lesson's central source teaching is sound: classical counting is explicitly limited to equally likely outcomes; the first-coin evidence produces 1/2; prompt and prior output condition subsequent predictions. Whole words are an intentional introductory simplification before the Tokens lesson.

For the AI connection, Hugging Face's official text-generation guide describes generating the next token from a prompt together with prior generated outputs, and distinguishes generation controls from the model's distribution: https://huggingface.co/docs/transformers/llm_tutorial . This supports the lesson's conditioning explanation, not literal elimination of every unlikely word or retrieval from a names database.

Narration verdict: **keep and repair the Conditional Probability candidate**. Coverage survives the two required cuts. Finished-video accuracy, board walk, sync, ending, and edit-integrity gates must be checked after repair; current raw visual errors mean no ship approval is implied by this selection.

## Correction following original-visual restoration

The recommendation to repair the 2:33–2:42 animation because its probabilities did not update after Spot was based on an intermediate frame. Further inspection confirms that the animation updates to continuation probabilities: period 38%, and 26%, comma 19%, other 17%. That specific concern is withdrawn. See ai-is-math-original-visuals-2026-09-09/frame-4750.jpg. The separate coin animation error (1/2 displayed beside 25%) remains confirmed.
