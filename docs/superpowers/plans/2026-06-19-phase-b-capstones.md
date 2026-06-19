# Phase B — New Capstone TRY ITs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline) to implement task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Author a single capstone TRY IT for each of the six teaching lessons that currently have no activity, so every teaching lesson ends with one hands-on "do it" moment.

**Architecture:** Single-file React-without-JSX app (`index.html`). Each capstone is **net-new content** authored from the lesson's teaching point, built on a proven Phase-A shell (Pattern 2 match = `ScenarioRow` + `FeedbackPill`; Pattern 2 judge = `QuizBlock`-per-scenario; Pattern 1 = `RevealSequence` + `QuizBlock`). No SEE IT/variant work — this only *adds* activities. The work is ~90% content design, ~10% wiring.

**Tech Stack:** React 18 UMD, `React.createElement`, existing components (`InteractiveBox` variant `try`/`mint`, `ScenarioRow`, `FeedbackPill`, `QuizBlock`, `ActivityCounter`, `ActivityInstruction`, `InnerCard`, `KeyInsight`).

---

## Shared wiring pattern (every task)

Each capstone is a **new component** placed at the bottom of its lesson, just above `LessonRule`/`NextLessonGate`. To make the gate point at the capstone (the capstone model), wire completion back to the section:

```js
// in the new component: call props.onComplete() once every item is answered
useEffect(function() { if (answeredCount >= TOTAL && props.onComplete) props.onComplete(); }, [answeredCount]);

// in the lesson section: track done + gate on it
var _d = useState(false), done = _d[0], setDone = _d[1];
// ...render the capstone:  React.createElement(TheCapstone, { onComplete: function(){ setDone(true); } })
// ...gate:  ready: done   (replacing the lesson's current ready:true)
```

