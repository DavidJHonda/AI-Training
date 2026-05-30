# Course Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Resequence `index.html` from 8 content sections into a 5-part spine (Understand AI → Work With AI → Judgment I → Judgment II → Build Your Advantage), plus Intro and Finish, with no teaching-content rewrites.

**Architecture:** All structure lives in three data structures — `SECTION_GROUPS` (grouping/sidebar/eyebrow), `SECTION_COMPONENTS` (id→component routing), and the per-lesson `completeAndNavigate(...)` / opener `nextLessonId` handoff chain. We rewrite the grouping, derive badges from `SECTION_GROUPS`, add three fresh opener components, orphan four old openers, and re-point ~13 handoff seams. Component function bodies do not move. Saved progress is untouched (content-keyed `useLocalStorage`; `activeSection` stores an id, verified).

**Tech Stack:** Single 1.18 MB `index.html`, inline Babel-compiled React (`React.createElement`). No build, no test framework. Verification = the in-file `validate()` invariant checker (console) + `design-check.sh` + manual browser click-through (the `verify` skill / Playwright). Deployed via Vercel from GitHub.

---

## Reference: verified seam map (source of truth)

Every handoff was mapped to its **owning lesson** by nearest-preceding `sectionId` anchor. "CHANGE" rows are the only nav edits; everything else stays.

| # | Owner lesson | Line | Current target / label | New target / label | Step |
|---|---|---|---|---|---|
| 1 | whatitdoesbest | 9037 | `openerusing` / "Next: Workflow" | `openerworkwith` / "Next: Work With AI" | 2 |
| 2 | customization | 7090 | `openertraps` / "Next: Traps" | `questionsvaluable` / "Next: Questions Matter" | 2 |
| 3 | thoughtpartner | 9541 | `critical` / "Next: Critical Thinking" | `openercheck` / "Next: Check the Output" | 3 |
| 4 | evaluating | 9940 | `openercontrols` / "Next: Controls" | `hallucination` / "Next: Hallucination" | 3 |
| 5 | documenttrap | 7286 | `mindtrap` / "Next: Mind Trap" | `openerprotect` / "Next: Protect Yourself" | 3 |
| 6 | supporttrap | 10879 | `openerjudgment` / "Next: Human Judgment" | `whennot` / "Next: When Not to Use AI" | 3 |
| 7 | howmuchtocheck | 2708 | `humanedge` / "Next: Skills That Matter" | `studying` / "Next: Studying With AI" | 3 |
| 8 | privacy | 11687 | `openerrealworld` / "Next: Real World" | `seeingisntproof` / "Next: Seeing Isn't Proof" | 3 |
| 9 | seeingisntproof | 12134 | `aifuture` / "Next: AI & The Future" | `openerrealworld` / "Next: Build Your Advantage" | 3 |
| 10 | stakeholders | 11991 | `seeingisntproof` / "Next: Seeing Isn't Proof" | `aifuture` / "Next: AI & The Future" | 4 |
| 11 | aifuture | 13967 | `buildedge` / "Next: Build Your Edge" | `humanedge` / "Next: Skills That Matter" | 4 |
| 12 | humanedge | 13489 | `studying` / "Next: Studying With AI" | `creativethinking` / "Next: Creative Thinking" | 4 |
| 13 | creativethinking | 10052 | `questionsvaluable` / "Next: Questions Matter" | `buildedge` / "Next: Build Your Edge" | 4 |

New opener `nextLessonId`s (created with components): `openerworkwith→modelselection`, `openercheck→critical`, `openerprotect→mindtrap`.

**Unchanged seams confirmed in-place** (do NOT touch): intro→openerfoundations (3416), data→openerinside (4001), training→openeranswers (5104), all Understand-AI internals, modelselection→choosemodel→thinkingmode→temperature→customization (7714/7842/7934/8082), questionsvaluable→prompting (13258), prompting→thoughtpartner (9332), critical→verify (8712), verify→evaluating (8381), hallucination→trainingbias (8278), trainingbias→documenttrap (4912), mindtrap→flattery (10348), flattery→engagementtrap (10535), engagementtrap→supporttrap (10671), whennot→howmuchtocheck (2476), studying→integrity (9675), integrity→privacy (11307), openerrealworld→workchanges (11022), workchanges→agents (13782), agents→aijudges (10206), aijudges→stakeholders (11863), buildedge→whatyoulearned (14240), all Finish internals.

