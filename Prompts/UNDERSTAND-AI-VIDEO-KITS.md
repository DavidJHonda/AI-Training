# Understand AI Video Kits

Materials rebuilt 2026-09-21 on the 2026-09-20 recipe (the "Prepare a new lesson" procedure
in `Prompts/README.md`): each Markdown is the live page's teaching as prose with one
Board / Image file / Teaching content section per board and no Scene or Takeaway labels;
each prompt is under 500 words with a required-verbatim list, a beat spine, a VOICE block
and the boards-and-visuals rules; boards with faces upload as text-only faceless variants
in `Prompts/` that the canonical board replaces in the edit. All ten lessons are registered
in `Prompts/upload-sets.json` and staged in `gemini-notebook/<slug>/` by the sync.

Course order: Opener → Training → AI is Math → Tokens → Embeddings → Transformer → Layers →
Vector Space → How AI Answers → One More Thing.

Every lesson in this section has a live video shipped 2026-09-16 to 2026-09-18 under the
old method (Scene-labelled Markdown, withheld face boards, no verbatim list). David asked on
2026-09-21 for all ten to be rerolled on the new materials. The beat spines below are the
plan David approves before each roll; a roll is then judged on its narration under
`scripts/video/NARRATION-REVIEW.md` before anything visual is considered.

Exempt from the standard bundle: the AI Brain Break activity inside Layers
(`course-assets/ai-brain-break/`) and the Transformer TRY IT quiz video; neither is in a
Markdown, and each prompt names the on-page activity as not to be narrated.

## Understand AI — Opener

**v10 SHIPPED 2026-09-22** (cache key 20260922ship2, pill 2 min, 2:28): the live v7 kept on David's call after four new rolls (1-4) - roll 1 alone read the card as written but David preferred the live's narration and drawings - with four changes: the card recaptured from the page at the Work With AI opener's size and shown at full view with gold line rings; the 0:35 pause removed; the current Under the Hood illustration; the 2:21 clause and the takeaway ring removed; corner mark cleaned. Review: `video-audit/understand-ai-opener-comparison-2026-09-22/`. Previous line: Status: materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `understand-ai-opener.mp4` shipped 2026-09-16 under the old method (v7 retrofit of v4); reroll pending David's approval of the beat spine below.

**Rebuilt 2026-09-22 after roll 1 (David):** the first roll on this kit held the card for 24 s and the Under the Hood board for 21 s, because the Markdown had folded the page's prose (the PhD/six-year-old contrast, the car analogy, the "inside the machine" paragraph) into those boards' Teaching content, and opened the map with the bare label "Understand AI." because the prompt said "read its title". Markdown rebuilt: Board 1 holds the card's question and four lines only; the two paragraphs sit under `## How Can the Same Tool Do Both?`; Board 2 holds "Time to look under the hood." and its banner line; the section paragraph sits under `## Inside the Machine`; Board 3 opens "Here is what you will learn in this section, Understand AI: how AI really works." The two invented hood-up sentences are gone. Prompt rebuilt: leave the card after its fourth line, draw the contrast and the car, show Board 2 for its two lines only, introduce the map with its lead-in, never hold a board through the prose after it; banned words gain processor, mechanics, interface. Rolls 1 and 2 of 2026-09-22 and the v9 candidate built from roll 1 (`video-audit/understand-ai-opener-comparison-2026-09-22/`) predate this rebuild; David is rerolling.

**Notebook sources**

1. `lessons/Opener-Understand.md` (rewritten in place)
2. `course-assets/understand-ai-opener/understand-ai-opener-kind.jpg` (Board 1, text only)
3. `Prompts/understand-ai-opener-under-hood-faceless.jpg` (Board 2, faceless variant)
4. `course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg` (Board 3, text only)
5. `course-assets/understand-ai-opener/understand-ai-opener-close.jpg` (close)

Prompt: `Prompts/opener-understand-video-prompt.txt` (490 words).

**Post-production boards**

- `course-assets/understand-ai-opener/understand-ai-opener-under-hood.jpg` replaces the faceless variant in the edit. Reason: two photo-realistic students with visible faces (Notebook rejects or redraws face boards). The variant keeps the 1600x1308 canvas, the "Under the Hood" title and the yellow banner; the photo panel is painted with the board's own lavender background.

**Beat spine**

1. Open on the What Kind of Thing Is AI? card; read the four lines exactly (no "definitely", no "entirely", no invented "different set of rules" line). Leave the card.
2. Over Notebook's drawn scene: a PhD expert at your side one moment, a six-year-old's mistake the next; understanding what happens inside explains why.
3. The car analogy as the page tells it: good at driving without opening the hood; knowing what is underneath tells you what the car can do and why something might go wrong; the same goes for AI. Banner line: "Knowing how it works helps you Be Smarter Than the Tool." Drawn car with the hood up, no people; the Under the Hood board arrives only for "Time to look under the hood." and its banner line, then leaves.
4. Over drawn scenes: inside the machine one piece at a time; some of it new; each piece builds on the one before; no need to memorize every term; the goal is to understand how your words become an answer.
5. The section map, introduced "Here is what you will learn in this section, Understand AI: how AI really works.": all five topics in order, each with its full one-line explanation from the page (How AI Learned; Why Probability Matters; How Words Become Numbers; How Meaning Takes Shape; How AI Builds an Answer). The numbers are the learning order, not five steps AI performs on a message. Banner: "Each piece builds on the one before it."
6. Close on the two lines with nothing after.

**Required verbatim lines**

- "It’s not magic. Not a person. Not normal software. It’s its own kind of thing." (the card’s four lines, carried as one line in both the Markdown and the prompt so the stand-alone rule holds)
- "Knowing how it works helps you Be Smarter Than the Tool."
- "This section takes you inside the machine, one piece at a time."
- "The goal is to understand how your words become an answer."
- "Each piece builds on the one before it."
- "The machine won’t feel like magic anymore."
- "Take it a piece at a time."

**Guardrails carried from the old prompt or reviews**

