# AI Answers Source-First Reorder — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorder the AI Answers section source-first (Patterns before Probability/Inference) and merge the Prediction lesson into a single Inference "loop" lesson, going from 7 lessons to 6.

**Architecture:** Single-file React app (`index.html`, `React.createElement`). Lessons are component functions; order/labels come from `SECTION_GROUPS` (line ~1180) and `SECTION_META` (line ~1223); components are wired in an id→component map (line ~14327). Navigation is per-lesson `NextLessonGate` `completeAndNavigate(id)` calls. No build step, no unit tests — verification is `design-check.sh`, the in-app `validate()` console check, and click-through.

**Tech Stack:** Inline React (UMD), no bundler. Verification via `design-check.sh` (bash) and Playwright/manual browser check.

**Spec:** `docs/superpowers/specs/2026-05-29-ai-answers-source-first-reorder-design.md`

---

## Branch setup (do first)

Repo is on `main`. Create a feature branch before any commit:

```bash
git checkout -b ai-answers-source-first-reorder
```

## File structure

- `index.html` — all lesson edits (the only code file).
- `docs/parking-lot.md` — **created** in Task 1; holds the parked "Scale" activity.
- `briefing.md` — lesson-map line + total count, updated in Task 5.

## Target order (end state)

`openeranswers → prompt → patterns → probability → inference → whatitdoesbest` (6 lessons; `prediction` deleted, its Luke/Nate activity merged into `inference`).

---

### Task 1: Park "The Scale of What's Happening" and remove its dead code

**Files:**
- Create: `docs/parking-lot.md`
- Modify: `index.html` (InferenceSection, lines ~6268–6273 and ~6385–6413)

- [ ] **Step 1: Create the parking-lot file**

Create `docs/parking-lot.md` with:

````markdown
# Parking Lot — cut-but-keepable lesson content

Content removed from a lesson but worth reusing later. Each entry: what it is, where it came from, the verbatim source, and where it might go.

---

## "The Scale of What's Happening" — billions-of-calculations SEE IT

- **Origin:** AI Answers → Inference lesson (`InferenceSection`), removed 2026-05-29 during the source-first reorder to keep the merged Inference lesson from getting dense.
- **Possible destination:** back into Inference, or a future "why it feels instant / cost of inference" lesson.
- **Supporting state it needs if restored:** `computePhase` ("typing-q"), `computeQChars`, `computeAiWords`, `computeReveal` (useState) + the compute `useEffect`, plus `computeQuestion` / `computeAnswer` string vars.

Verbatim JSX (from InferenceSection):

```jsx
React.createElement(SectionKicker, null, "The Scale of What’s Happening"),
React.createElement(InteractiveBox, {
  variant: "see",
  surface: "sand",
  title: "Why it feels instant"
},
React.createElement(ActivityInstruction, null, "Watch what happens behind the scenes when you ask a simple question."),
React.createElement("div", { style: { display: "flex", flexDirection: "column", gap: 10, marginBottom: 16 } },
  React.createElement(UserBubble, { text: computeQuestion, visibleChars: computeQChars }),
  computePhase === "thinking" ? React.createElement(ThinkingBubble, null) : null,
  (computePhase === "typing-ai" || computePhase === "done") ? React.createElement(AIBubble, { text: computeAnswer, visibleWords: computeAiWords }) : null),
/* ...reveal button + stats rows (Tokens ~14, Dimensions thousands, Layers ~100, every token checks every other) + "≈ 100,000,000,000+ calculations" + "over 3,000 years" line... */ ),
React.createElement(KeyInsight, { lead: "Billions of calculations, all for one word." }, "Every word the model writes is its own fresh pass through the whole network. The speed is the magic trick. The math underneath is the real machine."),
```

> When restoring, copy the full block from git history at commit before the reorder (the `computeReveal` stats grid is abbreviated above). Search the pre-reorder `index.html` for `"Why it feels instant"`.
````

> Note: the abbreviation is acceptable here because the authoritative full source remains in git history; the entry records exactly where to find it.

