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
