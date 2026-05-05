# Be Smarter Than the Tool — Project Briefing

## What this is
An instructor-led AI education web app for high schoolers. Single HTML file with inline React. Deployed via Vercel from GitHub repo "AI-Training". Owner: David. Audience: his twins and other 16-year-old students.

## Course structure
8 section groups, 51 lessons total.

- Intro (3): preassessment, whydeeper (titled "Why Learn AI?"), intro
- Foundations (8): aihistory, howwegothere, aistrengths, aivscode, blackbox, generative, data, hallucination
- Building the Model (6): training, trainingbias, tokens, embeddings, behindthenumbers, howreads
- Producing an Answer (7): context, probability, prediction, layers, attention, transform, inference
- Controls (5): modelselection, choosemodel, thinkingmode, temperature, customization
- Using AI Well (9): critical, mindtrap, flattery, engagementtrap, prompting, thoughtpartner, verify, evaluating, whenaiacts
- AI in the Real World (8): questionsvaluable, humanedge, integrity, privacy, judged, synthetic, workchanges, aifuture
- Finish Line (5): whatyoulearned, fullworkflow, keyterms, testyourself, headtohead

## Design system

### Tokens (CSS custom properties, defined in :root)
- Colors: --bg #f6f5fb, --card #fff, --primary #6e51ff, --primaryDeep #4c2dff, --primaryFaint #f7f4ff, --ink #0e0a1f, --inkSoft #3a3550, --inkMuted #6e6986, --rule #e7e3f2, --green #1f9d5f, --red #d4334a
- Section divider color: #e5e7eb (used directly, not as a token)
- Typography: --sans (Plus Jakarta Sans), --serif (Instrument Serif). Activity feedback prose uses Source Serif 4 (loaded from Google Fonts alongside the other two). All three are referenced directly by font-family string rather than CSS variable.
- Body paragraph standard: 17px / 1.65 line-height / var(--inkSoft)

### Design philosophy
- Borders are rare; prefer fill + shadow
- Borders only used on: lesson card, quiz container, lesson nav rule, section divider
- Three shadow roles: subtle (chips/pills), elevated (lesson card), active glow (purple)
- Active states are singular: one section pill, one chip, one primary button per page
- Serif (Instrument Serif) reserved for narrative moments only — lesson title and BottomLine
- Page background never goes white
- Spacing comes from a defined scale

### Components (defined near top of file)
- LessonHeader (~line 73): position eyebrow + serif title + optional subtitle. Eyebrow has split styling: "SECTION NN · GROUP · " in var(--inkMuted), "LESSON NN" in var(--primary).
- SectionKicker: page-level (size="large", 18px) or pre-content (size="small", 13px). Both purple, uppercase, weight 700. Use sparingly — only for genuinely multi-topic lessons or as the eyebrow for a ShowcaseBox. Default behavior is no kicker.
- BottomLine: italic eyebrow + 32px serif thought. Use {emphasis} braces for italic-purple emphasis spans.
- InteractiveBox: variant "try" (✎) or "see" (👁), purple-dashed border, --primaryFaint fill, green eyebrow. Optional title/hint/action/children. New `surface` prop accepts "mint" to switch container chrome to flat #eef4eb fill with no border (used by Pattern 2 activities). Default surface preserves the lavender + dashed treatment.
- ShowcaseBox: framed callout for introducing or illustrating a concept, typically containing supporting cards. --primaryFaint fill, no border, borderRadius 20, padding 24. Props: kicker (renders SectionKicker above box), headline (bold line at top of box), intro (supporting paragraph), marginBottom (override default 24px). Children render below the intro. All props except children are optional.
- KeyInsight: structural takeaway callout, distinct from ShowcaseBox. --info-bg fill (light blue), no border, borderRadius 14, 🔑 icon, inline layout (no eyebrow row, no flex columns). Props: lead (optional bold inline phrase rendered immediately after the 🔑), marginTop and marginBottom (override default 24px). Body renders at 17px / 1.65 line-height. Used for lesson-level zoom-out takeaways, not casual tips.
- PrimaryButton: purple fill, white text, hover lift, --primaryDeep on hover. Disabled prop. Renders trailing arrow automatically.
- SecondaryButton: transparent, --rule border, leading or trailing arrow.
- QuizBlock: recessed --bg fill, --rule border. Statement is sans 22px/600/--ink (NOT serif italic). Per-option correct via opt.correct.
- ProgressBar: 220px header right slot, "X of N lessons" where N = SECTIONS.length, gradient track --primary→#b08eff.