- [ ] **Step 2: Remove the Scale activity block from `index.html`**

Delete the contiguous block in InferenceSection that begins with the SectionKicker and ends with the KeyInsight (currently lines ~6385–6413). Remove from:

```jsx
  /*#__PURE__*/React.createElement(SectionKicker, null, "The Scale of What’s Happening"),
```

through and including:

```jsx
  /*#__PURE__*/React.createElement(KeyInsight, { lead: "Billions of calculations, all for one word." }, "Every word the model writes is its own fresh pass through the whole network. The speed is the magic trick. The math underneath is the real machine."),
```

Leave the following `LessonRule` and `NextLessonGate` intact.

- [ ] **Step 3: Remove the now-dead compute state and vars**

In InferenceSection, delete these four hooks (lines ~6268–6271):

```jsx
  const [computePhase, setComputePhase] = useState("typing-q");
  const [computeQChars, setComputeQChars] = useState(0);
  const [computeAiWords, setComputeAiWords] = useState(0);
  const [computeReveal, setComputeReveal] = useState(false);
```

Delete the two string vars (lines ~6272–6273):

```jsx
  const computeQuestion = "How many times did Michael Jordan win the MVP in the NBA?";
  const computeAnswer = "Michael Jordan won the NBA Most Valuable Player award five times: 1988, 1991, 1992, 1996, and 1998. All five were with the Chicago Bulls.";
```

And delete the `useEffect` immediately following them that drives `computePhase`/`computeQChars`/`computeAiWords` (the block with `if (computePhase === "typing-q")` … `}, [computePhase, computeQChars, computeAiWords]);`).

- [ ] **Step 4: Verify no dangling references**

Run: `grep -n "computePhase\|computeQuestion\|computeAnswer\|computeReveal\|computeQChars\|computeAiWords\|Why it feels instant\|Scale of What" index.html`
Expected: **no matches** (all removed).

- [ ] **Step 5: Verify in browser**

Run: `bash design-check.sh` — expected: no new FLAGs vs. baseline.
Open `index.html`, navigate to Inference, confirm the lesson renders, "The Complete Journey" SEE IT still works, and there are no console errors. Run `validate()` in the console — expected: all lessons pass (count unchanged this task).

- [ ] **Step 6: Commit**

```bash
git add docs/parking-lot.md index.html
git commit -m "Park the Scale-of-inference SEE IT to docs/parking-lot.md"
```

---

### Task 2: Build the merged Inference lesson (relocate Luke/Nate + rewrite open/close)

**Files:**
- Modify: `index.html` (InferenceSection: hooks ~6240, open ~6320–6323, body after ~6384, closing before gate)

- [ ] **Step 1: Add Prediction's state hooks and effects to InferenceSection**

Immediately after the existing `stagesRevealed` hook (line ~6240):

```jsx
  const [stagesRevealed, setStagesRevealed] = useLocalStorage("seeit-inference-stagesRevealed", 0);
```

insert:

```jsx
  const [seeStep, setSeeStep] = useLocalStorage("seeit-prediction-step", 0);
  const [promptChars, setPromptChars] = useState(0);
  const [promptDone, setPromptDone] = useState(false);
  const [aiRespWords, setAiRespWords] = useState(0);
  const [aiRespDone, setAiRespDone] = useState(false);
  var seePromptText = "What car should I buy after I graduate from college?";
  var lukeRespText = "Great question, Luke. I definitely recommend a Jeep Cherokee.";
  var nateRespText = "I’m happy you asked this question, Nate. At this point in your life, I recommend the Ford Raptor.";
  var nateRespWordsArr = nateRespText.split(" ");
  useEffect(function() {
    if (seeStep < 1 || promptDone) return;
    if (promptChars >= seePromptText.length) { setPromptDone(true); return; }
    var iv = setInterval(function() { setPromptChars(function(c) { if (c >= seePromptText.length) { clearInterval(iv); return c; } return c + 1; }); }, 35);
    return function() { clearInterval(iv); };
  }, [seeStep, promptChars, promptDone]);
  useEffect(function() {
    if (seeStep < 5 || aiRespDone) return;
    var t = setTimeout(function() {
      var iv = setInterval(function() { setAiRespWords(function(w) { if (w >= nateRespWordsArr.length) { clearInterval(iv); setAiRespDone(true); return w; } return w + 1; }); }, 90);
    }, 500);
    return function() { clearTimeout(t); };
  }, [seeStep]);
```