- The section map is a learning roadmap, not a pipeline, internal sequence, system diagram, or five operations AI performs on a prompt (old prompt's central guardrail; kept as negatives in TEACH).
- Do not turn car parts or breakdowns into claims about how AI is built or why it errs (old prompt).
- No added definitions, examples, diagrams, or claims about tokens, numbers, or why answers vary; later lessons teach the mechanics (old prompt's "patterns versus facts / one number per token / more calculation causes varied answers" bans, generalized).
- Read the card lines exactly: the shipped v4 narration paraphrased them ("it's definitely not normal software", "entirely its own kind of thing", "operating by a completely different set of rules"), per the 2026-09-16 review.
- No summary after the map: the v7 repair had to cut filler ("As you move through the course...") from the end of the map span.
- No pause-and-guess exercises (old prompt; now the standard VOICE negative).
- No on-page activity exists on this opener, so no activity guardrail was needed.

**Markdown versus page**

- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): section-map title added. Removed as not on the page or boards: the "learning order, not five steps" sentence (now a prompt negative) and the connective "Here are the five topics ahead".
- Page order followed: card first (it renders above the prose), then the three paragraphs with the Under the Hood board between paragraphs two and three, then the section map, then the close.
- Kept beyond the page: one sentence on the map, "The numbers show your learning order, not five steps AI performs whenever you send a message." It is the old Markdown's guardrail against the pipeline misreading; the page implies it, and the old rolls needed it said.
- Kept beyond the page: two short sentences describing the Under the Hood board (hood up, machinery in view, "you are going to look at what is under the hood of AI") so the board has spoken content; no people are described.
- Dropped from the old Markdown: the intro sentence "This is the introduction to the Understand AI section..."; the Board 1 restatement of the car analogy ("You can learn to drive without knowing how the engine works..."); the closing restatement "As you work through the lessons, each topic will help you understand the next..."; the Takeaway labels; the post-production note. All duplicated page prose or were production copy.
- The screen-reader text under the map ("In this section", "How AI Really Works") is folded into the board's first sentence.
- "Knowing how it works helps you Be Smarter Than the Tool." appears twice (end of the car paragraph and as the board banner), as on the page.
- Nothing on the page looked wrong.

**Open questions**

- Resolved 2026-09-21 (David): the Markdown title stays "Understand AI — Opener"; it is never narrated.

## Training

**Materials updated 2026-09-27 for a fresh roll of the revised lesson.** David selected a reroll after reviewing v8: at 0:18 the repaired video jumps from basketball to setup without the AI connection, while the old connecting line arrives around 1:00. The new source makes that connection immediately and uses the current lesson’s transitions throughout. This is preparation only; no new roll has been generated or published.

The page still references the published v6 (`course-assets/training/training.mp4`, cache key `20260922ship1`, approximately 4:50). `Prompts/training-v7.mp4` and `Prompts/training-v8.mp4` remain review candidates. The v8 review is `video-audit/training-repair-2026-09-27-v8/REVIEW.md`; its provisional repair recommendation is superseded by David’s reroll decision. Workflow status in the Video Tracker was not checked or changed.

**Notebook sources — current lesson order**

1. `lessons/training.md`
2. `course-assets/training/training-before-starts.jpg`
3. `course-assets/training/training-three-phases.jpg`
4. `course-assets/training/training-guess-check-adjust.jpg`
5. `course-assets/training/training-pretraining.jpg`
6. `course-assets/training/training-instruction-tuning.jpg`
7. `course-assets/training/training-preference-tuning.jpg`
8. `course-assets/training/training-close.jpg`

Upload all eight files from `gemini-notebook/training/upload/`. Paste `gemini-notebook/training/PROMPT.txt` into the customization field; do not upload it as a source. Save the raw roll as `Prompts/training-reroll.mp4`, or the next unused numbered raw-roll filename. Preserve existing sources and candidates.

**Post-production boards**

None withheld. Setup and loop boards depict objects, without people or visible faces; the phase overview and three phase boards are text. No faceless variants are needed. The uploaded Pretraining image is the current canonical **What Pretraining Builds** version, not the older panel describing the loop again. The current canonical boards and close replace Notebook’s versions in the eventual edit.

**Beat spine**

1. Capabilities question and basketball practice analogy. Immediately connect it to AI: “AI also learns through repeated attempts. Let’s follow the process from preparation to a model that is ready to use.” Do not explain the full loop here.
2. Before Training Starts: engineers design the model and give its internal numbers starting values; teams gather books, websites, conversations, code, images, audio, and video as the curriculum.
3. Three Phases of Training: the shared question “How do I shoot a basketball?” and the three names with their one-line roles. This is orientation, not three complete explanations.
4. Explain that guess, check, and adjust applies across all three phases; examples and feedback change. Then teach The Training Loop with peanut butter and jelly: guess cloud, check against jelly, adjust the internal numbers to make jelly more likely, repeat on another example. Do not read the banner as an additional takeaway.
5. Define weights after the example, then introduce the first phase, pretraining, using the approved paragraph unchanged.
6. Pretraining: vast text and code, more than 1,000 lifetimes of reading, patterns that support writing sentences, explaining ideas and producing code; the entire fluent basketball non-answer; does not reliably follow instructions. Do not teach the loop a second time.
7. Bridge into instruction tuning: weights keep changing; the examples and feedback guide the changes. Instruction tuning uses questions paired with helpful answers; practice, compare, adjust weights. Read the complete basketball answer and explain that it can still be unclear, incomplete or unhelpful.
8. Bridge into preference tuning: following instructions is a start; feedback identifies more helpful answers. Explain multiple answers, people comparing and selecting for clarity, usefulness and accuracy, then weights adjusted toward the selected answer. Read the entire improved basketball answer, including “Use one hand to shoot and the other to steady the ball” and the final practice sentence. Retain the warning that wrong answers can sound right.
9. When training ends the model is ready to use. Ordinary chat uses the resulting weights; new information in a conversation does not change them.
10. Close with the two required lines and nothing after.

**Required verbatim passages**

- “AI also learns through repeated attempts. Let’s follow the process from preparation to a model that is ready to use.”
- “Across all three phases, training follows a basic loop: guess, check, and adjust. What changes is the examples and feedback used to guide those adjustments. Here’s a simple example.”
- “Those adjustments change the model’s internal numbers, called weights. Now, let’s look at the first phase of training, called pretraining.”
- “Training keeps adjusting the model’s weights. What changes in the next phases is the kind of examples and feedback used to guide those adjustments.”
- “Following instructions is a start. Next, the model learns from feedback about which answers people find more helpful. That’s preference tuning.”
- “Feedback helps improve the answers, but AI can still give a wrong answer that sounds right.”
- “It can work with new information you give it, but your conversation does not change those weights.”
- “AI learns from examples and feedback.”
- “Guess. Check. Adjust. Repeat.”

Each required passage is its own paragraph in the Markdown. The shared basketball question and three complete illustrative answers also remain quoted in the source; the prompt requires the sample answers word for word.

**Narration and visual guardrails**

- Preserve the immediate basketball-to-AI bridge. Do not delay it until the shared loop, and do not restore the old “AI training follows a similar pattern” opening.
- Keep setup → phase overview → shared loop → weights → detailed phases. Do not present the loop as an additional phase or as applying only to pretraining.
- Use the exact current transition paragraphs. Do not restore “Before training begins, engineers set up the model and gather the data,” backward references to an already-taught loop, or “human taste.”
- Read all three sample answers fully as illustrations, not observed product outputs. Do not add counts of examples or training runs. Keep the thousand-lifetimes comparison from the board.
- Do not imply ordinary chatting trains the model. Do not narrate the Train a Kitchen Helper activity.
- Keep boards complete and unhighlighted during generation. Simple drawn scenes support the prose between boards; no photos or photorealistic imagery. Illustrated, cartoon and stylized people are allowed.
- Reuse the approved highlight and framing approach during the eventual edit, retimed to the new narration. Measure board durations across all zooms and pans and plan useful drawing breaks from the new roll. The old v8 timestamps do not apply to a new roll.

**Markdown versus page**

The current TrainingSection in `index.html` governs teaching and order. Its prose is preserved; the opening connection is separated from the analogy by a paragraph break so the required passage stands alone. The weights-to-pretraining transition remains one paragraph. Six `##` headings separate prose from the preceding board’s Teaching content; these headings are organizational labels, not spoken chapter cards. Board text is carried as spoken sentences, including “Here is what pretraining builds” in place of a bare panel heading. No lesson-page or board change is part of this preparation.

The loop’s repeat step remains “Then repeat. The loop runs again on the next example.” The banner is not required as a separate spoken slogan, preserving David’s earlier removal of that redundant read. Both closing lines remain stand-alone sentences. The prompt is under 500 words and self-contained.

**Preparation checks**

Training-only sync and `--check` passed. All eight staged uploads and the prompt match their sources; the seven JPGs decode; the six teaching boards follow page order. The prompt is 451 words. All nine required passages occur once as stand-alone source paragraphs and match the page’s wording; all page prose is preserved. The published video’s hash is unchanged. Targeted `git diff --check` passed. No generation, upload to Notebook, publication or tracker update was performed.

## AI is Math

Materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `ai-is-math.mp4` shipped 2026-09-16 under the old method (visual-only retrofit of v3); reroll pending David's approval of the beat spine below.

**Notebook sources**

1. `lessons/ai-is-math.md`
2. `course-assets/ai-is-math/ai-is-math-the-math.jpg` (Board 1, Standard Probability)
3. `course-assets/ai-is-math/ai-is-math-two-coins.jpg` (Board 2, Counting the Possibilities)
4. `course-assets/ai-is-math/ai-is-math-conditional-probability.jpg` (Board 3, A Clue Changes the Odds)
5. `course-assets/ai-is-math/ai-is-math-what-comes-next.jpg` (Board 4, What Comes Next?)
6. `course-assets/ai-is-math/ai-is-math-close.jpg`
7. `Prompts/ai-is-math-video-prompt.txt` (496 words)

**Post-production boards**

None. All four teaching boards were screened on 2026-09-21: formula text, drawn coins with H/T letters, and word cards. No faces, no photo-realistic people, so every canonical board uploads as-is and no faceless variant exists for this lesson.

**Beat spine**

1. Open on the question of what powers ChatGPT, Claude, and every other AI, answered at once: math. A big part of that math is probability, how likely something is. "When AI builds an answer, it calculates probabilities for what comes next."
2. Where probability math began: the 1654 Pascal and Fermat letters about gambling helped lay the foundation (they did not invent probability). Start simple: when every outcome is equally likely, count the possibilities.
3. Board 1, Standard Probability: the formula in words, ways to get the result divided by total possible outcomes equals probability.
4. Board 2, Counting the Possibilities: two coins, both heads? Name all four equally likely outcomes; only heads then heads gives both heads; one divided by four is 25 percent. Banner: before new evidence, one out of four is 25 percent.
5. Conditional probability named: new evidence can change the odds, and conditional probability takes that evidence into account.
6. Board 3, A Clue Changes the Odds: someone peeks, first coin is heads. The clue rules out both outcomes that start with tails; two remain; one is both heads; one divided by two is 50 percent. Banner: after the clue, one out of two is 50 percent.
7. The hinge: the coins didn't change when someone peeked, what you knew about them did, and that moved the odds from 25 percent to 50 percent.
8. Predicting what comes next: AI uses conditional probability to build answers; the question and the words already written shape the chances of the next word; each new word joins the text and the process repeats.
9. Board 4, What Comes Next?: "What should I name my new dog?" / "You could name him ____." Spot 22 percent, Max 17 percent, Buddy 14 percent; illustrative; other words make up the remaining 47 percent. The question and the words so far are the clue, the same way the peek was. Banner: the question and the words already written shape what is likely to come next.
10. Close on the two lines, nothing after.

**Required verbatim lines**

- "When AI builds an answer, it calculates probabilities for what comes next."
- "Ways to get the result divided by total possible outcomes equals probability."
- "Before new evidence, one out of four is 25 percent."
- "After the clue, one out of two is 50 percent."
- "The coins didn't change when someone peeked. What you knew about them did."
- "The question and the words already written shape what is likely to come next."
- "AI builds answers with probabilities."
- "One prediction at a time."

The three banner lines are spoken forms of the on-board banners (the board text uses "÷", "=", and "1 out of 4 = 25%"); each stands alone on its own line in the Markdown.

**Guardrails carried from the old prompt or reviews**

- Old prompt: preserve the distinction between examples and mechanisms. Carried as "The coins show the math, not how AI works" and "Do not present those numbers as real AI output."
- Old prompt: keep qualifications that affect accuracy. Carried as "illustrative" and "remaining 47 percent" in the spine, and "helped lay the foundation, they did not invent probability."
- Old prompt: do not invent numerical values. Carried as "or change any number" plus the generic no-invented-statistics rule.
- New for this recipe: say "word," not "token" (the next lesson is Tokens and the page never uses the word); do not say AI always picks the most likely word (no temperature or settings here); do not narrate the on-page Bayesian Mind Reader activity; "Bayesian" is on the banned list because the activity's name is the only place it appears.
- REVIEW.md (2026-09-16) was a visual-only retrofit and recorded no teaching pitfalls; nothing to carry from it.

**Markdown versus page**

- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): all four board titles added; "possible outcome" label on the clue board spoken.
- Every page sentence is in the Markdown, in page order. The three SectionKicker lines became `##` headings in title case.
- Added only spoken forms of what the boards show: the four outcomes named in words, the fraction worked as a sentence ("One divided by four is 25 percent"), the "possible outcome" versus "ruled out" labels, and one connective sentence on Board 4 tying the question-plus-reply-so-far back to the peek as "the clue." That bridge restates the page's own "Your question and the words already written shape the chances of what comes next"; it adds no new claim.
- Dropped from the old Markdown: the "Takeaway:" labels and the outcome tables (rewritten as sentences), and the parenthetical "These are the illustrative probabilities on the board" (now "These probabilities are illustrative").
- Percentages are written "25 percent" rather than "25%" so the verbatim lines have one spoken form.
- Nothing on the page looked wrong. One note: the page's accessible-only ShowcaseBox for Board 1 carries the headline "The Math" while the JPG is titled "Standard Probability"; the Markdown uses the board's own title.

