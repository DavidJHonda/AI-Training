# Back-Half Design Consistency — Design Spec

**Date:** 2026-07-14
**File touched:** `index.html` (single-file React app, `React.createElement`, no JSX)
**Goal:** Make the lessons in the 2nd half of the course (Avoid Traps, Embrace the Future, Build Your Skills, Finish Smarter) visually and structurally consistent with the polished first 3 sections (Start Smarter, Work With AI, Understand AI).

## Approach

The 2nd half already mostly follows the first-3 lesson skeleton. Inconsistency is concentrated in three places:

1. **`closeBoard` is missing from all 28 back-half lessons** (present in nearly every first-3 lesson).
2. **A handful of bespoke inline visuals** are hand-rolled repeatedly instead of reusing a shared component — and the same patterns recur in both halves.
3. **Six outlier lessons** carry teaching on load-bearing bespoke UI.

Strategy (confirmed with the user):
- **Extract a shared component kit first**, built to reproduce the existing first-3 inline styling *exactly*.
- **Do not touch the finished first-3 lessons.** Components are built to match their look; the first-3 lessons are not refactored (zero regression risk to signed-off work).
- **Adopt the kit + add `closeBoard`s across the 2nd half.**
- **`closeBoard` copy is drafted for the user to review** (it's content, not chrome).

## The canonical lesson skeleton (reference)

```
LessonHeader{sectionId}                     (kicker + serif H1 + optional WatchOverview pill)
→ intro BodyP(s), often ending on a bold thesis
→ teaching blocks ×N: SectionKicker → BodyP → visual block → optional KeyInsight/KeyTerm
→ closeBoard(sectionId)                      (dark pill + tilted yellow sticky parting line)
→ activity (InteractiveBox mint + ScenarioRow/QuizBlock, OR bespoke *TryIt, OR lab/teal)
→ LessonRule
→ NextLessonGate{onClick,label}
```

Verified placement: `closeBoard` sits **after teaching content, immediately before the activity.**

## Component 1 — `Callout`

**Purpose:** Consolidate the repeated `--info-bg` note box and amber warning/rule boxes.

**API:** `Callout({ tone, children, marginTop?, marginBottom? })`
- `tone: "info"` (default) → 💡, `background: var(--info-bg)`, `border: 1px solid var(--info)`
- `tone: "warn"` → ⚠️, amber (`#fef3c7` bg, amber border) — matches Support "THE ONE RULE" / DocumentChat "ALSO IN THE RULEBOOK"
- `tone: "rule"` → emphatic single-rule variant (amber, bolder label)

**Base style (reproduce exactly):** `borderRadius: 10, padding: 16, fontSize: BOX_TEXT, color: var(--ink), lineHeight: 1.6, marginTop/Bottom: 18`. Leading emoji is rendered by the component; caller passes only the text/children.

**Adopt at:** ChoosingModel (info), MindTrap (info), Engagement (info), WhenAIActs (info), Flattery (info), SupportTrap (warn/rule), DocumentChat (warn).

## Component 2 — `IconCardGrid`

**Purpose:** The single most-repeated inline pattern — an auto-fit grid of emoji + title + body mini-cards.

**API:** `IconCardGrid({ cards, minWidth? })` where `cards = [{ icon, title, body, color? }]`
- Renders `display: grid; gridTemplateColumns: repeat(auto-fit, minmax(minWidth||200px, 1fr)); gap: 12`.
- Each card: white/tinted `InnerCard`-style surface, emoji, bold title (optional `color`), muted body line.

**Reproduces:** WhatItDoesBest four-engines / WhyDeeper everyday-AI / Evaluating next-moves grids (first-3 look).

**Adopt at:** MindTrap 3-up row, Flattery 3-up row, Engagement 3-up row, CreativeThinking roles, HumanEdge skills grid, WorkChanges job-card grids, Hallucination 2-col.

## Component 3 — `StatusCards`

**Purpose:** The red/amber/green "traffic-light" card stack, plus its 2-panel red/green compare variant.

**API:** `StatusCards({ items, layout? })` where `items = [{ tone: "stop"|"caution"|"go", label, body }]`
- Palette (reproduce exactly): stop `#fef2f2`/`#fca5a5`, caution `#fffbeb`/`#fcd34d`, go `#ecfdf5`/`#86efac`.
- `layout: "stack"` (default, vertical) or `"cols"` (side-by-side compare, typically 2 items).

**Adopt at:** Integrity traffic-light stacks, Privacy data-sensitivity cards, Flattery sycophantic-vs-honest (2-col), WhenAIActs READ/WRITE (2-col), HumanEdge (2-col compare).

## Component 4 — `LabeledCardStack`

**Purpose:** The colored `borderLeft` "Label N·" card stack.

**API:** `LabeledCardStack({ items, accent? })` where `items = [{ label, body }]`
- Vertical stack of cards, each with a colored left border and a bold "Label N·" lead.
- `accent` sets the border color (default `var(--primary)`).

**Adopt at:** WhenAIJudges (Mode 1·/2·/3· stack + Role 1·–4· stack), SyntheticMedia (Check 1·/2·/3· stack).

## Component 5 — `DefinitionCard`

**Purpose:** The "📖 two related words" / "📖 the word" definition card used in trap lessons.

**API:** `DefinitionCard({ icon?, title, terms })` where `terms = [{ term, definition }]` (or `children` for freeform).
- Default icon 📖. Renders the card chrome with the term(s) + definition(s).

**Adopt at:** MindTrap ("Two related words"), Engagement ("The word").

## Component 6 — `Chip`

**Purpose:** The ~15 inline rounded-999 presentational pills (example tags, category labels).

**API:** `Chip({ children, tone?, bg?, color? })`
- `borderRadius: 999, padding: "6px 14px", fontSize: 13, fontWeight: 700`.
- `tone` provides a few named color pairs; `bg`/`color` allow explicit override.

**Adopt at:** low-visibility, opportunistic — swap inline pills as lessons are touched; not a forcing function.

## Component 7 — `Eyebrow`

**Purpose:** The ~40 inline in-card uppercase micro-labels (distinct from the large purple `SectionKicker`).

**API:** `Eyebrow({ children, color? })`
- `fontSize: 12, fontWeight: 800, textTransform: uppercase, letterSpacing: 0.1em, color: color||var(--inkMuted)`.

**Adopt at:** opportunistic — swap inline eyebrows as lessons are touched.

## `closeBoard` rollout

Add a `{ pill, sticky }` entry to `CLOSE_BOARDS` and a `closeBoard("<id>")` call (before the activity) for the **26 back-half teaching lessons**. The 3 openers (`openerprotect`, `openerrealworld`, `openerskills`) already inherit `closeBoard` via `OpenerSection` — verify their `CLOSE_BOARDS` entries exist and add if missing.

Voice: terse two-line parting statement matching existing entries (pill = the claim, sticky = the twist). Drafted for user review.

**Target ids:**
- Avoid: `hallucination`, `trainingbias`, `documenttrap`, `mindtrap`, `flattery`, `engagementtrap`, `supporttrap`, `faketrap`
- Embrace: `workchanges`, `agents`, `aijudges`, `computecost`, `aifuture`, `talkingai`
- Build: `choosemodel`, `askai`, `thoughtpartner`, `humanedge`, `creativethinking`, `becurious`, `buildedge`
- Finish: `whatyoulearned`, `integrity`, `privacy`, `fullworkflow`, `howwegothere`

**Judgment calls (flag individually, may skip):** `whatyoulearned` (recap ending on a trophy hero) and `fullworkflow` (capstone) — a parting sticky may not suit them.

## The 6 outliers (lighter, case-by-case)

Keep their load-bearing bespoke interactive UI; adopt the kit only for their **static panels**, and add a `closeBoard` where it fits:
- **Privacy** — custom SVG photo + redaction game stay; adopt `StatusCards` for data-sensitivity cards.
- **Integrity** — bespoke verdict quiz stays; adopt `StatusCards` for traffic-light/disclosure walls.
- **WhatYouLearned** — recap with no activity; kit for concept cards; closeBoard is a judgment call.
- **FullWorkflow** — drag-drop stays; closeBoard is a judgment call.
- **WhenAIJudges** — adopt `LabeledCardStack` for Mode/Role walls.
- **AIFuture** — keep bespoke flow diagrams; adopt `Callout` for the terms panel.

## Sequencing

1. **Build the 7 components** (no lesson touched). Verify: `validate()` clean, serve over http, `design-check.sh`.
2. **Roll out component swaps** across the ~20 minor-drift lessons, a few at a time, re-verifying each batch.
3. **Add `closeBoard` entries + calls**; user reviews drafted copy.
4. **Outliers** last.

Throughout: **first-3 sections stay untouched.**

## Verification (per `reference_verifying_index_html`)

- Run the in-file `validate()` (SECTION_GROUPS / SECTION_COMPONENTS integrity) — must stay clean.
- Serve over http (not file://) and load each touched lesson.
- Run `design-check.sh`.
- Full-chain trace on any lesson whose structure changed.
- Confirm the red-nav "incomplete" flag still renders (unrelated but in the same nav area).

## Out of scope

- No content rewrites beyond the drafted `closeBoard` lines.
- No changes to first-3 lessons.
- No new lessons, no resequencing.
- Video/PDF re-export (a separate pipeline) — note which lessons changed so assets can be re-exported later if needed.