> The `localStorage` key `seeit-prediction-step` is kept as-is so any in-progress student state still resolves.

- [ ] **Step 2: Rewrite the Inference opening paragraphs**

Replace the four opening BodyP lines (~6320–6323):

```jsx
React.createElement(BodyP, null, "You’ve learned what gets sent to AI: your prompt, plus everything else in the context window."),
  /*#__PURE__*/React.createElement(BodyP, null, "Now let’s map what AI does with all of that. The whole journey has a name: ", /*#__PURE__*/React.createElement("strong", null, "Inference"), "."),
  /*#__PURE__*/React.createElement(BodyP, null, "Inference is what happens every time you hit send. The trained model takes your prompt, runs it through its layers, predicts the next token, adds that token to the response, and repeats until the answer is complete."),
  /*#__PURE__*/React.createElement(BodyP, null, "It isn’t training again. It’s using what training already built."),
```

with:

```jsx
React.createElement(BodyP, null, "You’ve met the source (patterns) and one score (probability). Now chain it together."),
  /*#__PURE__*/React.createElement(BodyP, null, "The model picks a token, adds it to the response, and scores the next one — over and over until the answer is complete. The whole repeating journey has a name: ", /*#__PURE__*/React.createElement("strong", null, "Inference"), "."),
  /*#__PURE__*/React.createElement(BodyP, null, "It isn’t training again. It’s using what training already built — reading those frozen patterns back out, one token at a time."),
```

- [ ] **Step 3: Insert the Luke/Nate SEE IT after the Neural Network ShowcaseBox**

Find the end of the "Neural Network" `ShowcaseBox` (the BodyP ending `"…lives inside this one structure."` then the closing `)),` at ~6384). Immediately after that `)),` and before the `LessonRule`/`NextLessonGate`, insert the entire "Same question, different prediction" InteractiveBox copied verbatim from the current PredictionSection (lines ~5740–5873): the `React.createElement(InteractiveBox, { variant: "see", surface: "sand", title: "Same question, different prediction", action: …ActivityCounter… }, …RevealSequence… )` block.

> Copy it exactly as it appears in PredictionSection; it references `seeStep`, `setSeeStep`, `promptChars`, `promptDone`, `aiRespWords`, `aiRespDone`, `seePromptText`, `lukeRespText`, `nateRespText` — all added in Step 1.

- [ ] **Step 4: Add the merged closing KeyInsight**

Immediately after the inserted SEE IT and before `LessonRule`, add:

```jsx
  /*#__PURE__*/React.createElement(KeyInsight, { lead: "One answer. Many picks. Each one shapes what comes next." },
    "Pick the brand and the model options change. Pick the model and the next token changes. Every token along the way is its own fresh prediction, shaped by every pick before it."),
```

- [ ] **Step 5: Verify in browser**

Open `index.html` → Inference. Confirm: opening prose reads correctly; "The Complete Journey" SEE IT works; the Neural Network box renders; the "Same question, different prediction" SEE IT animates (prompt types, then 5 stages, then responses type); the merged KeyInsight shows. No console errors.

> The standalone Prediction lesson still exists and also shows Luke/Nate at this point — expected, removed in Task 3.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Merge Prediction's Luke/Nate walk into the Inference lesson"
```

---

### Task 3: Reorder the section, rewire navigation, delete Prediction

**Files:**
- Modify: `index.html` — `SECTION_GROUPS` (~1180), `SECTION_META` (~1226), opener groups (~6555–6586), four `NextLessonGate`s, PredictionSection (~5711–5878), component map (~14327)

- [ ] **Step 1: Reorder the section group and drop `prediction`**

Line ~1180, replace:

```jsx
  sections: ["openeranswers", "prompt", "inference", "probability", "prediction", "patterns", "whatitdoesbest"]