**Open questions**

- Resolved 2026-09-21 (David): name all four coin outcomes on both coin boards, as the page does.

## Tokens

Materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `tokens.mp4` shipped 2026-09-16 under the old method (v8 visual retrofit of v7 audio); reroll pending David's approval of the beat spine below.

**Notebook sources**

1. `lessons/tokens.md`
2. `course-assets/tokens/tokens-using-ai-feels-like.jpg` (Board 1)
3. `Prompts/tokens-building-blocks-faceless.jpg` (Board 2, text-only variant)
4. `course-assets/tokens/tokens-how-tokenization-works.jpg` (Board 3)
5. `course-assets/tokens/tokens-cat-token-id.jpg` (Board 4)
6. `course-assets/tokens/tokens-how-ai-splits-text.jpg` (Board 5)
7. `course-assets/tokens/tokens-close.jpg`

**Post-production boards**

- `course-assets/tokens/tokens-building-blocks.jpg`: two photo-realistic students (faces) and real NHL/Dallas Stars logos on their jerseys. Covered in the upload set by `Prompts/tokens-building-blocks-faceless.jpg` (same 1600x1518; photo panel repainted with the board's background and a white card carrying the board's own content: TEXT unbelievable, an arrow, TOKENS un / belie / vable, and the page line "A token can be a whole word or just part of one."; title, reuse row, banner and footer untouched). The canonical board replaces it in the edit.
- The old checklist's `tokens-building-blocks-notebook.jpg` no longer exists anywhere in the repo; the variant above was rendered fresh from today's canonical board (`?v=20260921batch3`).
- The cat board shows a photo-realistic cat but no person; screened and kept as an upload.

**Beat spine**

1. Math is the magic that powers AI, but you ask in words, not numbers.
2. Board 1: the Avengers exchange, words in and words out. Ask how words become numbers and answer right away.
3. The one-number-per-word idea, and why it breaks down: new words, names, slang, typos, emojis, code; even a million-word list falls short.
4. Definition: tokens are reusable pieces of text, whole words or parts; the full collection is the model's vocabulary; the same pieces recombine so new words need no new entry.
5. Board 2: unbelievable becomes un, belie, vable; un reused in unbelievable, unmatchable, unusual; the letters after un may span more than one token. Banner: Reuse the pieces. Build more words.
6. Where the pieces come from (taught before the chat): engineers choose the split and vocabulary size; a program builds the vocabulary from a large collection of text; each token gets a token ID, an address that says nothing about meaning; the same tokens and IDs serve training and chatting.
7. Vocabulary sizes as written: ChatGPT about 200,000, Gemini about 256,000, Claude's unpublished.
8. Board 3: the three Send steps by name (start with text, split into tokens, look up token IDs) with unbelievable and its IDs 359, 32898, 24694. Banner: Tokenization turns text into token IDs the model can use.
9. Board 4: the cat. Instant understanding for you; ID 4719 for AI; the number is not the meaning. Banner: A token ID identifies the token. Meaning comes later.
10. Bridge: all the text you send gets split into tokens.
11. Board 5: five examples with pieces and counts (unbelievable 3, basketball 2, ChatGPT 3, I ♥ AI 3, the web address on the board 8). SP is a label for a leading space, not letters the tokenizer adds; a space can join the piece after it. IDs are spoken only for unbelievable and cat; the web address is not read aloud.
12. The return trip: the reply comes out as token IDs; the tokenizer turns them back into pieces of text and joins them into the answer you read.
13. Close: "Words become numbers." / "That lets AI work with your language using math."

**Required verbatim lines**

- "Math is the magic that powers AI."
- "Instead of giving every word its own number, AI uses reusable pieces of text called tokens."
- "Reuse the pieces. Build more words."
- "Tokenization turns text into token IDs the model can use."
- "A token ID identifies the token. Meaning comes later."
- "Words become numbers."
- "That lets AI work with your language using math."

**Guardrails carried from the old prompt or reviews**

- Teach where the pieces come from before describing what happens at Send (old prompt beat 4).
- Keep every verified split, ID, and count unchanged; invent no token examples; add no processing-power or other statistics beyond the two vocabulary sizes.
- SP is only the board's label for a leading space, not text the tokenizer inserts; do not claim tokenization ignores spaces or punctuation.
- Preserve the distinction between a text piece and its numerical ID; an ID identifies, it does not mean.
- No neural-network detours; new this pass: no embeddings or vectors either, since Embeddings is the next lesson and this one stops at "Meaning comes later."
- Do not read every ID aloud (old prompt beat 6); the new prompt names unbelievable and cat as the only spoken IDs.
- The return trip must be narrated (old prompt beat 7); it is its own beat and its own Markdown section.
- Do not narrate the on-page true-or-false activity (`TokenTrueFalseTryIt`).
- The 2026-09-16 REVIEW was a visual-only retrofit and carried no teaching findings.

**Markdown versus page**

- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): all five board titles added. Removed as not on the board or page: "not letters the tokenizer adds" (now a prompt negative), the three-sentence Board 5 summary, and "A space and the piece after it can be one token."
- Kept beyond the page's prose: "The letters after un may be split into more than one token" (from the board's alt text; stops Notebook calling "believable" one token). Kept the SP-is-a-label qualifier from the old Markdown for the same reason. Kept the old Markdown's three-sentence summary under Board 5 (one word can hold several tokens; a token can include a leading space; names and web addresses split too) because it restates the board's own notes as sentences.
- Dropped: the old filler line "The lesson now asks how those words become numbers AI can use."; the "Human:"/"AI:" card prefixes from the page's accessible-only ShowcaseBox (replaced by "For you" / "For AI" sentences); Scene/Takeaway labels.
- Changed: the fifth split example is written as "the web address shown on the board" in narration lines; the URL itself appears only in the reference table so Notebook never speaks it. Board 5's tokens and IDs are also given as a table for reference; the sentences above it carry the pieces and counts.
- Page check: the page's Board 2 alt text (line 6603) describes the two students by appearance; harmless for the page, but it is why the board is post-only. Nothing on the page read as wrong.

**Open questions**

1. Resolved 2026-09-21 (David): spoken IDs stay limited to unbelievable and cat.
2. Resolved 2026-09-21 (David): the Avengers reply is narrated in full.

## Embeddings

**v5 SHIPPED 2026-09-22** (cache key 20260922ship7, pill 5 min, 4:38.33): roll 1 spine plus two audio grafts from roll 2, then four cuts and a full pass over the ring onsets on David's direction. Review: `video-audit/embeddings-stitch-2026-09-22/`; three-way comparison in `video-audit/embeddings-comparison-2026-09-22/`. **The beat spine and guardrails below are amended to match what shipped - read these, not the pre-ship versions, before any reroll.** Previous line: materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `embeddings.mp4` v6 shipped 2026-09-17 under the old method.

**Notebook sources**

1. `lessons/embeddings.md`
2. `Prompts/embeddings-student-id-faceless.jpg` (stands in for the student-ID board)
3. `course-assets/embeddings/embeddings-meaning-row.jpg`
4. `course-assets/embeddings/embeddings-new-dimension.jpg`
5. `course-assets/embeddings/embeddings-taste-test-to-ai.jpg`
6. `course-assets/embeddings/embeddings-inside-real-model.jpg`
7. `course-assets/embeddings/embeddings-close.jpg`

