# SEE IT → TRY IT (Phase A) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Rework the remaining `variant:"see"` boxes into TRY IT capstones (or static), clearing the last SEE ITs so the `see` variant can be decommissioned.

**Architecture:** Single-file React-without-JSX app (`index.html`). No unit-test framework — verification is `validate()` (in-browser), `bash design-check.sh`, `node --check` on the inline script, and a browser spot-check. Each lesson keeps **one** capstone TRY IT at the bottom; static aids may be many. TRY IT patterns are standardized (memory `project_tryit_patterns`): **Pattern 1** = sequential `RevealSequence` + `QuizBlock` per step + `Takeaway` as `completionElement`; **Pattern 2** = parallel `ScenarioRow` + `FeedbackPill` + answered-count, **no Takeaway** (synthesis in an adjacent `KeyInsight`). QuizBlock-per-scenario is a sanctioned Pattern-2 interior for A/B judgments with longer text.

**Tech Stack:** React 18 UMD, `React.createElement`, existing components (`InteractiveBox` variant `try`/`mint`, `QuizBlock`, `ScenarioRow`, `FeedbackPill`, `RevealSequence`, `Takeaway`, `KeyInsight`, `ActivityCounter`).

---

## Decision needed before execution

- **`thoughtpartner`:** it already has a working capstone, **"Keep the Thinking Yours"** (3-scenario move-picker). Recommendation: **demote "Thinking Together" to a static illustration** (Task 7) and keep the existing TRY IT — do *not* author a new one. Confirm, or say to supersede.

## Per-task verification protocol (every task)

Each task's "tests" are these steps (replace the pytest-style TDD; there is no test suite):
1. `node --check` on the inline script (extract lines 143..</script>).
2. `bash design-check.sh` → must print `PASS` (em-dashes baseline 7).
3. Browser: `validate()` returns `{errors:[],warnings:[],sectionCount:62}`; the lesson renders; **no `SEE IT` chrome / reveal buttons**; the **NextLessonGate now keys off the new TRY IT's answered state**; no console errors.
4. `grep -c 'variant: "see"'` decreased as expected.
5. Commit.

---

## Task 1: `howwegothere` "Build the machine" → TRY IT (Pattern 2 match) — LOCKED

**Files:** Modify `index.html` (`HowWeGotHereSection` + its `IDEAS`/`SPARK` data + box + gate).

**Activity design (locked):** Pattern 2 match — "What each idea gave the machine." Four rows (idea · year · who); for each, pick the contribution from shared `FeedbackPill` options:
- Probability (1650s, Pascal & Fermat) → **"Answers as odds, not certainties"**
- Prediction (1948, Shannon) → **"Guess the next word from the words before it"**
- Training (1957, the perceptron) → **"Learn patterns from examples, not hand-written rules"**
- Transformer (2017, *Attention Is All You Need*) → **"Weigh all the words at once to find the patterns between them"**

Per-row feedback on a wrong pick (e.g. *"That's Training — Probability is about expressing answers as odds."*). Counter `0/4`. No Takeaway; carry the existing line into a `KeyInsight`: **"Centuries apart, then all at once."**

- [ ] **Step 1:** Copy the Pattern 2 shell from the canonical ref `ThinkingModeSection` "Match the Task to the Effort" (`InteractiveBox` try/mint + `ScenarioRow` rows + `FeedbackPill` + answered-count). Reuse the existing `IDEAS`/`SPARK` data (label/year/who/caption) for row labels.
- [ ] **Step 2:** Replace the `variant:"see"` "Build the machine" box (and its assemble-on-click state: `lit`/`ignited`) with the match TRY IT. Move the existing "Centuries apart, then all at once" Takeaway content into a `KeyInsight` below.
- [ ] **Step 3:** Change the lesson gate from `ready: true` (current) to `ready: <all 4 rows answered>`.
- [ ] **Step 4:** Run the verification protocol. Expect `variant:"see"` 7 → 6.
- [ ] **Step 5:** Commit: `feat: rework howwegothere Build-the-machine SEE IT into a match TRY IT`.

## Task 2: `evaluating` "The Good Enough Checklist" → TRY IT (Pattern 2, QuizBlock-per-scenario) — LOCKED

**Files:** Modify `index.html` (`EvaluatingSection` + box + gate).