If a section is small, building the activity inline (answers state in the section, `ready: answeredCount >= TOTAL`) is equally fine. Pattern-2 activities carry **no Takeaway** (synthesis stays in the lesson's existing KeyInsight); Pattern-1 keeps a Takeaway as `completionElement`.

## Per-task verification protocol (every task)

1. `node --check` on the inline script (lines 143..`</script>`).
2. `bash design-check.sh` → `PASS` (em-dash baseline 7; avoid em-dashes in new copy).
3. Browser: `validate()` → `{errors:[],warnings:[],sectionCount:62}`; the lesson renders; the capstone answers latch with feedback; the counter tracks; gate becomes ready after completing it; no console errors.
4. Commit + push.

---

## Task 1: `llms` — "Recommendation or Generative?" (P2 binary sort) — LOCKED

**Files:** Modify `index.html` (`LLMsSection`).

**Component:** `RecOrGenTryIt`. Shell: `ScenarioRow` + two `FeedbackPill`s per row (copy `AIStrengthsSection` "Make the Call"). Title **"Recommendation or Generative?"**, instruction "For each one, decide: is it picking from what already exists, or making something new?" Two options per row: **Recommendation** / **Generative**. Counter `0/5`. No Takeaway (the existing "The tool, named" KeyInsight is the synthesis).

| Row | Correct | Feedback |
|---|---|---|
| Netflix suggesting your next show | Recommendation | Ranks shows that already exist and serves the top match. Makes nothing new. |
| ChatGPT writing you a birthday poem | Generative | The poem didn't exist until you asked. Built fresh, word by word. |
| Spotify's Discover Weekly | Recommendation | Chooses from songs that already exist and orders them for you. |
| An app that drafts your Instagram caption | Generative | Writes new text from patterns. There was no caption to pick from. |
| TikTok's For You feed | Recommendation | Ranks videos that already exist to predict what you'll watch. It never makes a video. |

- [ ] Build `RecOrGenTryIt`; render it at the bottom of `LLMsSection` above the gate; wire gate per shared pattern (LLMsSection gate currently `ready: true`).
- [ ] Run verification protocol. Commit: `feat: add llms Recommendation-or-Generative capstone TRY IT`.

## Task 2: `training` — "Match the step to the phase" (P2-match) — LOCKED

**Files:** Modify `index.html` (`TrainingSection`).

**Component:** `TrainingPhaseMatch`. Shell: `ScenarioRow` + three `FeedbackPill`s per row. Title **"Match the step to the phase"**, instruction "Match each training step to the phase it belongs to." Three options each, **numbered to match the lesson**: **Phase 1: Pretraining** / **Phase 2: Instruction tuning** / **Phase 3: Preference tuning**. Feedback opens with the phase number. Counter `0/5`. No Takeaway (existing "Weeks, money, and massive compute" KeyInsight is synthesis).

| Statement | Correct | Feedback |
|---|---|---|
| "It reads billions of pages and learns to predict the next word." | Phase 1 | Phase 1 — the raw stage: pattern-learning from mountains of text, no human grading each answer. |
| "Trainers show it example questions paired with ideal answers." | Phase 2 | Phase 2 — example Q&A teaches it to *answer* you, not just continue text. |
| "Humans rate which of two answers is better; it shifts toward the winners." | Phase 3 | Phase 3 — RLHF: human rankings shape its helpfulness and tone. |
| "It practices on books, websites, and code with no one scoring its replies." | Phase 1 | Phase 1 — still unsupervised: it's just absorbing patterns. |
| "Reviewers mark answers as more or less helpful, tuning its style." | Phase 3 | Phase 3 — the same RLHF signal: people's preferences nudge the model. |

- [ ] Build `TrainingPhaseMatch`; render at the bottom of `TrainingSection` above the gate; wire gate (TrainingSection gate currently `ready: true`).
- [ ] Verification protocol. Commit.

## Task 3: `aiismath` — "Pick the next word" (P2-match) — PROPOSED

**Files:** Modify `index.html` (`AIIsMathSection`).

**Design (proposed):** the lesson's core is *AI picks the next word by probability, shifted by context*. Capstone: given a sentence in progress, pick the word the model would most likely choose. Three rows, three word-options each; pick the highest-probability next word. Reuses the lesson's own "peanut butter and ___" framing. Counter `0/3`; no Takeaway (lesson's probability KeyInsight is synthesis).

| Sentence so far | Options | Correct | Feedback |
|---|---|---|---|
| "The forecast warned of a huge storm. Tomorrow it's going to ___" | rain / shine / cook | rain | "Storm" piles the odds onto "rain." The model just picks the highest-probability next word. |
| "Peanut butter and ___" | jelly / gravel / Tuesday | jelly | You predicted it the way the model does: "jelly" is by far the most probable. |
| "She was so tired she fell ___" | asleep / upward / blue | asleep | Common patterns make "asleep" the runaway favorite. Context sets the odds. |

*(Alt: a P1-sequential "build a forecast" mirroring the weather example — estimate, update on a clue, then pick the word. Heavier; the next-word match is simpler and hits the same point.)*

- [ ] Build `NextWordTryIt` (P2-match shell); render at bottom of `AIIsMathSection`; wire gate.
- [ ] Verification protocol. Commit.

## Task 4: `attention` — "What does it point to?" (P2-match) — PROPOSED

**Files:** Modify `index.html` (`HowAIReadsSection`).

**Design (proposed):** the lesson teaches attention links a word to the right earlier word across distance. Capstone: resolve the pronoun in tricky sentences (Winograd-style). Three rows; each gives a sentence and asks which word "it" refers to. Counter `0/3`; no Takeaway.

| Sentence | Options | Correct | Feedback |
|---|---|---|---|
| "The trophy didn't fit in the suitcase because **it** was too big." | trophy / suitcase | trophy | "Big" pulls attention to the trophy, the thing that wouldn't fit. |
| "The trophy didn't fit in the suitcase because **it** was too small." | trophy / suitcase | suitcase | Flip one word and attention swings to the suitcase. Same sentence, different target. |
| "The cat chased the mouse until **it** got tired." | cat / mouse | cat | Context ("chased… tired") links "it" to the cat doing the chasing. |

- [ ] Build `PronounAttentionTryIt` (P2-match shell, 2–3 options per row); render at bottom of `HowAIReadsSection`; wire gate.
- [ ] Verification protocol. Commit.

## Task 5: `computecost` — "Does this cost claim hold up?" (P2-judge) — PROPOSED

**Files:** Modify `index.html` (`TheHiddenCostSection`).

**Design (proposed):** tests the cost drivers (tokens × parameters, every answer re-runs the network). Three claims; True / False each with reasoning. `QuizBlock`-per-scenario or two `FeedbackPill`s. Counter `0/3`; no Takeaway (the "behind the magic" KeyInsight is synthesis).

| Claim | Answer | Feedback |
|---|---|---|
| "A longer answer takes more compute than a short one." | True | More tokens means the whole network runs more times. Length drives cost. |
| "A bigger model costs more compute per word than a smaller one." | True | More parameters means more calculations for every single token. |
| "Once a model is trained, answering is basically free." | False | Every answer re-runs billions of parameters: real electricity and water, every time. |

- [ ] Build `CostClaimsTryIt`; render at bottom of `TheHiddenCostSection`; wire gate.
- [ ] Verification protocol. Commit.

## Task 6: `talkingai` — "Spot the worry" (P2-judge) — PROPOSED

**Files:** Modify `index.html` (`TalkingAboutAISection`).

**Design (proposed):** the lesson's move is *meet the worry underneath, not the soundbite*. Capstone: for each soundbite, pick the response that engages the real concern (not a dismissal or a cheap debunk). `QuizBlock`-per-scenario, 3 options each. Counter `0/3`; no Takeaway (the lesson's closing "they're the ones who can judge" line is synthesis).

1. **"AI is going to take all the jobs."** → correct: *"Some tasks change fast. Which ones, and who adapts?"* · distractors: "Relax, every new tech makes jobs" (dismiss), "AI is overhyped anyway" (deflect).
2. **"AI is going to take over the world."** → correct: *"It only acts where someone gives it access. What would it need permission to do?"* · distractors: "That's just movies" (dismiss).
3. **"Using AI for homework is just cheating."** → correct: *"Depends how: using it to understand vs. to dodge the work."* · distractors: "Everyone does it" (dismiss).

- [ ] Build `SpotTheWorryTryIt`; render at bottom of `TalkingAboutAISection`; wire gate.
- [ ] Verification protocol. Commit.

---

## Notes
- **`whatyoulearned` deliberately gets no capstone** — it's the recap/celebration lesson; an activity there is busywork. Out of scope.
- Tasks 3–6 designs are **proposed** — review/edit the content before building (Tasks 1–2 are locked from your sign-off).
- This plan only *adds* activities; no SEE IT/variant changes. The SEE IT initiative is already complete.
