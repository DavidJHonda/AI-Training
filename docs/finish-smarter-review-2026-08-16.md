# Finish Smarter — pre-edit review pass (2026-08-16)

Eleven independent fresh-eyes reviews (one per lesson + one section-level), run against the
house rubrics in `docs/review-lesson.md` / `docs/review-section.md`, before David's editorial
pass. Verdicts: 🔴 blocks · 🟡 should-fix · 🟢 polish. Reviewers saw the build history's notes
as context but reached their own verdicts; where several reviewers hit the same item
independently, that's marked **[convergent]**.

## The three section-wide patterns (fix once, benefits everywhere)

1. **One premise, five openings [convergent — flagged by 5 reviewers].** "Everyone has the
   same AI / production got cheap" opens the Opener (as its question), People Skills,
   Creative Thinking, Skills That Matter, and Make Your Move. The section reviewer's cut:
   keep it full-strength in People Skills (first of the arc, best version), reduce the other
   openings to a one-line callback. Creative Thinking's reviewer suggests its opener should
   pick up FROM People Skills ("so now what do you bring instead") rather than re-argue
   sameness.
2. **Same activity mechanic, four times [convergent — 5 reviewers].** Scenario-classification
   sorts: AI Tips, then three consecutive (Skills That Matter → Be Curious → Make Your Move;
   the section reviewer counts Creative Thinking's two-scenario judgment as a fourth in a
   row). Strongest suggestion: swap Be Curious's sort for a do-it activity (pick one new
   feature to try this week), which also fixes its thinness.
