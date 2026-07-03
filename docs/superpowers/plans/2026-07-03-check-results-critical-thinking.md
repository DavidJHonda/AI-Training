# Check the Results Rebuild + Critical Thinking Reorder — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Swap the last two Work with AI lessons (Check the Results before Critical Thinking) and rebuild Check the Results as a truth-first evaluation procedure per `docs/superpowers/specs/2026-07-03-check-results-critical-thinking-design.md`.

**Architecture:** Everything lives in the single-file app `index.html` (plain `React.createElement` calls, no build step, no test suite). Verification is: extract the main `<script>` body and `node --check` it, run `./design-check.sh`, and finally regenerate the two lesson PDFs (which also proves both lessons render headlessly). Components are reused, never restyled: `BodyP`, `SectionKicker`, `KeyInsight`, `ShowcaseBox`, `InnerCard`, `Takeaway`, `LessonRule`, `NextLessonGate`, plus the embeddable `AIStrengthsSection`, `VerifySection`, and `GoodEnoughTryIt`.

**Tech Stack:** Single-file HTML + React (no JSX — `React.createElement`), zsh scripts, headless Chrome PDF pipeline.

## Global Constraints

- All lesson code is in `/Users/davidobrien/Developer/GitHub/AI-Training/index.html`. Anchor edits on unique strings, NOT line numbers (they shift between tasks).
- The file mixes two call styles: some components alias `var E = React.createElement;` locally, others write `/*#__PURE__*/React.createElement` inline. When rewriting a whole function, the local `E` alias is fine; when editing lines inside an existing function, match that function's existing style exactly.
- House rules (from project memory): static boxes use the `BOX_TEXT`/`BOX_LABEL`/`BOX_CARD_TITLE` typography constants; TRY IT activities never get an `ActivityCounter` chip or replay/reset controls; no dated per-app capability claims; cut-but-reusable content goes to `docs/parking-lot.md` (never left commented out); run `./design-check.sh` and reconcile FLAGs before committing `index.html`.
- Syntax check command (run from the repo root; scratchpad dir may differ — any writable temp dir is fine):
  ```bash
  python3 -c "
  import re
  html = open('index.html').read()
  scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
  open('/tmp/page-check.js','w').write(max(scripts, key=len))
  " && node --check /tmp/page-check.js && echo SYNTAX_OK
  ```
  Expected output: `SYNTAX_OK`.
- Commit after every task. Commit messages end with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Spec deviations locked during planning (recorded in the spec's Addendum): the embedded `VerifySection` is KEPT as the how-to of the "factual + it matters" branch; the `GoodEnoughTryIt` TRY IT and the "True isn't enough" KeyInsight are KEPT in the draft-branch/next-steps region.

---

### Task 1: Reorder lessons and rewire gates

Pure mechanical rewiring: SECTION_GROUPS order, three `NextLessonGate`s, FAQ entry order. No content changes. The app must be fully navigable in the new order after this task alone.

**Files:**
- Modify: `index.html` (5 anchored edits)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: lesson order `… prompting → prompt → evaluating → critical → openerfoundations` that Tasks 2–3 assume. Gate labels: `"Next: Check the Results"` (on `prompt`), `"Next: Critical Thinking"` (on `evaluating`), `"Next: Foundations"` (on `critical`).

- [ ] **Step 1: Swap the ids in SECTION_GROUPS**

In the Work with AI group (unique anchor: `"questionsvaluable", "prompting", "prompt"`), replace:

```js
  sections: ["openerworkwith", "aivscode", "whatitdoesbest", "modelselection", "questionsvaluable", "prompting", "prompt", "critical", "evaluating"]
```

with:

```js
  sections: ["openerworkwith", "aivscode", "whatitdoesbest", "modelselection", "questionsvaluable", "prompting", "prompt", "evaluating", "critical"]
```

- [ ] **Step 2: Rewire the Context Window lesson's gate**

Inside `PromptSection`'s ending (unique anchor: `completeAndNavigate("critical"); }, label: "Next: Critical Thinking"`), replace:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: labCheckedCount >= LAB_STEPS.length, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("critical"); }, label: "Next: Critical Thinking" }));
```

with:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: labCheckedCount >= LAB_STEPS.length, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("evaluating"); }, label: "Next: Check the Results" }));
```

- [ ] **Step 3: Rewire CriticalThinkingSection's gate**

Unique anchor: `problemAnswers).length >= CT_101.length && Object.keys(habitAnswers)` inside the `NextLessonGate` call. Replace:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: Object.keys(problemAnswers).length >= CT_101.length && Object.keys(habitAnswers).length >= CT_CONCEPTS.length, onClick: () => props.completeAndNavigate && props.completeAndNavigate("evaluating"), label: "Next: Check the Results" }));
```

with:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: Object.keys(problemAnswers).length >= CT_101.length && Object.keys(habitAnswers).length >= CT_CONCEPTS.length, onClick: () => props.completeAndNavigate && props.completeAndNavigate("openerfoundations"), label: "Next: Foundations" }));
```