**Activity design (locked): "Good enough?"** Three fresh scenarios, each a task + an AI response; `QuizBlock` asks what (if anything) blocks using it as-is. Options drawn from the lesson's checklist criteria (true / complete / right tone / right format / **good to go**):
1. **Confident but false** — a factual answer with a fabricated specific (date/stat) → answer: *Not actually true.*
2. **Correct but wrong tone** — accurate yet stiff/formal text for a casual use (e.g. an Instagram caption) → answer: *Wrong tone for the audience.*
3. **Actually fine** — a solid response → answer: *Good to go.* (Not-all-fail, on purpose.)

Per-scenario feedback. Counter `0/3`. No Takeaway — the lesson's existing `KeyInsight "True isn't enough."` stays as synthesis. Author the 3 scenarios fresh in course voice (teen-relevant); align option labels to the lesson's actual checklist criteria when building.

- [ ] **Step 1:** Copy the QuizBlock-per-scenario Pattern-2 interior from `SpotTheSycophancy`-style refs (parallel shell + `QuizBlock` per scenario + answered-count).
- [ ] **Step 2:** Replace the `variant:"see"` "Good Enough Checklist" box with the 3-scenario judge TRY IT. (The static "Refine" box stays above as the loop illustration.)
- [ ] **Step 3:** Change the gate from `ready: true` to `ready: <all 3 scenarios answered>`.
- [ ] **Step 4:** Verification protocol. Expect `variant:"see"` 6 → 5.
- [ ] **Step 5:** Commit: `feat: rework evaluating Good-Enough-Checklist SEE IT into a judge TRY IT`.

## Task 3: `verify` "Verification Strategies" → TRY IT (Pattern 2 match) — PROPOSED

**Files:** Modify `index.html` (`VerifySection`; gate currently `ready: activeStrategy >= VERIFY_STRATEGIES.length`).

**Activity design (proposed): "Which check catches it?"** Keep the 6 strategies as a static list (or brief inline aid), then a Pattern-2 match: 3–4 short AI claims, each with a planted flaw; student picks the strategy that would catch it:
- A suspiciously precise stat → **Watch for hallucination triggers**
- A real journal citing a study that doesn't exist → **Spot the "almost true" trap** / **Verify citations**
- A confident claim about a recent event → **Cross-reference the claim**
Per-item feedback; counter. No Takeaway (KeyInsight in flow).

- [ ] **Step 1:** Copy Pattern 2 shell. Keep `VERIFY_STRATEGIES` data for the static reference list above the activity.
- [ ] **Step 2:** Replace the `variant:"see"` RevealSequence box with: static strategy list (stripped of stepping) + the match TRY IT.
- [ ] **Step 3:** Change gate to key off the match's answered state (was `activeStrategy >= …`).
- [ ] **Step 4:** Verification protocol. `see` 5 → 4.
- [ ] **Step 5:** Commit.

## Task 4: `aifuture` "Why Smart Predictions Fail" → TRY IT (Pattern 2 match) — PROPOSED

**Files:** Modify `index.html` (`AIFutureSection`; gate `ready: predIdx >= ALL_CARDS.length`).

**Activity design (proposed): "Match the miss."** The lesson's point is *the miss is always the friction*. Show the 4 predictions (PCs / self-driving / ATMs / accountants) and have the student match each to **what actually slowed or flipped it**:
- PCs → cost + size + no use case yet
- Self-driving → regulation + liability + public trust
- ATMs → branch economics changed; relationship work couldn't be automated → *more* tellers
- Accountants → cheaper tools increased demand → *more* accounting jobs
Per-item feedback; counter. No Takeaway (KeyInsight carries "the miss is the friction"). *(Alt: a single fresh "predict the friction" on a contemporary claim — note for David.)*

- [ ] **Step 1:** Copy Pattern 2 shell; reuse `ALL_CARDS` data.
- [ ] **Step 2:** Replace the reveal box with the match TRY IT (keep the "How to judge the next claim" showcase below as-is).
- [ ] **Step 3:** Gate keys off answered state (was `predIdx >= …`).
- [ ] **Step 4:** Verification protocol. `see` 4 → 3.
- [ ] **Step 5:** Commit.

## Task 5: `prompt` "Same question, different prediction" → TRY IT (Pattern 2) — PROPOSED

**Files:** Modify `index.html` (`PromptSection`; gate `ready: seeStep >= 6`).

**Activity design (proposed): "Predict the split."** Keep a trimmed static version of the Luke/Nate setup (same question, two different context windows) as the illustration, then a Pattern-2 task: given each person's prior context, the student predicts **which recommendation each gets** (or which context produced a given answer). Reinforces *same model + different context → different tokens*.
- Luke ("all-terrain, camping, road trips") → Jeep Cherokee
- Nate ("loves pickup trucks") → Ford Raptor
- (Add a 3rd fresh persona for a non-trivial 3rd row.)
Per-item feedback; counter. No Takeaway (the existing "Same model. Different context." line → `KeyInsight`).

