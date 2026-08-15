# Finish Smarter Phase 4 — The Final + Certificate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn What You Learned into The Final: recap as study sheet, a timed 20-question quiz drawn from a 50-question bank, a review screen, and an 80%-threshold printable certificate. Course stays 55 lessons; id `whatyoulearned` is retained (ids are stable across retitles).

**Architecture:** All inside `index.html`. New pieces: a `FINAL_BANK` data const (50 questions), pure draw/score helpers, a `TheFinalQuiz` stateful component (idle → running → review states, countdown timer), and a certificate view using the app's existing print machinery. Recap content of the current `WhatYouLearnedSection` survives as the lesson's opening. Spec: `docs/superpowers/specs/2026-08-15-finish-smarter-merge-design.md` ("The Final — mechanics" + "The certificate" sections are the contract; defaults there are the numbers here).

**Tech Stack:** React.createElement inline; existing `useLocalStorage` (verify helper name by grep before use); existing print-view machinery (`?print=lesson:<id>` — study it before Task 3); Date.now for the countdown (fine in app code).

## Global Constraints

- **Mechanics (from the spec, fixed):** 20 questions per attempt drawn from a 50-question bank covering all six sections, order shuffled per attempt; 10-minute countdown, visible, starts on the student's click, never on page load; expiry submits what's answered; NO per-question feedback during the run; post-submit review screen explains each miss and points to its lesson; 80% unlocks the certificate; unlimited retakes, fresh draw each time, best score kept; localStorage state; NO anti-cheat.
- **Certificate (from the spec, fixed):** name pre-filled from the welcome gate's stored name (grep how the gate stores it), editable before generating; course title "Be Smarter Than the Tool", student name, completion date, best score, instructor line; serious house design, no clip-art ribbon energy; print-to-PDF via the browser print path.
- **Data contracts (fixed for all tasks):**
  - `FINAL_BANK`: array of `{ id: "fb##", section: "<group label>", lessonId: "<routed id>", q: "<question>", options: [4 strings], correct: <index 0-3>, explain: "<1-2 sentences, why + what the lesson taught>" }`. Exactly 50 entries; every `lessonId` must resolve in `SECTION_META`; section distribution ≈ proportional (Start Smarter 7, Work With AI 8, Understand AI 10, Avoid Traps 9, Embrace the Future 9, Finish Smarter 7).
  - `drawFinalQuestions(bank)`: returns 20 questions — at least 2 from every section, remainder random, order shuffled, option order NOT shuffled (options are authored with deliberate distractor order).
  - localStorage key `final-exam` via the house storage helper: `{ bestScore: <0-100 int|null>, attempts: <int>, certName: <string|null> }`.
