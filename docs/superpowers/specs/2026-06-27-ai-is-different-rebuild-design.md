# "AI is Different" lesson rebuild — design

**Date:** 2026-06-27
**Lesson:** `aivscode` ("AI is Different"), in *Work With AI*. Component: `AIvsCodeSection`.

## Goal

Reorganize and reframe the existing "AI is Different" lesson around a **Superman
spine** — AI's pattern-learning is its *superpower*, and being hard to control is
its *Kryptonite*. The lesson already absorbed "Harder to Control" (`norules` /
`BlackBoxSection` is rendered embedded at the end today); this rebuild dissolves
that embed into the new flow and merges the lesson's two TRY ITs into one
two-part TRY IT.

This is a **reorder + reframe, keeping good copy** (approach "A") — not a
from-scratch rewrite. Most beats already exist; we move them into the new order,
write the new connective/framing copy, and keep strong existing copy as-is.

## Decisions (settled with David)

- **Prose:** Approach A — reorder + reframe; keep good existing copy, write new
  connective/framing copy from David's outline.
- **Combined TRY IT:** Approach B — Part II reveals only after Part I is fully
  answered. Within each part, all questions show at once.
- **Part II count:** keep all **5** `RULE_PATTERN_SCENARIOS` (David's outline said
  "4"; keeping 5 unless he trims later).
- **Row 7 box:** reuse the existing `CompareHead` box (it already contrasts a
  structured table vs. unstructured/multimodal input), moved under the new
  STRUCTURED VS UNSTRUCTURED kicker and re-led with the messy-legal-pad framing.
- **Row 8 illustration:** `illustrations/rules-vs-patterns.jpg` — already rendered
  in this section; it just moves under the SUPERPOWERS kicker.

## New lesson structure (top to bottom)

| # | Beat | Source / action |
|---|------|-----------------|
| 1 | **Intro** — "AI is taking the world by storm… it has superpowers no other program has. In this lesson you'll learn those superpowers and how they exist." Then: best way to understand is to compare AI to non-AI software (calculator, Excel) = **"Traditional Software"**. | 🆕 David's copy |
| 2 | **Traditional software = rules** — a programmer writes code line-by-line; the essential idea is IF-THEN-ELSE. Password example (IF password matches → open app; ELSE "password not found"). "Traditional software is based on RULES." | ✏️ adapt existing |
| 3 | **AI is different** — "You've already seen this" → show **LEARN ONCE / ANSWER EVERY WORD** box. "AI isn't based on rules, it's based on learned patterns." | ♻️ `CoreLoopBox` (reused from *How an LLM Works*) |
| 4 | **Cooking analogy** — traditional software = a recipe (someone wrote every step, same dish every time); AI = a chef (learned by cooking thousands of dishes, can handle a new one). | ♻️ exists ~verbatim; keep |
| 5 | "That difference shows up everywhere — how each solves a problem, reaches an answer, fails, and whether you can even trace why." | 🆕 connective |
| 6 | Kicker **RULES VS PATTERNS** → "What's the best game for my new PS5?" (traditional returns a preset list; AI builds each answer from patterns) → **Fixed Rules vs. Built From Patterns** box. | ♻️ existing PS5 box (with its reveal + "Same question. Different games." Takeaway) |
| 7 | Kicker **STRUCTURED VS UNSTRUCTURED DATA** → messy-legal-pad framing ("we sketched messy notes… Excel needs rows and columns; AI takes the mess and returns what we ask") → **2nd Traditional-vs-AI box**. | 🆕 lead copy; ♻️ the existing `CompareHead` box moved here, re-led |
| 8 | Kicker **AI's SUPERPOWERS** → Superman framing (flying, stopping a train; traditional software = the ordinary person, can only do what a human wrote; AI's superpower = no human wrote its abilities) → **illustration**. | ✏️ expand existing superpower line; ♻️ `rules-vs-patterns.jpg` |
| 9 | Kicker **AI's KRYPTONITE** → Kryptonite framing (not fatal, but be aware) → "AI runs on patterns it learned, not rules someone wrote → harder to predict, inspect, lock down; no one can fully predict it" + "failures aren't AI breaking rules; no one wrote a rule for every situation" → **"You'll see stories like this"** box. | 🆕 Kryptonite lead; ♻️ harder-to-control prose + stories box from `BlackBoxSection` |
| 10 | Kicker **THE INDUSTRY'S ANSWER: GUARDRAILS** → companies can't rewrite learned behavior by hand, so they wrap a safety layer = a **guardrail** (blocks/redirects/limits specific behaviors; can be programs, filters, classifiers, safety-tuned behaviors → catches some, misses others). | ♻️ guardrails prose from `BlackBoxSection` |
| 11 | **KeyInsight** (above the TRY IT). | ✏️ adapt existing |
| 12 | **Combined two-part TRY IT** (see below). | 🆕 build |
| 13 | LessonRule + Next → **What AI Does Best** (`whatitdoesbest`). | unchanged |

