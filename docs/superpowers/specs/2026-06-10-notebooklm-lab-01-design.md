# Lab 01: Build Your Exam-Prep Machine (NotebookLM) — design

**Date:** 2026-06-10
**Lesson:** Study with AI (`studying` section in `index.html`)

## Context

First lab in the course. Labs are the hands-on layer pairing with theory
lessons: students actually use the tool the lesson recommends. Labs live as
**LAB blocks embedded at the end of their host lesson** (the same move as
SEE IT / TRY IT, which are box-level components, not pages). No new pages,
no navigation changes.

Labs are designed as **threads**: a lab can continue across lessons as
installments that build on the same artifact. This lab is installment one;
its artifact (the student's notebook) is what later installments return to.
A "Your Labs" summary page in the Finish section is deferred until two or
three labs exist.

Design constraint that shapes everything: the lab must be completable
**right now, by one person with a laptop** (~25 minutes). This serves both
delivery modes with one design: club sessions (30 min weekly; lesson one
week, lab the next) and self-paced students, including a future public
release. No "bring it back next week" dependency.

## Placement and identity

- Position: end of the Study with AI lesson, after the KeyInsight ("Pick
  the tool, then make it test you"), before `LessonRule` / `NextLessonGate`.
- New `InteractiveBox` variant: `lab`, with its own surface so labs read as
  a third box type alongside SEE IT (sand) and TRY IT (mint).
- **Surface: pale teal band** (approx `#e4f2f0`), **accent: deep teal**
  (approx `#0f766e`). Teal is unclaimed in the course (it appears only in a
  generic chart palette). Amber was rejected: it already carries
  warning/middle-verdict semantics. Blue was rejected: it is the dominant
  interior card color, including two panels in this same lesson. Exact hex
  values finalized with a visual check against mint adjacency at
  implementation time.
- Eyebrow: `LAB 01` with a tool-style glyph (final glyph chosen at
  implementation, consistent with the ◉ SEE IT / ✎ TRY IT convention).
- Title: **Build Your Exam-Prep Machine**.
- Header states the contract up front: about 25 minutes; needs a laptop, a
  Google account, and access to your class materials (backup provided).

## Structure: two parts

Copy always addresses the solo student. Club-session divergence (Nate/Luke
demo Part A on the shared screen, students skip to Part B) lives in the
facilitator note, never in app copy.

**Part A — See it work (about 5 minutes).** Load the starter kit sources
into a new notebook, generate a quiz, watch the machine run. Uniform,
stall-proof proof that the tool works before any personal materials enter
the picture.

**Part B — Build yours (about 20 minutes).** Numbered steps, each with a
self-check checkbox:

1. Pick a real test coming up in the next couple of weeks.
2. Create a notebook and name it like a binder (one notebook per subject,
   per the lesson's best practices).
3. Feed it three angles: your class notes, the teacher's slides or
   handouts, and one YouTube explainer you choose. Backup kit if you cannot
   reach your materials.
4. Generate a blind quiz using the exact prompt already shown in the
   lesson ("Generate a 10-question quiz from these sources only…").
5. Take it cold and grade yourself.
6. Click the citation on at least one answer to see where in your sources
   it came from.

**Wrap.** Your wrong answers are your study list; that is the machine
working. Keep this notebook: a later lab comes back to it. (The closing
clause plants the thread.)

## Completion behavior

- Checkbox state persists in `localStorage` like other interactions.
- The lab does **not** gate the next lesson. The `NextLessonGate` stays
  keyed to the Pick the Better Move activity. Reasoning: the lab happens
  outside the app and cannot be verified, and in the club rhythm a student
  finishes the lesson a week before the lab session.

## Backup kit

- Links only; nothing hosted or maintained in the repo.
- One fixed topic: **the French Revolution**. Three sources: a Crash
  Course video, a solid encyclopedia article, and a public-domain
  primary-source page. Exact URLs chosen and verified live at
  implementation.
- Presented as a card at the bottom of the block: "Can't reach your class
  materials? Use these and study this instead."

## Facilitator note

A short markdown doc at `docs/labs/lab-01-notebooklm.md`, outside the app:

- 30-minute session plan.
- The Part A demo move (one person on the shared screen).
- Circulation tips for common stalls (can't find notes, no upcoming test,
  source won't import).
- Optional two-minute coda if time remains: two volunteers say what they
  fed in and one question their quiz asked. Informal, not a structured
  activity.
- September pre-flight: **test NotebookLM on school Google accounts before
  the first meeting** (Workspace admins sometimes disable it); students'
  personal Google accounts are plan B. NotebookLM requires age 13+.

## Out of scope

- The "Your Labs" summary page in Finish (build when 2–3 labs exist).
- Future installments of this lab thread.
- Any change to existing lesson copy or the lesson's current gate.
- A per-section "Closer" lesson pattern (considered and rejected: labs
  pair with lessons, not sections).
