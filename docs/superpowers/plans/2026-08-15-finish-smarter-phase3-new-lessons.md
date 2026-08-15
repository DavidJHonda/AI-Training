# Finish Smarter Phase 3 — Four New Lessons Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the four new Finish Smarter lessons — AI Tips, Communication & People, Skills That Matter (rebuilt), Make Your Move — taking the section from 6 to 10 lessons and the course from 51 to 55, then resequence to the spec's final beat order.

**Architecture:** Single-file React app (`index.html`). Process per the trap-lesson playbook: parallel design docs → David approves directions (checkpoint) → sequential builds, one lesson per task, course working at every commit. Content sources: `docs/superpowers/specs/2026-08-15-finish-smarter-dedupe-audit.md` (survivor lists + David's additions — the content contract) and `docs/parking-lot.html` (verbatim parked copy incl. the revived Ask AI moves).

**Tech Stack:** React.createElement inline JS; shared components (InteractiveBox, ShowcaseBox, ScenarioRow, FeedbackPill, QuizBlock, LabeledCardStack, Callout, KeyInsight, Takeaway, SectionKicker, BodyP, closeBoard, NextLessonGate); localStorage state; no build step.

## Global Constraints

- **Voice:** David's — short sentences, colon setups, balanced contrast, NO em-dashes, no exclamation points outside quoted AI speech. Every design/build agent loads the `my-writing-style` skill (via the Skill tool) before writing copy.
- **Tone:** serious, clear, credible, sharp; accessible to smart 16-year-olds without dumbing down; no fast-aging product claims.
- **Lesson shape:** opener paragraphs (transitions live at the BEGINNING; no cross-references to other lesson titles in the opener) → demonstration/teaching beats (a box must demonstrate, never restate) → close board → capstone TRY IT (every teaching lesson has one; per-item feedback; no Takeaway after per-item feedback) → `LessonRule` → `NextLessonGate` ("Next: X" label). Close board before the TRY IT; the closing paragraph must not restate the board.
- **New lesson ids (fixed for all tasks):** `aitips`, `peopleskills`, `skillsthatmatter`, `makeyourmove`. ids are permanent; labels can change later.
- **Registry contract per new lesson:** entry in the Finish Smarter `sections` array (position per task), `SECTION_META` (kicker/label/icon), `SECTION_COMPONENTS`, `CLOSE_BOARDS` (pill + sticky), gate re-chains on neighbors, opener overview card + accurate bridge. New lessons sit after the `faketrap` draft boundary → they render Draft automatically; that is correct.
- **Audit fidelity:** survivor content moves per the audit doc's named lists (`THOUGHTPARTNER_INVENTORY` → aitips; `HUMANEDGE_SURVIVORS` → skillsthatmatter; `BUILDEDGE_SURVIVORS` → makeyourmove; David's additions per their recorded destinations). EDGE_CARDS' four move names survive verbatim in skillsthatmatter (buildedge's survivor copy cites them by name). Known survivor-copy fixes to apply when the copy lands: the "Verify and Evaluate" two-lesson citation becomes "Evaluate the Results"; the "Thought Partner" by-name citation is rewritten (that lesson no longer exists); "Skills That Matter gave you four moves" citation stays valid.
- **Sweep rule (learned in phases 1–2):** stray-reference sweeps must include RETITLED labels, not just dissolved ids.
- **Verification cycle (every build task ends with ALL of it):**
  1. `s=$(grep -n "^<script>" index.html | tail -1 | cut -d: -f1); e=$(awk -v s="$s" 'NR>s && /<\/script>/{print NR; exit}' index.html); sed -n "$((s+1)),$((e-1))p" index.html | node --check -` → silent pass
  2. Serve port 8754 + Chrome DevTools MCP: console `✓ validate(): all N lessons pass structural checks` (N stated per task)
  3. Chain trace: consecutive-pair assertion over `SECTION_GROUPS.flatMap(g=>g.sections)`; last id asserts its stated course-ending target
  4. `bash design-check.sh` → PASS (never raise a baseline; lower only when deletions demand it, stated in the commit body)
  5. Screenshot the new/changed lesson top-to-bottom; kill the server
- **Exports:** attempt `scripts/make-lesson-pdfs.sh` for the new lesson's slug; if the Chrome path is blocked, note "export pending regen pass" in the commit body (house precedent). Lesson slugs: `ai-tips`, `communication-and-people` (or the approved title's slug), `skills-that-matter`, `make-your-move`.
- **Commit style:** imperative subject; bullet body; `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>` trailer. Commit per task; push only on David's word.
- **Editing gotcha:** lines mixing literal `\uXXXX` escapes and real unicode defeat the Edit tool; use sed/python there.

