# How We Got Here — Demystification Redesign

**Date:** 2026-06-15
**Lesson:** Understand AI → Foundations → How We Got Here (id `howwegothere`, component `HowWeGotHereSection`, index.html ~line 2202)
**Status:** Approved in brainstorming; ready for implementation planning.

## Problem

The lesson was received lukewarm in the first live test. Root cause: it's a passive list of 9 dated
events that name concepts (autoregressive generation, the perceptron, backpropagation, the
transformer) before students understand any of them — names-before-meaning. It's also the only
lesson in the Welcome→Rules-vs-Patterns stretch with no SEE IT/TRY IT, and its genuinely good
payoff (four unrelated ideas collided; one 2017 turning point) is told as a flat list, not felt.

## Objective (flipped)

From "AI is old / it didn't appear overnight" (history for its own sake — weak for teens who never
experienced the 2022 "burst") to **demystification**:

> **AI isn't magic. It's four ordinary, human-made ideas — invented separately across centuries by
> people who weren't trying to build AI — that finally collided in 2017. And you're about to learn
> each one.**

This serves the course thesis directly: "be smarter than the tool" only works if students believe
the tool is *comprehensible*. The history is the vehicle for "not magic," not the destination.

## Approach

Chosen direction: **"Assemble the machine" + "two eras" finale** (the 1+2 hybrid). The lesson is
reorganized around the four ideas students already met in *What Is AI?* (probability, prediction,
training, patterns), NOT around a chronological list. Obscure historical names are demoted to small
flavor captions.

## Lesson arc

1. **Hook** (short prose): name the "AI appeared overnight, like magic" feeling and flip it — it's
   four ideas you've already met, invented by people who weren't trying to build AI, and you can
   watch them come together. (No em-dashes in copy — house style; design-check enforces.)
2. **The four ideas:** keep the existing `CoreLoopBox` (reinforces *What Is AI?*). Brief.
3. **Interactive SEE IT** (new core; replaces the 9-card static timeline). See below.
4. **KeyInsight:** reworked — keep a thread of "centuries in the making" awe, land it on *not magic /
   understandable parts*.
5. **Gate → Rules vs Patterns** (`aivscode`), unchanged.

## The interactive SEE IT: "Assemble the machine → ignition"

A guided reveal the student drives. No right/wrong answers, so it is a **SEE IT** (sand band,
`variant: "see"`, `surface: "sand"`) — and becomes the first activity this lesson has ever had.

**Phase 1 — bring in the three ancient parts.** Three faded/greyed pieces. Clicking each lights it
up and reveals a one-line plain-language origin with the historical name shrunk to flavor:
- **Probability** — "1650s. Started as gambling math: figuring the odds." (Pascal & Fermat, small)
- **Prediction** — "1948. Guess the next word from the last, like your phone's autocomplete." (Shannon, small)
- **Training** — "1957. The first machine that learned from examples instead of following instructions." (the perceptron, small)

**Phase 2 — the fourth click IS the turning point.** The last piece is **2017 · Patterns (the
transformer)**. Clicking it does not merely light up — it **snaps all four together** into one
glowing unit. The assembly click and the 2017 collision are the SAME action (no separate "press
2017" step). Copy for this piece names the transformer/"attention" idea in plain terms: the
breakthrough that let a machine find patterns across all the words at once.

**Phase 3 — the "two eras" payoff fires automatically** on the fourth click: a line/track that sat
flat for ~300 years suddenly rockets up to ChatGPT/today. Centuries of nothing, then ignition —
felt in one motion. (This absorbs the old "2018–2021 Scaling Up" + "2022 ChatGPT" beats.)

**Takeaway** (`Takeaway` component): "Not magic. Assembled, from four ideas you can understand.
You're about to learn each piece."

**State:** persist progress (which pieces are in / ignited) via a `useLocalStorage` key, following
the house pattern (e.g. `seeit-howwegothere-assembleStep`). The gate stays `ready: true` (always
open), matching the lesson's current behavior — the SEE IT is a reveal, not a required activity.

## What's cut vs. kept

- **CUT:** the static 9-event timeline as centerpiece; **Bayes (1763), Yule (1927, autoregressive),
  and backpropagation (1986)** as named milestones (confirmed — for brevity and engagement). Their
  dates disappear; they are not preserved as flavor.
- **COMPRESSED:** probability, prediction, training each keep ONE origin beat (1650s / 1948 / 1957);
  the 2017 transformer becomes the ignition; "Scaling Up" + "ChatGPT Launches" become the explosion
  payoff.
- **KEPT as-is:** `CoreLoopBox`, the gate target (`aivscode`).
- **Old data structures** `TIMELINE` and `IDEA` (index.html ~2202–2218) are replaced by the SEE IT's
  own data; remove what the new component no longer uses.

## Title / metadata

- **Label:** "How We Got Here" — unchanged (still fits the assemble-the-origins story; avoids churn).
- **Id:** `howwegothere` — unchanged (house pattern: ids are stable).
- **Kicker:** change `SECTION_META.howwegothere` kicker from **"THE LONG ROAD"** → **"AI ISN'T
  MAGIC"** (index.html line ~1339). Sets up the later *AI is Math* lesson (not magic → it's math).

## Design-system constraints

- New copy must contain **no em-dashes** (`design-check.sh` expects exactly 7 file-wide; all are
  pre-existing). Use commas/colons/periods.
- SEE IT/TRY IT activity interiors are **excluded** from the `BOX_TEXT`/`BOX_LABEL` typography tokens
  (per house convention) — the SEE IT may size its own text.
- Any counter/progress UI must use the `ActivityCounter` component, not hand-built pills (design-check
  baseline = 4 hand-built pills; do not add more).
- SEE IT band tokens: `--seeBand` (sand), `--seeAccent` (amber), `--seeRule`. Serif (`--serif`) only
  for activity numerals/display moments; all prose/feedback in `--sans`.
- Reuse existing activity primitives where they fit: `InteractiveBox` (variant "see", surface "sand"),
  `ActivityInstruction`, `Takeaway`, `KeyInsight`, `InnerCard`. Build a custom assemble/ignition
  sub-component for the four-pieces interaction and the flat→explosion finale.

## Code touch points

- `HowWeGotHereSection` (index.html ~2202–2270): rewrite body — new hook prose, keep `CoreLoopBox`,
  replace `TIMELINE` render with the new SEE IT, rework the `KeyInsight`, keep the gate.
- `SECTION_META.howwegothere` kicker (index.html ~1339): "THE LONG ROAD" → "AI ISN'T MAGIC".
- Remove now-unused `TIMELINE`/`IDEA` locals.

## Out of scope

- No change to lesson order, ids, gates, or the Understand AI count (this is a within-lesson
  redesign, not a structural change). **No `briefing.md` update needed** — label and id are unchanged
  and the briefing lesson map does not record kickers or activity content.
- The two-sittings split of Understand AI (separate, earlier-discussed delivery decision).

## Follow-ups

- Run `design-check.sh` and reconcile FLAGs before committing `index.html`.
- Browser-verify the SEE IT renders and the ignition + explosion fire (the prior session's count-
  drift was caught only by a live render — do the walkthrough).
- Log any cut copy worth keeping in `docs/parking-lot.md` (the full historical timeline text, if you
  want it retrievable).
