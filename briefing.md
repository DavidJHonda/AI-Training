# Be Smarter Than the Tool — Project Briefing

## What this is
A self-paced AI education web app for high schoolers. Single HTML file (index.html) with inline React. Deployed via Vercel from GitHub repo "AI-Training". Owner: David. Audience: his twins and other 16-year-old students.

## Lesson map
67 lessons across 10 section groups. Each lesson is listed as `Displayed Label (internal id)`. The id is the React component key and navigation reference used in code; the label is what students see in the UI.

- Intro (4): Welcome (welcome), Why Learn AI? (whydeeper), What Only You Can Do (humanjob), The Roadmap (intro)
- Foundations (9): Opener (openerfoundations), What Is AI? (aihistory), What's an LLM? (llms), AI is Math (aiismath), How We Got Here (howwegothere), Rules vs Patterns (aivscode), No One Wrote the Rules (blackbox), Generative (generative), AI's Fuel (data)
- Under the Hood (8): Opener (openerinside), Tokens (tokens), Embeddings: Meaning as Numbers (embeddings), Vector Space: Meaning by Similarity (vectorspace), Inside the Model (behindthenumbers), Attention & Transformation (howreads), Training (training), Training Bias (trainingbias)
- AI Answers (6): Opener (openeranswers), Context Window (context), Probability (probability), Prediction (prediction), Layers (layers), Inference: From Prompt to Output (inference)
- Controls (6): Opener (openercontrols), Choosing the Product (modelselection), Choosing the Model (choosemodel), Thinking Mode (thinkingmode), Temperature (temperature), Customization & Memory (customization)
- Traps (8): Opener (openertraps), Hallucination (hallucination), Whole Document Trap (documentchat), Mind Trap (mindtrap), Flattery Trap (flattery), Engagement Trap (engagementtrap), Support Trap (supporttrap), When AI Acts (whenaiacts)
- Human Judgment (5): Opener (openerjudgment), The AI Trust Test (aistrengths), Critical Thinking & AI (critical), Questions Matter (questionsvaluable), Skills That Matter (humanedge)
- Workflow (7): Opener (openerusing), What AI Does Best (whatitdoesbest), The Art of Prompting (prompting), Your Thought Partner (thoughtpartner), Studying With AI (studying), How to Verify (verify), Evaluating the Results (evaluating)
- Real World (9): Opener (openerrealworld), Academic Integrity (integrity), Privacy & Awareness (privacy), When AI Judges You (judged), Who Else Is Affected (stakeholders), Seeing Isn't Proof (synthetic), Work Changes (workchanges), AI & The Future (aifuture), Build Your Edge (buildedge)
- Finish (5): What You Learned (whatyoulearned), Full Workflow (fullworkflow), Vocab Quiz (keyterms), Test Yourself (testyourself), Beat the Clock (headtohead)

## Design system

### Tokens (CSS custom properties, defined in :root)
- Colors (surfaces): --bg #f6f5fb, --card #fff, --primary #6e51ff, --primaryDeep #4c2dff, --primaryFaint #f7f4ff
- Colors (text): --ink #0e0a1f, --inkSoft #3a3550, --inkMuted #6e6986, --inkFaint #b3aec8
- Colors (lines): --rule #e7e3f2
- Colors (semantic): --green #1f9d5f, --red #d4334a, --info #3b82f6, --info-bg #eff6ff
- SEE IT band: --seeBand #faf6ec (sand surface), --seeAccent #a36a17 (amber accent), --seeRule rgba(163, 106, 23, 0.18) (amber hairline)
- KEY TERM band: --termBand #fdf2f8 (light pink surface), --termAccent #be185d (magenta accent)
- TRY IT colors (inlined, no named vars): mint surface #eef4eb, green accent #2f7d4f, mint hairline rgba(63, 107, 63, 0.18)
- Typography: --sans (Plus Jakarta Sans, Google Fonts), --serif (Instrument Serif, Google Fonts), --mono (system monospace stack). Activity feedback prose uses Source Serif 4 (also from Google Fonts) referenced directly by font-family string.
- Body paragraph standard: 17px / 1.65 line-height / var(--inkSoft)

