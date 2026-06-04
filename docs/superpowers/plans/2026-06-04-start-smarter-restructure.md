# Start Smarter Restructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Relocate the AI Primer's loop into "What is AI?", split the overloaded "What is AI?" into single-purpose lessons (adding a new "You Already Use AI"), move the next-word-prediction + generative content into "What's an LLM?", and delete the standalone Primer.

**Architecture:** Single-file inline-React app (`index.html`, `React.createElement`, no JSX/build). Lessons are functions registered in `SECTION_GROUPS` (~1206), `SECTION_META` (~1228), `SECTION_COMPONENTS` (~13534); `SECTIONS` derives from these. Tasks are ordered so destination lessons are filled BEFORE source lessons are trimmed — content is never missing in an intermediate state (temporary duplication is fine and resolved by later tasks).

**Tech Stack:** HTML + inline React + design tokens. Verification gates: `bash design-check.sh`, the in-app `validate()` consistency checker (logs to console), and browser render. No unit-test framework — do NOT invent one.

**Spec:** `docs/superpowers/specs/2026-06-04-start-smarter-restructure-design.md`

**Global copy rules (every new/adapted line):**
- Everyday language; keep Start Smarter approachable.
- **No em-dashes (—).** `design-check.sh` baselines em-dashes at 4; any new one FLAGs. Use colons/commas.
- Reuse existing components; never hand-build counter pills or raw surfaces (would FLAG design-check).
- Use the Edit tool with unique anchors; never sed/echo/cat to edit `index.html`.

**Source-block convention:** several tasks MOVE existing JSX. The plan gives the exact source function + identifying anchors + transform instructions rather than re-pasting hundreds of lines (the code already exists in the file). Copy the block verbatim from the named source unless told to change something.

---

## File structure

Only `index.html` (code) + `briefing.md` + `docs/parking-lot.md` (docs) change.

