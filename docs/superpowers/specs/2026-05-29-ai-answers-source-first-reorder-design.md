# AI Answers — Source-First Reorder (Design)

**Date:** 2026-05-29
**Section:** AI Answers (section 04 / 10) in `index.html`
**Goal:** Fix the disjointed feel of the AI Answers learning arc by reordering the middle source-first and merging the redundant generation-loop lessons.

## Problem

The current arc runs:

```
Opener · Context Window · Inference · Probability · Prediction · Patterns · What AI Does Best   (7 lessons)
```

Three issues make it feel disjointed:

1. **Overlap in the middle.** Inference already teaches the whole loop ("predicts the next token, adds that token, repeats until complete"). Probability re-teaches the scoring step; Prediction re-teaches pick-and-repeat. The "...and then it repeats" beat is taught three times.
2. **Effects before cause.** Patterns' own insight says it cleanly: *"Probability is the score. Prediction is the action. Patterns are the source."* Yet the section teaches score → action → **source**, explaining symptoms for three lessons before revealing the mechanism.
3. **False parallelism.** Probability / Prediction / Patterns are presented as a flat P-P-P triad, but they are nested: patterns is the substrate, probability is derived, prediction is the act.

What works and must be preserved: the opener's training/inference split as the organizing frame; the Luke/Nate context example threading through the section; all surviving activities.

## Target arc (6 lessons)

```
Opener
1 Context Window    — PACKAGE: what the model can see this turn          (unchanged in place)
2 Patterns          — THE SOURCE: what training left in the weights      (moved up from #5)
3 Probability       — READ ONE: a pattern -> a score for the next token  (reordered after Patterns)
4 Inference         — READ IT ALL: pick + append + repeat = full answer  (= old Inference + old Prediction, merged)
5 What AI Does Best  — PUT IT TO WORK: four engines                       (unchanged in place)
```

Organizing logic flips from "trace the pipeline" to **"training wrote patterns into the model; here's how inference reads them back out into an answer."** Source precedes effects; the nesting (source → one read → many reads = journey) becomes the spine; "Inference" earns its name as the full read-out at the end of the run block; the triple-taught "it repeats" beat collapses to once.

## Opener changes (`openeranswers`)

Re-sequence the four move-groups (still four moves):

| Move | Lesson(s) | Bridge line (draft) |
|---|---|---|
| PACKAGE THE INPUT | Context Window | "Every turn, your input gets packaged." |
| WHAT TRAINING LEFT BEHIND | Patterns | "Inside the model sits one thing training wrote: patterns." |
| READ IT INTO AN ANSWER | Probability → Inference | "The model reads those patterns out, token by token, into a full answer." |
| PUT IT TO WORK | What AI Does Best | "What all that machinery makes AI genuinely good at." |

- Featured-card preview list reorders to: *"…what gets packaged each turn, the patterns training left inside, how the model reads them into an answer token by token, and what all of that makes AI genuinely good at."*
- The old "RUN THE MODEL" group's three questions (inference, probability, prediction) collapse: the prediction question folds into the Inference loop; probability and inference sit under "READ IT INTO AN ANSWER."
- `sectionOverview` subtitle "Four moves, from your input to what AI does best" still holds — keep.

## Per-lesson seam rewrites

Copy below is draft-level; tighten at implementation. Use sans for prose (no Source Serif), per the design system.

**1 · Context Window → Patterns** (was → Inference)
- Nav target `inference` → `patterns`; label "Next: Inference" → "Next: Patterns".
- Closing handoff points inward: *"You've seen what the model can see. Next: the one thing inside the model that turns all of it into an answer."*

**2 · Patterns** (moved to position 2)
- Keep the Luke/Nate open — still valid (Context Window introduces Luke/Nate one lesson earlier).
- Rewrite the false line "This section has been about patterns the whole time" → forward-looking: *"Everything after this — the scoring, the picking, the whole answer — is this one idea in motion. Let's name it first."*
- Keep the "Training Writes. Inference Reads." section — now the anchor at position 2, reinforcing the opener's split.
- Rewrite the closing insight (currently *"Probability is the score. Prediction is the action. Patterns are the source"*, which references lessons that now come after) into a forward promise: *"Patterns are the source. Now watch them get read out — first as a score for one token, then chained into a whole answer."*
- Nav target `whatitdoesbest` → `probability`; label → "Next: Probability".

