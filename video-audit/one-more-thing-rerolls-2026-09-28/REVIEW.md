# One More Thing — three rerolls, 2026-09-28

## Recommendation and verification limits

**Editorial choice: roll 1 as the base; roll 2 for the math-board explanation. Roll 3 is not the base.** This is a conditional edit recommendation, not a KEEP or shipping certification. No video or lesson was changed during this review.

Read the current page, upload Markdown, prompt, shared workflow, Narration Review and relevant Edit Spec sections. Read all three complete fresh transcripts and inspected all 17 four-second contact sheets. A second small.en transcription checked roll 1's divergence/math/close, roll 2's temperature explanation and roll 3's 100-tries explanation/close. These are ASR and sampled-picture findings, **not direct listening or continuous playback**. Voice quality, pronunciation and proposed audio joins remain unauditioned. ASR boundaries are planning ranges, not frame-accurate edit points; roll 2's final base.en segment extends past the file duration and must not be used as an out-point.

Fresh source SHA-256, lengths and frame counts are in `sources.json`. These newly uploaded numbered files are different generations from the same filenames mentioned in September 22–23 records; those old reviews do not apply.

| File | Runtime | Editorial use |
|---|---:|---|
| `Prompts/one-more-thing-1.mp4` | 3:16.03 | Strongest base: complete probability example and fullest useful temperature comparison; compressed math ending. |
| `Prompts/one-more-thing-2.mp4` | 3:12.40 | Best math donor: explicit multiplication and generated-token qualifier. Earlier sections compress or paraphrase required teaching. |
| `Prompts/one-more-thing-3.mp4` | 4:54.80 | Some useful visual ideas, but more setup/repetition, lost probability qualification and paraphrased close. |

## Per-roll verdicts under the current strict wording gate

**All three: REROLL under the unchanged exact-wording requirement, with a conditional repair route below.** None contains the complete required “Every choice starts with calculations. Now count what an answer takes.” No identified donor supplies the missing second sentence. This rule alone prevents calling a proposed assembly a verified REPAIR resolving every requirement. Editorially, I recommend accepting roll 1's shorter bridge rather than generating again for that sentence. That is a proposed exception, not an assumed approval.

### Roll 1

- **Teaching:** strongest probability and temperature narration (comparison below). Math numbers are correct, but the generated-token scope is less explicit and the multiplication is compressed. Borrow roll 2's complete worked example.
- **Hard requirements:** preserves the 22%-over-100 qualification, Spot-once passage, best-chance takeaway, temperature question/definition, named-app sentence (ASR writes “chat GPT”), learning distinction, trillions takeaway and both closing lines. Omits “Now count what an answer takes.” Uses “these weights” instead of required “those weights.” The latter is harmless meaning-preserving wording; accept it or use the already shipped exact line only if exactness is essential.
- **Errors/overstatement:** 1:26–1:30 says one variation **“will send … in a completely different direction.”** The page says it **can**. Proposed replacement: roll 2's complete “Each token the AI chooses shapes what comes next” sentence at 1:04.96–1:08.00; omit its following stronger claim. This retains the dependency teaching without guaranteeing a wholesale change. The drawing can demonstrate the different possible continuations.
- **Additions/excess:** “This chart shows…” at 0:37.36–0:40.08 and “This table tracks…” at 1:45.52–1:48.48 are production-furniture narration, not teaching. Cut these complete sentences. “Robotic,” “necessary variety,” and “mathematically” are less plain than the source; no need to stitch individual words.
- **Source QA:** no conflict in the approved teaching example. Keep the imagined-model and generated-token qualifications; do not read the table cells merely because they exist on the board.
- **Listening:** not performed. “Doc” in the first ASR, the token-name pronunciation and the apparent “Up” at 1:58.96 need audition rather than being declared actual errors.

### Roll 2

- **Teaching:** probability example is understandable but lacks the explicit best-chance takeaway. Temperature gives the three Spot values, but “concentrates odds / spreads the odds” never explicitly explains the better chance for less likely choices. Roll 1 is the better teacher for that passage. Math is the richest of the three.
- **Hard requirements:** exact temperature connecting question, trillions takeaway and both close lines are present. The 100-tries explanation preserves the meaning but rearranges it; Spot-once omits “even with the highest probability”; best-chance sentence is missing. Definition, named-app, learning-distinction and fixed-weights lines are paraphrased. The math bridge is incomplete.
- **Errors/overstatement:** changed-token sentence at 1:08–1:11.76 is more categorical than the page. Keep only its preceding complete dependency sentence as a donor. Do not use this roll's weak temperature compression as the final version.
- **Additions/excess:** cut “This board shows…” at 0:39.36–0:41.92 and “This graphic lays out…” at 2:17.76–2:20.48 if using those areas. “Entry fee” is optional metaphor/filler, not an extra literal cost fact; not needed in the proposed donor.
- **Repair route:** roll 1 supplies the qualified 100-tries explanation, five-pick conclusion, temperature explanation and most required wording. Starting from roll 1 is simpler than replacing these sections in roll 2. Missing full math bridge still requires a wording decision.
- **Source QA:** correct worked-example arithmetic and explicit scope/estimate qualification. Listening and donor join verification outstanding.

