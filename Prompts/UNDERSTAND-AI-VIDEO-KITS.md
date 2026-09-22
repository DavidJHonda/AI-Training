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

**v6 SHIPPED 2026-09-22** (cache key 20260922ship1, pill 5 min, 4:50): roll 1 of 2026-09-22 as the narration with six of its own additions cut (production phrases, a garbled line, the summary after the phases, and, on David's note, the word-for-word banner read) and two audio grafts from the live v4 ("steady the ball"; "the heavy lifting is done… ready for public use"); canonical boards, the phase boards dense with section dives, standard close. Review: `video-audit/training-comparison-2026-09-22/`. Previous line: Materials rebuilt 2026-09-21 on the 2026-09-20 recipe. Live video: `training.mp4` v4, shipped 2026-09-16 as a visual retrofit of a 2026-09-09 roll; reroll pending David's approval of the beat spine below.

**Notebook sources**

1. `lessons/training.md`
2. `course-assets/training/training-guess-check-adjust.jpg`
3. `course-assets/training/training-before-starts.jpg`
4. `course-assets/training/training-three-phases.jpg`
5. `course-assets/training/training-pretraining.jpg`
6. `course-assets/training/training-instruction-tuning.jpg`
7. `course-assets/training/training-preference-tuning.jpg`
8. `course-assets/training/training-close.jpg`

**Post-production boards**

- None. All six teaching boards were screened: Boards 1 and 2 carry 3D-rendered objects (machines, scales, a dial, layered grids, conveyors) with no people or faces; Boards 3 to 6 are text only. No faceless variants were made.

**Beat spine**

1. Hook: AI can explain chemistry, write code, and improve an essay. How did it learn?
2. Basketball analogy: shoot, check where it goes, adjust aim or force.
3. Training follows the same pattern, guess, check, adjust, but adjusts the numbers inside the model, not aim or force.
4. Board 1, The Training Loop: the peanut butter and jelly example; guess cloud; check against jelly, no match; adjust the internal numbers so jelly is more likely; the loop runs again; banner "Repeat with more examples. The patterns build."
5. Board 2, Before Training Starts: set up the system (engineers design the model, give its numbers starting values, training will adjust them); gather the data (books, websites, conversations, code, images, audio, video; this becomes the curriculum).
6. Bridge: training also teaches the model to follow instructions and give more useful answers; we follow one basketball question through three phases.
7. Board 3, Three Phases: orientation only. The shared question "How do I shoot a basketball?" and the three phase names with their one-line roles. No full explanation here.
8. Board 4, Pretraining: vast amounts of data, more than 1,000 lifetimes of reading; guess what comes next, check against the example; "Training adjusts its internal numbers, called weights."; learns to write sentences, explain ideas, produce code; sample answer read in full; still needs work: fluent but does not reliably follow instructions.
9. Board 5, Instruction Tuning: questions paired with helpful example answers; model practices, compares its guesses with the examples; weights adjusted toward the examples; sample answer read in full; still needs work: may be unclear, incomplete, or unhelpful.
10. Board 6, Preference Tuning: one question, several answers; people pick the best (clear, useful, accurate); weights adjusted so answers like the chosen one are more likely; sample answer read in full to its last sentence; "Feedback helps improve the answers, but AI can still give a wrong answer that sounds right."
11. When training ends the model is ready to use; a normal chat uses the trained weights; it can work with new information you give it, but the conversation does not change the weights.
12. Close: "AI learns from examples and feedback." then "Guess. Check. Adjust. Repeat." Nothing after.

**Required verbatim lines**

- "AI training follows a similar pattern: guess, check, and adjust."
- "Repeat with more examples. The patterns build."
- "How do I shoot a basketball?"
- "Training adjusts its internal numbers, called weights."
- "Feedback helps improve the answers, but AI can still give a wrong answer that sounds right."
- "It can work with new information you give it, but your conversation does not change those weights."
- "AI learns from examples and feedback."
- "Guess. Check. Adjust. Repeat."

**Guardrails carried from the old prompt or reviews**

- Three Phases board is an orientation only: shared question plus phase names and one-line roles; each phase is then named explicitly as its own board appears; do not repeat the orientation afterward (old prompt).
- Keep the analogy and the mechanism apart: the basketball is the analogy; training adjusts numbers, not aim or force (old prompt's "preserve distinctions between analogies and mechanisms").
- Follow the page's board order, Training Loop before Before Training Starts; the 2026-09-09 roll swapped them (REVIEW.md).
- Name all seven data kinds; the live roll dropped audio and video (REVIEW.md).
- Read all three sample answers in full; the live roll trailed off partway through the third (REVIEW.md).
- Do not add counts of examples or runs; the live roll's "millions of times" was accurate but is an invented figure under the new recipe.
- "hallucinate" added to the banned list: the live roll used it and the review accepted it, but the lesson does not use the word.
- Do not imply chatting teaches the model (closing paragraph's distinction).
- Do not narrate the Train a Kitchen Helper TRY IT.

**Markdown versus page**

- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): loop board steps now in the board's exact words plus "Then repeat."; Three Phases title and all six labels added; the "What an Answer Might Look Like" and "Learn to..." sub-headers folded into each phase board. Dropped "cloud does not match" (on neither board nor page).
- Kept beyond the page: nothing. The old Markdown already matched the page one to one; it was restructured, not expanded.
- Spoken adaptations: Board 1's blank ("Peanut butter and ___") is written as "with the last word missing"; the Check step states the result ("cloud does not match"), which the board leaves implied; each phase board opens with "Phase N is ..." so the narrator names the phase on entry; the sample answers are introduced as "an answer to the basketball question might look like this" instead of the card heading.
- Split for the stand-alone rule: "AI training follows a similar pattern: guess, check, and adjust." and "Training adjusts its internal numbers, called weights." were pulled out of their paragraphs; the closing paragraph's last sentence stands alone.
- Dropped: the old Markdown's bold labels, numbered lists, and "Takeaway" label.
- Page looked wrong nowhere. One note: the page's Board 1 alt text uses "Given ‘Peanut butter and ___,’" with a literal blank, which is fine on screen but unreadable aloud; handled in the Markdown as above.

**Open questions**

- None.

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

Materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `transformer.mp4` v8 shipped 2026-09-17 under the old method (visual-only retrofit of v7); reroll pending David's approval of the beat spine below.

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

Materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `layers.mp4` v6 shipped 2026-09-17 under the old method.

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

**Picture fixes measured for the next build** (they live in `scripts/video/build_layers_v1.py`, not in the roll): the board title
is ringed while the sentence is spoken (46, 48-961, 89); Board 1's read rings end at the illustration's bottom edge, y 780, not
the white box's 818; Board 2 is compact throughout with no dives; its diagram ring widens to x 48-1552 so it clears the NUMBERS IN
and FINAL NUMBERS labels; and its number-card rings take each card's own border, y 860-992 with x 74-389, 453-768, 832-1147 and
1212-1526, where the first build sat about ten pixels proud top and bottom.

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
4. Pivot: "AI doesn't read your message the way you do." Layers; attention and transformation update the numbers inside each layer; updated numbers pass to the next layer; like rereading, it builds on what came before.
5. Definition: "The whole stack of layers is called a neural network."
6. Board 2: numbers in, many layers, final numbers out; each row holds many numbers, two shown; the first pair (.42/−1.15) and the final pair (.19/−1.12) are spoken, the middle two are not, and the values change at every layer. Banner: "Attention and transformation update the numbers at each layer."
7. Bridge: follow one word, IT, through the layers.
8. Board 3, five stages in order: start (‘it’ could refer to different things; .12/−.34 spoken), layer 1 (begins to capture the connection to ‘cat’), layer 2 (carries more information), repeat (each layer builds on the previous), result (.41/.06 spoken): "AI works out that ‘it’ refers to ‘cat.’"
9. Scale with qualifier: companies don't always share the count; published designs suggest dozens, sometimes more than a hundred.
10. Why depth: the horse sentence took a few reads; sarcasm, story twists, complicated reasoning take more; layers give AI more steps.
11. Why not keep adding layers: more computing power and time. "The extra benefit has to be worth the cost."
12. Close: "Meaning builds up, layer by layer." / "Attention and transformation. Dozens of times."

**Required verbatim lines**

- "Each read updates the meaning until it clicks."
- "AI doesn't read your message the way you do."
- "The whole stack of layers is called a neural network."
- "Attention and transformation update the numbers at each layer."
- "AI works out that ‘it’ refers to ‘cat.’"
- "The extra benefit has to be worth the cost."
- "Meaning builds up, layer by layer."
- "Attention and transformation. Dozens of times."

**Guardrails carried from the old prompt or reviews**

- Old prompt: keep the lesson's qualifications (companies don't always share layer counts); do not invent numerical values or diagrams; explain what the number comparison shows rather than treating the table as a recitation.
- v6 review: David asked for a one-second pause after "The horse raced past the barn fell." The prompt now asks for that beat in the narration so it need not be spliced in.
- v5/v6 review noted two photograph spans in the shipped roll; the prompt bans stock photographs and asks for drawn scenes with no people.
- New, lesson-specific: do not imply a word is only two numbers; do not call the numbers probabilities or scores; do not say ‘it’ is ‘cat’ or that layer 2 is the last; read ‘it’ and ‘cat’ as words, never as spelled letters (2026-09-22); do not name a model or give an exact layer count; do not say AI thinks, understands, or has a brain; do not narrate the AI Brain Break activity; do not preview Vector Space; do not read the site address printed on the boards.
- Banned words beyond the generic list: neurons, weights, parameters, vectors, embeddings, algorithm, deep learning, garden path.

**Markdown versus page**

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

**LIVE VIDEO KEPT 2026-09-22 (David):** two rolls on this kit were reviewed (roll 1 REPAIR with 7/8 required lines; roll 2 donor) and a candidate built, then David rewrote the page's opening and the drinks-table read, re-evaluated the live v5 against the new page, and kept it: it teaches the lesson, reads the drinks table the new way, and its boards match. Candidates removed; rolls retained. Review: `video-audit/vector-space-comparison-2026-09-22/`. Do not re-propose a reroll without a page change. Previous line: Materials rebuilt 2026-09-21 on the 2026-09-20 recipe; live `vector-space.mp4` v5 shipped 2026-09-17 under the old method (visual-only retrofit of the 2026-09-10 roll); reroll pending David's approval of the beat spine below.

**Notebook sources** (`lessons/vector-space.md` plus, in board order)
1. `course-assets/vector-space/vector-space-cities.jpg`
2. `course-assets/vector-space/vector-space-cities-closest.jpg`
3. `course-assets/vector-space/vector-space-taste.jpg`
4. `course-assets/vector-space/vector-space-neighborhoods.jpg`
5. `course-assets/vector-space/vector-space-closest-drink.jpg`
6. `course-assets/vector-space/vector-space-meaning-map.jpg`
7. `course-assets/vector-space/vector-space-close.jpg`

**Post-production boards:** none. All six boards were screened 2026-09-21; none shows a human face or a photo-realistic person. The meaning map is photo-realistic but its only figures are a cat, a dog, and a kitten, so it uploads as-is. No faceless variants exist for this lesson.

**Beat spine** (approve before rolling)
1. Open on the page's question: embeddings are rows of numbers; the layers change them; if the numbers are different, how do they still represent meaning? This is the page's own hand-off from the Layers cliffhanger; nothing about a blank card is added.
2. Map: latitude and longitude, Dallas at 33° N 97° W, three cities as the only cities on the map (Board 1, banner "Latitude and longitude give each city a position").
3. Two new positions, answered in the next sentence: 38° N 120° W is closest to Mountain View; 40° N 76° W is closest to New York City (Board 2, banner "When nothing matches exactly, distance finds the closest one"). Nothing matched exactly; comparing positions still finds the closest city.
4. From places to meaning: seven ratings per drink, each row a vector; the three rows read aloud; Coke and Pepsi match on six and differ only on Citrus (1 vs 10); coffee differs on all seven (Board 3, banner "Coke and Pepsi have more similar profiles than either does to coffee").
5. Definition: seven ratings give a drink a position in a seven-dimension space; that's vector space. Picture it on a map: Coke and Pepsi close, coffee farther (Board 4, soft drinks / hot drinks neighborhoods, dotted lines short vs long).
6. Mystery drink 9, 1, 10, 2, 3, 8, 9, answered in the same breath: closest match is Pepsi (Board 5, banner "The mystery drink's ratings are closest to Pepsi's").
7. Distance: first six match Pepsi; Citrus gap 1 vs Pepsi, 8 vs Coke; compare numbers in matching positions; "Smaller gaps mean closer positions."
8. Scale up: thousands of dimensions, values learned during training, similar meanings usually nearby.
9. When the numbers change: the CAT/IT sentence; IT could refer to many things; the layers update IT's numbers to connect it to CAT; changing numbers changes position (Board 6: starting numbers .12, −.34 …, path "The layers update the numbers," updated .41, .06 … beside CAT in the animals neighborhood; banner "IT's new position reflects its connection to CAT in this sentence").
10. Close on the two lines, nothing after.

**Required verbatim lines** (8)
- "Just as latitude and longitude give a city a position, a drink's seven ratings give it a position in a space with seven dimensions. That's vector space."
- "When nothing matches exactly, distance finds the closest one."
- "Coke and Pepsi have more similar profiles than either does to coffee."
- "The mystery drink's ratings are closest to Pepsi's."
- "Smaller gaps mean closer positions."
- "IT's new position reflects its connection to CAT in this sentence."
- "Meaning is a position in vector space."
- "Similar meanings usually sit close together."

Each stands alone on its own line in the Markdown. Banners 1 and 4 ("Latitude and longitude give each city a position"; "Similar scores place Coke and Pepsi close together in the soft drinks neighborhood") are in the Markdown as stand-alone sentences but left off the verbatim list to keep it at eight.

**Guardrails carried from the old prompt or reviews**
- Speak the answers (the old prompt was the course's reference for this): both closest-city answers and the Pepsi answer are stated as sentences immediately after each question in the Markdown, and the prompt names them.
- Read the values a comparison depends on, not every table cell; the prompt says "reading the values the comparison depends on."
- Preserve the analogy/mechanism distinction: the map pictures the change; do not say the model looks up the nearest word on a map (the old Markdown carried this as a narrated disclaimer; it is now a prompt negative only).
- Keep "usually" on similar meanings sitting together (page wording; the prompt says "similar meanings usually nearby").
- No invented numbers, formula, extra cities/drinks/dimensions, or a real model's dimension count.
- Do not narrate the Rock, Paper, Patterns game (`Game2048TryIt`).
- Coke and Pepsi are real brands: the prompt bans real logos or brand marks.
- REVIEW.md (2026-09-17) was a visual-only retrofit and recorded no teaching pitfalls; the 2026-09-10 roll's narration was kept as-is, which is why the reroll is the first roll on this recipe.

**Markdown versus page**
- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): all six board titles added; Board 2 city coordinates, Board 3 and 5 headers and score rows, the mystery-drink label and the Pet bowl label spoken. Removed the Board 3 column comparison and the Board 6 mat/rainstorm sentence (not on the board or page).
- Kept beyond the page: (a) explicit column comparison under Board 3 ("Coke and Pepsi match on the first six dimensions and differ only on Citrus, where Coke scores 1 and Pepsi scores 10. Coffee's ratings differ from both on every one of the seven") so the banner is earned in narration rather than asserted; (b) one sentence under Board 6 noting the mat and the rainstorm are also in the sentence, so IT might have pointed to either, which is why the map has objects and weather neighborhoods; (c) a short-vs-long dotted-line sentence under Board 4 describing what the board draws.
- Dropped from the old Markdown: the Scene/Takeaway labels and Markdown tables (recipe); the narrated disclaimer "It does not mean the model identifies a word's meaning by looking up the nearest original token embedding" (moved to the prompt as a negative); the duplicated closest-city and Pepsi paragraphs the old file carried twice.
- Page sentence changed for the ear only: "Let's see how this works in vector space:" ends with a period; the bulleted coordinates and mystery ratings became sentences with degree words spelled "north"/"west" as the page's own prose does for Dallas.
- Nothing on the page looked wrong.

**Open questions**
- Resolved 2026-09-21 (David): the narration follows the page and does not name a blank card; the Layers cliffhanger is retired, so no page edit is needed.

## How AI Answers

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

Materials rebuilt 2026-09-21 on the 2026-09-20 recipe (Fake Trap template). Live video: `one-more-thing.mp4` v5, shipped 2026-09-18 as a visual-only retrofit of the old-method roll; reroll pending David’s approval of the beat spine below.

- Prompt: `Prompts/one-more-thing-video-prompt.txt` (497 words)
- Markdown: `lessons/one-more-thing.md`
- Notebook sources:
  1. `course-assets/one-more-thing/one-more-thing-draws.jpg`
  2. `course-assets/one-more-thing/one-more-thing-temperature.jpg`
  3. `course-assets/one-more-thing/one-more-thing-bill.jpg`
  4. `course-assets/one-more-thing/one-more-thing-close.jpg`
- Post-production boards: none. All three teaching boards were screened; each is typography, bars, dots and squares only, with no faces or photo-realistic people, so the canonical files upload as-is and no faceless variants were made.

### Beat spine

1. Open on the three questions: why the same prompt can give a different answer, what makes answers more predictable or more varied, how much math one answer takes. No title card.
2. Dog-name example: AI calculates a probability for every token; Spot leads at 22%; the top choice is not guaranteed; 22% means about 22 picks in 100 tries, on average, if the odds stay the same.
3. Board 1: all six probabilities (Spot 22, Max 17, Buddy 14, Rex 9, Biscuit 6, other 32), the five separate tries in order (Max, Spot, Buddy, Rex, Max), Spot came up once; separate selections at the same point, not five tokens in one reply; one possible set, not a required pattern. Banner: “The best chance is not a guarantee.”
4. Two important points: always picking the top token can make answers repetitive; one different token can send the answer in a new direction.
5. Temperature defined in the page’s words (the app reshapes the probabilities before AI picks a token); low makes likely choices more likely, high gives less likely choices a better chance.
6. Board 2 column by column with every number: starting odds, low temperature (Spot 36, Max 21, Buddy 15, Rex 6, Biscuit 3, other 19), high temperature (Spot 16, Max 14, Buddy 13, Rex 10, Biscuit 8, other 39). Spot 22 to 36 to 16; each column adds to 100; Spot stays the single most likely name. Banner: “Temperature reshapes the probabilities. It does not change what the model learned.”
7. Weights: training created them; they stay fixed in use; each new token uses them in a massive set of calculations. The imagined trillion-weight model at two calculations per weight gives about two trillion per token.
8. Board 3 with the multiplication: one token about 2 trillion; 100 tokens about 200 trillion; 1,000 tokens about 2 quadrillion. Counts cover tokens AI writes; estimates for an imagined model, not measurements. Banner: “Even a short answer takes trillions of calculations.”
9. Close on the two lines, nothing after.

### Required verbatim lines

1. “A 22% probability means AI would pick Spot about 22 times out of 100 tries, on average, if the odds stay the same.”
2. “The best chance is not a guarantee.”
3. “Behind the scenes, the app uses a setting called temperature to reshape the probabilities before AI picks a token.”
4. “Temperature reshapes the probabilities. It does not change what the model learned.”
5. “When you use AI, those weights stay fixed.”
6. “Even a short answer takes trillions of calculations.”
7. “Not a mind. Math, at a scale nobody can picture.”
8. “Every time you hit send.”

All eight stand alone on their own line in the Markdown (the 22% sentence, the temperature definition, and the weights line were split out of their page paragraphs).

### Guardrails carried from the old prompt or reviews

- Keep the page’s distinction between the imagined trillion-weight model and real mechanisms: the prompt says to present it as imagined and bans naming real models, weight counts, hardware or costs (old prompt: “preserve distinctions between examples, analogies, estimates, and actual mechanisms”).
- Do not invent numbers: every figure the narration may speak is written as a sentence in the Markdown, and the prompt says “add no other numbers” (old prompt: “do not invent numerical values”).
- Five tries are separate selections at the same point, not one reply that lists five names and not a reroll the user sees (old Markdown note, kept).
- The 2026-09-18 REVIEW.md is a visual-only retrofit record (ring states, close swap) and carries no narration verdicts; nothing further to carry.
- Recipe-level: no on-page activity narration (the “How Big Is 2 Quadrillion?” TRY IT with burgers, coins, Coke and horses is excluded), no URLs (the boards’ besmarterthanthetool.com credit is not spoken), close lines last with nothing after.

### Markdown versus page

- Board-coverage pass 2026-09-21 (David: the Markdown matches the lesson, and every printed point on a board must be in it because Notebook sometimes skips them): all three board titles, try numbers, the Name header and the trillion-weights caption added. Removed "separate selections / not five tokens" (now a prompt negative) and "each column adds up to 100%" (not printed anywhere); "more evenly" dropped.
- Kept beyond the page (clarifies the board): “These are five separate selections at the same point in the answer, not five tokens in a row in one reply. They show one possible set of outcomes, not a required pattern.” (Board 1 says “One possible set”.) Also “Each column adds up to 100%” for Board 2 (verified: all three columns sum to 100).
- Added as spoken answers derived from the boards: “Spot, the top choice, came up once in five tries”; “Spot’s chance goes from 22% to 36%”; “Temperature changes how far ahead the top choice is” (the Spot-stays-most-likely clause was cut on David’s call); the two multiplications on Board 3 (100 × 2 trillion, 1,000 × 2 trillion); “estimates for an imagined model, not measurements of a real one.”
- Dropped from the old Markdown: “They do not assume that all earlier work is repeated for every new token.” It is not on the page, and spoken aloud it raises a mechanism the lesson never explains. The prompt instead bans extra numbers and real-model claims.
- Dropped old tables and Takeaway labels; banner lines carried as plain sentences.
- Page check: the three boards and prose agree with each other; no errors found. Minor: the page shows the close board before the TRY IT, so the video’s close matches the page’s teaching end.

### Open questions

- Resolved 2026-09-21 (David): the derived line “Spot stays the single most likely name in every column” is cut from the Markdown; the column now ends “Temperature changes how far ahead the top choice is.”