### Patterns
- Append-only progressive disclosure: state variable revealedCount, increments on click, content blocks render conditionally. Used in howwegothere (9 reveals through 350 years of history). Lighter than full state-machine progressive disclosure; classroom-friendly because past content stays visible.
- BottomLine and Next-button gating: when content uses progressive disclosure, BottomLine and the lesson's Next-button should be disabled until the final reveal. Pattern in use on aivscode, data, training, howwegothere.

## Activity Patterns
TRY IT and SEE IT activities follow one of two sanctioned interaction patterns. Both share the same visual language so the course feels unified across activities.

### Choosing between patterns
- **Pattern 1 (Progressive Disclosure)**: each scenario is its own moment with setup + question + per-question feedback. Use when sequential pacing builds the lesson. Best for quiz-style scenarios where the student needs to focus on one item at a time.
- **Pattern 2 (Parallel Sort/Match)**: all items visible at once, sorted independently. Use when the cognitive work is "look at the full picture, make multiple decisions." Best for sorting/categorization tasks. Per-item feedback reveals as each item is answered.
- Bespoke activities (text entry, redaction, builders, sliders) sit outside both patterns and stay one-off.

### Shared visual language
Both Pattern 1 and Pattern 2 inherit the mint surface and the typography below.

- Container: InteractiveBox with `surface: "mint"` — flat #eef4eb fill, no border, borderRadius 16, padding 26px 28px
- TRY IT eyebrow: Plus Jakarta Sans 700, 11px, letter-spacing 0.14em, uppercase, mint accent #2f7d4f
- Activity title: Plus Jakarta Sans 700, 22px (default InteractiveBox title size), --ink color
- Question numerals: Instrument Serif 400, 44px, line-height 1, color #2f7d4f, opacity 0.6 when locked / 1.0 when active or answered
- Question prompts: Plus Jakarta Sans 600, 18px, line-height 1.4, color #0e0a1f, max-width 56ch
- Answer pills: Plus Jakarta Sans 700, 14px, padding 11px 22px, min-width 96px, borderRadius 999. Default state: white fill, --rule border, --ink text. Correct selection: filled #1f9d5f, white text, ✓ inside. Wrong selection: #f1f0f3 fill, transparent border, #6e6986 text, red ✕ inside (#d4334a). Untouched pill on a wrong row: stays default white outline.
- Feedback prose: Source Serif 4 (italic optional), 16px, line-height 1.55, max-width 60ch. Color #1f9d5f for correct, #d4334a for wrong. Prefixed by a 20px circular ✓ or ✕ icon in matching color with white glyph.
- Counter pill (top-right of activity): white fill, soft shadow, "N OF M" — bold count + uppercase letterspaced "of M".

### Pattern 1: Progressive Disclosure spec
- InteractiveBox `variant: "try"` or `"see"`, `surface: "mint"`, with title and counter `action`
- RevealSequence drives advancement: state for currentIdx, started, answer-per-scenario
- Inside RevealSequence children, render: scenario card (mint subtle), optional chat bubbles, then QuizBlock
- QuizBlock renders vertical-stack option buttons styled to match the shared visual language (same fonts, same border treatment, in-place feedback expansion)
- Completion element: centered card, soft icon, bold one-line takeaway, soft body text — all in shared typography

### Pattern 2: Parallel Sort/Match spec
- InteractiveBox `variant: "try"`, `surface: "mint"`, with title and counter `action`
- All items render in vertical sequence with hairline dividers between rows: `1px solid rgba(63, 107, 63, 0.18)`, padding 24 above/below per row, no divider above first row
- Each row layout: numeral on left + content stack on right, vertically centered with each other (alignItems center on the title row), gap 22px
- Content stack indents pills and feedback under the task text using paddingLeft equal to numeral width + gap (typically 66px)
- Per-item feedback reveals immediately after answer; answers lock once chosen
- NextLessonGate ready when `Object.keys(answers).length >= items.length`

Reference implementation: ThinkingMode "Match the Task to the Mode" (canonical Pattern 2). Pattern 1 reference implementations: MindTrap, FlatteryTrap, EngagementTrap, BlackBox (Rule/Pattern/Guardrail), Hallucination.

## Workflow

David's process:
1. Discuss the change in this Project chat
2. Get an implementation-ready prompt as a copyable code block
3. Paste into Claude Code (claude --dangerously-skip-permissions for long waves)
4. Verify in browser
5. Iterate

