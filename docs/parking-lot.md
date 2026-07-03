# Parking Lot — cut-but-keepable lesson content

Content removed from a lesson but worth reusing later. Each entry: what it is, where it came from, the verbatim source, and where it might go.

---

## "Bayes' Theorem in Action" — bag-of-basketballs SEE IT

- **Origin:** AI is Math lesson (`AIIsMathSection`), Conditional Probability section. Removed 2026-06-15 and replaced by the static "Update With New Evidence" ShowcaseBox, which reuses the lesson's own 2-coin grid: new evidence ("the first coin landed on heads") greys out the tails-first outcomes and updates P(both heads) from 25% to 50%. The static box keeps conditional probability tied to the coins the learner just met, instead of introducing a fresh bag-of-balls scenario (beta learners struggled with the example switch).
- **Possible destination:** back into Conditional Probability if an interactive, graded-posterior beat is wanted again, or any lesson that needs to show a belief updating across multiple pieces of evidence (it shows a true posterior sliding 50% → 80% → 94%, which the static coin box does not).
- **Supporting state it needs if restored:** `visibleBayesSteps` (useLocalStorage key `seeit-aiismath-bayesStep`, default 0) + its setter for the step-by-step reveal, and the `BAYES_CONTINUE_LABELS` array (`["See the setup →", "Check your starting belief →", "Draw a red ball →", "Draw again →"]`). Both were declared at the top of `AIIsMathSection` and removed in the same commit. The lesson's `NextLessonGate` was also gated on `visibleBayesSteps >= 4`; it is now `ready: true`, so restoring the gate means re-adding that condition. Depends on the shared `InteractiveBox` and `Takeaway` components, both still in `index.html`.
- **Full source:** in git history at the commit before this one, inside the `AIIsMathSection` function — the `InteractiveBox` titled "Bayes' Theorem in Action" (anchor string for search). It's a 4-step reveal: (1) the setup with two SVG bags of 10 basketballs each (Red Bag 8R/2B, Blue Bag 2R/8B), (2) 50/50 starting belief with a "Ways it happens (1) / Total outcomes (2) = 50%" math row, (3) draw a red ball → belief shifts to 80% with an "(8)/(10) = 80%" row, (4) draw red again → 94%, closing on the Takeaway "Bayes is about how new evidence changes probability."

---

## "See you ___" — original next-word bar-chart example

- **Origin:** the "How the model picks the next word" ShowcaseBox. Retired 2026-06-04 when What Is AI? adopted a single peanut-butter throughline and the bar chart was re-themed to "I went to the store to buy peanut butter and ___" (top word "jelly"). The chart structure lives on in `AIHistorySection`; only this example's wording/data was replaced.
- **Possible destination:** an alternative or second next-word example anywhere the prediction idea recurs.
- **Verbatim data:** header "See you tomorrow"; bars `tomorrow 40%, later 28%, soon 15%, there 6%, again 3%`; outlier `jump 0.0001%`; caption "The model picks tomorrow because it has the highest probability. Then it repeats the entire process for the next word, and the next, and the next, until the answer is complete."

---

## "The Scale of What's Happening" — billions-of-calculations SEE IT

- **Origin:** AI Answers → Inference lesson (`InferenceSection`), removed 2026-05-29 during the source-first reorder to keep the merged Inference lesson from getting dense.
- **Possible destination:** back into Inference, or a future "why it feels instant / cost of inference" lesson.
- **Supporting state it needs if restored:** the `computePhase`, `computeQChars`, `computeAiWords`, `computeReveal` (useState) hooks + the compute `useEffect`, plus the `computeQuestion` / `computeAnswer` string vars and `computeAnswerWords` (= `computeAnswer.split(" ")`). Also depends on the shared `ThinkingBubble` component — still defined in `index.html`, currently unused elsewhere; kept available for this restoration, so do not delete it.
- **Full source:** in git history at the commit before this one, inside the `InferenceSection` function. Note the pieces sit in two different regions of that component: the state hooks/vars above are declared near the top of `InferenceSection` (~120 lines above the JSX), while the JSX block lives lower down. Searching the pre-removal `index.html` for the string `Why it feels instant` finds only the JSX — a restorer must recover BOTH regions, not just that anchor. The JSX block is the complete unit: SectionKicker "The Scale of What's Happening" + the "Why it feels instant" InteractiveBox with its ThinkingBubble/AIBubble compute animation, the reveal button, the stats grid [Tokens ~14, Dimensions thousands, Layers ~100, "every token checks its relationship to every other token"], the "≈ 100,000,000,000+ calculations" figure, the "over 3,000 years" line, and the KeyInsight "Billions of calculations, all for one word.".

---

## "Patterns Are Weights" — the whole lesson (`PatternsSection`)

- **Origin:** Understand AI part, sat between Context Window and Probability (`PatternsSection`, route id `patterns`), removed 2026-06-03. It was one of the first three lessons developed; once the surrounding lessons (Rules vs Patterns, Training, Attention, Layers) became robust, most of it was redundant. Its one unique idea — *training **writes** patterns into the weights, inference **reads** them back out* — was folded into the opening of the Probability lesson instead. The term "weights" now debuts in Training (its natural home), so this lesson no longer had to carry it.
- **Possible destination:** individual pieces are reusable if a dedicated "what a pattern is" beat is ever wanted again. The strongest reusable units, in priority order:
  - **"What Pattern Dynamic Is This?" TRY IT quiz** — two scenarios (a fabricated-citation hallucination → "the pattern of how citations look activated, it doesn't know if the paper exists"; vague vs. specific essay prompt → "specific prompts activate specific patterns"). Good fit for the Traps chapter (hallucination) or the prompting lessons.
  - **Rule / Memory / Pattern showcase** — three tinted cards contrasting a calculator rule, a search lookup, and a soft AI pattern ("flexes with context, sometimes too much"). Overlaps the Black Box lesson's Rule/Pattern/Guardrail quiz, so only restore if that framing is wanted in a different spot.
  - **"The Same Pattern, Two Moments" SEE IT** — a 3-step reveal (good→morning written into weights during training; stored as connection strengths; read back at inference). The training-writes/inference-reads idea it teaches now lives in the Probability intro, so this is the most redundant piece.
- **Supporting state it needs if restored:** `bridgePanel` (useLocalStorage key `seeit-patterns-bridgePanel`) for the three-step reveal, and `picks` (useState) for the scenario quiz. Both are self-contained to the function.
- **Full source:** in git history at the commit before this one, the full `PatternsSection` function (search anchor: `function PatternsSection`). The lesson also had a meta entry (`patterns: { kicker: "ONE IDEA EXPLAINS THE REST", label: "Patterns Are Weights" }`), a `sections` array slot, a component-map entry (`patterns: PatternsSection`), and an overview group ("WHAT TRAINING LEFT BEHIND") in `OpenerAnswersSection` — all removed in the same commit.

---