### Design philosophy
- Borders are rare in page-level chrome and narrative containers. ShowcaseBox, KeyInsight, KeyTerm, CompareCard, and InteractiveBox (mint and sand surfaces) all use fill + shadow with no border.
- Activity interiors may use --rule borders where the border carries meaning, separating choices, feedback, and interactive states.
- Three shadow roles: subtle (chips/pills), elevated (lesson card), active glow (purple).
- Active states are singular: one section pill, one chip, one primary button per page.
- Serif (Instrument Serif) reserved for the lesson title only.
- Page background never goes white.
- Spacing comes from a defined scale.

### Components (defined near top of file)
- **BodyP**: standard body paragraph (17px / 1.65 / var(--inkSoft)). Props: marginBottom (default 18), style (additional overrides like maxWidth). Used for all lesson prose. Inline `<p>` is reserved for non-standard sizes (captions, card body text).
- **LessonHeader**: position eyebrow + serif title + optional subtitle. Eyebrow has split styling: "SECTION NN · GROUP · " in var(--inkMuted), "LESSON NN" in var(--primary).
- **SectionKicker**: page-level (size="large", 18px) or pre-content (size="small", 13px). Both purple, uppercase, weight 700. Also serves as the in-body section break within a lesson — what used to be LessonSubhead is now a SectionKicker call. Default behavior is no kicker.
- **ShowcaseBox**: framed callout for introducing or illustrating a concept, typically containing supporting cards. --primaryFaint fill, no border, borderRadius 20, padding 24. Props: kicker, headline, intro, marginBottom (default 24px), children.
- **KeyInsight**: structural takeaway callout. --info-bg fill (light blue), no border, borderRadius 14, 🔑 icon, inline layout. Props: lead (optional bold inline phrase), marginTop, marginBottom (default 24px each). Used for lesson-level zoom-out takeaways.
- **KeyTerm**: vocab introduction card. Pink band (--termBand) with 📖 icon and bold magenta term (--termAccent). Props: term (required). Looks up the matching entry from the TERMS array, so vocab definitions in lessons cannot drift from the vocab quiz. Currently used in BlackBox for "Guardrail."
- **InteractiveBox**: activity container. Variant "try" (✎) or "see" (◉). Surface "mint" (flat #eef4eb, no border, 16px radius) or "sand" (var(--seeBand), no border, 24px radius, 32-36px padding). Sand surface renders the eyebrow in var(--seeAccent) amber. Default surface uses --primaryFaint with dashed border. Optional title/hint/action/children.
- **PrimaryButton**: purple fill, white text, hover lift. Auto-adds trailing arrow. The end-of-lesson Next button.
- **ActivityButton**: dark-ink fill, white text. Used inside activities for RevealSequence start/next buttons and other in-activity actions. Quieter than PrimaryButton. Sizes: default and "large".
- **NextLessonGate**: bottom-of-lesson Next button gated on a `ready` boolean. Renders the PrimaryButton when ready, otherwise a small `lockedMessage` string (default "Complete the exercises to continue"). Strong-gate lessons use the default; weak-gate lessons override with "Try one to continue."
- **OpenerSection**: standardized opener-page wrapper. Slots: LessonHeader (with optional bigIdea subtitle), whyThisMatters paragraphs, optional featuredCard, whatYoullLearnIntro, ShowcaseBox-wrapped openQuestions grid, whatYoullLearnClosing, optional KeyInsight (lead "The common mistake:"), framing KeyInsight (lead "Keep this question in mind:" rendered from each opener's `question` prop), PrimaryButton. Each section group's opener is a thin wrapper passing content props, so format changes propagate to every opener.
- **QuizBlock**: recessed --bg fill, --rule border. Statement is sans 22px/600/--ink. Per-option correctness via opt.correct.
- **RevealSequence**: state-machine progressive-disclosure driver for SEE IT activities. Manages currentIdx, started, per-stage state. Drives Pattern A (one stage swaps in at a time) and the ladder-mode sub-variant (cumulative reveal). Accepts a surface prop matching InteractiveBox.
- **CompareCard**: tinted comparison card chrome. No border, 16px radius, 20px padding, soft shadow (0 8px 22px rgba(14, 10, 31, 0.05)). Props: bg (required tint color), centered (optional), style (optional). Canonical inner-block treatment: any visible container inside a CompareCard is white with no border.
- **ScenarioRow**: wraps Pattern 2 row chrome. Serif numeral, optional kicker, prompt text, indented pill row, feedback strip. Props: index (1-based), kicker, prompt, answered, correct, feedback, children.
- **FeedbackPill**: pill button for Pattern 2 sort activities. Props: state ("default" | "picked-correct" | "picked-wrong" | "answered-untouched"), label, onClick.
- **UserBubble / AIBubble / ThinkingBubble**: chat-style speech bubbles. UserBubble (right-aligned, primary-faint fill), AIBubble (left-aligned, white card), ThinkingBubble (left-aligned, animated ellipsis). UserBubble and AIBubble accept optional visibleChars / visibleWords props for typing animations.
- **ProgressBar**: 220px header right slot, "X of N lessons" where N = SECTIONS.length, gradient track --primary→#b08eff.
- **useReducedMotion**: hook reading prefers-reduced-motion via matchMedia, updates mid-session. Returns boolean. Gates JS-driven typewriter and reveal animations so they tick at 1ms when reduced motion is requested.

### TERMS array
Source of truth for vocabulary. Defined near the top of the file as a flat array of `{ term, definition, source }` entries. The KeyTerm component looks up definitions here, and the Vocab Quiz lesson uses the same array (currently slicing the first 16 entries across two rounds of 8). Adding a new term in two places (the array and the quiz round count, if growing past 16) keeps lesson copy and quiz definitions aligned.

### Activity Patterns
TRY IT and SEE IT activities share a visual language and follow one of two interaction patterns each. Bespoke activities (text entry, redaction, builders, sliders) sit outside both patterns and stay one-off.

#### Shared visual language (TRY IT, both patterns)
- Container: InteractiveBox with `surface: "mint"`. Flat #eef4eb fill, no border, borderRadius 16, padding 26px 28px.
- Eyebrow: "✎ TRY IT" in Plus Jakarta Sans 700, 11px, letter-spacing 0.14em, uppercase, mint accent #2f7d4f.
- Title: Plus Jakarta Sans 700, 22px, --ink.
- Question numerals: Instrument Serif 400, 44px, line-height 1, color #2f7d4f. Opacity 0.6 when locked, 1.0 when active or answered.
- Question prompts: Plus Jakarta Sans 600, 18px, line-height 1.4, color #0e0a1f, max-width 56ch.
- Answer pills: Plus Jakarta Sans 700, 14px, padding 11px 22px, min-width 96px, borderRadius 999. Default state: white fill, --rule border, --ink text. Correct selection: filled #1f9d5f, white text, ✓ inside. Wrong selection: #f1f0f3 fill, transparent border, #6e6986 text, red ✕ inside (#d4334a).
- Feedback prose: Source Serif 4 (italic optional), 16px, line-height 1.55, max-width 60ch. Color #1f9d5f for correct, #d4334a for wrong. Prefixed by a 20px circular ✓ or ✕ icon in matching color.
- Counter pill (top-right of activity): white fill, soft shadow, "N OF M" (bold count, uppercase letterspaced "of M").

#### TRY IT Pattern 1: Progressive Disclosure
Each scenario is its own moment with setup + question + per-question feedback. Use when sequential pacing builds the lesson.
- InteractiveBox variant "try", surface "mint", title and counter action.
- RevealSequence drives advancement: state for currentIdx, started, answer-per-scenario.
- Inside RevealSequence children: scenario card (mint subtle), optional chat bubbles, then QuizBlock.
- QuizBlock vertical-stack option buttons styled to match the shared visual language.
- Completion element: centered card, soft icon, bold one-line takeaway, soft body text.

#### TRY IT Pattern 2: Parallel Sort/Match
All items visible at once, sorted independently. Best for sorting/categorization tasks. Per-item feedback reveals as each item is answered.
- InteractiveBox variant "try", surface "mint", title and counter action.
- All items render in vertical sequence with hairline dividers between rows: 1px solid rgba(63, 107, 63, 0.18), padding 24 above/below per row, no divider above first row.
- Each row uses ScenarioRow: numeral on the left, content stack on the right, vertically centered.
- Pills indent to align under the prompt (paddingLeft equal to numeral width + gap, typically 66px).
- Per-item feedback reveals immediately after answer; answers lock once chosen.
- NextLessonGate ready when `Object.keys(answers).length >= items.length`.

#### SEE IT Pattern A: Progressive Reveal, Sand Chrome
Stages reveal one at a time. Mirrors TRY IT Pattern 1 structurally; differs in color, shell, and the absence of QuizBlock.
- Shell: InteractiveBox with variant "see" and surface "sand". Sand band wrapper (var(--seeBand), no border, 24px radius, 32-36px padding). Eyebrow "◉ SEE IT" in var(--seeAccent) amber.
- Counter pill: identical to TRY IT visually.
- Engine: RevealSequence with surface "sand". Uses ActivityButton for start/next/finish buttons (dark ink, shared with mint surface).
- Stage interior: ivory inner card (white, 14px radius, soft shadow at 0 4px 12px rgba(14,10,31,0.05), 18-22px padding). Header row: serif amber numeral (Instrument Serif 32px, zero-padded "01" through "0N"), icon + Plus Jakarta Sans bold label (17px), Source Serif 4 description (15px, color #3a3550). Subsequent sections separated by var(--seeRule) hairlines, each introduced by an amber 11px eyebrow with emoji prefix.
- Completion card: centered, emoji + Plus Jakarta Sans bold heading + Source Serif 4 body, 60ch max-width.
- NextLessonGate: gates on full completion (activeIdx >= items.length).
- Ladder-mode sub-variant: stages stay visible cumulatively in one ivory card with var(--seeRule) hairlines between them. Most recent reveal animates in; earlier stages render statically. Used when stages build on each other (How LLMs Train, Three Steps to an Answer).
- No-completion-card variant: set isComplete: false on RevealSequence and gate canAdvance on `... && currentIdx < items.length - 1` so the activity ends on the last stage's content (Context "Same Prompt, Different Context").
- Pedagogical color preservation: SEE IT migrations recolor chrome to amber. They do NOT recolor interior content where color carries lesson meaning (Messy In's blue/red/purple Computer/Failure/AI palette, Context's role colors, Prediction's blue/purple/green steps).

#### SEE IT Pattern B: Parallel Reveal, Sand Chrome
Comparison matters more than sequence. All stages render at once as ivory cards stacked inside the sand band, separated by var(--seeRule) hairlines. No RevealSequence, no counter pill.

## Working agreements

### David's setup
Designs prompts in chat with Claude (this Project). Pastes prompts into Claude Code in his VS Code terminal, where they get applied to the file. Verifies changes in his browser. Repo: AI-Training, single index.html file, deployed via Vercel.

### Preferences
- Plain copy, McDonald's-humor friendly tone for the student audience (16-year-olds).
- Implementation-ready prompts referencing exact line numbers, existing patterns, and variable names.
- No file downloads, always copyable code blocks.
- David avoids em-dashes in his own writing. Course content uses them freely.

### Default mode
Collaborative content design. Propose options, ask for confirmation, then draft prompts. When David has clearly decided something, skip straight to the prompt. When something is ambiguous, ask before drafting.

### The pattern for content changes
1. Read the current state of the relevant section in index.html before suggesting copy or structure.
2. Propose options or ask clarifying questions if ambiguous.
3. Once aligned, draft the prompt as a code block.
4. After David runs it, ask what he saw in the browser and iterate if needed.

### When David returns with twin-testing feedback
Name the lesson, describe what felt off, read the relevant section in index.html before proposing options. Twin feedback might be a copy fix, an interaction fix, or a sign the lesson itself needs rethinking. Figure out which before drafting any prompt.
