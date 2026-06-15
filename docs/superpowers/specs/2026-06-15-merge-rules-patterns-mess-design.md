# Merge "Rules vs Patterns" + "Mess to Meaning" — Design

**Date:** 2026-06-15
**Section:** Understand AI → Foundations
**Motivation:** The Understand AI section runs too long in a single sitting. The Foundations
group has three lessons that are really one idea (AI runs on *learned patterns*, not *written
rules*) explored from three angles. "Harder to Control" is the only one that introduces new
machinery (guardrails, the control problem) and earns a standalone page. "Rules vs Patterns" and
"Mess to Meaning" are the same contrast stated then proven, so they merge.

## Decision

- **Merge** `aivscode` (Rules vs Patterns) + `data` (Mess to Meaning) into one lesson.
- **Surviving id:** `aivscode` (house pattern: keep the stable id).
- **Title:** keep **"Rules vs Patterns."** Do NOT rename to "Traditional Software" — the lesson
  is about what makes AI different, with traditional software only as the foil; the title must
  keep AI in the foreground.
- **Keep `norules` (Harder to Control) standalone**, immediately after the merged lesson.
- **Keep both TRY ITs** on the merged page (owner is fine with two activities per page).
- Understand AI: 15 → 14 lessons. Foundations: 6 → 5.

## Ordering ripple (accepted)

The mess payoff moves *before* Harder to Control. New Foundations arc:

`Opener → How We Got Here → Rules vs Patterns (merged) → Harder to Control → AI is Math`

So the trio reads **distinction → upside (mess) → downside (control)**, ending the "what's
different" beat on the sober control note before the mechanics (AI is Math, Tokens…). This is a
natural **sitting break** point (after the merged lesson, before Harder to Control); the real
"too long" relief comes from splitting Understand AI across two sittings, which this merge sets up.

## Merged lesson outline (delivery order)

**Act 1 — The distinction** *(from aivscode, intact)*
- Intro prose + `if/then/otherwise` rules paragraphs
- Recipe / chef analogy (anchor metaphor)
- CompareBox (when-wrong / ask-twice / why / superpowers) — its "superpowers" cell names
  "makes sense of mess," the hinge into Act 4

**Act 2 — See it live** *(from aivscode, intact)*
- "Here's what that looks like in action" → **SEE IT: Fixed Rules vs Built From Patterns** (PS5)

**Act 3 — Sort it** *(from aivscode, intact)*
- Kicker "THAT'S WHY AI EXPLODED" + "handling the unfamiliar / rules break" prose
- **TRY IT #1: Which One Handles This?** (bill split / voice memo / password / scam)

**Act 4 — The payoff: mess** *(from data)*
- **Bridge (new/reworked prose):** the cases AI won in TRY IT #1 (rambling voice memo,
  never-seen scam) won *because the input was messy and unfamiliar*. Name that as AI's real edge.
- "It learned from the messy stuff humans produce" prose — **KEEP**
- data's CompareBox (table vs modalities grid) — **KEEP**. It carries a *different* idea from
  Act 1's CompareBox (input: structured/clean rows vs. messy/unstructured data, not behavior),
  and it's the one place structured-vs-unstructured gets a concrete visual (ASCII grade table vs.
  the Text/Images/Audio/Video/Documents strip) — a core AI-literacy concept. The two CompareBoxes
  are separated by the SEE IT and TRY IT #1, so they don't read as a back-to-back echo.
  Constraint: the Act 4 bridge prose must NOT re-explain structured-vs-messy in words right above
  the box — let the box carry that visual; keep the prose pointing back to TRY IT #1.
- ShowcaseBox "The move, step by step" — **COMPRESS** to a tight 3-step strip (or cut)

**Act 5 — Apply it** *(from data)*
- **TRY IT #2: What Could AI Pull Out?** (grades text / grocery photo / drive-thru order)
- KeyInsight → LessonRule → **gate to `norules` (Harder to Control)**

## What gets cut / parked

- **COMPRESS:** data's "The move, step by step" ShowcaseBox.
- **Nothing else is dropped** — both CompareBoxes, both TRY ITs, and the SEE IT survive.
  The only real trim is the ShowcaseBox; the merge's value is mainly lesson-count
  consolidation plus the two-sittings split it enables.

## Code-level changes (for the plan)

- `DataSection` content folds into `AIvsCodeSection`; `DataSection` becomes dead code (stays
  defined per house pattern) and is removed from `SECTION_GROUPS`, `SECTION_META`,
  `SECTION_COMPONENTS`.
- Rewire gates: the merged lesson's final gate points to `norules` (already does). Confirm
  `howwegothere` → `aivscode` and `norules` → `aiismath` are intact; remove the old
  `aivscode` → `norules` → `data` → `aiismath` chain's `data` hop.
- Update `SECTION_GROUPS` Foundations list to drop `data`.
- localStorage keys from `data`'s activity (`fuelAnswers` is component state, no persisted keys
  to migrate; confirm during implementation).
- Section badge counts ("Section · N of M") derive from `SECTION_GROUPS`, so they update
  automatically.

## Out of scope

- The two-sittings split of Understand AI (delivery decision, not a code change here).
- Any change to Harder to Control beyond it now following the merged lesson.

## Follow-ups (post-merge)

- Update `briefing.md` lesson map (Foundations 6 → 5, Understand AI 15 → 14, note the merge and
  the `data` → dead-code transition).
- Run `design-check.sh` and reconcile FLAGs before committing `index.html`.
- Log any cut copy in `docs/parking-lot.md`.
