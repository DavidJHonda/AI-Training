# Finish Smarter merge — design

**Date:** 2026-08-15 · **Status:** approved in brainstorming, pending spec review

## Problem

Build Your Skills (7 lessons) and Finish Smarter (4 lessons) both feel weak — not
for lack of volume but for lack of identity. Neither section has a job it clearly
owns: Build Your Skills is a drawer of good-but-unrelated lessons; Finish Smarter
is an ending that doesn't end anything. The course has also had no end-of-course
knowledge check since the three dated finals (Vocab Quiz, Test Yourself, Beat the
Clock) were deleted 2026-06-26 with a rebuild-later note.

## Decision

Merge both sections into a single **Finish Smarter** that mirrors Start Smarter's
intent: Start Smarter is more than a course introduction; Finish Smarter is more
than a wrap-up. The section's job: *the course is done teaching you the tool —
here's what's left to say, what the tool can't do, and what you do next.*

The alternative — keeping two sections and writing content until each stands
alone — was considered and rejected: it treats an identity problem with volume,
stretches the course's ending across two sections when student attention is
scarcest, and asks an AI course to carry a standalone human-skills curriculum it
has less authority for. If the skills material genuinely grows later (labs layer,
capstones), it can split back out then, with earned content in hand.

Course structure becomes **6 section groups / 55 lessons** (from 7 / 56).

## The new section — 10 lessons, 4 beats

The arc's trajectory is the design: it starts at the tool and walks steadily
toward the person. Each beat is an opener-overview group.

### Beat 1 — THE LAST OF THE AI

1. **Opener** — NEW. Written to mirror Start Smarter's beyond-an-intro intent.
   Built last, once the section exists.
2. **Tune the Model** — kept as-is (its existing edit-down-later flag is out of
   scope here).
3. **AI Tips** — NEW. The parked Ask AI moves revived (its four meta-prompt moves
   are flagged in the parking lot as the strongest surviving idea with no other
   home), Thought Partner folded in, plus new tips. Framing: not power-user
   tricks — things good AI users know.
4. **Habits for the Road** — NEW as a page; merges Integrity + Privacy under
   their original two-habits-for-the-road framing: own what you submit, guard
   what you type. Absorbs When AI Judges You's core material in compressed form:
   detectors land in the integrity half, screening systems in the privacy half.
   Ends the beat on "what you type travels" — the course's last word about AI,
   pivoting the section toward the person.

### Beat 2 — SKILLS AI WON'T REPLACE

5. **Communication & People** — NEW (working title). One lesson, one thesis:
   these skills got more valuable the day everyone got the same AI. Ladder
   structure: communicate clearly → collaborate well → lead — each rung more
   human than the last. If it outgrows one strong idea per rung during writing,
   split it then; design it as one.
6. **Creative Thinking** — moves in as-is.
7. **Skills That Matter** — the name survives as the roundup lesson, rebuilt:
   only skills the course doesn't teach elsewhere, drawn from the humanedge /
   buildedge dedupe audit plus new additions.

### Beat 3 — YOUR MOVE

8. **Be Curious** — kept.
9. **Make Your Move** — NEW (working title). The concrete directives: make
   things, not just prompts; get good at something; whatever else survives the
   dedupe. Absorbs Your Edge's closing energy ("Your move now. The tool is
   ready. Are you?").

### Beat 4 — LAND IT

10. **The Final** — NEW. What You Learned's recap content opens the lesson as
    the study sheet, then a clear break ("That's the course. Ready to prove
    it?"), then the timed quiz and certificate. See below.

## The Final — mechanics

Defaults below are adjustable; treat them as the starting numbers.

- **Quiz:** ~20 questions per attempt drawn from a bank of ~50 covering all six
  sections, order shuffled, so a retake is a fresh test rather than a memorized
  answer key.
- **Timer:** 10-minute countdown (~30s/question), visible but not theatrical.
  Starts on the student's click, never on page load. Expiry submits whatever is
  answered.
- **No per-question feedback during the run** — this is a test, not a TRY IT.
  After submission: score plus a review screen where each miss is explained and
  points back at its lesson. That's what makes a retake worth something.
- **Certificate bar: 80%.** Below it: score, review, retake button. Unlimited
  attempts, best score kept.
- **Implementation posture:** reuse existing quiz components; localStorage for
  state like everything else. New machinery is limited to the timer and the
  bank-draw.
- **Non-goal:** anti-cheat. Everything is client-side and inspectable; in a
  teacher-run club that is a non-issue, and engineering against your own
  students is a non-feature.

## The certificate

- Name pre-filled from the welcome gate's name field, editable before
  generating (students will want their full name).
- An in-app certificate page in the course's design language — serious and
  credible per house tone. Fields: course title ("Be Smarter Than the Tool"),
  student name, completion date, score, instructor line.
- Print-to-PDF via the browser print path the app already uses for lesson
  exports. No backend, no accounts: its authority is the class, not
  cryptography.

## Fallout

- **Dissolved as standalone pages:** Thought Partner, Skills That Matter (old
  form), Your Edge, When AI Judges You, What You Learned, and Integrity +
  Privacy as separate pages. House pattern throughout: absorbed material moves
  with a note; cut-but-keepable material gets parking-lot entries; dedupe audits
  produce survivor lists.
- **Close boards:** the merged habits lesson needs one board (two exist today).
  Your Edge's "Your move now. The tool is ready. Are you?" should survive on
  Make Your Move or the section's final board.
- **Videos:** shipped videos attached to dissolved lessons retire to the donor
  pool; merged and new lessons need kits and tracker updates later, on the
  video track as usual. Restructure ships text-first.
- **Labs:** audit whether any of the eight labs live in affected lessons;
  re-home if so.
- **Mechanical sweep:** SECTION_GROUPS 7 → 6, briefing map and counts, draft
  boundary check (new lessons sit after `faketrap`, so they're drafts
  automatically), print groups, per-lesson PDF slugs, parking entries, memory
  updates.
- **Lesson ids:** house rule is ids stable across retitles. Merge/absorb id
  choices (e.g. whether Habits for the Road keeps `integrity`, whether The
  Final keeps `whatyoulearned`) are implementation-time decisions; record them
  in the briefing when made.

## Build order

Dependency-driven, course working at every commit:

1. **Dedupe audit** — read humanedge, buildedge, whatyoulearned against the
   course; produce survivor lists. Everything downstream depends on this.
2. **Structural resequence** — merge the sections, move keepers, park the
   dissolved. New-lesson slots may sit as drafts.
3. **New lessons one at a time** — trap-lesson-playbook process: parallel
   evals → David approves directions → sequential builds.
4. **The Final + certificate** — the one real feature build (timer, bank-draw,
   certificate render).
5. **Opener last** — it summarizes a section that by then exists.

## Open items

- Real titles for the working titles: AI Tips, Habits for the Road,
  Communication & People, Make Your Move, The Final.
- The quiz bank itself (~50 questions) is a content-writing task inside phase 4.
- Which skills the roundup lesson carries depends on the phase-1 audit plus
  David's additions.
