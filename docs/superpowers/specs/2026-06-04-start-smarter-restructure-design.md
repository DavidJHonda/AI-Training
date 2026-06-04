# Start Smarter Restructure — Relocate the AI Primer Loop — Design

**Date:** 2026-06-04
**Status:** Approved (design); pending implementation plan
**Sections affected:** Start Smarter (primary), Understand AI (Primer removal + opener recap)
**Supersedes part of:** `2026-06-04-ai-primer-design.md` (the AI Primer lesson built there is relocated/dissolved by this work)

## Problem

The newly-built **AI Primer** lesson (in Understand AI) duplicates content the Start
Smarter lesson **What is AI?** already teaches. "What is AI?" already states the
Primer's whole thesis verbatim:

> "There's one lens behind most of what AI does: patterns, probability, and
> prediction. AI finds repeated patterns in the data it's seen and predicts what's
> most likely. You'll see this same lens in every lesson."

So the patterns → probability → prediction loop is taught twice, in two sections.

Separately, **What is AI?** is overloaded — it currently does five jobs in one lesson:
define AI, teach the lens, debunk three myths, show "you already use AI" everyday
examples, walk a Google Maps example, introduce generative AI, and run a
"stored vs built" SEE IT. That is too much for one Start Smarter lesson.

## Idea

Dissolve the standalone Primer and **relocate its loop up into "What is AI?"**, then
**redistribute the overloaded "What is AI?" content** into single-purpose lessons:

- **What is AI?** becomes the conceptual model (the loop), light and prose-driven.
- A new **You Already Use AI** lesson carries the breadth (AI is everywhere, mostly
  narrow, not just ChatGPT).
- **What's an LLM?** absorbs the next-word-prediction mechanism and the generative-AI
  content, restructured into two movements.

The loop frame now lives early in Start Smarter, benefiting the whole course; the
dense Understand AI section keeps its on-ramp via a short recap in its opener.

## Decisions (locked during brainstorming)

1. **Understand AI:** remove the standalone Primer; add a brief recap to the
   Foundations opener that calls back to the loop now taught in What is AI?.
2. **"What is AI?" depth:** carries the loop **as prose only** — no activities. Both
   of the Primer's pieces (the "How the model picks the next word" worked-example bar
   chart, and the "Guess the Most Probable Word" TRY IT) move out of it.
3. **Destination of the two prediction pieces:** both go to **What's an LLM?**.
4. **New lesson order:** Welcome → Why Learn AI? → What is AI? → **You Already Use AI**
   → What's an LLM? → Does AI Think? … (You Already Use AI sits *after* What is AI?).
5. **Three allocation defaults (confirmed):** Google Maps example, the "Most AI is not
   ChatGPT" KeyInsight, and the "sometimes it misses" beat all move to **You Already
   Use AI**.

## Design

### Lesson map changes

- **Delete** lesson `primer` from Understand AI (remove from SECTION_GROUPS,
  SECTION_META, SECTION_COMPONENTS; delete the `PrimerSection` function).
- **Add** lesson `youalreadyuse` to Start Smarter, inserted between `aihistory`
  (What is AI?) and `llms` (What's an LLM?).
- **Counts:** Start Smarter 7 → 8; Understand AI 16 → 15; total course lessons
  unchanged (one lesson removed, one added).

### Content allocation (what moves where)

**What is AI? (`aihistory`) — the conceptual model, light and prose-driven:**
- KEEPS: AI definition; the `what-is-ai.jpg` image; the three myths (not magic / not
  a person / not a search engine).
- GAINS: the loop **as prose** — the Primer's four beats (patterns → training →
  probability → prediction) rewritten as plain-language narrative, merged with the
  existing "one lens" paragraph (which already states this). NO activities.
- LOSES (moves out): everyday-uses showcase; Google Maps example + "sometimes it
  misses" beat; "Most AI is not ChatGPT" KeyInsight + "most products are mixes"
  point; generative-AI section; the "Stored Answers vs Built From Probability" SEE IT.

