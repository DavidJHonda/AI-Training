# Merge "Rules vs Patterns" + "Mess to Meaning" Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fold the `data` (Mess to Meaning) lesson into `aivscode` (Rules vs Patterns) as one lesson, keep `norules` (Harder to Control) standalone after it, and rewire navigation/registries so Understand AI goes 15 → 14 lessons.

**Architecture:** Single-file inline-React app (`index.html`). `AIvsCodeSection` absorbs `DataSection`'s Act-4/Act-5 JSX (bridge prose, structured-vs-messy CompareBox, "What Could AI Pull Out?" TRY IT, KeyInsight). `DataSection` is **moved out of**, not copied — its body is gutted to a dead stub so design-check counts and code aren't duplicated. The `data` id is removed from `SECTION_GROUPS` / `SECTION_META` / `SECTION_COMPONENTS`; the one glossary term sourced to `data` repoints to `aivscode`; `norules`'s gate retargets `aiismath`.

**Tech Stack:** HTML + inline React via Babel (no build, no test runner). Verification = `bash design-check.sh`, targeted `grep`, and manual browser check.

**Reference (current line numbers, pre-edit — re-confirm before editing, the file shifts as you go):**
- `AIvsCodeSection`: 3354–3525. Its TRY IT #1 ("Which One Handles This?") ends at line 3521 `)))`; `LessonRule` at 3522; gate at 3523 (`ready: fitAllAnswered` → `norules`).
- `TypingAICard` helper: 3526–3577 (used by aivscode SEE IT; **do not touch**).
- `BlackBoxSection` (`norules`) gate: 3693 (`completeAndNavigate("data")`, label "Next: Mess to Meaning").
- `DataSection`: 3695–3800. Blocks: opener prose 3700–3705; CompareBox 3706–3717; ShowcaseBox "The move, step by step" 3718–3737; TRY IT #2 "What Could AI Pull Out?" 3738–3795; KeyInsight 3796; LessonRule 3797; gate 3798 (→ `aiismath`).
- `SECTION_GROUPS` Understand AI sections array: line 1309.
- `SECTION_META`: `data` at 1342, `aivscode` at 1340, `aiismath` at 1338.
- `SECTION_COMPONENTS`: `data: DataSection` near line 13660.
- Glossary "Unstructured Data" term `source: "data"`: line 326.

---

### Task 1: Move DataSection's content into AIvsCodeSection

**Files:**
- Modify: `index.html` (`AIvsCodeSection`, ~3354–3525)

- [ ] **Step 1: Add the fuel-activity state to AIvsCodeSection**

At the top of `AIvsCodeSection`, immediately after the existing line:

```js
  const [fitAnswers, setFitAnswers] = useState({});
```

add:

```js
  const [fuelAnswers, setFuelAnswers] = useState({});
```

- [ ] **Step 2: Add the fuelAllAnswered derived flag**

`AIvsCodeSection` already computes `var fitAllAnswered = Object.keys(fitAnswers).length >= FIT_SCENARIOS.length;` just before its `return`. Immediately after that line add:

```js
  var fuelAllAnswered = Object.keys(fuelAnswers).length >= 3;
```

- [ ] **Step 3: Insert the merged Act 4 / Act 5 blocks before the closing LessonRule**

Find the end of TRY IT #1 in `AIvsCodeSection` — the line that closes the "Which One Handles This?" `InteractiveBox` (currently line 3521, three close-parens `)))` ), directly followed by:

```js
    /*#__PURE__*/React.createElement(LessonRule, null),
```

Insert the following **between** that `)))` and the `LessonRule` line. Two prose blocks are NEW copy; the CompareBox, the TRY IT #2, and the KeyInsight are **moved verbatim** from `DataSection` (cut them from there in Task 2).

NEW bridge prose (replaces `DataSection`'s redundant "AI runs on patterns, not rules…" opener; no em-dashes, course style):

```js
    /*#__PURE__*/React.createElement(BodyP, null,
      "Look back at the two jobs AI handled in that exercise: turning a rambling voice memo into a clean list, and flagging a scam text nobody had seen before. Neither arrived in neat fields, and nobody wrote a rule for them. That is exactly AI’s edge. It takes the messy, unfamiliar input that rules choke on and pulls something usable out."
    ),
```

KEPT prose (move verbatim from `DataSection` line 3703–3705):

```js
    /*#__PURE__*/React.createElement(BodyP, null,
      "It can do this because it learned from the messy stuff humans actually produce: conversations, images, audio, video, emails, code, reviews, and notes. So new mess looks familiar."
    ),
```

Then the **CompareBox** (move verbatim from `DataSection` 3706–3717: the `CompareBox` with "Needs structure first" / "Learns from messy data" panels — the structured-vs-unstructured visual we are keeping).

Then the **TRY IT #2** `InteractiveBox` "What Could AI Pull Out?" (move verbatim from `DataSection` 3738–3795, the block beginning `React.createElement(InteractiveBox, { variant: "try", surface: "mint", title: "What Could AI Pull Out?", ... })` through its closing `)))`).

Then the **KeyInsight** (move verbatim from `DataSection` 3796, the `fuelAllAnswered ? React.createElement(KeyInsight, { lead: "It restructures; it doesn’t invent." }, …) : null` expression).

> **Do NOT** move `DataSection`'s opener paragraph (3700–3702) or the "The move, step by step" ShowcaseBox (3718–3737). The opener is replaced by the bridge prose above; the ShowcaseBox is cut (per spec — the TRY IT teaches the same send→match→return loop by doing it).

- [ ] **Step 4: Update the lesson's final gate to require both activities**

Change the existing gate line (currently 3523):

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: fitAllAnswered, onClick: () => props.completeAndNavigate && props.completeAndNavigate("norules"), label: "Next: Harder to Control" })
```

to:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: fitAllAnswered && fuelAllAnswered, onClick: () => props.completeAndNavigate && props.completeAndNavigate("norules"), label: "Next: Harder to Control" })
```