## "What goes in the context window" — click-to-reveal SEE IT

- **Origin:** Context Window lesson (`PromptSection`), removed 2026-06-03 and replaced by the `illustrations/context-window.jpg` illustration, which makes the same four-component point plus the context-window → model → answer flow and the "outside the window is out of reach" idea.
- **Possible destination:** back into the Context Window lesson if an interactive beat is wanted again, or any lesson that needs to itemize what the model can see. Note the Controls lesson (`CustomizationSection`) still has a near-identical recap built on `CONTEXT_GROUPS_RECAP` — restore from that if you want the live version, rather than rebuilding.
- **Supporting state it needs if restored:** the `CONTEXT_GROUPS` data array (two groups: "From this chat" #1e40af with Your current prompt / Earlier in this chat; "Beyond this chat" #8b5cf6 with Your custom instructions / Saved memory) and its derived `CONTEXT_PARTS`; plus `cwContainerRef`, `cwTitleRefs`, `cwCardRefs` (useRef), `cwPaths` (useState), `cwRevealed` (useLocalStorage key `seeit-context-cwRevealed`), the `revealCw` toggle, and the `useEffect` that measures title/card positions to draw the connecting SVG paths. The lesson's `NextLessonGate` was also gated on `Object.keys(cwRevealed).length === 4`; it is now `ready: true`, so restoring the gate means re-adding that condition.
- **Full source:** in git history at the commit before this one, inside the `PromptSection` function. The state/data sits at the top of the component (declared right after `function PromptSection(props) {`), and the JSX is the `InteractiveBox` titled "What goes in the context window" (anchor string for search), holding the group headers, click-to-reveal title row, the SVG connector layer, and the reveal-on-click description cards.

---

## Start Smarter restructure — AI Primer dissolved and What Is AI? split (2026-06-04)

The 2026-06-04 Start Smarter restructure involved two coordinated moves:

1. **AI Primer (primer) dissolved.** The standalone AI Primer lesson — added to Understand AI Foundations on 2026-06-04, then removed the same day — was dissolved into existing lessons: its conceptual loop (patterns → training → probability → prediction) relocated to What Is AI? (aihistory) as prose; its prediction pieces (bar chart SEE IT + "Guess the Most Probable Word" TRY IT) moved to What's an LLM? (llms); the generative-AI intro and "Stored Answers vs Built From Probability" SEE IT also moved to What's an LLM?.

2. **What Is AI? (aihistory) split.** The everyday-AI breadth content (Spotify/Netflix/Maps showcase, Google Maps example, "Most AI is not ChatGPT" framing) was moved out of What Is AI? into the new You Already Use AI lesson (youalreadyuse), which was inserted between What Is AI? and What's an LLM? in Start Smarter.

Unique copy cut entirely (not carried into any active lesson):

**Primer framing intro** (the "whole machine in one short page" orientation, from the opening of `PrimerSection`):

> This section is long, and it goes deep. Before any of the detail, here is the whole machine in one short page. If the later lessons ever feel like a lot, this is the shape to come back to.

> Almost everything AI does runs on one simple loop: it learns patterns, weighs what is likely, and predicts the next piece. Four words carry it. Here they are, in plain language.

**Primer closing KeyInsight** (the "You have the shape now" beat, from the `KeyInsight` at the end of `PrimerSection`):

> AI learned patterns from huge amounts of text, and it uses them to weigh what is probable and predict the next word, one word at a time. Everything else in this section is a closer look at one part of that loop. You have the shape now. The rest opens up each piece.

*(The lead was: "That is the whole loop:")*

**Possible destination:** the framing intro could anchor a returning-orientation callout inside the Understand AI opener or a mid-section recap in What Is AI?. The closing KeyInsight's "You have the shape now. The rest opens up each piece." phrasing is reusable at any lesson that serves as a conceptual overview before diving into detail.

---

## Probability lesson intro (folded into AI Primer, 2026-06-04)

The standalone Probability lesson was removed and folded into the new AI Primer. Its SEE IT (the "See you ___" bar chart) and TRY IT ("Guess the Most Probable Word") moved to the Primer. Its unique intro prose, which framed the loop in terms of "weights" (a term the Primer deliberately avoids since it predates the Tokens/Training lessons), is preserved here for possible reuse in the Training lesson:

> In Training, the model tuned billions of **weights** until they captured the patterns in its data: which words tend to follow which. Training **wrote** those patterns into the weights. Answering **reads** them back out.
>
> Here's the first thing it reads out. When the model needs the next token, it turns those weights into a score for every word it could pick. That step has a name: **probability**. It's worth slowing down on, because it's the single move AI repeats for every word in every response you've ever seen.
>
> The SEE IT below zooms in on one short phrase so you can see what those scores actually look like.

## "When Not to Use AI" — the whole lesson (`WhenNotSection`)

- **Origin:** Protect Yourself, between Support Trap and How Much to Check (`WhenNotSection`, route id `whennot`), removed 2026-06-10. Merged into How Much to Check (`howmuchtocheck`), which moved at the same time from Protect Yourself into Check the Output as that section's first lesson. Rationale: the lesson's content indexed points owned by other lessons (rules → Integrity, private info → Privacy, danger → Support Trap's ONE RULE, can't-verify → How Much to Check), and two of its four "Stop or Go?" scenarios near-duplicated Make the Call rows.
- **What moved where (not parked):** the four-category "DON'T REACH FOR IT WHEN" ShowcaseBox moved verbatim into How Much to Check under a "SOMETIMES THE ANSWER IS NO" kicker; the "Send it for me?" scenario became Make the Call row 7 (tag "Acting for you", correct: careful); the KeyInsight test ("If you'd be embarrassed to say out loud how you used AI, that's your answer") was folded into Academic Integrity's KeyInsight body alongside the teacher-without-notes test.
- **Cut entirely (parked here):**
  - **Opening framing paragraph** — "Every other lesson in this course assumes you've already decided to use AI, then teaches you to do it well... This lesson asks the question that comes first. Before any of that, should you open the tool at all? Sometimes the sharpest move is to leave it closed and handle something yourself, or hand it to a real person. That call is its own skill, and it's the one that keeps you in charge of the tool instead of the other way around." (Condensed version now opens the merged beat.)
  - **"A friend's secret" scenario** — friend shares something personal over text; tempted to paste the conversation into AI. Correct: keep it between you two ("Their private information stays private. If you want to help, do it as a friend."). **Possible destination: Privacy (`privacy`)** — it is squarely that lesson's others'-information point and would make a good scenario there.
  - **"A worrying symptom" and "It won't click" scenarios** — dropped as near-duplicates of Make the Call's medical (ibuprofen/amoxicillin) and explaining-concepts (chain rule) rows.
  - **Completion card** — "✋ You can feel the difference. Using AI well includes knowing the moments to leave it closed."
- **Full source:** `WhenNotSection` and `WHENNOT_SCENARIOS` remain defined in `index.html` as dead code (removed from SECTION_GROUPS/SECTION_META/SECTION_COMPONENTS). The dead `OpenerJudgmentSection` also still references `whennot` in its FAQ data; harmless.

## "Who Else Is Affected" — the whole lesson (`StakeholdersSection`)

- **Origin:** Build Your Advantage, between When AI Judges You and AI & The Future (`StakeholdersSection`, route id `stakeholders`), removed 2026-06-10 in the back-half restructure. Rationale: the course's least personally actionable lesson (analysis with no move attached), with real overlap against When AI Judges You (its lead scenario was the same plagiarism-detector territory, and its "no appeal path" KeyInsight restated the five questions' question 5).
- **What moved where (not parked):** the "FOUR ROLES IN EVERY DEPLOYMENT" ShowcaseBox (user / subject / operator / bystander, with the operator-incentives line "knowing what they were optimizing for tells you most of the story") moved near-verbatim into When AI Judges You, after the THREE MODES box, with a bridge paragraph ("naming the seats tells you who has power, who has risk, and who gets a say"). The roles footnote about overlapping roles was dropped for length.
- **Cut entirely (parked here):**
  - **"FOUR NAMED TRADE-OFFS" ShowcaseBox** — Speed vs fairness ("the system decides fast across the average case; edge cases get the worst version of the trade"), Convenience vs privacy, Efficiency vs human judgment ("context gets compressed into a score; what gets lost is the part that didn't fit the form"), Scale vs care ("watching one person carefully is expensive; watching everyone is cheap; watching everyone carefully is impossible"). Plus the footnote: a trade-off isn't automatically wrong; the question is whether the cost is named, whether affected people can challenge mistakes, and who ends up paying.
  - **"Spot the Cost" TRY IT** — three scenarios (district plagiarism detector, image-generation tools vs artists' training data, school communication monitoring), each asking "who carries the cost the design overlooked?" with full per-option feedback. Strong material if a stakeholder beat ever returns; the artists/training-data scenario is the only place the course discussed that debate.
  - **KeyInsights** — "A lot of AI conversation is about how users feel" (most of the cost lands elsewhere); "No appeal path is its own answer"; and the closer "The question isn't only 'Does this AI work?' It's 'Who does it work for, and who carries the cost?'" — that last line is a candidate for When AI Judges You's ending if it ever wants a sharper close.
- **Full source:** `StakeholdersSection` remains defined in `index.html` as dead code (removed from SECTION_GROUPS/SECTION_META/SECTION_COMPONENTS).

---

## "The move, step by step" — messy-input ShowcaseBox (2026-06-15)

- **Origin:** the Mess to Meaning lesson (`DataSection`), cut 2026-06-15 when Mess to Meaning was merged into Rules vs Patterns (aivscode). The merged lesson kept both CompareBoxes, the PS5 SEE IT, and both TRY ITs, but dropped this "The move, step by step" ShowcaseBox; the data lesson's "AI runs on patterns" opener was replaced by a bridge paragraph back to the first TRY IT.
- **Possible destination:** any lesson that needs a one-line frame for how AI turns messy input into usable output (Rules vs Patterns, What AI Does Best, or a prompting lesson).
- **Verbatim intro:** "AI takes your messy input, matches it against the patterns it learned, and hands back something you can use."
- **Step titles:** "What you send" / "Matches what it learned" / "What it sends back".

## "How We Got Here" — the static 9-event timeline (2026-06-15)

- **Origin:** the How We Got Here lesson (`HowWeGotHereSection`), cut 2026-06-15 when the lesson was redesigned around an interactive "assemble the four ideas, then ignite them at 2017" SEE IT (`HistoryAssembleSeeIt`). Rationale: the flat timeline listed concepts before students understood them (names-before-meaning) and was the only passive lesson in the Welcome→Rules-vs-Patterns stretch. Probability/prediction/training each kept one origin beat in the new SEE IT; Bayes, Yule (autoregressive), and backpropagation were dropped as named milestones. Full prior version is in git history before commit `Redesign How We Got Here`.
- **Possible destination:** a later "history of AI" enrichment, or flavor in AI is Math / Training if any single milestone is wanted.
- **Old KeyInsight — "AI was centuries in the making.":** "No one set out to build it. Probability, prediction, training, and patterns were each worked out by different people, decades and even centuries apart, for reasons that had nothing to do with AI. What we call AI today is what happened when those separate ideas finally came together."
- **Verbatim 9-entry timeline:**
  - 1654 Standard Probability (probability): "Blaise Pascal and Pierre de Fermat traded letters about games of chance, the start of modern probability math."
  - 1763 Conditional Probability (probability) [DROPPED]: "Thomas Bayes found a formal way to update probabilities as new evidence comes in."
  - 1927 Autoregressive Generation (prediction) [DROPPED]: "George Udny Yule proposed the autoregressive model: predict each step in a sequence from the ones before it."
  - 1948 Generating English (prediction): "Claude Shannon applied the autoregressive idea to language, picking each word from the probability of the one before it: an early statistical model of language."
  - 1957 The Perceptron (training): "One of the first machines that could learn from examples. It was primitive, but it proved the concept: machines can learn, not just follow instructions."
  - 1986 Backpropagation (training) [DROPPED]: "How a machine learns from its mistakes: each wrong answer makes the next one better, over billions of tries."
  - 2017 Attention Is All You Need (patterns): "A team at Google published one paper that changed everything. AI could now read all your words at once instead of one at a time. The transformer was born."
  - 2018 to 2021 Scaling Up: "Researchers fed transformers more of the internet and more computing power. The bigger they got, the more capable they got, turning a research idea into something powerful."
  - 2022 ChatGPT Launches: "The public finally saw what large language models could do. AI started feeling like a tool anyone could use."

## "Where AI sits in some jobs" — fields ShowcaseBox (2026-06-16)

- **Origin:** the Why Learn AI? lesson (`WhyDeeperSection`), cut 2026-06-16 as redundant. The point ("whatever career you pick, AI will be in the middle of the work") is already stated in the paragraph directly above it, made personally in Does School Matter? (the "dream job at Google" walkthrough), and covered in full by How AI Absorbs Work (`WorkChangesSection`). Removing it tightened the motivation lesson.
- **Possible destination:** How AI Absorbs Work, or any lesson wanting concrete cross-field proof that AI is already in the work.
- **Verbatim headline/intro:** "Where AI sits in some jobs" / "A few real fields where it's already part of the work, not something coming someday."
- **Six FIELD_CARDS (icon · title · body):**
  - 🩺 Medicine: "Reading scans, drafting chart notes, and flagging risks a tired human might miss."
  - ⚖️ Law: "Combing thousands of pages for the one clause that matters."
  - 🎨 Design & Art: "Mockups, drafts, and variations in seconds for a human to choose between."
  - 💻 Software: "Writing code, catching bugs, and explaining what a stranger's repo actually does."
  - 📊 Business: "Developing strategy, entering data, and writing the email."
  - 🔬 Science: "Proposing experiments and chewing through data faster than a lab could by hand."

## "Pick the Better Move" TRY IT — Study with AI (2026-06-16)

- **Origin:** the Study with AI lesson (`StudyingWithAISection`, studying), cut 2026-06-16. Once the lesson refocused on NotebookLM and the hands-on Lab ("Build Your Course Notebook") became the payoff, this 3-scenario TRY IT was redundant: each point is already stated in the Best practices list and the comparison box, and two are done for real in the Lab. The Next gate (formerly keyed to this activity) is now `ready: true`, since the Lab is take-home.
- **Possible destination:** any future lesson wanting a pitfall-recognition ("here's the tempting wrong move") check on retrieval practice, citation-checking, or tool choice. Rendered as a mint `InteractiveBox` over `ScenarioRow`/`QuizBlock`, gated on `picks ≥ scenarios`.
- **Kicker / intro:** "Pick the better move" / "Three real moments studying with NotebookLM. Each one is a fork, and you pick the move that actually makes you learn." Instruction: "Pick the better move in each one. We'll explain why as you go."
- **Three verbatim scenarios (✓ = correct):**
  1. *"Your class notes and slides are loaded into NotebookLM, and the test is tomorrow morning. Pick the better move."*
     - Generate a study guide and read it twice before bed. — "Reading a guide feels productive, but it's recognition, not recall. You'll recognize the words tomorrow and still freeze on the test."
     - ✓ Generate a blind quiz from your sources, take it closed-book, then have it grade you. — "Right. A blind quiz is retrieval: you find out what you actually don't know while there's still time to fix it."
     - Make flashcards and call it a night. — "Flashcards are a fine tool, but making them isn't studying. Quizzing yourself with them is the part that sticks, so take a real quiz tonight."
  2. *"NotebookLM hands you a perfect-sounding fact to use in your history essay. Pick the better move."*
     - Paste it straight into your essay. It's grounded in your sources, so it's safe. — "Grounded doesn't mean flawless. It can still misread a sentence or stitch two unrelated facts together. Trust, then check."
     - ✓ Click the citation bubble and check the spot in your notes it came from. — "Right. The citation shows exactly where it pulled the fact. Five seconds to confirm it wasn't taken out of context before it lands in your paper."
     - Ask NotebookLM whether it's sure. — "It'll almost always say yes. Asking the model to rate its own confidence proves nothing. Check the source yourself."
  3. *"Studying from your notes in NotebookLM, you hit a concept your teacher never actually covered. Pick the better move."*
     - Ask NotebookLM to explain it anyway. — "It can only work from what you gave it. With nothing in your sources on this, it comes up empty or starts guessing. This is exactly its blind spot."
     - ✓ Switch to a general AI to learn it, then add what you learn to your notes. — "Right. Source-grounded AI can't teach what isn't in the binder. A general tutor is built to explain something new, so use it for the gap."
     - Skip it. If it's not in your notes, it won't be on the test. — "Risky bet. Gaps in your notes are exactly where you lose points. Learn it with a general AI instead of gambling that it won't show up."

## "What Could AI Pull Out?" TRY IT — Rules vs Patterns (2026-06-16)

- **Origin:** the merged Rules vs Patterns lesson (`AIvsCodeSection`, aivscode), cut 2026-06-16. When the lesson was re-pitched as one idea (patterns → therefore handles mess), its two activities collapsed into one fused "Which One Handles This?" TRY IT whose pattern-win feedback now reveals the extraction. This standalone 3-scenario extraction activity became redundant. Its grocery-photo case was adapted into the fused TRY IT's row 4 (as a rule-vs-pattern row with a can't-invent guardrail); the grades-text and drive-thru cases are fully cut and reusable.
- **Possible destination:** any future lesson on multimodal input or "what AI can/can't extract from mess." Rendered as a mint `InteractiveBox` over an `InnerCard`, each scenario a stimulus (text / image item-list / speech) plus three options, gated on `fuelAnswers ≥ 3`. It carried the "It restructures; it doesn't invent" KeyInsight (which survives in the live lesson).
- **Instruction:** "Three real messes: a text, a photo, a spoken order. For each, pick what AI could actually pull out of it."
- **Three verbatim scenarios (✓ = correct):**
  1. *"A friend texts you about their grades. What could AI pull out?"* — stimulus: "Honestly math was rough, I think I got like a B minus? English went really well though, probably my best score this semester. Science was okay I guess, not great not terrible."
     - Your exact percentage scores. — "It can't invent what isn't there." / "The text never gives real numbers, so AI can't produce them. It can read a signal like 'around a B minus,' but it won't make up an exact score."
     - ✓ The subjects, a grade signal for each, and how you felt about them. — "Right." / "AI matches the casual words to what it learned: 'rough' reads as a struggle, 'best score' as strong, 'not great not terrible' as average. Out comes subject, signal, and feeling."
     - Nothing usable, it's too messy. — "Messy is the whole point." / "A casual sentence is exactly the kind of mess AI is built to read. Traditional software would choke on it; AI finds the structure inside."
  2. *"You snap a photo of a handwritten grocery list. What could AI pull out?"* — stimulus (image items): Milk x2 (whole) / Eggs - 1 dozen lg / Sourdough bread / Bananas (ripe) x6
     - ✓ Each item with its quantity and notes, as a clean checklist. — "Right." / "AI reads the handwriting and the shorthand: 'x2' is a quantity, '(whole)' is a note. The photo becomes an organized list."
     - Nothing, a photo is just pixels to AI. — "AI reads the pixels like text." / "Not so. AI learned from countless images, so it reads the pixels the same way it reads messy text, and pulls the list right out."
     - The store name and the prices. — "It can only pull what's there." / "The photo shows items and quantities, not a store or prices, so AI has nothing to pull those from."
  3. *"Someone speaks a drive-thru order. What could AI pull out?"* — stimulus: "Yeah can I get a double burger but no onions, large fries with extra salt, and like two medium Cokes"
     - Nothing until someone types it into a form. — "AI handles the speech directly." / "Traditional software needs typed fields. AI takes the spoken words and structures them itself."
     - The customer's name and payment. — "It can only pull what's in the audio." / "The clip is just the order. AI won't invent a name or payment that was never said."
     - ✓ A clean order: each item, its size, and the special requests. — "Right." / "AI transcribes the speech and maps the casual sentence into fields: a double burger with no onions, large fries with extra salt, two medium Cokes."