**You Already Use AI (`youalreadyuse`, NEW) — AI is everywhere, mostly invisible and narrow:**
- The "YOU ALREADY USE AI" everyday-uses showcase (Spotify/Netflix, Maps, face
  unlock, photo search, voice assistants).
- The Google Maps worked example (the patterns/probability/prediction lens on a
  non-chatbot AI) + the "sometimes it misses" attitude beat.
- The "Most AI is not ChatGPT" KeyInsight + the "most products are mixes" point.
- Has no TRY IT (its activity moved to LLMs); ships as a breadth lesson with two
  showcases. Acceptable; flagged as a watch-item for live review.

**What's an LLM? (`llms`) — restructured into two movements:**
- **Part 1 — what an LLM is and does:** LLM-decoded (L/L/M) → phone autocomplete →
  the "How the model picks the next word" bar chart (worked example) → "Guess the
  Most Probable Word" TRY IT → generative AI (it doesn't just predict, it *generates*)
  → the "Stored Answers vs Built From Probability" SEE IT.
- **Part 2 — the landscape:** ChatGPT/Claude/Gemini (products) → Opus/Sonnet/Haiku
  (models).
- This is a large lesson; the two-movement structure keeps it navigable. Flagged for
  live length review.

### Understand AI changes

- Delete the `primer` lesson (above).
- Add a recap to the Foundations opener (`openerfoundations`): one or two lines
  calling back to the loop now taught in What is AI? (e.g. "You met the core loop back
  in What is AI? — patterns, probability, prediction. This section opens up each
  part."). Preserves the forward-reference on-ramp without re-teaching.

### Wiring & housekeeping

- **Order/nav:** insert `youalreadyuse` between `aihistory` and `llms` in
  SECTION_GROUPS (Start Smarter). Re-point navigation: What is AI? → You Already Use
  AI → What's an LLM? (today What is AI? navigates straight to `llms`). Add
  `youalreadyuse` to SECTION_META (kicker/label/icon) and SECTION_COMPONENTS.
- **Quiz fix:** the Test Yourself question currently pointing to `primer` (the
  word-by-word probability question) re-points to `llms` (where the prediction demo +
  generative content now live); update its `section:` display label off "AI Primer".
- **Stale-ref sweep:** grep every remaining `"primer"` reference (nav targets,
  `lessonId`, `review`, SECTION_* keys) and reconcile so nothing points to the deleted
  lesson.
- **Housekeeping:** update `briefing.md` (new lesson, removed lesson, re-scoped
  lessons, both section counts, order arrays); log genuinely-cut copy to
  `docs/parking-lot.md`; run `design-check.sh` and reconcile FLAGs; keep all new/moved
  copy em-dash-free (design-check baselines em-dashes at 4).

## Scope

**In scope:** the lesson-map changes, content moves, the new You Already Use AI lesson,
the What's an LLM? restructure, the Understand AI opener recap, the Primer deletion,
nav/quiz/stale-ref fixes, and housekeeping above.

**Out of scope:** reworking products/models content (note: it overlaps with the Work
With AI lessons "Choosing the Product"/"Choosing the Model" — a pre-existing concern,
not addressed here); any other lesson; adding a new activity to You Already Use AI.

## Done criteria

- `youalreadyuse` lesson renders, placed after `aihistory`, before `llms`; Start
  Smarter nav chain is What is AI? → You Already Use AI → What's an LLM?.
- `primer` lesson fully removed (registries + `PrimerSection` function); Understand AI
  is 15 lessons; opener carries the loop recap.
- What is AI? teaches the loop as prose (no activities) plus definition + myths.
- You Already Use AI carries the everyday-uses showcase, Google Maps + "sometimes it
  misses", and "Most AI is not ChatGPT" + "most products are mixes".
- What's an LLM? carries the two prediction pieces, generative AI, and the
  stored-vs-built SEE IT, in the two-movement structure.
- Test Yourself quiz no longer references `primer`; review points to `llms`.
- No remaining reference anywhere points to the deleted `primer` lesson (live code).
- `briefing.md` updated; cut copy in `docs/parking-lot.md`; `design-check.sh` PASS.