**Lesson count:** drops 70 → **69** by design (4 old openers retire: openerusing/openercontrols/openertraps/openerjudgment; 3 new ones added: openerworkwith/openercheck/openerprotect; Understand AI keeps its 3). No content lesson is dropped.

## File structure

- **Modify only:** `index.html`. Edits cluster in: `SECTION_GROUPS` (~1169), `SECTION_META` (~1200), the `partBadge` helper (new, ~1272) + badge render (658), three new opener components (new, near ~8842), `SECTION_COMPONENTS` (~14242), the 13 seam lines above, the Roadmap (`IntroSection`, ~3381), and the `creativethinking` cross-reference (~9989).
- **Verification scripts (run, don't edit):** `design-check.sh`; in-app `validate()`.

## Per-step verification gate (run after EVERY task before committing)

1. `bash design-check.sh` → expect pass (no structural errors).
2. Open `index.html` in a browser; open devtools console. Expect `✓ validate(): all 69 lessons pass structural checks` and **no red errors**. (If `validate()` is not auto-invoked on load, call it once from the console.)
3. Click the **full nav chain Intro → Finish** via "Next" buttons. Confirm every handoff lands on the intended next lesson with no dead/locked gate. For the part(s) touched in the task, confirm the new order specifically.
4. Only then commit.

---

## Task 1: Rewrite SECTION_GROUPS + SECTION_META + derive badges (structure only)

**Files:** Modify `index.html`: `SECTION_GROUPS` (1169–1199), `SECTION_META` (1200–1271), badge render (658), new `partBadge` helper, remove 8 hand-typed `badge:` props.

- [ ] **Step 1.1: Replace the `SECTION_GROUPS` array** (lines 1169–1199) with the 7-entry structure:

```js
const SECTION_GROUPS = [{
  label: "Intro",
  sections: ["welcome", "whydeeper", "doesaithink", "whybother", "control", "intro"]
}, {
  label: "Understand AI",
  sections: ["openerfoundations", "aihistory", "llms", "aiismath", "howwegothere", "aivscode", "norules", "data", "openerinside", "tokens", "embeddings", "vectorspace", "insidethemodel", "attention", "layers", "training", "openeranswers", "prompt", "patterns", "probability", "inference", "whatitdoesbest"]
}, {
  label: "Work With AI",
  sections: ["openerworkwith", "modelselection", "choosemodel", "thinkingmode", "temperature", "customization", "questionsvaluable", "prompting", "thoughtpartner"]
}, {
  label: "Judgment I: Check the Output",
  sections: ["openercheck", "critical", "verify", "evaluating", "hallucination", "trainingbias", "documenttrap"]
}, {
  label: "Judgment II: Protect Yourself",
  sections: ["openerprotect", "mindtrap", "flattery", "engagementtrap", "supporttrap", "whennot", "howmuchtocheck", "studying", "integrity", "privacy", "seeingisntproof"]
}, {
  label: "Build Your Advantage",
  sections: ["openerrealworld", "workchanges", "agents", "aijudges", "stakeholders", "aifuture", "humanedge", "creativethinking", "buildedge"]
}, {
  label: "Finish",
  sections: ["whatyoulearned", "fullworkflow", "keyterms", "testyourself", "headtohead"]
}];
```

> NOTE: `openerworkwith`/`openercheck`/`openerprotect` are referenced here but created in Tasks 2–3. Until then the in-app `validate()` (check 2) will report these three as errors and the app won't fully render those parts. That is expected mid-Task-1. To keep Step 1 independently runnable, **do Step 1.2 (the three placeholder components) and Step 1.5 (registry) in this same task before verifying.**

- [ ] **Step 1.2: Add three minimal placeholder opener components.** Insert after the `OpenerUsingSection` function (immediately after its closing `}` at ~line 8842). Copy is PLACEHOLDER — final copy is David-approved in Task 5. No `badge` key (badges are derived in Step 1.4):

```js
function OpenerWorkWithSection(props) {
  return React.createElement(OpenerSection, {
    sectionId: "openerworkwith",
    whyThisMatters: ["PLACEHOLDER (David copy pass). Frame: pick the right tool, then use it well."],
    sectionOverview: { eyebrow: "In this section", title: "Work With AI", subtitle: "Pick the right tool, then use it well." },
    groups: [
      { kicker: "PICK THE TOOL", bridge: "PLACEHOLDER — choose product, model, mode, and settings before blaming the tool." },
      { kicker: "USE IT WELL", bridge: "PLACEHOLDER — ask sharp questions, write clear prompts, think with it." }
    ],
    question: "PLACEHOLDER — keep-this-question prompt.",
    nextLessonId: "modelselection",
    nextLessonLabel: "Next: Choosing the Product",
    completeAndNavigate: props.completeAndNavigate
  });
}
function OpenerCheckSection(props) {
  return React.createElement(OpenerSection, {
    sectionId: "openercheck",
    whyThisMatters: ["PLACEHOLDER (David copy pass). Frame: AI's answer is a draft, not a verdict — check it before you trust it."],
    sectionOverview: { eyebrow: "In this section", title: "Check the Output", subtitle: "Is what AI handed you true and good enough?" },
    groups: [
      { kicker: "QUESTION THE ANSWER", bridge: "PLACEHOLDER — think critically, verify claims, judge if it's good enough." },
      { kicker: "KNOW THE FAILURE MODES", bridge: "PLACEHOLDER — hallucination, training bias, the whole-document trap." }
    ],
    question: "PLACEHOLDER — keep-this-question prompt.",
    nextLessonId: "critical",
    nextLessonLabel: "Next: Critical Thinking",
    completeAndNavigate: props.completeAndNavigate
  });
}
function OpenerProtectSection(props) {
  return React.createElement(OpenerSection, {
    sectionId: "openerprotect",
    whyThisMatters: ["PLACEHOLDER (David copy pass). Frame: the tool can work on you, not just for you — and some calls stay yours."],
    sectionOverview: { eyebrow: "In this section", title: "Protect Yourself", subtitle: "The tool acts on you; the judgment stays yours." },
    groups: [
      { kicker: "WHEN THE TOOL WORKS ON YOU", bridge: "PLACEHOLDER — the mind, flattery, engagement, and support traps." },
      { kicker: "THE CALLS THAT STAY YOURS", bridge: "PLACEHOLDER — when not to use AI, how much to check, studying, integrity, privacy, and doubting what you see." }
    ],
    question: "PLACEHOLDER — keep-this-question prompt.",
    nextLessonId: "mindtrap",
    nextLessonLabel: "Next: Mind Trap",
    completeAndNavigate: props.completeAndNavigate
  });
}
```

- [ ] **Step 1.3: Add `SECTION_META` entries** for the three new openers. Insert inside the `SECTION_META` object (anywhere among the existing keys, e.g. after the `openerusing` meta line):

```js
  openerworkwith: { kicker: "OPENER", label: "Opener", icon: "🗺️" },
  openercheck: { kicker: "OPENER", label: "Opener", icon: "🗺️" },
  openerprotect: { kicker: "OPENER", label: "Opener", icon: "🗺️" },
```

- [ ] **Step 1.4: Add the `partBadge` helper** immediately after the `SECTIONS` definition (after line ~1275, the `.map(... SECTION_META[id])` block):

```js
function partBadge(sectionId) {
  var gi = SECTION_GROUPS.findIndex(function(g) { return g.sections && g.sections[0] === sectionId; });
  if (gi <= 0) return null;                          // not a lead opener, or Intro (index 0): no pill
  if (gi >= SECTION_GROUPS.length - 1) return null;  // Finish (last group): no pill
  return ("0" + (gi + 1)).slice(-2) + " / " + SECTION_GROUPS.length;
}
```

- [ ] **Step 1.5: Switch the badge render to the derived value.** At line 658, replace:

```js
        ov.badge ? E("div", { style: { flexShrink: 0, background: "#ffffff", borderRadius: 999, padding: "6px 14px", fontFamily: "var(--sans)", fontSize: 13, fontWeight: 700, letterSpacing: "0.78px", color: "#5a47c9", whiteSpace: "nowrap" } }, ov.badge) : null),
```

with (only `ov.badge` → `partBadge(props.sectionId)`, twice):

```js
        partBadge(props.sectionId) ? E("div", { style: { flexShrink: 0, background: "#ffffff", borderRadius: 999, padding: "6px 14px", fontFamily: "var(--sans)", fontSize: 13, fontWeight: 700, letterSpacing: "0.78px", color: "#5a47c9", whiteSpace: "nowrap" } }, partBadge(props.sectionId)) : null),
```

- [ ] **Step 1.6: Register the 3 new components + unregister the 4 retired ones** in `SECTION_COMPONENTS` (~14242). Add:

```js
  openerworkwith: OpenerWorkWithSection,
  openercheck: OpenerCheckSection,
  openerprotect: OpenerProtectSection,
```

Delete these four registry lines (the function definitions stay in the file as dead code): `openerusing: OpenerUsingSection,` (~14289), `openercontrols: OpenerControlsSection,` (~14275), `openertraps: OpenerTrapsSection,` (~14264), `openerjudgment: OpenerJudgmentSection,` (~14249).

- [ ] **Step 1.7: Remove the 8 stale hand-typed `badge:` props** so nothing reads `ov.badge` anymore. Delete the `badge: "NN / 10"` line (and fix the trailing comma on the preceding `subtitle`/`eyebrow` line if needed) at: 1304, 5231, 6497, 8817, 7354, 8116, 2511, 10988. (These are inside retired or interior openers and `openerfoundations`; the derived `partBadge` now supplies the only pill, on `openerfoundations` = `02 / 7`.)

- [ ] **Step 1.8: Verify** (run the per-step gate). Specifically confirm: sidebar shows 7 groups; Understand AI lesson eyebrows read "Understand AI"; `openerfoundations` shows `02 / 7`, Work With AI `03 / 7`, Judgment I `04 / 7`, Judgment II `05 / 7`, Build Your Advantage `06 / 7`; `openerinside`/`openeranswers` show **no** pill; Intro/Finish show no pill; `validate()` reports 69 lessons pass.

- [ ] **Step 1.9: Commit**

```bash
git add index.html
git commit -m "Restructure step 1: 7-part SECTION_GROUPS, placeholder openers, derived badges"
```

---

## Task 2: Re-thread the Controls-before-prompting seam (Work With AI order)

**Files:** Modify `index.html` lines 9037 (whatitdoesbest exit) and 7090 (customization exit).

- [ ] **Step 2.1: Re-point whatitdoesbest → Work With AI.** At line 9037 replace `props.completeAndNavigate("openerusing")` with `props.completeAndNavigate("openerworkwith")`, and the adjacent `label: "Next: Workflow"` with `label: "Next: Work With AI"`.

- [ ] **Step 2.2: Re-point customization → questionsvaluable.** At line 7090 (a `PrimaryButton`), replace:

```js
  /*#__PURE__*/React.createElement(PrimaryButton, { onClick: () => props.completeAndNavigate && props.completeAndNavigate("openertraps") }, "Next: Traps"));
```

with:

```js
  /*#__PURE__*/React.createElement(PrimaryButton, { onClick: () => props.completeAndNavigate && props.completeAndNavigate("questionsvaluable") }, "Next: Questions Matter"));
```

- [ ] **Step 2.3: Verify** (per-step gate). Click from `whatitdoesbest` → it should now land on the Work With AI opener → modelselection → choosemodel → thinkingmode → temperature → customization → **questionsvaluable** → prompting → thoughtpartner.

- [ ] **Step 2.4: Commit**

```bash
git add index.html
git commit -m "Restructure step 2: thread Work With AI (Controls before prompting)"
```

---

## Task 3: Assemble Judgment I + Judgment II (the judgment cluster)

**Files:** Modify `index.html` lines 9541, 9940, 7286, 10879, 2708, 11687, 12134.

- [ ] **Step 3.1: thoughtpartner → Judgment I opener.** At line 9541 replace target `critical` → `openercheck` and label `"Next: Critical Thinking"` → `"Next: Check the Output"`.

- [ ] **Step 3.2: evaluating → hallucination.** At line 9940 replace target `openercontrols` → `hallucination` and label `"Next: Controls"` → `"Next: Hallucination"`.

- [ ] **Step 3.3: documenttrap → Judgment II opener.** At lines 7286–7287 replace target `mindtrap` → `openerprotect` and label `"Next: Mind Trap"` → `"Next: Protect Yourself"`.

- [ ] **Step 3.4: supporttrap → whennot.** At line 10879 replace target `openerjudgment` → `whennot` and label `"Next: Human Judgment"` → `"Next: When Not to Use AI"`.

- [ ] **Step 3.5: howmuchtocheck → studying** (humanedge has left this part). At line 2708 replace target `humanedge` → `studying` and label `"Next: Skills That Matter"` → `"Next: Studying With AI"`.

- [ ] **Step 3.6: privacy → seeingisntproof.** At line 11687 replace target `openerrealworld` → `seeingisntproof` and label `"Next: Real World"` → `"Next: Seeing Isn't Proof"`.

- [ ] **Step 3.7: seeingisntproof → Build Your Advantage opener.** At line 12134 replace target `aifuture` → `openerrealworld` and label `"Next: AI & The Future"` → `"Next: Build Your Advantage"`.

- [ ] **Step 3.8: Verify** (per-step gate). Click from `thoughtpartner` → openercheck → critical → verify → evaluating → hallucination → trainingbias → documenttrap → openerprotect → mindtrap → flattery → engagementtrap → supporttrap → whennot → howmuchtocheck → studying → integrity → privacy → seeingisntproof → (lands on Build Your Advantage opener `openerrealworld`).

- [ ] **Step 3.9: Commit**

```bash
git add index.html
git commit -m "Restructure step 3: split judgment into Check the Output + Protect Yourself"
```

---

## Task 4: Relocate creativethinking + humanedge into Build Your Advantage

**Files:** Modify `index.html` lines 11991, 13967, 13489, 10052. (openerrealworld copy update is deferred to Task 5.)

- [ ] **Step 4.1: stakeholders → aifuture** (seeingisntproof has left this part). At line 11991 replace target `seeingisntproof` → `aifuture` and label `"Next: Seeing Isn't Proof"` → `"Next: AI & The Future"`.

- [ ] **Step 4.2: aifuture → humanedge.** At line 13967 replace target `buildedge` → `humanedge` and label `"Next: Build Your Edge"` → `"Next: Skills That Matter"`.

- [ ] **Step 4.3: humanedge → creativethinking.** At line 13489 replace target `studying` → `creativethinking` and label `"Next: Studying With AI"` → `"Next: Creative Thinking"`.

- [ ] **Step 4.4: creativethinking → buildedge.** At line 10052 replace target `questionsvaluable` → `buildedge` and label `"Next: Questions Matter"` → `"Next: Build Your Edge"`.

- [ ] **Step 4.5: Verify** (per-step gate) — full Intro→Finish click-through. Build Your Advantage order must be: openerrealworld → workchanges → agents → aijudges → stakeholders → aifuture → humanedge → creativethinking → buildedge → (Finish: whatyoulearned). Confirm zero dead/locked gates anywhere in the course.

- [ ] **Step 4.6: Commit**

```bash
git add index.html
git commit -m "Restructure step 4: move Creative Thinking + Skills That Matter into Build Your Advantage"
```

---

## Task 5: Copy pass (David-approved content)

> All copy in this task is content design. Per the spec and the editing guidelines, **David approves before finalizing.** Draft, present, revise — do not auto-finalize. Tone: serious, clear, credible, sharp; no em-dashes (course style).

- [ ] **Step 5.1: Rewrite the ROADMAP array** in `IntroSection` (line ~3381). Collapse the 10 old rows to **7 stops** matching the new spine. Draft for David approval:

```js
  var ROADMAP = [
    { question: "Why should I care, and what am I responsible for?", section: "Intro", icon: "👋", outcome: "Know why this matters and what’s in your hands." },
    { question: "What is AI, and how does it actually build an answer?", section: "Understand AI", icon: "🧱", outcome: "See how text becomes numbers and numbers become an answer." },
    { question: "How do I pick the right tool and use it well?", section: "Work With AI", icon: "🎛️", outcome: "Choose the tool on purpose, then prompt and think with it." },
    { question: "Is what it handed me true and good enough?", section: "Judgment I: Check the Output", icon: "🔍", outcome: "Question the answer and know the failure modes." },
    { question: "How is the tool working on me, and what stays my call?", section: "Judgment II: Protect Yourself", icon: "🧭", outcome: "Hold your thinking, your honesty, and your data." },
    { question: "When everyone has AI, what makes me valuable?", section: "Build Your Advantage", icon: "🌍", outcome: "See where this lands in work, society, and you." },
    { question: "What should I remember and prove I can do?", section: "Finish", icon: "🏁", outcome: "Prove the ideas stuck." }
  ];
```

- [ ] **Step 5.2: Update the Roadmap subtitle** (line ~3396): `subtitle: "Ten stops, one route."` → `subtitle: "Seven stops, one route."`

- [ ] **Step 5.3: Update the Roadmap body** (line ~3399): keep "Six lessons in, you've got the why and what's in your hands." and rewrite the "each section" framing to the new arc (draft for approval): "The rest of the course follows one arc: understand it, use it, keep your judgment, and build your advantage."

- [ ] **Step 5.4: Rewrite the `creativethinking` cross-reference** (line ~9989). The current paragraph positions Creative Thinking as "one layer earlier" than Critical Thinking / Questions Matter, which are now far behind it. Replace that one `BodyP` with copy that fits its new near-the-end position (draft for approval), e.g.: "You have spent this whole course learning to work the tool well and check what it returns. This is the part the tool can't do for you: the angle you bring before AI ever gets the question." Keep the surrounding paragraphs and the "Creativity isn't just art" section intact.

- [ ] **Step 5.5: Update `openerrealworld` copy** (Build Your Advantage opener, component at ~10972). It now loses `seeingisntproof` and gains `humanedge` + `creativethinking`, and is the course's emotional landing. Any "you'll see..." preview copy must match the new contents and ending. Draft for approval.

- [ ] **Step 5.6: Finalize the three fresh opener bodies** (`OpenerWorkWithSection`, `OpenerCheckSection`, `OpenerProtectSection`) — replace all PLACEHOLDER copy with David-approved copy using the framings in spec SYSTEM 5.

- [ ] **Step 5.7 (optional, David's call): movement labels** on `openerinside` / `openeranswers`. If wanted, add a quiet hand-authored "Understand AI · 2 of 3" / "· 3 of 3" marker (NOT a `NN / 7` pill). Skip if David prefers no marker.

- [ ] **Step 5.8: Verify** (per-step gate) + read each rewritten lesson in-browser to confirm tone/voice continuity (editing-guideline: read surrounding content, match voice).

- [ ] **Step 5.9: Commit**

```bash
git add index.html
git commit -m "Restructure step 5: roadmap, opener copy, and cross-reference copy pass"
```

---

## Self-review

**Spec coverage:** SYSTEM 1 (Understand AI one entry) → Task 1.1. SYSTEM 2 (derived badges) → 1.4–1.7. SYSTEM 3 (SECTION_META) → 1.3 + 1.6. SYSTEM 4 (nav chain) → Tasks 2–4 (all 13 seams in the verified map, including the 3 corrections vs the spec's line refs). SYSTEM 5 (openers: 3 fresh, 4 retired incl. openertraps) → 1.2/1.6 + 5.5/5.6. SYSTEM 6 (Roadmap) → 5.1–5.3. SYSTEM 7 (cross-refs): creativethinking → 5.4; the "VERIFY" items (workchanges ~10127, ~13120, humanedge ~14106) and "SAFE" item (~6808) → covered by the Task 4/5 full click-throughs (confirm "you just saw" referents still precede; adjust in 5.x if not). Decisions list (pointer stores id; localStorage untouched) → verified, no task needed.

**Placeholder scan:** The only placeholders are the opener bodies, intentionally deferred to Task 5 under David's approval gate — flagged, not silent.

**Type/name consistency:** New ids `openerworkwith` / `openercheck` / `openerprotect` are used identically in `SECTION_GROUPS` (1.1), component `sectionId`s (1.2), `SECTION_META` (1.3), `SECTION_COMPONENTS` (1.6), and seam targets (#1/#3/#5). `partBadge` keys on `group.sections[0]` — consistent with the lead-opener-only badge rule.

**Open confirmations for execution** (not blockers): (a) confirm `validate()` is auto-invoked on load; (b) confirm `design-check.sh`'s checks match the in-app validator; (c) the three "VERIFY" cross-refs in SYSTEM 7 — adjust prose only if a "you just saw" referent no longer immediately precedes.
