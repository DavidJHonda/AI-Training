# Why Answers Vary: versions 4, 5, and 6

**Version 4 is the strongest foundation. Version 5 is second. Version 6 compresses essential explanations too far. None is ready for production unchanged.**

Reviewed November 10, 2026 against the current `InferenceSection` in `index.html`, the lesson Markdown, the generation prompt, and all four canonical board images. These are the new uploads named `why-answers-vary-4.mp4`, `-5.mp4`, and `-6.mp4`, not the older installed `v4` edit. Source hashes are in `sources.json`.

## Evidence and limits

Complete base.en and small.en timestamped transcripts were read for all three candidates. Sequential frame decoding covered all three files; every four-second contact-sheet sample was inspected. The second ASR pass confirmed the consequential omissions and overstatements; it did not resolve version 4's “tries” pronunciation. This is a transcript-led teaching review and sampled-frame visual review, **not direct perceptual listening or uninterrupted audiovisual playback**. Voice quality, pronunciation, natural pacing, animation quality, and donor joins remain unverified. Proposed cuts and grafts below are textual candidates, not auditioned repairs. No video was edited or installed.

| Upload | Runtime | Assessment |
|---|---:|---|
| 4 | 3:44.80 | Best explanation of the fixed-odds example and strongest overall lesson continuity. Extra technical-sounding commentary introduces problems. |
| 5 | 3:20.83 | Useful explicit sampling definition and correct temperature numbers, but less faithful language, weaker qualifiers, and an expanded close. |
| 6 | 2:01.73 | Clear short sampling/temperature bridge and exact ending, but important sampling conditions and the role of context in starting odds are unspoken. |

Under `NARRATION-REVIEW.md`, the current candidates fall in **REROLL pending a verified repair**: all miss at least one required sentence, and no complete, auditioned repair exists. This does not mean throwing away version 4. Its strongest passages can be retained if corrected narration is obtained. Do not label an unauditioned donor plan REPAIR or a promising base KEEP.

## Teaching comparison and best-of plan

Times below are source times, rounded from ASR segments. RICH and TAUGHT both pass; hard wording requirements are checked separately. A correct teaching beat does not excuse an incorrect addition elsewhere.

