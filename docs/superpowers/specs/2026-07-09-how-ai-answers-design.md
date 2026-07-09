# How AI Answers — Prediction lesson redesign

Date: 2026-07-09. Approved by David in chat.

## Why

The Prediction lesson explains the pick and the probability list, but doesn't show how the model
gets from a real question to a typed word. Prediction and probability are two big parts, but they
aren't what the lesson is *about* — the lesson is about how AI answers you. The rework retitles it,
walks a real question through the whole pipeline (doubling as a section review), and lands the pick
on a concrete, funny moment: the model naming a dog.

## Decisions (made during brainstorming)

1. **Split the job with Inference.** How AI Answers owns ONE token: a light recap-walk of the read
   pipeline plus deep treatment of scoring, probability, and the pick, ending on "Spot" — one word.
   Inference keeps the LOOP: no memory, run-it-again, output streaming, the full-journey diagram,
   the frozen-engine section, and the checkpoint quiz. Handoff is a cliffhanger: "that's one word —
   what writes the rest?"
2. **Unify on the dog example.** Keep the phone-keyboard hook. Retire the "See you ______" thread:
   ThreeChatsBox is replaced by a dog-name probability chart, and the "Call the Top Pick" TRY IT
   re-themes to dog names. One example carries the lesson.
3. **Compact recap strip.** The pipeline review is one visual (four mini-stage cards), not prose
   sections — it must not steal Inference's full-diagram capstone.

## Lesson structure (in order)

1. **Title/meta.** SECTION_META label: `Prediction` → `How AI Answers`. Internal id stays
   `prediction` (ids are stable across retitles). Vector Space's NextLessonGate label becomes
   "Next: How AI Answers". Kicker text may update (vestigial; not rendered).
2. **Intro** (David's draft): Vector Space callback — final vector landing in its neighborhood,
   "that landing was about meaning: the model understanding the words you put in" — ending "Now we
   move to the next step: how AI answers you." The current intro's Training sentence is dropped.
3. **Teaser statement.** Setup line: "The following statement is confusing right now. By the end of
   this lesson, it won't be." Then a statement card (house statement-card pattern; doubles as a
   future video board): **"AI predicts the next word based on what you already typed."** The folk
   phrasing ("word", not "token") is deliberate — the lesson sharpens it in beat 7. Follow with the
   review framing: getting there doubles as a review of the whole section, because that's how AI
   works.
4. **The question.** "Let's take a simple question and watch AI build its answer:" — chat bubble:
   "What should I name my new dog?"
5. **Recap strip.** One compact visual: four mini-cards with arrows, each tagged with the lesson it
   reviews — TOKENS (question split into chips) → POSITION STAMPS (#1–#8 mixed in) → STARTING
   MEANING (each token's vector) → THROUGH THE LAYERS (attention + transformation, ~100 passes,
   meaning locked in). Framed explicitly as all-review.
6. **Scoring (new material begins).** Phone-keyboard hook moves here (three chips above the
   keyboard; "AI runs the same logic, way deeper"): the model scores every token it knows against
   the final position and ranks them by probability. The existing 3-step ordered list is absorbed
   into this beat (rewritten around the dog question, not kept verbatim).
7. **The chart + the pick.** The answer-in-progress reaches the name slot ("You could name him
   ___") and the dog-name probability chart appears: Spot on top, then Max, Buddy, Rex, and a long
   tail — bar-chart style reused from What Is AI?'s peanut-butter chart. The model picks Spot and
   types it. Key point: this is **prediction** — score every possible next token, pick from the
   top.
8. **Teaser resolved.** Return to the bold statement and sharpen it: "word" → token; "what you
   already typed" → everything in the context window. The existing attention/context-window
   paragraph survives here as the bridge to the TRY IT.
9. **TRY IT re-themed.** "Call the Top Pick", same ScenarioRow/FeedbackPill mechanics, three rows
   of context steering the dog-name list (e.g., Great Dane puppy → Titan; Star Wars chat → Chewie;
   brand-new chat → safe generic Buddy). Feedback lines reference the context window. Gate
   unchanged: unlocks on completion, "Next: Inference".
10. **Cliffhanger close.** "Spot is one token. The answer isn't finished — and the model doesn't
    even remember the work it just did. What turns one pick into a whole reply is the next lesson."

## Inference-side edit (light)

One-sentence intro adjustment to receive the handoff: reference the Spot moment ("You watched the
model pick Spot: one token"). The journey diagram, loop, frozen engine, and MatchTermsTryIt stay
untouched.

## Removals and bookkeeping

- ThreeChatsBox ("See you ___") and the old CTX_TASKS rows → docs/parking-lot.md entries.
- Briefing lesson map regenerated from SECTION_GROUPS after the label change.
- Check other lessons for references to the lesson label "Prediction" (the concept name stays
  taught; LoopLocator's "Prediction" concept in What Is AI? is unaffected).
- Glossary: prediction-sourced terms keep their source id (`prediction`).
- design-check.sh before commit; browser verify of the new lesson and both gates.
- No video exists for this lesson yet; the eventual prompt gets written against the new structure.

## Out of scope

- Any change to Inference beyond the one-sentence handoff.
- New interactive mechanics (the TRY IT reuses existing components).
- The Prediction video prompt (future work, after the lesson ships).