### Roll 3

- **Teaching:** clear five-pick setup, but the 100-tries passage drops “on average, if the odds stay the same,” then says **“The other 78 times, it will pick something else”** at 1:00.20–1:03.20. That turns an expectation into a promised count. Both ASR passes agree on this wording.
- **Hard requirements:** preserves “The best chance is not a guarantee” and “Every time you hit send.” Other required passages are paraphrased or incomplete, including “It is math and probability, executed one token at a time” at 4:46–4:50. The full math bridge is absent.
- **Errors/overstatement:** 2:13–2:20 says a variation “instantly sends the entire rest of the sentence” down a different path. Same overstatement as the shorter rolls, amplified. Closing math generalization “baseline reality holds true across the board” is broader than the carefully qualified imagined-model example.
- **Additions/excess:** 0:00–0:09.88 adds the very preamble the prompt asked to omit. Uses formal language such as “margin of dominance” at 3:31. Several chart/graphic announcements. More duration does not buy a clearer math example.
- **Repair route:** correct donor passages exist in rolls 1/2 for most teaching, but replacing them leaves little reason to use roll 3 as base. Full math bridge still absent. Do not ask for another full generation solely to salvage this base.
- **Source QA:** the written source has the needed qualification; this is generation drift. Listening not performed.

## Beat-by-beat best-of comparison

Quotes are from the fresh ASR. RICH/TAUGHT describe teaching, independent of exact-wording compliance. Where a line overstates the source, WRONG refers to that stronger wording.