```

with:

```jsx
  sections: ["openeranswers", "prompt", "patterns", "probability", "inference", "whatitdoesbest"]
```

- [ ] **Step 2: Re-cluster the opener groups into the four new moves**

Replace the entire `groups: [ … ]` array in OpenerAnswersSection (~6555–6586) with:

```jsx
    groups: [
      {
        kicker: "PACKAGE THE INPUT",
        bridge: "Every turn, your input gets packaged.",
        questions: [
          { question: "What can the model see when it answers your prompt?", lessonId: "prompt" }
        ]
      },
      {
        kicker: "WHAT TRAINING LEFT BEHIND",
        bridge: "Inside the model sits one thing training wrote: patterns.",
        questions: [
          { question: "What one idea is the model actually built from?", lessonId: "patterns" }
        ]
      },
      {
        kicker: "READ IT INTO AN ANSWER",
        bridge: "The model reads those patterns out, token by token, into a full answer.",
        questions: [
          { question: "How does the model decide what might come next?", lessonId: "probability" },
          { question: "How do those picks chain into a whole answer?", lessonId: "inference" }
        ]
      },
      {
        kicker: "PUT IT TO WORK",
        bridge: "Finally, what all that machinery makes AI genuinely good at.",
        questions: [
          { question: "What is AI actually good at, and why?", lessonId: "whatitdoesbest" }
        ]
      }
    ],
```

- [ ] **Step 3: Rewire the four navigation gates**

Context Window gate (~6782): replace
```jsx
onClick: function() { props.completeAndNavigate && props.completeAndNavigate("inference"); }, label: "Next: Inference" }));
```
with
```jsx
onClick: function() { props.completeAndNavigate && props.completeAndNavigate("patterns"); }, label: "Next: Patterns" }));
```

Patterns gate (~6027–6028): replace
```jsx
      onClick: function() { props.completeAndNavigate && props.completeAndNavigate("whatitdoesbest"); },
      label: "Next: What AI Does Best"
```
with
```jsx
      onClick: function() { props.completeAndNavigate && props.completeAndNavigate("probability"); },
      label: "Next: Probability"
```

Probability gate (~4689): replace
```jsx
onClick: function() { props.completeAndNavigate && props.completeAndNavigate("prediction"); }, label: "Next: Prediction" }
```
with
```jsx
onClick: function() { props.completeAndNavigate && props.completeAndNavigate("inference"); }, label: "Next: Inference" }
```

Inference gate (currently `…("probability"), label: "Next: Probability"`, after the merged content): replace
```jsx
onClick: () => props.completeAndNavigate && props.completeAndNavigate("probability"), label: "Next: Probability" }));
```
with
```jsx
onClick: () => props.completeAndNavigate && props.completeAndNavigate("whatitdoesbest"), label: "Next: What AI Does Best" }));
```

- [ ] **Step 4: Delete the standalone Prediction lesson**

Delete the entire `function PredictionSection(props) { … }` (lines ~5711–5878), from `function PredictionSection(props) {` through its closing `}` after the `NextLessonGate`.

- [ ] **Step 5: Delete the Prediction SECTION_META entry**

Line ~1226, delete:
```jsx
  prediction: { kicker: "THE GUESSING GAME", label: "Prediction", icon: "🎯" },
```

- [ ] **Step 6: Delete the Prediction component mapping**

Line ~14327, delete:
```jsx
  prediction: PredictionSection,