New lesson id: `youalreadyuse` → function `YouAlreadyUseSection`.
Removed lesson id: `primer` → function `PrimerSection` (deleted).
Modified lessons: `aihistory` (What is AI?), `llms` (What's an LLM?), `openerfoundations` (recap).

---

## Task 1: Add the prediction pieces to What's an LLM?

Fill the first destination. Copy the Primer's bar-chart worked example and "Guess the Most Probable Word" TRY IT into `LLMsSection`. The Primer still exists (deleted in Task 5), so this is temporary duplication.

**Files:**
- Modify: `index.html` — `LLMsSection` (grep `function LLMsSection`).
- Source (read-only): `PrimerSection` (grep `function PrimerSection`).

- [ ] **Step 1: Add the activity state + data to LLMsSection**

Inside `LLMsSection`, immediately after the existing `var revealLlmLetter = ...` line (the last state line before the `useEffect`), insert the `phrases` array and the guess-activity hooks copied VERBATIM from `PrimerSection` — specifically these lines from PrimerSection: the `const phrases = [ ... ];` array (3 phrase objects) and the hooks `const [phraseIdx, setPhraseIdx] = useState(0);` through `const nextPhrase = function() { ... };` (i.e. phraseIdx, guess, revealed, viewWord, seenWords, phrase, topWord, guessedCorrectly, handleGuess, isLastPhrase, nextPhrase). Paste them unchanged.

- [ ] **Step 2: Insert the bar-chart worked example**

In `LLMsSection`'s returned tree, find the close of the "LLM, decoded" InteractiveBox (the SEE IT that ends just before `React.createElement(SectionKicker, null, "PRODUCT")`). Immediately BEFORE that `SectionKicker "PRODUCT"`, insert a lead-in paragraph and the bar-chart `ShowcaseBox` copied VERBATIM from `PrimerSection` (the `React.createElement(ShowcaseBox, { headline: "How the model picks the next word", ... }, ...)` block — from `React.createElement(ShowcaseBox,` through its matching close, the block whose final visible text is "...until the answer is complete."). Prepend this lead-in paragraph:

```js
    /*#__PURE__*/React.createElement(SectionKicker, null, "PREDICTING THE NEXT WORD"),
    /*#__PURE__*/React.createElement(BodyP, null, "That autocomplete on your phone is the whole idea in miniature. An LLM does the same thing on a far bigger scale: given the words so far, it scores how likely each possible next word is, and picks from the top. Here is what those scores look like up close."),
```

(Then the copied ShowcaseBox.)

- [ ] **Step 3: Insert the Guess the Most Probable Word TRY IT**

Immediately after the bar-chart ShowcaseBox you just inserted (still before `SectionKicker "PRODUCT"`), insert a lead-in paragraph and the TRY IT `InteractiveBox` copied VERBATIM from `PrimerSection` (the `React.createElement(InteractiveBox, { variant: "try", surface: "mint", title: "Guess the Most Probable Word", ... }, ...)` block through its matching close, including the inner quiz `div`, the reveal branches, the "Next Phrase" button, and the dots). It references the state you added in Step 1. Prepend:

```js
    /*#__PURE__*/React.createElement(BodyP, null, "Try the prediction step yourself, on three short phrases. Pick the word you think is most likely, then see the scores."),
```

- [ ] **Step 4: Gate the lesson on the new activity too**

`LLMsSection`'s `NextLessonGate` currently has `ready: Object.keys(llmRevealed).length >= LLM_COLS.length`. Change it to also require finishing the guess activity:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: Object.keys(llmRevealed).length >= LLM_COLS.length && isLastPhrase && revealed, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("doesaithink"); }, label: "Next: Does AI Think?" })
```

- [ ] **Step 5: Verify**

Run: `bash design-check.sh` → expect `PASS - no new drift against baselines.`
Browser: open What's an LLM?. Confirm the LLM-decoded SEE IT still works, then the new bar chart renders, then the Guess activity runs (3 phrases, counter "X of 3"), and the Next card unlocks only after both the decode and the third guess are done. Console: no validate() errors. Confirm no em-dash was introduced (`git diff -- index.html | grep -c '^+.*—'` → 0).

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Add next-word-prediction pieces (bar chart + guess activity) to What's an LLM?

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Add generative AI + the stored-vs-built SEE IT to What's an LLM?

Complete Part 1 of the LLMs lesson by moving the generative-AI content (currently in `AIHistorySection`). Still duplicated until Task 4 trims What is AI?.

**Files:**
- Modify: `index.html` — `LLMsSection`.
- Source (read-only): `AIHistorySection` (grep `function AIHistorySection`) — the `SectionKicker "GENERATIVE AI"` block, the two paragraphs after it, and the `InteractiveBox` titled "Stored Answers vs. Built From Probability" with its `revealStep`/`askCount`/`seeComplete` state.

- [ ] **Step 1: Add the generative-demo state to LLMsSection**

Inside `LLMsSection`, after the activity hooks added in Task 1, add the three state hooks the stored-vs-built SEE IT needs, copied from `AIHistorySection` but with `llms` localStorage keys (so they do not collide with the originals that still exist until Task 4):

```js
  var _rs = useLocalStorage("seeit-llms-twoSystemsRevealStep", 0), revealStep = _rs[0], setRevealStep = _rs[1];
  var _aa = useLocalStorage("seeit-llms-twoSystemsAskCount", 0), askCount = _aa[0], setAskCount = _aa[1];
  var _sc = useState(false), seeComplete = _sc[0], setSeeComplete = _sc[1];
```

- [ ] **Step 2: Insert the generative-AI prose + SEE IT**

In `LLMsSection`, immediately AFTER the Guess TRY IT (from Task 1) and still BEFORE `SectionKicker "PRODUCT"`, insert: the `SectionKicker "GENERATIVE AI"` + the two generative paragraphs + the "Stored Answers vs. Built From Probability" `InteractiveBox`, all copied VERBATIM from `AIHistorySection`. Copy the block that starts at `React.createElement(SectionKicker, null, "GENERATIVE AI")` through the close of the InteractiveBox (the one whose Takeaway headline is "Same question. Different games."). It references `revealStep/askCount/seeComplete` (added in Step 1) and the global `CompareCard`, `TypingAICard`, `Takeaway`. Do not change its internals.

Optionally prepend one bridge line so generative AI follows naturally from prediction:

```js
    /*#__PURE__*/React.createElement(BodyP, null, "Predicting the next word is powerful for one reason: chained together, those predictions do not just finish your sentence, they build something new."),
```

- [ ] **Step 3: Make the two movements explicit**

So the now-large lesson reads as two parts, add a section header right before `SectionKicker "PRODUCT"`:

```js
    /*#__PURE__*/React.createElement(SectionKicker, { size: "large" }, "THE LANDSCAPE"),
    /*#__PURE__*/React.createElement(BodyP, null, "You have seen what an LLM is and how it works. Now meet the ones you will actually use."),
```

(If `SectionKicker` does not accept a `size` prop in this codebase, use a plain `SectionKicker` with the label "THE LANDSCAPE" — check an existing large-kicker usage first by grepping `size: "large"`.)

- [ ] **Step 4: Verify**

`bash design-check.sh` → PASS. Browser: What's an LLM? now shows, in order: LLM decoded → bar chart → guess activity → generative AI prose → Stored-vs-Built SEE IT → THE LANDSCAPE → products → models. The stored-vs-built SEE IT works (reveal traditional, reveal AI, ask again). Next card gating still correct. No em-dash added. Console clean.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "Move generative AI + stored-vs-built SEE IT into What's an LLM?

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Create the You Already Use AI lesson

Second destination. New lesson built from the breadth content currently in `AIHistorySection`. Register it after `aihistory`. Still duplicated until Task 4.

**Files:**
- Modify: `index.html` — `SECTION_GROUPS` (~1208), `SECTION_META` (~1236), `SECTION_COMPONENTS` (~13537); add new `YouAlreadyUseSection`.
- Source (read-only): `AIHistorySection` — the `EVERYDAY_AI_USES` and `MAPS_LENS` arrays, the "YOU ALREADY USE AI" ShowcaseBox, the Google Maps ShowcaseBox + "sometimes it misses" paragraphs, the "Most AI is not ChatGPT" KeyInsight, and the "most products are mixes" paragraph.

- [ ] **Step 1: Register the lesson id**

In `SECTION_GROUPS` "Start Smarter" array, insert `"youalreadyuse"` between `"aihistory"` and `"llms"`:

```js
  sections: ["welcome", "whydeeper", "aihistory", "youalreadyuse", "llms", "doesaithink", "whybother", "control"]
```

- [ ] **Step 2: Add metadata**

In `SECTION_META`, directly below the `aihistory` line, add (pick an emoji escape NOT already used in SECTION_META — verify with grep; 📱 `📱` is expected free):

```js
  youalreadyuse: { kicker: "AI IS EVERYWHERE", label: "You Already Use AI", icon: "📱" },
```

- [ ] **Step 3: Create the component**

Add a new `function YouAlreadyUseSection(props)` (place it immediately AFTER `function AIHistorySection(props) { ... }` closes). Build it from a `LessonHeader { sectionId: "youalreadyuse" }`, then the content copied VERBATIM from `AIHistorySection`:
- Declare the `EVERYDAY_AI_USES` and `MAPS_LENS` const arrays at the top of the function (copy both from AIHistorySection).
- Body order: an opening framing paragraph (new, below) → the "YOU ALREADY USE AI" ShowcaseBox (copy) → the Google Maps ShowcaseBox (copy) → the two "sometimes it misses" / "that's the attitude" paragraphs (copy) → the "Most AI is not ChatGPT" KeyInsight (copy) → the "most products are mixes" paragraph (copy) → `LessonRule` → `NextLessonGate`.

New opening framing paragraph (replaces the old in-lesson lead so it stands alone):

```js
    /*#__PURE__*/React.createElement(BodyP, null, "You do not have to open ChatGPT to use AI. It is already running quietly inside apps you touch every day, usually doing one specific job: predicting what you might tap, watch, say, or need next."),
```

End with:

```js
    /*#__PURE__*/React.createElement(LessonRule, null),
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: true, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("llms"); }, label: "Next: What’s an LLM?" })
  );
}
```

(This lesson has no activity, so `ready: true`.)

- [ ] **Step 4: Register the component**

In `SECTION_COMPONENTS`, below the `aihistory: AIHistorySection,` line, add:

```js
  youalreadyuse: YouAlreadyUseSection,