Prompt: `Prompts/embeddings-video-prompt.txt` (under 500 words). Save the roll as `Prompts/embeddings-reroll.mp4`.

**Post-production boards**

- `course-assets/embeddings/embeddings-student-id.jpg`: four photo-realistic students with visible faces (cafeteria, lanyard badges 1024/2048/3072/4096, fry-stealing gag). Covered in the upload by `Prompts/embeddings-student-id-faceless.jpg`: same 1600x1308 canvas, the photo panel painted with the board's own lavender background and replaced by four plain drawn ID cards carrying the same badge numbers, title and banner untouched. The canonical board replaces it in the edit.
- All other boards screened: tables and a diagram (the cat is an icon). No faces.

**Beat spine**

1. Token IDs identify but do not describe: a token ID is just a number, like a Student ID that opens the building but says nothing about who you are. Board 1: four badges, the fry gag, "An ID identifies you. It doesn't describe you." The four badge numbers are on the board and are not spoken; the gag is carried by its callback, "His ID number won't tell you he's the one who steals fries."
2. The taste test: Coke and coffee rated on six named characteristics, 0 to 10, higher means more. Board 2: Coke's row spoken in full as the worked example, coffee's row shown but not read aloud ("coffee gets a completely different set of scores"), what the scores show, "Each position always means the same thing. The number says how much."
3. The "9 for Sweet, 1 for Bitter, 10 for Fizz" question, answered Coke immediately. Then vector, dimension, value, defined in that order.
4. Pepsi joins and matches Coke on all six; the seventh dimension, Citrus (Coke 1, Pepsi 10, coffee 0), separates them. Board 3: "Six numbers match. The seventh tells them apart."
5. Bridge to AI: each token has its own row of numbers; "That row is called an embedding."
6. Board 4, all five comparison rows with both sides: what gets a row, dimensions per row, values (chosen vs learned, positive and negative with decimals), what they capture, dimension labels (none in AI). "Both use a row of numbers to describe something."
7. Board 5, the cat walk: token cat, ID 4719, its row in the embedding table, columns d1 through dn, the circled 0.45 as a value also called a parameter, the whole row as the embedding. The values along cat's row are on the board and are not read aloud.
8. Pieces of words: "unbelievable" as un, belie, vable, each with its own embedding.
9. Close on the two closing lines.

**Required verbatim lines**

- "An ID identifies you. It doesn't describe you."
- "Each position always means the same thing. The number says how much."
- "The whole row of numbers is a vector."
- "Six numbers match. The seventh tells them apart."
- "That row is called an embedding."
- "Both use a row of numbers to describe something."
- "AI uses numbers to work with meaning."
- "Those numbers help AI recognize similarities and differences."

**Guardrails carried from the old prompt or reviews**

- Do not read the embedding table cell by cell (old prompt: "do not read every table cell or token ID aloud"); only cat's row is walked, the other tokens are named as neighbours.
- Keep the analogy and the mechanism distinct (old prompt): AI's dimensions are unlabeled, not named traits like Sweet; the table's numbers are illustrative, not values from a named model.
- Do not invent numbers or diagrams to fill gaps (old prompt).
- Board-furniture ban widened 2026-09-22: the old wording banned only "this diagram, panel, or graphic shows", and roll 1 still produced "Look at this illustration...", "This table captures...", "This updated table shows..." and "This comparison chart maps...". The prompt now bans introducing a board by pointing at it at all. Two of the four came out with the v5 cuts; the other two carry teaching content and could not be lifted cleanly.
- The student-ID illustration is post-production only (old upload checklist); this rebuild adds a faceless stand-in so the ID teaching lands on a real board rather than an invented scene.
- **Superseded 2026-09-22 (David, at the v5 ship).** The 2026-09-21 guardrail read "every number spoken as a sentence (Coke, coffee, Pepsi rows, Citrus values, cat's first values, 4719, 0.45) so the narration never depends on Notebook reading a table." The rule is now: **read a number aloud only where that number is the point of its sentence.** Coke's six, the Citrus trio, 4719 and the circled 0.45 are spoken; the four badge numbers, coffee's six scores and the values along cat's row are shown and not spoken, because the board carries them and the ring points at them as they are discussed. This is exactly what three of the v5 cuts removed - do not reinstate them.

**Markdown versus page**

- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): board titles, DRINK / TOKEN ID / TOKEN column headers and the 0-to-10 scale added; Board 4 wording matched to the board. Removed the Coke/Coffee taste gloss (not on the board or page). Board 5's five other token rows remain unspoken by David's approved guardrail against reading that table cell by cell.
- Kept beyond the page: one sentence reading Board 2 ("Coke is sweet and fizzy. Coffee is bitter and hot, with much more caffeine."), a tightened version of the old Markdown's gloss; the board itself only shows the numbers. Also a sentence naming the neighbouring tokens on Board 5 (dog, latte, truck, bicycle, map), which are on the board but not in the page prose.
- Restated from the board alt text: the Board 1 scene (four badges, fry gag) so the narration can teach it over the faceless variant.
- Dropped from the old Markdown: the Takeaway labels and the three tables (all converted to spoken sentences); nothing else.
- Page check: no errors found. Board 4 says "Three drinks" while the opening prose introduces two; the Pepsi section closes that gap in order, so it reads correctly.

**Open questions**

- Resolved 2026-09-21 (David): the faceless variant keeps its drawn ID cards.

## Transformer

**v10 SHIPPED 2026-09-22** (cache key 20260922ship6, pill 4 min, 3:46): roll 2 of 2026-09-22 (8/8 required lines) with roll 3's 2017 beat grafted in (fixes "the D in ChatGPT" and restores the paper title) under the live v8's own 2017 drawing, one production sentence cut, canonical boards, and David's ring notes (no ring on the already-bordered IT chip; clue rings hug the tinted boxes); close hold faded to silence to remove the room-tone loop pulse. Rolls 1 (REROLL) and 3 (donor) retained. Review: `video-audit/transformer-comparison-2026-09-22/`. Previous line: Materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `transformer.mp4` v8 shipped 2026-09-17 under the old method (visual-only retrofit of v7); reroll pending David's approval of the beat spine below.

**Notebook sources**

1. `lessons/transformer.md`
2. `course-assets/transformer/transformer-context-problems.jpg` (Board 1, canonical; photo strip has no faces, David 2026-09-21)
3. `course-assets/transformer/transformer-before-transformers.jpg`
4. `course-assets/transformer/transformer-how-transformer-reads.jpg`
5. `course-assets/transformer/transformer-attention-transformation.jpg`
6. `course-assets/transformer/transformer-resolves-meaning.jpg` (Board 5, canonical; same strip)
7. `course-assets/transformer/transformer-word-order.jpg`
8. `course-assets/transformer/transformer-close.jpg`

**Post-production boards**

- None. Boards 1 and 5 carry a photo strip (a hand at a lamp, a shoulders-down person with a suitcase, two cats) with no visible faces. Faceless variants were rendered and then dropped on David's call (2026-09-21): the boards upload as they appear in the lesson.

**Beat spine**

1. Words in, words out; underneath, tokens, each with an embedding, a row of numbers for its starting meaning. The lesson uses whole words instead of tokens to make connections easier to see.
2. Board 1: two problems context must solve. Different meanings: LIGHT means brightness in "turn on the light," not heavy in "light enough to carry." Pronouns: IT refers to the cat when it was thirsty, the milk when it was fresh. "Context determines which meaning fits."
3. Why this was hard for AI: earlier AI read in order, one word at a time, and could lose track of earlier words. Board 2 walks the cat-and-rainstorm sentence left to right; we know IT refers to CAT. "Earlier AI often struggled to keep that connection, especially in longer passages."
4. The breakthrough: 2017, eight researchers at Google, "Attention Is All You Need," the Transformer, the T in ChatGPT. "The Transformer reads your whole message at once." Board 3: the complete message arrives together; IT can draw on CAT with several words in between; all words are present from the start.
5. Reading at once is only the start: AI has to figure out which words matter and update the numbers. Board 4: attention weighs and blends information from relevant words into the token's numbers (IT back to CAT); transformation uses learned patterns to further process those numbers (bars: IT after attention, IT with context). Both steps update the token's numbers. "Attention and transformation work together to build meaning from context."
6. "The model's learned weights stay fixed." What changes is the row of numbers for each token in your message.
7. Board 5: return to the two examples and name the clue words: "turn on" gives brightness, "carry" gives not heavy, "thirsty" gives the cat, "fresh" gives the milk. Attention and transformation help AI work out which meaning fits. Also sarcasm, idioms, and the empty "it" in "it was a cold day."
8. One catch, word order: "Dog bites man" versus "Man bites dog," same three tokens, same starting embeddings, order carries the meaning. Board 6: without positions the model cannot tell which came first; position stamps DOG 1, BITES 2, MAN 3. "Positional encoding tells the Transformer where every token belongs."
9. Close: "Attention is all you need." / "AI uses relationships between words to help interpret your message."