David's preferences:
- Plain copy, McDonald's-humor friendly tone for students
- Implementation-ready prompts referencing exact line numbers, existing patterns, variable names
- No file downloads — always copyable code blocks
- Says "agree" or "yes" when aligned; pushes back when not
- Avoids em-dashes in his own writing; course content uses them freely

When David asks for content changes, the right pattern is:
1. Read the current state of the relevant section in index.html
2. Propose options or ask clarifying questions if ambiguous
3. Once aligned, draft the prompt as a code block
4. After he runs it, ask what he saw in the browser and iterate if needed

## Recent significant decisions

### Earlier waves
- "Why Go Deeper?" renamed to "Why Learn AI?" and moved from Foundations to Intro. Navigation chain: PreAssessment → WhyDeeper → Intro → AIHistory.
- "The G in GPT" renamed to "Generative." New intro covers generation and non-retrieval; ends with probability-priming sentence.
- "Where AI Helps" labels changed: Good Fit / Look It Up (was Good Fit / Use Carefully). Question changed to "Can you judge the result yourself?" Sub-categories removed.
- "Rules vs Patterns" intro rewritten: calculator vs ChatGPT framing, two paragraphs, probability-priming.
- "How We Got Here" restructured as 9-step progressive reveal. Order: intro → "Where it began" button → Pascal & Fermat 1654 → Bayes 1763 → 1943 → 1950 → 1956 → 1957 → 1986 → 2017 → 2022 → BottomLine.
- "No One Wrote the Rules" rewritten with credit card analogy, news bullets (criminals/bullies/medical), and AI Companies note (OpenAI, Anthropic, Google). Comparison boxes and books-don't-exist callout removed.
- AGI/ASI vocabulary block lives in aifuture, not aihistory. Frames them as "vocabulary of the argument," not present-tense objects.

### Coverage gap session (added two new lessons + content additions across the file)
- New lesson: "Seeing Isn't Proof" (id `synthetic`) in AI in the Real World. Three-checks framework (Source / Context / Corroboration), five teen-stakes scenarios (voice clone, fake photo, principal deepfake, DM video call, fake screenshot), BottomLine "Seeing is no longer proof. Where it came from is."
- New lesson: "When AI Judges You" (id `judged`) in AI in the Real World, slotted between Privacy and Synthetic. Three modes (what you see / what you can do / what gets attached to your name), five-question framework, five teen-stakes scenarios (AI detector flag, AI-assisted college admissions, TikTok For You feed, Discord auto-removal, AI-screened internship), BottomLine "The AI you never opened is still making decisions about you."
- Generative: added "What about when it searches?" closing block introducing the model-vs-product distinction so students aren't confused when ChatGPT shows search animations.
- Verify: added a 6th strategy "Don't trust the source link" to the existing five-strategy reveal sequence.
- When AI Acts: added a sixth permission scenario (email forwarding via prompt injection) and a new "hidden-instruction rule" gradient highlight box pairing the existing "five-word rule" highlight. Big bold line: "The AI can't tell you apart from a webpage."
- Integrity: added "Plagiarism vs Copyright" section (two-card neutral contrast + three practical rules), "Show Your Process" section (5 artifact types + receipts callout). Removed misleading "AI detectors are getting better" line from a scenario explanation. BottomLine updated to "'AI made it' doesn't mean 'I did it.' And it doesn't mean 'I own it.'"
- Choosing the Model: added "When you hear 'best model'" closing section with four-question checklist (On what test? For what task? With what tools? At what cost and speed?).

### Audit pass
- ProgressBar fallback now reads from SECTIONS.length instead of hardcoded 45.
- PredictionSection routing fixed: was incorrectly routing to "howreads" (Building the Model group), now correctly routes to "layers" (Producing an Answer group).
- Seven Next button labels aligned to match the destination page's actual title (e.g. "Next: Customization & Memory" → "Next: Customization", "Next: Privacy & Awareness" → "Next: Privacy", etc.).
- Four cross-group transition labels intentionally retained as group names ("Next: Building the Model", "Next: Producing an Answer", "Next: Controls", "Next: Using AI Well").

