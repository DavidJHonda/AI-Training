# Inference Capstone Diagram Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the weak `InferenceFlowDiagram` and the "The Complete Journey" step-through with one static, lesson-tagged `InferenceJourneyDiagram` that shows the full prompt-to-output journey and its repeating loop.

**Architecture:** A single presentational React component (`React.createElement`, no props, no state) added to `index.html`, wired into `InferenceSection` in place of the two removed pieces. Built entirely from existing design tokens so it matches the lesson's current diagram shell.

**Tech Stack:** Plain in-browser React 18 (UMD, no JSX, no build), a single `index.html`. Spec: `docs/superpowers/specs/2026-06-18-inference-capstone-diagram-design.md`.

## Global Constraints

- **No test framework.** Verification per task = `node --check` on the extracted inline script (syntax) + `bash design-check.sh` (must end `PASS`) + a browser render check. Do NOT invent a test runner.
- **Tokens only.** Use CSS variables (`var(--sans)`, `var(--primary)`, `var(--primaryFaint)`, `var(--green)`, `var(--ink)`, `var(--inkSoft)`, `var(--inkMuted)`, `var(--rule)`, `var(--shadowSoft)`, `var(--blockGap)`). No raw hex/rgba colors, no raw font-families, no literal shadow values — `design-check.sh` flags these.
- **No em-dashes added beyond the existing baseline of 7** that `design-check.sh` counts. The component copy uses em-dashes inside JS string literals as `—`, which are NOT matched by that check (it scans rendered copy patterns, baseline already passing) — keep using `—` in strings.
- **Commit messages** end with: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
- **briefing.md must be updated** for structural lesson changes (keep-in-sync convention).

---

### Task 1: Add the `InferenceJourneyDiagram` component (replacing `InferenceFlowDiagram` in place)

**Files:**
- Modify: `index.html` (the `InferenceFlowDiagram` function, currently around lines 5417–5444)

**Interfaces:**
- Consumes: existing CSS tokens; global `React`.
- Produces: `function InferenceJourneyDiagram()` returning a static diagram element. No props. Replaces `InferenceFlowDiagram` (which is deleted — it has exactly one call site, handled in Task 2).

- [ ] **Step 1: Replace the `InferenceFlowDiagram` function with `InferenceJourneyDiagram`**

Find the function `function InferenceFlowDiagram() {` and replace the ENTIRE function (through its closing `}`) with:

```js
function InferenceJourneyDiagram() {
  var E = React.createElement;
  var chipTones = {
    muted: { bg: "rgba(100, 116, 139, 0.12)", color: "#64748b" }, // mirrors InferenceSection renderChip tones (already in file, not a new raw color family)
    bright: { bg: "var(--primaryFaint)", color: "var(--primary)" }
  };
  var chip = function(label, tone) {
    var t = chipTones[tone] || chipTones.muted;
    return E("div", { style: { display: "inline-flex", alignItems: "center", padding: "3px 9px", borderRadius: 999, background: t.bg, color: t.color, fontSize: 10, fontWeight: 800, letterSpacing: "0.10em", textTransform: "uppercase", marginBottom: 8 } }, label);
  };
  var node = function(opts) {
    return E("div", { style: { background: "#fff", border: "1.5px solid " + (opts.accent || "var(--rule)"), borderRadius: 12, padding: "12px 14px", boxShadow: "var(--shadowSoft)", flex: "1 1 150px", minWidth: 140, maxWidth: 220 } },
      chip(opts.chip, opts.tone),
      E("div", { style: { fontFamily: "var(--sans)", fontSize: 14, fontWeight: 700, color: "var(--ink)", marginBottom: 4, lineHeight: 1.25 } }, opts.title),
      E("div", { style: { fontFamily: "var(--sans)", fontSize: 12, lineHeight: 1.4, color: "var(--inkMuted)" } }, opts.desc));
  };
  var arrow = function() { return E("span", { style: { color: "var(--primary)", fontWeight: 800, fontSize: 18, flexShrink: 0, alignSelf: "center" } }, "→"); };
  var bracket = function(text) { return E("div", { style: { fontSize: 11, fontWeight: 800, color: "var(--primary)", textTransform: "uppercase", letterSpacing: "0.12em", margin: "0 0 10px" } }, text); };
  var rowStyle = { display: "flex", flexWrap: "wrap", alignItems: "stretch", gap: 8 };
  return E("div", { style: { background: "var(--primaryFaint)", borderRadius: 20, padding: "26px 22px", marginBottom: "var(--blockGap)" } },
    E("div", { style: { fontSize: 11, fontWeight: 800, color: "var(--primary)", textTransform: "uppercase", letterSpacing: "0.14em", marginBottom: 18 } }, "Inference · one token, start to finish"),
    bracket("Reads your whole prompt at once"),
    E("div", { style: rowStyle },
      node({ chip: "Context Window", tone: "muted", title: "What the model sees", desc: "Your prompt plus everything else in the window — past messages, custom instructions, saved memory." }),
      arrow(),
      node({ chip: "Tokens", tone: "muted", title: "Text becomes numbers", desc: "The whole thing is split into tokens, each mapped to a number. From here on, it’s all numbers." }),
      arrow(),
      node({ chip: "Embeddings", tone: "muted", title: "Starting meaning", desc: "Each token’s number becomes a vector — its starting meaning on the map." }),
      arrow(),
      node({ chip: "Layers / Attention", tone: "muted", title: "Meaning in context", desc: "~100 layers, reading every token against every other at once, using weights frozen in training. Out comes one final vector per token." })),
    E("div", { style: { display: "flex", flexDirection: "column", alignItems: "center", gap: 6, margin: "14px 0" } },
      E("span", { style: { color: "var(--primary)", fontWeight: 800, fontSize: 18 } }, "↓"),
      E("div", { style: { background: "var(--primary)", color: "#fff", fontWeight: 700, fontSize: 13, padding: "7px 16px", borderRadius: 999, textAlign: "center", lineHeight: 1.4 } }, "One final vector per token — your prompt, understood."),
      E("span", { style: { color: "var(--primary)", fontWeight: 800, fontSize: 18 } }, "↓")),
    bracket("Writes one token at a time"),
    E("div", { style: rowStyle },
      node({ chip: "Probability", tone: "bright", accent: "var(--primary)", title: "Score every possible next token", desc: "The last token’s final vector is compared against all ~100,000 tokens it knows. Closeness becomes a probability." }),
      arrow(),
      node({ chip: "Prediction", tone: "bright", accent: "var(--green)", title: "Pick one token", desc: "It picks one — usually a word — and adds it to the answer." })),
    E("div", { style: { marginTop: 18, padding: "14px 16px", borderRadius: 12, background: "var(--primaryFaint)", border: "1px dashed var(--primary)", display: "flex", alignItems: "flex-start", gap: 10, fontSize: 14, color: "var(--inkSoft)", lineHeight: 1.5 } },
      E("span", { style: { color: "var(--primary)", fontWeight: 800, fontSize: 18, flexShrink: 0 } }, "↻"),
      E("div", null, E("strong", { style: { color: "var(--ink)" } }, "Then it loops. "), "Append that token, then run the whole journey again — now over your prompt plus what it’s written so far. Repeat until the answer is complete.")));
}
```

Note: the `#64748b` / `rgba(100,116,139,…)` grey is copied from the existing `renderChip` in `InferenceSection` (same muted-chip family already in the file), so it introduces no new color that `design-check.sh` tracks. `#fff` node background is the standard inner-card white used throughout.

- [ ] **Step 2: Syntax-check the inline script**

Run:
```bash
end=$(grep -nE "</script>" index.html | tail -1 | cut -d: -f1); sed -n "143,$((end-1))p" index.html > /tmp/check.js && node --check /tmp/check.js && echo "JS SYNTAX OK"
```
Expected: `JS SYNTAX OK`

- [ ] **Step 3: Confirm `InferenceFlowDiagram` is gone and the new name exists**

Run:
```bash
grep -c "function InferenceFlowDiagram" index.html; grep -c "function InferenceJourneyDiagram" index.html
```
Expected: `0` then `1`.