```

- [ ] **Step 7: Verify no residual prediction references**

Run: `grep -n "PredictionSection\|\"prediction\"\|prediction:" index.html`
Expected: only incidental matches in unrelated data (e.g., the "Recommendations / Predicts what you might like" object around line 1371 which uses a `prediction:` data field). **No** matches for `PredictionSection`, the `"prediction"` lesson id in `sections`/nav, or the `prediction:` SECTION_META/component entries.

- [ ] **Step 8: Verify order and validation in browser**

Open `index.html`. Run `validate()` in the console — expected: all lessons pass, `sectionCount` reduced by one. Click the AI Answers section through end to end: opener → Context Window → Patterns → Probability → Inference → What AI Does Best. Confirm each "Next" lands on the correct next lesson and none reaches a missing `prediction`. Confirm the ProgressBar "X of N lessons" reflects the new total.

- [ ] **Step 9: Commit**

```bash
git add index.html
git commit -m "Reorder AI Answers source-first and remove the standalone Prediction lesson"
```

---

### Task 4: Rewrite the seam prose (handoffs)

**Files:**
- Modify: `index.html` — opener featured card (~6541–6543), Patterns open (~5908–5913) + closing insight (~6021–6022), Probability open (~4571–4578) + closing, Context Window closing.

- [ ] **Step 1: Reorder the opener featured-card preview list**

In OpenerAnswersSection featured card (~6543), replace the sentence:

```
You’ll see what gets packaged each turn, how the model runs it into an answer, the one idea that ties it all together, and what all of that makes AI genuinely good at.
```

with:

```
You’ll see what gets packaged each turn, the patterns training left inside the model, how it reads them into an answer token by token, and what all of that makes AI genuinely good at.
```

- [ ] **Step 2: Rewrite the Patterns opening (forward-looking)**

Replace (~5912–5913):

```jsx
React.createElement(BodyP, null,
      "This section has been about patterns the whole time. Now let’s name the thread. A pattern is a learned tendency: when this kind of input shows up in this kind of context, this kind of output tends to fit."),
```

with:

```jsx
React.createElement(BodyP, null,
      "Everything after this — the scoring, the picking, the whole answer — is this one idea in motion. Let’s name it first. A pattern is a learned tendency: when this kind of input shows up in this kind of context, this kind of output tends to fit."),
```

> The Luke/Nate opening lines just above (~5908–5911) stay — Context Window still introduces Luke/Nate one lesson earlier, so the callback holds.

- [ ] **Step 3: Rewrite the Patterns closing KeyInsight (forward promise)**

Replace (~6021–6022):

```jsx
React.createElement(KeyInsight, { lead: "Probability is the score. Prediction is the action. Patterns are the source." },
      "Probability scores each next token. Prediction acts on those scores, one token after another. Patterns are where the scores come from, the learned tendencies that training writes and inference reads."),
```

with:

```jsx
React.createElement(KeyInsight, { lead: "Patterns are the source." },
      "They’re where every score comes from — the learned tendencies that training writes and inference reads. Next you’ll watch them get read out: first as a score for one token, then chained into a whole answer."),
```

- [ ] **Step 4: Rewrite the Probability opening**

Replace (~4571–4575):

```jsx
React.createElement(BodyP, null,
      "You just saw Inference. Stage 5 was where the model scores every possible next token and picks one."
    ),
    /*#__PURE__*/React.createElement(BodyP, null,
      "That step has its own name: probability. And it’s worth slowing down because it’s the single move AI repeats for every word in every response you’ve ever seen."
    ),
```

with:

```jsx
React.createElement(BodyP, null,
      "You just saw what training leaves behind: patterns, stored as connection strengths between tokens. Now watch one get read. When the model needs the next token, it turns those strengths into scores."
    ),
    /*#__PURE__*/React.createElement(BodyP, null,
      "That step has its own name: probability. And it’s worth slowing down because it’s the single move AI repeats for every word in every response you’ve ever seen."
    ),
```

- [ ] **Step 5: Rewrite the Probability closing into a loop setup**

Locate the closing element directly above the Probability `NextLessonGate` (~4689) — the final KeyInsight/BodyP of the lesson. Append (or adjust the last BodyP to) a loop hand-off. Add this BodyP immediately before the `LessonRule`/`NextLessonGate`:

```jsx
  /*#__PURE__*/React.createElement(BodyP, null,
    "That’s one token’s score. But an answer is hundreds of tokens. Next: how one score becomes a whole answer."),
