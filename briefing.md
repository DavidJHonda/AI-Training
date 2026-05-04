# Be Smarter Than the Tool — Project Briefing

## What this is
An instructor-led AI education web app for high schoolers. Single HTML file with inline React. Deployed via Vercel from GitHub repo "AI-Training". Owner: David. Audience: his twins and other 16-year-old students.

## Course structure
8 section groups, 50 lessons total.

- Intro (3): preassessment, whydeeper (titled "Why Learn AI?"), intro
- Foundations (8): aihistory, howwegothere, aistrengths, aivscode, blackbox, generative, data, hallucination
- Building the Model (6): training, trainingbias, tokens, embeddings, behindthenumbers, howreads
- Producing an Answer (7): context, probability, prediction, layers, attention, transform, inference
- Controls (5): modelselection, choosemodel, thinkingmode, temperature, customization
- Using AI Well (8): critical, mindtrap, flattery, prompting, thoughtpartner, verify, evaluating, whenaiacts
- AI in the Real World (8): questionsvaluable, humanedge, integrity, privacy, judged, synthetic, workchanges, aifuture
- Finish Line (5): whatyoulearned, fullworkflow, keyterms, testyourself, headtohead

## Design system

### Tokens (CSS custom properties, defined in :root)
- Colors: --bg #f6f5fb, --card #fff, --primary #6e51ff, --primaryDeep #4c2dff, --primaryFaint #f7f4ff, --ink #0e0a1f, --inkSoft #3a3550, --inkMuted #6e6986, --rule #e7e3f2, --green #1f9d5f, --red #d4334a
- Section divider color: #e5e7eb (used directly, not as a token)
- Typography: --sans (Plus Jakarta Sans), --serif (Instrument Serif)
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
- InteractiveBox: variant "try" (✎) or "see" (👁), purple-dashed border, --primaryFaint fill, green eyebrow. Optional title/hint/action/children.
- ShowcaseBox: framed callout for introducing or illustrating a concept, typically containing supporting cards. --primaryFaint fill, no border, borderRadius 20, padding 24. Props: kicker (renders SectionKicker above box), headline (bold line at top of box), intro (supporting paragraph), marginBottom (override default 24px). Children render below the intro. All props except children are optional.
- KeyInsight: structural takeaway callout, distinct from ShowcaseBox. --info-bg fill (light blue), no border, borderRadius 14, 🔑 icon. Props: lead (optional bold inline phrase before body), marginTop and marginBottom (override default 24px). Children render as body text at standard 17px. Used for lesson-level zoom-out takeaways, not casual tips. Different visual color from ShowcaseBox to differentiate the two patterns.
- PrimaryButton: purple fill, white text, hover lift, --primaryDeep on hover. Disabled prop. Renders trailing arrow automatically.
- SecondaryButton: transparent, --rule border, leading or trailing arrow.
- QuizBlock: recessed --bg fill, --rule border. Statement is sans 22px/600/--ink (NOT serif italic). Per-option correct via opt.correct.
- ProgressBar: 220px header right slot, "X of N lessons" where N = SECTIONS.length, gradient track --primary→#b08eff.

### Patterns
- Append-only progressive disclosure: state variable revealedCount, increments on click, content blocks render conditionally. Used in howwegothere (9 reveals through 350 years of history). Lighter than full state-machine progressive disclosure; classroom-friendly because past content stays visible.
- BottomLine and Next-button gating: when content uses progressive disclosure, BottomLine and the lesson's Next-button should be disabled until the final reveal. Pattern in use on aivscode, data, training, howwegothere.

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

## Open / pending

- 16 BottomLine takeaways drafted from scratch during Wave 4b — David said he'd review in context later
- Mobile responsive pass not validated
- 7 quizzes intentionally bespoke, not converted to QuizBlock (Test Yourself, Probability, Integrity, AI Strengths, HeadToHead, Key Terms, Training sorting)
- The twins haven't tested the app yet — recommendation is to ship and watch real students use it
- Two leftover items identified during audit, intentionally not cleaned up: dead "capstone" entry in CHIP_LABELS, orphan "llm-precheck-score" localStorage write that nothing reads back
- Consistency push: Wave 1 (ShowcaseBox) shipped. Future waves to extract TipCard (icon + title + desc pattern), StageCard (colored-border ladder pattern), and HighlightBox (dark gradient highlight pattern) once enough usages are catalogued. Smaller standardization passes still pending: h3 spacing, info-callout format consistency, two-column compare blocks.

## How to ask for help in this Project

Good first messages for new chats:
- "Look at the [lesson name] page. [What feels off]. WDYT?"
- "I want to change [specific thing] on [lesson]. Here's my draft: [draft]"
- "Audit the [section group] for [specific concern]"
- "Continue from where we left off — last session I [decision]"

Always ask Claude to read the current state of the relevant section in index.html before suggesting changes.