```

- [ ] **Step 5: Verify**

`bash design-check.sh` → PASS. Browser: the chip nav shows "You Already Use AI" after "What Is AI?". Open it: framing paragraph, everyday-uses showcase, Google Maps example, the misses paragraphs, "Most AI is not ChatGPT", products-are-mixes, then Next → What's an LLM?. Console: no validate() errors (validate confirms the new id has meta + component). No em-dash added.

Note: `aihistory` still navigates to `llms` at this point, so its Next card temporarily skips the new lesson. Task 4 re-points it. The new lesson is reachable via chip nav meanwhile. This is expected.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Add You Already Use AI lesson (breadth content from What is AI?)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Re-scope What is AI? to the conceptual loop

Trim `AIHistorySection` to definition + loop prose + myths, and re-point its nav. The content removed here now lives in You Already Use AI (Task 3) and What's an LLM? (Tasks 1-2), so nothing is lost.

**Files:**
- Modify: `index.html` — `AIHistorySection`.

- [ ] **Step 1: Replace the single "lens" paragraph with the loop prose**

In `AIHistorySection`, find the paragraph that begins "How do they do it? There’s one lens behind most of what AI does" and ends "You’ll see this same lens in every lesson." Replace that ONE `BodyP` with the loop intro + four beats below (adapted from the Primer; no activity lead-ins, no em-dashes):

```js
    /*#__PURE__*/React.createElement(BodyP, null, "How do they do it? Almost everything AI does runs on one simple loop: it learns patterns, weighs what is likely, and predicts the next word. Four words carry it, and you will see this same loop in every lesson."),
    /*#__PURE__*/React.createElement(SectionKicker, null, "PATTERNS"),
    /*#__PURE__*/React.createElement(BodyP, null, "AI works by finding patterns. Read enough writing and the regularities start to show: which words tend to follow which, how a question is usually answered, what a polite reply sounds like. AI does this at a scale no person could, across more text than you could read in a thousand lifetimes. It does not memorize that text. It picks up the patterns running through it."),
    /*#__PURE__*/React.createElement(SectionKicker, null, "TRAINING"),
    /*#__PURE__*/React.createElement(BodyP, null, "Those patterns have to come from somewhere. Training is where AI learns them. It reads enormous amounts of text and slowly adjusts itself until it is good at one task: given some words, guess what comes next. That happens once, up front, before you ever type anything. A later lesson opens up exactly how. For now: training is how the patterns get in."),
    /*#__PURE__*/React.createElement(SectionKicker, null, "PROBABILITY"),
    /*#__PURE__*/React.createElement(BodyP, null, "Once it is trained, here is what AI actually does when you talk to it. It looks at the words so far and scores how likely each possible next word is. Not one guess: a ranked list, with a number on every option. \"See you ___\" might score \"tomorrow\" high, \"later\" a little lower, \"giraffe\" near zero. That scoring step has a name worth knowing, because it is the single move AI repeats for every word in every answer you have ever seen: probability."),
    /*#__PURE__*/React.createElement(SectionKicker, null, "PREDICTION"),
    /*#__PURE__*/React.createElement(BodyP, null, "Picking that next word is the prediction. Then AI does the one thing that turns a single guess into a whole answer: it adds the word it picked, looks at everything again, and predicts the next word. Then again, and again. A paragraph is just this loop run a few hundred times. One likely word after another, fast enough to look like thought."),
