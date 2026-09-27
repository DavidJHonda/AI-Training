# How an LLM Works — editorial shortening recommendation

2026-09-25. Scope: evaluate natural deletions from the shipped version; no video changes made.

Source: `course-assets/how-an-llm-works/how-an-llm-works.mp4`, 6:22.93, SHA-256 `5f3f2674150905c7b14d4ecf3dad2850d361ea5c4a87ff085fe47de2202d83ad`. Matches the v13 shipping record and the current `LESSON_VIDEOS.aihistory` entry in `index.html` (cache key `20260917ship1`). Hosting bytes were not independently fetched.

Basis: current page lesson, complete existing timestamped transcript, prior review and measured board spans, and visual inspection of contact sheets covering the probability entrance and ending. This is a transcript-based editorial assessment, not a fresh continuous watch/listen or certification of audio joins. Transcript times below identify sentences approximately; final cuts must be placed in the actual silences.

## Judgment

The teaching is substantially complete, but the explanation repeatedly moves from a concrete example to an abstract restatement that adds little. Recommend REPAIR for material repetition: ten sentence-level deletions totaling approximately 79.5 seconds, taking 6:23 to about 5:03. The previous KEEP review established coverage; this recommendation addresses the owner's specific concern about excess. No reroll is needed to identify these deletions. Their audible joins remain untested.

Preserve the pace of the worked examples. Training, patterns, probabilities, and repeated prediction are different teaching steps even though they reuse peanut butter. Removing a whole step would save time at the expense of understanding.

## Proposed deletions

Times refer to the existing 6:23 video, not the shortened output. Quoted sentences identify the intended cuts more reliably than the coarse transcript boundaries.

| Approximate source span | Delete | Why the teaching survives |
|---|---|---|
| 0:46.3–0:54.8 (8.5 s) | “This flowchart shows the mechanical loop used to build those patterns. We can use the peanut butter and jelly example to see how the model actually learns.” | The preceding sentence already introduces training. Go directly to “It starts with step one, read.” The example follows immediately. |
| 1:52.3–1:59.3 (7 s) | “This continuous cycle of practicing predictions and correcting internal numbers is what training means in the context of AI.” | All four steps and repetition across billions of examples have just been explained. The next sentence supplies the result: learned patterns. |
| 2:08.3–2:14.3 (6 s) | “The training process has established this sequence as a high probability pattern within the model's numbers.” | The familiar peanut-butter continuation has just been stated. Move directly to the other familiar phrases. |
| 2:35.3–2:46.3 (11 s) | “It is important to note that pattern recognition is not a separate step that happens after training is over. These patterns emerge and solidify directly as the internal numbers shift during the ongoing training loop.” | The retained next sentence says training has built patterns into the internal numbers. The initial worked training example already establishes how. This detour interrupts the transition to answering. |
| 3:18.3–3:25.3 (7 s) | “Answering a prompt is actually an active mathematical calculation of possibilities. Let's look at the exact numbers.” | Continue from the token clarification into the left-side worked example, which immediately explains calculated probabilities. |
| 3:46.3–3:50.3 (4 s) | “They aren't fixed mathematical constants shared by every AI model.” | Keep the preceding sentence explicitly identifying the percentages as illustrative. One qualification is enough. |
| 3:59.3–4:05.3 (6 s) | “The model is simply calculating the most likely continuation from the words provided so far.” | Keep “While jelly has the highest probability here, it is not a forced choice.” Then move to “Now, watch what happens when we change the text slightly.” |
| 4:42.3–4:49.3 (7 s) | “The surrounding context words are the primary variables that dynamically dictate the probability of the next word.” | The concrete 41% to 2% comparison immediately before this teaches the point more clearly. |
| 5:39.3–5:47.3 (8 s) | “This constant cycle of adding a word, updating the sentence, and recalculating probabilities is the central engine of text generation.” | Keep the preceding rule that each selected word joins the next input. Follow it with the full-paragraph explanation. That preserves the loop and its scale without a second abstract summary. |
| 5:58.3–6:13.3 (15 s) | “This entire generation process connects directly back to the initial training phase. Training changes the internal numbers to learn the patterns of language, while answering uses those established patterns to calculate what comes next.” | The distinction is established by the worked examples and the transition at 2:46–2:53. The two exact closing lines immediately repeat it. Go from the full-paragraph explanation to those closing lines. |

The probability-related cuts total about 24 seconds. Approximately 17 of those come out of the 90.6-second continuous board span; the rest remove its spoken lead-in. This improves the pace but does not by itself eliminate the long board hold.

## Teaching retained

- App versus engine; full term Large Language Model; all three components and language functions.
- Read, guess cloud, check against jelly, adjust internal numbers; repeat across billions of examples.
- Peanut butter and jelly, all three familiar phrase examples, and broader explanation/problem-solving/misspelling patterns.
- Training precedes answering; answering constructs an output rather than retrieving a complete prepared answer.
- Whole words are a teaching simplification; actual generation uses tokens.
- Both probability prompts and every listed number; illustrative numbers, remaining probability, and highest probability not being compulsory.
- The explicit jelly 41% → 2% comparison and surrounding-context explanation.
- Phone analogy; jelly → for → lunch; each chosen word updates the next input; repetition produces paragraphs quickly.
- Both closing lines unchanged.

## Provisional picture plan for these cuts

Existing treatment is the starting point. This is a narrow shortening proposal, not approval to rebuild unrelated visuals. Final output times depend on measured audio joins.

| Board | Highlights and camera | Effect of proposed cuts |
|---|---|---|
| What's an LLM? | Existing banner, Large, Language, Model sequence; full view | Unchanged. |
| How Training Works | Full view; Read, Guess, Check, Adjust, then repetition/banner as spoken | Bring the board in under the retained training introduction so it is visible before “Read.” Remove the redundant introduction and trailing definition; preserve the worked steps. |
| How AI Learns Patterns | Full view; familiar-pattern card then other-phrases card | Remove the 6-second abstract restatement. Cut the later numerical-network detour with its 11 seconds of narration. Preserve the examples and broader-pattern illustration. |
| Same Word. Different Odds. | Full view, complete left card, complete right card, full view for paired jelly comparison | The cut lead-in requires a new full-view entrance before the left-card dive, using the retained prompt introduction. Retiming is required; do not splice directly into a zoom. Preserve number onsets and paired comparison. Shorten the left-card commentary and final recap. |
| One Word at a Time | Full view; three panels then banner under the retained next-input rule | Keep the complete board walk. Start the following loop drawing on the retained full-paragraph explanation after deleting the redundant summary. |
| Close | Existing unmarked close and motion | Enter directly after the full-paragraph/speed explanation. Remove the intervening training-versus-answering drawings with their recap narration. |

No new pauses or speech-speed changes proposed. Preserve natural breaths at the joins. The probability entrance and final-close join need particular visual/audio checks. Do not use the coarse transcript boundaries as render instructions.