3. **The "Notice what these have in common" template stamp [convergent — 3 reviewers].**
   AI Tips ("all five"), People Skills ("those three moves"), Skills That Matter ("the two
   places"). AI Tips fires first and keeps it; vary the later two.

## Per-lesson triage (delivery order)

### 1. Opener (`openerskills`) — Tweak
Strongest opening in its family (crisp course-arc recap pivoting into "the person holding
the tool"); the flaw is doubling.
- 🟡 The final whyThisMatters paragraph ("So the order from here is deliberate. First…
  Then… Then… Then…") restates the overview box directly beneath it. No sibling opener
  doubles up this way → cut the paragraph or shrink to a single transition line. **[convergent
  with the phase-5 build review]**
- 🟢 Only opener with no full-width illustration → intake item when an image exists.
- 🟢 The closing question is a near-verbatim cousin of a Creative Thinking line → fine if
  deliberate bookend (the opener asks; the lesson answers); confirm consciously.

### 2. Tune the Model (`choosemodel`) — Tweak
The model/effort teaching is strong (hockey-line analogy, both TRY ITs land); the July
"stitched merge, edit down later" debt is now visible.
- 🟡 Temperature is taught AFTER the "App. Model. Effort." synthesis box, isn't on the close
  board, and has zero practice reps → move it before the synthesis (fold in as a small
  fourth item) or cut to a short callback to One More Thing. **[convergent: lesson + section
  reviewers]**
- 🟡 Still a three-topic stitch, denser than when it was flagged → trim temperature's
  re-teaching of the dog-name table; the section reviewer adds: merge the two TRY ITs into
  one at the end (the first is stranded mid-lesson).
- 🟢 Fact-check: "they're actually different LLMs, not the same brain dialed up or down"
  is stated as a universal — gut-check before shipping.

### 3. AI Tips (`aitips`) — Tweak
Five concrete, copyable moves with relatable scenarios; its devices got reused downstream.
- 🟡 Owns the "notice what all five have in common" device and the scenario-sort mechanic
  that later lessons repeat → keep here (it fires first); vary the later lessons instead.
- 🟢 The "Options" move's TRY IT explain nearly duplicates its NumberedRows prompt wording —
  confirm it reads as reinforcement, not copy-paste.

### 4. Habits for the Road (`integrity`) — Tweak, and the section's one 🔴
Two on-target TRY ITs (the judgment scenarios + Redact the Prompt); the merge carries a
third topic it never promised.
- 🔴 (section reviewer) / 🟡 (lesson reviewer) **[convergent]**: the "It isn't only what you
  type" screening-systems block (three-modes cards, second five-questions list, paper trail,
  proxy variables) is a third major topic in a lesson framed as exactly two habits, with no
  activity of its own. Lesson reviewer: compress to the single strongest thread (the
  being-judged five questions) and cut the rest. Section reviewer: cut the whole block out
  of this lesson (its natural home is Avoid Traps or Embrace the Future). **This is also
  where the parked FOUR ROLES box and four screening TRY IT scenarios await your ruling —
  the same decision: how much "AI judges you" material lives here, if any.**
- 🟡 Two different "five questions" lists in one half, visually identical, one skimmable
  disambiguation line → give them distinct memorable names.
- 🟢 The three-modes card stack lost its wrapper and reads as an orphaned fragment → add a
  kicker. **[convergent with the phase-1-2 build review]**
- Fact-check: per-platform retention/training claims (ChatGPT 30-day hold, Claude "up to
  5 years", Gemini 3-year human review) and the 2023 ChatGPT titles-exposure bug — all
  time-sensitive specifics.

### 5. People Skills (`peopleskills`) — Solid
The ladder lands; the closing run-through (draft/message/plan vs. presence/trust/turnout)
is the strongest move. Keep the premise here at full strength (see pattern 1).
- 🟢 Vary the "notice what those three moves have in common" phrasing (pattern 3).
- 🟢 Confirm the premise's third restatement inside the lesson still earns its space.

### 6. Creative Thinking (`creativethinking`) — Tweak
Core works (one takeaway, well-matched two-scenario TRY IT, clean ending).
- 🟡 Opening re-argues the same-AI premise People Skills just made two paragraphs earlier →
  reframe to pick up from it: open on "so what do you bring instead." (Pattern 1.)
- 🟢 Internal echo: "everyone has the same tool" appears twice within the lesson → collapse
  to one instance.

### 7. Skills That Matter (`skillsthatmatter`) — Tweak
The close ("AI makes production cheap. That's what makes the rest of it expensive") lands
hard; the problems are neighborhood, not page.
- 🟡 First of the three consecutive scenario-sorts (pattern 2) → this one or a neighbor
  changes mechanic.
- 🟡 Opening premise is the section's third telling (pattern 1) → different angle in.
- 🟢 "shelf life… shelf lives" wordplay stalls → "and the shelf life keeps getting shorter."
- Note (section reviewer): its "shelf life / be a beginner again" passage is arguably
  Be Curious's argument — candidate to MOVE there, which thickens Be Curious and
  de-densifies this lesson in one move.

### 8. Be Curious (`becurious`) — Tweak
"Reps are the only seniority in AI" is clear and earned; thinnest lesson in the section.
- 🟡 Middle of the three-sort run → strongest candidate for a different activity shape:
  a do-it activity (pick one new feature, try it this week) fits the lesson's own thesis.
  **[convergent: lesson + section reviewers]** Section reviewer adds: its sort partially
  re-tests Habits for the Road's honesty line.
- 🟢 Opens cold ("Here's a fact worth sitting with…") with no seam from Skills That
  Matter's close → one bridging clause.
- Consider: absorbing Skills That Matter's shelf-life passage (see #7) fixes the thinness
  honestly. Also: the only teaching lesson with no final-exam bank question — if it
  thickens, add one (swap against the bank's closest duplicate).

### 9. Make Your Move (`makeyourmove`) — Tweak
Strongest capstone synthesis in the course; closes on a quotable line.
- 🟡 "Use the second mode too" names a second mode when the first was never called one →
  label the first usage ("Use AI two ways while you build…"). **[convergent with the
  phase-3 build review]**
- 🟢 Densest lesson in the course right before the exam (3 ShowcaseBoxes + illustration +
  3 calls + 5-item activity) → consider folding one box into prose.
- 🟢 Last of the three-sort run — resolves itself if a neighbor changes (pattern 2).

### 10. The Final (`whatyoulearned`) — Tweak
Break beat and exam framing are tight and honest; the inherited recap hasn't caught up
with the course it now fronts.
- 🟡 The study sheet's three-ideas framework + 8-question self-test give zero coverage to
  Embrace the Future and only glancing coverage to Avoid Traps — but the exam draws evenly
  from all six sections → add an idea card and/or self-test questions for the missing
  sections. Section reviewer goes further **[convergent]**: the recap never lands Finish
  Smarter's own payload — close the study sheet on the opener's question answered
  ("Everyone will have the same tool. Here's what you bring") before the exam.
- 🟢 Fact-check: "Pre-trained" DecodeCard's "billions of pages of text, images, audio,
  video, and code" scale claim.

## Section verdict (from the dedicated section review) — Tweak

Biggest strength: the human-skills ladder (People Skills → Creative Thinking → Skills That
Matter → Be Curious → Make Your Move) is a well-built arc with clean seams and the course's
best ending. Biggest weakness: the front third's two merged lessons (Habits for the Road,
Tune the Model) carry more topics than they admit, and the section's thesis never gets
consolidated at the end (The Final's recap tests the machine half only).

No lesson was judged misplaced, mergeable, or cuttable — the order stands. The three 🔴s
are the screening-block scope in Habits for the Road, The Final's recap gap, and the
five-fold premise repetition; all three appear in the per-lesson entries above.

## Open owner decisions this pass surfaces again

- FOUR ROLES box + four screening TRY IT scenarios (parked): fold in, or stay parked —
  now entangled with the Habits for the Road 🔴 (the answer may be "neither: the block
  shrinks").
- Sparring-partner mode is taught nowhere (stale design premise): candidate AI Tips beat.
- Whether the opener question ↔ Creative Thinking echo is a deliberate bookend.
