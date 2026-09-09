# One More Thing: two-candidate narration review

Reviewed 2026-09-09. Recommendation: **use version 2 as the edit source.** It teaches the complete lesson; version 1 leaves out essential instruction. No new generation is needed to obtain the main teaching material.

This is a raw-roll intake, not a final ship grade. The primary criterion is accurate, clear, complete narration. No MP4 was changed or shipped.

## Evidence

- Candidates: `Prompts/one-more-thing-1.mp4` (3:08.90) and `Prompts/one-more-thing-2.mp4` (4:06.13).
- Grounding: current `lessons/one-more-thing.md`, the One More Thing section in `index.html`, and the three current board assets: `lessons/one-more-thing-1-draws.jpg`, `lessons/one-more-thing-2-temperature.jpg`, and `lessons/one-more-thing-3-bill.jpg`.
- Read both complete transcripts. Cross-checked recognition with small.en and an independent base.en continuous-audio transcription. Timing ranges below are editorial candidates, not frame-accurate edit decisions.
- Inspected all four version-1 and all six version-2 contact sheets, sampled every four seconds; read scene boundaries, holds, and manual teaching allocations. These samples do not constitute every-frame shipping validation or listening QA of edit joins.
- `one-more-thing-1/` and `one-more-thing-2/` contain the corresponding transcript, sections, holds, scenes, and visual sheets. Automatic keyword-based section estimates are retained separately because they misassign shared probability vocabulary.

## Comparison

| Teaching point | Version 1 | Version 2 |
| --- | --- | --- |
| Highest probability does not guarantee selection | At 0:28–0:33 merely identifies Spot at 22, then moves to temperature. The visible board cannot substitute for missing explanation. | 0:39–0:56 explains the tempting assumption, rejects it, and explains about 22 selections out of 100 with unchanged odds. |
| Five separate tries | Does not explain what the five outcomes represent. | 0:59–1:17 walks the outcomes and explicitly distinguishes separate tries from successive words in one answer. |
| Why allow alternatives? | Does not teach the repetition/variety reason. | 1:20–1:29 connects less likely selections to variety. |
| Each choice changes what comes next | Omitted. | 1:30–1:38 connects changed context to a different continuation. Wording is more absolute than the lesson, but the underlying relationship is taught. |
| Low and high temperature | 0:34–1:30 teaches concentration/spreading and unchanged weights, but introduces temperature before teaching sampling. | 1:38–2:41 builds on the previous example; explains Spot 22→36 and Other combined 32→39, then distinguishes temperature from learned weights. |
| Scale of computation | 1:48–2:33 gives the hypothetical trillion-weight example and all three totals. | 3:14–3:54 gives the hypothetical model, two operations per weight, and all three totals; clarifies that the count refers to newly written tokens. |
| Closing | 2:41–3:05 expands and paraphrases the close, adds “executes instantly,” then adds another summary. | 3:57–4:03 delivers the approved closing wording apart from natural punctuation/pauses. |

## Version 1 verdict

**Do not use as the primary source.** It has usable temperature and math narration, but a student watching it would not learn the lesson’s central probability explanation. Its approximately five-second probability introduction does not establish what 22% means, why the top choice can lose, or why repeated tries vary. Cutting cannot restore those omissions.

The narration also repeatedly uses “draw” without explaining that analogy. The long introduction and extended ending occupy time that the missing first teaching beat needed. Version 2 supplies that beat coherently, so repairing version 1 with donor audio would add unnecessary work.

Visual repair is substantial: narration already discusses temperature at 0:34 while the probability board remains onscreen through roughly 0:52, and the main temperature board does not appear until approximately 1:07. Math narration starts before the corresponding math visual. These are repairable timing defects, separate from the missing spoken teaching.

## Version 2 verdict

**Keep and edit.** All three main ideas and the essential connections are spoken. Its extra minute contains useful explanation, especially the sampling example. It is stronger because it teaches more, not because it runs longer.

The best passages to preserve are 0:39–1:17 (probability and independent tries), 1:20–1:38 (variety and changed context), 1:51–1:59 (Spot’s temperature comparison), 2:14–2:41 (high temperature and unchanged weights), and 3:14–3:25 plus 3:36–3:54 (the computation example).

