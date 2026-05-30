# Be Smarter Than the Tool — Project Briefing

## What this is
An instructor-led AI education web app for high schoolers, built to be taught live but easily repurposed for self-paced use. Single HTML file (index.html) with inline React. Deployed via Vercel from GitHub repo "AI-Training". Owner: David. Audience: his twins and other 16-year-old students.

## Lesson map
69 lessons across 7 section groups (a five-part content spine plus Intro and Finish), listed in delivery order. Each lesson is listed as `Displayed Label (internal id)`. The id is the React component key and navigation reference used in code; the label is what students see in the UI.

- Intro (6): Welcome (welcome), Why Learn AI? (whydeeper), Does AI Think? (doesaithink), Why Bother Learning? (whybother), What You Can Control (control), The Roadmap (intro)
- Understand AI (22): one section group spanning three movements (former Foundations, Inside AI, AI Answers; internal order unchanged):
  - Foundations movement: Opener (openerfoundations), What Is AI? (aihistory), What's an LLM? (llms), AI is Math (aiismath), How We Got Here (howwegothere), Rules vs Patterns (aivscode), No One Wrote the Rules (norules), AI's Fuel (data)
  - Inside AI movement: Opener (openerinside), Tokens (tokens), Embeddings: Meaning as Numbers (embeddings), Vector Space: Meaning by Similarity (vectorspace), Inside the Model (insidethemodel), Attention & Transformation (attention), Layers (layers), Training (training)
  - AI Answers movement: Opener (openeranswers), Your Input & the Context Window (prompt), Patterns (patterns), Probability (probability), Inference: From Prompt to Output (inference), What AI Does Best (whatitdoesbest)
- Work With AI (9): Opener (openerworkwith), Choosing the Product (modelselection), Choosing the Model (choosemodel), Thinking Mode (thinkingmode), Temperature (temperature), Customization & Memory (customization), Questions Matter (questionsvaluable), The Art of Prompting (prompting), Your Thought Partner (thoughtpartner)
- Judgment I: Check the Output (7): Opener (openercheck), Critical Thinking (critical), How to Verify (verify), Evaluating the Results (evaluating), Hallucination (hallucination), Training Bias Trap (trainingbias), Whole Document Trap (documenttrap)
- Judgment II: Protect Yourself (11): Opener (openerprotect), Mind Trap (mindtrap), Flattery Trap (flattery), Engagement Trap (engagementtrap), Support Trap (supporttrap), When Not to Use AI (whennot), How Much to Check (howmuchtocheck), Studying With AI (studying), Academic Integrity (integrity), Privacy & Awareness (privacy), Seeing Isn't Proof (seeingisntproof)
- Build Your Advantage (9): Opener (openerrealworld), Work Changes (workchanges), The Rise of Agents (agents), When AI Judges You (aijudges), Who Else Is Affected (stakeholders), AI & The Future (aifuture), Skills That Matter (humanedge), Creative Thinking (creativethinking), Build Your Edge (buildedge)
- Finish (5): What You Learned (whatyoulearned), The Full Loop (fullworkflow), Vocab Quiz (keyterms), Test Yourself (testyourself), Beat the Clock (headtohead)

Structure notes (after the May 2026 restructure): the spine is Intro → Understand AI → Work With AI → Judgment I: Check the Output → Judgment II: Protect Yourself → Build Your Advantage → Finish. Part badges read "NN / 7" and are derived from `SECTION_GROUPS` via `partBadge()`, not hand-typed; Intro and Finish carry no badge, and within Understand AI only openerfoundations carries the part badge while openerinside/openeranswers show a quiet "Understand AI · N of 3" movement label. The four former section openers (openerusing, openercontrols, openertraps, openerjudgment) are retired: still defined in the file as dead components, but removed from `SECTION_GROUPS` and `SECTION_COMPONENTS`. The Build Your Advantage opener keeps the component id `openerrealworld` (displayed title "Build Your Advantage"). Studying/Integrity/Privacy now live in Judgment II (the responsible-use home), no longer "parked."