| Teaching point | Version 4 | Version 5 | Version 6 | Selection |
|---|---|---|---|---|
| Two new chats, same question, Spot then Max | **RICH**, 0:00–0:14: “You start a new chat and ask the exact same question. This time, it suggests Max.” | **TAUGHT**, 0:00–0:16: “You start a brand new chat, ask the exact same question…” The question becomes “How did the exact same input yield a totally different result?” | **RICH**, 0:00–0:14: approved setup and question. | Keep 4. Both 4 and 6 preserve the distinction between the same question and a second attempt. |
| Model and thinking | **TAUGHT**, 0:17–0:21: “the specific model you use and its processing time.” Less direct than the approved thinking wording. | **THIN**, 0:19–0:25: “The specific system and computing power change the answer.” Computing power does not clearly teach thinking mode/effort. | **TAUGHT**, 0:18–0:22: “the model you use and its thinking time changes the answer.” | Keep 4 provisionally; 6 is closer in wording but not worth an isolated graft without improving the whole overview. |
| Prompt and available information | **TAUGHT**, 0:21–0:25: “what the AI receives, your prompt and provided context.” | **TAUGHT**, 0:25–0:31: “Prompt and context alter starting conditions.” | **TAUGHT**, 0:22–0:28: “your prompt and context alters the output.” | 4 is sufficient; new narration should prefer “available” to “provided.” |
| Selection techniques and transition | **TAUGHT**, 0:29–0:34: “AI uses techniques giving different tokens a chance, sampling and temperature.” | **THIN** in the overview, 0:31–0:37: “the AI's choices. Techniques like sampling and temperature.” Explained later. | **TAUGHT**, 0:28–0:39: “selection techniques giving different tokens a chance” and “Two techniques explain AI's choices…” | 4 carries the idea. None speaks the required transition exactly. |
| The single open blank and vocabulary-wide probabilities | **THIN overall**, 0:47–0:53: clearly speaks “You could name him” and “the next open blank,” but never says a probability is calculated for every token. | **THIN overall**, 0:37–0:41: “calculating a probability for every token,” but never reads the unfinished reply or establishes the single blank explicitly. | **MISSING**: jumps to “In this breakdown, Spot leads…” at 0:39. | Keep 4's single-blank setup; obtain the vocabulary sentence. An older donor is identified below. |
| Spot's 22% and what it means | **RICH**, 0:54–1:11: leads at 22%, expected automatic winner, about 22/100 “on average, if the odds stay the same.” | **TAUGHT**, 0:41–1:00: “roughly 22 times out of 100 attempts,” then an explicit weighted-draw definition. The fixed-odds condition arrives in the next example rather than the required sentence. | **THIN**, 0:39–0:49: “22 times out of 100 on average. That's sampling.” No unchanged-odds condition. | Keep 4. The ASR disagreement around “tries” needs listening; do not treat “drives/dries” as a confirmed spoken error. |
| Five independent attempts with unchanged odds | **RICH**, 1:11–1:35: “five separate random picks with these exact unchanged probabilities,” all five names, Spot only once, another set could differ. | **RICH**, 1:00–1:24: “five random picks against these exact same probabilities,” all names, Spot once, another set. | **THIN**, 0:49–0:56: lists the names and says another five could differ, but omits unchanged odds and the spoken observation that Spot appeared only once. | Keep 4. No need for a donor from 5. |
| Why allow alternatives? | **WRONG qualifier**, 1:49–2:07: selecting the top token “makes” answers rigid and repetitive; alternatives make them creative. The approved claim is “can.” | **WRONG qualifier**, 1:31–1:48: answers “would become highly repetitive and read like a machine.” | **WRONG qualifier**, 0:57–1:09: choosing the top token “creates repetitive loops”; alternatives “prevent repetitive answers.” | No clean whole-beat donor among these three. Obtain the approved qualified explanation. |
| One choice shapes later choices | **TAUGHT with an overstatement to fix**, 2:07–2:19: a different token shifts context and shapes what comes next, but asserts the rest goes in an “entirely different direction.” | **TAUGHT with an overstatement to fix**, 1:48–1:58: “Choosing a different token shapes what comes next,” followed by guaranteed “completely divergent path.” | **THIN**, 1:05–1:09: “completely shapes the direction of the following text.” | Version 5's first complete sentence is clean but very brief. An older complete qualified donor is identified below. |
| Sampling selects; temperature adjusts | **RICH**, 2:28–2:34: exact two sentences. | **TAUGHT**, 1:58–2:06: “Sampling is the mechanism…” and “Temperature is the tool…” | **RICH**, 1:09–1:14: exact two sentences. | Keep 4; no graft needed. |
| Named apps set temperature behind the scenes | **TAUGHT**, 2:34–2:38, but omits “for you.” | **TAUGHT**, 2:06–2:16: “everyday consumer interfaces…” and “managed for you automatically.” | **RICH**, 1:14–1:20: approved sentence in ASR, subject to pronunciation check. | Candidate whole-sentence donor from 6, under the transition visual. |
| Starting odds come from training and context | **RICH**, 2:43–2:50: “the model's training and the context you provided.” | **TAUGHT**, 2:18–2:26: “training data and your prompt.” | **THIN**, 1:22–1:26: “baseline odds from AI's training.” Omits context. | Keep 4. |
| Low temperature concentrates, Spot 22% to 36% | **RICH**, 2:50–3:01: “concentrates the odds onto the most likely choices,” then both numbers. | **RICH**, 2:26–2:39: concentrates “around the leading choices,” then both numbers. | **TAUGHT**, 1:26–1:33: concentrates probability and gives both numbers. | Keep 4. |
| High temperature spreads, Spot 22% to 16%; same baseline | **RICH**, 3:01–3:13: “spreading the odds out more widely,” Spot 16%, “exact same starting odds.” | **RICH**, 2:39–3:00: wider spread, explicitly 22% to 16%, same baseline. | **TAUGHT**, 1:33–1:44: wider spread, 16%, same starting odds. | Keep 4. 5's explicit repeat of 22% is optional richness, not a reason to graft. |
| Other combines the remaining vocabulary | **WRONG detail**, 3:13–3:20: calls it “the hundreds of remaining low probability vocabulary words.” The source says remaining vocabulary, with no such count or word/token substitution. | **MISSING** in narration. | **MISSING** in narration. | Replace 4's sentence with a verified neutral donor or new narration. |
| Spot remains highest individual token; probability changes | **RICH**, 3:20–3:27: exact approved two sentences. | **TAUGHT**, 3:00–3:09: “highest individual token” and “degree of its dominance.” | **RICH**, 1:44–1:51: exact approved two sentences. | Keep 4. |
| Two-line close | **RICH**, 3:37–3:42: exact close. | **TAUGHT**, 3:09–3:18: expands “AI answers vary” with a causal sentence and adds “and” to the last line. | **RICH**, 1:53–1:59: exact close. | Keep 4. |

