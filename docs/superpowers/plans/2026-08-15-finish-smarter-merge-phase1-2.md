# Finish Smarter Merge — Phases 1–2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Execute phases 1–2 of the Finish Smarter merge spec (`docs/superpowers/specs/2026-08-15-finish-smarter-merge-design.md`): the dedupe audit, then the structural resequence that merges Build Your Skills + Finish Smarter into one working 6-group section.

**Architecture:** Single-file React app (`index.html`, `React.createElement` calls, no build step). All routing derives from `SECTION_GROUPS`; every routed id must resolve in `SECTION_META` and `SECTION_COMPONENTS`. Merges use the house `embedded` prop pattern. Cut copy goes to `docs/parking-lot.html`, never comments.

**Tech Stack:** Vanilla JS + React via CDN in one HTML file; python http.server + Chrome DevTools MCP for verification; no test framework — the house verification cycle below is the test suite.

**End state of this plan:** 6 section groups, 51 lessons, course working at every commit. Interim Finish Smarter lineup: `openerskills, choosemodel, integrity (as Habits for the Road), creativethinking, becurious, whatyoulearned`. Dissolved and parked: `thoughtpartner, humanedge, buildedge, aijudges, privacy` (privacy merged, aijudges compressed). Follow-up plans add the four new lessons (→ 55) and build The Final.

## Global Constraints

- **Tone:** serious, clear, credible, sharp; never playful or youth-marketing (editing guidelines).
- **No em-dashes** in new course copy; `design-check.sh` baseline is the gate.
- **ids are stable across retitles** — the merged habits lesson keeps id `integrity`; never rename ids.
- **Transitions live at the BEGINNING of lessons**, never end-of-lesson handoffs.
- **Lesson shape:** ends on KeyInsight → TRY IT → gate; TRY-IT-last; gates are "Mark as complete" soft nudges (no `ready` prop exists).
- **Cut-but-reusable copy** goes in `docs/parking-lot.html` — new entries at the TOP of `<main>`, template in the HTML comment there. Entries: Origin / Possible destination / verbatim strong pieces / Full source git anchor.
- **Delete verified dead code** — when a component is dissolved, check definition + registries + call sites, then delete fully; git is the archive.
- **Edit-tool gotcha:** lines mixing literal `\uXXXX` escapes with real unicode chars (e.g. `’`) defeat Edit's escape-swapping; use `sed -i '' 'Nd'` line deletes or python line edits for those.
- **Verification cycle (every task ends with this; "VERIFY" below means all of it):**
  1. `s=$(grep -n "^<script>" index.html | tail -1 | cut -d: -f1); e=$(awk "NR>$s && /<\/script>/{print NR; exit}" index.html); sed -n "$((s+1)),$((e-1))p" index.html | node --check -` → must print nothing (pass)
  2. `python3 -m http.server 8753 --bind 127.0.0.1 &` then open `http://127.0.0.1:8753/index.html` via Chrome DevTools MCP; console must show `✓ validate(): all N lessons pass structural checks` with the expected N
  3. Chain trace in evaluate_script: walk `SECTION_GROUPS.flatMap(g=>g.sections)`, assert each component's `toString()` contains the next id; assert the last lesson (`aijudges` until Task 4 dissolves it... see per-task notes) points where the task says
  4. `bash design-check.sh` → PASS (bump a baseline ONLY when the task says so)
  5. Screenshot the lessons the task touched; eyeball for layout breaks
- **Commit style:** imperative subject, bullet body, end with `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`. Commit after each task; do not push until David says so or the plan completes.

---

### Task 1: Dedupe audit

**Files:**
- Create: `docs/superpowers/specs/2026-08-15-finish-smarter-dedupe-audit.md`
- Read-only: `index.html` (components: grep `SECTION_COMPONENTS` for the ids below)

**Interfaces:**
- Consumes: nothing (first task)
- Produces: the audit doc. Every later content move in this plan and the follow-up plans cites it. Its four survivor lists are named exactly: `HUMANEDGE_SURVIVORS`, `BUILDEDGE_SURVIVORS`, `THOUGHTPARTNER_INVENTORY`, `AIJUDGES_CORE`.

