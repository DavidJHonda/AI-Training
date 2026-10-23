# Evaluation Matters: three new generations

Reviewed October 23, 2026. Scope: compare the three raw generations against the current lesson and identify usable material. No video built, installed, or published; source videos and lesson unchanged.

## Conclusion

None is a complete replacement for the lesson. The recurring problem is compressed instructional detail coupled with expanded generic commentary. The chapter structure survives, but important teaching does not. The current installed video's instructional passages are substantially more complete than these generations.

Recommended direction: preserve the installed video's teaching as the base, use roll 3 as a candidate for the new overview, roll 2 for the conditional bridge, and roll 1 for the exact new closing. Replace the old boards and restructure the old five-check narration into the new three-card organization. Do not commission another full generation yet. This is a proposed repair direction, not a verified audible assembly.

## Evidence and limits

- Read the current `EvaluatingSection` in `index.html`, current lesson Markdown, prompt, and preparation notes.
- Inspected all five canonical board images.
- Read complete fresh word-timestamp ASR transcripts of all three generations and the current installed donor. Transcripts are in `transcripts/`.
- Confirmed three material passages with a second local ASR model: roll 2's premature publish instruction, roll 1's ending, and roll 3's revision instruction. See `asr-spot-check.txt`.
- Sequentially decoded each generation to collect timestamped visual samples every 12 seconds. Inspected all three contact sheets. These samples do not establish animation quality, boundary integrity, or absence of short visual defects.
- Source hashes, sizes, frame counts and durations are in `sources.json`. The installed donor matches the hash in `gemini-notebook/evaluation-matters/DONOR.json`: `2e6ec85067a3d004089806d3fba0b2d380e997e8ad2df253c086f3f3bf3e644e`.
- **Direct listening and continuous audiovisual playback were not performed.** Quotes and timings below are ASR evidence, not a claim of hearing. Candidate spans need auditioning and silence/word-boundary measurements before an edit is considered feasible. No source earns a final KEEP or verified REPAIR verdict from this review alone.
- Video Tracker was not accessed or changed.

## Per-roll assessment

### Roll 1 — `Prompts/evaluation-matters-1.mp4` — 2:55.83

Narration assessment: incomplete; potential donor, not a base. No KEEP. Repairing it would require replacing most of the instructional middle, so retaining the installed teaching is more sensible.

Its opening spends 14 seconds on a corporate financial-report example, then uses language such as “computational power,” “rigorous system,” and “deploy this when failure risks are high.” These are less suitable for the course's conversational voice and teenage audience.

Quick Review lasts about 20 seconds and loses the concrete simpler-paragraph request and part of Validate. Take a Closer Look gives three method names in about 15 seconds without teaching source reliability, current-information checking, asking what was omitted, or evaluating the counterargument. Make Your Move omits the revision check and barely explains fixing the answer.

Useful asset: the exact new closing subtext at 2:45.90–2:50.04. The main closing line is also present at 2:39.20–2:41.00, but an extra sentence separates it from the subtext. Additional commentary follows the subtext and should be removed.

### Roll 2 — `Prompts/evaluation-matters-2.mp4` — 4:03.60

Narration assessment: incomplete and structurally confused; selective donor. No KEEP.

The opening is shorter and closer to the lesson than roll 3. It has the strongest new conditional bridge: ordinary checks are often enough, but uncertainty OR consequences call for deeper checking (1:53.90–2:10 approximately). It distinguishes the kind of task from the stakes.

At 1:24–1:43 it interrupts Read/Understand/Validate with an invented explanation that “quick review ends” in three options, says an accurate answer can be published immediately, and adds an AI-attribution instruction. Understand and Validate arrive afterward. This is an instructional ordering error, not merely different wording. The extra attribution instruction is outside this lesson; no claim about its universal appropriateness is needed to remove it.

At 0:59.74–1:09.38 it promises use “without inheriting any of its hidden errors.” At 3:56.34–4:00.08 it says testing guarantees that the final product remains entirely your own. These are unsupported assurances and should not survive.

The source check is more useful than roll 1's, but it still omits searching for current information. Challenge omits missing information and the user's judgment of the response. The close is paraphrased and narrows closer checking to high stakes. “Walk away” becomes abandoning the approach entirely when AI hallucinates or struggles, losing the lesson's more useful alternative approach/person.

### Roll 3 — `Prompts/evaluation-matters-3.mp4` — 4:10.37

Narration assessment: the clearest new overview and strongest new explanation of checking revisions, but incomplete overall. No KEEP.

