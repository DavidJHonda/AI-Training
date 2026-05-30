# Course Restructure — 8 Content Sections → 5-Part Spine (Design)

**Date:** 2026-05-30
**Scope:** Structural resequence of `index.html`. No teaching content rewritten.
**Goal:** Improve the learning arc — collapse the spine from 8 content sections to 5 parts
(plus Intro and Finish), split judgment into "Check the Output" and "Protect Yourself,"
move Controls ahead of prompting, and make the course narrate its own structure correctly.

---

This is a structural resequence of index.html. No teaching content gets rewritten.
Lessons move, the course spine changes from 8 content sections to 5 (plus Intro and Finish),
two new section containers get created, three openers get written fresh, and the copy that
narrates the structure gets updated to match.

Decisions already made (do not relitigate):
- Controls moves AHEAD of the prompting lessons (pick the tool, then use it).
- The big judgment section splits into two parts: "Check the Output" and "Protect Yourself."
- "Understand AI" is ONE SECTION_GROUPS entry containing Foundations + Inside AI + AI Answers
  (see SYSTEM 1 for the full treatment — this was the one genuinely ambiguous point and it's
  now resolved).
- Component function definitions stay where they are in the file. Order lives in the data
  structures and the nav chain, not in source layout. Do not relocate 1000-line function
  blocks. Let the SECTION_COMPONENTS registry (~line 14275) do the routing.