```

- [ ] **Step 2: Add the loop KeyInsight after the image**

Find the `what-is-ai.jpg` `img` element. Immediately AFTER it, insert:

```js
    /*#__PURE__*/React.createElement(KeyInsight, { lead: "That is the whole loop:" },
      "AI learns patterns from huge amounts of text, then uses them to weigh what is probable and predict the next word, one word at a time. Keep this loop in mind. The rest of the course is really just a closer look at one part of it or another."),
```

- [ ] **Step 3: Remove the moved content**

Delete these blocks from `AIHistorySection` (all now living in You Already Use AI or What's an LLM?):
- The `EVERYDAY_AI_USES` and `MAPS_LENS` const arrays (top of the function).
- The "YOU ALREADY USE AI" ShowcaseBox.
- The Google Maps ShowcaseBox and the two paragraphs after it ("And sometimes it misses..." and "That’s the attitude we want...").
- The "Most AI is not ChatGPT" KeyInsight and the "Most products are mixes" paragraph.
- The `SectionKicker "GENERATIVE AI"`, its two paragraphs, and the "Stored Answers vs. Built From Probability" InteractiveBox.
- The now-unused state hooks: `revealStep`/`setRevealStep`, `askCount`/`setAskCount`, `seeComplete`/`setSeeComplete` (the three `var _rs`/`_aa`/`_sc` lines at the top of AIHistorySection).

After this, `AIHistorySection` should contain only: the two opening definition paragraphs, the loop intro + four beats, the image, the loop KeyInsight, the three-myths paragraph ("That clears up three big myths..."), and the nav gate.

- [ ] **Step 4: Re-point the nav (and fix the gate, since the SEE IT is gone)**

Replace `AIHistorySection`'s `NextLessonGate` (which currently has `ready: revealStep >= 2 && askCount >= 1` and navigates to `"llms"`) with:

```js
    /*#__PURE__*/React.createElement(NextLessonGate, { ready: true, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("youalreadyuse"); }, label: "Next: You Already Use AI" })
  );
