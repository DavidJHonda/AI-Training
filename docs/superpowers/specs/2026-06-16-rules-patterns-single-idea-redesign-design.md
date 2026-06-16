# Rules vs Patterns — Single-Idea Redesign

**Date:** 2026-06-16
**Section:** Understand AI → Foundations
**Lesson id:** `aivscode` (unchanged)
**Status:** approved, ready for implementation plan

## Background

The 2026-06-15 merge folded `data` (Mess to Meaning) into `aivscode` (Rules vs Patterns).
That merge was lesson-count consolidation: it kept *both* CompareBoxes and *both* TRY ITs,
so the lesson now reads as two half-lessons stapled together — idea A (patterns, not rules)
followed by idea B (AI reads the mess) — each with its own CompareBox and its own activity.

This redesign re-pitches the lesson as **one idea**, not two.

## The decision that drives everything: it's one idea, told as cause → effect

"AI reads the mess" is **not** a second, co-equal takeaway. It is the **consequence** of
"patterns, not rules":

> AI is built on learned patterns instead of written rules — **and that's exactly why**
> it can take messy, unfamiliar input and hand back something usable.

Every structural choice below follows from collapsing the two halves into this single
cause → effect arc.

## Decisions

1. **Title:** keep **"Rules vs Patterns."** Considered renaming (e.g. "Patterns & Data") but
   rejected: an `&` frames the two ideas as co-equal, which is the parallel reading we are
   explicitly dropping; and "Data" is generic in a course where most Foundations lessons touch
   data. The contrast is what makes "patterns" legible, so a mechanism-led title earns its keep —
   provided the *flow* delivers the mess payoff. It does.

2. **One TRY IT, fused (Approach 3).** Replace the two activities with a single progressive
   activity. The learner's one action per row stays the **discrimination** (rule or pattern?);
   on the pattern-wins rows, the **feedback reveals what AI pulls out** of the mess and, on the
   last row, what it **can't invent**. The choice carries idea A; the feedback carries idea B.
   This resolves the title-vs-spine tension instead of picking a side: the contrast sets up every
   row, the mess payoff is the reward, and the guardrail survives as the closing KeyInsight.

   - Rejected **Approach 1** (keep discrimination activity, demote the payoff to tell-not-do):
     contradicts the spine — the payoff is the point and should be *done*, not just shown.
   - Rejected **Approach 2** (keep extraction activity, drop the discrimination): the one
     hands-on moment in a lesson called "Rules vs Patterns" would never touch rules.

3. **One CompareBox, merged.** Combine the two CompareBoxes into a single, taller box. Both old
   boxes already share the same two columns (Traditional software / AI), so each column tells a
   top-to-bottom causal story: **what it needs (input) → how it acts (behavior) → its superpower.**
   A longer box is acceptable because the vertical order *is* the connection — the data idea
   (input row) and the mess payoff (superpower row) sit in the same box that establishes the
   rules-vs-patterns mechanism.

4. **Reorder: SEE IT before the merged CompareBox.** Today CompareBox #1 precedes the SEE IT.
   New order is experience-first: watch the difference live, *then* let the box systematize it
   and extend it to data/mess. The modalities grid then sits right where it primes the activity.

## New lesson arc (delivery order)

1. **Intro** — patterns recap + `if/then/otherwise` rules paragraph + chef/recipe analogy.
   *(mechanism; unchanged copy)*
2. **SEE IT** — "Fixed Rules vs. Built From Patterns" (PS5). *(watch the difference; unchanged)*
3. **Kicker "THAT'S WHY AI EXPLODED"** + "handling the unfamiliar / rules break" prose.
   *(unchanged copy)*
4. **Merged CompareBox** — the full contrast, ending on "Makes sense of mess." *(new structure,
   assembled from the two existing boxes; see below)*