---

### Task 1: Four parallel lesson design docs

**Files:**
- Create: `docs/superpowers/specs/2026-08-15-phase3-design-aitips.md`, `...-peopleskills.md`, `...-skillsthatmatter.md`, `...-makeyourmove.md`
- Read-only: audit doc, parking-lot.html, spec, briefing.md, index.html (neighbor lessons for arc fit; shared component vocabulary)

**Interfaces:**
- Consumes: audit named lists; parked entries (Ask AI moves, ThinkingTogetherStatic worked example, close-board pill candidates incl. buildedge's reserved "Your move now." pair and the "curiosity is the new currency" candidate line)
- Produces: four design docs, each the build contract for its Task 2–5. Required sections per doc: **Thesis** (one bolded sentence); **Arc position** (what the lesson before/after it does; opening bridge intent); **Structure** (ordered beats: each beat = kicker + content type [prose/box/cards] + which survivor or new copy fills it, survivors cited by audit-list name + item); **What's NEW to write** (explicit list); **Close board** (proposed pill + sticky); **Capstone TRY IT** (mechanic, item count, what it drills, per-item feedback approach); **SECTION_META proposal** (kicker/label/icon); **≤4 judgment calls for David** (real forks only).

- [ ] **Step 1: Dispatch four design agents in parallel** (they do not edit anything). Each loads `my-writing-style`, reads the audit + its survivor list + relevant parked entries + its neighbor lessons in index.html, and writes its design doc. Per-lesson seeds:
  - **aitips** (position: after choosemodel, beat 1): "things good AI users know," not power-user tricks. Sources: parked Ask AI four moves (parking lot, "Ask AI — whole lesson removed") — "Ask me whatever you need about me and this job to do ___ well" flagged strongest; `THOUGHTPARTNER_INVENTORY` (five thought-partner prompts, opening thesis, TP_MOVES TRY IT as practice-candidate, ThinkingTogetherStatic worked example parked as optional exhibit); room for 2–4 new tips (candidates the designer proposes: e.g. ask for options not answers; tell it what you already tried; make it quiz you; start a fresh chat when it drifts — designer's call, grounded in course teachings).
  - **peopleskills** (position: after integrity/Habits in the final order, beat 2 opener): one thesis, ladder structure communicate → collaborate → lead; content from David's additions items 1a/1b (persuasive speaking, storytelling, reading a room, active listening, teamwork, conflict resolution, leading peers); all-new copy; the "AI can synthesize information, but people hire, follow, and collaborate with people they trust" idea from David's source list is the seed the thesis should sharpen.
  - **skillsthatmatter** (position: after creativethinking, beat 2 closer/roundup): rebuilt roundup of skills the course doesn't teach elsewhere. Sources: `HUMANEDGE_SURVIVORS` (opening production-to-direction thesis, Break down messy problems, Taste/judgment/prioritization, EDGE_CARDS four moves + MISSING_SCENARIOS TRY IT, Spot the Stronger Use TRY IT, closing thesis) + David's additions (adaptability, resilience & ambiguity tolerance, learning how to learn, ethical judgment). Designer decides which of the two inherited TRY ITs survives as capstone (or a fused one) — flag as judgment call if close.
  - **makeyourmove** (position: after becurious, beat 3 closer): the directives lesson. Sources: `BUILDEDGE_SURVIVORS` nearly whole (floor/middle/edge, Five Places Depth Still Pays + Spot the Gap TRY IT, HOW TO BUILD DEPTH incl. "Make things, not just prompts", five closing calls); reserved close-board pair "Your move now." / "The tool is ready. Are you?"; apply the two known citation fixes (Global Constraints). Mostly assembly + fresh bridges; designer states what little is new.

- [ ] **Step 2: Controller sanity pass** — the four docs don't overlap each other's territory (e.g. aitips vs peopleskills both claiming "ask better questions" territory would repeat phases 1–2's dedupe sin); beat bridges match the final target order; ids/slugs per Global Constraints.

- [ ] **Step 3: Commit the four docs** (one commit).

- [ ] **Step 4: CHECKPOINT — David approves the four directions** (+ rules on each doc's judgment calls). STOP until approved. Edits from David land in the design docs before builds start.

---

### Task 2: Build AI Tips (`aitips`)

**Files:**
- Modify: `index.html` (new `AITipsSection` component + registries), `briefing.md` (map line + count), opener overview
- Create: none (component lives in index.html)

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-08-15-phase3-design-aitips.md` (as amended at the checkpoint) — the build contract
- Produces: `aitips` routed after `choosemodel`; gates: `choosemodel`→`aitips` ("Next: AI Tips"), `aitips`→`creativethinking` (current interim order; final resequence happens in Task 6); validate() = 52

- [ ] **Step 1:** Load `my-writing-style`; read the design doc + audit items it cites + parked source copy; write the component following the design doc exactly (deviations only for discovered problems, flagged in the report).
- [ ] **Step 2:** Wire registries per the Global Constraints contract; insert into `sections` after `choosemodel`; re-chain gates; add opener overview card + adjust beat bridge if it now lies.
- [ ] **Step 3:** Full verification cycle (N=52). Export attempt per Global Constraints.
- [ ] **Step 4:** Update briefing.md (count 52, map line). Commit.

---

### Task 3: Build Communication & People (`peopleskills`)

**Files/Interfaces:** same pattern as Task 2. Consumes its design doc. Position: insert after `creativethinking` for the interim (final order lands in Task 6 — but if David approved a different final label/title at the checkpoint, use it). Gates: `creativethinking`→`peopleskills`, `peopleskills`→`becurious`. validate() = 53.

- [ ] Steps 1–4 as Task 2, adjusted to this lesson (N=53).

---

### Task 4: Build Skills That Matter (`skillsthatmatter`)

**Files/Interfaces:** same pattern. Consumes its design doc. Position: insert after `peopleskills`. Gates: `peopleskills`→`skillsthatmatter`, `skillsthatmatter`→`becurious`. validate() = 54. EDGE_CARDS four move names must appear verbatim (downstream makeyourmove copy cites them).

- [ ] Steps 1–4 as Task 2, adjusted (N=54).

---

### Task 5: Build Make Your Move (`makeyourmove`)

**Files/Interfaces:** same pattern. Consumes its design doc. Position: insert after `becurious`. Gates: `becurious`→`makeyourmove`, `makeyourmove`→`whatyoulearned`. validate() = 55. Apply the two citation fixes from Global Constraints; claim the reserved "Your move now." close-board pair if the approved design kept it.

- [ ] Steps 1–4 as Task 2, adjusted (N=55).

---

### Task 6: Final resequence to spec order + sweep

**Files:**
- Modify: `index.html`, `briefing.md`, `docs/parking-lot.html` (only if strays found), memory files (outside repo)

**Interfaces:**
- Consumes: everything above
- Produces: final Finish Smarter order `["openerskills", "choosemodel", "aitips", "integrity", "peopleskills", "creativethinking", "skillsthatmatter", "becurious", "makeyourmove", "whatyoulearned"]` — 10 lessons; `whatyoulearned` becomes the course's last lesson and takes the Back to Start gate verbatim (`nav: true`, target `"welcome"`, label "🗺️ Back to Start"); `integrity` (Habits for the Road) moves to beat 1 and gates `integrity`→`peopleskills` ("Next: " + peopleskills' approved label); `aitips`→`integrity` ("Next: Habits for the Road"). All other gates re-chained to match; opener overview groups + bridges made exactly truthful for the final order.

- [ ] **Step 1:** Resequence `sections`; re-chain every affected gate; move the Back to Start gate from `integrity` to `whatyoulearned` (integrity gets a standard "Next:" gate).
- [ ] **Step 2:** Opener overview final pass (four beats, cards + bridges truthful).
- [ ] **Step 3:** Stray-reference sweep incl. retitled labels; draft-boundary check; briefing.md final (count `55 lessons across 6 section groups.`, full map line).
- [ ] **Step 4:** Full verification cycle (N=55; last id `whatyoulearned` → `"welcome"`). Screenshot the opener overview + whatyoulearned's gate.
- [ ] **Step 5:** Memory update (phase 3 complete; pending: The Final + certificate [phase 4], opener rewrite [phase 5], deferred edit pass, export regen). Commit.

---

## Self-review notes (applied)

- Counts: 51 → 52 → 53 → 54 → 55 across Tasks 2–5; Task 6 rearranges without count change; matches the spec's 10-lesson section.
- Course ending never breaks: Back to Start stays on `integrity` through Task 5; moves to `whatyoulearned` in Task 6.
- Interim insert positions in Tasks 2–5 keep each new lesson adjacent to a stable neighbor so each commit's chain is simple; the one big resequence happens once, in Task 6.
- The two known stale-citation fixes and the EDGE_CARDS name dependency are pinned in Global Constraints so build agents can't miss them.