- **Also cut (prose + one TRY IT #1 row):**
  - Bridge paragraph (back-reference, no longer fits a single activity): "Look back at the two jobs AI handled in that exercise: turning a rambling voice memo into a clean list, and flagging a scam text nobody had seen before. Neither arrived in neat fields, and nobody wrote a rule for them. That is exactly AI's edge. It takes the messy, unfamiliar input that rules choke on and pulls something usable out."
  - Modalities prose: "It can do this because it learned from the messy stuff humans actually produce: conversations, images, audio, video, emails, code, reviews, and notes. So new mess looks familiar." (the idea now lives in the merged box's "What it needs" row.)
  - The "Flag a scam text you've never seen before" row from "Which One Handles This?" (✓ AI), swapped out for the grocery-photo row: ai feedback "It is brand new, so no rule exists for this exact message. AI handles the unfamiliar by matching patterns from the many scams it has seen."; trad feedback "A written rule only catches scams someone already described. A brand-new one walks right past it. Spotting the unfamiliar is AI's strength." Reusable if the activity ever wants an "unfamiliar" facet alongside the "extraction" ones.

## "Best for" row — "The big three, side by side" box (2026-07-01)

- **Origin:** the Which App? lesson (`ModelSelectionSection`), cut 2026-07-01. The row listed per-app capability strengths, which age fast as the models leapfrog each other — the lesson itself warns "the gap you remember may already be gone," and the checklist sat in direct tension with that. The box now runs tagline / What it is / [Company] Asks, all philosophy-derived and durable. The durable one-line version survives in the paragraph below the box ("ChatGPT is built for breadth. Claude is built for depth. Gemini is built for context.").
- **Possible destination:** probably none as-is — a dated "current strengths" sidebar would need a "as of [date]" stamp to be honest. The Gemini column (ecosystem-structural, so durable) is the only piece safe to reuse.
- **Verbatim `STRENGTHS` data:**
  - ChatGPT: Brainstorming / Quick drafts / Varied everyday tasks / General multimodal work with text, voice, images, files, and data
  - Claude: Coding and code review / Analysis and research / Long-form writing / Careful critique when the stakes are higher, but still verify
  - Gemini: Current events / Live web research / Summarizing YouTube videos and Drive files / Drafting in Gmail and Docs
- **Markup if restored:** a fourth subgrid row per card (grid was `auto auto auto auto`, cards `span 4`), rendered as a ✓-list in the app's accent color under a "Best for" `secLabel`. Removed in the same commit: the dead `philContainerRef`/`bestForContainerRef` path-measuring plumbing at the top of `ModelSelectionSection` (never attached to any element; predates this box's current static form).

---

## "Same AI. Different question. Different result." — climate-debate weak/better example

- **Origin:** Questions Matter lesson (`QuestionsValuableSection`), removed 2026-07-02 when the lesson gained the "What Makes a Good Question?" section, whose four quality cards each carry their own Bad/Better example pair — a fifth weak/better comparison immediately after read as repetition. The section's closing disclaimer ("A better question doesn’t make the answer automatically true. It just makes the answer more focused, more useful, and easier to check.") was kept in the lesson.
- **Possible destination:** Art of Prompting (`prompting`), as a makeover example of a fully-loaded question — the better version stacks audience ("I’m a high school student preparing for a class debate"), format ("the 3 strongest arguments for... against..."), and a success bar ("tell me which side has the stronger evidence") in one ask, which is exactly that lesson’s territory.
- **Verbatim content:** kicker "Same AI. Different question. Different result."; intro "Two students ask about the same topic. One gets a textbook paragraph. The other gets something they can actually use."; Weak question card "Tell me about climate change."; Better question card "I’m a high school student preparing for a class debate. Give me the 3 strongest arguments for carbon taxes, the 3 strongest arguments against them, and tell me which side has the stronger evidence."; explanation box "The second person gets more value not because the AI is smarter, but because the human asked a better question. It frames the task, takes a real position, and says what a useful answer looks like."
- **Markup if restored:** two-column grid (`1fr 1fr`, gap 12) of red (#fef2f2 / 2px #fca5a5) and green (#ecfdf5 / 2px #86efac) cards with 11px uppercase labels and italic question text, followed by a full-width `var(--bg)` explanation box. Self-contained JSX, no state.

---

## "What a Better Question Does" — four-things NumberedRows

- **Origin:** Questions Matter lesson (`QuestionsValuableSection`), removed 2026-07-02, same rework session that added the "What Makes a Good Question?" quality cards (Open-Minded / Specific / On Target / Open-Ended). After that addition this list was a second numbered four-item list with heavy overlap: "Frames the problem" ≈ On Target, "Creates the next move" ≈ Open + On Target. The lesson's KeyInsight ("The advantage no longer goes to whoever produces the fastest first answer...") was kept.
- **Possible destination:** Art of Prompting (`prompting`). The one idea nothing else in the course states this crisply is **"Defines success"** — know what a good answer looks like *before* you ask — a strong pre-prompt habit beat or ninth-quality candidate there (it also foreshadows Check the Results). "Sets constraints" is already covered by the 8 Qualities (Context / Format Instructions / Constraints), so it needs no new home.
- **Verbatim `VALUABLE` data:**
  - 🎯 Frames the problem — "Most bad AI output starts with a fuzzy question. Naming what actually needs to be solved is half the work."
  - 📏 Sets constraints — "“Do it well” isn’t a spec. Deciding the audience, the format, the limits, and what to leave out shapes everything that comes back."
  - 🏁 Defines success — "Before you ask, know what a good answer looks like. Without that, you can’t tell whether the output is useful or just fluent."
  - ➡️ Creates the next move — "A good question asks for something you can use, test, revise, or decide from. Not just something fluent to read."
- **Markup if restored:** SectionKicker "WHAT A BETTER QUESTION DOES" + intro BodyP "You know what a good question looks like. Here’s what one buys you in an AI chat: four things a well-framed question hands the model to work with." + `NumberedRows` (marginBottom 32) fed `VALUABLE.map` to `{icon, title, body}`. Self-contained, no state.

---

## "Pick the Stronger Question" — three-option prompt-upgrade TRY IT

- **Origin:** Questions Matter lesson (`QuestionsValuableSection`), replaced 2026-07-02 by the "What’s Missing?" TRY IT, which has students diagnose which of the lesson's four qualities (Open-Minded / Specific / On Target / Open-Ended) a flawed question lacks. The old activity was pick-the-better-version — a move the lesson's quality cards' Bad/Better pairs now make four times — and its correct answers were really prompt makeovers (context + format + constraints stacked), which belongs to Art of Prompting under the new lesson split.
- **Possible destination:** Art of Prompting (`prompting`) — five ready-made weak→strong prompt makeovers with graded distractors ("more words, still vague" and "sharp but wrong target" per scenario). Could work as a TRY IT there against the 8 Qualities, or as source material for worked examples.
- **Verbatim scenarios (weak prompt → the three options each, correct one marked):** in git history at the commit before this one, `UPGRADE_SCENARIOS` in `QuestionsValuableSection` (anchor string for search). The five weak prompts: "What should I do for my project?", "Help me with my essay.", "Give me ideas.", "Should I quit the robotics club?", "What's a good college?". Each has one fully-loaded correct option (e.g. AP Bio genetics project with 3-week timeframe; Gatsby thesis paragraph review; $200 Dallas birthday with 8 friends; robotics club decision framing; 3.7-GPA/$25K/southern-US college list grouped reach/target/safety) and two flawed ones with hint + feedback text.
- **Markup if restored:** `InteractiveBox` (variant try, mint) + per-scenario `UserBubble` (label "Weak prompt") + mint `QuizBlock` (statement "Which version asks the right question?"). State: `upgradeAnswers` (useState {}), gate `Object.keys(upgradeAnswers).length >= UPGRADE_SCENARIOS.length`. Ended with a Takeaway ("Specific isn’t the same as right.") — house rule now says omit Takeaways when the TRY IT gives per-item feedback.

---

## "Bad Prompt, Better Prompt" — Career cover-letter example

- **Origin:** Art of Prompting lesson (`PromptingSection` region), removed 2026-07-02 when the two-example "Bad Prompt, Better Prompt" opener box was slimmed to one example, retitled "The Qualities at Work", and relocated to after the 8 Qualities overview (so readers can name why the better prompt wins). The Academic (AP US History) example was kept; this Career one was cut to keep the lesson moving.
- **Possible destination:** back into Art of Prompting if a second worked example is wanted (it shows Context + Constraints where the kept example shows Context + Specificity + Format + One Task), or the planned hands-on prompting LAB as a scripted example students reproduce live.
- **Verbatim data (`BEFORE_AFTER` entry):**
  - label: "Career"
  - bad: "Help me write a cover letter."
  - good: "I’m 17 applying for a summer internship at a local marketing agency. I have no work experience but I’ve run my school’s Instagram account for two years and grown it from 200 to 1,400 followers. Write me a cover letter that leads with that as my main qualification and keeps it under 200 words."
  - badOut: "Dear Hiring Manager, I am writing to express my interest in the internship position at your company. I am a hardworking student who is eager to learn and contribute to your team. I have good communication skills and work well with others. Thank you for your consideration."
  - goodOut: the three-paragraph Instagram-growth letter ("In two years managing my school’s Instagram account, I grew our following from 200 to 1,400...").
  - callout (never rendered; the box used a shared Takeaway instead): "Same task. One gets a template. The other gets a letter that could actually land the job."

---

## "The 8 Qualities" reveal box + dead `PROMPT_QUALITIES` const

- **Origin:** Art of Prompting, removed 2026-07-02 when the lesson's quality list was unified with Questions Matter's into one numbered framework: qualities 1–4 (Open-Minded / Specific / On Target / Open-Ended, recapped in a compact 2x2 band labeled "From Questions Matter") + 5–10 (Context, Role/Persona, Format Instructions, Constraints, Examples, One Task at a Time) as full cards with Bad/Better prompt pairs. Two of the old eight were dropped as duplicates of the question qualities: **Clarity** ("Say exactly what you mean. Vague prompts get vague answers.") and **Specificity** ("The more specific the ask, the more useful the answer. Narrow the scope to what you actually need.").
- **What was removed:**
  - The `QUALITIES_OVERVIEW` RevealSequence ShowcaseBox ("The 8 Qualities", sand surface, "See First Quality ↓" stepper, Takeaway "Eight qualities. One habit." — the takeaway line lives on after the new cards as "Ten qualities. One habit.").
  - `const PROMPT_QUALITIES` — dead code (defined, never rendered) but content-rich: per-quality `goal` / `bad` / `good` / `why` fields with polished scenarios (vertical-jump clarity, Common App context, chill-math-tutor persona, laptop-comparison table, volleyball-tweet constraints, photography-captions few-shot, Cold War one-task). The bad/good pairs were harvested into the new 5–10 cards; the `goal` and `why` fields were NOT carried over and are strong material for the planned hands-on prompting LAB (students reproduce each pair live and the `why` text explains what changed).
- **Full source:** in git history at the commit before this one — search `QUALITIES_OVERVIEW` (inside the prompting section's return) and `const PROMPT_QUALITIES` (top level, above `OpenerWorkWithSection`).

---

## "Why Good Prompts Work" — three-reason NumberedRows

- **Origin:** Art of Prompting, removed 2026-07-02. Sat between the lesson intro and the unified ten-qualities framework; cut because the hands-on prompting LAB (planned to replace the TRY IT) will show the effect live, and its internal 1-2-3 numbering competed with the framework's 1-10. The mechanism content is taught properly in the Understand AI section.
- **Possible destination:** the prompting LAB debrief (each reason explains what students just observed), or Context Window (`prompt`), which already owns the context-window idea.
- **Verbatim items:** 🧠 "LLMs are pattern completers" — "LLMs run on patterns: specific prompts activate specific patterns, vague ones activate vague patterns. A precise input narrows the model to the best path." / 📋 "Context is everything" — "The model can only work with what's in its context window. A good prompt puts the right information in front of the model." / 🎯 "You're the director" — "Think of prompting as directing. The model fills in whatever you leave blank, sometimes well, sometimes not. A clear prompt replaces its defaults with your specifics."
- **Markup if restored:** SectionKicker "WHY GOOD PROMPTS WORK" + `NumberedRows` (marginBottom 28) with the three items above.

---

## Six-card "packaging qualities" list (5–10) — superseded same-day by the three moves

- **Origin:** Art of Prompting, built and replaced 2026-07-02. The unified ten-quality framework (question qualities 1–4 + Context, Format Instructions, Constraints, Examples, One Task, Role/Persona as 5–10) proved too deep: students would lose the key points in the detail. Restructured into three packaging moves: "Share your situation" (absorbs Context + who-it’s-for), "Describe the answer you want" (absorbs Format Instructions, Constraints, Examples, Persona as ingredient bullets), "One job at a time" (One Task). The recap band of question qualities 1–4 stayed.
- **Dropped Bad/Better pairs** (kept pairs live on in the move cards: Common App context, volleyball tweet, Cold War thesis):
  - Role/Persona: "Explain derivatives." → "You’re a chill math tutor who explains things with sports and video game analogies. Explain what a derivative is to someone who’s fine at algebra but struggling with calculus."
  - Format Instructions: "Compare the MacBook Air and the Dell XPS 13." → "Compare the MacBook Air and Dell XPS 13 in a table: price, battery life, performance, weight, and best use case for a college student."
  - Examples: "Write captions for my photos." → "Write Instagram captions for my photography account. Here’s my style: “The sky did all the work. I just pointed the camera.” Now write three more in that voice."
- **Possible destination:** the planned hands-on prompting LAB (each pair is a ready-made live exercise), or worked examples if a move card ever needs a second pair.
- **Full source:** git history, search `PACKAGING_QUALITIES`.

---

## "The Moves at Work" — AP History worked example with mock outputs

- **Origin:** Art of Prompting, removed 2026-07-02 (same session as the three-moves restructure). With each move card carrying its own Bad/Better pair, this was the page's fourth contrast, and its mock AI outputs will be superseded by the hands-on LAB where students see real outputs live. Cut for lesson weight.
- **Possible destination:** the prompting LAB, as the scripted exercise itself (send the bad prompt, then the good one) or as a printed fallback for students without app access. The takeaway line "Same ask. Different prompt. Different answer." is a ready-made LAB headline.
- **Verbatim `BEFORE_AFTER` data:** bad "Help me study history." with output "Sure! Here are some general tips for studying history: make a timeline, use flashcards, review your notes, and practice with past exams. Good luck!" / good "I have an AP US History exam Friday. Quiz me on the political, economic, and social causes of the Civil War. Give me five questions, then check my answers and explain what I missed." with the five-question Civil War output (Missouri Compromise, Southern economy, Dred Scott, John Brown, Lincoln 1860). Takeaway body counted the moves: situation shared (AP US History, exam Friday), answer described (five questions, then check and explain), one job (quiz me).
- **Markup if restored:** SectionKicker + intro BodyP + ShowcaseBox of one InnerCard (red bad-prompt box, mono AI Output, green better-prompt box, mono AI Output) + Takeaway. Search git history for `BEFORE_AFTER`.

---

## Prompting diagnostics line — cut from lesson body

- **Origin:** Art of Prompting, removed 2026-07-02 during the lesson slim-down. Verbatim: "Two diagnostic patterns: if answers keep coming back the wrong shape (too long, too formal, too generic), you didn’t describe the answer you want. If they keep missing your situation, you didn’t share it."
- **Possible destination:** the prompting LAB debrief — it reads best right after a student has watched a wrong-shaped answer come back live.

---

## "Build a Study Prompt" — interactive prompt builder

- **Origin:** Art of Prompting, replaced 2026-07-02 by Lab 03 "Good Prompt, Bad Prompt" (log in to Claude, send a bad prompt, send a loaded one on a different subject, run it on something real). The builder simulated prompt assembly; the lab does it live, which the lesson rework prioritized.
- **Possible destination:** could return as a pre-lab warm-up if students need scaffolding before typing real prompts, or be adapted into a worksheet. Its five-part structure (subject, test format, what I understand, what confuses me, how to help + what not to do) is a solid study-prompt template independent of the UI.
- **What it was:** a TRY IT (mint) titled "Build a Study Prompt": chip-select Subject (AP Biology, US History, AP Calc, English Lit, Spanish, Chemistry) and Test format; free-text "What I already understand" / "What I'm confused about"; chip-select "How AI should help" (quiz one at a time, simple analogies, practice problems, mixed difficulty) and "What AI should NOT do" (no instant answers, no textbook voice, no restating, no disclaimer pile); a live "Your Prompt So Far" mono preview assembling the sentence; on completion, a side-by-side compare against a strong AP Biology example with the closing note that both cover the same five things.
- **Supporting state it needs if restored:** `pSubject/pFormat/pUnderstand/pConfused/pHowHelp/pNotDo/pRevealed` (useState) + `STUDY_FIELDS` const + `pAllFilled`/`pFilledCount` derived values; the lesson's NextLessonGate was gated on `pAllFilled`. Search git history for `STUDY_FIELDS`.

---

## Customization & Memory — the whole lesson (`CustomizationSection`)

- **Origin:** Build Your Skills section (route id `customization`, between Tune the Model and Ask AI), deleted 2026-07-02. Its two core ideas (custom instructions and saved memory) moved into Context Window (`prompt`) at a lighter level: a four-feeds box, a three-flavor "Make It Yours" row (Personalization / Projects / Memory), an app-vs-model clarification, and LAB 04 "Same Question, Different You" (ask the Luke/Nate car question, add personalization in Settings, ask again, then "What do you know about me?"). Tune the Model's gate now points to Ask AI.
- **Cut-but-strong pieces, in priority order:**
  - **"Where should this go?" sort TRY IT** — five snippets sorted into Personalization / Projects / Memory / Current chat / Nowhere ("Call me David." → all chats; Macbeth rubric → project; "I only have 30 minutes tonight." → current chat; cellular-respiration struggle → memory; "Always tell me my work is great." → nowhere, the flattery trap as a setting). Candidate home: Ask AI or Thought Partner if a management-skills beat is ever wanted.
  - **"Three things can go sideways" KeyInsight** and the conflict rule (more specific wins: project overrides personalization).
  - **Nate's real personalization example** (first-person walkthrough).
  - **Animated four-part recap** (CONTEXT_GROUPS_RECAP with connector lines) — superseded by the static feeds box now in Context Window.
- **Full source:** git history at the commit before this one, `function CustomizationSection` (~780 lines incl. sort TRY IT state `sortAnswers`).
- **Related survivors:** the Flattery trap lesson's "you can bake the Flattery Trap into your settings" box stands on its own and still works.

---

## "What actually gets sent" — stateless re-read beat (destination: Inference)

- **Origin:** Context Window (`prompt`), removed 2026-07-02. The fact ("the model sees the whole window") stays in Context Window in one sentence; the mechanism moved out because it belongs with Understand AI depth. **Intended destination: the Inference lesson**, where tokens/vectors/layers are already established and it lands as "remember the context window? Here's what actually happens each turn."
- **Verbatim paragraphs:**
  1. "It feels like a conversation that remembers you. But the model treats every turn as a one-off: it wakes up, reads the entire window as if for the first time, answers, then starts fresh the next turn. It’s the Chinese Room from Does AI Think? again: a fresh note slides under the door, the model answers from only what’s written on it, and keeps nothing. The window is that note."
  2. "And everything you learned earlier applies to all of it. The whole window is broken into tokens, each token becomes a vector, and the entire thing runs through the layers together, every single time. That window is the only thing the model can see."
  3. "It’s also why ChatGPT and Claude can feel slower as a chat gets long: there’s simply more in the window to work through before the model can start answering."
  Plus the original stronger opener: "It receives the entire context window: your prompt, everything earlier in the chat, your custom instructions, and any saved memory. All of it, every single turn."

---

## "Predict the split" — context-window prediction TRY IT (`PromptSplitTryIt`)

- **Origin:** Context Window (`prompt`), removed 2026-07-02 during the lesson's customization merge and Lab 04 addition (the lab now carries the lesson's hands-on beat). It was a compact TRY IT: everyone asks "What car should I get after college?", only their earlier message differs, and the student predicts which car the AI suggests for each person — reinforcing that the window, not the question, drives the split.
- **Possible destination:** could return if the lesson ever needs a no-account activity (the lab requires a Claude login; this worked for students without one), or adapt for the Inference lesson when the parked stateless beat lands there.
- **Full source:** git history at the commit before this one, `function PromptSplitTryIt` (~2.5k chars, self-contained with its own state).

---

## "Context Window Size" — token measurement + growth facts box (destination: Inference)

- **Origin:** Context Window (`prompt`), removed 2026-07-02. Replaced by a two-sentence "The window has a limit" beat (long chats fall out, apps summarize or forget, fresh chats help). Moved out because tokens aren’t taught yet at this point in the course (the copy claimed "the same chunks you met in the Tokens lesson" — a stale forward reference), and the facts box carried a perishable per-app capability claim. **Intended destination: the Inference lesson**, alongside the parked stateless every-turn re-read beat — with tokens established there, window size lands correctly.
- **Verbatim copy:** "The whole window is measured in tokens, the same chunks you met in the Tokens lesson. Pile up enough of them and you hit the context window’s limit." / "Before that limit, the model sees everything in the chat. After it, it doesn’t. Some apps summarize the older parts. Others just forget." / "And that limit is growing fast."
- **Verbatim `CONTEXT_WINDOW_FACTS`:** 1st version of ChatGPT (November, 2022): 4,096 tokens, ~3,000 words, "About 6 pages" / Latest Claude models: 1 Million tokens, ~1,000,000 words, "About the size of the first 5 Harry Potter novels" (the "latest" row needs refreshing whenever restored).
- **Markup if restored:** ShowcaseBox of cards: token-count pill + label on the left, words-and-analogy panel on the right. Search git history for `CONTEXT_WINDOW_FACTS`.

## "Prompt → Evaluate → Refine" — basketball-recap iteration walkthrough (+ usable-checklist framing)

- **Origin:** Check the Results lesson (`EvaluatingSection`). Removed 2026-07-03 when the lesson was rebuilt as a truth-first evaluation procedure (Read → Understand → Validate → Decide → go-deeper branches → Use it / Fix it / Walk away; spec: `docs/superpowers/specs/2026-07-03-check-results-critical-thinking-design.md`). The loop taught prompt-writing, the wrong altitude for an evaluation lesson — and The Art of Prompting couldn't absorb it either, since that lesson's thesis is "you don't need a prompting class, just three moves."
- **Possible destination:** a future dedicated "iterating with AI" lesson or lab; the walkthrough's round-2 beat (AI invents a "51-49 Lincoln lead" mid-draft and the learner catches it) is also a strong worked example for any hallucination-in-generative-work teaching.
- **Supporting state it needs if restored:** none — the `ITERATION_STEPS` array is a plain const rendered with shared components (`ShowcaseBox`, `InnerCard`, `UserBubble`, `AIBubble`, `Takeaway`), all still in `index.html`.
- **Full source:** in git history at the commit before the 2026-07-03 "Check the Results: rebuild as truth-first evaluation procedure" commit, inside `EvaluatingSection` — search anchor `ITERATION_STEPS`. The complete unit is: the 3-step `ITERATION_STEPS` const (generic prompt → refined prompt with invented-stat catch → Instagram-format polish), the "WHY EVALUATION MATTERS" ShowcaseBox (2 cards: "Correct doesn't mean usable" / "Evaluation tells you what to fix"), the "HOW TO REFINE" ShowcaseBox (3 cards: "Don't start over" / "Be specific about what's wrong" / "2–3 rounds is normal"), the "Prompt → Evaluate → Refine" ShowcaseBox that renders the steps with per-round 🔍 Evaluation / → Next Step callouts, and the Takeaway "Prompt. Evaluate. Refine. Repeat." Note the referenced six-criteria checklist ("Use these six criteria as a checklist") never existed in the code — only the sentence referring to it did.

## "Don't Reach for It When" — when-not-to-use-AI checklist (+ "Sometimes the answer is no" framing)

- **Origin:** the `AIStrengthsSection` module embedded in Check the Results (`evaluating`). Removed 2026-07-03: the lesson is about evaluating results, not deciding when to use AI, and the block predates the lesson's rebuild (it was scaffolding from a never-shipped standalone "How Much to Check" lesson — the component's non-embedded branch still references `sectionId: "howmuchtocheck"`). The module's intro paragraphs ("HOW MUCH TO CHECK" + trust framing) were cut in the same pass as redundant with the lesson's Step 4 Decide card.
- **Possible destination:** Integrity or Privacy lessons (two of the four groups are literally policy and private-information rules), a Work with AI opener, or a future "when to leave the tool closed" beat. The "You can't stand behind the result" group overlaps Check the Results' Walk-away verdict and When AI Acts' review rule.
- **Supporting state it needs if restored:** none — a static ShowcaseBox over an inline array of {group, items}.
- **Verbatim data:** ShowcaseBox kicker "DON'T REACH FOR IT WHEN"; lead-in "Before the dial even matters, there's a faster call. Some moments shouldn't go to AI at all: the sharpest move is to leave the tool closed and handle it yourself, or hand it to a real person." Groups: "The rule already says no" (assignment/policy forbids it; dodging the very skill you're there to build), "It involves private information" (your own sensitive details; someone else's private information), "You can't stand behind the result" (can't verify truth; high-stakes call needs a qualified human; would act under your name without review), "It's yours, or it needs a person" (needs your own voice or judgment; someone in real danger needs a person, now).

## "How Much to Check" — Good Fit / Needs Follow-Up decision-tree diagram

- **Origin:** the `AIStrengthsSection` module embedded in Check the Results (`evaluating`). Removed 2026-07-03: it was a second, parallel taxonomy of the decision the lesson's Step 4 card already teaches ("Can you judge the result yourself?" vs. "What kind of task was this?"), and its "Good Fit" verdict label is when-to-use-AI vocabulary. The Make the Call quiz that followed it survives (relabeled "Good to go" / "Needs Follow-Up") as the Step 4 practice; the quiz feedback now teaches the task-type taxonomy through play. The vestigial `howmuchtocheck` SECTION_META entry was removed in the same pass.
- **Possible destination:** Where AI Works Best (`whatitdoesbest`) — the diagram is literally a where-AI-works-well-vs-needs-care map; or any future when-to-use-AI beat.
- **Supporting state it needs if restored:** none as last shipped (the old Yes/No reveal had been made static: `yesClicked`/`noClicked` hardcoded true; those vars were deleted with it). Restoring the interactive reveal means real useState hooks plus the `softPulse` CSS animation (still in index.html).
- **Full source:** in git history at the commit before the 2026-07-03 "cut the parallel How Much to Check dial" commit, inside `AIStrengthsSection` — search anchor `Can you judge the result yourself?`. The complete unit: ShowcaseBox headline "How Much to Check"; root question card; SVG fork arrows; Yes → "✅ Good Fit" panel (Brainstorming / Summarizing / First drafts / Explaining concepts / Reformatting, each with a one-liner, footer "Best when you can judge whether the result makes sense."); No → "🔍 Needs Follow-Up" panel (Citations / Current events / Medical advice / Your Original Voice / Judgment calls, footer "Answer needs truth, safety, sources, or your judgment."). Also cut alongside: the "SET THE DIAL" kicker + type-of-task lead paragraph and the "Good Fit doesn't mean ready to use" paragraph.