- [ ] **Step 5: Verify the file still parses (no syntax errors)**

Run: `node --check index.html 2>&1 | head -5 || true`
Note: `node --check` will reject the HTML wrapper, so instead grep-verify the moved markers landed once in the new home. Run:

```bash
grep -c 'title: "What Could AI Pull Out?"' index.html
grep -c 'lead: "It restructures' index.html
```
Expected: `1` and `1` (the blocks now live in `AIvsCodeSection`; you will remove the originals from `DataSection` in Task 2, so during this step it may briefly read `2` if you copied instead of cut — if so, finish the cut in Task 2 and it returns to `1`).

---

### Task 2: Gut DataSection to a dead stub

**Files:**
- Modify: `index.html` (`DataSection`, ~3695–3800)

- [ ] **Step 1: Replace the entire DataSection body with a stub**

Replace the whole function `DataSection(props) { … }` (everything from `function DataSection(props) {` through its closing `}` before `function HowAIReadsSection`) with:

```js
function DataSection(props) {
  // Merged into AIvsCodeSection (Rules vs Patterns) on 2026-06-15. Kept as dead code
  // per house pattern; removed from SECTION_GROUPS/SECTION_META/SECTION_COMPONENTS.
  return null;
}
```

- [ ] **Step 2: Confirm the moved content now exists exactly once**

Run:

```bash
grep -c 'title: "What Could AI Pull Out?"' index.html
grep -c 'eyebrow: "Traditional software", title: "Needs structure first"' index.html
grep -c 'lead: "It restructures' index.html
```
Expected: `1`, `1`, `1` (each block lives only in `AIvsCodeSection` now).

- [ ] **Step 3: Commit the content move**

```bash
git add index.html
git commit -m "Merge Mess to Meaning into Rules vs Patterns; gut DataSection to dead stub"
```

---

### Task 3: Remove `data` from the registries and rewire `norules`

**Files:**
- Modify: `index.html` (lines 1309, 1342, ~13660, 3693, 326)

- [ ] **Step 1: Drop `data` from SECTION_GROUPS**

On line 1309, in the Understand AI `sections` array, remove the `"data"` element. The array goes from:

```js
  sections: ["openerfoundations", "howwegothere", "aivscode", "norules", "data", "aiismath", "tokens", "embeddings", "vectorspace", "insidethemodel", "attention", "layers", "training", "prompt", "inference"]
```
to:
```js
  sections: ["openerfoundations", "howwegothere", "aivscode", "norules", "aiismath", "tokens", "embeddings", "vectorspace", "insidethemodel", "attention", "layers", "training", "prompt", "inference"]
```

- [ ] **Step 2: Remove the `data` SECTION_META entry**

Delete line 1342 entirely:

```js
  data: { kicker: "IT READS THE MESS HUMANS MAKE", label: "Mess to Meaning", icon: "🧩" },
```

- [ ] **Step 3: Remove the `data` SECTION_COMPONENTS entry**

Delete the `data: DataSection,` line (near 13660):

```js
  data: DataSection,
```

- [ ] **Step 4: Retarget the `norules` gate to `aiismath`**

In `BlackBoxSection`, change the gate (line 3693) from:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: scenarioIdx >= RULE_PATTERN_SCENARIOS.length, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("data"); }, label: "Next: Mess to Meaning" }));
```
to:
```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: scenarioIdx >= RULE_PATTERN_SCENARIOS.length, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("aiismath"); }, label: "Next: AI is Math" }));
```

- [ ] **Step 5: Repoint the "Unstructured Data" glossary term to `aivscode`**

On line 326, change `source: "data"` to `source: "aivscode"`:

```js
  { term: "Unstructured Data", definition: "Information that doesn't fit neatly into rows and columns: conversations, images, audio, video, reviews, jokes. Traditional code can't make sense of it. AI was trained on it.", source: "aivscode" }
