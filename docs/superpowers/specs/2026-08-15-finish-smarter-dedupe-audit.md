# Finish Smarter merge — dedupe audit

**Date:** 2026-08-15 · Task 1 of `docs/superpowers/plans/2026-08-15-finish-smarter-merge-phase1-2.md`

**Method:** read all five components in full from `index.html` (`ThoughtPartnerSection` 8118–8200
incl. its exclusive helper `ThinkingTogetherStatic`; `WhenAIJudgesSection` 10530–10695;
`WhatYouLearnedSection` 10851–10959; `HumanEdgeSection` 11164–11393; `BuildEdgeSection`
12337–12608), then grepped the whole file for every candidate overlap and read the competing
lesson enough to quote it verbatim. Checked `docs/parking-lot.html` for existing entries; none
cover these five lessons' content directly (closest are the "Who Else Is Affected" and "Ask AI"
entries, cited below where relevant).

Every unit below is in exactly one bucket (CUT / SURVIVOR / park). Where a unit's overlap is real
but partial, it's marked SURVIVOR with the overlap noted, so David can decide rather than have it
silently dropped.

---

## humanedge — Skills That Matter

### Taught elsewhere (CUT list)

- **COMPARE box, left column ("What AI does fast")** — "First drafts of almost anything /
  Summaries of long text / Generating ten options / Reformatting and rewriting / Routine code and
  boilerplate / Surface-level explanations" duplicates `whatitdoesbest` ("Where AI Works Best")'s
  four-strengths framework almost item for item: "AI is strongest when the job has one of four
  shapes" → Patterned transformation ("recast it into something clearer, cleaner, or better
  structured"), Generative variation ("give you several versions at once"), Semantic compression
  and retrieval ("shrink long documents down to the core"), Structured reasoning and synthesis
  ("work through them toward an answer"). `whatitdoesbest` is the dedicated lesson for this claim
  and `buildedge` already cites it by name ("You already have this one. **Where AI Works Best**
  showed you the work it's genuinely good at").
- **COMPARE box, right column ("What still depends on you")** — "Knowing what question to ask /
  Deciding whether the answer is good / Catching weak reasoning / Verifying what matters / Choosing
  what's actually important / Owning the final call" is a compressed restatement of this same
  lesson's own SKILLS cards (see below), which are separately flagged CUT against their true
  external sources. Redundant with content already covered once this lesson is rebuilt.
- **"The question to ask yourself first" section** — "Some prompts are low-stakes. Background
  music, a quick title, a summary you'll forget in an hour. Let AI handle it. Some aren't. What to
  write your college essay about. Whether to submit something as your own work. How to handle a
  hard conversation." duplicates `evaluating` ("Evaluate the Results")'s stakes question: "**How
  much is riding on it?** Picking a movie for tonight: you're done. A college essay, a health
  question, anything with your name on it: keep going."
- **SKILLS card "Ask better questions"** — "AI output is bounded by the prompt. Vague in, vague
  out. Knowing what you want, why, and in what form is itself a skill, and one most people are bad
  at." duplicates `questionsvaluable` ("Questions Matter")'s core thesis: "the less time we spend
  chasing the answer, the more time we have for the half that's still 100% ours: **asking the right
  question**" and its `WhereValueLivesBox`: "AI only answered the question it was given. When
  anyone can get a fast answer, the edge shifts to the person who can ask the better question." Also
  covered by `prompting` ("Art of Prompting"): "the quality of your prompt directly controls the
  quality of the response."
- **SKILLS card "Judge output quality"** — "AI sounds fluent every time. The harder skill is
  recognizing when fluent isn't the same as right, useful, or honest." duplicates `evaluating`'s
  opening: "AI makes mistakes. It uses the same confident voice whether the facts are right or
  wrong... what do you do with an AI answer, knowing it might be wrong?" and its whole Read/
  Understand/Validate + dig-deeper apparatus.
- **SKILLS card "Spot weak reasoning"** — "AI often skips steps, assumes the conclusion, or sounds
  confident about a shaky claim. Noticing that is on you, not the model." duplicates `critical`
  ("Critical Thinking")'s entire CT_101 apparatus (five worked reasoning-trap scenarios:
  correlation/causation, missing-context statistics, trace-to-source, reverse causation, small
  sample size) and its framing: "actively analyzing, questioning, and evaluating information...
  before deciding what to believe or do."