The opening takes about 1:23 to reach the overview. It expands into coffee, a week's emails, hours of labor, and falling behind other people. These additions crowd out instructional detail rather than replace missing explanations.

The overview uses recognizable versions of the three headings (1:29.54–1:48.56), though it does not obey the requested verbatim wording. Validate checks the original prompt and missing information but leaves out comparison with what the learner knows. The method section is again compressed: sources, alternative perspectives, independent checks. Task-specific checks are not explained, and current information and omissions are missing.

Its revision passage at 3:13.70–3:26.20 clearly says to change the answer and review the new text. The installed donor still states this more concisely and covers manual as well as AI revision directly.

“If the answer is accurate, deploy it into your workflow” (3:06.80–3:10.74) drops the second criterion, usefulness. The ending paraphrases the new subtext and again narrows closer checking to high stakes. Its opening assertion of “absolute certainty” is unnecessarily absolute.

## Teaching comparison

RICH = useful example/reason retained; TAUGHT = adequately explained; THIN = materially incomplete; MISSING = absent; WRONG = contradicts the lesson. Quotes are excerpts, not complete transcripts. Each row compares the same teaching point, and missing elements are part of the judgment even when a related phrase appears.

| Teaching point | Roll 1 | Roll 2 | Roll 3 | Preferred material |
|---|---|---|---|---|
| Confidence does not establish truth | TAUGHT 0:14–0:23 “same authoritative tone” | TAUGHT 0:04–0:14 “same confident tone” | TAUGHT 0:00–0:10 “whether its facts are accurate or completely wrong”; cut the absolutist opening | Installed opening, concise and complete |
| Accurate can still be unsuitable; joke, explanation, plan | TAUGHT 0:23–0:34 “explanation might leave you confused”; joke absent | TAUGHT 0:04–0:14 “joke that falls completely flat”; confusing explanation absent | RICH 0:11–0:36 “a failure of tone, not truth,” dense explanation, unworkable plan | Installed 0:11.26–0:24.78 preserves all three economically |
| Learn evaluation rather than ignore useful AI | TAUGHT 0:35–0:50 “need a rigorous system”; inflated language | TAUGHT 0:15–0:33 “learn how to actively evaluate” | TAUGHT 0:36–1:14 “mastering the evaluation process”; excessive fear/office commentary | Roll 2 0:15.08–0:32.9 candidate addition to installed opening |
| Both questions: right AND good enough | TAUGHT 0:50–0:58 “Is it right?...good enough” | TAUGHT 0:33–0:43 “factually right...good enough” | TAUGHT 1:14–1:23 “Is this right?...good enough” | Installed 0:25.42–0:33.62 |
| Three-step orientation; middle conditional | TAUGHT 0:59–1:19 “fast preliminary check”; labels paraphrased | TAUGHT 0:43–0:59 “closer look if the situation demands it” | TAUGHT 1:23–1:49 “doing a quick review...taking a closer look...making your move” | Roll 3 best label correspondence; exact overview request still unmet |
| Read and take responsibility | TAUGHT 1:22–1:27 “read the complete answer...responsible” | TAUGHT 1:15–1:24 “reading the answer in full...personally own it,” followed by WRONG premature publish detour | TAUGHT 1:58–2:02 “responsible for what it says” | Installed 1:21.66–1:29.62 |
| Understand; concrete simpler-paragraph prompt | THIN 1:27–1:32 “asking the AI to simplify if needed” | THIN 1:43–1:48 “understand the text”; no explanation request | THIN 2:03–2:07 “explain it simply”; concrete prompt missing | Installed 1:30.48–1:40.62 |
| Validate against knowledge AND request; wrong/missing/not useful | THIN 1:32–1:35 “against known facts” | THIN 1:47–1:53 “against your constraints...missing information or obvious factual errors” | THIN 2:08–2:13 “original prompt...missing information” | Installed 1:41.58–1:54.09 |
| Quick review often enough; uncertainty OR stakes warrant more | THIN 1:40–1:52 “low-stakes tasks...scholarship...medical advice”; uncertainty missing | TAUGHT 1:53–2:10 “unsure...correct, or...consequences...high” | THIN 2:13–2:29 movie/grocery vs scholarship/injury; uncertainty missing | Roll 2 |
| Kind of task determines useful checks | MISSING; only high stakes discussed | TAUGHT 2:11–2:19 “historical essay needs facts...email needs polite writing”; plan example absent | THIN 2:34–2:38 merely “based on the task and stakes” | Installed 2:13.91–2:21.41 without old ordinal |
| Stakes: movie, scholarship, injury | TAUGHT 1:40–1:52 movie/scholarship/medical advice | TAUGHT 2:19–2:25 movie/medical advice; scholarship absent | RICH 2:13–2:29 movie/grocery/scholarship/sports injury | Installed 2:24.43–2:38.71 preserves examples concisely |
| Effort should match consequence | THIN 2:10–2:13 “Deploy this when failure risks are high” | TAUGHT 2:25–2:36 “more that depends...more carefully...check” | TAUGHT 2:29–2:34 “more that depends...more rigorously” | Roll 2 or installed risk-matching sentence; exact bridge unmet |
| Choose checks that fit, not mandatory sequence | THIN 1:55–2:10 “three checking methods...first...second...third” | THIN 2:35–2:53 “start...also...finally”; some optionality, no explicit fit principle | THIN 2:38–2:54 “First...Next...Finally” | Installed 2:40.15–2:45.19, cut following “all five” |
| Sources: ask/open/support/reliability/current search | THIN 1:59–2:01 “check the AI's sources” | THIN 2:35–2:42 “Open...links...reliably support”; current search absent | THIN 2:38–2:43 “opening citations...support”; reliability and current search absent | Installed 2:48.49–2:55.21 plus 3:14.43–3:19.59 |
| Challenge: strongest opposing case, omissions, decide effect | THIN 2:01–2:05 “asking for counter-arguments” | THIN 2:41–2:48 “arguments against its own conclusion” | THIN 2:43–2:47 “reveal alternative perspectives” | Installed 2:56.21–3:03.15 plus 3:05.89–3:11.83; omit separate old heading |
| Independent check: math, code, knowledgeable person | THIN 2:05–2:10 “consult experts or test it yourself” | RICH 2:47–2:53 “running the math, testing code, or consulting an expert” | RICH 2:48–2:54 same concrete methods | Installed 3:20.33–3:29.13 retains all examples |
| Use it only if right and good enough | TAUGHT 2:21–2:24 “meets your requirements” in context of both questions | TAUGHT 3:09–3:13 “meets your standards” | THIN 3:06–3:11 “If...accurate, deploy it” | Installed 3:43.05–3:48.03 explicit both conditions |
| Fix by asking or editing, then recheck | MISSING explanation 2:24–2:26 only “fix it” | TAUGHT 3:14–3:21 “telling...what to change...manual edits...re-review” | RICH 3:13–3:26 “run that new text back through your quick review” | Installed 3:48.71–3:55.65 concise and exact revision line |
| Walk away: another approach or knowledgeable help | THIN 2:26–2:30 “walk away entirely” | THIN 3:22–3:28 “abandon the approach entirely” | THIN 3:26–3:36 “when it's wasting it”; alternatives absent | Installed 3:56.31–4:02.81 |
| Complete new closing | TAUGHT exact words at 2:39.20–2:41 and 2:45.90–2:50.04, interrupted and followed by extras | THIN 3:38–4:00 paraphrase, high-stakes-only restriction, unsupported guarantee | THIN 3:49–4:07 exact main line, changed subtext/high-stakes restriction, extra ending | Roll 1, two sentence groups with an intervening cut |