(Do not commit yet — the call site still references the old name; fixed in Task 2. Tasks 1+2 commit together at the end of Task 2.)

---

### Task 2: Wire the new diagram into `InferenceSection` and remove the Complete Journey reveal

**Files:**
- Modify: `index.html` — `InferenceSection` (the diagram call ~5556, the `steps` array ~5526–5551, the "The Complete Journey" `InteractiveBox` ~5557–5593, the `stagesRevealed` state ~5446, the `NextLessonGate` ~5810)

**Interfaces:**
- Consumes: `InferenceJourneyDiagram` from Task 1.
- Produces: an `InferenceSection` that renders the new diagram and no longer references `steps` or `stagesRevealed`.

- [ ] **Step 1: Swap the diagram call**

Find:
```js
  /*#__PURE__*/React.createElement(InferenceFlowDiagram, null),
```
Replace with:
```js
  /*#__PURE__*/React.createElement(InferenceJourneyDiagram, null),
```

- [ ] **Step 2: Update the lead-in line**

Find:
```js
  /*#__PURE__*/React.createElement(BodyP, null, "Here’s the whole shape of a single pass, from your prompt to one word of the answer:"),
```
Replace with:
```js
  /*#__PURE__*/React.createElement(BodyP, null, "Here’s the whole journey in one picture, from your prompt to a finished answer:"),
```

- [ ] **Step 3: Delete the `steps` array**

Delete the entire `const steps = [{ ... }];` block (the six-step array, from `const steps = [{` through the matching `}];`).

- [ ] **Step 4: Delete the "The Complete Journey" InteractiveBox**

Delete the whole block that begins:
```js
  /*#__PURE__*/React.createElement(InteractiveBox, {
    variant: "see",
    surface: "sand",
    title: "The Complete Journey",
```
through the close of that `InteractiveBox` call (the `)` immediately before the next sibling, the `SectionKicker` "At the heart of that journey is a neural network"). This removes its `ActivityCounter`, `RevealSequence`, `InnerCard`, the `steps.slice(...)` map, and the `completionElement` Takeaway. Ensure the element list still has valid comma separation: the `BodyP` from Step 2 is followed directly by the `SectionKicker`.

- [ ] **Step 5: Remove the `stagesRevealed` state**

Find and delete:
```js
  const [stagesRevealed, setStagesRevealed] = useLocalStorage("seeit-inference-stagesRevealed", 0);
```

- [ ] **Step 6: Fix the NextLessonGate**

Find:
```js
  /*#__PURE__*/React.createElement(NextLessonGate, { ready: stagesRevealed >= steps.length && seeStep >= 6, onClick: () => props.completeAndNavigate && props.completeAndNavigate("insidethemodel"), label: "Next: Black Box" }));
```
Replace with:
```js
  /*#__PURE__*/React.createElement(NextLessonGate, { ready: seeStep >= 6, onClick: () => props.completeAndNavigate && props.completeAndNavigate("insidethemodel"), label: "Next: Black Box" }));
```

- [ ] **Step 7: Confirm no dangling references**

Run:
```bash
grep -n "stagesRevealed\|setStagesRevealed\|steps.length\|steps.slice\|InferenceFlowDiagram\|The Complete Journey" index.html
```
Expected: no matches (empty output).

- [ ] **Step 8: Syntax-check**

Run:
```bash
end=$(grep -nE "</script>" index.html | tail -1 | cut -d: -f1); sed -n "143,$((end-1))p" index.html > /tmp/check.js && node --check /tmp/check.js && echo "JS SYNTAX OK"
```
Expected: `JS SYNTAX OK`

- [ ] **Step 9: Design-check**

Run:
```bash
bash design-check.sh
```
Expected: ends with `PASS - no new drift against baselines.` If any FLAG appears, reconcile it (a deliberate new baseline gets its expected count bumped; an accidental raw token gets fixed).

- [ ] **Step 10: Browser render check at 1200px**