- **SKILLS card "Verify what matters"** — "AI generates what sounds true, not what is true. The
  better it sounds, the more important it becomes to check the things that actually matter."
  duplicates `evaluating`'s "dig deeper" tactics (Ask for citations / Challenge the AI / Ask what's
  missing / Ask for a live web search / Leave the chat) and its "does this answer deserve the dig?"
  framework.
- **SKILLS card "Apply real domain knowledge"** — "AI knows a little about everything. People who
  know one thing deeply can catch mistakes, push back, and steer AI toward genuinely better
  answers." duplicates `buildedge`'s own "Deep knowledge in any field" category (this audit, same
  batch): "AI sounds knowledgeable about almost anything. People with real depth catch when it's
  shallow, wrong, or missing the point, and use AI as a power tool because of it. Everyone else gets
  answers they can't verify." `buildedge`'s version is the fuller, categorized treatment (one of its
  Five Places Depth Still Pays) and is explicitly load-bearing there; this one-line card is the
  redundant copy.
- **SKILLS card "Know when not to trust it"** — "The most valuable instinct is the one that says,
  'this sounds confident, but I shouldn't act on it yet.' Calibration beats blind trust." duplicates
  `hallucination`'s core teaching: "Sometimes AI gives you a false claim delivered in the same
  confident voice it uses for real facts. That confident-but-wrong claim is called a
  **hallucination**" and its illustration's closing line, "AI can be confidently wrong. Check
  sources."

### Survivors (KEEP list)

**HUMANEDGE_SURVIVORS** (destination: rebuilt **Skills That Matter** roundup lesson, per spec):

- **Opening thesis (2 paragraphs)** — "AI can produce a first draft of almost anything in seconds.
  That changes what makes a person valuable... The bottleneck moves from production to direction."
  + "You've been building these moves all course. The human edge is knowing which one to bring in
  at which moment." Appears nowhere else verbatim; frames the whole rebuilt lesson. (Note: thematic
  cousin of `buildedge`'s "AI raised the floor... squeezed the middle" thesis — see judgment calls
  below; not a literal duplicate, both lessons build to different downstream destinations.)
- **SKILLS card "Break down messy problems"** — "Real problems don't arrive as clean prompts.
  Splitting a tangled question into pieces AI can actually help with is the work AI won't do for
  you." No lesson teaches this exact claim (parsing an ambiguous real-world problem before you even
  reach a prompt). Related but distinct from `prompting`'s Move 3 ("Big work goes in steps. One
  prompt, one job, so each part lands and you can check it before you build on it."), which is about
  sequencing a *known* task into ordered prompts, not identifying what's askable in a *messy* one.
  Flagged for David's judgment — partial overlap.
- **SKILLS card "Taste, judgment, prioritization"** — "AI can hand you ten options. Picking the
  right one, and knowing why, is what separates good work from average work." No other lesson
  teaches taste/prioritization as a named skill.