**Required verbatim lines**

- "Context determines which meaning fits."
- "Earlier AI often struggled to keep that connection, especially in longer passages."
- "The Transformer reads your whole message at once."
- "Attention and transformation work together to build meaning from context."
- "The model's learned weights stay fixed."
- "Positional encoding tells the Transformer where every token belongs."
- "Attention is all you need."
- "AI uses relationships between words to help interpret your message."

(Two other banners, "All words are present from the start." and "Attention and transformation help AI work out which meaning fits.", stand alone in the Markdown and are named in the beat spine but were left off the verbatim list to keep it at eight.)

**Guardrails carried from the old prompt or reviews**

- Old prompt: preserve the distinction between examples and actual mechanisms; keep the qualifications that affect accuracy; do not read every table cell aloud. Carried as: teach the Markdown's definitions of attention and transformation only, and add no mechanism beyond what the Markdown states (no layers, neural networks, self-attention, query/key/value).
- Old Markdown (Board 5): "These examples illustrate interpreting the complete sentences. They do not depict a token attending to words that come after it." Carried as a negative in the prompt: the clues come from the complete sentence; do not describe a token reaching ahead to later words.
- New, from the page's weights-stay-fixed sentence: do not say the model learns or retrains while reading your message.
- Activity exclusion: the TRY IT (`BeTheAttentionTryIt`, which plays `transformers-quiz.mp4`) is out of the Markdown and named in the prompt as not to be narrated.
- REVIEW.md (2026-09-17) was a visual-only retrofit and carries no teaching pitfalls; its one note is that the two tall boards read small at full view, which matters for the edit, not the roll.

**Markdown versus page**

- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): all six board titles added. Removed "Information from CAT had to be carried forward" (not on the board or page; now a prompt negative).
- Kept beyond the page prose, from the boards themselves: the two card lead-ins ("The same word can mean something different in each sentence." / "The same pronoun can point to a different thing in each sentence."), the two "The problem" questions with their answers spoken, "The complete message arrives together," and the Board 6 card sentences.
- Kept from the old Markdown because it clarifies Board 2: the left-to-right, word-by-word description with information from CAT carried forward to IT. Also kept: the spoken position answers (DOG 1, BITES 2, MAN 3).
- Dropped from the old Markdown: the Board 5 qualifier about not attending to later words (moved to the prompt as a guardrail rather than narrated to students); the "Takeaway:" labels and the clue table (rewritten as sentences).
- Split for the stand-alone rule: "The Transformer reads your whole message at once." and "The model's learned weights stay fixed." now sit on their own lines.
- "not-heavy" on the board is written "not heavy" for the ear.
- Page wrinkle, noted only: Board 5 presents "thirsty" and "fresh" as the clues for IT, and both words come after IT in the sentence. At sentence level this is right, but a literal narration could imply IT looks ahead. The prompt guards against that wording; the page itself is unchanged.

**Open questions**

1. Resolved 2026-09-21: Boards 1 and 5 upload as the canonical boards.
2. Resolved 2026-09-21 (David): the later-words qualifier stays prompt-only, not spoken.

## Layers

**v9 SHIPPED 2026-09-28 (David: “ship it”; cache key 20260928ship1):** `Prompts/layers-v9.mp4` (3:23.367) replaces two repeated stack breaks with new drawn illustrations: many numbers/two shown at 1:19.867–1:24.867, and successive updates to “it” at 2:19.767–2:27.200. David approved v8's narration and lesson progression; v9 preserves its AAC audio exactly and keeps all timing. Final assets and built-in imagegen prompts: `scripts/video/assets/layers-visual-variety/`. Encoded-frame, audio-identity and four transition checks passed; review: `video-audit/layers-build-2026-09-28-v9/REVIEW.md`. Installed as `course-assets/layers/layers.mp4`; runtime pill remains 3 min.

**v8 BUILT FOR REVIEW 2026-09-28 (David approved):** `Prompts/layers-v8.mp4` (3:23.367) retains v7's complete teaching and inserts the explicit horse-to-AI bridge from the new roll 3 at 0:45.167–0:49.733. Adds the horse-sentence title outline, a horse-drawing break and the inspected Transformer ACTIVE DATA illustration. Current raw rerolls `layers-1.mp4` / `layers-2.mp4` / `layers-3.mp4` were evaluated in `video-audit/layers-rerolls-2026-09-28/REVIEW.md`; build and checks are in `video-audit/layers-build-2026-09-28-v8/REVIEW.md`. David subsequently approved the narration and progression before v9; v8 is retained as its narration reference.

**REROLL MATERIALS READY 2026-09-28 (David):** the horse-to-AI connection must be spoken at the transition. The heading “AI Does Something Similar” cannot carry that teaching by itself. This supersedes the v7 review’s earlier KEEP recommendation. `Prompts/layers-v7.mp4` remains a reference candidate; the published video is unchanged. Preparation only: no generation or new edit authorized by this materials update.

**Lesson arc:** repeated reads resolve the horse sentence → explicitly connect repeated updates to AI → explain layers updating numbers → follow those updates for ‘it’ in a complete sentence → explain depth and its cost → close. The first numbers board establishes the general process; the IT/CAT board applies it without restarting the explanation.

**Current post-production plan (timings provisional until the reroll exists):**

- Horse board: full view first; outline the sentence/title during its introduction and complete reading (David’s v7 request at about 0:06), then clear it before First Read. Use complete-column outlines and the approved zoom/pan treatment for the three reads; full view for the takeaway. Fixed 4 px outlines at 720p. Count the full continuous board duration across camera moves. Prefer a relevant drawing if the new roll supplies one; do not invent filler.
- AI bridge: preserve useful new drawings. Avoid repeating v7’s single layer-stack picture throughout approximately 0:48–1:03. The current Transformer video has a usable ACTIVE DATA drawing around 2:17–2:21; consider it under the numerical-update explanation, retaining the stack for introducing layers and defining the neural network. This is a post-production donor option, not an upload or a verified final cut range. Recheck source identity and complete span before use. Reference images: `video-audit/layers-repair-2026-09-28-v7/bridge-options/`.
- Numbers board: compact full view, diagram → first pair → final pair → banner. IT/CAT: full board, sentence strip while the complete sentence is read, then one complete stage at a time. Use relevant drawing breaks following the actual new narration; do not inherit v7 timestamps.
- Keep useful original late illustrations and the canonical close. No extra pauses requested; evaluate natural pacing after generation.
- Evaluate the new roll’s spoken bridge, complete sentence, diagram relationships, and ‘it’ pronunciation before building. The original v7 donor is not needed if the new roll reads the sentence itself.

**v3 SHIPPED 2026-09-23** (cache key 20260923ship1, pill 3 min, 3:14.70): roll 6 of 2026-09-23 as the narration (rolls 5 and 6 reviewed; roll 5 donor) with audio grafts from roll 2 and the live v6, canonical boards, standard close, and the live v6's drawn animation (pronoun scene, nuance stack, architectural trade-off balance) borrowed under 2:38-3:06 on David's note that the roll's single graphic there was less engaging; the live's first animation scene ("Total Layers: 128") left out. Video title rewritten to "Meaning builds up, layer by layer." (open question 2 below, closed). Review: `video-audit/layers-comparison-2026-09-23/`. Previous line: Materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `layers.mp4` v6 shipped 2026-09-17 under the old method.

**Rolls 1 and 2 reviewed 2026-09-22** (`video-audit/layers-comparison-2026-09-22/REVIEW.md`): roll 2 earned KEEP and was built as
`Prompts/layers-v1.mp4` (`video-audit/layers-build-2026-09-22/`). David then found a defect the review had missed by reading only
transcripts: **the narrator spells the pronoun out, "I-T", every time**, because the Markdown wrote it in capitals. Word durations
confirm it - "IT" runs 0.42-0.56 s against 0.20-0.38 s for ordinary two-letter words in the same roll, while "CAT" runs 0.22-0.30 s
and is spoken as a word. **Materials updated 2026-09-22 for a second reroll** (below); the built candidate is superseded.

**2026-09-22 materials changes**

1. The pronoun and the noun are written as words in single quotes - ‘it’ and ‘cat’ - never in capitals, everywhere in the
   narration source. The boards keep their IT and CAT badges. The prompt adds the negative: read them as words, never as spelled
   letters.
2. **The middle values are no longer read.** Each number board speaks its first and final pair only; "the values shift at every
   layer" carries the rest. David, 2026-09-22: "The number rule depends on the video. We must have applied it to a lesson when we
   needed the numbers." This is a per-lesson relaxation of the speak-the-answers rule, not a repeal.
3. A rereading beat is added after Board 1, from the live v6's own wording, which David asked to keep: "Working the sentence out
   depends on each repeated pass. With every read, you update the meaning of the words until the whole thought makes sense."
4. Required verbatim line 5 becomes "AI works out that ‘it’ refers to ‘cat.’"

**Historical picture measurements:** the September 22 build notes are superseded by the current plan above and `EDIT-SPEC.md`. Measure against current assets; use full shared-white-box column boundaries and fixed 4 px strokes at 720p. Do not reuse old ring widths or partial-column bounds.

**Notebook sources**