## Design system

### Tokens (CSS custom properties, defined in :root)
- Colors (surfaces): --bg #f6f5fb, --card #fff, --primary #6e51ff, --primaryDeep #4c2dff, --primaryFaint #f7f4ff
- Colors (text): --ink #0e0a1f, --inkSoft #3a3550, --inkMuted #6e6986, --inkFaint #b3aec8
- Colors (lines): --rule #e7e3f2
- Colors (semantic): --green #1f9d5f, --red #d4334a, --info #3b82f6, --info-bg #eff6ff
- SEE IT band: --seeBand #faf6ec (sand surface), --seeAccent #a36a17 (amber accent), --seeRule rgba(163, 106, 23, 0.35) (amber separator, commonly used as a 2px rule)
- KEY TERM band: --termBand #e9ecf0 (slate surface), --termAccent #475569 (slate accent)
- TRY IT band: --tryBand #eef4eb (mint activity surface), --tryRule rgba(63, 107, 63, 0.18) (mint hairline divider), --tryAccent #2f7d4f (green accent; mint InteractiveBox eyebrows and TRY IT Takeaway completions). The AIBubble reuses the same mint as its fill, documented under UserBubble/AIBubble.
- ILLUSTRATION band: --illoBand #f5e1d4 (warm sand surface), --illoAccent #b5532f (terracotta accent). Opener-support display band; see Illustration component.
- Typography: --sans (Plus Jakarta Sans, Google Fonts) for all reading text, --serif (Instrument Serif, Google Fonts) for display moments only (lesson titles, activity numerals, and opener/Illustration display phrases), never explanatory prose or feedback. --mono (system monospace stack). Source Serif 4 is no longer used; it was retired when all explanatory and feedback prose moved to sans.
- Shadows: --shadowSoft (0 4px 12px rgba(14, 10, 31, 0.05)) for inner cards, pills, and counters; --shadowElevated (0 8px 22px rgba(14, 10, 31, 0.05)) for support cards. Active-glow and a few one-off elevated/inset shadows remain inlined per-use, mostly on assessment and diagram surfaces.
- Body paragraph standard: 17px / 1.65 line-height / var(--inkSoft)

### Design philosophy
- Borders are rare in page-level chrome and narrative containers. ShowcaseBox, KeyInsight, KeyTerm, CompareCard, and InteractiveBox (mint and sand surfaces) all use fill + shadow with no border.
- Activity interiors may use --rule borders where the border carries meaning, separating choices, feedback, and interactive states.
- Two shadow tokens: --shadowSoft (inner cards, pills, counters) and --shadowElevated (support cards). Active-glow and one-off elevated/inset shadows are inlined per-use on assessment and diagram surfaces.
- Active states are singular: one section pill, one chip, one primary button per page.
- Serif (Instrument Serif) is for display moments only: lesson titles, activity numerals (SEE IT and TRY IT), and editorial display phrases inside opener Illustrations and late synthesis headings. Every other piece of text, including all explanatory prose and activity feedback, is sans (Plus Jakarta Sans). The old reading serif (Source Serif 4) has been retired.
- Page background never goes white.
- Vertical rhythm: card-level blocks (InteractiveBox, ShowcaseBox, KeyInsight) carry a default bottom margin of var(--blockGap) (24px); body paragraphs use 18px. Blocks render in normal flow, so adjacent margins collapse to the larger value and never stack. Pass marginBottom/marginTop to override. Spacing inside components and diagrams is still inline per-context; there is no global numeric scale beyond --blockGap.