**BASE: version 4, conditional on obtaining missing/corrected narration.** No cross-roll graft is approved or verified. Potential grafts: one from version 6, up to three older complete beats below, plus new narration for unresolved requirements. The exact count depends on whether the new roll supplies a coherent overview and qualified explanation together. Avoid assembling a patchwork of short phrases.

## Required verbatim audio

Punctuation and ASR capitalization do not count as differences. An added leading conjunction does not erase an otherwise intact sentence. A paraphrase can teach correctly while still missing a hard wording requirement.

| Required line | 4 | 5 | 6 |
|---|---|---|---|
| Full two-chat opening | MET, 0:00–0:11 | MISSED: “an AI,” “brand new,” altered connective wording | MET, 0:00–0:11 |
| “Why did the same question get a different answer?” | MET, 0:11–0:14 | MISSED: “How did the exact same input yield…” | MET, 0:11–0:14 |
| “Two techniques help explain AI's choices: sampling and temperature.” | MISSED, 0:29–0:34 | MISSED, 0:31–0:37 | MISSED, 0:35–0:39: omits “help” |
| Qualified 22%-means-22/100 sentence | PROVISIONALLY MET, 1:01–1:10; listen to “tries” | MISSED, 0:47–0:54: paraphrased, qualifiers absent here | MISSED, 0:39–0:47: abbreviated, fixed-odds condition absent |
| “That's called sampling.” | MET, 1:10–1:11 | MISSED: longer definition | MISSED: “That's sampling” |
| “Sampling selects a token using probabilities.” | MET, 2:28–2:31 | MISSED, 1:58–2:03: paraphrase | MET, 1:09–1:12 |
| “Temperature adjusts those probabilities.” | MET, 2:31–2:34 | MISSED, 2:03–2:06: paraphrase | MET, 1:12–1:14 |
| Named-app sentence, including “for you” | MISSED, 2:34–2:38: omits “for you” | MISSED, 2:06–2:16: paraphrase | MET in ASR, 1:14–1:20; pronunciation not verified |
| Spot remains highest individual token / temperature changes its probability | MET, 3:20–3:27 | MISSED, 3:00–3:09: paraphrase | MET, 1:44–1:51 |
| “AI answers vary.” | MET, 3:37–3:38 | MISSED as standalone sentence, 3:09–3:14 | MET, 1:53–1:55 |
| “Different inputs. Different odds. Different choices.” | MET, 3:38–3:42 | MISSED, 3:14–3:18: adds “and” | MET, 1:55–1:59 |

The missing “help” in version 6 is a production wording issue, not a conceptual error. The unchanged-odds omission and “prevents repetitive answers” claim are substantive teaching issues. Keep that distinction clear.