1. `lessons/layers.md`
2. `course-assets/layers/layers-horse-three-reads.jpg`
3. `course-assets/layers/layers-inside-layer.jpg`
4. `Prompts/layers-resolves-it-lowercase.jpg` (Board 3, lowercase variant — see below)
5. `course-assets/layers/layers-close.jpg`

**Post-production boards**

- `course-assets/layers/layers-resolves-it.jpg`: the canonical board prints the pronoun as **IT** in badges and in its title, and
  every roll so far has read that as an initialism — "I-T" — because, as David put it on 2026-09-22, "Gemini Notebook thinks we
  are referring to IT as in Information Technology." Four rolls failed on it: roll 2 (0.42–0.70 s per instance), roll 4
  (0.38–0.56 s), roll 3 (mixed, and confirmed by ear), and the original v6. Writing the word in lowercase in the Markdown was not
  enough, because Notebook reads the board. `Prompts/layers-resolves-it-lowercase.jpg` is the upload copy: same 1600x835 board
  with the four IT badges reading **it**, the three CAT badges reading **cat**, and the title "How AI Connects ‘it’ to ‘cat’".
  Everything else is untouched, and the canonical board replaces it in the edit, so nothing about the shipped picture changes.
- No faces on any of the three content boards, so no faceless variants are needed.
- `layers-why-dozens.jpg` is not uploaded (see Markdown versus page).

**Beat spine**