## Combined TRY IT (Row 12)

One `InteractiveBox` (variant `try`, surface `mint`). David wants each part's
title kept inside the box as a part header.

- **Part I — "Which One Handles This?"** — all 4 `FIT_SCENARIOS` shown at once,
  using the existing pill rendering (inlined from `ChoiceQuiz`, since `ChoiceQuiz`
  is itself an `InteractiveBox` wrapper and can't be nested). Track `part1Answers`
  (map).
- **Reveal gate:** once all 4 of Part I are answered, **Part II fades in below.**
- **Part II — "Which would have stopped it?"** — all 5 `RULE_PATTERN_SCENARIOS`
  shown at once, using the `QuizBlock`-per-scenario rendering (the parallel shell
  built 2026-06-27). Track `part2Answers` (map).
- **Dual Takeaway pattern** (per the 2026-06-27 convention):
  - KeyInsight **above** the box (Row 11), un-gated — video-safe.
  - One gated `Takeaway` **below** the box, shown once Part II is fully answered,
    tying both halves together: superpower = builds from patterns; Kryptonite =
    can't be fully controlled; guardrails = the bolted-on partial fix.
- **NextLessonGate `ready`:** Part II all answered
  (`Object.keys(part2Answers).length >= RULE_PATTERN_SCENARIOS.length`).

## Components / data reused

- `CoreLoopBox` — the LEARN ONCE / ANSWER EVERY WORD box (Row 3).
- `CompareHead` box — moved to Row 7, re-led.
- `Fixed Rules vs. Built From Patterns` ShowcaseBox — Row 6, kept.
- `rules-vs-patterns.jpg` — Row 8.
- `FIT_SCENARIOS` (4) → Part I; `RULE_PATTERN_SCENARIOS` (5) → Part II.
- Guardrails prose + "stories like this" ShowcaseBox — from `BlackBoxSection`,
  Rows 9–10.

## Cleanup / structural changes

- Rewrite `AIvsCodeSection`'s render in the new order.
- **Stop embedding `BlackBoxSection`.** Move the content it currently supplies
  (harder-to-control prose, "stories like this" box, guardrails prose, and the
  `RULE_PATTERN_SCENARIOS` data) into `AIvsCodeSection` (or shared module scope).
  After this, `BlackBoxSection` is unused → delete it, and remove the now-dead
  `norules` `SECTION_META` entry if nothing else references it.
- Remove the standalone `ChoiceQuiz` "Which One Handles This?" call and the
  standalone "Rule, Pattern, or Guardrail?" TRY IT; their data arrays now feed
  the combined TRY IT.
- Keep `norules` out of nav (already the case).

## Verification

- `?print=all` loads with **0 JS errors** (CDP console check, the method used for
  the 2026-06-27 TRY IT conversions).
- Combined TRY IT: Part II hidden until Part I's 4 are answered; gate unlocks on
  Part II's 5; gated Takeaway appears on completion.
- Lesson reads top-to-bottom in the new order; TRY IT is the last content block.

## Open / deferred

- Part II at 5 vs. 4 — keeping 5; David may trim.
- KeyInsight (Row 11) and the combined Takeaway exact wording — drafted during
  implementation, flagged for David's copy pass.
- The Group B TRY IT conversions (What's Real What's Made Up, Redact the Prompt)
  remain paused on a separate feedback-layout decision — out of scope here.