| Teaching point | Roll 1 | Roll 2 | Roll 3 | Take / reason |
|---|---|---|---|---|
| Three opening questions | TAUGHT 0:00–0:12: “Why can the exact same prompt…” | TAUGHT 0:00–0:11: “Why can the same prompt…” | TAUGHT 0:00–0:22: “We are going to look at three specific parts…” before questions | 1; starts on the question. No narration graft needed. |
| Dog-name prediction and Spot 22% | RICH 0:12–0:37: “probability for every possible word, or token”; “does not guarantee selection” | RICH 0:13–0:39: “probability for every token”; “top choice doesn't always win” | TAUGHT 0:24–0:52: “Before it outputs a single letter…” | 1; contextualized at the name, no extra preamble. |
| Meaning of 22% | RICH 0:40.64–0:48.64: “on average, if the odds stay the same” | RICH 0:24.80–0:33.92: “if the odds stay exactly the same … on average” | WRONG 0:52–1:03: “The other 78 times, it will pick something else” | 1; correct and required wording intact. |
| Unchanged odds, separate picks | RICH 0:48.64–1:04.40: “unchanged across five separate picks”; names all five; “one possible set” | TAUGHT 0:45.12–0:53.04: “unchanged across five random picks”; names all five | RICH 1:07–1:31.68: “next token is completely open”; “probabilities frozen in place” | 1; 3's open-slot explanation is richer but not worth another graft; 1 already establishes name position and separate picks. |
| Spot once, another set, takeaway | RICH 1:04.96–1:12.40: full three sentences | TAUGHT / MISSING exact takeaway 0:53.60–0:57.28: “Spot was picked only once. Another five picks…” | TAUGHT 1:31.68–1:51.68: “another five picks … different combination”; takeaway | 1; clearest and most concise complete conclusion. |
| Why allow variety | TAUGHT 1:12.96–1:21.76: “Giving other highly ranked tokens a chance … adds necessary variety” | TAUGHT 0:57.84–1:04.40: “Giving other likely tokens a chance adds variety” | TAUGHT 1:51.68–2:08.60: “fair chance … adds necessary variety” | 1 retained; 2 plainer but no essential gain from another graft. |
| Each token affects the next | WRONG stronger conclusion 1:21.84–1:30.32: “will send … completely different direction” | TAUGHT complete sentence 1:04.96–1:08: “Each token the AI chooses shapes what comes next”; following sentence too categorical | WRONG stronger conclusion 2:08.60–2:20.76: “instantly sends … completely different path” | 2's first complete sentence only; join and matching picture provisional. |
| Temperature transition and definition | RICH 1:31.04–1:41.04: required question, “mechanism called temperature,” definition | TAUGHT 1:12.32–1:21.36: required question, “answer is temperature,” definition with extra “the” | TAUGHT 2:20.76–2:38.36: extended question and “probability distribution across the vocabulary” | 1; the new question genuinely connects the ideas. |
| Handled behind scenes | TAUGHT 1:41.04–1:44.88: “In chat GPT, Claude, and Gemini…” | TAUGHT 1:21.36–1:27.76: “this temperature calculation is handled…” | TAUGHT 2:38.36–2:47.36: “interface handles temperature settings…” | 1, subject to pronunciation check. |
| Low/high example | RICH 1:48.48–2:23.20: 22→36; “less likely choices a much better chance”; 16; top-choice lead | THIN 1:30.16–1:41.20: “concentrates odds … spreads the odds,” with numbers but no explanation of lower choices | RICH 2:47.36–3:33.48: effects and 22→36/16, with repeated setup | 1. Cut only optional table-announcement sentence. |
| Does not change learning | TAUGHT 2:23.76–2:27.60: exact two sentences | TAUGHT 1:42.08–1:46: “doesn't change what the model learned” | TAUGHT 3:33.48–3:42.72: “does not alter … data … learned” | 1, precise distinction. |
| Bridge to math | TAUGHT, incomplete required wording 2:28.40–2:30.32: “Every choice starts with calculations” | TAUGHT, incomplete 1:46–1:47.92: same sentence | TAUGHT, paraphrased 3:42.72–3:54.28: “Reshaping probabilities is just one step…” | 1 shorter bridge; owner wording exception needed. |
| Training-created weights, fixed in use, used per token | TAUGHT 2:31.12–2:43.04: “training creates its weights”; “these weights stay fixed”; “For each new token…” | RICH 1:48.48–2:00.32: “Training created”; “those weights stay fixed”; “For each new token…” | TAUGHT 3:54.28–4:09.68: “established during … training”; “remain completely frozen” | 1 adequate; these/those variation harmless. |
| Hypothetical model and per-token math | TAUGHT 2:43.04–2:53.04: “Imagine … one trillion weights … two calculations per weight” | RICH 2:01.04–2:11.92 and 2:20.56–2:29.76: “one pass through our example model's trillion weights” | TAUGHT 4:12.52–4:21.60: same numerical premise | 1 setup, then 2 board explanation. |
| 100 / 1,000 tokens | TAUGHT 2:53.60–3:00.64: “hundred token answer equals two hundred trillion”; “thousand … two quadrillion” | RICH 2:30.48–2:52.32: explicitly multiplies each token count by two trillion | TAUGHT 4:21.60–4:31.84: “multiplies to 200 trillion”; “roughly two quadrillion” | 2 whole math-board beat. |
| Scope and estimates | THIN scope / TAUGHT estimate 3:01.36–3:04.72: “estimates for an imagined model” | RICH 2:52.96–2:59.28: “tokens the AI writes … not measurements of a real one” | THIN scope / TAUGHT estimate 4:31.84–4:38.08: “estimates … rather than measurements … commercial AI” | 2; the useful precision is explicit, not left to inference. |
| Trillions takeaway | TAUGHT 3:04.72–3:07.68: exact line | TAUGHT 3:01.04–3:04: exact line | TAUGHT / overbroad lead-in 4:38.08–4:46.28: “across the board … staggering trillion calculation process” | 2 with its math beat, avoiding duplicate takeaway. |
| New closing message | TAUGHT, exact 3:08.32–3:12.56 | TAUGHT, exact 3:04.80–end of narration | TAUGHT but paraphrased 4:46.28–4:51.60: “It is … executed…” | 1 preserves base close; 2 is an alternative if listening favors it. |

## What changed versus v12, and what still needs visual work

