# Lab 01: NotebookLM Course-Notebook Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorder the last two Start Smarter lessons, add per-part print packets, and add the first LAB block ("LAB 01 · Build Your Course Notebook," teal) to the end of Study with AI, plus a facilitator note.

**Architecture:** `index.html` is a single-file React app using `React.createElement` (no JSX, no build step). Three independent changes land in sequence: (1) a lesson reorder in `SECTION_GROUPS` plus three `NextLessonGate` retargets; (2) the existing `?print=all` mode extended to `?print=<part-slug>`; (3) a new `InteractiveBox` variant (`lab`, teal surface) rendered by a new component `Lab01CourseNotebook` inside `StudyingWithAISection`. Checkbox state persists via the existing `useLocalStorage` hook. The lab does NOT gate the next lesson. The facilitator note is a standalone markdown doc.

**Tech Stack:** React via `React.createElement` in `index.html`; verification via `validate()` (auto-runs in browser console), `bash design-check.sh`, and a local HTTP server with the Playwright MCP (`file://` is blocked — serve over HTTP).

**Spec:** `docs/superpowers/specs/2026-06-10-notebooklm-lab-01-design.md`

**House rules that apply to every task:**
- NO em-dashes anywhere in new copy (design-check baseline is exactly 4; any new one fails the check).
- No hand-built counter pills (`borderRadius: 999, padding: "6px 14px"`); use `ActivityCounter`.
- Fonts only via `var(--sans)` / `var(--serif)` / `var(--mono)`; shadows only via `var(--shadowSoft)` / `var(--shadowElevated)`.
- Copy uses curly apostrophes (`’`), matching the file convention.
- Line numbers below were verified on commit `3f3eeb4`; re-grep if drifted.

---

### Task 1: Reorder What You Can Control before Study with AI

Start Smarter currently ends `… whybother → studying → control`. After this task it ends `… whybother → control → studying`, so the Start Smarter packet covers exactly what has been taught when the lab runs. Verified already: no lesson copy back-references the old order; only the group array and three gates change.

**Files:**
- Modify: `index.html:1216` (`SECTION_GROUPS`, Start Smarter entry)
- Modify: `index.html:~3082-3086` (whybother's gate)
- Modify: `index.html:~3230-3235` (control's gate)
- Modify: `index.html:9084` (studying's gate)

- [ ] **Step 1: Swap the array order**

Replace:

```js
  sections: ["welcome", "whydeeper", "aihistory", "llms", "doesaithink", "whybother", "studying", "control"]
```

with:

```js
  sections: ["welcome", "whydeeper", "aihistory", "llms", "doesaithink", "whybother", "control", "studying"]
```

- [ ] **Step 2: Retarget whybother's gate** (currently points to studying)

Replace:

```js
    E(NextLessonGate, {
      ready: allAnswered,
      onClick: function() { props.completeAndNavigate && props.completeAndNavigate("studying"); },
      label: "Next: Study with AI"
    }));
```

with:

```js
    E(NextLessonGate, {
      ready: allAnswered,
      onClick: function() { props.completeAndNavigate && props.completeAndNavigate("control"); },
      label: "Next: What You Can Control"
    }));
```

(This is the gate at the end of the component that defines `allAnswered` just above `function ControlSection`; confirm with `grep -n 'completeAndNavigate("studying")' index.html` — exactly one hit before this edit.)

- [ ] **Step 3: Retarget control's gate** (currently points to openerfoundations; it is inside `ControlSection`, found via `grep -n 'completeAndNavigate("openerfoundations")' index.html` — take the hit inside `ControlSection`, around line 3232)

Replace:

```js
    E(NextLessonGate, {
      ready: allAnswered,
      onClick: function() { props.completeAndNavigate && props.completeAndNavigate("openerfoundations"); },
      label: "Next: Foundations"
    }));
```

with:

```js
    E(NextLessonGate, {
      ready: allAnswered,
      onClick: function() { props.completeAndNavigate && props.completeAndNavigate("studying"); },
      label: "Next: Study with AI"
    }));
```

- [ ] **Step 4: Retarget studying's gate** (`index.html:9084`)

Replace:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: Object.keys(picks).length >= SCENARIOS.length, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("control"); }, label: "Next: What You Can Control" })
```

with:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: Object.keys(picks).length >= SCENARIOS.length, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("openerfoundations"); }, label: "Next: Foundations" })
```