- **EDGE_CARDS, "Four moves AI can't own"** (all four, as a set) — "Frame the real problem" / "Make
  sense of weird behavior" / "Check what matters" / "Make the human call," each with its one-line
  body. Appears nowhere else, and is **load-bearing**: `buildedge` cites these four by name verbatim
  ("**Skills That Matter** gave you four moves: frame the real problem, make sense of weird
  behavior, check what matters, make the human call."). Must survive under these exact names or
  `buildedge`'s citation (and its future home in Make Your Move) needs a matching edit.
- **MISSING_SCENARIOS TRY IT ("Which Move Was Missing?")** — four scenarios (vague-study-tips /
  ChatGPT arithmetic error / CS-vs-English major / Luka Dončić hallucination on Snapchat's My AI)
  testing the EDGE_CARDS categories. Bound to EDGE_CARDS; survives with it. Not a duplicate of the
  $60-hoodie-20%-off arithmetic scenario in `whybother` (different point: `whybother` shows you
  already know enough to catch AI; this teaches *why* AI gets arithmetic wrong at all — "it predicts
  the result instead of calculating it," a claim that appears nowhere else in the course).
- **SCENARIOS TRY IT ("Spot the Stronger Use of AI")** — four scenarios (essay on a novel not fully
  read / gap-year decision / fixing code you don't understand / poster design). Distinct surface
  scenarios from `thoughtpartner`'s TP_MOVES and `mindtrap`'s SPOT_EXERCISES (different specific
  situations); no verbatim overlap.
- **Closing thesis** — "AI makes production cheaper... The skills above don't replace AI. They're
  what makes AI worth using." Bound to whichever SKILLS cards survive.

### Verbatim copy worth parking regardless

- Close board pill pair: **"Some skills stay yours."** / **"That's where your value compounds."**
  (`CLOSE_BOARDS.humanedge`). Park for reuse if Skills That Matter's rebuild wants a different pair.
- The full COMPARE box and the four CUT SKILLS cards themselves, verbatim, in case the rebuilt
  lesson wants a single line of any of them even though the lesson-level duplicate is being cut.

---

## buildedge — Your Edge

### Taught elsewhere (CUT list)

None found as clean external duplicates — this lesson is almost entirely original synthesis. Two
things worth flagging instead of cutting:

- **"Deep knowledge in any field" category** duplicates `humanedge`'s "Apply real domain knowledge"
  card (see humanedge's CUT list above). Resolution recommended there: `buildedge`'s version wins
  (richer, part of the load-bearing Five Places framework); `humanedge`'s card is the one cut.
- **Opening thesis** ("AI raised the floor... That squeezes the middle...") is a thematic cousin of
  `humanedge`'s opening thesis (both argue production got cheap, judgment got valuable). Not a
  literal duplicate — `buildedge` explicitly builds on top of it ("Catching that is the human
  skillset this course has spent whole sections on... AI didn't make those skills less valuable.")
  — but the two lessons overlap in spirit. Since they're headed to different downstream lessons
  (Skills That Matter vs. Make Your Move per spec), keep both; flagged for awareness only.

### Survivors (KEEP list)

**BUILDEDGE_SURVIVORS** (destination: future **Make Your Move**, per spec — "the concrete
directives: make things, not just prompts; get good at something; whatever else survives the
dedupe"):

- **Opening thesis (4 paragraphs + bold line)** — floor/ceiling/squeezed-middle framing, "This is
  the move the whole course has been pointing at. Now we name it." Unique.
- **THE EXPERT PARADOX / LAYERS box** — "The floor" / "The middle" / "The edge" three-tier framing.
  Unique, no duplicate found.
- **Illustration** (`illustrations/your-edge.jpg`) and its two following paragraphs (the
  "wait-until-you're-an-expert" trap; AI-related roles built on depth; "So is every other job worth
  doing"). Unique.
- **"1. What do I use AI for?"** — cites `whatitdoesbest` and `thoughtpartner` by name (intentional
  cross-reference, not a duplicate to cut). **Flag:** once `thoughtpartner` dissolves into AI Tips
  (Task 3), the line "And don't forget the second mode, from **Thought Partner**: AI as sparring
  partner..." will cite a page that no longer exists under that name — needs a rewrite when this
  survivor moves to Make Your Move, not before.
- **"2. What do I never hand off?"** — cites the EDGE_CARDS four moves by name (safe citation; see
  humanedge's Survivors note — those names are staying put in rebuilt Skills That Matter, so this
  reference doesn't go stale).
- **"3. What do I get good at?"** intro paragraph, the **CATEGORIES box** ("Five Places Depth Still
  Pays": Communication, Judgment, Hands-on action, Human systems, Deep knowledge in any field, each
  with its full body copy), the two follow-up paragraphs ("Depth isn't the same as prestige..." /
  "Here's how AI fits while you're building..."), **"Pick one, not five"** kicker + 3 paragraphs, and
  the **HOW TO BUILD DEPTH box** (5 moves: Pick one real interest / **"Make things, not just
  prompts"** / Learn to catch the mistakes / Get feedback from people / Keep proof of work). This is
  the seed example named in the plan: "**'Make things, not just prompts' is untaught → SURVIVOR
  (destination: Make Your Move)**." Confirmed untaught elsewhere. Note: "Get feedback from people"'s
  justification line ("AI agrees with you too easily") echoes `flattery`'s sycophancy thesis, but
  the *directive itself* (seek human feedback while building depth) is not taught there — keep as
  is.
- **Two closing paragraphs** after HOW TO BUILD DEPTH ("Your edge isn't avoiding AI..." / "Those
  five categories aren't the only depth that pays..."). Unique.
- **"4. How do I check my work?"** — cites "**Verify** and **Evaluate** gave you the two checks that
  matter." **Flag — pre-existing stale reference, not caused by this merge:** there is no standalone
  "Verify" lesson in the current course (`SECTION_META`/`SECTION_COMPONENTS` have no `verify` id;
  only `evaluating`, "Evaluate the Results," exists). This citation predates this audit and should
  be corrected to a single lesson name when this survivor lands in Make Your Move.
- **"5. Why pick me over AI?"** — 2 paragraphs, unique ("if AI can produce the average version of
  your work for free, then 'I can do the average version too' is not an answer. It's the reason to
  pick AI instead.").
- **Closing kicker + paragraph** — "Anyone can sound smart now. Get good at something anyway." /
  "Five calls, one move underneath them... Average is free now. Be the reason someone picks you over
  it."
- **SCENARIOS TRY IT ("Spot the Gap")** — five scenarios (grandma's birthday speech / CEO
  genius-or-fraud / bike chain / distant friend's text / team-loss stats explanation) testing the
  five CATEGORIES. Bound to the CATEGORIES box; survives with it. Distinct scenarios from
  `humanedge`'s two TRY ITs and `thoughtpartner`'s TP_MOVES — no verbatim overlap.

### Verbatim copy worth parking regardless

- Close board pill pair: **"Your move now."** / **"The tool is ready. Are you?"** (`CLOSE_BOARDS.
  buildedge`). Per spec, this should survive "on Make Your Move or the section's final board" —
  park verbatim so whichever lesson claims it can pull it directly.

---

## thoughtpartner — Thought Partner

Per the plan, this lesson doesn't get a CUT/SURVIVOR split against the rest of the course — it
dissolves wholesale into the future **AI Tips** lesson ("Thought Partner folded in"). This is
therefore an inventory of every tip-shaped unit, not a dedupe gate. No literal verbatim duplicate of
this lesson's content was found elsewhere in the course (its closest cousins — `mindtrap`'s
"pressure-test your thinking, then take the decision to people" and the general "pressure-test"
vocabulary used in a few other lessons — teach a related but different point: who should *decide*,
not how to *prompt* a thought partner. Noted, not cut.)

### Taught elsewhere (CUT list)

None. (See note above — the whole lesson is an inventory, not a gate.)

### Survivors (KEEP list)

**THOUGHTPARTNER_INVENTORY** (destination: future **AI Tips**, per spec):

- **Opening thesis (2 paragraphs)** — "A good prompt gets you an answer in one shot. Thought
  partnership is for the messier work..." + "AI can help you explore ideas, pressure-test your
  thinking, and get unstuck. But the thinking still has to be yours... you drive the conversation and
  you make the decisions." Framing paragraph for whatever AI Tips does with this material.
- **"Five thought-partner prompts to copy"** (tip-shaped, the strongest unit for AI Tips'
  copy-this-tip format):
  - "Ask me five questions before giving advice."
  - "Challenge my assumption."
  - "Give me three possible explanations."
  - "What would a skeptical reader say?"
  - "Where might I be fooling myself?"
- **TP_MOVES TRY IT ("Keep the Thinking Yours")** — three scenarios (AI rewrites a weak history
  essay outright / AI agrees your AP-Stats-vs-CS lean makes sense / AI ranked ten fundraiser ideas
  and you like #3), each pairing a "keeps the thinking yours" move against a "hands over the
  thinking" move. Demonstrates the five prompts above in use; carry as a unit if AI Tips wants a
  practice activity.
- **Closing line** — "Different problems take different moves. The pattern is the same: you stay in
  the work, AI helps you see what you're not seeing."

### Verbatim copy worth parking regardless

- **ThinkingTogetherStatic + TP_EXCHANGES** (its exclusive helper, used nowhere else) — the full
  6-exchange "summer plans" worked conversation (vague goal → narrowed → direction picked → obstacle
  named → pushback on a bad plan → turned into action) plus its closing Takeaway, "AI explored. You
  decided. It opened up the options, pushed back on a weak plan, and poked at the obstacles, but
  every choice stayed yours. A good thought partner widens your thinking without taking it over."
  Too long-form to be "tip-shaped," but it's the lesson's best single demonstration of thought
  partnership in action — park it in case AI Tips (or any future lesson) wants a worked example
  rather than a list of copyable lines.
- Close board pill pair: **"Think with it, not for you."** / **"It's a partner, not the author."**
  (`CLOSE_BOARDS.thoughtpartner`).

---

## aijudges — When AI Judges You

Per the plan, this lesson compresses into the merged Habits for the Road lesson: detector material
into the integrity half, screening-systems material into the privacy half, everything else parked.
**Important finding:** the detector bucket substantially overlaps content `integrity` already
teaches today (quoted below) — Task 4 should treat that bucket as "confirm/extend," not "add
wholesale."

### AIJUDGES_CORE

**(a) Detector material → destination: integrity half**

- **TRY IT Scenario 1** (English teacher, AI-detector 73% score, essay you actually wrote yourself)
  — full scenario + three options + feedback, correct answer "Bring your process: outline, drafts,
  version history, sources. Ask which detector was used, what the score actually means in the
  teacher's policy, and what the appeal path is." (headline "Bring the receipts.")
  **Taught elsewhere — near-duplicate:** `integrity`'s existing "SHOW YOUR PROCESS" box already
  covers most of this ground: "Some schools run student work through AI detectors... They produce
  both false positives (honest work flagged as AI) and false negatives (real AI use missed). A
  detector score isn't proof by itself..." / "Build a defense the detector can't take from you: a
  visible record of how the work actually came together" (Drafts as you go / Sources with links and
  dates / AI conversation logs) / closing line "**The best defense isn't hoping the detector
  believes you.** It's having the receipts." The genuinely incremental piece aijudges adds is
  narrower than the whole scenario: (1) naming the five-questions framework explicitly as the tool
  being run, and (2) the in-the-moment meeting script (bring receipts to a real accusation
  conversation, ask which detector + what the score means in *this teacher's* policy + the appeal
  path *before* the meeting) — `integrity` today is about building the trail proactively, not about
  what to do once you're already sitting across from a teacher. Recommend Task 4 add only that
  incremental angle rather than restate the scenario in full.
- Related supporting language: the Mode 3 card's "plagiarism scores" mention (see screening bucket
  below) touches detectors too but is bundled with hiring/credit/fraud scores generally — left in
  the screening bucket since it's not detector-specific.

**(b) Screening-systems material → destination: privacy half**

- **Opening framing (3 paragraphs)** — "This whole course has been about you using AI well. But
  there's a side of AI you don't open and don't control. AI is also being used on you..." / "Maybe a
  system already decided which posts you saw on TikTok this morning..." / "Sometimes you're the user
  of AI. Sometimes you're the subject of AI." No overlap found — `privacy` today is entirely about
  what *you* type/upload into AI tools, never about third-party systems scoring or ranking you using
  data gathered elsewhere. This is new territory for Privacy, not a duplicate.
- **THREE MODES box** — "What you see" (ranking algorithms) / "What you can do" (filters and flags)
  / "What gets attached to your name" (scores and classifications, incl. "plagiarism scores").
- **FOUR ROLES box** — User / Subject / Operator / Bystander, each with its body copy. (Note: this
  box itself was moved here from the retired `StakeholdersSection` per the existing parking-lot
  entry "Who Else Is Affected" — dated 2026-06-10 — so it already has one migration behind it.)
- **FIVE QUESTIONS box** — "Who is responsible? / What data was used? / Can you push back? / What
  happens if it's wrong? / Who is this helping, and who is it hurting?" plus the "notice the first
  question is who, not what" paragraph. This is the single most reusable artifact in the lesson.
- **"Ask for the paper trail" callout** — the five in-writing questions (What policy applies here? /
  What data, document, score, or evidence was used? / Was there human review? / How do I correct a
  mistake? / What is the appeal path?) and "A school or company that won't put any of this in
  writing is telling you something."
- **"Every system optimizes for something"** section.
- **"When mostly right isn't right enough"** section (accuracy-at-scale, false positive/negative
  framing).
- **"When fair-on-paper isn't fair"** section + proxy-variables paragraphs.
- **Closing lines** — "When AI judges you, don't argue with the machine." / "Find the human, ask
  what data was used, and learn how to appeal."
- **TRY IT Scenarios 2–5** — college AI-assisted admissions review; TikTok political-content feed;
  Discord auto-removed comment with no appeal path; internship application AI screen. All four are
  "systems using data about you to decide something" scenarios with no equivalent elsewhere in the
  course.

**(c) Everything else → park**

- Illustration (`illustrations/when-ai-judges-you.jpg`) and its alt text (masked AI judge with a
  gavel, scoring housing/jobs/school admissions on zip code, grades, attendance, credit score). New
  art will be needed for whichever half absorbs this material; park the alt text as a starting
  reference.
- TRY IT framing copy ("What's Your Move?" title/lead) and its closing Takeaway: "Five questions.
  Every system. Every time. You won't always get clear answers. The questions still work. A system
  that won't tell you who's responsible is telling you something."
- The lesson's own kicker/label ("DECISIONS ABOUT YOU" / "When AI Judges You") — retires with the
  page.

**No close board to migrate:** `closeBoard("aijudges")` is called in the component but
`CLOSE_BOARDS` has no `aijudges` entry, so this call currently renders nothing. This lesson has
never had a close board — nothing to park on that front.

---

## whatyoulearned — What You Learned

Per the plan, this lesson survives as-is content-wise until the follow-up Final plan (Beat 4).
This is an inventory of what its recap currently covers, plus stale-claim flags for this plan's
resequence.

### Taught elsewhere (CUT list)

Not applicable — this lesson is an intentional recap of prior material by design; its whole job is
restating things taught elsewhere. Nothing to cut.

### Survivors (KEEP list)

Whole lesson survives untouched by this plan (Task 3–5 only re-chain its gates). Inventory of what
it currently covers:

- **Opening illustration block** — "You see how it works. / You catch what's wrong. / You make the
  call. / now you're smarter than the tool."
- **Three-group recap** — Patterns 🧩 / Probability & Prediction 🎲 / Human Judgment 🧭, each with a
  one-paragraph summary (Human Judgment: "You set the goal, give the context, check the claims,
  protect what's private, and make the final call. AI can help with the work. It can't own any of
  that for you.").
- **"READ THE NAME ON THE BOX" + DecodeCards** — "ChatGPT, decoded" (Chat / Generative / Pre-trained
  / Transformer).
- **QUESTIONS_YOU_CAN_ANSWER ShowcaseBox** — 8 questions the student can now answer (hallucination,
  tokens, temperature/variance, context, prompting, sycophancy, verification, ownership).
- **Closing trophy block** — "You know more about AI than most people who use it," tokens/
  embeddings/attention callback.

### Verbatim copy worth parking regardless

Not applicable — nothing is being cut from this lesson in this plan.

### Stale-claim flags (post-resequence)

- **`NextLessonGate` label "Next: Integrity"** (`props.completeAndNavigate("integrity")`) will
  become inaccurate once Task 4 relabels the `integrity` id to "Habits for the Road." The gate
  target (id `integrity`) stays correct — only the visible button label text needs to change to
  "Next: Habits for the Road" when Task 4 lands. Not a content problem, just a label that will go
  stale one task later than this one.
- No other recap claim references a lesson, id, or section structure that this plan changes — the
  three-group recap and the eight questions are all about Understand AI / Avoid Traps material,
  untouched by the Build Your Skills + Finish Smarter merge.

---

## Summary of named lists (for downstream tasks)

- `HUMANEDGE_SURVIVORS` — humanedge section, Survivors (KEEP list), above.
- `BUILDEDGE_SURVIVORS` — buildedge section, Survivors (KEEP list), above.
- `THOUGHTPARTNER_INVENTORY` — thoughtpartner section, Survivors (KEEP list), above.
- `AIJUDGES_CORE` — aijudges section, three lettered buckets (a)/(b)/(c), above.

## Open judgment calls for David

1. `humanedge`'s "Apply real domain knowledge" vs. `buildedge`'s "Deep knowledge in any field" —
   recommended resolution: cut humanedge's, keep buildedge's (richer, load-bearing in Five Places).
2. `humanedge`'s "Break down messy problems" — partial overlap with `prompting`'s Move 3; kept as
   SURVIVOR on the read that they teach different skills (framing a messy real problem vs.
   sequencing a known task), but it's close enough to flag rather than assume.
3. `aijudges`'s detector scenario (bucket a) is mostly redundant with `integrity`'s existing "SHOW
   YOUR PROCESS" box — Task 4 should treat it as a small addition (the meeting script + naming the
   five questions), not a wholesale transplant.
4. `buildedge` cites "Verify and Evaluate" as two lessons; only "Evaluate the Results" (`evaluating`)
   currently exists. Pre-existing bug, unrelated to this merge, worth a one-line fix whenever this
   survivor is edited into Make Your Move.
5. `buildedge`'s citation of "Thought Partner" by name will go stale once Task 3 dissolves that
   lesson — flagged for whoever writes Make Your Move, not something to fix in Task 1–2.