1. English-class hook: a passage that only makes sense after a few reads; try the sentence.
2. Speak "The horse raced past the barn fell" once, then a beat of silence (David's v6 pause request carried into the narration itself).
3. Board 1, three reads by name: first read (doesn't make sense, missing word?), more reads (did the barn fall? did the horse race past afterward?), meaning clicks (someone raced a horse past a barn, then the horse fell). Banner: "Each read updates the meaning until it clicks."
4. Pivot: "AI does something similar: it builds meaning through repeated updates." Then "AI doesn’t read your message the way you do." Layers; attention and transformation update the numbers inside each layer; updated numbers pass to the next layer; like rereading, it builds on what came before.
5. Definition: "The whole stack of layers is called a neural network."
6. Board 2: numbers in, many layers, final numbers out; each row holds many numbers, two shown; the first pair (.42/−1.15) and the final pair (.19/−1.12) are spoken, the middle two are not, and the values change at every layer. Banner: "Attention and transformation update the numbers at each layer."
7. Bridge: apply the general process to one word, ‘it,’ in a real sentence; read the complete cat sentence before Start.
8. Board 3, five stages in order: start (‘it’ could refer to different things; .12/−.34 spoken), layer 1 (begins to capture the connection to ‘cat’), layer 2 (carries more information), repeat (each layer builds on the previous), result (.41/.06 spoken): "AI works out that ‘it’ refers to ‘cat.’"
9. Scale with qualifier: companies don't always share the count; published designs suggest dozens, sometimes more than a hundred.
10. Why depth: the horse sentence took a few reads; sarcasm, story twists, complicated reasoning take more; layers give AI more steps.
11. Why not keep adding layers: more computing power and time. "The extra benefit has to be worth the cost."
12. Close: "Meaning builds up, layer by layer." / "Attention and transformation. Dozens of times."

**Required verbatim lines**

- "Each read updates the meaning until it clicks."
- "AI does something similar: it builds meaning through repeated updates."
- "AI doesn’t read your message the way you do."
- "The whole stack of layers is called a neural network."
- "Attention and transformation update the numbers at each layer."
- "The cat sat on the mat during the May rainstorm because it was tired."
- "AI works out that ‘it’ refers to ‘cat.’"
- "The extra benefit has to be worth the cost."
- "Meaning builds up, layer by layer."
- "Attention and transformation. Dozens of times."

**Guardrails carried from the old prompt or reviews**

- Old prompt: keep the lesson's qualifications (companies don't always share layer counts); do not invent numerical values or diagrams; explain what the number comparison shows rather than treating the table as a recitation.
- v6 review: David asked for a one-second pause after "The horse raced past the barn fell." The prompt now asks for that beat in the narration so it need not be spliced in.
- v5/v6 review noted two photograph spans in the shipped roll; the prompt bans stock photographs and asks for drawn scenes. Current rule: no photos or photorealistic imagery; illustrated, cartoon, and stylized people are allowed.
- New, lesson-specific: do not imply a word is only two numbers; do not call the numbers probabilities or scores; do not say ‘it’ is ‘cat’ or that layer 2 is the last; read ‘it’ and ‘cat’ as words, never as spelled letters (2026-09-22); do not name a model or give an exact layer count; do not say AI thinks, understands, or has a brain; do not narrate the AI Brain Break activity; do not preview Vector Space; do not read the site address printed on the boards.
- Banned words beyond the generic list: neurons, weights, parameters, vectors, embeddings, algorithm, deep learning, garden path.

**Markdown versus page**

- September 28: the page’s “AI Does Something Similar” kicker and repeated-update explanation are expressed as a required spoken bridge in the Markdown. The live page is unchanged. Board 3’s Markdown image reference now names the actual lowercase upload variant.
- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): horse board's three panel labels added; Board 2 and 3 titles added.
- Kept beyond the page, small: one clarifying clause per read on Board 1 ("you reach 'fell' and the sentence seems to stop short"; "'raced' describes the horse, and 'fell' is what the horse did") so the narrator can explain why the sentence trips readers, since the board only shows it. Also a plain-sentence description of Board 2's picture (numbers in, line of layers, final numbers out), which the board shows but the page prose does not say.
- Numbers spoken: all board values are written as sentences (.42/−1.15 ... .19/−1.12 and IT's .12/−.34 ... .41/.06) so the comparison result ("the values shift at every layer") is stated, per the speak-the-answers rule. The old Markdown carried these as tables only.
- Dropped: the old Markdown's Takeaway labels and tables; nothing else, since the old Markdown was already page-faithful.
- `layers-why-dozens.jpg` is not on the page. `WhyDozensBox` (index.html line 7405) is defined but never rendered by `LayersSection`; the v5 review already noted "Why Dozens not in the video." Its third card matches the page prose word for word; its first card ("Plain meaning settles early. It is only a handful of layers.") and banner ("More depth leaves room for deeper meaning.") appear nowhere on the page. Excluded from Markdown and uploads.
- The "one box stays blank" cliffhanger: the task brief says the page frames Layers as a setup for Vector Space with a blank card. The current `LayersSection` has no such language, and no "blank" text exists in `VectorSpaceSection` either. The only trace is the `LESSON_VIDEOS.layers.title` string, "Meaning builds up, layer by layer — and one box stays blank." (line 1125). The Markdown follows the page and does not mention a blank box.
- AI Brain Break (`TransformerClaimsTryIt`) excluded entirely from the Markdown; the prompt names it as not to be narrated.

**Open questions**

1. Resolved 2026-09-21 (David): the Why Dozens board is no longer used; it stays out of the bundle. The unrendered `WhyDozensBox` component and its JPG are a page cleanup for another task.
2. Resolved 2026-09-21 (David): the "one box stays blank" video title is stale; rewrite it when the Layers reroll ships. The cliffhanger is not coming back.

## Vector Space

**REROLL MATERIALS READY 2026-09-28 (David):** after reviewing the live video, David requested a reroll because the opening is critical to understanding. This supersedes the Sept. 22 decision to keep the live version without another reroll. The live v5 remains unchanged. Current review: `video-audit/vector-space-live-review-2026-09-28/REVIEW.md`. These are preparation materials; no new generation or candidate has been produced.

**Notebook sources** (`lessons/vector-space.md` plus, in board order)

1. `course-assets/vector-space/vector-space-cities.jpg`
2. `course-assets/vector-space/vector-space-cities-closest.jpg`
3. `course-assets/vector-space/vector-space-taste.jpg`
4. `course-assets/vector-space/vector-space-neighborhoods.jpg`
5. `course-assets/vector-space/vector-space-closest-drink.jpg`
6. `course-assets/vector-space/vector-space-meaning-map.jpg`
7. `course-assets/vector-space/vector-space-close.jpg`

**Upload folder:** `gemini-notebook/vector-space/upload/` (eight files). Paste the separate `gemini-notebook/vector-space/PROMPT.txt` into the customization box. Save as `Prompts/vector-space-reroll.mp4`, or the next unused numbered filename.

**Post-production boards:** none withheld. The current boards have no human faces; the meaning map's animals do not require a faceless upload variant. Upload the canonical boards, including the close. Generated scenes follow the no-photos rule; the existing canonical illustration stays intact.

**Lesson arc:** numbers need not match a token's starting numbers to carry meaning; city positions demonstrate this, drink ratings extend it to more dimensions, and IT/CAT applies changing positions to context.

**Beat spine**

1. Establish embeddings and layers changing their numbers for context. Speak the complete opening question and answer from David's screenshot, verbatim, before moving to the city example. Do not replace it with a question about preserving the original meaning.
2. Three cities share two dimensions, latitude and longitude. Give their coordinates accurately, particularly Mountain View at 37 N, 122 W.
3. Two new positions: 38 N, 120 W is closest to Mountain View; 40 N, 76 W is closest to New York City. Explain the dotted connections. Explicitly return to the opening idea: the coordinates do not match a city, but their position still tells us which city is near.
4. Move from places to meaning: seven drink ratings, each row a vector. Compare Coke/Pepsi with coffee; do not read table rows digit by digit. State the city-to-drink definition and then explain the similarity map's neighborhoods, values, and short/long dotted distances.
5. Give the mystery drink's ratings and Pepsi answer. Work the comparison: first six scores match Pepsi; Citrus 9 against 10 is a gap of 1, against Coke's 1 a gap of 8. Generalize to comparing matching positions across vectors.
6. Scale to thousands of dimensions with values learned during training; similar meanings usually occupy nearby positions.
7. Read the CAT/IT sentence. Explain IT's ambiguity, the layers updating its numbers and position, and its contextual connection to CAT. Walk the starting numbers, update path, and ending numbers on the map. Connect this example back to the opening rather than presenting a detached final fact.
8. End with the two current closing lines, in order, with nothing after.

**Required verbatim passages**

The canonical list is in `Prompts/vector-space-video-prompt.txt`. It includes all six sentences from the screenshot, the closest-city callback, the city-to-drink definition, the existing required takeaway lines, and both closing lines. Each quoted passage occupies its own line in the Markdown. Evaluate these requirements on the new roll; the older live video's accepted omissions do not set the target for this reroll.

**Markdown preparation**

- Preserve the current page's teaching and wording. The opening's bold styling was removed and its sentences separated so every required line stands alone; no teaching was rewritten.
- Separate the city question, closest-city callback, city-to-drink bridge, and mystery-drink introduction from the preceding board's Teaching content using prose headings. These are transitions, not extra board narration.
- Preserve all six boards, map values, worked answers, the agreed comparison instead of a digit-by-digit table read, and both closing lines.
- Do not add a new overview board or flowchart. This lesson's examples supply the progression.

**Generation guardrails**

- Teach the opening answer immediately; do not postpone it until after the city example. Preserve the explanatory transitions.
- The maps illustrate relationships. Do not describe nearest-word lookup or literal physical movement.
- Speak IT and CAT as words, not spelled letters. Use plain source language, without “numerically quantify,” “semantic,” “coreference,” or “algorithm.”
- No invented charts, vectors, similarity scores, exact dimension/layer counts, placeholder text, logos, or URLs. No photos or photorealistic imagery. Illustrated, cartoon, and stylized people are allowed.
- Do not narrate the on-page 2048 game or production labels. Do not ask the viewer to pause or guess. No title card, preview, or extra ending.
- Board pictures accompany board teaching; drawings accompany the prose between them. Preserve useful drawn transitions for the edit, rather than planning to extend boards over every transition.

## How AI Answers

**v4 SHIPPED 2026-09-23 (David: "we can ship how-ai-answers-v4")** - `Prompts/how-ai-answers-v4.mp4`,
4:13.90, is the live `course-assets/how-ai-answers/how-ai-answers.mp4`, cache key `20260923ship1`,
pill 4 min. It is v1 with the live 9/18 video's opening grafted under Boards 1 and 2 at David's
instruction (verbatim lines 1 and 2 not spoken, 5/8), the 2:14 flash fixed, the repeated line cut, and
Board 3's middle ring blue and clear of the chips. The offered Boards 1-2 rebuild with the dive motion
(which would restore lines 1 and 2, 7/8) was not taken. Record: `video-audit/how-ai-answers-stitch-2026-09-22/REVIEW.md`.

**v1 BUILT 2026-09-22 from roll 4, awaiting David's eye test** - `Prompts/how-ai-answers-v1.mp4`,
3:46.47, four grafts and two cuts, review in `video-audit/how-ai-answers-stitch-2026-09-22/`. All
measurable checks pass: 8/8 verbatim lines, all six percentages, all four step names, guard 15/15, zero
audio dips, no true silence, 0 real corner-mark hits, 9/9 protected sources. **One blocker for the ship:
roll 4 invents a drawn scene reading `DOG: 92% CAT: 85% MOUSE: 30% CRUST: 15% FISH: 10%` at 0:56-1:01,
which says the top next token for "What should I name my new dog?" is DOG at 92% when Board 3 teaches You
at 18% a minute later.** Neither roll has a usable picture donor - roll 2 invents "Capital of France ->
Paris 76%" at the same beat and roll 3 ends its scene on a banned chapter card - so this needs David's
call: live with it, or reroll for a clean drawn scene.

**Rolls 3 and 4 of 2026-09-22 (rolled 18:00, after the 17:15 prompt amendment): roll 4 is a REPAIR and
the build base; roll 3 is a REROLL.** Roll 4 is the first of five files to speak all eight verbatim
lines, all six percentages at both prediction beats, and all four step names with "pick" said correctly.
Six edits fix the rest - one banned word ("understands"), one "word"-for-"token" slip, one always-highest
lean and three board-furniture phrases - all with identified donors from rolls 2 and 3 and boundaries
measured in quiet windows. Roll 3 rewrites both closing lines and says "AI thinking is a recursive
high-speed microcycle" ("thinks" is banned). Awaiting David's approval of the narration changes.

**Two of the three prompt edits worked; the third did not.** The line-2 collision note landed - roll 4
speaks the line verbatim, which no earlier file had - and the per-beat percentages requirement landed.
**The widened board-furniture ban failed outright**: roll 4 has five furniture phrases, the most of any
file, and roll 3 has four. Naming the constructions does not suppress them; this reads as a Notebook
house habit that prompt wording does not reach. Recommendation carried forward: stop spending prompt
words on it and cut the phrases in the edit, where four of roll 4's five lift out as whole sentences.

**Round 1 (rolls 1 and 2), superseded by the above.** Review:
`video-audit/how-ai-answers-comparison-2026-09-22/`. Roll 2 was close - 7/8 verbatim lines, Board 4's
four steps with all three percentages, no banned words, and the only one of the three that never claims
AI always picks the highest-probability token - but it missed verbatim line 2 and said "Step two is
**kick**" where the board reads Pick (confirmed real: a `small.en` re-decode biased with "Rank. Pick.
Add. Repeat." still returns "kick", and "pick" appears nowhere in the roll). Roll 1 was 0/8 and built its
explanation on the prohibited always-highest framing. The live video is 2/8 and speaks none of the six
percentages.

**The line-2 miss was a materials problem, not luck: all three files failed it the same way.** Board 2's
"The Final Token: its updated numbers are its final vector, and they help AI predict a reply that fits
the question." sits immediately before the quoted "AI uses the final token's vector to predict the first
token of its answer." The two restate each other, and every roll merged them. It is the only verbatim
line in this lesson with an adjacent restatement and the only one roll 2 missed; the other seven have no
duplicate neighbour and all seven landed.

**Fixed in the prompt, 2026-09-22 (David), not the Markdown** - the Markdown matches the page and the
page carries both lines, so changing one without the other would break the "upload Markdown = the lesson
page" rule; a copy change is a separate decision. Three edits: (1) REQUIRED VERBATIM AUDIO now says the
two Board 2 lines restate each other on purpose and must be spoken as separate sentences, not merged;
(2) each prediction beat must carry its own three percentages, since reading them once on the last board
does not cover it; (3) the board-furniture ban widened to "never introduce a board by pointing at it",
with the constructions the rolls actually produced - the old wording banned "this diagram, panel, or
graphic shows" by name and roll 2 opened with "this diagram shows" anyway. 498 -> 499 words: the three
edits cost 60 words and 60 came back out of the surrounding prose (David 2026-09-22: "They have to be
under 500."), with all eight verbatim lines and every requirement verified intact afterwards.

Previous line: materials rebuilt 2026-09-21 on the 2026-09-20 recipe (Markdown + prompt rewritten in
place); live video how-ai-answers.mp4 v6 shipped 2026-09-18 under the old method. Registry entry drafted
in tmp/understand-ai-kit/how-ai-answers.json, not yet added to Prompts/upload-sets.json.

Also open, unrelated to the rolls: `index.html:1127` gives the live 3:02.77 file a 4 min pill.

Notebook sources

1. lessons/how-ai-answers.md
2. course-assets/how-ai-answers/how-ai-answers-before-answer-begins.jpg (Board 1)
3. course-assets/how-ai-answers/how-ai-answers-where-answer-begins.jpg (Board 2)
4. course-assets/how-ai-answers/how-ai-answers-token-by-token.jpg (Board 3)
5. course-assets/how-ai-answers/how-ai-answers-building-an-answer.jpg (Board 4)
6. course-assets/how-ai-answers/how-ai-answers-close.jpg

Post-production boards

- None. All four teaching boards were screened: Board 1's Tokens panel is a 3D render of a tape-and-cutter device with no people; Boards 2 to 4 are token chips, bars, and cards. The old checklist's face board (how-ai-answers-inference.jpg, a photo strip) no longer exists; the current Board 4 is the four-card layout with no people, so no faceless variant is needed. The old checklist's "-v2" filenames are also gone; uploads use the files on disk.

Beat spine

1. Open on the new problem: AI has worked out what the words mean together, so how does it begin an answer? Set up the dog-name question; words are shown as single tokens to keep the example simple.
2. Board 1: the four steps before the answer, by name and one-line job each: Tokens, Positions, Starting Vectors, Through Layers. Banner: AI uses the final token's updated numbers to predict what comes next.
3. Board 2: the final token gathers information from every token before it; in this example the question mark is the final token; its updated numbers help AI predict a reply that fits. Banner: AI uses the final token's vector to predict the first token of its answer.
4. Starting the Answer: AI calculates a probability for every token in its vocabulary. The loop: select a token, add it to the reply, predict again with the growing context.
5. Board 3, Prediction 1: You 18 percent, A 14 percent, Great 9 percent; AI selects You in this example. Three more predictions add could, name, and him.
6. Board 3, Prediction 5: reply so far You could name him, final token him; Spot 22 percent, Max 17 percent, Buddy 14 percent; AI selects Spot in this example. Banner: You could name him Spot.
7. Why it started with You, not a dog name: each added token changes what can fit next; after You could name him a dog name becomes a likely continuation.
8. The stop: AI keeps predicting tokens until it produces a special token that signals the answer is finished.
9. Board 4: Rank, Pick, Add, Repeat, each with the dog-name example on its card (Spot 22 / Max 17 / Buddy 14; picks Spot; You could name him Spot; next token?). Banner: Inference is the process AI uses to generate an answer one token at a time.
10. Close on the two lines, nothing after.

Required verbatim lines

- "AI uses the final token's updated numbers to predict what comes next."
- "AI uses the final token's vector to predict the first token of its answer."
- "You could name him Spot."
- "Each added token changes what can fit next."
- "AI keeps predicting tokens until it produces a special token that signals the answer is finished."
- "Inference is the process AI uses to generate an answer one token at a time."
- "Every answer is built one token at a time."
- "The whole run is called inference."

Guardrails carried from the old prompt or reviews

- Keep the page's distinction between examples and mechanism: the picks of You and Spot are "in this example"; do not say AI always picks the highest-probability token (the page never says so, and the v6 review kept the picks framed as examples).
- Do not say AI plans or knows the whole answer in advance; the page's point is that it began with You, not a dog name.
- Do not invent tokens, percentages, dog names, or diagrams beyond the Markdown (old prompt: "Do not invent numerical values or diagrams to fill gaps").
- Speak the percentages as sentences rather than a cell-by-cell table read (old prompt: explain what the comparisons show; new recipe: speak the answers). Every number on Boards 3 and 4 is now written as a sentence in the Markdown.
- Do not narrate the on-page TRY IT (PredictionLoopTryIt: the floating-ice question with Ice / floats picks).
- After the setup sentence, say token, not word; banned lesson-specific words: algorithm, neural network, autocomplete, sampling, temperature, guess, understands, thinks, knows.
- Web address on the boards' credit line must not be spoken or shown separately.

Markdown versus page

- Kept beyond the page: "In this example, the question mark is the final token." (from the old Markdown; the Board 2 image labels the ? as FINAL TOKEN and the page prose never says it aloud, so the sentence clarifies the board). Also kept the old Markdown's connective "Follow the repeating process..." as the Board 4 intro, reworded.
- Added for the ear only: a one-line reading of the Board 2 token row (What, should, I, name, my, new, dog, question mark), the Board 4 "answer so far" line and per-card examples written out (Rank scores, Pick Spot, Add makes You could name him Spot, Repeat asks for the next token), and "The completed answer is a full sentence." as a lead-in so the banner "You could name him Spot." stands alone. Percentages are written as "18 percent" etc. so Notebook speaks them.
- Dropped from the old Markdown: its board step wording ("Break the question into small pieces", "Represent each token's starting meaning with numbers", "using information from the message"), replaced with the current board text; the Scene/Takeaway labels; the Markdown tables; "Each prediction uses the growing context." (page prose already says it).
- Temperature: the page does not hold it, so the Markdown and prompt do not mention it (the prompt bans the word).
- Page wording check: nothing looked wrong. One note: the page's Board 3 lists a probability for "A" at 14 percent and Board 4's Rank card shows Buddy at 14 percent; the coincidence is on the page, not an error.

Open questions

- The verbatim list is at the recipe's ceiling of eight. If David wants it shorter, "You could name him Spot." is the line most likely to land unprompted and could be cut to seven.

**Markdown versus page**

- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): all four board titles and the step numbers added; FINAL VECTOR label folded in. The question-mark sentence stays: Board 2 labels the tile FINAL TOKEN.

## One More Thing

Reroll materials updated 2026-09-28 after David’s v12 review. Live video remains `one-more-thing.mp4?v=20260923ship3`; v12 is a visual-repair review candidate, not the new narration. The new closing copy and canonical closing JPG are updated locally. No video published.

- Prompt: `Prompts/one-more-thing-video-prompt.txt` (464 words).
- Narration source: `lessons/one-more-thing.md`.
- Ready-to-upload folder: `gemini-notebook/one-more-thing/upload/` (Markdown and four JPGs).
- Paste `gemini-notebook/one-more-thing/PROMPT.txt` into customization; do not upload it as a source.
- Canonical uploads: `one-more-thing-draws.jpg`, `one-more-thing-temperature.jpg`, `one-more-thing-bill.jpg`, `one-more-thing-close.jpg`, all from `course-assets/one-more-thing/`.
- No face variants or post-only boards. All three teaching boards remain unchanged.
- Save as `Prompts/one-more-thing-reroll.mp4`, or the next unused numbered filename.

### Lesson arc and scene directions

The same dog-name example connects three questions: why unchanged odds can produce different choices, how temperature changes those odds, and how much calculation each token requires.

1. Start immediately with the three questions. Give each its own relevant visual: changing answer paths → contrasting odds → calculation scale. This visual preview accompanies the existing questions; no extra preview speech or title card. Introduce the dog only when the narration reaches the example. Avoid the previous opening’s consecutive dog holds.
2. Establish the open token in “You could name him…” and Spot leading at 22%. Explain about 22 selections out of 100, on average, if the odds stay the same. Use a consistent unfinished sentence throughout; avoid the old generated “The dog was Max…” paths.
3. **Same Probabilities, Different Choices:** retain the unchanged odds and the five picks in order, Max, Spot, Buddy, Rex, Max. They are separate selections at the same open token, one possible set, not five tokens in one reply. Spot appears once despite the highest probability. Another set could differ. No recital of all six percentages: the printed table stays available for reference.
4. Leave the board for the two connected ideas: other likely choices add variety, and one changed token changes what follows. The Markdown gives this prose its own section so it can receive drawn scenes.
5. Bridge explicitly: “So what changes how predictable those choices are?” Immediately answer with the temperature definition. Return visually to the same starting odds, then compare how they change.
6. **How Temperature Changes the Odds:** explain low versus high using Spot’s 22% starting chance, 36% at low and 16% at high. Explain what happens to less likely choices. Do not recite every cell or tell viewers to adjust a slider. Preserve the distinction between reshaping probabilities and changing what the model learned.
7. Bridge: “Every choice starts with calculations. Now count what an answer takes.” Training created the weights; they stay fixed during use. Draw the imagined trillion-weight model and the roughly two-calculations-per-weight explanation.
8. **The Math Adds Up Fast:** walk through one token ≈ 2 trillion calculations, 100 generated tokens ≈ 200 trillion, and 1,000 generated tokens ≈ 2 quadrillion. Keep the generated-token scope and imagined-model qualification. Use relevant drawn scenes at conceptual transitions; do not force continuous board holds.
9. End with “Math and probability, one token at a time.” Then “Every time you hit send.” Nothing after. The close now ties together choices, temperature and calculations.

### Required verbatim audio

The prompt contains twelve required passages, each standing alone in the Markdown: the 22%-over-100 explanation; Spot picked once / another five could differ; best chance is not a guarantee; the temperature connecting question; temperature’s definition; the named apps handling it behind the scenes; temperature’s learning distinction; the bridge to calculations; weights stay fixed; even a short answer takes trillions; and both new closing lines.

### Source decisions and review priorities

- David approved reducing numerical recitation on 2026-09-28. This lesson’s narration source intentionally does not transcribe every probability-table cell. Preserve the unchanged-odds relationship, five outcomes and low/high contrast. The source JPGs retain all numbers.
- The temperature and math bridges are video narration additions grounded in the existing lesson. Page prose remains unchanged; the approved closing message is updated in the page, Markdown and closing JPG.
- Review the generated opening for three meaningful visual beats, not two dog views. Review whether the temperature question receives an immediate answer and a visual connection to the same example.
- Board timings and outline onsets must be measured against the new roll. Use current Edit Spec: full-board introductions, fixed 4px outlines, purposeful drawing breaks. Do not inherit v12 timing. Highlight the five picks as spoken where it helps follow the sequence; a percentage recital is not requested.
- Keep numbers hypothetical; no real model sizes, hardware or cost claims. No on-page “How Big Is 2 Quadrillion?” activity narration. Do not add technical labels such as sampling, softmax, parameters or FLOPs.
- Older One More Thing raw rolls were not found locally during the review. The live file contains reusable branching and calculation scenes, but the reroll should supply a coherent new opening and transitions.