- [ ] **Step 5: Verify the chain in the browser**

Serve: `python3 -m http.server 8753 --bind 127.0.0.1` (background), navigate Playwright to `http://127.0.0.1:8753/index.html`.
Expected console: green `✓ validate(): all N lessons pass structural checks`, no errors.

Then run the full-chain trace in `browser_evaluate`:

```js
(function() {
  var ids = SECTION_GROUPS.flatMap(function(g) { return g.sections; });
  var bad = [];
  for (var i = 0; i < ids.length - 1; i++) {
    var src = SECTION_COMPONENTS[ids[i]].toString();
    if (src.indexOf('"' + ids[i + 1] + '"') === -1) bad.push(ids[i] + " !-> " + ids[i + 1]);
  }
  return bad.length ? bad.join("; ") : "CHAIN OK";
})()
```

Expected: `CHAIN OK`.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Reorder Start Smarter: What You Can Control before Study with AI"
```

---

### Task 2: Per-part print packets (`?print=<part-slug>`)

`?print=all` currently renders the whole course for print-to-PDF. Extend it so `?print=start-smarter` (etc.) renders one part with the same layout. Four places check the print param today; all must treat any non-empty value as print mode.

**Files:**
- Modify: `index.html:273-276` (`ActivityCounter` print check)
- Modify: `index.html:~885-887` (`QuizBlock` mint print check)
- Modify: `index.html:~1163-1165` (`RevealSequence` print check)
- Modify: `index.html:~14036-14075` (App print branch)

- [ ] **Step 1: Loosen the three component-level checks**

In `ActivityCounter`, `QuizBlock`, and `RevealSequence`, change each occurrence of:

```js
new URLSearchParams(window.location.search).get("print") === "all"
```

to:

```js
!!new URLSearchParams(window.location.search).get("print")
```

(Three occurrences; the fourth `get("print")` site is the App branch handled next. `grep -c '=== "all"' index.html` should go from 4 to 1 after this step.)

- [ ] **Step 2: Add group filtering to the App print branch**

Replace:

```js
  var isPrintMode = false;
  try {
    isPrintMode = typeof window !== "undefined" && new URLSearchParams(window.location.search).get("print") === "all";
  } catch (ex) {}
  if (isPrintMode) {
```

with:

```js
  var printParam = null;
  try {
    printParam = typeof window !== "undefined" ? new URLSearchParams(window.location.search).get("print") : null;
  } catch (ex) {}
  var printSections = null;
  if (printParam === "all") {
    printSections = SECTIONS;
  } else if (printParam) {
    var printSlug = function(s) { return s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, ""); };
    var printGroup = SECTION_GROUPS.find(function(g) { return printSlug(g.label) === printParam; });
    if (printGroup) printSections = SECTIONS.filter(function(s) { return printGroup.sections.indexOf(s.id) !== -1; });
  }
  if (printSections) {
```

and inside the branch change the map source from `SECTIONS.map(function(section, idx) {` to `printSections.map(function(section, idx) {`, and the last-item check from `idx === SECTIONS.length - 1` to `idx === printSections.length - 1`. An unknown slug leaves `printSections` null and falls through to the normal app. (Edge case, accepted: with an unknown slug the three component checks still see a truthy param and render print-style; harmless because it only happens on a hand-typed bad URL.)

- [ ] **Step 3: Verify both print modes**

Navigate to `http://127.0.0.1:8753/index.html?print=start-smarter`.
Expected: a print layout containing exactly the 8 Start Smarter lessons, `welcome` first, `studying` last (post-reorder order). Check with `browser_evaluate`: `document.body.innerText.indexOf("Study with AI") !== -1` and that no Understand AI lesson titles appear.

Navigate to `http://127.0.0.1:8753/index.html?print=all`.
Expected: unchanged whole-course print layout.

Navigate to `http://127.0.0.1:8753/index.html?print=bogus`.
Expected: the normal app loads.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Extend print mode to per-part packets via ?print=<part-slug>"
```

---

### Task 3: Add the LAB design tokens and the `lab` InteractiveBox variant

**Files:**
- Modify: `index.html:40-44` (CSS custom properties, TRY IT band block)
- Modify: `index.html:346-362` (`InteractiveBox`)

- [ ] **Step 1: Add the LAB band tokens**

In the `:root` CSS block, directly after the TRY IT band group (after the line `--tryRule: rgba(63, 107, 63, 0.18);`, before `--blockGap: 24px;`), add:

```css
    /* LAB band */
    --labBand: #e4f2f0;
    --labAccent: #0f766e;
    --labRule: rgba(15, 118, 110, 0.25);
```

- [ ] **Step 2: Extend `InteractiveBox` with the `lab` variant and `teal` surface**

In `function InteractiveBox(props)` (`index.html:346`), replace these two lines:

```js
  var variant = props.variant === "see" ? "see" : "try";
  var iconAndLabel = variant === "see" ? "◉ SEE IT" : "✎ TRY IT";
```

with:

```js
  var variant = props.variant === "see" ? "see" : props.variant === "lab" ? "lab" : "try";
  var iconAndLabel = variant === "see" ? "◉ SEE IT" : variant === "lab" ? "⚒ LAB" + (props.labNumber ? " " + props.labNumber : "") : "✎ TRY IT";
```

Then replace the surface line:

```js
  var surface = props.surface === "mint" ? "mint" : props.surface === "sand" ? "sand" : "default";
```

with:

```js
  var surface = props.surface === "mint" ? "mint" : props.surface === "sand" ? "sand" : props.surface === "teal" ? "teal" : "default";
```

Then replace the `containerStyle` ternary:

```js
  var containerStyle = surface === "mint"
    ? { background: "var(--tryBand)", border: "none", borderRadius: 16, padding: "26px 28px" }
    : surface === "sand"
    ? { background: "var(--seeBand)", border: "none", borderRadius: 24, padding: "32px 36px 36px" }
    : { background: "var(--primaryFaint)", border: "2px dashed var(--primary)", borderRadius: 16, padding: "26px 28px" };
```

with:

```js
  var containerStyle = surface === "mint"
    ? { background: "var(--tryBand)", border: "none", borderRadius: 16, padding: "26px 28px" }
    : surface === "sand"
    ? { background: "var(--seeBand)", border: "none", borderRadius: 24, padding: "32px 36px 36px" }
    : surface === "teal"
    ? { background: "var(--labBand)", border: "none", borderRadius: 16, padding: "26px 28px" }
    : { background: "var(--primaryFaint)", border: "2px dashed var(--primary)", borderRadius: 16, padding: "26px 28px" };
```

Then replace the eyebrow color line:

```js
  var eyebrowColor = surface === "sand" ? "var(--seeAccent)" : "var(--tryAccent)";
```

with:

```js
  var eyebrowColor = surface === "sand" ? "var(--seeAccent)" : surface === "teal" ? "var(--labAccent)" : "var(--tryAccent)";
```

(No CSS targets `interactive-box--<variant>` classes; the only occurrence is the className construction at `index.html:400`. No stylesheet change needed.)

- [ ] **Step 3: Check baselines**

Run: `bash design-check.sh`
Expected: `PASS - no new drift against baselines.`

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Add lab InteractiveBox variant with teal band tokens"
```

---

### Task 4: Add and render the `Lab01CourseNotebook` component

**Files:**
- Modify: `index.html` — insert the component directly above `function StudyingWithAISection(props) {` (currently `index.html:8923`), then add one render line inside `StudyingWithAISection`

- [ ] **Step 1: Insert the component**

Paste this complete component immediately before `function StudyingWithAISection(props) {`:

```js
function Lab01CourseNotebook() {
  var E = React.createElement;
  var [labChecked, setLabChecked] = useLocalStorage("llm-lab01-steps", {});
  var STEPS = [
    { title: "Print your packet", body: [
      "Open the ",
      E("a", { key: "pk", href: "?print=start-smarter", target: "_blank", rel: "noopener", style: { color: "var(--labAccent)", fontWeight: 700 } }, "Start Smarter packet"),
      ", then save it as a PDF: press Ctrl+P (Cmd+P on a Mac) and choose “Save as PDF”. Name the file Start Smarter."
    ] },
    { title: "Create the course notebook", body: "At notebooklm.google.com, make a new notebook and name it after the course: “Be Smarter Than the Tool”. This notebook grows with you. Every part of the course will land in it." },
    { title: "Add the packet as a source", body: "Upload the PDF you just saved. One part of the course, one source. That’s the filing system." },
    { title: "Generate a blind quiz", body: "Use the prompt from this lesson: “Generate a 10-question quiz from these sources only. Don’t show the answers yet. Wait for mine, then grade me.”" },
    { title: "Take it cold", body: "Close the lesson tabs first. Answer all ten, then let it grade you. Recognition isn’t recall; cold is the point." },
    { title: "Click one citation", body: "Pick one graded answer and click its numbered citation. It lands on the exact passage of the course that taught it. Make that check a habit." },
    { title: "Transfer it", body: "This week, make a second notebook for whichever class has your next test, and feed it your real materials: notes, slides, a YouTube explainer. The course showed you the machine; your grades are where it pays." }
  ];
  var checkedCount = STEPS.reduce(function(n, _s, i) { return n + (labChecked[i] ? 1 : 0); }, 0);
  return E(InteractiveBox, {
    variant: "lab",
    surface: "teal",
    labNumber: "01",
    title: "Build Your Course Notebook",
    hint: "About 25 minutes. You’ll need a laptop and a Google account.",
    action: E(ActivityCounter, { count: checkedCount, total: STEPS.length })
  },
    E("div", { style: { display: "flex", flexDirection: "column", gap: 16 } },
      E("div", { style: { fontSize: BOX_TEXT, color: "var(--inkSoft)", lineHeight: 1.55 } },
        "You just learned what a source-grounded tutor is. Now aim it at this course: study Start Smarter with the tool Start Smarter taught you."),
      E("div", { style: { display: "flex", flexDirection: "column", gap: 10 } },
        STEPS.map(function(st, i) {
          var done = !!labChecked[i];
          return E("button", {
            key: i,
            "aria-pressed": done,
            onClick: function() { setLabChecked(function(prev) { var next = Object.assign({}, prev); next[i] = !prev[i]; return next; }); },
            style: { display: "flex", alignItems: "flex-start", gap: 12, width: "100%", textAlign: "left", background: "#fff", border: "1px solid " + (done ? "var(--labAccent)" : "var(--rule)"), borderRadius: 12, padding: "14px 16px", cursor: "pointer", fontFamily: "var(--sans)", boxShadow: "var(--shadowSoft)" }
          },
            E("span", { "aria-hidden": "true", style: { width: 20, height: 20, flexShrink: 0, borderRadius: 6, marginTop: 1, border: "2px solid " + (done ? "var(--labAccent)" : "var(--inkFaint)"), background: done ? "var(--labAccent)" : "#fff", color: "#fff", fontSize: 13, fontWeight: 800, display: "flex", alignItems: "center", justifyContent: "center" } }, done ? "✓" : ""),
            E("span", null,
              E("span", { style: { display: "block", fontSize: BOX_CARD_TITLE, fontWeight: 800, color: "var(--ink)", marginBottom: 3 } }, (i + 1) + ". " + st.title),
              E("span", { style: { display: "block", fontSize: BOX_TEXT, color: "var(--inkSoft)", lineHeight: 1.55, fontWeight: 400 } }, st.body)));
        })),
      E("div", { style: { borderTop: "1px solid var(--labRule)", paddingTop: 14, fontSize: BOX_TEXT, color: "var(--ink)", lineHeight: 1.6 } },
        E("strong", { style: { color: "var(--labAccent)" } }, "The payoff: "),
        "your wrong answers are your study list for the next meeting. Keep this notebook: every lab from here adds the next part of the course to it, and the quizzes grow as you go."))
  );
}
```

Notes for the implementer:
- `useLocalStorage`, `ActivityCounter`, `InteractiveBox`, `BOX_TEXT`, `BOX_CARD_TITLE` are globals defined earlier in the file; nothing to import.
- The key `llm-lab01-steps` starts with `llm-` so the app's existing reset flow (which clears `llm-*` keys) covers it.
- Step 1's `body` is an array of children (text + link element); React renders arrays fine and the `key` on the anchor silences the list warning.
- The quiz prompt in step 4 deliberately matches the lesson's "Quiz yourself blind" tip prompt; do not reword one without the other.
- The packet link is relative (`?print=start-smarter`) so it works on localhost and in production.

- [ ] **Step 2: Render it in `StudyingWithAISection`**

Find this passage at the end of `StudyingWithAISection`:

```js
    E(KeyInsight, { lead: "Pick the tool, then make it test you." },
      "Point NotebookLM at your own notes and slides, or a general AI at a topic you don’t have materials for. Either way, the win comes from producing the answers yourself, not watching it summarize. That’s the difference between feeling ready and being ready."),
    /*#__PURE__*/React.createElement(LessonRule, null),
```

and insert one line between the `KeyInsight` and `LessonRule` so it reads:

```js
    E(KeyInsight, { lead: "Pick the tool, then make it test you." },
      "Point NotebookLM at your own notes and slides, or a general AI at a topic you don’t have materials for. Either way, the win comes from producing the answers yourself, not watching it summarize. That’s the difference between feeling ready and being ready."),
    E(Lab01CourseNotebook, null),
    /*#__PURE__*/React.createElement(LessonRule, null),
```

Do NOT touch the `NextLessonGate` line below it (it now points to `openerfoundations` after Task 1). The lab does not gate.

- [ ] **Step 3: Check baselines**

Run: `bash design-check.sh`
Expected: `PASS` (em-dash count still 4; the new copy uses none).

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Add LAB 01 Build Your Course Notebook block to Study with AI"
```

---

### Task 5: Functional and visual verification

**Files:** none (verification; one optional hex tune)

- [ ] **Step 1: Serve and validate**

With `python3 -m http.server 8753 --bind 127.0.0.1` running, navigate Playwright to `http://127.0.0.1:8753/index.html`.
Expected console: green `✓ validate(): all N lessons pass structural checks`, no errors.

- [ ] **Step 2: Jump to the lesson**

In `browser_evaluate`:

```js
localStorage.setItem("llm-explorer-progress", JSON.stringify({ activeSection: "studying", visited: ["studying"], completed: [] }));
```

Reload. Scroll to the bottom of Study with AI. Confirm, in order: KeyInsight → teal LAB block → lesson rule → gate labeled "Next: Foundations".

- [ ] **Step 3: Interaction checks**

1. Eyebrow reads `⚒ LAB 01`; title "Build Your Course Notebook"; counter shows `0 / 7`.
2. Clicking a step toggles its checkbox and the counter increments.
3. Reload preserves checked steps (localStorage `llm-lab01-steps`).
4. The step-1 packet link's href is `?print=start-smarter`; clicking it (new tab) renders the 8-lesson Start Smarter print layout.
5. The next-lesson gate state is unchanged by checking/unchecking lab steps.

- [ ] **Step 4: Visual adjacency check (teal vs mint)**

Screenshot the LAB block, then the "Pick the Better Move" mint TRY IT above it. The teal band must read as a distinct surface from mint at a glance (band hue plus deep-teal eyebrow vs forest-green eyebrow). If they read as the same color, deepen the band toward `#dcefec` and re-check. This is the spec's "pending visual check"; record the final hex in a commit message if changed.

- [ ] **Step 5: Reorder spot-check in the nav**

In the in-section nav for Start Smarter, confirm the order ends: … Why Bother → What You Can Control → Study with AI. Walk the gate from What You Can Control: its button must read "Next: Study with AI".

- [ ] **Step 6: Run the design-drift check**

Run: `bash design-check.sh`
Expected: `PASS - no new drift against baselines.`

- [ ] **Step 7: Commit (only if Step 4 changed the hex)**

```bash
git add index.html
git commit -m "Tune LAB band hex after visual adjacency check"
```

---

### Task 6: Write the facilitator note

**Files:**
- Create: `docs/labs/lab-01-notebooklm.md`

- [ ] **Step 1: Create the doc with this exact content**

```markdown
# Lab 01 facilitator note: Build Your Course Notebook

For whoever is running the session (Nate / Luke). The lab itself lives at
the end of the **Study with AI** lesson in the app; students follow it on
their own laptops. This note is the session plan around it.

## Before September (one-time pre-flight)

- Test NotebookLM (notebooklm.google.com) on a **school** Google account.
  Workspace admins sometimes disable it. If it is blocked, plan B is
  students' personal Google accounts (NotebookLM requires age 13+).
- Run the full chain once yourself: open the Start Smarter packet from the
  lab's step 1 link, save it as a PDF, upload it to a fresh notebook,
  generate the quiz. You will hit the same snags students will.

## The 30-minute session

| Time | What happens |
|------|--------------|
| 0-3 | Everyone opens the Study with AI lesson, scrolls to LAB 01, signs into NotebookLM. |
| 3-8 | **Demo on the shared screen:** you run steps 1-4 once (packet, notebook, source, quiz) while narrating the one idea: every question comes from the course and nowhere else. |
| 8-26 | **Everyone builds:** students work the seven steps on their own machines. Circulate. |
| 26-30 | Optional coda if time remains: two volunteers read out one quiz question and say how they scored. Keep it informal. |

## Common stalls and the move for each

- **Print dialog confusion.** The packet opens as a long page; the PDF
  comes from the browser's own print dialog (Ctrl+P / Cmd+P, destination
  "Save as PDF"). Students who tap a "Print" button inside NotebookLM are
  in the wrong app.
- **Upload doesn't appear.** NotebookLM source uploads can take a moment on
  school Wi-Fi; have them wait for the source chip before generating.
- **"My quiz shows the answers."** The prompt was paraphrased. It must say
  *don't show the answers yet*; have them re-send the exact prompt from
  step 4.
- **Finished early.** Point them at step 7 (the second notebook for a real
  class). That step is the whole point; early finishers start it now.

## What done looks like

A student leaves with the course notebook holding the Start Smarter packet,
a graded 10-question quiz, and at least one citation clicked. Their wrong
answers are their study list for the week. Next lab adds the next part of
the course to the same notebook.
```

- [ ] **Step 2: Commit**

```bash
git add docs/labs/lab-01-notebooklm.md
git commit -m "Add facilitator note for Lab 01 (course notebook)"
```

---

## Spec coverage map (self-review)

- Course reorder (array + three gates, no copy edits needed) → Task 1.
- Per-part print packets, `print=all` preserved, unknown slug falls through, three component checks loosened → Task 2.
- New `lab` variant, teal band/accent, `LAB 01` eyebrow, title, contract hint → Tasks 3-4.
- One arc, seven checkboxed steps incl. packet link (step 1) and transfer challenge (step 7); intro meta-loop line; wrap planting the thread → Task 4.
- Checkbox persistence (`llm-` key), no gating → Task 4 + Task 5 step 3.
- Facilitator note incl. pre-flight (school accounts + full-chain run), demo move, stalls, coda → Task 6.
- Pending visual check of teal vs mint → Task 5 step 4.
- Out of scope (summary page, future installments, Understand AI mid-part packets, copy beyond gate labels) → no task touches them.