```

- [ ] **Step 6: Confirm no dangling references to the `data` lesson id remain**

Run:

```bash
grep -n 'completeAndNavigate("data")' index.html || echo "no nav to data — good"
grep -n 'source: "data"' index.html || echo "no glossary source data — good"
grep -n 'data: DataSection' index.html || echo "no SECTION_COMPONENTS data key — good"
grep -n 'data: { kicker' index.html || echo "no SECTION_META data key — good"
grep -n 'sectionId: "data"' index.html || echo "no LessonHeader for data — good"
```
Expected: every line prints its "good" message. If `sectionId: "data"` prints a hit, the gutted `DataSection` stub still contains old JSX — redo Task 2 Step 1. (Note: do not grep bare `"data"` — it appears legitimately in copy like "training data" and "structured data".)

- [ ] **Step 7: Commit the rewiring**

```bash
git add index.html
git commit -m "Drop data from registries; rewire norules -> aiismath; repoint glossary"
```

---

### Task 4: Design-check and manual verification

**Files:** none (verification only)

- [ ] **Step 1: Run the design consistency check**

Run: `bash design-check.sh`
Expected: `PASS - no new drift against baselines.` In particular `em-dashes in copy` must stay `OK ... 7` (the new bridge prose uses no em-dashes). If any line FLAGs, reconcile it before continuing (a FLAG here would mean the move duplicated counted content — re-check Task 2).

- [ ] **Step 2: Open the app and verify the merged lesson**

Open `index.html` in a browser (or use the `run` skill). Navigate to **Rules vs Patterns** and confirm, top to bottom:
- Header reads "Rules vs Patterns"; section badge reflects **14** total Understand AI lessons (Rules vs Patterns is 3rd).
- Chef/recipe analogy + first CompareBox (behavior) render.
- SEE IT "Fixed Rules vs Built From Patterns" (PS5) works: reveal traditional, then AI types, "Ask Again" cycles.
- TRY IT #1 "Which One Handles This?" answers + feedback work.
- Bridge prose references the voice memo + scam, then the structured-vs-messy CompareBox (grade table vs Text/Images/Audio/Video/Documents) renders.
- TRY IT #2 "What Could AI Pull Out?" answers + feedback work.
- KeyInsight "It restructures; it doesn’t invent." shows after TRY IT #2 is complete.
- The **Next: Harder to Control** button is disabled until **both** TRY ITs are fully answered, then enabled.

- [ ] **Step 3: Verify navigation chain**

- From Rules vs Patterns, click **Next: Harder to Control** → lands on `norules`.
- On Harder to Control, complete it and confirm its button now reads **Next: AI is Math** and lands on `aiismath`.
- Confirm "Mess to Meaning" no longer appears anywhere in the lesson nav / sidebar.

- [ ] **Step 4: Verify the glossary link**

Open the glossary / KeyTerm for **Unstructured Data** and confirm its source link now navigates to **Rules vs Patterns** (`aivscode`), not a dead lesson.

---

### Task 5: Sync briefing.md and finalize

**Files:**
- Modify: `briefing.md`

- [ ] **Step 1: Update the lesson map and add a change note**

In `briefing.md`, update the Understand AI line: Foundations drops `Mess to Meaning (data)` and the group goes 6 → 5; Understand AI count goes 15 → 14. Add a dated update note in the same style as the existing ones, e.g.:

```
Update (2026-06-15): Mess to Meaning (data) was merged into Rules vs Patterns (aivscode) — the rules-vs-patterns contrast and its mess payoff are one idea. The merged lesson keeps both CompareBoxes, the PS5 SEE IT, and both TRY ITs ("Which One Handles This?" then "What Could AI Pull Out?"), gated on completing both; data's "AI runs on patterns" opener and its "step by step" ShowcaseBox were cut. Harder to Control (norules) stays standalone and now gates to AI is Math (aiismath). DataSection remains in the file as a dead stub (returns null), removed from SECTION_GROUPS/SECTION_META/SECTION_COMPONENTS; the "Unstructured Data" glossary term repoints to aivscode. Understand AI 15 → 14, Foundations 6 → 5, course total 61 → 60.
```

Adjust the exact wording/counts to match the file's current totals when you run this.

- [ ] **Step 2: Log cut copy in the parking lot (if any worth keeping)**

If the cut ShowcaseBox intro ("AI takes your messy input, matches it against the patterns it learned, and hands back something you can use.") is worth preserving, append it to `docs/parking-lot.md` under a dated heading. Otherwise skip.

- [ ] **Step 3: Commit the docs**

```bash
git add briefing.md docs/parking-lot.md docs/superpowers/specs/2026-06-15-merge-rules-patterns-mess-design.md docs/superpowers/plans/2026-06-15-merge-rules-patterns-mess.md
git commit -m "Sync briefing + park cut copy for Rules vs Patterns merge"
```

---

## Notes for the implementer

- **Course total:** removing one lesson takes the course from 61 to 60. Confirm the actual current total in `briefing.md` before writing the number.
- **Why move, not copy:** `design-check.sh` counts style patterns across the whole file; leaving a full duplicate of `DataSection`'s JSX would double those counts and could FLAG. Gutting the stub keeps the house "dead code stays defined" pattern without duplication.
- **No automated tests exist** for this app; the design-check + browser walkthrough in Task 4 is the verification gate. Do not skip it.
