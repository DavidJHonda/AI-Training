# Inference Capstone Diagram — Design

Date: 2026-06-18
Lesson: Inference (`inference`), the closing lesson of the Understand AI section.

## Problem

The Inference lesson opens with `InferenceFlowDiagram`, a compact two-phase box that
"feels weak" and doesn't visibly connect back to everything the Understand AI section
taught. Immediately after it, "The Complete Journey" SEE IT walks the same six steps
again as an interactive reveal, so the same material is taught twice back-to-back.

We want a single, richer, static diagram that acts as the capstone for the whole
section: one glance shows the full journey from prompt to output, the read-all-at-once
vs write-one-at-a-time contrast, and the repeating loop — with each stage tied to the
lesson it came from.

## Decisions (from brainstorming)

- **Replace both** the weak `InferenceFlowDiagram` and the "The Complete Journey"
  6-step reveal with one new diagram.
- **Static** — everything visible at once (no step-through), like the user's sketch.
- **Single pipeline + loop-back arrow** as the structure; the loop is the visual
  centerpiece (not three repeated rows).
- **Lesson-tagged** — each node carries an uppercase chip naming its source lesson.

## Scope of changes in `InferenceSection`

Remove:
- the `InferenceFlowDiagram` call and the `InferenceFlowDiagram` function (no longer used).
- the `steps` array, the "The Complete Journey" `InteractiveBox` + `RevealSequence`,
  its `ActivityCounter`, and the `stagesRevealed` state.

Add:
- a new presentational component `InferenceJourneyDiagram` (no props, no state), rendered
  where the weak box was — after the intro prose, before the
  "At the heart of that journey is a neural network" `SectionKicker`.

Adjust:
- Lead-in prose: keep "Here's the whole shape of a single pass, from your prompt to one
  word of the answer:" as the diagram's intro. The "Step through each stage…" instruction
  disappears with the reveal. The "Now repeat the entire journey" takeaway folds into the
  diagram's loop copy.
- `NextLessonGate`: currently gates on `stagesRevealed >= steps.length && seeStep >= 6`.
  Drop the `stagesRevealed` half so it gates only on the Luke/Nate demo (`seeStep >= 6`).

Untouched: the neural-network section + image, "Same question, different prediction" demo,
embedded Temperature section, "ChatGPT, decoded".

## Component: `InferenceJourneyDiagram`

Pure presentational, no props, no state. Lives next to the other inference helpers in
`index.html`. Built from the existing design tokens so it matches the lesson's current
diagram shell.

### Layout

A faint-purple band (`var(--primaryFaint)`, borderRadius 20, generous padding) holding a
continuous pipeline of six white node-cards joined by primary `→` arrows, with a bold
loop-back arrow returning from the last node to the first.

```
┌─ INFERENCE: ONE TOKEN, START TO FINISH ──────────────────────────────┐
│  ╾─────────────  reads your whole prompt at once  ─────────────╼      │
│  ┌──────────┐  ┌────────┐  ┌────────────┐  ┌──────────────┐           │
│  │CONTEXT   │→ │ TOKENS │→ │ EMBEDDINGS │→ │ LAYERS /     │           │
│  │WINDOW    │  │        │  │            │  │ ATTENTION    │           │
│  └──────────┘  └────────┘  └────────────┘  └──────┬───────┘           │
│       ▲                                           │                   │
│       │   ╾──────  writes one token at a time  ───┼──╼                │
│       │   ┌──────────────┐  ┌──────────────┐  ◀───┘                   │
│       │   │ PROBABILITY  │→ │ PREDICTION   │                          │
│       │   └──────────────┘  └──────┬───────┘                          │
│       └──────◀── ↻ append that token, run it all again ──────◀────────┘
│              until the answer is complete                              │
└───────────────────────────────────────────────────────────────────────┘
```

- **Chips** reuse the step-through's chip tones: encode stages (Context Window, Tokens,
  Embeddings, Layers/Attention) in muted/grey tones; `PROBABILITY` and `PREDICTION` in the
  bright primary tone, marking the "now it answers" pivot — same color logic the removed
  reveal used.
- **Bracket labels** annotate the two spans: "reads your whole prompt at once" over
  Context Window → Layers; "writes one token at a time" over Probability → Prediction.
  These are light annotations on one continuous pipeline, not a hard two-phase split.