- [ ] **Step 1: Read the five components in full.** Find each in `index.html` via `SECTION_COMPONENTS` (grep the ids `humanedge`, `buildedge`, `thoughtpartner`, `aijudges`, `whatyoulearned` to get function names, then read each function completely, including consts and helper components used only by them).

- [ ] **Step 2: Write the audit doc** with this exact structure per lesson (five sections):

```markdown
## <id> — <current label>
### Taught elsewhere (CUT list)
- "<claim/skill/box name>" — duplicate of <lesson id> "<where>" (verbatim quote of the overlapping line from BOTH lessons)
### Survivors (KEEP list)
- "<claim/skill/box name>" — appears nowhere else; destination: <target lesson per spec>
### Verbatim copy worth parking regardless
- <quotes>
```

For each candidate overlap, actually grep the course for the competing coverage (e.g. "ask the right questions" → `questionsvaluable`) and quote both sides. The known seed examples from the spec: "ask the right questions" is taught (Questions Matter) → CUT; "Make things, not just prompts" is untaught → SURVIVOR (destination: Make Your Move). For `aijudges`, `AIJUDGES_CORE` lists exactly which boxes/paragraphs carry (a) the detector material → destination integrity half, (b) the screening-systems material → destination privacy half, (c) everything else → parking. For `whatyoulearned`, the audit only inventories what its recap covers (it survives until the follow-up Final plan) and flags recap claims that will be stale after this plan's resequence. For `thoughtpartner`, inventory every tip-shaped unit for the future AI Tips fold.

- [ ] **Step 3: Self-check the audit.** Every unit of each lesson is in exactly one list (CUT / SURVIVOR / park). No unit unaccounted for — the follow-up plans treat this doc as exhaustive.

- [ ] **Step 4: Commit**

