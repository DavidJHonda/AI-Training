# SEE IT elimination — locked plan

**Date:** 2026-06-19. **Step 1 (decisions) LOCKED** with David, box by box.
Goal: zero `InteractiveBox variant:"see"` in `index.html`. Each SEE IT becomes a
TRY IT (flagged for the deferred capstone pass), a static box, or is deleted.

## Rules that drove the calls

- **One TRY IT (capstone) per lesson.** If a lesson already has a TRY IT, its SEE IT
  goes **static**. A SEE IT only becomes the TRY IT when the lesson has no activity
  (or the SEE IT is clearly stronger and should supersede a weak existing TRY IT).
- **Static aids can be many per lesson** — only the capstone activity is limited.
- **TRY-IT conversions are authored in the deferred capstone pass, not now.** This
  pass converts reveal-only boxes to static and *flags* the TRY-IT candidates.
- Every static conversion **drops the reveal/stepping interaction** and **rewords
  prose** that names "SEE IT".

## Disposition table (23 live boxes)

| Line | Lesson | Title | Decision |
|---|---|---|---|
| 1984 | llms | Two kinds of AI, one task | **static** |
| 1993 | llms | What's an LLM? (click each letter) | **static** |
| 2433 | howwegothere | Build the machine | **→ TRY IT** (flag) |
| 2653 | howmuchtocheck | How Much to Check | **static** (lesson has a TRY IT) |
| 3611 | aivscode | Fixed Rules vs. Built From Patterns | **static** |
| 4581 | training | Watch It Happen | **static** |
| 5368 | layers | Watch Meaning Build Layer by Layer | **→ TRY IT** (flag) |
| 5603 | inference | ChatGPT, decoded | **static** |
| 5925 | prompt | Same question, different prediction | **static** |
| 6151 | customization | What goes in the context window | **DELETE** (later: replace w/ Context Window illustration) |
| 6555 | documenttrap | How Chunks Get Picked | **static** |
| 6758 | modelselection | Three theories of AI | **static** — merge w/ 6835 |
| 6835 | modelselection | Three kinds of strength | **static** — merge into one compare card |
| 7551 | verify | Verification Strategies | **→ TRY IT** (flag) |
| 7852 | critical | The 5 Habits | **static** (lesson has 2 TRY ITs) |
| 8499 | prompting | Bad Prompt, Better Prompt | **static** |
| 8571 | prompting | The 8 Qualities | **static** |
| 8790 | thoughtpartner | Thinking Together | **static + flag as future TRY IT** (supersedes the lesson's current weaker TRY IT) |
| 9219 | evaluating | The Good Enough Checklist | **→ TRY IT** (flag) |
| 9301 | evaluating | Prompt → Evaluate → Refine | **static** |
| 10919 | privacy | The Whole Photo | **static** (lesson has a TRY IT) |
| 13256 | computecost | What one answer costs | **static** |
| 13332 | aifuture | Why Smart Predictions Fail | **→ TRY IT** (flag) |

## Flags for the deferred capstone-authoring pass

**SEE IT → rework into the lesson's TRY IT (6):**
`howwegothere` (Build the machine), `layers` (Watch Meaning Build), `verify`
(Verification Strategies), `evaluating` (Good Enough Checklist), `aifuture` (Why
Smart Predictions Fail), and `thoughtpartner` (Thinking Together — *supersedes* the
existing weaker TRY IT).

**Lessons left with NO activity → author a brand-new capstone (6):**
`llms`, `aivscode`, `training`, `inference`, `prompt`, `computecost`.

## Dead-function sweep (delete all 10; verify-before-delete)

Confirmed defined-but-never-rendered (referenced once = definition only, inactive
sectionId). Two carry SEE ITs; all 10 to be removed as hygiene. **Verify each is
absent from any sectionId→component registry before deleting.**

`OpenerInsideSection` (has SEE IT), `OpenerAnswersSection` (has SEE IT),
`BehindTheNumbersSection`, `YouAlreadyUseSection`, `WhenNotSection`,
`OpenerJudgmentSection`, `DataSection`, `OpenerTrapsSection`, `OpenerUsingSection`,
`StakeholdersSection`.

**Do NOT blind-delete** (referenced >1 / shared): `OpenerSection` (live, shared by
all openers), `VectorSpaceSection`, `TemperatureSection` — inspect separately.

## Prose & meta cleanup (alongside conversions)

- Reword prose naming "SEE IT": ~lines 1982, 2331/2333, 2651/2657, 3609, 5364
  ("In this SEE IT…"), 6149 ("This SEE IT shows…").
- **Welcome "how lessons work"** (PATTERNS data ~2763–2791 + copy ~2887–2890,
  "complete the TRY IT and SEE IT activities to move on"): remove the SEE IT card,
  reword once the variant is gone.

## Decommission (final, after zero `variant:"see"` remain)

Remove the `see` branch from `InteractiveBox`, the `seeBand`/`seeAccent` tokens, the
SEE IT CSS band (~line 35), and the typography comment (~line 154).

## Reusable components for static conversions

- **`DecodeCards`** (`headline`, `items: [{badge, label, color, bg, desc}]`) — the
  "decode a term into parts" format (lavender band → white card → tinted letter
  tiles). Built for `llms` "What's an LLM?"; **reuse for `inference` "ChatGPT,
  decoded"** (C/G/P/T) and any similar acronym box.
- Default static treatment for other reveals: `ShowcaseBox` (lavender band +
  optional headline) with the content rendered in its fully-revealed end state.

## Status (updated 2026-06-19)

**All planned static conversions DONE** (`variant:"see"` 25 → 9). Converted/handled:
llms×2, inference, prompting×2, howmuchtocheck, critical, documenttrap, privacy,
computecost, training, evaluating "Refine", aivscode → static; modelselection×2 →
merged into one card; customization → deleted. Gate fixes where reveal-state fed the
NextLessonGate: llms, critical, privacy, evaluating.

**Remaining 9 `variant:"see"`** — none are "convert to static" anymore:
- **Capstone-pass reworks (7):** `prompt`, `thoughtpartner` (flagged to *become* TRY
  ITs) + the 5 flagged TRY-IT candidates (`howwegothere`, `layers`, `verify`,
  `evaluating` "Checklist", `aifuture`). Left as SEE ITs until authored into TRY ITs.
- **Orphans (2):** `OpenerInsideSection`, `OpenerAnswersSection` — remove in the
  dead-function sweep (10 dead functions total).
- Then the **variant decommission** (after the capstone pass clears the last `see`).

## Execution order (Step 2)

1. Per-lesson static conversions + prose fixes (small commits per lesson/batch).
2. Delete box 6151 (`customization`).
3. Dead-function sweep (verify, then delete the 10).
4. Decommission the `see` variant + tokens.
5. Verify throughout: `validate()`, `design-check.sh`, browser spot-check.
