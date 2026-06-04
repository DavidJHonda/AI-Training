# AI Primer — Design

**Date:** 2026-06-04
**Status:** Approved (design); pending implementation plan
**Section affected:** Understand AI

## Problem

Understand AI is the course's largest, densest section (16 lessons). The lesson
order is pedagogically sound — understand the model, then see how it was trained,
then see how it answers — but that ordering forces the section to *mention*
core ideas long before it *defines* them. Two clear examples:

- **Training** is the 13th lesson, yet training is referenced repeatedly before
  it appears, never having been defined.
- **Probability** is fundamental to how AI works but sits 15th (it belongs to the
  "how AI answers" cluster).

You can't build the course without mentioning things not yet covered. Today each
such mention is an unpaid comprehension debt: the student is asked to "hold this,
trust me." Across 16 lessons that debt compounds.

## Idea

Add one new content lesson — the **AI Primer** — early in the section. It installs
a coarse but correct mental model of how AI works, in everyday language, so that
every later mention lands on a frame the student already holds. The Primer gives
the *map*; later lessons give the *territory*.

Crucially, the four ideas it covers are not four separate entries — they are **one
loop**:

> AI learns **patterns** from huge amounts of data (**training**). It uses those
> patterns to judge how **probable** each possible next piece is, and **predicts**
> the most likely one — one piece at a time.

That single sentence is essentially "how AI works." The Primer's job is to install
that loop; every later lesson is a zoom-in on one part of it.

## Decisions (locked during brainstorming)

1. **Form:** one connected loop (a single narrative), not four mini-definitions.
2. **Probability:** folded *fully* into the Primer. The standalone Probability
   lesson (`probability`) is **removed**. Net section count stays **16**.
3. **Title:** displayed **"AI Primer"**, internal id **`primer`**.
4. **Placement:** first content lesson of Understand AI — immediately after the
   Foundations opener (`openerfoundations`), before `howwegothere`.
5. **Depth rule:** everyday language, "what not how." Conceptual-and-plain in the
   Primer; mechanism-and-technical stays in the later lessons.

## Design

### Placement & ordering

- Insert `primer` into the section order array (index.html ~line 1211) directly
  after `openerfoundations`.
- Remove `probability` from that array.
- Resulting Understand AI order:
  `openerfoundations, primer, howwegothere, aivscode, norules, data, aiismath,
  tokens, embeddings, vectorspace, insidethemodel, attention, layers, training,
  prompt, inference`.
- The "How AI builds an answer" cluster becomes **Context Window + Inference**
  (Probability gone).
- Wire `primer` through the existing lesson plumbing (`SECTION_GROUPS` /
  `SECTION_COMPONENTS`, the sections metadata map that defines kicker/label/icon).

### The spine — four beats, one story

Told as one flowing narrative, not four headed entries:

1. **Patterns** — AI works by finding repeated patterns in what it has seen.
   Plain language; the word "weights" does **not** appear (it debuts in Training).
2. **Training** — where those patterns are *learned* and stored, by reading
   enormous amounts of text. *What* it does and *why* it matters only — the gears
   (weights, adjustment) stay in the later Training lesson.
3. **Probability** — given some text, AI scores how likely each possible next
   piece is. This beat carries real weight: it is the fully-folded Probability
   lesson, including its interactive assets (below).
4. **Prediction** — it picks the most probable piece, then repeats, one piece at a
   time, to build a whole answer. The inference mechanism stays in the later
   Inference lesson.

The loop closes the way the old Probability intro did — **training writes the
patterns in; answering reads them back out** — but expressed in plain words, since
"weights" and "token" are not yet available vocabulary at this point in the section.

### Critical constraint: the Primer precedes Tokens and Training

The current Probability lesson leans on later vocabulary ("the model tuned billions
of **weights**… the next **token**"). Because the Primer sits *before* Tokens and
Training, that framing must be **re-expressed in plain language** — "the next word,"
"what it learned" — not copy-pasted. The Primer becomes the place that *plants* the
seeds (patterns, learning, next-piece prediction) that Tokens and Training later
formalize. This is a light rewrite, not a move.

### Activities (inherited from the removed Probability lesson)

Both of Probability's strongest assets carry over, re-expressed without later vocab:

- **SEE IT** — the "See you ___" bar chart (tomorrow / later / soon / …). Reframed
  to "next **word**." Drop or soften the "+ ~99,995 other tokens" line (token-as-a-
  unit is a Tokens-lesson idea) to e.g. "+ thousands of other words."
- **TRY IT** — "Guess the Most Probable Word" (the three phrases: "Once upon a…",
  "She opened her laptop and started…", "I went to the store to buy some…"). Already
  plain-language; carries over largely intact.

Keeping these means the Primer stays interactive and the fold loses nothing good.

### Depth guardrail (the redundancy risk)

The single failure mode is redundancy creep: if the Primer drifts into mechanism,
later lessons feel like reruns and the section grows longer without getting clearer.
The guardrail, applied to every sentence:

> Does the student need this to hold the loop, or is it the mechanism a later lesson
> owns? Loop → in. Gears → out (Probability excepted).

- **In:** what each part does, why it matters, plain-language analogies, the
  "Guess the Most Probable Word" interaction.
- **Out:** weights and how they adjust (→ Training), tokens as a unit (→ Tokens),
  attention / routing (→ Attention), inference-loop mechanics (→ Inference).
- **Register:** everyday language; beats may breathe (a short paragraph plus an
  example each) — *not* one-liners.
- **No false closure:** avoid any "now you understand how AI works" ending — it
  risks a student disengaging from the deeper lessons. Prefer "now you've got the
  shape; the rest of this section opens up each part."

## Scope

**Primary deliverable:** the AI Primer page + removal of the standalone Probability
lesson. That is the build.

**Secondary / follow-up (not in this build):** a light downstream pass shifting a
handful of forward references in earlier lessons from "you'll see this later" to
"you saw this in the Primer." Deferred until the Primer exists — YAGNI until then.

**Out of scope:** reworking any other lesson, re-clustering, or touching the
"How AI builds an answer" cluster beyond removing Probability.

## Done criteria

- `primer` lesson renders, placed after `openerfoundations`, before `howwegothere`.
- Standalone `probability` lesson removed from the order array and section maps.
- Primer teaches the four-beat loop in everyday language, honoring the depth
  guardrail (no "weights"/"token" vocabulary, no mechanism, no false closure).
- SEE IT and TRY IT activities carried over and re-expressed.
- `briefing.md` updated (structural change: new lesson, removed lesson, order array,
  cluster note for "How AI builds an answer").
- Any genuinely-cut Probability content moved to `docs/parking-lot.md`, not
  commented out in index.html.
- `design-check.sh` run and FLAGs reconciled before commit.