- [ ] **Step 1:** Copy Pattern 2 shell. Keep a static context-window comparison as the lead illustration; drop the typing/step machinery.
- [ ] **Step 2:** Replace the `variant:"see"` box accordingly; gate keys off the match's answered state (was `seeStep >= 6`).
- [ ] **Step 3:** Verification protocol. `see` 3 → 2.
- [ ] **Step 4:** Commit.

## Task 6: `layers` "Watch Meaning Build Layer by Layer" → TRY IT (Pattern 1 sequential) — PROPOSED

**Files:** Modify `index.html` (`LayersSection`; gate `ready: reachedFinal`).

**Activity design (proposed): "Trace the word."** Keep the "bank" layer walkthrough as a static illustration (early→noun, middle→physical place, deeper→outdoor scene, final→full context), then a Pattern-1 sequential TRY IT on a **new ambiguous word**: e.g. "bat" in "The bat swooped over the field at dusk." For each of ~3 steps, a `QuizBlock`: "By which layer can the model rule out the baseball meaning?" / "What did this layer add?" `Takeaway` as `completionElement`: a real conceptual point (e.g. *"No single layer knows the word — each one nudges it closer."*).

- [ ] **Step 1:** Copy Pattern 1 shell from canonical `BiasQuiz` "What Did the Model Actually Learn?" (RevealSequence + QuizBlock per step + Takeaway completionElement).
- [ ] **Step 2:** Convert the "bank" box to a static illustration; add the sequential TRY IT below. Author the new-word steps in course voice.
- [ ] **Step 3:** Gate keys off the TRY IT reaching its Takeaway (was `reachedFinal`).
- [ ] **Step 4:** Verification protocol. `see` 2 → 1.
- [ ] **Step 5:** Commit.

## Task 7: `thoughtpartner` "Thinking Together" → static (pending decision)

**Files:** Modify `index.html` (`ThoughtPartnerSection`).

**Design (recommended):** convert the scripted "Thinking Together" conversation to a **static** illustration (show the 6 beats as a static chat transcript; drop the click-through/typing). **Keep** the existing "Keep the Thinking Yours" TRY IT as the capstone — do not author a new one. Gate already keys off that TRY IT (`tpAnswers >= TP_MOVES.length`); just drop the `allDone` (animation-finished) clause so it no longer waits on the now-static playback.

- [ ] **Step 1:** Pin the conversation playback to its done state / render all beats statically; drop the typing effect + Continue button.
- [ ] **Step 2:** Swap the `variant:"see"` wrapper for `ShowcaseBox`.
- [ ] **Step 3:** Update gate `ready:` to drop the `allDone` clause (keep `tpAnswers >= TP_MOVES.length`).
- [ ] **Step 4:** Verification protocol. `see` 1 → 0.
- [ ] **Step 5:** Commit.

## Task 8: Decommission the `see` variant

**Files:** Modify `index.html` (`InteractiveBox`, CSS band ~line 35, token comment ~line 154, `seeBand`/`seeAccent` tokens).

Only after Tasks 1–7 leave **zero** `variant:"see"`.

- [ ] **Step 1:** Confirm `grep -c 'variant: "see"' index.html` → `0`.
- [ ] **Step 2:** Remove the `see` branch from `InteractiveBox` (the `iconAndLabel`/surface logic) and the SEE IT CSS band.
- [ ] **Step 3:** Decide `--seeAccent`/`--seeRule`/`--seeBand`: several converted static boxes still reference `--seeAccent`/`--seeRule`. EITHER keep them as plain palette tokens (rename optional) OR migrate those references. Grep first: `grep -c 'var(--seeAccent)\|var(--seeRule)' index.html`. Do NOT remove tokens still referenced.
- [ ] **Step 4:** Verification protocol + `validate()` clean.
- [ ] **Step 5:** Commit: `chore: decommission the SEE IT variant`.

---

## Notes / open questions
- Tasks 3–6 designs are **proposed** — review the activity content before execution; alt options noted inline (`aifuture` single-prediction alt; `prompt`/`layers` keep-static-illustration choices).
- Each rework's gate moves from the old reveal-state to the new TRY IT's answered state — this is the intended "capstone is what the gate points at" behavior.
- Phase B (brand-new capstones for `llms`, `aiismath`, `attention`, `training`, `computecost`, `talkingai`, and a `whatyoulearned` decision) is a separate plan.