## Per-roll findings

### Version 4

**VERDICT: REROLL pending verified repair; preferred foundation.**

TEACHING POINTS and HARD REQUIREMENTS: see the complete tables above.

ERRORS / REQUIRED CORRECTIONS:

- 0:34–0:45 says the model, inputs, and probability mechanics “interact differently in every session.” This implies universal session-by-session change. The lesson says these factors can change an answer. Remove the added summary.
- 1:35–1:48 contrasts probability as “a frequency guide” with “a strict mathematical rule.” Sampling follows mathematical probability rules. This distinction is misleading and redundant after the correct five-pick example. Remove the sentence.
- 1:49–2:07 and 2:09–2:19 lose the lesson's “can” qualifications. Obtain corrected whole beats, rather than accepting guaranteed repetition, creativity, or complete divergence.
- 2:19–2:28 adds an explanation about mimicking “human thought in conversation.” Unsupported purpose claim and unnecessary abstraction. Cut.
- 3:13–3:20 adds “hundreds” and changes tokens to words. Replace with the source's neutral explanation of the remainder.
- 3:27–3:37 returns to “core understanding,” an extra concept the lesson deliberately removed. Cut the entire added temperature summary. “Focus style” in ASR is uncertain; do not flag it as a confirmed spoken phrase without listening.

ADDITIONS WORTH KEEPING: the explicit “next open blank,” “five separate random picks,” and “exact unchanged probabilities” are useful. They make the five names separate attempts rather than one generated sentence.

SOURCE_QA: PASS for alignment with the approved simplified lesson. The problematic additions above come from the candidate, not the lesson. This review is not a fresh audit of app settings or model implementations.

REPAIR PLAN: the cuts and donor candidates below would improve the base, but do not yet resolve every required line. No auditioned repair exists. Corrected narration is still required.

LISTENING: not performed; full transcripts and sampled frames inspected.

### Version 5

**VERDICT: REROLL if used as the base; prefer 4.**

TEACHING POINTS and HARD REQUIREMENTS: see tables.

ERRORS / REQUIRED CORRECTIONS: “computing power” substitutes for thinking; the 22/100 sentence drops the approved qualifications; repetitive output and complete divergence are asserted rather than qualified. “The exact same input” is broader than the opening establishes, which guarantees only the same question. The narration does not explain the combined Other category. All eleven required lines are paraphrased or incomplete as exact lines.

ADDITIONS: “drawing a token based on a set of weighted odds” at 0:54–1:00 is a useful explicit definition; “weighted advantage, not a guarantee” at 1:15–1:19 is clear. Neither warrants replacing the stronger and already qualified sampling run in 4.

REPAIR PLAN: 4 supplies the opening, qualified 22/100 explanation, sampling name, temperature bridge, comparison takeaway, and close. 6 supplies the app sentence. Replacing so many sections defeats choosing 5 as the base, and still leaves the shared unresolved transition and qualified rationale. No joins auditioned; no verified complete repair.

SOURCE_QA: PASS for alignment. EDITING NOTES: retain the useful weighted-draw visual only if a motion review confirms it helps; do not import its extra technical headings and formulas into the lesson. Several board views crop content. The 2:06–2:16 app scene uses stylized brand-like symbols; use a plain text treatment in production.

LISTENING: not performed; full transcript and sampled frames inspected.

### Version 6

**VERDICT: REROLL if used as the base; possible short donor.**

TEACHING POINTS and HARD REQUIREMENTS: see tables.

ERRORS / REQUIRED CORRECTIONS: “creates repetitive loops” and “prevents repetitive answers” overstate what the lesson says. The single open blank, vocabulary-wide probabilities, unchanged odds across the five attempts, Spot appearing once, context's role in starting odds, and the combined Other category are missing or too thin in speech. Showing these on a board does not supply the missing narration.

