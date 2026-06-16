# `ChoiceQuiz` — Reusable One-Shot Choice Activity — Design

**Date:** 2026-06-16
**Status:** approved, ready for implementation plan
**Origin:** extracted from the "Which One Handles This?" TRY IT in `AIvsCodeSection` (Rules vs Patterns).

## Motivation

The "Which One Handles This?" discrimination quiz was hand-rolled inline. The codebase already
has two shared quiz components, but neither matches this interaction:

- **`QuizBlock`** (15 uses) — self-contained, boxed option tiles, "mint" mode is *try-until-correct*
  (multi-attempt), plus a print mode.
- **`ScenarioRow`** (5 uses) — row layout only (numeral + prompt + caller-supplied option children +
  feedback grid); caller owns state.

Our pattern is a distinct third thing: **one-shot** (pick once, see correct / not-quite, the activity
counts it answered either way) with clean **horizontal radio buttons**. The decision is to extract it as
a new standalone component, `ChoiceQuiz`, and convert the originating activity to use it so there is a
single source of truth (extract-and-dogfood).

This is also the codebase's first shared **radio-style choice control** (no `ChoiceButton`/`RadioOption`
exists today; every `ScenarioRow` caller hand-rolls its option buttons).

## Component: `ChoiceQuiz`

Self-contained. Renders the entire TRY IT box (instruction + numbered rows with radio options + reveal
feedback), owns its answer state, and calls back when every scenario is answered so the lesson can gate.

### Props

```
ChoiceQuiz({
  title,            // InteractiveBox title, e.g. "Which One Handles This?"
  instruction,      // ActivityInstruction text
  scenarios,        // array, see shape below
  surface = "mint", // passthrough to InteractiveBox (try styling)
  onComplete,       // () => void, fired once when all scenarios are answered
})
```

### Scenario / option shape

Generalized to N options, reusing `QuizBlock`'s option vocabulary for codebase consistency:

```
{
  prompt: "You log in to your school's portal …",   // full-width situation text
  options: [
    { label: "Traditional software", correct: true,  headline: "It's a rule.",            feedback: "Your GPA is exact math …" },
    { label: "AI",                    correct: false, headline: "You don't want patterns here.", feedback: "AI could try …" },
  ]
}
```

- Exactly one option has `correct: true`.
- On pick, reveal **the picked option's** `headline` + `feedback`, accented green ("Correct") or red
  ("Not quite"). The eyebrow defaults from `correct` and is overridable per option via `option.eyebrow`.
- Renders N options (two today); they sit in a horizontal, wrapping radio group.

### Behavior

- **One-shot:** pick once per row; feedback reveals immediately. Re-picking is allowed and just updates
  the shown feedback. A row counts as "answered" on any pick, right or wrong.
- **State:** `answers` (`{ rowIndex: optionIndex }`) lives inside `ChoiceQuiz` via `useState` — ephemeral,
  matching today's behavior (no localStorage).
- **Completion:** `ChoiceQuiz` calls `onComplete()` when a pick on a previously-unanswered row brings the
  answered-count to `scenarios.length` (i.e. the transition into "all answered"). The parent's handler
  (`setQuizDone(true)`) is idempotent, so an extra call would be harmless, but fire it on the transition.
  The lesson uses this flag for the gate and any follow-on content (e.g. the KeyInsight).
- **No progress counter.** `ChoiceQuiz` does NOT render an `ActivityCounter`; the `InteractiveBox` `action`
  slot is left empty. (Explicit decision — the "0 of 4" pill is dropped from this component.)

### Look (preserve the tuned styling exactly)

- Row: numeral (`var(--serif)`, 30) + full-width prompt (`var(--sans)`, 16, lineHeight ~1.45), with the
  numeral top-aligned (`alignItems: flex-start`).
- Options: their own line, indented `marginLeft: 46`, `marginTop: 14`; horizontal group
  (`flexDirection: row`, `gap: 28`, `flexWrap: wrap`).
- Radio control (new internal helper): 22px circle (`border: 2px`), 11px inner fill; label 17px / weight
  600; transparent button (no pill background or border); `gap: 10` between dot and label. Selected state
  colors the dot fill + border + label green (`#1f9d5f`) when the picked option is correct, red
  (`#d4334a`) when not. Unselected: `var(--rule)` border, transparent fill, `#0e0a1f` label.
- Feedback (on answered): `marginLeft: 46`, `marginTop: 14`, dashed top rule (`var(--tryRule)`), a
  `1fr 2fr` grid — left: eyebrow dot + "Correct"/"Not quite" (11px uppercase) and headline (20, accent);
  right: feedback text (15, `#0e0a1f`).
- Rows separated by `borderTop: 1px solid var(--rule)` (first row none), inside an `InnerCard`.

These are the exact values currently in `AIvsCodeSection`; the conversion must be visually identical.

### Placement

Define `ChoiceQuiz` (and its internal radio helper) alongside the other shared activity components, near
`ScenarioRow` / `QuizBlock` (index.html ~815–1100).

## Converting "Which One Handles This?"

1. Reshape `FIT_SCENARIOS` from the current `{ situation, correct: "trad", trad:{…}, ai:{…} }` form into
   the new `{ prompt, options: [{label, correct, headline, feedback}, …] }` form (two options each:
   Traditional software / AI, with the existing copy verbatim; mark the right one `correct: true`).
2. Delete the inline `renderOpt`, the row map, and the `ActivityCounter` from `AIvsCodeSection`.
3. Replace the `InteractiveBox(...)` block with:
   ```
   ChoiceQuiz({ title: "Which One Handles This?", instruction: "<existing instruction>", scenarios: FIT_SCENARIOS, onComplete: () => setQuizDone(true) })
   ```
4. Section state: replace `fitAnswers`/`fitAllAnswered` with a single `const [quizDone, setQuizDone] = useState(false)`.
5. Keep the section's own `KeyInsight` (render on `quizDone`), `LessonRule`, and `NextLessonGate`
   (`ready: quizDone`, → `norules`).

Net result: the activity is pixel-identical to today (minus the now-removed counter pill), sourced from
the shared component.

## Out of scope (v1 — noted as future extensions)

- **Stimulus block.** The parked "What Could AI Pull Out?" activity had per-scenario stimuli
  (text / image item-list / audio quote). Not needed for the current reuse; add a `scenario.stimulus`
  slot when a reuse site requires it.
- **Print mode.** `QuizBlock` renders a reveal-all print view; `ChoiceQuiz` will render interactively only.
  The current inline version has no print handling, so this is not a regression — flagged for later.
- **Answer persistence (localStorage).** Ephemeral state matches today.
- **Migrating existing `QuizBlock` / `ScenarioRow` activities.** This spec only adds `ChoiceQuiz` and
  converts the one originating activity; it does not touch the 20 existing quiz usages.

## Verification

- `node --check` on the extracted `AIvsCodeSection` (and the new component) parses.
- `bash design-check.sh` passes. Note the **hand-built counter pills** baseline is currently `4`; removing
  the "Which One Handles This?" counter does not change it (that counter used `ActivityCounter`, not a
  hand-built pill), but re-run to confirm the count is unchanged and reconcile if it shifts.
- Browser walkthrough of Rules vs Patterns: rows render, radios pick + color, feedback reveals, the gate
  enables only after all four are answered, and the KeyInsight appears.

## Follow-ups

- No `briefing.md` change (lesson structure/map unchanged; this is a component refactor).
- No parking-lot entry (no lesson copy cut).