### Consistency push (in progress)
- Wave 1: Defined ShowcaseBox component. Migrated three boxes in AIHistorySection to use it. Canonical style: --primaryFaint fill, no border, borderRadius 20, padding 24, with SectionKicker outside the box.
- Wave 2: Defined KeyInsight component. Migrated 5 existing key-insight boxes (ModelSelection, Verify, FlatteryTrap, QuestionsValuable, WorkChanges) to use it. Canonical style: --info-bg fill, no border, 🔑 icon, body at 17px. Distinct from ShowcaseBox by color.
- Wave 3: Redesigned KeyInsight to inline layout (icon + text in one flow, no flex columns). Migrated 17 callouts total: PreAssessment, Embeddings, BehindTheNumbers, Inference (restructured from wrapped demo to h3 + body + KeyInsight), Customization, ModelSelection, ChoosingModel (merged two boxes into one), ThinkingMode, Hallucination, FlatteryTrap, Integrity (×3: simple test, best defense, goal), Privacy (golden rule), QuestionsValuable (The shift), HumanEdge, WorkChanges. Zero remaining "🔑 Key Insight" or "🔑 The key insight" eyebrow strings in the file.
- Mind Trap rewrite: replaced opening with Moby Dick boat-personification hook ("A noble craft, but somehow a most melancholy"). Added two-word definition card teaching personification (linguistic move) + anthropomorphization (cognitive trap). Reframed second ShowcaseBox to "Who's Behind the Words?" comparing human writing vs AI generation. Replaced 3-scenario activity with 3-option format (correct / mind-trap wrong / overcorrection wrong); scenario 1 swapped from analysis-of-quote to AI-personifying-code example. Added KeyInsight ("The danger isn't that AI sounds nice"). Updated BottomLine to "Language makes your brain search for a person. With AI, {don't invent one}."
- New lesson: Engagement Trap (id `engagementtrap`) added to Using AI Well between Flattery and Prompting. Teaches the conversation-continuation pattern (offering follow-ups, asking clarifying questions, volunteering next steps). Three-card "Pattern in the wild" ShowcaseBox + 3-scenario activity + KeyInsight on training-for-engagement + Don't Overcorrect closer. Course total moved from 50 to 51 lessons. Made it the third entry in the trap-trilogy alongside Mind Trap and Flattery Trap.
- Wave 4 (in progress): Activity Pattern visual system established. Pattern 2 canonical built on ThinkingMode "Match the Task to the Mode": mint InteractiveBox surface, Instrument Serif numerals (44px, mint accent), Plus Jakarta Sans question prompts (18px / 600), pill answer buttons (no icons, correctness-based fill colors — green correct / soft-gray wrong with red ✕), Source Serif 4 feedback prose, hairline dividers between rows, "N OF M" counter pill in top-right. Pattern 1 visual migration to mint surface + matching typography pending across roughly 20 activities.

## Open / pending

- Mobile responsive pass not validated
- 7 quizzes intentionally bespoke, not converted to QuizBlock (Test Yourself, Probability, Integrity, AI Strengths, HeadToHead, Key Terms, Training sorting)
- The twins haven't tested the app yet — recommendation is to ship and watch real students use it
- Two leftover items identified during audit, intentionally not cleaned up: dead "capstone" entry in CHIP_LABELS, orphan "llm-precheck-score" localStorage write that nothing reads back
- Consistency push: Waves 1 (ShowcaseBox), 2/3 (KeyInsight), and the Activity Patterns work shipped. ShowcaseBox migrations applied across roughly 28 sections including IntroSection (Skills hero + Roadmap blocks consolidated to ShowcaseBox) and WhyDeeperSection (EDGE_CARDS + FUTURE_CARDS converted). IntroSection's Skills hero specifically merged the freestanding hero gradient + SectionKicker + cards into one unified ShowcaseBox. AIFuture closing previously restructured to remove gradient frame and use SectionKicker + body + ShowcaseBox + page-level callouts. Lavender-fill-no-border established as a usable pattern in two flavors: full ShowcaseBox component for framework content with cards, plain styled wrapper for prose sidebars. Future waves to extract TipCard (icon + title + desc pattern), StageCard (colored-border ladder pattern, used in 3+ ShowcaseBoxes), and HighlightBox (dark gradient highlight pattern) once enough usages are catalogued. Decision pending whether to demote casual 💡 lightbulb tips to plain bold body paragraphs (current lean) or formalize as a separate small Tip pattern. Smaller standardization passes still pending: h3 spacing, info-callout format consistency, two-column compare blocks. Pattern 1 visual migration to the new mint Activity Pattern system pending across the roughly 20 progressive-disclosure quiz activities.

## How to ask for help in this Project

Good first messages for new chats:
- "Look at the [lesson name] page. [What feels off]. WDYT?"
- "I want to change [specific thing] on [lesson]. Here's my draft: [draft]"
- "Audit the [section group] for [specific concern]"
- "Continue from where we left off — last session I [decision]"

Always ask Claude to read the current state of the relevant section in index.html before suggesting changes.