ADDITIONS: none needed. Its useful strength is concise approved wording in the temperature bridge, app sentence, comparison takeaway, and close.

REPAIR PLAN: importing 4's sampling run and fuller temperature setup would fix several omissions, but would also import 4's issues unless selectively repaired. Prefer 4 as the coherent spine. No joins auditioned; no verified complete repair.

SOURCE_QA: PASS for alignment. EDITING NOTES: the repetition-loop scene at 0:57–1:09 visually reinforces the overclaim; repair the explanation before deciding what motion to retain. Board pans visibly crop columns, and the overview includes distorted text. The plain close is effective once replaced by the exact current asset and standard motion.

LISTENING: not performed; full transcript and sampled frames inspected.

## Potential repair sources

Older October 9 transcripts for raw versions 1–3 were read as a donor search. They do not contain the new required “Two techniques help explain…” sentence or a clean qualified repetition explanation. Their old closing lines are obsolete. The following older version 3 passages are candidates only; their source correspondence and audio joins must be verified before use.

| Target in 4 | Candidate source and exact words | Feasibility |
|---|---|---|
| After the open-blank setup, about 0:53 | `Prompts/why-answers-vary-3.mp4`, 0:26.86–0:33.08: “At this exact blank, the AI calculates a probability for every token in its vocabulary.” | Complete beat, clear reference to the preceding blank. Under sampling board. Needs listening and source verification. |
| Replace 2:34–2:38 app sentence | Version 6, 1:14.36–1:19.80: “In ChatGPT, Gemini, and Claude, temperature is set for you behind the scenes.” | Complete sentence; the bridge before it and chart introduction after it still connect. Needs listening and level/voice check. |
| Replace 2:07–2:19 continuation beat | Older version 3, 2:02.66–2:10.44: “One slightly different token choice at a critical juncture can send the entire remainder of the generated answer in a completely new direction.” | Qualified complete sentence, though wordier than approved copy and does not itself explain the context mechanism. New narration of the approved two-part explanation is preferable. Do not delete the context relationship merely to gain “can.” |
| Replace 3:13–3:20 Other sentence | Older version 3, 3:14.16–3:17.42: “The other category comprises the vast remainder of the vocabulary.” | Complete beat under temperature board; avoids invented count. Needs listening and source verification. |

**Still unresolved:** the exact techniques transition and the qualified rationale about repetitive answers/creative variety. A new narration source is needed. Do not invent a donor, splice isolated words to add “can,” or treat corrected on-screen copy as corrected audio.

## Proposed production treatment

This is one provisional full-production plan for the preferred base, not authorization to build. Timing-dependent choices remain provisional until corrected narration is chosen. All spans below refer to version 4. Use its coherent dog-name example throughout; no TRY IT narration.