- **Loop-back arrow** (`↻`) is the boldest element — primary color, thick — running from
  Prediction back to Context Window, carrying the repeat-until-done message.

### Responsive behavior

- Desktop: two visual rows as drawn (4 encode nodes, then 2 generate nodes), loop arrow
  curving back to the top-left.
- Narrow screens: nodes stack vertically top-to-bottom, `→` arrows become `↓`, and the
  loop-back becomes a labeled "↻ back to the top — until the answer is complete" strip.
- Built with flex-wrap / responsive grid so it degrades without overflow. Exact arrow
  rendering (SVG path vs styled element) is an implementation choice; the loop arrow must
  read clearly at both widths.

### Node copy

| Chip | Title | Description |
|---|---|---|
| CONTEXT WINDOW | What the model sees | Your prompt plus everything else in the window — past messages, custom instructions, saved memory. |
| TOKENS | Text becomes numbers | The whole thing is split into tokens, each mapped to a number. From here on, it's all numbers. |
| EMBEDDINGS | Starting meaning | Each token's number becomes a vector — its starting meaning on the map. |
| LAYERS / ATTENTION | Meaning in context | ~100 layers, reading every token against every other at once, using weights frozen in training. Out comes one final vector per token. |
| PROBABILITY | Score every possible next token | The last token's final vector is compared against all ~100,000 tokens it knows. Closeness becomes a probability. |
| PREDICTION | Pick one token | It picks one — usually a word — and adds it to the answer. |

**Loop-back label:** "↻ Append that token, then run the whole journey again — now over your
prompt plus what it's written so far. Repeat until the answer is complete."

**Bracket labels:** "reads your whole prompt at once" / "writes one token at a time".

## Content-accuracy rationale

These corrections (from the review of the sketch, checked against the lesson's own
"Complete Journey" wording) are baked into the copy:

1. **"Score every possible *next* token"** — not "assigns probability to each token", which
   read as the input tokens. The model scores the ~100,000 candidates in its vocabulary.
2. **Closeness / closest-vector lives in the PROBABILITY (prediction) phase**, not the
   encode phase. The sketch put "finds closest vector" in the reading stage, duplicating the
   probability step.
3. **Token ≠ word** — "picks one — usually a word" keeps the Tokens lesson honest.
4. **The loop has a stop condition** — "until the answer is complete."
5. **Order is tokenize → embed → layers**, with "all at once" attached to Layers/Attention
   (it's a property of attention, not a step before tokenizing).
6. **Training callback** — "weights frozen in training" pulls the Training lesson into the
   capstone alongside Tokens, Embeddings, Layers/Attention, Context Window, Probability,
   Prediction.

The "re-run the whole journey each token" framing is an intentional simplification the
lesson already uses (it omits KV-caching); the diagram keeps it for consistency.

## Styling notes

- Band: `var(--primaryFaint)`, borderRadius 20, padding ~28px/24px, `marginBottom: var(--blockGap)`.
- Node cards: `#fff`, `1.5px solid var(--rule)` (Probability/Prediction may use a primary or
  green accent border to echo the pivot), borderRadius 12, `var(--shadowSoft)`.
- Arrows: `var(--primary)`.
- Chips: reuse the existing `renderChip` tone styles (neutral/muted/bright) from
  `InferenceSection`; extract or mirror that helper so the new component shares it.
- Typography via tokens only (`var(--sans)`); no raw fonts/shadows/colors that would trip
  `design-check.sh`.

## Verification & follow-ups

- `node --check` the inline script after editing (extract the `<script>` block).
- Run `bash design-check.sh` and reconcile any FLAGs before committing.
- Sync docs per project conventions:
  - `briefing.md` — update the Inference lesson notes (weak box + Complete Journey reveal
    replaced by the static `InferenceJourneyDiagram`); add a dated Update line.
  - The component is lesson-specific (like `InferenceFlowDiagram` / `CoreLoopBox`), not a
    shared library component, so a `docs/components` gallery entry is optional — add one only
    if we decide it's reusable.
- This is a structural lesson change, so `briefing.md` must be updated (per the keep-in-sync
  convention).

## Out of scope

- No changes to the "Same question, different prediction" demo, Temperature, or
  ChatGPT-decoded.
- No new interactivity — the diagram is static. (Progressive-highlight interactivity was
  considered and declined.)