### Components (defined near top of file)
- **BodyP**: standard body paragraph (17px / 1.65 / var(--inkSoft)). Props: marginBottom (default 18), style (additional overrides like maxWidth). Used for all lesson prose. Inline `<p>` is reserved for non-standard sizes (captions, card body text).
- **ActivityInstruction**: the one-line "how to do this activity" instruction that sits below the title inside an InteractiveBox (TRY IT or SEE IT), as the box's first child. Renders a `<p>` at 14px / var(--inkSoft) / line-height 1.55 / marginBottom 24. Every activity carries one where there's a real interaction cue; the text lives inside the box, not in prose above it. Use this instead of an inline `<p>` or the InteractiveBox `hint` prop for instruction text. Exceptions left without one: a few activities whose lead-in is genuinely just framing prose above the box (e.g., Welcome's opener TRY IT).
- **LessonHeader**: position eyebrow + serif title + optional subtitle. Eyebrow has split styling: "SECTION NN · GROUP · " in var(--inkMuted), "LESSON NN" in var(--primary).
- **SectionKicker**: page-level (size="large", 18px) or pre-content (size="small", 13px). Both purple, uppercase, weight 700. Also serves as the in-body section break within a lesson — what used to be LessonSubhead is now a SectionKicker call. Default behavior is no kicker.
- **ShowcaseBox**: framed callout for introducing or illustrating a concept, typically containing supporting cards. --primaryFaint fill, no border, borderRadius 20, padding 24. Props: kicker, headline, intro, marginBottom (default 24px), children.
- **KeyInsight**: structural takeaway callout. --info-bg fill (light blue), no border, borderRadius 14, 🔑 icon, inline layout. Props: lead (optional bold inline phrase), marginTop, marginBottom (default 24px each). Used for lesson-level zoom-out takeaways.
- **KeyTerm**: vocab introduction card. Slate band (--termBand) with 📖 icon and bold slate term (--termAccent). Props: term (required). Looks up the matching entry from the TERMS array, so vocab definitions in lessons cannot drift from the vocab quiz. Currently used in the No One Wrote the Rules lesson (norules) for "Guardrail."
- **InteractiveBox**: activity container. Variant "try" (✎) or "see" (◉). Surface "mint" (flat var(--tryBand), no border, 16px radius) or "sand" (var(--seeBand), no border, 24px radius, 32-36px padding). Sand surface renders the eyebrow in var(--seeAccent) amber. Default surface uses --primaryFaint with dashed border. Optional title/hint/action/children.
- **InnerCard**: standard white inner card used inside activities. White fill, 14px radius, --shadowSoft, default padding 22px 26px. Pass pad="snug" for the SEE IT stage size (18px 22px). Accepts a style prop for other overrides (display flex, marginBottom, custom padding) and children. Use instead of hand-building white cards inside InteractiveBox or RevealSequence.
- **ActivityCounter**: the "X of N" progress pill for an activity's InteractiveBox action slot. White pill, 999 radius, --shadowSoft, bold count plus uppercase "of N". Props: count, total. Convention: reveal-sequence activities pass the visible card position, count = Math.min(currentIdx + 1, total) gated by the start latch so it reads 0 before starting and never jumps when an answer is picked. Parallel activities pass the number answered. Use instead of hand-building counter pills.
- **PrimaryButton**: purple fill, white text, hover lift. Auto-adds trailing arrow. Used for the opener advance button. Lesson-to-lesson navigation uses the card-based NextLessonGate.
- **ActivityButton**: dark-ink fill, white text. Used inside activities for in-activity actions. Quieter than PrimaryButton. Sizes: default and "large". (RevealSequence currently hand-builds visually matching buttons rather than calling ActivityButton; a future cleanup may consolidate them.)
- **NextLessonGate**: bottom-of-lesson navigation gated on a `ready` boolean. Renders a card-based control: a PreviousCard plus a NextCardUnlocked when ready, or a NextCardLocked when not. NextCardLocked renders the `lockedMessage` string (default "Complete activities to continue"). All lessons fall back to the default; the `lockedMessage` prop is still available for one-off overrides but is no longer set per-lesson. Card navigation is the intended pattern for this course.
- **OpenerSection**: standardized opener-page wrapper. Slots: LessonHeader (with optional bigIdea subtitle), whyThisMatters paragraphs, optional featuredCard, "BIG QUESTIONS WE'LL ANSWER" SectionKicker, whatYoullLearnIntro, ShowcaseBox containing the lesson-question cards (either a flat grid via `openQuestions` or a clustered display via `groups` where each group has a kicker label, a bridge subhead, and its own card grid), whatYoullLearnClosing, optional KeyInsight (lead "The common mistake:"), framing KeyInsight (lead "Keep this question in mind:" rendered from each opener's `question` prop), PrimaryButton. Each section group's opener is a thin wrapper passing content props, so format changes propagate to every opener.
- **Illustration**: opener-support display band, used as the featuredCard in OpenerSection (8 openers). Tinted band (--illoBand fill, no border, 20px radius, 24px 28px padding) with an uppercase --illoAccent eyebrow (default "◆ ILLUSTRATION"), optional headline and intro, and a children slot. The children slot holds the large Instrument Serif display phrases (clamp ~28-40px); this is the documented exception to the serif rule.
- **QuizBlock**: recessed --bg fill, --rule border. Statement is sans 22px/600/--ink. Per-option correctness via opt.correct.
- **RevealSequence**: state-machine progressive-disclosure driver for SEE IT activities. Manages currentIdx, started, per-stage state. Drives Pattern A (one stage swaps in at a time) and the ladder-mode sub-variant (cumulative reveal). Accepts a surface prop matching InteractiveBox.
- **Takeaway**: standard activity-completion takeaway, replacing the old centered emoji cards. Two-column grid (1fr / 2fr, 36px gap): left is an uppercase 11px eyebrow (default "The takeaway") above a 24px/600 sans headline; right is the 16px sans explanation. Props: headline, body, eyebrow, accent, merged. accent defaults to var(--seeAccent) amber for SEE IT; TRY IT completions pass #2f7d4f green. Standalone mode renders a white card (14px radius, soft shadow, 24px 28px padding); merged mode renders just a dashed-accent top divider plus the grid, for dropping inside an existing content card where rows or a table sit above (Tokens, Inference, Choosing the Model).
- **CompareCard**: tinted comparison card chrome. No border, 16px radius, 20px padding, soft shadow (0 8px 22px rgba(14, 10, 31, 0.05)). Props: bg (required tint color), centered (optional), style (optional). Canonical inner-block treatment: any visible container inside a CompareCard is white with no border.
- **CompareBox**: the comparison-group frame, distinct from ShowcaseBox and dedicated to the "X vs Y" comparison family. var(--primaryFaint) fill, 22px radius, 32px 40px padding. Renders an optional kicker inside the frame (13.5px, 700, uppercase, 0.18em tracking, var(--primary), 18px margin-below) then a 1fr/1fr grid holding two ComparePanels. Props: kicker, marginBottom (default 32), gap (default 18), children. Reference implementation: DoesAIThinkSection.
- **ComparePanel**: one tinted column inside a CompareBox. Wraps CompareCard (panel tint, overridden to 18px radius and 22px padding) around a CompareHead plus a white InnerCard (12px radius, 18px 22px 20px padding, flex 1, keeps var(--shadowSoft)) that holds the body. The white body card is constant across every comparison box; the body inside it is a free slot formatted per content: bullets, code, a demo, an accent-colored monospace highlight line above dotted rows (the embeddings boxes), two labeled rows split by a hairline var(--rule) divider inside the one white card (Luke/Nate), or a centered hero such as a large emoji or number with the head left-aligned (the drink and cat boxes). Props: bg (panel tint), accent (head color), emoji (optional; omit to suppress on bodies that already carry an emoji, like the cat or drink boxes), eyebrow (optional; omit for an emoji-plus-title head like Luke/Nate), title, style (optional CompareCard override), children. For a body that genuinely should not sit on a white card, compose CompareCard plus CompareHead directly instead.
- **CompareHead**: the standardized panel header used by ComparePanel: optional emoji (15px, rides the eyebrow line) plus eyebrow (11px, 700, uppercase, 0.18em, accent color) plus title (24px, 700, -0.018em, line-height 1.15, accent color). Props: emoji, eyebrow, title, accent.
- Comparison family palette: blue panel #d6e2f4 with #2f4cb8 head, purple panel #ddd0ef with #5a3aa6 head. Comparison body text is 15px / 1.45 / var(--ink) with a 6px round var(--ink) dot at 0.45 opacity. ComparePanel keeps the 18/22 panel geometry as a convention, leaving CompareCard's 16/20 default untouched for its other uses. One sanctioned palette exception: Attention & Transformation in HowReads keeps its own coding (var(--primary) head on a #6e51ff22 panel, #f59e0b head on a #f59e0b22 panel), because the three-solutions explorer just below color-codes the same two concepts in those colors. It uses STEP 1 / STEP 2 eyebrows since it is a sequence, not an opposition.
- **ScenarioRow**: wraps Pattern 2 row chrome. Serif numeral, optional kicker, prompt text, indented pill row, feedback strip. Props: index (1-based), kicker, prompt, answered, correct, feedback, headline, eyebrow, children. headline and eyebrow override the feedback strip defaults (eyebrow defaults to "Correct" / "Not quite", headline to "Right." / "Not quite."); several sorts pass them per item.
- **FeedbackPill**: pill button for Pattern 2 sort activities. Driven by booleans `answered`, `isCorrect`, `isPicked` (plus `label`, `onClick`); a legacy precomputed `state` string is still accepted but no longer passed by any activity. Four looks: neutral white (unanswered or untouched), green fill for a correct pick, solid red for the current wrong pick, pale red for a remembered earlier wrong pick. Each pill latches its own memory via an internal everWrong flag: once it has been a wrong pick it stays marked pale red even after the student switches answers. Green only ever appears on a pill the student actually picked; the correct answer is never auto-revealed.
- **UserBubble / AIBubble / ThinkingBubble**: chat-style speech bubbles, the standard way to show a prompt and/or an AI response. Each carries a dot-plus-uppercase eyebrow in its fixed role color (UserBubble violet --primary, AIBubble green #2f7d4f) regardless of surface. UserBubble has a lavender #ECEAFB fill, AIBubble a green-tinted #eef4eb fill, both flat with no border or shadow and a tail that follows alignment. Props: text, optional label (overrides the eyebrow word, e.g. "You · Vague prompt"), optional align ("left"/"right"; a paired exchange puts You on the right and AI on the left, while a single standalone message goes left), and optional visibleChars / visibleWords for typing animations. ThinkingBubble (left-aligned, animated ellipsis).
- **ProgressBar**: 220px header right slot, "X of N lessons" where N = SECTIONS.length, gradient track --primary→#b08eff.
- **useReducedMotion**: hook reading prefers-reduced-motion via matchMedia, updates mid-session. Returns boolean. Gates JS-driven typewriter and reveal animations so they tick at 1ms when reduced motion is requested.

### TERMS array
Source of truth for vocabulary. Defined near the top of the file as a flat array of `{ term, definition, source }` entries. The KeyTerm component looks up definitions here, and the Vocab Quiz lesson uses the same array. The array currently holds 18 entries, but the quiz slices only the first 16 across two rounds of 8, so the last two entries (Transformation, Unstructured Data) are defined for KeyTerm lookups but not quizzed. Adding a new term in two places (the array and the quiz round count, if growing past 16) keeps lesson copy and quiz definitions aligned.

### Activity Patterns
TRY IT and SEE IT activities share a visual language and follow one of two interaction patterns each. Bespoke activities (text entry, redaction, builders, sliders) sit outside both patterns and stay one-off.

#### Shared visual language (TRY IT, both patterns)
- Container: InteractiveBox with `surface: "mint"`. Flat var(--tryBand) fill, no border, borderRadius 16, padding 26px 28px.
- Eyebrow: "✎ TRY IT" in Plus Jakarta Sans 700, 11px, letter-spacing 0.14em, uppercase, mint accent #2f7d4f.
- Title: Plus Jakarta Sans 700, 22px, --ink.
- Instruction line: the ActivityInstruction component as the box's first child, directly below the title (14px / var(--inkSoft) / line-height 1.55 / marginBottom 24). Applies to both TRY IT and SEE IT.
- Question numerals: Instrument Serif 400, 44px, line-height 1, color #2f7d4f. Opacity 0.6 when locked, 1.0 when active or answered.
- Question prompts: Plus Jakarta Sans 600, 18px, line-height 1.4, color #0e0a1f, max-width 56ch.
- Answer pills: Plus Jakarta Sans 600, 15px, padding 14px 18px, borderRadius 12, 1.5px border. Untouched: white fill, --rule border, --ink text; hover var(--tryBand) fill + var(--tryAccent) border. Pills key off whether they are the one currently being viewed (dim-in-place): exactly one pill is fully saturated at a time, the one whose feedback is showing. Correct pick viewing: #1f9d5f fill, white text, white ✓. Correct pick dimmed: #e7f6ee fill, #b6e3cd border, #1f9d5f text and ✓. Wrong pick viewing: #d4334a fill, white text, white ✕. Wrong pick dimmed: #fbe9ec fill, #f0b8c1 border, #d4334a text and ✕. transition all 150ms.
- Feedback (mint QuizBlock): a two-column block below a dashed divider (1px dashed rgba(63, 107, 63, 0.18), marginTop and paddingTop 18), mirroring the SEE IT Takeaway. Grid 1fr/2fr, gap 24. Left column is a colored dot plus an uppercase 11px eyebrow, then a 22px/700 headline, both in the accent color. Right column is the 16px/400 body in neutral ink #0e0a1f. Accent #1f9d5f for correct, #d4334a for wrong. All sans; the only serif in the activity is the numeral.
- Counter pill (top-right of activity): white fill, soft shadow, "N OF M" (bold count, uppercase letterspaced "of M").

#### TRY IT Pattern 1: Progressive Disclosure
Each scenario is its own moment with setup + question + per-question feedback. Use when sequential pacing builds the lesson.
- InteractiveBox variant "try", surface "mint", title and counter action.
- RevealSequence drives advancement: state for currentIdx, started, answer-per-scenario.
- Inside RevealSequence children: a single white card (#fff, borderRadius 14, boxShadow 0 4px 12px rgba(14, 10, 31, 0.05), padding 22px 26px) wrapping the scenario intro (THE EVENT eyebrow plus setup, plus any chat bubbles or essay text) and the QuizBlock together. The TRY IT eyebrow, title, and counter stay on the mint above the card.
- QuizBlock (mint) is retry-until-correct. Wrong picks lock as red and never advance, and the correct answer is never revealed. onAnswer fires only on the correct pick, so parent gating (canAdvance, counter) needs no per-activity change.
- After solving, every option stays clickable for exploration ("see why this one is wrong"). Clicking any option shows its feedback and makes it the single loud pill (dim-in-place); all other results dim to a pale tint.
- Two-phase wrong content: while unsolved, a wrong pick shows a withholding hint that must not name the answer (the `hint` field; default generic). After solving, clicking a wrong option shows its full `feedback`, since the answer is already out.
- Option data: { label, correct, feedback, headline?, eyebrow?, hint? }. feedback is the right-column body; headline defaults to "Right." or "Not the best fit."; eyebrow defaults to "Correct" or "Not quite"; hint is the during-attempt nudge.
- Completion element: the Takeaway component with accent #2f7d4f (green) so it matches the mint shell.

#### TRY IT Pattern 2: Parallel Sort/Match
All items visible at once, sorted independently. Best for sorting/categorization tasks. Per-item feedback reveals as each item is answered.
- InteractiveBox variant "try", surface "mint", title and counter action.
- All items render in vertical sequence with hairline dividers between rows: 1px solid var(--tryRule), padding 24 above/below per row, no divider above first row.
- Each row uses ScenarioRow: numeral on the left, content stack on the right, vertically centered.
- Pills indent to align under the prompt (paddingLeft equal to numeral width + gap, typically 66px).
- Per-item feedback reveals immediately after answer. Pills never lock: the student can re-pick freely. A correct pick fills green, a wrong pick fills solid red and stays remembered as pale red even after the student switches, and the correct answer is never auto-revealed (a pill turns green only when picked).
- NextLessonGate ready when `Object.keys(answers).length >= items.length`.

#### SEE IT Pattern A: Progressive Reveal, Sand Chrome
Stages reveal one at a time. Mirrors TRY IT Pattern 1 structurally; differs in color, shell, and the absence of QuizBlock.
- Shell: InteractiveBox with variant "see" and surface "sand". Sand band wrapper (var(--seeBand), no border, 24px radius, 32-36px padding). Eyebrow "◉ SEE IT" in var(--seeAccent) amber.
- Counter pill: identical to TRY IT visually.
- Engine: RevealSequence with surface "sand". It currently hand-builds its start/next/finish buttons (dark-ink fill, visually matching ActivityButton); a future cleanup may move these to the shared component.
- Stage interior: ivory inner card (white, 14px radius, soft shadow at 0 4px 12px rgba(14,10,31,0.05), 18-22px padding). Header row: serif amber numeral (Instrument Serif 32px, zero-padded "01" through "0N"), icon + Plus Jakarta Sans bold label (17px), Plus Jakarta Sans description (15px, color #3a3550). Subsequent sections separated by var(--seeRule) hairlines, each introduced by an amber 11px eyebrow with emoji prefix.
- Completion takeaway: the Takeaway component (default amber accent). Standalone when the completion is only the takeaway; merged (a dashed-divider footer inside the content card) when rows or a table precede it (Tokens, Inference, Choosing the Model).
- NextLessonGate: gates on full completion (activeIdx >= items.length).
- Ladder-mode sub-variant: stages stay visible cumulatively in one ivory card with var(--seeRule) hairlines between them. Most recent reveal animates in; earlier stages render statically. Used when stages build on each other (How LLMs Train, Three Steps to an Answer).
- No-completion-card variant: set isComplete: false on RevealSequence and gate canAdvance on `... && currentIdx < items.length - 1` so the activity ends on the last stage's content (Context "Same Prompt, Different Context").
- Pedagogical color preservation: SEE IT migrations recolor chrome to amber. They do NOT recolor interior content where color carries lesson meaning (Messy In's blue/red/purple Computer/Failure/AI palette, Context's role colors, Prediction's blue/purple/green steps).
- Decorative color order: for non-semantic card arrays (maps where color only distinguishes cards and carries no meaning), use the canonical palette in order, taking the first N: blue #3b82f6, green #10b981, amber #f59e0b, purple #8b5cf6. Colors that carry lesson meaning are exempt and follow the rule above.

#### SEE IT Pattern B: Parallel Reveal, Sand Chrome
Comparison matters more than sequence. All stages render at once as ivory cards stacked inside the sand band, separated by var(--seeRule) hairlines. No RevealSequence, no counter pill.

## Lesson structure

### End-of-lesson transitions
A lesson ends on its landing beat (Key Insight, Takeaway, or completed activity). It does not end on a forward-pointing paragraph. The NextLessonGate button is the structural pivot; a "...next lesson, we'll..." sentence dilutes the insight and adds reading load.

If a transition is genuinely needed for orientation, it goes at the top of the next lesson, not at the bottom of the current one. Each lesson reads as a standalone unit; the next lesson sets up its own question.

Practical rules:
- The last component before LessonRule should be a Key Insight, Takeaway, or activity-completion beat. Not a BodyP that pivots forward.
- Key Insight bodies should not trail off with "...next we'll..." or "...that's the idea behind X." Trim those sentences.
- Forward references inside mid-lesson copy are fine. The rule applies to the lesson's final beat.

## Working agreements

### David's setup
Designs prompts in chat with Claude (this Project). Pastes prompts into Claude Code in his VS Code terminal, where they get applied to the file. Verifies changes in his browser. Repo: AI-Training, single index.html file, deployed via Vercel.

### Course PDF export
A print-mode view is available via the URL parameter `?print=all`, with a "Print Course PDF" link beneath Reset Progress in the LLMExplorer footer. Renders every lesson in sequence with a page break between lessons, bypasses the name gate, and uses no-op nav callbacks. Component-level overrides expand activities into static, fully-answered form so the printable output is self-contained: ActivityCounter renders null, RevealSequence renders all children plus its completionElement and skips the start/next/finish buttons, and mint-surface QuizBlock renders the title row plus each option in answered state with full feedback below. Not yet expanded for non-mint QuizBlock surface, custom interactive widgets, or multi-scenario activities (those show only the first scenario in print mode). Full multi-scenario expansion would require per-lesson refactoring.

### Preferences
- Plain copy, McDonald's-humor friendly tone for the student audience (16-year-olds).
- Implementation-ready prompts referencing exact line numbers, existing patterns, and variable names.
- No file downloads, always copyable code blocks.
- David avoids em-dashes, and new course content avoids them too. The 7 existing uses in the file are the design-check.sh baseline; new copy stays at zero.

### Default mode
Collaborative content design. Propose options, ask for confirmation, then draft prompts. When David has clearly decided something, skip straight to the prompt. When something is ambiguous, ask before drafting.

### The pattern for content changes
1. Read the current state of the relevant section in index.html before suggesting copy or structure.
2. Propose options or ask clarifying questions if ambiguous.
3. Once aligned, draft the prompt as a code block.
4. After David runs it, ask what he saw in the browser and iterate if needed.

### When David returns with twin-testing feedback
Name the lesson, describe what felt off, read the relevant section in index.html before proposing options. Twin feedback might be a copy fix, an interaction fix, or a sign the lesson itself needs rethinking. Figure out which before drafting any prompt.

- Pre-ship governance: run `bash design-check.sh` from the repo root before shipping a new lesson. It flags hand-built counter pills, raw fonts, literal shadows, non-token mint dividers/surfaces, and em-dashes against known baselines. A deliberate diagram or assessment exception is fine; bump that check's expected count so the baseline stays honest.

### Assessment and diagram exceptions
Some late-course lessons intentionally step outside the standard component rhythm. These are exceptions, not patterns. Do not copy their chrome into ordinary lessons.

Known exception zones:
- Beat the Clock (headtohead): a timed assessment with custom game states (intro, playing, done), its own timer, score display, and stateful buttons.
- Late Build Your Advantage and Finish lessons: bespoke diagrams, flowcharts, score cards, and assessment panels where the visual itself carries the instructional meaning.
- RevealSequence start/next/finish buttons: hand-built rather than ActivityButton. Known, slated for a later cleanup.
- Custom shadows: active glows and a few elevated/inset shadows live inline on these surfaces. var(--shadowSoft) and var(--shadowElevated) remain the default everywhere else.

Boundaries when building an exception, so it still reads as part of the course:
- Use the course color tokens. Do not introduce a new raw palette.
- Use the standard type: var(--sans) and var(--serif). Do not add a new font.
- Reuse InnerCard, ActivityButton, and ActivityCounter wherever they fit.
- Include a standard or compact LessonHeader where feasible so the lesson stays in the course frame.

An exception is never a reason to skip tokens or standard type. If you deliberately add a new custom shadow or other flagged pattern, bump its expected count in design-check.sh so the pre-ship check stays meaningful.
