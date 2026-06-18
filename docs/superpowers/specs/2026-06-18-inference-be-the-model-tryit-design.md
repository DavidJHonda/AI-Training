# Inference "Be the Model" TRY IT — Design

> **Status: removed (2026-06-18).** Built and shipped, then removed the same week. Once the "Name the Piece" vocab checkpoint moved to the end of Inference (the Black Box dissolution), this TRY IT was redundant and felt weak, so `InferenceLoopTryIt` + its data were deleted. Kept as a design record.

Date: 2026-06-18
Lesson: Inference (`inference`), the closing lesson of the Understand AI section.

## Problem

The Inference lesson is the section's capstone but has **no TRY IT** — nothing
hands-on that makes the learner *experience* what the page is about. Its only
interactive is the "ChatGPT, decoded" SEE IT, which is vocabulary recognition, not
the inference process. The old interactive prediction demo (Luke/Nate, "same
question, different prediction") was moved out to Context Window. So the page's
core thesis — generation happens **one token at a time, in a loop, with no plan and
no memory** — is only ever *read* (in the static `InferenceJourneyDiagram`), never
*done*.

## Goal

A TRY IT where the learner acts AS the model's loop: repeatedly pick the next token
from a ranked list and watch a sentence build itself one token at a time, with the
ending depending on their picks. It should make autoregression and "no plan" *felt*,
and tie directly back to the diagram's Probability → Prediction → Loop steps.

## Decisions (from brainstorming)

- **Idea chosen:** "Be the Model / drive the loop" (over predict-the-top-token,
  order-the-journey, fact-vs-myth, etc.) — the most hands-on and the only option that
  enacts the loop the page owns.
- **Steering = Hybrid (1–2 real forks):** mostly a guided spine, but the first pick is
  a genuine fork that sends the sentence to a different ending. Sells "the sentence
  goes where your picks lead" without authoring a full combinatorial tree.
- **Probabilities shown** on each candidate (illustrative), reinforcing the diagram's
  Probability step and the deck's existing ranked-list convention.
- **Placement:** immediately **after `InferenceJourneyDiagram`** (and its lead
  paragraph), before the "At the heart of that journey is a neural network"
  `SectionKicker`. The diagram's loop rail says "runs again"; this TRY IT *is* that
  "again."
- **No gating / no localStorage:** the Next gate stays on the existing ChatGPT-decoded
  reveal.
- **Conclusion = `Takeaway` component, no replay control:** the activity ends with the
  deck's standard `Takeaway` (matching every other sequential TRY IT), not a "Start
  over" button. A replay/reset control is an interaction the deck doesn't use elsewhere.
  (Original design used Start over + a separate `KeyInsight`; changed during review.)

## Content (data)

Seed phrase: **"After school, I like to"**

One real fork at pick 1, then short per-branch tails to a period. Probabilities are
illustrative and need not sum to 100 (the list is the top few of ~100k).

```
Pick 1 — FORK:  play 47%  |  go 26%  |  watch 18%
  play  → basketball 38% | video games 33% | the guitar 14%
  go    → outside 41%    | home 29%        | for a walk 12%
  watch → videos 44%     | movies 22%      | the game 16%
Pick 3 — per branch, 3 ranked closing candidates (each ends the sentence), e.g.:
  play  basketball → with my friends 45% | at the park 30% | after dinner 15%
  go    outside    → until dinner 40%    | with my dog 28% | for a bit 16%
  watch videos     → on my phone 43%     | with my sister 24% | till late 13%
```

**Every pick presents 3 ranked candidate chips** (the core mechanic is "pick from a
ranked list"). Only pick 1 *forks* the eventual ending; picks 2 and 3 are ranked
choices *within* the chosen branch, and all of pick 3's options are valid sentence
closers (the chosen one appends with a period). Total picks per run: **3**. Authored as
a small nested object keyed by path; the sentence is easy to swap later.

## Component behavior

New presentational+stateful component `InferenceLoopTryIt` (no props), rendered inside
`InferenceSection`.

State (`useState`, no persistence):
- `picks` — array of chosen tokens so far (drives both the "So far:" line and which
  candidate list to show next).

Render:
- Wrapped in the deck's `InteractiveBox` (`variant: "try"`, `surface: "mint"`,
  `title: "Be the model"`), with an `ActivityInstruction` ("Tap the next word. Each tap
  is one trip through the journey above.").
- An `InnerCard` containing:
  - **"So far:"** the seed + chosen tokens as a mono string; the most recent token
    briefly emphasized (reuse the amber/`--primary` accent + a short `fadeIn`).
  - **If not complete:** "Pick the next token →" plus the 3 current candidates as
    ranked chips (word + `%`), styled like the Core Loop probability rows (amber bars
    / chips). Tapping appends to `picks`.
  - A sub-label: *"Each pick runs the whole journey again. The model has no plan: it
    only sees the words so far."*
  - After the fork pick: a one-line nudge — *"A different pick here would send the
    sentence somewhere else."*
  - The standard disclaimer line, shown while picking.
  - **If complete:** the picker is replaced by a "THE ANSWER YOU BUILT" eyebrow above
    the finished sentence (no replay control).
- Conclusion (renders once complete): the deck's `Takeaway` component
  (`accent: "var(--tryAccent)"`), headline *"One word, look again, the next."*, body
  *"Each tap ran the whole journey once: score every token, pick one, add it, then look
  again. That's inference, and it's why the model has no fixed plan for where a sentence
  ends. The path you chose is what decided this one."* It sits inside the box, below the
  finished-sentence card, matching the other sequential TRY ITs.

Completion = `picks.length === 3` (depth of the authored data along the chosen path).

## Styling / consistency

- Reuse existing tokens and box components (`InteractiveBox`, `InnerCard`,
  `ActivityInstruction`, `Takeaway`); mono font for the building sentence
  (`var(--mono)`), matching other prediction demos.
- Candidate chips reuse the amber probability palette (`#d97706` / `#fbedd3`) from the
  Core Loop "Same word, different odds" box, so the % reads as the same idea.
- Include the standard disclaimer line ("Simplified demo: real models score every
  token and exact numbers vary by model.").

## Out of scope

- Full branching tree (rejected in favor of hybrid).
- Temperature / sampling controls (that content now lives on the Choose the Model page).
- Any change to gating, the journey diagram, or the ChatGPT-decoded SEE IT.

## Risks

- Mild thematic overlap with the Core Loop's phone-autocomplete prediction beat; this is
  the *deep, interactive* version at the capstone, which is the intended payoff.
- Keep the box compact so it doesn't crowd the page between the diagram and the
  neural-net beat.