- **Question copy rules:** David's voice; NO em-dashes; every question answerable from the course's own claims (no outside trivia, no invented numbers — reuse the lessons' own numbers only); distractors plausible, never joke options; `explain` must teach, not just assert; no two questions testing the identical fact.
- **Voice:** every content-writing agent loads the `my-writing-style` skill first.
- **Verification cycle (every task):** node --check (house recipe with `awk -v`), serve 8754 + Chrome MCP validate() = 55, chain trace (last id `whatyoulearned` → `"welcome"`), `bash design-check.sh` PASS, screenshots of touched surfaces, kill server. Task-specific checks listed per task.
- **Commit style:** imperative subject, body, `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` trailer. Never commit owner's unrelated uncommitted work or memory files.
- **Editing gotcha:** `\uXXXX`-plus-unicode lines defeat the Edit tool; use sed/python there.

---

### Task 1: The question bank

**Files:** Modify `index.html` (add `FINAL_BANK` const + `drawFinalQuestions` + `scoreFinal(answers, questions)` near the other top-level data consts; NOT yet rendered anywhere).

**Interfaces:** Produces the exact data contracts above. Consumed by Task 2.

- [ ] Load `my-writing-style`. Read the course broadly enough to ground every question: each question cites a real lesson claim (the implementer reads each target lesson's actual copy before writing its questions). Harvest-check git history's deleted finals (Vocab Quiz/Test Yourself/Beat the Clock, deleted 2026-06-26) and the live "Name the Piece" quiz for reusable question material, adapting to the current course (many claims changed since June — the CURRENT lesson text is the authority; do not import stale facts).
- [ ] Write the 50 questions + helpers. `drawFinalQuestions` guarantees ≥2 per section (seeded from a per-attempt `Math.random` shuffle; no fixed seed).
- [ ] Verify: node --check; in the served page's console, run `drawFinalQuestions(FINAL_BANK)` 5 times via evaluate_script and assert: 20 questions, ≥2 per section, no duplicate ids, different orderings across runs; assert all 50 `lessonId`s resolve in `SECTION_META`, all `correct` indices in range, exactly 4 options each. Full verification cycle (nothing renders yet, so validate() and the chain must be unchanged).
- [ ] Commit.

---

### Task 2: The Final lesson — recap, run, review

**Files:** Modify `index.html`: rework `WhatYouLearnedSection` + add `TheFinalQuiz` component.

**Interfaces:** Consumes Task 1's bank + helpers. Produces: the lesson (id `whatyoulearned`) = existing recap content (kept, light seam edits only) → break beat ("That's the course. Ready to prove it?" framing per spec) → `TheFinalQuiz` → LessonRule → the existing Back to Start gate (unchanged). `TheFinalQuiz` exposes its passing state to Task 3 via the `final-exam` storage record (Task 3 reads `bestScore`).

- [ ] Load `my-writing-style` for the framing copy. Build states: **idle** (start card: what the quiz is — 20 questions, 10 minutes, 80% earns the certificate, retakes allowed; a single start button; timer NOT running), **running** (visible mm:ss countdown, question list with pill/option selection, no feedback, progress "answered X of 20", submit button always available; timer expiry auto-submits), **review** (score headline + pass/fail state; every question shown with the student's answer, the correct answer, `explain`, and "From: <lesson label>"; a retake button that redraws; best score persisted; if `bestScore >= 80`, a "Your certificate is ready" affordance placeholder — Task 3 replaces the placeholder with the real certificate flow).
- [ ] Reuse existing option-pill styling conventions (read a live quiz for the look; but NO FeedbackPill correctness coloring during the run — neutral selected-state only).
- [ ] Timer: setInterval + Date.now anchored (not tick-decrement drift); clear on unmount/submit; expiry submits.
- [ ] Verify (cycle +): serve; evaluate_script to jump to the lesson; screenshot idle; start the quiz via click; answer 3 questions; screenshot running (timer visible, no feedback); submit via evaluate_script; screenshot review (misses explained + lesson pointers); confirm `final-exam` record updates and a retake redraws different questions; reload mid-“running” and confirm no timer runs on load (state returns to idle without penalty; in-flight attempts don't persist — that's the accepted behavior, note it).
- [ ] Commit.

---

### Task 3: Certificate

**Files:** Modify `index.html`: certificate flow inside/alongside `TheFinalQuiz`'s passed state + print styling.

**Interfaces:** Consumes `final-exam.bestScore` + welcome-gate name. Produces: name-confirm step (input prefilled from the gate's stored name, editable, persisted to `certName`) → certificate view (course title, student name, date of generation, best score, instructor line "David O'Brien · Course Instructor" — verify David's preferred name form by grepping how the course/gate signs things; if unclear use "Course Instructor" alone and flag) → a Print / Save as PDF button invoking the browser print path such that ONLY the certificate prints (study the existing `?print=` machinery first; either a `?print=certificate` route or print-CSS isolation, whichever fits the existing pattern — say which you chose and why in the report).
- [ ] Design: house tokens, serif display for the title, generous whitespace, rule lines; landscape-friendly print CSS; no borders/clip-art, no emoji on the certificate.
- [ ] Gate honestly: certificate affordance renders only when `bestScore >= 80`.
- [ ] Verify (cycle +): set `final-exam` bestScore to 85 via evaluate_script; walk name-confirm → certificate; screenshot the certificate view; open the print path (screenshot print preview via Chrome MCP if possible, else the print-view route directly); confirm a sub-80 state hides the affordance.
- [ ] Commit.

---

### Task 4: Retitle, sweep, wrap

**Files:** Modify `index.html`, `briefing.md`, memory files (outside repo, uncommitted).

- [ ] `SECTION_META.whatyoulearned` → label **"The Final"** (kicker proposal: "PROVE IT"; keep an appropriate icon); check `CLOSE_BOARDS` (whatyoulearned currently has none — confirm; The Final's landing is the certificate, no close board needed; if one exists, retire it to the parking lot).
- [ ] Gate labels pointing at the lesson: `makeyourmove`'s gate label → "Next: The Final". Opener overview LAND IT card/bridge updated ("the big picture, then prove it" flavor — truthful).
- [ ] Export: regenerate the lesson's export under slug `the-final` (delete the old `what-you-learned.*` if present; note the print=lesson view must not include the interactive quiz — verify how TRY ITs export today and match that convention).
- [ ] Sweep: grep for "What You Learned" across repo (fix or justify; parking-lot/spec/plan docs historical); briefing map line + any lesson-shape notes; count stays 55.
- [ ] Memory: phase 4 complete (The Final live: bank of 50, 20-draw, 10:00, 80% certificate; spec's beat 4 done; pending phase 5 opener rewrite + editorial pass + export regen batch). MEMORY.md hook updated.
- [ ] Full verification cycle + print-view spot check of the retitled lesson. Commit.

---

## Self-review notes (applied)

- Count stays 55 throughout; no routing changes at all (the lesson keeps id and position); the only chain-visible change is gate labels.
- The quiz never blocks navigation (house rule: gates are soft; the Back to Start gate stays always-available).
- Task 2's reload-behavior decision (in-flight attempt does not survive reload) is deliberate: simplest honest behavior, no anti-cheat pretense, note it in the report.
- The bank task renders nothing, so its commit is verifiable as a no-visual-change commit (validate()/chain unchanged) — clean bisection point.