```

- [ ] **Step 6: Add the Context Window inward handoff**

In PromptSection, immediately before the closing `NextLessonGate` (~6782) and after the existing `KeyInsight` ("Same question, different answer…"), add:

```jsx
  /*#__PURE__*/React.createElement(BodyP, null,
    "You’ve seen what the model can see. Next: the one thing inside the model that turns all of it into an answer."),
```

- [ ] **Step 7: Verify in browser**

Open `index.html`, read through opener → Context Window → Patterns → Probability → Inference. Confirm every handoff sentence reads cleanly into the next lesson, no reference points backward to a lesson that now comes later, and no console errors.

- [ ] **Step 8: Commit**

```bash
git add index.html
git commit -m "Rewrite AI Answers seam prose for the source-first order"
```

---

### Task 5: Update briefing.md

**Files:**
- Modify: `briefing.md` (line 12, and the "71 lessons" total on line 6/7)

- [ ] **Step 1: Rewrite the AI Answers lesson-map line**

Replace line 12:

```
- AI Answers (7): Opener (openeranswers), Your Input & the Context Window (prompt), Inference: From Prompt to Output (inference), Probability (probability), Prediction (prediction), Patterns (patterns), What AI Does Best (whatitdoesbest)
```

with:

```
- AI Answers (6): Opener (openeranswers), Your Input & the Context Window (prompt), Patterns (patterns), Probability (probability), Inference: From Prompt to Output (inference), What AI Does Best (whatitdoesbest)
```

- [ ] **Step 2: Bump the total lesson count**

Find the "71 lessons" reference (line ~7: "71 lessons across 10 section groups") and change `71` to `70`.

Run: `grep -n "71 lessons\|71 " briefing.md` first to confirm the exact location; update to `70`.

- [ ] **Step 3: Commit**

```bash
git add briefing.md
git commit -m "Sync briefing.md with the AI Answers reorder (7 to 6 lessons)"
```

---

### Task 6: Final verification

**Files:** none (verification + any FLAG fixes)

- [ ] **Step 1: Run design-check and reconcile**

Run: `bash design-check.sh`
Reconcile every FLAG it raises (per the run-design-check-before-commit rule). If a FLAG requires an `index.html` change, make it and re-run until clean.

- [ ] **Step 2: Full in-app validation**

Open `index.html`. In console run `validate()` — expected: "all N lessons pass structural checks" with N reduced by one from the pre-change count. Confirm 0 errors.

- [ ] **Step 3: Click-through (Playwright or manual)**

Navigate the entire AI Answers section in order, completing each activity enough to unlock each gate: opener → prompt → patterns → probability → inference → whatitdoesbest, then confirm whatitdoesbest's "Next" still leads to the Workflow opener (`openerusing`). Confirm no broken nav, no console errors, animations run.

- [ ] **Step 4: Final residual-reference sweep**

Run: `grep -rn "prediction" index.html briefing.md | grep -vi "predicts\|prediction:.*Predicts\|Recommendations"`
Expected: no lesson-level `prediction` id, component, meta, or nav references remain.

- [ ] **Step 5: Commit any verification fixes**

```bash
git add -A
git commit -m "Reconcile design-check FLAGs after AI Answers reorder"
```

(Skip if no changes were needed.)

---

## Self-review notes

- **Spec coverage:** target arc (Task 3 §1-2), opener reframe (Task 3 §2, Task 4 §1), all five seam rewrites (Task 4), merged Inference incl. kept activities + parked Scale (Tasks 1–2), wiring deletes (Task 3), briefing sync (Task 5), design-check + validate + click-through (Task 6). All spec sections map to a task.
- **Naming consistency:** the relocated hooks (`seeStep`, `promptChars`, `promptDone`, `aiRespWords`, `aiRespDone`) and the localStorage key `seeit-prediction-step` are used identically in Task 2 Step 1 (definition) and the SEE IT block (Task 2 Step 3, consumer). The Inference gate edited in Task 2 (still `probability`) is the same gate rewired in Task 3 Step 3 (to `whatitdoesbest`) — sequence is intentional.
- **Note for the executor:** line numbers drift as edits land; always match on the quoted strings, not the line numbers.