## Hard wording requirements

All three miss the requested exact overview lines, both exact conditional-bridge sentences, the exact task/stakes connector, and “Then check the revised answer before you use it.” The installed donor has that last sentence at 3:53.41–3:55.65.

Roll 1 has both exact closing components, but not consecutively: remove “The machine generates content, but you provide final judgment” between them, and “Your critical judgment is vital” afterward. Roll 2 changes both components. Roll 3 preserves the main closing sentence but changes the subtext.

There is enough identified material to investigate a substantively complete hybrid, but **not** enough identified verbatim audio to claim every preparation requirement can be met. Before building, either accept natural equivalents for the overview/bridges or obtain just those short lines. A full fourth roll is not the recommended first response.

## Best-of assembly direction, pending audition

Base: the current installed donor, preserved under a stable candidate/source path before any future installation overwrites it. Keep its 0:00–0:33 opening, 1:21.66–1:54.09 Quick Review, task/stakes explanation, detailed checking, and 3:38.71–4:02.81 Make Your Move.

Candidate additions/replacements:

1. Optional reason-to-learn insertion: roll 2 0:15.08–approximately 0:32.9, from “But pretending this technology doesn't exist...” through “smarter than the tool you are using.” Locate the actual sentence boundary using the word transcript. Avoid repeating its following two questions.
2. Replace the donor's 0:34.66–1:19.52 old branching-flowchart explanation with roll 3 approximately 1:22.94–1:48.56, “This graphic lays out...” through “handle the generated material.” It is the best new overview, but still paraphrases the required headings and descriptions. Cut before its unnecessary restart/habit commentary.
3. Before the task/stakes material, consider roll 2 1:53.90–approximately 2:09.6, “For straightforward tasks...” through “you have to dig deeper.” This retains the uncertainty branch missing from the other new rolls. Its actual ending is inside a transcript segment; no frame-accurate cut is approved.
4. Remove the donor's old Can You Judge It section and ordinal lead-ins. Keep “Different tasks require different checks. A factual answer needs accuracy. A draft needs clear writing. A plan must be workable” at 2:13.91–2:21.41. Keep movie/scholarship/injury and risk matching at 2:24.43–2:38.71. These sentences supply the needed why-to-how transition without new wording.
5. Use donor 2:40.15–2:45.19, “When an answer needs a closer look, you choose the specific checks that fit your task.” Remove “You don't necessarily need all five every time.”
6. Under Check the Sources, assemble donor 2:48.49–2:55.21 then 3:14.43–3:19.59. This places the current-information explanation within the source card without its old separate heading.
7. Under Challenge the Answer, keep donor 2:56.21–3:03.15 and 3:05.89–3:11.83. Remove the separate “Ask what's missing” heading while retaining its full teaching.
8. Keep donor 3:20.33–3:29.13 for Check It Yourself. Remove retired-banner narration 3:30.01–3:36.93.
9. Keep the donor's full Make Your Move passage 3:38.71–4:02.81, including the exact revision check.
10. Replace old close with roll 1 main sentence 2:39.20–2:41.00 and subtext 2:45.90–2:50.04. Cut the intervening explanation and trailing commentary. Keep only approved closing words on the canonical close.