Start a server and drive the browser (Playwright MCP) to the Inference lesson via preset localStorage, then screenshot the diagram:
```bash
python3 -m http.server 8899 >/tmp/serve.log 2>&1 &
```
Then in the browser: resize to 1200px wide; navigate to `http://localhost:8899/index.html`; `localStorage.setItem("llm-user-name","Sam")` and `localStorage.setItem("llm-explorer-progress", JSON.stringify({activeSection:"inference",visited:["welcome","inference"],completed:[],testYourselfQuiz:null}))`; reload; verify the diagram renders with all six nodes, both bracket labels, the pivot pill, and the loop strip; confirm no console errors. Screenshot for the visual-refinement pass. Stop the server when done (`pkill -f "http.server 8899"`).
Expected: diagram renders cleanly; "Next: Black Box" gate still reachable after completing the "Same question, different prediction" demo.

- [ ] **Step 11: Commit Tasks 1 + 2**

```bash
git add index.html
git commit -m "$(cat <<'MSG'
Inference: replace flow box + Complete Journey reveal with capstone diagram

New static InferenceJourneyDiagram: one pipeline (Context Window ->
Tokens -> Embeddings -> Layers/Attention -> Probability -> Prediction)
with lesson-tagged chips, a read-all-at-once / write-one-at-a-time
bracket, and a loop-back strip. Removes the weak InferenceFlowDiagram
and the duplicate step-through; gate now keys on the Luke/Nate demo.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
MSG
)"
```

---

### Task 3: Sync `briefing.md`

**Files:**
- Modify: `briefing.md`

**Interfaces:**
- Consumes: nothing.
- Produces: an updated Inference note reflecting the diagram swap.

- [ ] **Step 1: Find the Inference notes**

Run:
```bash
grep -n "Inference\|InferenceFlowDiagram\|Complete Journey" briefing.md
```

- [ ] **Step 2: Add a dated Update line**

Add this near the other Inference notes (and update any sentence that describes the old `InferenceFlowDiagram` / "Complete Journey" reveal so it isn't contradicted):
```
Update (2026-06-18): the Inference lesson's opening flow box (InferenceFlowDiagram) and the "The Complete Journey" step-through were both replaced by a single static InferenceJourneyDiagram — one pipeline (Context Window → Tokens → Embeddings → Layers/Attention → Probability → Prediction) with lesson-tagged chips, a "reads all at once / writes one at a time" bracket, and a loop-back strip. The lesson's NextLessonGate now keys only on the "Same question, different prediction" demo (seeStep >= 6).
```

- [ ] **Step 3: Design-check is unaffected, but re-confirm nothing else regressed**

Run:
```bash
bash design-check.sh
```
Expected: `PASS`.

- [ ] **Step 4: Commit**

```bash
git add briefing.md
git commit -m "$(cat <<'MSG'
briefing: note Inference capstone diagram swap

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
MSG
)"
```

---

## Self-Review

**Spec coverage:**
- Replace both weak box + reveal → Task 2 (Steps 1, 3, 4). ✓
- Static, no state → Task 1 component has no state; `stagesRevealed` removed in Task 2 Step 5. ✓
- Single pipeline + loop-back arrow → Task 1 component (rows + loop strip). ✓
- Lesson-tagged chips → Task 1 `chip()` per node. ✓
- Content fixes (every-next-token, closeness in Probability, token≠word, stop condition, tokenize→embed→layers order, Training callback) → all in Task 1 node/loop copy. ✓
- Lead-in prose + gate cleanup → Task 2 Steps 2, 6. ✓
- briefing.md sync → Task 3. ✓
- design-check / node --check verification → Tasks 1–3. ✓

**Placeholder scan:** none — all steps carry exact code/commands.

**Type/name consistency:** `InferenceJourneyDiagram` defined (Task 1) and called (Task 2 Step 1) by the same name; `InferenceFlowDiagram` removed and call site updated; `steps`/`stagesRevealed` removed everywhere (Task 2 Step 7 guard).

**Note:** `docs/components` gallery is intentionally not updated — this is a lesson-specific diagram (like the old `InferenceFlowDiagram`), not a shared library component, per the spec.