5. **Bridge prose** — short, points from "makes sense of mess" into the activity. *(trim the
   current two bridge paragraphs to one tight lead-in; do not re-explain structured-vs-messy in
   words — the box's input row already carries that visual)*
6. **Fused TRY IT — "Which One Handles This?"** — single activity, 4 rows. *(new)*
7. **KeyInsight** "It restructures; it doesn't invent." + LessonRule + gate to `norules`.
   *(unchanged copy; gate now requires only the one activity)*

## Merged CompareBox structure

Two `ComparePanel` columns, each a vertical stack of three labeled sections:

**💻 Traditional software** — eyebrow; title "Built from rules a person wrote"
- **What it needs:** clean, structured input — rows, fields, labels, defined ahead of time.
  → ASCII grade-table visual (from old CompareBox #2).
- **So how it acts:** Ask twice → same answer every time · When wrong → a bug on one line, find
  and fix it · Why → open the code and read it. *(from old CompareBox #1; lead with "Ask twice"
  because the SEE IT just demonstrated the answer staying fixed)*
- **Superpower:** "Sorry, none. It only does what it was written to do."

**🤖 AI** — eyebrow; title "Built from patterns in data"
- **What it needs:** messy human input — conversations, photos, audio, half-formed questions; no
  neat fields required. → Text / Images / Audio / Video / Documents grid (from old CompareBox #2).
- **So how it acts:** Ask twice → the answer can change · When wrong → confidently wrong, no line
  to point to · Why → even the people who built it can't fully say.
- **Superpower:** "Handles the unfamiliar. **Makes sense of mess.**"

Source material is the two existing boxes — this is reorganization, not new copy, except the
small section labels ("What it needs" / "So how it acts" / "Superpower") and any glue.

## Fused TRY IT — "Which One Handles This?"

One `InteractiveBox` (variant try, surface mint). Each row: a situation → pick **Traditional
software** vs **AI** → feedback. On pattern-wins rows the feedback *reveals the extraction*; the
last row's feedback also carries the *can't-invent* guardrail, flowing into the KeyInsight.

| # | Situation | Correct | Feedback carries |
|---|-----------|---------|------------------|
| 1 | Split a dinner bill four ways, with tax and tip | Traditional | exact math, one right answer, same every time |
| 2 | Turn a rambling voice memo into a clean to-do list | AI | the tasks AI pulls out of the ramble (extraction) |
| 3 | Check a password has 8+ characters and a number | Traditional | precise fixed yes/no, no judgment |
| 4 | Photo of a handwritten grocery list | AI | the clean checklist it pulls out **+ it won't invent a store or prices that weren't there** (guardrail) |

- 2 rule-wins, 2 pattern-wins; extraction shown twice, guardrail once on the final row.
- Reuse the existing FIT_SCENARIOS copy for rows 1–3 (bill, voice memo, password) where it fits;
  row 4 (grocery photo) is adapted from the old TRY IT #2 grocery scenario, including its
  can't-invent feedback.
- **Dropped from the activity:** the standalone scam-text and drive-thru rows. The "handles the
  unfamiliar" facet stays in the step-3 prose. *(Optional 5th row — scam for unfamiliarity, or
  drive-thru for audio — is a known extension if we want the activity to exercise those facets;
  not in scope for v1.)*

## Code-level changes (for the plan)

All edits are inside `AIvsCodeSection` (index.html ~3494–3744). No registry/nav changes — the
lesson id, gates, and `SECTION_GROUPS` are already correct from the 2026-06-15 merge.

- **State:** the section keeps `fitAnswers`; the second activity's `fuelAnswers` state and
  `fuelAllAnswered` flag are **removed** (only one activity remains). The gate's `ready` goes from
  `fitAllAnswered && fuelAllAnswered` back to a single-activity flag.
- **CompareBox #1 (~3545–3587) and CompareBox #2 (~3670–3681):** replaced by one merged
  `CompareBox` placed *after* the SEE IT (~after line 3615) and the kicker prose, before the
  fused TRY IT.
- **SEE IT (~3589–3615):** unchanged content; now precedes the merged box.
- **TRY IT #1 (FIT_SCENARIOS, ~3500–3513 + render ~3623–3663):** becomes the single fused
  activity. The current FIT_SCENARIOS order is bill (trad), voice memo (ai), password (trad),
  scam (ai); the new set keeps rows 1–3 and **replaces row 4 (scam) with the grocery-photo
  scenario**. Enrich the two pattern-row feedbacks (voice memo, grocery) to reveal extraction,
  and add the can't-invent guardrail to the grocery feedback.
- **TRY IT #2 (fuel activity, ~3682–3739):** removed; its grocery scenario + can't-invent copy is
  absorbed into fused-TRY-IT row 4 and the KeyInsight.
- **Bridge prose (~3664–3669):** trim two paragraphs to one tight lead-in.
- **KeyInsight (~3740):** keep "It restructures; it doesn't invent."; render condition repoints
  from `fuelAllAnswered` to the single-activity flag.
- **Gate (~3742):** `ready` uses the single-activity flag; target `norules` and label unchanged.

## Out of scope

- The optional 5th TRY IT row (scam / drive-thru).
- Any change to `norules` (Harder to Control), `DataSection` (already a dead stub), or registries.
- The two-sittings split of Understand AI.

## Follow-ups (post-implementation)

- Run `design-check.sh` and reconcile FLAGs before committing `index.html` (merging two boxes
  into one and dropping an activity changes style-pattern counts — expect baseline shifts, e.g.
  CompareBox count 2 → 1 within this lesson; confirm no *unexpected* drift).
- Sync `briefing.md` only if the change is structural to the lesson map. Lesson count is
  unchanged (still one lesson, `aivscode`), so this is likely a no-op beyond a dated note that
  the lesson went from two activities/boxes to one.
- Log any cut copy worth keeping (the second bridge paragraph; the drive-thru scenario) in
  `docs/parking-lot.md`.
- Recapture the component screenshot only if a documented component's design/props changed
  (the merged box reuses CompareBox/ComparePanel, so likely not).