- [ ] **Step 4: Rewire EvaluatingSection's gate**

Unique anchor: `completeAndNavigate("openerfoundations"), label: "Next: Foundations"` inside `EvaluatingSection` (it is the only gate with that target besides the one just created in Step 3 — so do Step 4 by matching the FULL line below, which is unique because of `ready: true`). Replace:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: true, onClick: () => props.completeAndNavigate && props.completeAndNavigate("openerfoundations"), label: "Next: Foundations" }));
```

with:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: true, onClick: () => props.completeAndNavigate && props.completeAndNavigate("critical"), label: "Next: Critical Thinking" }));
```

NOTE: Task 2 rewrites this whole function and preserves this gate; Step 4 still matters so the app is consistent if Task 2 is reviewed/landed separately.

- [ ] **Step 5: Swap the two FAQ entries to match lesson order**

Unique anchor: `How do I question an answer that sounds right?`. Replace:

```js
          { question: "How do I question an answer that sounds right?", lessonId: "critical" },
          { question: "Is the answer right, and good enough for what I need?", lessonId: "evaluating" }
```

with:

```js
          { question: "Is the answer right, and good enough for what I need?", lessonId: "evaluating" },
          { question: "How do I question an answer that sounds right?", lessonId: "critical" }
```

- [ ] **Step 6: Syntax check**

Run the Global Constraints syntax check. Expected: `SYNTAX_OK`.

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Work with AI: Check the Results now precedes Critical Thinking

Reorder SECTION_GROUPS, rewire the three lesson gates, and match the
FAQ entry order. Content changes land separately.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Rebuild EvaluatingSection (Check the Results)

Replace the whole function body with the spec's flow: opener → Read → Understand → Validate (two false statements) → Decide (task type × stakes, with the relocated `AIStrengthsSection` as practice) → go deeper factual (citations/currency/professional + embedded `VerifySection`) → go deeper drafts (+ kept `KeyInsight` "True isn't enough") → next steps (Use it / Fix it / Walk away + kept `GoodEnoughTryIt`) → gate.

**Files:**
- Modify: `index.html` — the entire `function EvaluatingSection(props) { … }` (currently ~line 7417 to the closing `}` right before `function CreativeThinkingSection`), including deleting the `ITERATION_STEPS` const.

**Interfaces:**
- Consumes: shared components listed in Architecture; `AIStrengthsSection`, `VerifySection`, `GoodEnoughTryIt` all accept `{ embedded: true, completeAndNavigate, markComplete, onNavigate }` (GoodEnoughTryIt takes no props); typography constants `BOX_TEXT`, `BOX_LABEL`, `BOX_CARD_TITLE`; gate target `"critical"` from Task 1.
- Produces: nothing later tasks call; Task 4's parking-lot entry describes what this task deletes.

- [ ] **Step 1: Replace the function**

Delete everything from `function EvaluatingSection(props) {` through its final `}` (the line right before `function CreativeThinkingSection(props) {`), and insert:

```js
function EvaluatingSection(props) {
  var E = React.createElement;
  var VALIDATE_CLAIMS = [
    {
      label: "YOU CATCH IT",
      claim: "The American Civil War started in 1083, on the border of England and Argentina.",
      body: "Everything you’ve ever learned about the Civil War contradicts this: the century, the country, the geography. You don’t need to look anything up. Your own knowledge catches it instantly."
    },
    {
      label: "IT SLIPS PAST",
      claim: "Maria Petronoski won 3 gold medals at the 1932 Olympics in Athens.",
      body: "Nothing about this sounds wrong. But the 1932 Games were in Los Angeles, not Athens, and Maria Petronoski doesn’t exist. Unless you happen to know Olympic history, “sounds fine to me” waves it right through."
    }
  ];
  var NEXT_MOVES = [
    { icon: "✅", title: "Use it", desc: "It passed your checks. Most answers end here. Read, understood, validated, done." },
    { icon: "🔧", title: "Fix it", desc: "Something’s off and you can name it. Say exactly what’s wrong in a follow-up: “cut the stat I never gave you,” “make it shorter.” Being specific about what’s wrong beats starting over." },
    { icon: "🚪", title: "Walk away", desc: "Wrong tool, or stakes too high. Do it yourself, or take it to a person who actually knows: a teacher, a doctor, a pro." }
  ];
  return E("div", null,
    E(LessonHeader, { sectionId: "evaluating" }),
    E(BodyP, null,
      "By now you’ve seen it yourself: AI makes mistakes. It states wrong facts in the same confident voice it states right ones. So what do you do with an AI answer, knowing it might be wrong?"),
    E(BodyP, null,
      "One option is to ignore AI entirely. Nobody who’s made it this far in the course is doing that: AI is too powerful to leave on the shelf. The real move is in between trusting and dismissing. ",
      E("strong", null, "You evaluate the results"),
      ", every time, with a process. Here it is."),
    E(SectionKicker, null, "First, read it"),
    E(BodyP, null,
      "This sounds too obvious to write down, and yet: weak AI users take AI’s output and share it without reading it. They paste it into the assignment, drop it in the group chat, hit send. Reading every word is the floor. Every other check in this lesson builds on it."),
    E(SectionKicker, null, "Understand what it’s saying"),
    E(BodyP, null,
      "You’ll never know whether an answer is right if you don’t understand what it says. If a paragraph uses a term you don’t know, or a step you can’t follow, that’s not a reason to skip it. It’s a reason to stop."),
    E(KeyInsight, { lead: "If something is unclear, ask." },
      "The fastest explainer of an AI answer is the same AI. “Explain the second paragraph in simpler terms” costs you one message, and now you can actually judge what it said."),
    E(SectionKicker, null, "Validate it against what you know"),
    E(BodyP, null,
      "As you read, hold the answer up against your own knowledge. This is where everything you’ve ever learned pays off. Try it on these two AI statements. Both are false. Watch how differently they fail."),
    E(ShowcaseBox, { kicker: "TWO FALSE STATEMENTS", marginBottom: 20 },
      E("div", { style: { display: "flex", gap: 14, flexWrap: "wrap" } },
        VALIDATE_CLAIMS.map(function(c, i) {
          return E("div", {
            key: i,
            style: { flex: 1, minWidth: 240, background: "var(--card)", border: "1px solid var(--rule)", borderRadius: 12, padding: "16px 18px" }
          },
            E("div", { style: { fontFamily: "var(--sans)", fontSize: BOX_LABEL, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.14em", color: "var(--seeAccent)", marginBottom: 8 } }, c.label),
            E("div", { style: { fontFamily: "var(--serif)", fontSize: 17, color: "var(--ink)", lineHeight: 1.5, marginBottom: 10, fontStyle: "italic" } }, "“" + c.claim + "”"),
            E("div", { style: { fontSize: BOX_TEXT, color: "var(--inkSoft)", lineHeight: 1.55 } }, c.body));
        }))),
    E(BodyP, null,
      "The first statement shows why learning still matters in the AI era: a well-stocked head is your fastest fact-checker. The second shows its limit. When the topic is beyond what you know, “it sounds fine” isn’t validation, and you’ll need the deeper checks below. Hold that thought; the next lesson comes back to it."),
    E(SectionKicker, null, "Decide: does it need more?"),
    E(BodyP, null,
      "You’ve read it, understood it, and validated what you could. Before going deeper, ask two quick questions."),
    E(ShowcaseBox, { kicker: "THE TWO-QUESTION GATE", marginBottom: 20 },
      E("div", { style: { display: "flex", gap: 14, flexWrap: "wrap" } },
        [{
          icon: "📋",
          title: "1. What kind of task was this?",
          desc: "Factual work (research, real events, claims about the world) gets checked against the world. Generative work (first drafts, brainstorms) gets checked against what you asked for. Different task, different follow-up."
        }, {
          icon: "⚖️",
          title: "2. How much is riding on it?",
          desc: "Picking a movie for tonight? If it passed your read-through, you’re done. A college entrance essay, a health question, anything with your name on it? Keep going."
        }].map(function(item, i) {
          return E("div", {
            key: i,
            style: { flex: 1, minWidth: 240, background: "var(--card)", border: "1px solid var(--rule)", borderRadius: 12, padding: "16px 18px" }
          },
            E("div", { style: { fontSize: 24, marginBottom: 8 } }, item.icon),
            E("div", { style: { fontWeight: 700, fontSize: BOX_TEXT, color: "var(--ink)", marginBottom: 4 } }, item.title),
            E("div", { style: { fontSize: 13, color: "var(--inkSoft)", lineHeight: 1.5 } }, item.desc));
        }))),
    E(BodyP, null,
      "Notice what this means: ",
      E("strong", null, "sometimes read, understand, validate is all you do"),
      ". Low stakes and it held up? Use it and move on. The deeper checks are for answers that matter."),
    E(AIStrengthsSection, { embedded: true, completeAndNavigate: props.completeAndNavigate, markComplete: props.markComplete, onNavigate: props.onNavigate }),
    E(SectionKicker, null, "Go deeper: facts that matter"),
    E(BodyP, null,
      "A factual answer with real stakes needs evidence, not vibes. Three checks:"),
    E(BodyP, null,
      E("strong", null, "Check the citations. "),
      "AI got its information from somewhere. Reply with: “Give me citations in your response.” The answer comes back with links to the pages behind it. Then, and this is the part people skip, click a link and read the page. Does it actually say what the AI claims?"),
    E(BodyP, null,
      E("strong", null, "Check that it’s current. "),
      "As you’ll learn in the Training lesson, models have a training cut-off date: a point after which they know nothing. For anything recent (prices, standings, versions, news), ask the AI to run a web search and update its answer."),
    E(BodyP, null,
      E("strong", null, "Know when it’s not AI’s call. "),
      "Some questions deserve a professional, not a chatbot: medical symptoms, legal trouble, a mental-health crisis. AI can help you prepare questions for that person. It shouldn’t replace them."),
    E(BodyP, null,
      "Those three checks are the habit. The strategies below are the skill: how to verify a specific claim when it really counts."),
    E(VerifySection, { embedded: true, completeAndNavigate: props.completeAndNavigate, markComplete: props.markComplete, onNavigate: props.onNavigate }),
    E(SectionKicker, null, "Go deeper: drafts that matter"),
    E(BodyP, null,
      "A draft or brainstorm doesn’t need a citation trail. But it isn’t exempt from checking, because AI pads generative work with things you never said. For a draft that matters, ask three questions: does it do what I actually asked, does it fit the person who’ll read it, and did AI slip in any “facts” I never gave it? That last one is sneaky: ask for a game recap and it will happily invent the score of the third quarter."),
    E(KeyInsight, { lead: "True isn’t enough." }, "The real question is whether the answer is good enough for what you’re about to do with it. A correct sentence in the wrong tone, at the wrong length, missing the point of your question, still fails."),
    E(SectionKicker, null, "Then make your move"),
    E(BodyP, null,
      "Every evaluation ends in one of three moves."),
    E(ShowcaseBox, { kicker: "THREE MOVES", marginBottom: 20 },
      E("div", { style: { display: "flex", gap: 14, flexWrap: "wrap" } },
        NEXT_MOVES.map(function(item, i) {
          return E("div", {
            key: i,
            style: { flex: 1, minWidth: 200, background: "var(--card)", border: "1px solid var(--rule)", borderRadius: 12, padding: "16px 18px" }
          },
            E("div", { style: { fontSize: 24, marginBottom: 8 } }, item.icon),
            E("div", { style: { fontWeight: 700, fontSize: BOX_TEXT, color: "var(--ink)", marginBottom: 4 } }, item.title),
            E("div", { style: { fontSize: 13, color: "var(--inkSoft)", lineHeight: 1.5 } }, item.desc));
        }))),
    E(GoodEnoughTryIt, null),
    E(LessonRule, null),
    E(NextLessonGate, { ready: true, onClick: () => props.completeAndNavigate && props.completeAndNavigate("critical"), label: "Next: Critical Thinking" }));
}
```