- Per-lesson useLocalStorage keys are content-keyed, not position-keyed, so reordering does
  NOT orphan saved progress. Leave them alone. (Verify only that the course-level "current
  section" pointer stores a section ID, not a numeric index. If it stores an index, fix it.)
- Three openers get written fresh and go in the copy-approval queue (David approves before
  finalizing): the merged Work With AI opener, the Judgment I opener, the Judgment II opener.
  Do NOT auto-finalize opener copy. Build structure with placeholders if needed and flag.


## TARGET STRUCTURE

SECTION_GROUPS becomes exactly 7 entries:

1. Intro — unchanged (no part pill, same as today)
2. Understand AI — Foundations + Inside AI + AI Answers, one entry (see SYSTEM 1)
3. Work With AI
4. Judgment I: Check the Output
5. Judgment II: Protect Yourself
6. Build Your Advantage
7. Finish — unchanged (no part pill, same as today)

Badge denominator becomes /7. The five content parts read 02/07 through 06/07. Intro (01)
and Finish (07) carry no pill.

Lesson assignments (in order) for the parts that change:

Understand AI (one part, three movements, current internal order preserved):
  [Foundations movement] openerfoundations, aihistory, llms, aiismath, howwegothere,
    aivscode, norules, data
  [Inside AI movement] openerinside, tokens, embeddings, vectorspace, insidethemodel,
    attention, layers, training
  [AI Answers movement] openeranswers, prompt, patterns, probability, inference, whatitdoesbest

Work With AI:
  [new merged opener], modelselection, choosemodel, thinkingmode, temperature, customization,
  questionsvaluable, prompting, thoughtpartner

Judgment I: Check the Output:
  [new opener], critical, verify, evaluating, hallucination, trainingbias, documenttrap

Judgment II: Protect Yourself:
  [new opener], mindtrap, flattery, engagementtrap, supporttrap, whennot, howmuchtocheck,
  studying, integrity, privacy, seeingisntproof

Build Your Advantage:
  openerrealworld, workchanges, agents, aijudges, stakeholders, aifuture, humanedge,
  creativethinking, buildedge


## THE SIX LESSON MOVES

1. critical (Critical Thinking): Workflow -> Judgment I
2. verify (How to Verify): Workflow -> Judgment I
3. evaluating (Evaluating the Results): Workflow -> Judgment I
4. creativethinking (Creative Thinking): Workflow -> Build Your Advantage (2nd to last, before buildedge)
5. humanedge (Skills That Matter): Human Judgment -> Build Your Advantage (before creativethinking)
6. seeingisntproof (Seeing Isn't Proof): Real World -> Judgment II

Note on move 6: kept deliberately, with framing. The skill it teaches is "doubt what comes
at you, fakes are cheap now" — auditing reality, not auditing the tool's output. That's
self-protection, which is why it lands in Judgment II (Protect Yourself), not Judgment I
(Check the Output). New position: last in Judgment II, after privacy. Strong adjacency —
privacy is "guard what you put in," seeingisntproof is "doubt what comes at you"; together
they close the part on a protect-yourself note. (privacy already exits to seeingisntproof in
the old Real World chain ~line 11307, so the seam may already be clean — confirm.)


## SYSTEM 1: SECTION_GROUPS — "Understand AI" treatment (the resolved ambiguity)

"Understand AI" is ONE SECTION_GROUPS entry holding all three former sections in their current
order. This is what makes the 5-part spine real in the sidebar and lesson eyebrows, instead of
existing only as a word in the Roadmap.

"Unchanged internally" governs exactly two things and nothing more:
  (1) The lesson order and teaching content inside the block do not move.
  (2) openerfoundations, openerinside, and openeranswers STAY as full OpenerSection pages —
      Illustrations, question cards, "BIG QUESTIONS" blocks, framing KeyInsights all intact.
      They are NOT demoted to in-section dividers. (OpenerSection is a heavy standardized
      component per briefing line 58; gutting these to SectionKickers would be a teardown.)

What DOES change: those three openers stop being top-level group openers and become the three
movements inside the single "Understand AI" part. The sidebar and every lesson eyebrow across
all three movements read "Understand AI."

Badges within Understand AI:
  - Only openerfoundations carries the part pill (02/07).
  - openerinside and openeranswers DROP the part pill.
  - If a marker is wanted on the two interior openers, use a quiet hand-authored movement label
    ("Understand AI · 2 of 3" style), NOT another NN/07 pill. Three identical-denominator pills
    stacked inside one part would read as broken.

Apply the same one-entry logic to every top-level part: each is one SECTION_GROUPS entry with
one part pill on its lead opener.


## SYSTEM 2: BADGES — derive from SECTION_GROUPS (don't hand-type)

Badges are currently hand-typed strings "NN / 10", one per opener, and they went stale the
moment the structure moved. Replace with a value DERIVED from SECTION_GROUPS so it never drifts
again.

Current hand-typed locations (for reference, all being replaced by the derived value):
  line 1304 "02 / 10", line 5231 "03 / 10", line 6497 "04 / 10", line 8817 "05 / 10",
  line 7354 "06 / 10", line 8116 "07 / 10", line 2511 "08 / 10", line 10988 "09 / 10"

Derivation rules:
  - Denominator = number of SECTION_GROUPS entries = 7.
  - The pill shows the part's index within SECTION_GROUPS (02 through 06 for content parts).
  - Intro (01) and Finish (07) carry NO pill — skip them, matching today's behavior.
  - One pill per part, on the part's lead opener only (see SYSTEM 1 for the Understand AI
    interior-opener exception).
  - Movement labels on interior Understand AI openers stay hand-authored.


## SYSTEM 3: SECTION_META (line ~1200+)

- Add entries (kicker / label / icon) for the two new Judgment parts.
- Add/repurpose the meta for the merged "Work With AI" part.
- Retire or repurpose the metas that named the old standalone Workflow, Controls, Traps, and
  single Human Judgment sections, since those groupings no longer exist.


## SYSTEM 4: THE nextLessonId / completeAndNavigate CHAIN

Every lesson hands off to the next by a hardcoded string, either as nextLessonId on opener
components or as a completeAndNavigate("...") call in NextLessonGate/PrimaryButton. Reordering
means re-pointing every handoff at the seams. The seams that change:

- AI Answers exit: whatitdoesbest currently -> openerusing. Re-point to the new Work With AI
  opener / first Controls lesson (modelselection), since Controls now follows Understand AI.
- Controls internal chain (modelselection->choosemodel->thinkingmode->temperature->customization)
  stays intact internally.
- customization exit: currently -> openercontrols-era target (line ~9940 region, "Next:
  Controls" -> openercontrols). Now customization flows INTO questionsvaluable (start of the
  prompting cluster inside Work With AI). Rethread.
- prompting/thoughtpartner cluster exit: now exits into critical (start of Judgment I), not
  into the old Controls opener.
- critical->verify->evaluating stay chained to each other, but the cluster now OPENS Judgment I.
  evaluating's exit must point into hallucination.
- Traps chain (hallucination->trainingbias->documenttrap->mindtrap->flattery->engagementtrap->
  supporttrap): hallucination, trainingbias, documenttrap close Judgment I; mindtrap onward
  open Judgment II. The documenttrap->mindtrap handoff now crosses a part boundary. Rethread.
- humanedge and creativethinking relocate to Build Your Advantage. Rethread their handoffs AND
  the handoffs of lessons currently pointing AT them:
    - line ~2708: a gate currently -> humanedge ("Next: Skills That Matter"). Source lesson no
      longer precedes humanedge. Re-point to whatever now follows it in its part.
    - line ~9541: a gate -> critical ("Next: Critical Thinking") from the prompting cluster.
      Confirm/rethread for new order.
    - line ~8838: openerusing nextLessonId is creativethinking — and openerusing is being
      retired entirely (see SYSTEM 5). Moot, but noted.
- aifuture exit (line ~13967): currently -> buildedge ("Next: Build Your Edge"). New Build
  Your Advantage order inserts humanedge then creativethinking between aifuture and buildedge.
  Re-point aifuture -> humanedge and change the label.
- Build Your Advantage keeps openerrealworld as its opener (copy changes, see SYSTEM 5),
  gains humanedge + creativethinking, loses seeingisntproof to Judgment II.

After every step, click the full nav chain Intro -> Finish to confirm no dead handoffs.


## SYSTEM 5: OPENERS

Three openers RETIRE from the nav chain: openerusing, openercontrols, openerjudgment.
Three openers get WRITTEN FRESH (copy to David's approval queue, do not auto-finalize):

1. Work With AI opener (replaces openerusing + openercontrols).
   - openerusing currently describes a THREE-job sequence ("bring your angle / ask clearly /
     check what comes back"). The "check" third is being removed (critical/verify/evaluating
     leave for Judgment I). openercontrols described the standalone Controls section.
   - New job: "pick the right tool, then use it well." Flows into modelselection.

2. Judgment I: Check the Output opener.
   - Pedagogical basis: this part is about the ARTIFACT — is what AI handed me true and good?
     Lessons: critical, verify, evaluating, then the three output-property traps (hallucination,
     trainingbias, documenttrap).
   - Opener job: "AI's answer is a draft, not a verdict. Here's how to check it before you
     trust it."

3. Judgment II: Protect Yourself opener.
   - Pedagogical basis: this part is about the INTERACTION — the tool acting on you, and the
     calls that stay yours. Lessons: the manipulation traps (mindtrap, flattery, engagement,
     support), then whennot, howmuchtocheck, studying, integrity, privacy, seeingisntproof.
   - Opener job: "The tool can work on you, not just for you, and some calls stay yours no
     matter how good it gets."

Do NOT inherit openerjudgment's body into either new opener: its copy summarizes the Traps as
already-completed ("you've learned the warning signs: AI can hallucinate, feel like a mind,
flatter you..."), which is wrong now that the traps are split across both Judgment parts.

openerrealworld (Build Your Advantage opener) stays as the opener but its copy needs updating:
it loses seeingisntproof and gains humanedge + creativethinking. Any "you'll see..." preview
copy must reflect the new contents and the new ending shape (this part is now where the course
lands emotionally — "when everyone has AI, what makes me valuable?").


## SYSTEM 6: THE ROADMAP LESSON (intro, line ~3379-3416)

Hardcodes the old structure. Update:

- ROADMAP array (line ~3381): 10 hardcoded rows, one per old section. Collapse to the new
  spine. The middle sections become: Understand AI, Work With AI, Judgment I, Judgment II,
  Build Your Advantage. Rewrite each row's section name, `question`, and `outcome`. Note the
  old "Workflow" row's outcome ("without handing over your thinking, your honesty, or your
  data") actually describes Judgment now — move that framing to the Judgment rows.
- subtitle (line ~3396): "Ten stops, one route." Stop count changes. Update.
- body (line ~3399): "Six lessons in... the rest of the course is each section, one more thing
  you take control of." "Six lessons in" stays accurate (Intro unchanged). Update "each
  section" framing to the new spine: understand it -> use it -> keep your judgment -> build
  your advantage.

This is the course narrating its own structure up front; it must match the new arc.


## SYSTEM 7: IN-BODY CROSS-REFERENCES (prose that depends on lesson order)

Most "you just saw / earlier" references are inside the Understand AI block (Embeddings,
Patterns, Context, Attention, Training — lines ~4401, 5901, 7161, 9148, 9152, etc.). That
block's internal order is unchanged, so those all hold. Leave them.

These break and need attention:

NEEDS REWRITE:
- creativethinking, line ~9989: "This isn't Critical Thinking, which asks if the answer is
  right. It isn't Questions Matter, which is about phrasing your prompt cleanly. Creative
  Thinking sits one layer earlier than either: what angle are you bringing before AI even gets
  the question?" — creativethinking now moves to near the END (Build Your Advantage). Critical
  Thinking and Questions Matter are far BEHIND it, not adjacent/upcoming. The "sits one layer
  earlier" framing breaks. Rewrite for its new position.
- (openerjudgment line ~2499 is moot — openerjudgment is retired per SYSTEM 5.)

VERIFY (likely fine, confirm referent still immediately precedes):
- workchanges, line ~10127: "You just saw which parts of work AI takes over first." workchanges
  still opens Build Your Advantage, but its predecessor changes (now follows the Judgment II
  close). Confirm "you just saw" still lands or adjust.
- line ~13120: "You just saw the four kinds of work AI is built for." Confirm the referent
  still immediately precedes after resequencing.
- humanedge, line ~14106: "Earlier in the course you saw newer AI-related roles like prompt
  engineer..." Referent is workchanges, which comes BEFORE humanedge in the new order
  (workchanges 1st, humanedge 6th). Safe — confirm only.

SAFE (no change, noted so it isn't touched):
- line ~6808: "Remember the lesson on Context Window?" Context Window is in the Understand AI
  block (unchanged), and Work With AI now follows it — this reference is better positioned now.


## DO NOT CHANGE

- Internal order of the Foundations / Inside AI / AI Answers lessons, and Finish.
- Any lesson's actual teaching content, activities, or interactions. Pure resequence + reframe.
- Per-lesson saved-progress localStorage keys.
- The three Understand AI openers' status as full OpenerSection pages.
- The component function definitions' location in the file.


## SUGGESTED BUILD ORDER (so the file never breaks between steps)

Each step independently testable in the browser before the next.

1. Rewrite SECTION_GROUPS to 7 entries + update SECTION_META. Switch badges to the derived
   value (SYSTEM 2). No nav-chain changes yet. Verify sidebar/progress grouping renders, pills
   read 02/07–06/07, Intro/Finish show none, the two interior Understand AI openers show no
   part pill. Nav still works because handoffs are untouched.
2. Re-thread the Controls-before-prompting seam (AI Answers exit, customization exit) and build
   the fresh Work With AI opener (placeholder copy ok). Verify click-through of Work With AI in
   the new order.
3. Move the judgment cluster: rethread critical/verify/evaluating, build the Judgment I and
   Judgment II openers (placeholder copy ok), rethread the documenttrap->mindtrap part boundary
   and the seeingisntproof move. Verify click-through.
4. Relocate creativethinking + humanedge into Build Your Advantage, rethread
   aifuture->humanedge->creativethinking->buildedge and every gate that pointed at the old
   positions. Update openerrealworld copy. Verify click-through to the end.
5. Copy pass: the Roadmap lesson (array + subtitle + body), the creativethinking cross-reference
   rewrite (line ~9989), and the verify-list confirmations. Final opener copy for the three
   fresh openers (Work With AI, Judgment I, Judgment II) pending David's approval.

After each step, click the full nav chain from Intro to Finish to confirm no dead handoffs.


---

## Code-verification notes (added during spec review, 2026-05-30)

Confirmed against the current `index.html` so the build starts from verified ground. These do
not alter the spec above; they record what was checked and two small corrections.

**Confirmed — no fix needed:**
- **Section pointer stores an ID, not an index.** `progress.activeSection` holds a section id
  (`activeSection: "welcome"`, `activeSection: id`; lines ~14375–14416). Reordering will not
  orphan the course-level pointer or saved progress. The "verify only" item in the decisions
  list is satisfied.
- **Built-in invariant checker exists** (line ~14652): validates every `SECTION_GROUPS` id
  resolves in `SECTIONS` and that grouping coverage is complete. Plus `design-check.sh`. Use
  both as a fast pre-check before each browser pass.
- **Badge openers map** as: 1304 `openerfoundations`, 5231 `openerinside`, 6497 `openeranswers`,
  8817 `openerusing`, 7354 `openercontrols`, 8116 `openertraps`, 2511 `openerjudgment`,
  10988 `openerrealworld`.
- **`SECTION_GROUPS` label drives both the sidebar** (render at ~14576, labeled groups only)
  **and the per-lesson header eyebrow** ("SECTION NN · GROUP · LESSON NN", computed ~143–147).
  This is why the SYSTEM 1 collapse makes all 22 Understand AI lesson eyebrows read
  "Understand AI" — confirmed mechanism.

**Corrections to line references / claims in the spec above** (verified against live code; the
implementation plan carries the full verified seam table):
- **Move 6 / `privacy → seeingisntproof` is NOT pre-wired.** The spec's parenthetical (privacy
  already exits to seeingisntproof, ~line 11307) is incorrect. Verified current handoffs:
  `integrity → privacy` (11307), **`privacy → openerrealworld` (11687)**, and
  **`stakeholders → seeingisntproof` (11991)**. So in the new Judgment II,
  `privacy → seeingisntproof` is a **genuine new handoff** (re-point 11687), and
  `seeingisntproof`'s own exit (currently `→ aifuture`, 12134) must be re-pointed to
  **`openerrealworld`** (the Build Your Advantage opener).
- **`customization` exit is at line 7090** (`completeAndNavigate("openertraps")`, "Next: Traps"),
  **not** ~9940. Line **9940 is `evaluating → openercontrols`** ("Next: Controls"). Both re-point:
  `customization → questionsvaluable`, and `evaluating → hallucination`.
- **A fourth opener retires: `openertraps`.** SYSTEM 5 named three retirees (openerusing,
  openercontrols, openerjudgment), but the Traps section dissolves entirely (its lessons split
  across Judgment I and II), so `openertraps` is orphaned too. All four stay defined in the file
  but are removed from `SECTION_GROUPS` and `SECTION_COMPONENTS` (dead-component warnings are
  non-fatal per the invariant checker, but unregistering them keeps the checker output clean).
- **Three fresh opener ids** to add to `SECTION_COMPONENTS` + `SECTION_GROUPS`: `openerworkwith`
  (Work With AI), `openercheck` (Judgment I), `openerprotect` (Judgment II).
- **Badge derivation** uses the render at line **658** (`ov.badge` inside `OpenerSection`'s
  `renderOverview`, which has `props.sectionId` in scope) — replace with a `partBadge(sectionId)`
  helper keyed on `group.sections[0]`, so only each part's lead opener shows a pill and
  interior Understand AI openers (`openerinside`, `openeranswers`) get none automatically.