**3 · Probability** (after Patterns)
- Rewrite the open (currently *"You just saw Inference. Stage 5 was where…"*, now broken): *"You just saw what training leaves behind: patterns stored as connection strengths. Now watch one get read. When the model needs the next token, it turns those strengths into scores."*
- Keep "How the model picks a token", the "Guess the Most Probable Word" TRY IT, and the "High probability isn't truth" insight.
- Rewrite closing → loop setup: *"That's one token's score. But an answer is hundreds of tokens. Next: how one score becomes a whole answer."*
- Nav target `prediction` → `inference`; label "Next: Prediction" → "Next: Inference".

**4 · Inference** (merged; see next section)

**5 · What AI Does Best** (unchanged in place)
- Light touch. The opener line "three ideas: patterns, probability, prediction" still holds — all three are still taught; prediction now lives inside Inference rather than as its own lesson. Keep unless reword is requested.

## Merged Inference lesson (new position 4)

Assemble, in order:

1. **New open** — names the loop, ties patterns + probability together: *"You've met the source (patterns) and one score (probability). Now chain it: the model picks a token, adds it to the response, and scores the next — and the whole repeating journey has a name: Inference."*
2. **SEE IT "The Complete Journey"** *(kept from Inference)* — the generic loop pick → append → repeat; ends on "Now repeat the entire journey" takeaway.
3. **ShowcaseBox "Neural Network"** *(kept from Inference)* — nodes / weights / "70 billion parameters." One-line trim so it doesn't re-introduce weights from scratch (Patterns now introduces weights two lessons earlier).
4. **SEE IT "Same question, different prediction"** *(kept from Prediction — the Luke/Nate token walk)* — proves context reshapes every pick. The anchor activity.
5. **KeyInsight** — merged: *"One answer. Many picks. Each one shapes what comes next."*
6. Gate → What AI Does Best (`whatitdoesbest`).

Net: two SEE ITs + one showcase. Parking the heaviest activity (below) keeps density in check.

### Parked content

Move to `docs/parking-lot.md` verbatim, with origin + possible-destination note:
- The `SectionKicker` "The Scale of What's Happening"
- The SEE IT "Why it feels instant" (the ~100,000,000,000+ calculations counter, ThinkingBubble/AIBubble compute animation, the "3,000 years" line)
- Its KeyInsight *"Billions of calculations, all for one word."*

This is parked, not cut — it may return to Inference or another lesson later.

## Wiring changes (verified by grep)

- `SECTION_GROUPS` (line ~1180): reorder the AI Answers `sections` array to `["openeranswers", "prompt", "patterns", "probability", "inference", "whatitdoesbest"]` and drop `"prediction"`. `SECTIONS` derives from this, so lesson count and ProgressBar update automatically.
- Opener `groups` (line ~6555): re-cluster questions into the four new moves; fold the old prediction question into the Inference loop group.
- Navigation `completeAndNavigate` targets: Context Window→`patterns`; Patterns→`probability`; Probability (line ~4689)→`inference`; Inference→`whatitdoesbest`. (Opener `nextLessonId` stays `prompt`.)
- Delete the standalone `prediction` lesson: its component function (LessonHeader at line ~5735), its `SECTION_META` entry, and its id→component mapping (~line 14335). Its content (Luke/Nate SEE IT + merged insight) moves into the Inference component.
- Confirm the `inference` `SECTION_META` title/subtitle still reads correctly for the merged role ("Inference: From Prompt to Output" is fine; adjust only if needed).
- `briefing.md`: rewrite the AI Answers lesson-map line (6 lessons, new order, no `prediction`) and bump the total lessons from 71 → 70. (Per keep-briefing-in-sync.)
- No vocab `TERMS` entries are sourced to `prediction`, and no recap/cross-link references it — confirmed by grep. Re-grep before deleting to be safe.

## Out of scope

- No visual/design-token changes; reuse existing components (InteractiveBox, RevealSequence, ShowcaseBox, KeyInsight, Takeaway, NextLessonGate).
- No changes to other sections except the briefing.md count.
- No new activities authored; only kept/parked/reordered.

## Verification

- Run `design-check.sh` and reconcile any FLAGs before committing `index.html`. (Per run-design-check-before-commit.)
- Manually click through the section in-app: opener → Context Window → Patterns → Probability → Inference → What AI Does Best, confirming every "Next" gate lands on the right lesson and no nav points at a deleted `prediction`.
- Confirm the in-app `validate()` console check still passes with the new `SECTIONS.length`.
- Confirm `docs/parking-lot.md` holds the parked block verbatim.