What this deletes (Task 4 records it in the parking lot): the `ITERATION_STEPS` const (3-round basketball walkthrough), the "WHY EVALUATION MATTERS" 2-card box, the "Use these six criteria" + "refine and try again" BodyPs, the "HOW TO REFINE" 3-card box, the "Prompt → Evaluate → Refine" ShowcaseBox rendering + its Takeaway, and the old opener BodyP ("Is this actually good enough to use?").

What this keeps: the `AIStrengthsSection` embed (moved from lesson top to after Decide), the `VerifySection` embed (moved into the factual branch with a lead-in), `GoodEnoughTryIt`, the "True isn't enough" KeyInsight, the gate.

- [ ] **Step 2: Syntax check**

Run the Global Constraints syntax check. Expected: `SYNTAX_OK`.

- [ ] **Step 3: Design check**

Run: `./design-check.sh` — reconcile any FLAG lines it prints (fix or consciously accept each; do not commit with unexplained FLAGs).

- [ ] **Step 4: Render check**

```bash
bash scripts/make-lesson-pdfs.sh evaluating
```
Expected: `check-the-results.pdf` regenerates without error (proves the lesson renders). The PDF content gets its final regeneration in Task 6; this run is just a smoke test.

- [ ] **Step 5: Commit**

```bash
git add index.html packets/lessons/check-the-results.pdf
git commit -m "$(cat <<'EOF'
Check the Results: rebuild as truth-first evaluation procedure

Read -> Understand -> Validate (two false statements that fail
differently) -> two-question Decide gate (task type x stakes) ->
go-deeper branches (factual: citations/currency/professional +
embedded VerifySection; drafts: match-the-ask checks) -> Use it /
Fix it / Walk away. AIStrengths scenario quiz moves from unexplained
preamble to Decide-step practice. Refine-loop material cut (parked
separately).

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Critical Thinking repositioning retouch

Three surgical text edits inside `CriticalThinkingSection`: opener receives the handoff, "Know Your Limits" pays off the Petronoski example, closer bridges to Understand AI. This function uses the inline `/*#__PURE__*/React.createElement` style — match it.

**Files:**
- Modify: `index.html` — three anchored edits inside `CriticalThinkingSection`

**Interfaces:**
- Consumes: Task 2's Petronoski example (the payoff references it by name); Task 1's gate (already points to `openerfoundations`).
- Produces: nothing downstream.

- [ ] **Step 1: Retouch the opener**

Unique anchor: `A sharper question gets you a better answer`. Replace the first `BodyP`:

```js
/*#__PURE__*/React.createElement(BodyP, null, "A sharper question gets you a better answer, but not a guaranteed one. ", /*#__PURE__*/React.createElement("strong", null, "Critical thinking"), " is what you do with the answer that comes back: not taking it at face value. AI makes you faster at both good work and bad work, and the difference is whether you question the output before you use it."),
```

with:

```js
/*#__PURE__*/React.createElement(BodyP, null, "You now have a process for an AI answer: read it, understand it, validate it, decide how deep to go. ", /*#__PURE__*/React.createElement("strong", null, "Critical thinking"), " is where that process comes from, and it’s bigger than AI. It works on a chatbot’s answer, a TikTok claim, a friend’s hot take, a headline. AI makes you faster at both good work and bad work, and the difference is whether you question the output before you use it."),
```

- [ ] **Step 2: Pay off the Petronoski hook in "Know Your Limits"**

Unique anchor: `The further the topic is from what you know, the more carefully you have to verify.` — it appears TWICE in the file: once in `CT_CONCEPTS` (near `id: "unknowns"`, with a `scenario` object) and once in the `HABITS_OVERVIEW` array inside the lesson body. Edit the `HABITS_OVERVIEW` one (it's the one on a line starting `{ id: "unknowns", icon:`). Replace:

```js
      { id: "unknowns", icon: "🧐", label: "Know Your Limits", lead: "If you can’t evaluate it, you’re flying blind.", detail: "The further the topic is from what you know, the more carefully you have to verify. That’s exactly when AI feels most authoritative." },
```

with:

```js
      { id: "unknowns", icon: "🧐", label: "Know Your Limits", lead: "If you can’t evaluate it, you’re flying blind.", detail: "Remember Maria Petronoski’s three gold medals? Perfectly plausible, completely made up. The further the topic is from what you know, the more carefully you have to verify, and that’s exactly when AI feels most authoritative." },
```

- [ ] **Step 3: Add the bridge to Understand AI before the closing rule**

Anchor: the lesson's final lines (the conditional Takeaway `In real life, the trap isn’t labeled.` followed by `E(LessonRule, null)` — in this function written as `/*#__PURE__*/React.createElement(LessonRule, null),`). Insert ONE new BodyP between the Takeaway conditional and the LessonRule call:

```js
  /*#__PURE__*/React.createElement(BodyP, null, "There’s one more level to this. Every habit on this list gets easier when you know what the machine on the other side is actually doing, because you can’t be fooled by something you understand. That’s exactly where this course goes next."),
```

So the ending reads: `…Takeaway conditional…` → new BodyP → `LessonRule` → `NextLessonGate`.

- [ ] **Step 4: Syntax + design check**

Run the Global Constraints syntax check (expected `SYNTAX_OK`), then `./design-check.sh` and reconcile FLAGs.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Critical Thinking: reposition as section closer

Opener receives the Check the Results handoff, Know Your Limits pays
off the Petronoski example, and a closing bridge points at Understand
AI.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Parking-lot entry for the cut refine-loop material

**Files:**
- Modify: `docs/parking-lot.md` (append one entry in the established format: origin / possible destination / supporting state / full source)

**Interfaces:**
- Consumes: knowledge of exactly what Task 2 deleted and the commit that deleted it.
- Produces: the historical record house rules require.

- [ ] **Step 1: Append the entry**

Append to `docs/parking-lot.md` (after the last entry, keeping the `---` separators):

```markdown
## "Prompt → Evaluate → Refine" — basketball-recap iteration walkthrough (+ usable-checklist framing)

- **Origin:** Check the Results lesson (`EvaluatingSection`). Removed 2026-07-03 when the lesson was rebuilt as a truth-first evaluation procedure (Read → Understand → Validate → Decide → go-deeper branches → Use it / Fix it / Walk away; spec: `docs/superpowers/specs/2026-07-03-check-results-critical-thinking-design.md`). The loop taught prompt-writing, the wrong altitude for an evaluation lesson — and The Art of Prompting couldn't absorb it either, since that lesson's thesis is "you don't need a prompting class, just three moves."
- **Possible destination:** a future dedicated "iterating with AI" lesson or lab; the walkthrough's round-2 beat (AI invents a "51-49 Lincoln lead" mid-draft and the learner catches it) is also a strong worked example for any hallucination-in-generative-work teaching.
- **Supporting state it needs if restored:** none — the `ITERATION_STEPS` array is a plain const rendered with shared components (`ShowcaseBox`, `InnerCard`, `UserBubble`, `AIBubble`, `Takeaway`), all still in `index.html`.
- **Full source:** in git history at the commit before the 2026-07-03 "Check the Results: rebuild" commit, inside `EvaluatingSection` — search anchor `ITERATION_STEPS`. The complete unit is: the 3-step `ITERATION_STEPS` const (generic prompt → refined prompt with invented-stat catch → Instagram-format polish), the "WHY EVALUATION MATTERS" ShowcaseBox (2 cards: "Correct doesn't mean usable" / "Evaluation tells you what to fix"), the "HOW TO REFINE" ShowcaseBox (3 cards: "Don't start over" / "Be specific about what's wrong" / "2–3 rounds is normal"), the "Prompt → Evaluate → Refine" ShowcaseBox that renders the steps with per-round 🔍 Evaluation / → Next Step callouts, and the Takeaway "Prompt. Evaluate. Refine. Repeat." Note the referenced six-criteria checklist ("Use these six criteria as a checklist") never existed in the code — only the sentence referring to it did.
```

- [ ] **Step 2: Commit**

```bash
git add docs/parking-lot.md
git commit -m "$(cat <<'EOF'
Parking lot: record cut Prompt->Evaluate->Refine walkthrough

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Update briefing.md lesson map

**Files:**
- Modify: `briefing.md` — the Work With AI line of the lesson map (regenerated from SECTION_GROUPS per house rules)

**Interfaces:**
- Consumes: Task 1's SECTION_GROUPS order.
- Produces: the up-to-date lesson map future sessions rely on.

- [ ] **Step 1: Update the Work With AI map line**

In `briefing.md`, replace:

```markdown
- **Work With AI (9):** Opener (openerworkwith), AI is Different (aivscode), Where AI Works Best (whatitdoesbest), Which App? (modelselection), Questions Matter (questionsvaluable), Art of Prompting (prompting), Context Window (prompt), Critical Thinking (critical), Check the Results (evaluating)
```

with:

```markdown
- **Work With AI (9):** Opener (openerworkwith), AI is Different (aivscode), Where AI Works Best (whatitdoesbest), Which App? (modelselection), Questions Matter (questionsvaluable), Art of Prompting (prompting), Context Window (prompt), Check the Results (evaluating), Critical Thinking (critical)
```

- [ ] **Step 2: Check for other stale briefing references**

Run: `grep -n "Check the Results\|Critical Thinking\|evaluating\|critical" briefing.md` and update any line that still describes the old order or the old lesson content (e.g., a lesson one-liner describing Check the Results as the usable/refine lesson). Rewrite such lines to match the rebuilt lesson; keep briefing style (one line per fact, no changelog).

- [ ] **Step 3: Commit**

```bash
git add briefing.md
git commit -m "$(cat <<'EOF'
briefing: Work With AI lesson map reflects reorder and rebuild

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Final verification + PDF regeneration

**Files:**
- Regenerate: `packets/lessons/check-the-results.pdf`, `packets/lessons/critical-thinking.pdf`

**Interfaces:**
- Consumes: all prior tasks landed.
- Produces: shippable artifacts + the proof both lessons render.

- [ ] **Step 1: Full design check**

Run `./design-check.sh`. Expected: no unreconciled FLAGs.

- [ ] **Step 2: Regenerate both lesson PDFs**

```bash
bash scripts/make-lesson-pdfs.sh evaluating critical
```

Expected output: `check-the-results.pdf` and `critical-thinking.pdf` regenerate, each `Done.` with a plausible px height (the old check-the-results was built from a much longer composite; height will change).

- [ ] **Step 3: Verify PDF content**

```bash
osascript -l JavaScript -e '
ObjC.import("PDFKit");
const check = (p, needles) => {
  const doc = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(p));
  const t = doc.string.js.toLowerCase();
  return needles.map(n => n + "=" + t.includes(n.toLowerCase()));
};
JSON.stringify({
  evaluating: check("/Users/davidobrien/Developer/GitHub/AI-Training/packets/lessons/check-the-results.pdf", ["Petronoski", "Walk away", "Give me citations"]),
  critical: check("/Users/davidobrien/Developer/GitHub/AI-Training/packets/lessons/critical-thinking.pdf", ["Petronoski", "where this course goes next"])
});
'
```

Expected: every needle `=true`. (The critical-thinking needles confirm the Task 3 retouches; the check-the-results needles confirm the new Validate example, the three moves, and the citations beat.)

- [ ] **Step 4: In-browser smoke test**

Serve the repo (`python3 -m http.server 8901`) and load `http://127.0.0.1:8901/index.html` in headless Chrome or a browser MCP tool; navigate to the Check the Results lesson and confirm: no console errors, the AIStrengths quiz renders after the two-question gate box, the VerifySection strategies render inside "Go deeper: facts that matter", and the gate reads "Next: Critical Thinking". Then check Critical Thinking's gate reads "Next: Foundations".

- [ ] **Step 5: Commit**

```bash
git add packets/lessons/check-the-results.pdf packets/lessons/critical-thinking.pdf
git commit -m "$(cat <<'EOF'
Regenerate Check the Results + Critical Thinking lesson PDFs

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
EOF
)"
```
