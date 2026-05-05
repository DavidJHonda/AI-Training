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
- TRY IT colors (inlined, no named vars): mint surface #eef4eb / #ecf6e6, green accent #2f7d4f, mint hairline rgba(63, 107, 63, 0.18)
- SEE IT colors (added during SEE IT Pattern A reference implementation): --seeBand #faf6ec (sand background for the SEE IT container band), --seeAccent #a36a17 (amber accent used for the SEE IT eyebrow, interior section eyebrows, and serif numerals), --seeRule rgba(163, 106, 23, 0.18) (amber hairline used as section divider inside the ivory cards). These three variables are the SEE IT counterparts to the TRY IT mint/green palette and live in the :root style block.
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
- InteractiveBox: variant "try" (✎) or "see" (◉), purple-dashed border, --primaryFaint fill, green eyebrow. Optional title/hint/action/children. New `surface` prop accepts "mint" (flat #eef4eb fill, no border, 16px radius) or "sand" (var(--seeBand) #faf6ec fill, no border, 24px radius, 32-36px padding). Sand surface renders the eyebrow in var(--seeAccent) amber. Default surface preserves the lavender + dashed treatment.
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

### SEE IT Pattern A: Progressive Reveal, Sand Chrome

Reference implementation: Verify "Verification Strategies" at L7131. Used for SEE IT activities where stages reveal one at a time and the student walks through them in sequence. Mirrors TRY IT Pattern 1 structurally; differs only in color, shell, and the absence of QuizBlock.

Shell: InteractiveBox with variant: "see" and surface: "sand". The sand surface variant produces a sand-band wrapper (var(--seeBand) #faf6ec, no border, 24px border-radius, 32-36px padding). The SEE IT eyebrow ("◉ SEE IT") renders in var(--seeAccent) amber.

Header: title in var(--ink), counter pill in the action prop (white pill, 999px radius, dark ink count + uppercase amber-leaning meta, identical to TRY IT counter visually).

Engine: RevealSequence with surface: "sand". The sand surface case shares the canonical dark ink (#0e0a1f) Plus Jakarta Sans buttons with TRY IT's mint surface, and uses var(--seeRule) for any hairline dividers.

Stage interior: ivory inner card (white background, 14px radius, soft shadow at 0 4px 12px rgba(14,10,31,0.05), 18-22px padding). Inside the ivory card:
- Header row: serif amber numeral (Instrument Serif 32px, var(--seeAccent), zero-padded "01" through "0N") on the left, then a stack of icon + Plus Jakarta Sans bold label (17px) and Source Serif 4 description (15px, color #3a3550) on the right.
- Subsequent sections separated by var(--seeRule) hairlines, each introduced by a Plus Jakarta Sans 11px amber eyebrow with 0.14em tracking and an emoji prefix, followed by Source Serif 4 body or AIBubble content.

Completion card: same pattern as canonical TRY IT (centered, emoji + Plus Jakarta Sans bold heading + Source Serif 4 body, no border or fill, 60ch max-width body).

NextLessonGate convention: gates on activeIdx >= items.length (full completion), matching TRY IT behavior. Earlier SEE ITs gated on "any progress unlocks" which we deprecated during the Pattern A reference work.

Numeral size note: SEE IT numerals are 32px, matching TRY IT, not the 44px showpiece size suggested by Claude Design's external spec. Smaller numerals keep SEE IT and TRY IT visually parallel and prevent the SEE IT chrome from competing with surrounding lesson copy.

Pattern A "ladder-mode" sub-variant. Used when stages build on each other and the student should see the whole pipeline emerge cumulatively (How LLMs Train, Three Steps to an Answer). Same shell, eyebrow, counter pill, and RevealSequence engine as standard Pattern A, but the ivory card contains all revealed stages stacked rather than swapping in one stage at a time. Each stage row is separated by var(--seeRule) hairlines (no individual borders or backgrounds per stage). The most recently revealed row gets a fadeIn animation; earlier rows render statically. The completion element typically renders the full stage ladder one more time without animation, optionally followed by a summary block (metadata pills, takeaway prose). When the ladder uses pedagogical color signals (per-stage colors that carry meaning), the serif numerals and stage labels render in the stage's brand color rather than amber, while the SEE IT chrome (eyebrow, hairlines, buttons, counter pill) stays amber.

Pedagogical color preservation rule. SEE IT Pattern A migrations recolor chrome (eyebrow, numerals, buttons, eyebrow, hairlines, completion typography) to amber/sand. They do NOT recolor interior content where the color carries lesson meaning. Examples from migrated activities: Messy In keeps the blue (Regular Software) / red (failure) / purple (AI inferring structure) palette intact because that color trio IS the lesson. Context preserves the system/user/assistant role colors (amber/purple/green) for the same reason. The general rule: if removing the color would damage the pedagogy, keep the color. If the color is just default product chrome, recolor to amber.

No-completion-card variant. Some Pattern A activities end naturally on the final stage without a completion card (Context "Same Prompt, Different Context"). To suppress the completion card and the finish button: set isComplete: false on RevealSequence (use `&& false` to make it explicitly hard false), and gate canAdvance on `... && currentIdx < items.length - 1` so the Next button doesn't render on the last stage. The student sees the final stage's content and reads the surrounding lesson copy as the natural endpoint.

### SEE IT Pattern B: Parallel Reveal, Sand Chrome

Used for SEE IT activities where comparison matters more than sequence and all stages render at once. Same sand band shell as Pattern A. Drops RevealSequence and the counter pill. All stages rendered as ivory cards stacked inside the sand band, separated by var(--seeRule) hairlines. Spec to be finalized when the first Pattern B candidate is migrated. Likely candidates from the SEE IT inventory: Generative "Stored Answers vs Built From Probability" (L2550), Customization "Same Prompt, Different Setup" (L6228), Prompting "Format Changes Everything" (L7637), AIHistory "Two Coins, Three Outcomes".

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
- Wave 5 (complete): Pattern 1 interior migration across all six Bucket C activities. WhyDeeper "What's the AI Missing?" (chrome only, typing animation preserved via UserBubble/AIBubble visibleChars/visibleWords props). ModelSelection "Pick the Right Tool" (per-option feedback written for 8 wrong-answer paths; lesson copy fixed from "five real scenarios" to "four"). Prompting "Fix the Prompt" (per-option feedback for 9 wrong-answer paths; two-phase reveal preserved with improved-prompt block rendered below QuizBlock once answered, separated by hairline divider; exerciseRevealed state retired). AIFuture "Classify the Claim" (per-bucket feedback for 10 wrong paths; bucket emojis preserved in option labels; "The goal is not cynicism" callout folded into completion element; claimsDone state replaced with startedClaims). CriticalThinking pair restructured from reveal-only to actual quizzes: "Spot the Problem" (5 items × 3 options × per-option feedback) and "The 5 Habits" (5 habits × 3 options × per-option feedback, scenario.question reused as QuizBlock statement, UserBubble + AIBubble setup preserved). show101 and showAnalysis state removed; problemAnswer and habitAnswer added. Canonical bucket grew from 9 to 15 of 50 activities.
- SEE IT Pattern A reference (complete): Established the SEE IT spec by adding sand-band CSS variables (--seeBand, --seeAccent, --seeRule), adding a "sand" surface variant to InteractiveBox and RevealSequence (the latter shares the dark ink button color with mint, so canonical buttons unify across TRY IT and SEE IT), and migrating Verify "Verification Strategies" as the reference implementation. Pattern A uses RevealSequence with stage cards built from a serif amber numeral + icon/label/desc header followed by amber-eyebrow sections separated by hairline dividers, all inside an ivory card inside the sand band. NextLessonGate convention updated to require full completion. The migration also recolored the lesson's "The question: Is this true?" header from primary purple to amber for visual continuity above the sand band. SEE IT Pattern A migration of remaining progressive SEE ITs deferred until after twin testing; the reference itself was tactical to lock in the spec.
- SEE IT Pattern A migration (Wave SEE-1 + SEE-2 complete): Seven additional Pattern A activities migrated, bringing the canonical SEE IT bucket from 1 (Verify reference only) to 8 of 19 in-scope SEE ITs. Wave SEE-1 covered the two Evaluating activities ("The 6 Criteria" and "Prompt → Evaluate → Refine") which already used RevealSequence with clean stage data and were chrome-only migrations. The "Is this actually good enough to use?" lesson header recolored from primary purple to amber for visual continuity above the sand bands. NextLessonGate convention re-applied: gates on full completion of the final activity in the lesson. Wave SEE-2 covered five activities with bespoke per-stage interiors: Data "Messy In, Structured Out" (preserved blue/red/purple Regular Software vs AI palette as pedagogical signal, replaced ad-hoc scenario state with RevealSequence wiring, removed dataComplete state in favor of derived boolean, folded "What this unlocks" callout into completion element); Training "How LLMs Train" (established SEE IT Pattern A "ladder-mode" sub-variant for cumulative reveal where each stage stays visible as new ones appear, all inside one ivory card with hairline dividers between stages, four metadata pills folded into completion); Context "Same Prompt, Different Context, Different Answer" (preserved typing animation across phase 0/1/1.5/2/3 states verbatim through unchanged useEffect, role-colored context message rows kept since system/user/assistant colors carry semantic meaning, set isComplete to hard false since this activity has no completion card and ends naturally on scenario 3 with the explanation visible).

## Open / pending

- Mobile responsive pass not validated
- 7 quizzes intentionally bespoke, not converted to QuizBlock (Test Yourself, Probability, Integrity, AI Strengths, HeadToHead, Key Terms, Training sorting)
- The twins haven't tested the app yet — recommendation is to ship and watch real students use it
- Two leftover items identified during audit, intentionally not cleaned up: dead "capstone" entry in CHIP_LABELS, orphan "llm-precheck-score" localStorage write that nothing reads back
- SEE IT Pattern A spec is settled with eight activities migrated (Verify "Verification Strategies" reference, plus seven Wave SEE-1 + SEE-2 conversions). Pattern A now has three documented sub-variants: standard (one stage swaps in at a time, used by Verify, 6 Criteria, Prompt-Evaluate-Refine, Messy In, Same Prompt Different Context); ladder-mode (cumulative reveal with hairline-separated stages in one ivory card, used by How LLMs Train); and no-completion-card (used by Same Prompt Different Context where the activity ends naturally on the last stage). Wave SEE-3 will establish the SEE IT Pattern B reference; the natural candidate is Generative "Stored Answers vs Built From Probability" since it is a clean two-card comparison with no animation or scenarios. Other Pattern B candidates: Customization "Same Prompt, Different Setup", Prompting "Format Changes Everything", AIHistory "Two Coins, Three Outcomes". Bucket SEE-D bespoke chrome-only migrations (sand band + amber accent only, interior intact) are queued for a later wave and now include nine activities: AIHistory "ChatGPT, decoded", AIHistory "Bayes' Theorem in Action", HowAIReads "Who Does 'IT' Refer To?", Probability "How the model picks a word", Training "Watch It Happen", Token "Tokenize It", Prediction "Meaning Map", Layers "Watch Meaning Build Layer by Layer" (reclassified mid-wave), and ThoughtPartner "Thinking Together". Pattern B reference and SEE-D bulk are both deferred until after twin user testing. Future waves to extract TipCard, StageCard, and HighlightBox once enough usages are catalogued. Decision pending whether to demote casual 💡 lightbulb tips to plain bold body paragraphs (current lean) or formalize as a separate small Tip pattern. Smaller standardization passes still pending: h3 spacing, info-callout format consistency, two-column compare blocks. Wave 6 (Bucket D Pattern 2 interior migration for HumanEdge and WorkChanges) and bespoke-chrome normalization across the 13 legitimately bespoke TRY IT activities both deferred until after twin user testing. Twin testing remains the next priority.

## How to ask for help in this Project

Good first messages for new chats:
- "Look at the [lesson name] page. [What feels off]. WDYT?"
- "I want to change [specific thing] on [lesson]. Here's my draft: [draft]"
- "Audit the [section group] for [specific concern]"
- "Continue from where we left off — last session I [decision]"

Always ask Claude to read the current state of the relevant section in index.html before suggesting changes.

When David returns with notes from the twins testing the app, the right pattern is: name the lesson, describe what felt off, then read the relevant section in index.html before proposing options. Twin feedback might be a copy fix, an interaction fix, or a sign that the lesson itself needs rethinking; figure out which before drafting any prompt.

For twin testing notes specifically: the right pattern is to name the lesson, describe what felt off, and let David and Claude figure out together whether it is a copy fix, an interaction fix, or a sign that the lesson itself needs rethinking. Visual chrome inconsistencies are now mostly resolved across TRY IT (Patterns 1 and 2 plus normalized button colors) and SEE IT Pattern A; if twins flag visual issues, those are most likely in the still-unmigrated Pattern B comparison activities, the Bucket SEE-D bespoke activities, or the bespoke TRY IT activities (Bucket E) where chrome varies. Naming the lesson and describing the friction is enough; do not pre-diagnose.