```

Also remove any `LessonRule` duplication if the gate was preceded by one that no longer fits; keep a single `LessonRule` before the gate if that matches the lesson's prior pattern.

- [ ] **Step 5: Verify**

`bash design-check.sh` → PASS. Browser: What is AI? now reads as a light conceptual lesson (definition → loop beats → image → KeyInsight → myths) with NO activities, and its Next card goes to You Already Use AI. Confirm no leftover references to `revealStep`/`askCount`/`seeComplete` remain in AIHistorySection (`grep -n` and check they appear only in LLMsSection now). No em-dash added. Console clean.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "Re-scope What is AI? to the conceptual loop (prose only)

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Remove the Primer lesson, add the opener recap, fix references

The Primer's content now lives in What is AI? (loop) and What's an LLM? (pieces). Delete it and reconcile every reference.

**Files:**
- Modify: `index.html` — `SECTION_GROUPS`, `SECTION_META`, `SECTION_COMPONENTS`, `OpenerFoundationsSection`, the Test Yourself QUIZ entry; delete `PrimerSection`.

- [ ] **Step 1: Remove primer from the three registries**

- In `SECTION_GROUPS` "Understand AI", delete `"primer", ` (the array tail becomes `..."openerfoundations", "howwegothere", ...`).
- In `SECTION_META`, delete the `primer: { kicker: "THE WHOLE PICTURE", label: "AI Primer", icon: "🔮" }` line.
- In `SECTION_COMPONENTS`, delete the `primer: PrimerSection,` line.

- [ ] **Step 2: Delete the PrimerSection function**

Delete the entire `function PrimerSection(props) { ... }` (grep `function PrimerSection`; it ends just before `function BiasQuiz(props) {`). Do not bleed into `BiasQuiz`.

- [ ] **Step 3: Re-point the Foundations opener and add the loop recap**

In `OpenerFoundationsSection`, change the nav back to How We Got Here (the Primer is gone):

```js
    nextLessonId: "howwegothere",
    nextLessonLabel: "Next: How We Got Here",
```

And add a recap line so the section's forward-references still land. Append this string as a new paragraph in the opener's `whyThisMatters` array (the array of strings), as its final element:

```js
      "You already met the core loop back in What is AI?: AI learns patterns, weighs probability, and predicts the next word. This section opens up each part of that loop, one piece at a time."
```

- [ ] **Step 4: Re-point the Test Yourself quiz**

Grep `review: "primer"`. In that QUIZ entry (the question "Same prompt, three runs, three different answers..."), change:
- `review: "primer",` → `review: "llms",`
- `section: "AI Primer",` → `section: "What’s an LLM?",`

(The concept now lives in What's an LLM?. `review` is the wrong-answer nav target; `section` is the display label.)

- [ ] **Step 5: Stale-reference sweep**

Run `grep -n 'primer\|PrimerSection' index.html`. Expect ZERO matches except inside the retired/dead `OpenerAnswersSection` if any pre-existing one is there (it is not primer-related; it referenced `probability`). There must be NO remaining `primer` lesson-id reference in live code: registries, nav targets, `lessonId`, `review`. If any appear, reconcile (nav/review → the appropriate live lesson).

- [ ] **Step 6: Verify**

`bash design-check.sh` → PASS. Browser: Understand AI no longer lists AI Primer (now 15 lessons); the Foundations opener Next card goes to How We Got Here and the opener shows the recap line. The Test Yourself quiz question's wrong-answer review navigates to What's an LLM? (not a redirect-to-welcome). Console: no validate() errors, no "navigates to unknown section id: 'primer'". No em-dash added.

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "Remove standalone AI Primer; add loop recap to Understand AI opener

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: Sync briefing.md, park cut copy, final checks

**Files:**
- Modify: `briefing.md`; `docs/parking-lot.md`.

- [ ] **Step 1: Update the lesson map in briefing.md**

Grep `Start Smarter` and `Understand AI` in `briefing.md`. Update:
- **Start Smarter:** bump count 8 (it already says 8 if `intro`/roadmap counted; verify the actual list) and insert `You Already Use AI (youalreadyuse)` after `What Is AI? (aihistory)`.
- **Understand AI:** change the count from 16 to 15 and remove `AI Primer (primer)` from the Foundations cluster.
- Update the prose notes: What is AI? is now the conceptual-loop lesson; the everyday-AI breadth moved to the new You Already Use AI lesson; the next-word-prediction pieces and generative AI now live in What's an LLM?; the standalone AI Primer (added 2026-06-04) was dissolved the same day and its loop relocated to What is AI?.
- Reconcile every other `primer` / `probability` mention so none implies a live Primer lesson.

- [ ] **Step 2: Update the order-array references in briefing.md**

If briefing quotes the Start Smarter or Understand AI `sections` arrays, update them: Start Smarter gains `youalreadyuse` after `aihistory`; Understand AI drops `primer`.

- [ ] **Step 3: Park cut copy**

Append a dated section to `docs/parking-lot.md` noting the 2026-06-04 Start Smarter restructure: the AI Primer page was dissolved (loop → What is AI?, pieces → What's an LLM?), and What is AI? was split (breadth → You Already Use AI). If any unique Primer copy (e.g. the "This section is long, here is the whole machine" framing intro, or the closing KeyInsight wording) was not carried into any lesson, paste it there verbatim for possible reuse. Match the file's existing heading/format.

- [ ] **Step 4: Final consistency checks**

- `bash design-check.sh` → `PASS - no new drift against baselines.`
- `grep -nc '—' index.html` should still report the baseline em-dash count (4); if higher, find and remove the added em-dash.
- Confirm Start Smarter nav chain end to end: What is AI? → You Already Use AI → What's an LLM? → Does AI Think?.
- Confirm Understand AI opens: Opener (with recap) → How We Got Here.
- Final browser read-through of all four touched lessons (What is AI?, You Already Use AI, What's an LLM?, Understand AI opener).

- [ ] **Step 5: Commit**

```bash
git add briefing.md docs/parking-lot.md
git commit -m "Sync briefing.md and parking-lot for Start Smarter restructure

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Self-review notes (already reconciled)

- **Spec coverage:** prediction pieces → LLMs (T1), generative + stored-vs-built → LLMs (T2), new You Already Use AI lesson (T3), What is AI? re-scoped to the loop (T4), Primer removal + opener recap + quiz/stale-ref (T5), briefing/parking-lot/design-check (T6). The three confirmed allocation defaults (Google Maps, "Most AI is not ChatGPT", "sometimes it misses") land in You Already Use AI via T3.
- **Ordering safety:** destinations (T1, T2 = LLMs; T3 = new lesson) are filled before sources are trimmed (T4 = What is AI?; T5 = Primer). No intermediate state loses content; temporary duplication is resolved by T4/T5.
- **localStorage keys:** the stored-vs-built SEE IT uses fresh `seeit-llms-twoSystems*` keys in LLMs (T2) so it never collides with the original `seeit-aihistory-*` keys before they are removed (T4).
- **Naming consistency:** new id `youalreadyuse` ↔ `YouAlreadyUseSection` used identically across SECTION_GROUPS, SECTION_META, SECTION_COMPONENTS, and nav targets. Removed id `primer`/`PrimerSection` purged from all registries, the function, inbound nav (opener), and the quiz review.
- **No invented test framework:** verification is design-check.sh + validate() + browser.
- **Watch-items flagged for live review:** You Already Use AI has no activity; What's an LLM? becomes a long two-movement lesson.