All times are source-time ASR locators. Several are inside continuous narration. Whole-sentence grafts must be checked in surrounding context for voice continuity, complete consonants, cadence, and silence boundaries. No joins have been auditioned; this is not an edit manifest. Do not introduce default pauses. Measure existing gaps before proposing any pause changes.

## Proposed board treatment

| Board | Highlight sequence | Camera | Span / breaks | Reason |
|---|---|---|---|---|
| How to Evaluate an AI Answer | Whole purple, blue, teal cards as introduced | Full board, stationary | Roughly 26 seconds if roll 3 overview retained; no extra pause | Compact overview; replace generated crops and markers |
| Do a Quick Review | Whole Read, Understand, Validate cards | Full board, stationary | Roughly 32 seconds with donor detail; assess readability and existing supporting scene opportunities | Preserve same purple treatment; no small flowchart |
| Take a Closer Look | Whole task card, whole stakes card, connector as spoken, then each complete method card | Start full board; compare complete-card closer views for this taller board at 720p | Approximately 80–90 seconds of selected teaching across the topic; needs meaningful visual breaks, not one uninterrupted board hold | Full-view text is small; timing and any retained donor cutaways require a separate motion inspection |
| Make Your Move | Whole Use It, Fix It, Walk Away cards | Full board, stationary | Approximately 24 seconds using donor | Teal; no banner or individual-sentence outlines |
| Closing message | No highlights | Standard closing treatment on canonical image | Approximately 8 seconds plus measured natural gaps; confirm after assembly | Ends on exact new subtext; no post-close commentary |

Visual candidates observed in still samples only: roll 2's failed-plan illustration around 0:12 could support the opening; roll 1's scholarship/injury illustration around 1:48 could support stakes; roll 3's tangled explanation around 0:24 could support confusion. Their motion, exact spans and narration compatibility have not been evaluated. Do not replace useful motion with stills by default. Roll 3's added revision diagram around 3:24 labels the final step TRUST; prefer the canonical Fix It card rather than implying a quick review certifies safety. Board recreations show cropping, blur and baked-in marks; replace them with canonical assets as standard production work.

## Producer-notes finding

The supplied seven-part producer outline describes sections and visual intentions but does not itself preserve their complete spoken teaching. These outputs follow that broad sequence while omitting methods and elaborating generic commentary. This supports using producer notes as an outline checkpoint, not treating approved notes as evidence that the generated narration will be complete. It does not establish whether the notes feature, model, format, or some combination caused the omissions. No final refined notes or generation settings were inspected for these three files.

Source QA: no material contradiction found in the current instructional lesson. TRY IT remains a separate activity intentionally excluded from the video prompt. No lesson text changes are recommended as a remedy for these generation omissions.