- **No percentage recital in any roll.** All name the five picks. This preparation change worked.
- **Temperature bridge landed in 1 and 2.** It asks the connecting question and answers it, rather than just arriving at a new heading. Roll 3 does a longer version. No additional pause is proposed without listening.
- **The new close landed in 1 and 2.** The words now connect the full lesson. Cadence comparison still requires listening.
- **Opening motion improved, accuracy did not.** Roll 1 cycles through odds/temperature/math pictures, but displays unrelated percentages, an invented temperature value and “creative.” Roll 2 opens on “The sky is…” with invented percentages; it does not deliver all three promised visual beats cleanly. Roll 3 has a three-part overview but adds a ten-second spoken preamble, “Describe the ocean,” invented percentages and a 1.8-trillion label. None of these opening scenes is ready to keep intact.
- Roll 1's early dog-name graph has wrong names/percentages (Buddy 14, Max 11, Bella 7, Charlie 4). Roll 2 has useful dog-question and blank answer-box drawings around 0:11.60–0:21.43, plus a useful 22%-over-100 scene around 0:24.60–0:34.03. Inspect every in/out before reuse; a separate unlabeled bar sketch reaches roughly 29 while narration says 22.
- Roll 1's 1:13.07–1:21.87 name collage is usable illustration material. Its later branching picture changes to a robot example and invents percentages. Roll 2 repeats the awkward “The dog was Spot …” paths. Roll 3's 2:08.57–2:20.67 cat/dog/robot branches are more intelligible and show different continuations without new percentages, though jargon headings should be removed or covered before reuse.
- All temperature lead-ins introduce invented extra distributions. Roll 3's “CONTROLLING THE ODDS” slider is the wrong framing for this lesson. Reuse the canonical comparison or a genuinely matching drawing, not these diagrams unchanged.
- Generated weights scenes add inference/parameters/FLOPs labels. Some are reusable after targeted label treatment, but not approved wholesale. All recreated boards, native yellow fills, marker lines, crops and Notebook branding require normal production replacement/removal.
- Approximate raw board runs from scene cuts: roll 1 B1 35.60s, B2 42.90s, B3 20.57s; roll 2 B1 18.50s, B2 18.27s, B3 46.97s; roll 3 B1 48.57s, B2 44.00s, B3 36.57s. Continuous comparison holds may be justified, but the combined candidate needs purposeful breaks, not a return to v12's static opening.

## Conditional edit plan — no build authorized by this review

**Base:** roll 1. **Audio donor candidates:** roll 2's dependency sentence and complete math-board walk. Two proposed grafts, the second entirely under the canonical math board. No seam has been auditioned or finalized. Do not describe them as verified repairs yet.

1. Cut roll 1 0:37.36–0:40.08, “This chart shows how these probabilities work in practice.” Preserve its following qualified 22% explanation.
2. Replace roll 1 1:21.84–1:30.32, “And because … completely different direction,” with roll 2 1:04.96–1:08.00, “Each token the AI chooses shapes what comes next.” The donor's following stronger sentence is excluded. Carry a matching branching drawing; avoid orphaning roll 1's robot scene.
3. Cut roll 1 1:45.52–1:48.48, “This table tracks exactly how that setting behaves.”
4. Keep roll 1's weight/model setup through roughly 2:47.20. Replace its 2:47.76–3:07.68 math-board narration with roll 2 2:20.56–3:04.00, starting “On the left, producing one token, such as Spot…” and ending “Even a short answer takes trillions of calculations.” This includes explicit multiplication, generated-token scope and estimate qualification. Keep roll 1's new close. “On the left / middle / right” references are supported by the canonical three-card board.
5. Accept the shorter math bridge and “these weights” wording as proposed exceptions, or retain the strict gate and obtain the exact missing narration. Do not manufacture speech or splice isolated words to satisfy typography.

Durations above are ASR planning ranges. Measure silences and local levels and audition complete preceding/donor/following sentences before building. No additional pauses are proposed; preserve natural gaps unless direct listening establishes a need. Nominal assembled duration is about 3:28 before the standard outro replacement, not a runtime promise.

| Board | Proposed highlight sequence | Camera | Screen time / break | Reason or exception |
|---|---|---|---|---|
| Same Probabilities, Different Choices | Probability column → each of five pick rows at spoken names → full picks caption → takeaway banner | Complete unmarked arrival; full view, restrained push only | Main walk about 33s after the chart-announcement cut; use roll 2's 100-trial drawing for the qualified 22% passage before the five-pick comparison. This reduces the continuous board walk to roughly 24s. | Row highlights are useful here because each separate selection is explicitly named. Keep the two columns visible for comparison. |
| How Temperature Changes the Odds | Starting odds → low column / Spot 36 → high column / Spot 16 → banner | Full view so all three columns compare | Main walk about 39s after the table-announcement cut. Potential break under the restatement about the top-choice lead, only if an accurate donor survives review; otherwise disclose the comparison hold. | Current raw temperature drawings are not clean donors. Do not invent filler or use misleading distributions simply to break the board. |
| The Math Adds Up Fast | Complete one-token card → 100-token card → 1,000-token card → banner | Full view; complete cards and fixed 4px outlines | Donor walk about 43.4s; break during 2:52.96–2:59.28 donor scope/estimates caveat to a verified hypothetical-weight drawing, returning for the takeaway. Initial numerical comparison ~32s. | Retain the complete worked multiplication. Candidate donor is the shipped hypothetical-model illustration used in v12; bind to its reviewed source hash. |
| Math and probability, one token at a time. | Unmarked canonical closing JPG | Standard hold/push/settle | Narration through both lines, replacing Notebook outro | Keep the new copy and course closing treatment. |

Opening production remains provisional: use the best accurate drawings across the three rolls, preserving the three-question order. No existing full opening is approved unchanged. The useful new donor inventory supports an edit; it does not yet establish a finished opening.