| Board / scene | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| Opening two chats | Preserve the separate Spot and Max reveals | Retain the illustrated phone scenes and question drawing, subject to motion review | 0:00–0:14.37, about 14s | Good fit to the exact two-chat narration. No title card. |
| **Why Answers Vary** | Whole Model & Thinking card, What AI Receives card, AI's Choices card at spoken onsets | Full board first; complete-card zoom only if full-view text fails readability. Never crop illustration or card copy. | Current 0:14.37–0:34.30, about 20s; extend or shorten to repaired transition. Omit the added systems diagram at 0:34–0:45 with its proposed narration cut. | Replace distorted/cropped recreation with current JPG. The replacement is standard course-board treatment, not a reason to prefer one roll's narration. |
| **Same Probabilities, Different Choices** | Open phrase; left probability section/Spot as introduced; right five-pick section as one coherent example; concluding caption | Full board to preserve the fixed distribution alongside outcomes. Preview legibility at delivery size; do not magnify only the five names and lose the unchanged-odds relationship. | 0:45.07–1:35.23, about 50s plus any vocabulary donor. Leave for the illustrated rationale. Remove 1:35–1:48 weather-distribution recap with its misleading narration. | Keep all five names once. No need to narrate every remaining probability cell. |
| Repetition, variety, and branching | Preserve useful native scene emphasis | Retain dog-grid and varied-dog drawings where corrected narration fits. Retain branching motion if review confirms clear alternate continuations. | Current 1:47.63–2:18.80, about 31s, duration will change with repaired rationale. | 1:49–1:57 dog grid, 1:57–2:07 varied drawings, 2:07–2:19 branching are promising teaching visuals. Sampled frames only: motion retention is provisional. Remove technical heading or incidental percentage only if it confuses the simplified explanation. Do not flatten useful branching motion into a still by default. |
| Sampling/temperature bridge | Selection, then adjusted probabilities; named-app text | Supporting visual; avoid implying a user-facing temperature dial in those apps | Current 2:28.23–2:38.30, about 10s; replace app sentence with donor if verified | The current dial drawing should be assessed with narration for possible user-control confusion. A plain selection/odds illustration plus app names is a targeted alternative. |
| **How Temperature Changes the Odds** | Center starting odds, low column, high column, combined Other row, then Spot comparison across three columns | Use the retained temperature demonstration for the center → low → high progression, preserving the current numbers and labels. Full comparison view for the final sentence. No cropped rows or columns. | Current 2:38.30–3:27.10, about 49s; shorten Other sentence. Do not append the extra generic token chart at 3:27–3:37. | The tall JPG is the complete reference; the retained animated layout can make the comparison more readable. Preview before final camera decisions. Highlight comparison targets together only when narration compares them. |
| **Closing Message: AI answers vary.** | Standard close treatment, no additional copy | Exact current closing JPG; prescribed hold/push/settle | Start with “AI answers vary” at about 3:36.80; end on the course close | Remove Notebook outro at approximately 3:41.80. Do not leave the course close while the required last line is being spoken. |

### Proposed cuts from version 4

ASR speech boundaries, not approved frame/sample edit points. Keep complete words and natural gaps; audition both neighboring sentences. These cuts remove about 38 seconds of added speech before any donor or replacement durations.

| Speech span | Exact text to remove | Surviving connection |
|---|---|---|
| 0:34.48–0:44.26 | “Because the model, the inputs and these internal probability mechanics interact differently in every session, the AI builds each response dynamically based on choices made in the moment.” | Overview/techniques transition → “Take a look at this probabilities chart.” |
| 1:35.46–1:46.62 | “Because the AI uses probability as a frequency guide rather than a strict mathematical rule, the exact same underlying state will naturally produce varying outputs across different attempts.” | “Another five picks could turn out entirely differently” → “Why does AI work this way?” |
| 2:18.82–2:27.28 | “Incorporating this probabilistic selection is a deliberate choice that allows the system to mimic the dynamic, varied nature of human thought in conversation.” | Repaired continuation explanation → “Sampling selects a token using probabilities.” |
| 3:27.14–3:35.82 | “Temperature acts as a focus style, tightening or loosening the AI's adherence to the most predictable path. But it never overwrites the core understanding.” | “Temperature changes its probability” → “AI answers vary.” “Focus style” is ASR wording and needs listening, but the whole added passage is unnecessary regardless. |

### Selective pauses

No added silence is proposed from transcript timing alone. Added duration: **0 seconds pending listening**. The completed example, repaired rationale, temperature comparison, and close are listening checkpoints, not automatic pause insertion points. Existing and target gaps must be measured if a later listening review proposes a pause. Donor joins also need contextual audition; no seam has been certified.

## Decision

Keep version 4 as the preferred foundation and retain the useful version 6 app sentence as a possible donor. Obtain corrected narration for the unresolved lines before committing to the production edit. Version 6's shorter runtime is not a reason to accept missing explanations. Version 5 does not offer enough unique teaching value to justify rebuilding around it.

The current lesson, prep materials, installed video, and unrelated work were left unchanged. This evaluation does not authorize or perform editing, installation, commit, or publication.