The narration occasionally says “word” where the mechanism uses tokens. The worked dog-name example remains understandable, but preserve the explicit per-token math and remove the redundant one-word restatement listed below. “Forces” at 2:02 and “safe” at 2:45 are stronger than the probabilities justify; both occur in removable summaries. “Pauses” at 0:27 adds an unnecessary impression of a special stop at the name; removing that short phrase is optional if the audio edit can be clean.

## Suggested cuts in version 2

| Source range | Passage | Recommendation |
| --- | --- | --- |
| 1:58.6–2:06.0 | “By pulling points away … forces the AI into a highly predictable state.” | Cut. The preceding Spot 22→36 example already explains the effect, and this restatement overstates the result. |
| 2:06.7–2:13.3 | “Based on what you just saw, take a moment to predict …” | Optional cut for flow. The next sentence immediately teaches high temperature. Retain only if a deliberate prediction pause is wanted. |
| 2:42.0–2:50.2 | “Temperature operates as a direct control dial, allowing you to balance safe …” | Cut. Repeats the lesson and can imply both a student-facing control and safety from lower temperature. The preceding explanation is sufficient. |
| 3:25.8–3:31.6 | “Two trillion calculations is the hidden computational cost required to produce just one word.” | Cut. Repeats the immediately preceding per-token calculation and unnecessarily changes token to word. |
| 3:54.9–3:56.9 | “They do not account for repeating old work.” | Cut. Introduces an unexplained aside. Keep 3:50–3:54, which clearly says the estimates apply to newly written tokens. |
| After closing narration, approximately 4:03 | Notebook logo | Remove in the standard closing-board replacement. |

These are proposed edit spans, not executed cuts. Check word boundaries, sentence flow, breaths, and room tone before splicing. Add one-second pauses at the main transitions to temperature, computation, and the closing message, accounting for any pauses already present. Do not force a target runtime.

## Visual repairs for version 2

1. Use the exact current probability board through its explanation. Notebook pans crop the title and the opposite column (approximately 0:35–1:22). Restore the full board and course highlights while preserving the spoken left/right references.
2. Replace the invented temperature charts in the opener and at 1:38–1:46 with visuals consistent with the lesson. Use the current temperature board for the comparison and ensure the mentioned columns and values are visible.
3. Replace the altered math board. Across the samples at 3:36, 3:40, and 3:44, the third card contains merged text such as “A Longer Conversa… One Token” and repeated “calculations.” The correct full card returns later; the intervening generated zoom is unsuitable for shipping. This is visual damage, not faulty narration.
4. Replace all Notebook emphasis with course highlights. Insert the exact standard closing board and hold it through the last frame. The logo follows the close in both raw candidates.

No claim is made here that either raw candidate passes final board, sync, closing, or edit-integrity gates. Those are editing and final-review tasks.

## What this tells us about the source system

Version 2 successfully narrates details that were explicitly added to the Markdown: the five separate tries, the changed-context connection, the numeric temperature comparison, and the computation assumptions. That is encouraging evidence that the expanded source can produce the required teaching. Version 1 shows that complete source material does not guarantee complete generation; narration intake remains necessary. Two candidates are not enough to establish the workflow’s reliability.

## Technical reference checks

The expected-frequency explanation applies to sampling from the stated selection probabilities, with those probabilities held fixed. Temperature changes that distribution; it does not retrain the weights. See [Hugging Face’s sampling documentation](https://huggingface.co/docs/transformers/generation_strategies#sampling) and [generation settings](https://huggingface.co/docs/transformers/main_classes/text_generation). The model in the lesson is explicitly hypothetical; the approximate 2N operations per inference token is a standard rough compute model, as used in [Beyond Chinchilla-Optimal](https://openreview.net/pdf?id=0bmXrtTDUu). These checks support the lesson’s main teaching without turning the hypothetical trillion-weight example into a claim about a specific chatbot.

## Tracker-ready intake notes

| Candidate | Narration intake | Next action |
| --- | --- | --- |
| one-more-thing-1 | Not selected: essential probability/variety/context teaching missing | Retain as alternate raw material; use version 2. |
| one-more-thing-2 | Selected for editing: all essential teaching present; removable overstatements and repetition | Review proposed cuts, replace damaged visuals and highlights, add transition pauses, insert standard close, then perform ship QA. |

The external tracker has not been updated. These rows are ready to transfer; neither candidate is marked shipped.