```bash
git add docs/superpowers/specs/2026-08-15-finish-smarter-dedupe-audit.md
git commit -m "Dedupe audit for Finish Smarter merge (phase 1)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

- [ ] **Step 5: CHECKPOINT — David reviews the audit.** Stop. Do not start Task 2 until David approves the survivor lists (he said he'll likely add skills; additions land in the audit doc before the moves happen).

---

### Task 2: Merge the section groups and update the interim opener

**Files:**
- Modify: `index.html` — `SECTION_GROUPS` (the two group objects; grep `label: "Build Your Skills"` and `label: "Finish Smarter"`), the `openerskills` opener wrapper component (grep `openerskills` in `SECTION_COMPONENTS` for its function name), and the gate of `choosemodel` (grep `completeAndNavigate && props.completeAndNavigate("thoughtpartner")` — it currently gates to Thought Partner per the Ask AI removal)
- Modify: `briefing.md` — the two group map lines and the "56 lessons across 7 section groups" line

**Interfaces:**
- Consumes: nothing from Task 1 (structure only — no content moves yet)
- Produces: the merged group. All later tasks assume `SECTION_GROUPS` has 6 groups and Finish Smarter = `["openerskills", "choosemodel", "thoughtpartner", "humanedge", "creativethinking", "becurious", "buildedge", "whatyoulearned", "integrity", "privacy", "aijudges"]` (an 11-lesson interim superset — dissolves happen in Tasks 3–5 so the course works at every commit).

- [ ] **Step 1: Replace the two groups with one.** Delete the `{ label: "Build Your Skills", sections: [...] }` object and change the Finish Smarter object to:

```js
}, {
  label: "Finish Smarter",
  sections: ["openerskills", "choosemodel", "thoughtpartner", "humanedge", "creativethinking", "becurious", "buildedge", "whatyoulearned", "integrity", "privacy", "aijudges"]
}];
```

(Keepers first in eventual spec order, dissolve-pending lessons still routed. `openerskills` becomes the merged section's title page; `aijudges` is temporarily last and already carries the course-ending "🗺️ Back to Start" gate from the 2026-08-15 cut, so the course ending stays intact through this task.)

- [ ] **Step 2: Re-chain the gates for the new order.** The interim order changes which lesson follows which. Grep each affected component's `NextLessonGate` and set: `openerskills`→`choosemodel` (already true), `choosemodel`→`thoughtpartner` (already true), `thoughtpartner`→`humanedge` (already true), `humanedge`→`creativethinking` (already true), `creativethinking`→`becurious` (already true), `becurious`→`buildedge` (already true), `buildedge`→`whatyoulearned` (WAS the section end or →whatyoulearned? grep and fix to `whatyoulearned`, label `"Next: What You Learned"`), `whatyoulearned`→`integrity` (already true), `integrity`→`privacy` (already true), `privacy`→`aijudges` (already true), `aijudges`→Back to Start (already true). Only edit gates the grep shows are wrong; record in the commit body which ones changed.

- [ ] **Step 3: Update the interim opener.** In the `openerskills` opener wrapper: set its group label references and `sectionOverview` groups to match the interim lineup (four groups per the spec beats, listing only currently-routed lessons). Do not write the new opener copy (that's phase 5); only fix the overview cards and any "Build Your Skills" self-references so nothing on the page lies. Retitle its `SECTION_META` label to `"Opener"` style consistent with other openers if it isn't already.

- [ ] **Step 4: Update `briefing.md`:** merge the two map lines into one `- **Finish Smarter (11 — interim, mid-merge):** ...` line listing the interim order, and change the header line to `56 lessons across 6 section groups.` (count unchanged this task — nothing dissolved yet). Add one sentence noting the merge is mid-flight per this plan.

- [ ] **Step 5: VERIFY.** validate() must report 56; chain trace passes with the new order; design-check PASS.

- [ ] **Step 6: Commit** (subject: `Merge Build Your Skills into Finish Smarter (structure only)`).

---

### Task 3: Dissolve Thought Partner, Skills That Matter, and Your Edge

**Files:**
- Modify: `index.html` — remove the three ids from the Finish Smarter `sections` array; delete their `SECTION_META`, `SECTION_COMPONENTS`, `CLOSE_BOARDS`, and `LESSON_VIDEOS` entries (grep each id across the whole file; also grep `CHIP_LABELS` and the labs/`LESSON_LABS` registry if one names them); delete their component functions and any helpers used only by them; re-chain gates `choosemodel`→`humanedge`... becomes `choosemodel`→`creativethinking`? NO — see Step 1 order note.
- Modify: `docs/parking-lot.html` — three new entries at top of `<main>`
- Delete: `lessons/<slug>.md` + `lessons/<slug>.pdf` for the three (grep `ls lessons/` for their title slugs)
- Modify: `briefing.md` — interim count and map line

**Interfaces:**
- Consumes: Task 1's `HUMANEDGE_SURVIVORS`, `BUILDEDGE_SURVIVORS`, `THOUGHTPARTNER_INVENTORY` (quoted verbatim into the parking entries' survivor notes)
- Produces: interim `sections` array `["openerskills", "choosemodel", "creativethinking", "becurious", "whatyoulearned", "integrity", "privacy", "aijudges"]`; gate chain `choosemodel`→`creativethinking`, `becurious`→`whatyoulearned`.

- [ ] **Step 1: Remove the three ids from `sections`** so the array reads exactly as in Interfaces above.

- [ ] **Step 2: Re-chain the two broken gates:** `choosemodel`'s gate → `creativethinking` (label `"Next: Creative Thinking"`), `becurious`'s gate → `whatyoulearned` (label `"Next: What You Learned"`).

- [ ] **Step 3: Delete each lesson's code fully.** For each id: grep the whole file for the id AND the component function name; delete the function, exclusive helpers/consts (verify each helper has zero other call sites before deleting — `CoreLoopBox`-style shared components must survive), and all registry entries. If any of the three has a shipped video in `LESSON_VIDEOS`, delete the entry and note the orphaned `videos/*.mp4` in the commit body (file stays in the donor pool; tracker sheet update is a follow-up-plan item).

- [ ] **Step 4: Write the three parking entries** at the top of `docs/parking-lot.html` `<main>`, per the template comment there. Each entry: Origin (dissolved 2026-08-15 into the Finish Smarter merge, spec link), destination note (Thought Partner → future AI Tips lesson; humanedge survivors → rebuilt Skills That Matter roundup; buildedge survivors → future Make Your Move; each citing the audit doc), the close-board pills verbatim (`buildedge`: "Your move now." / "The tool is ready. Are you?" — flag it as reserved for Make Your Move or the section's final board per spec), and Full source git anchors (the function names).

- [ ] **Step 5: Delete the three lessons' `.md`/`.pdf` exports** from `lessons/`.

- [ ] **Step 6: Update `briefing.md`** map line and count: `53 lessons across 6 section groups.`

- [ ] **Step 7: VERIFY.** validate() = 53; chain trace passes; screenshot `choosemodel` bottom (new gate) and the opener overview.

- [ ] **Step 8: Commit** (subject: `Dissolve Thought Partner, Skills That Matter, Your Edge (parked)`).

---

### Task 4: Habits for the Road — merge Privacy into Integrity, compress When AI Judges You

**Files:**
- Modify: `index.html` — `IntegritySection` + `PrivacySection` (grep registry for exact names), `SECTION_META` `integrity` entry, `CLOSE_BOARDS`, `sections` array, gates; delete `aijudges`' `WhenAIJudgesSection` and exclusive helpers after extraction
- Modify: `docs/parking-lot.html` — entries for aijudges and for any Integrity/Privacy copy cut in the merge
- Delete: `lessons/` exports for privacy + aijudges slugs; regenerate/rename integrity's export slug per the new title (note: export regeneration needs the make-lesson-pdfs.sh Chrome path — if blocked, delete stale exports and flag regeneration in the commit body, matching house precedent)
- Modify: `briefing.md` — count + map + the "Merges use the `embedded` prop" example list if it names these lessons

**Interfaces:**
- Consumes: Task 1's `AIJUDGES_CORE` (the exact detector/screening pieces and their destinations)
- Produces: id `integrity` relabeled **"Habits for the Road"**; `sections` array `["openerskills", "choosemodel", "creativethinking", "becurious", "whatyoulearned", "integrity"]`; `integrity` carries the course-ending Back to Start gate.

- [ ] **Step 1: Merge via the house `embedded` pattern.** `PrivacySection` gains an `embedded` prop (swaps its `LessonHeader` for a `SectionKicker` seam, suppresses its own `LessonRule`/`NextLessonGate`), rendered inside `IntegritySection` after integrity's content. Integrity half first (own what you submit), privacy half second (guard what you type) so the lesson ends on "what you type travels" per spec. Write a one-paragraph bridge at the START of the privacy half (transitions-at-beginning rule), not a handoff at the end of the integrity half.

- [ ] **Step 2: Compress aijudges per `AIJUDGES_CORE`.** Move the detector material into the integrity half and the screening-systems material into the privacy half, compressed to a beat each (a box or short kicker run, not a lesson-within-a-lesson). Everything in `AIJUDGES_CORE`'s park list goes to the parking entry.

- [ ] **Step 3: Meta + boards.** `SECTION_META` `integrity` → `{ kicker: "TWO HABITS FOR THE ROAD", label: "Habits for the Road", icon: keep integrity's }`. `CLOSE_BOARDS`: replace the two entries with one on `integrity` — proposed copy (David can veto at checkpoint): pill `"Own what you submit. Guard what you type."` sticky `"Two habits. They travel well."` Park both old pill pairs verbatim in the parking entry. The `closeBoard("privacy")` call inside the embedded half is removed; `closeBoard("integrity")` sits at the merged lesson's close, before its TRY IT, per convention.

- [ ] **Step 4: Activities check.** The merged lesson keeps at most the strongest TRY IT set; if both halves carry TRY ITs, keep both only if they test different skills (integrity's and privacy's do — keep both, integrity's mid-lesson at its half's end, privacy's last, TRY-IT-last rule satisfied by the final one). Any dropped activity is parked verbatim.

- [ ] **Step 5: Routing.** Remove `privacy` and `aijudges` from `sections`; delete `WhenAIJudgesSection` + exclusive helpers (grep-verify) and all `privacy`/`aijudges` registry entries (meta/components/boards/videos/chips). Give `integrity` the Back to Start gate verbatim: `React.createElement(NextLessonGate, { nav: true, onClick: function() { props.completeAndNavigate && props.completeAndNavigate("welcome"); }, label: "🗺️ Back to Start" })`. Re-chain `whatyoulearned`'s gate → `integrity` (label `"Next: Habits for the Road"`).

- [ ] **Step 6: Parking + exports + briefing.** Parking entries (aijudges full entry; merge-cut copy entry if anything was dropped). Delete `lessons/` exports for privacy and aijudges slugs. Briefing: count `51 lessons across 6 section groups.`, map line final interim order, embedded-pattern example updated.

- [ ] **Step 7: VERIFY.** validate() = 51; chain trace ends `integrity` → welcome; screenshot the full merged lesson top to bottom; design-check PASS (if the merge deleted em-dash-bearing copy and the count drops below baseline, bump the baseline DOWN in `design-check.sh` in this commit and say so).

- [ ] **Step 8: Commit** (subject: `Merge Integrity+Privacy into Habits for the Road; compress When AI Judges You`).

- [ ] **Step 9: CHECKPOINT — David read-through** of the merged lesson before the plan is called done.

---

### Task 5: Mechanical sweep and wrap-up

**Files:**
- Modify: `briefing.md` (final pass), `docs/parking-lot.html` (only if sweep finds strays), memory files per below
- Read-only sweep targets: `index.html`, `scripts/`, `packets/`, `videos/`, `lessons/`

**Interfaces:**
- Consumes: everything above
- Produces: a clean tree for the phase-3 plans.

- [ ] **Step 1: Stray-reference sweep.** Grep the repo (excluding git history and `docs/parking-lot.html`) for every dissolved id and old label: `thoughtpartner`, `humanedge`, `buildedge`, `aijudges`, `privacy` (as a routed id), `"Build Your Skills"`, `"Thought Partner"`, `"Skills That Matter"` (should only remain as the future roundup name in spec/plan docs), `"Your Edge"`, `"When AI Judges You"`. Every hit is either fixed, or justified in the commit body (e.g. historical parking-lot text, spec docs, video tracker names pending the video-track follow-up).

- [ ] **Step 2: Draft-boundary check.** Confirm the boundary id `faketrap` still resolves and the intended lessons show Draft; the merged section's first lesson (`openerskills`) must not show Draft (title-page exemption is automatic).

- [ ] **Step 3: Update memory.** `project_finish_smarter_merge.md`: phases 1–2 DONE with date, interim lineup, checkpoint outcomes, pointer to the audit doc; note follow-up plans pending (new lessons ×4, The Final, opener). Update `MEMORY.md` hook line to match. Update the labs memory ONLY if Step 1 found a lab re-home (spec flagged the audit; record the finding either way).

- [ ] **Step 4: Final VERIFY** (full cycle) plus one extra: print-view spot check — open `?print=lesson:integrity` and confirm the merged lesson renders for export.

- [ ] **Step 5: Commit** (subject: `Finish Smarter merge phases 1-2: sweep and wrap`) and, with David's go-ahead, push the branch of commits.

---

## Self-review notes (already applied)

- Spec coverage: phases 1–2 fully tasked; phases 3–5 explicitly deferred to follow-up plans (spec's own checkpoint gates make them unplannable in detail today). The spec's "labs audit" lives in Task 5 Step 1+3; "videos retire to donor pool" lives in Task 3 Step 3 and Task 4 Step 5 with tracker updates deferred to the video track.
- Counts audited: 56 (Task 2, structure only) → 53 (Task 3, −3) → 51 (Task 4, −2). Follow-ups: +4 new lessons = 55 per spec.
- Interim course ending is never broken: Back to Start lives on `aijudges` through Task 3, moves to `integrity` in Task 4 Step 5.
- Type/name consistency: survivor-list names (`HUMANEDGE_SURVIVORS` etc.) defined in Task 1 and consumed by name in Tasks 3–4.
