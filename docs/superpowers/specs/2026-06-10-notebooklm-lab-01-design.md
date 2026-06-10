# Lab 01: Build Your Course Notebook (NotebookLM) — design

**Date:** 2026-06-10 (revised same day: course-notebook pivot)
**Lesson:** Study with AI (`studying` section in `index.html`)

## Context

First lab in the course. Labs are the hands-on layer pairing with theory
lessons: students actually use the tool the lesson recommends. Labs live as
**LAB blocks embedded at the end of their host lesson** (the same move as
SEE IT / TRY IT, which are box-level components, not pages). No new pages.

**The pivot (decided 2026-06-10):** the notebook students build is about
**the course itself**. They print the part of the course they just
finished, feed that PDF to NotebookLM, and quiz themselves on it. This
replaces the earlier design (notebook for one of their school classes, with
a French Revolution backup kit). Why it wins:

- The materials problem disappears: every student has the course, club or
  self-paced public alike. No stalls, no stand-in topic, no backup kit.
- The quiz doubles as retrieval practice on the course content itself.
- It is the cleanest thread anchor: one printed packet per course part,
  one source per packet, added installment by installment. By the Finish
  section the notebook holds the whole course and the final quiz spans it.
- Real-class transfer is kept as the lab's final step (see Structure)
  rather than its core mechanic.

Design constraint unchanged: the lab must be completable **right now, by
one person with a laptop** (~25 minutes). Club rhythm: 30-minute weekly
meetings; lesson one week, lab the next. No "bring it back next week"
dependency.

## Course reorder (prerequisite)

Swap the last two lessons of Start Smarter so the part ends at the lab's
host lesson and the packet covers exactly what has been taught:

- Before: … `whybother` → `studying` → `control` → `openerfoundations`
- After: … `whybother` → `control` → `studying` → `openerfoundations`

Touches: the `SECTION_GROUPS` entry plus three `NextLessonGate` targets
(`whybother`→`control`, `control`→`studying`, `studying`→`openerfoundations`).
Verified: no lesson copy back-references the old order (checked the
openings of `control`, `studying`, and `openerfoundations` and the closings
of `whybother` and `control`), so no copy edits are needed.

## Print packets (prerequisite)

The existing Print Course PDF tool (`?print=all`, button in the app
footer/settings) renders every lesson for browser print-to-PDF. Extend the
same mechanism to one part at a time:

- `?print=<part-slug>` renders only that `SECTION_GROUPS` entry's lessons,
  using the same print layout. Slug = group label lowercased,
  non-alphanumerics collapsed to dashes (e.g. `start-smarter`,
  `understand-ai`). `?print=all` keeps its current behavior. An unknown
  slug falls through to the normal app.
- The three component-level print checks (`ActivityCounter`, `QuizBlock`
  mint print rendering, `RevealSequence`) currently test `print === "all"`;
  they must treat ANY non-empty print param as print mode.
- The lab links students to their packet (`?print=start-smarter`) and tells
  them to save it as a PDF.

**Known future need (deferred, David's call when its labs are designed):**
Understand AI stays one section (it matches the course arc) but is the
longest and most technical part; its labs will likely need mid-part
packets rather than waiting for the section's end. Possible shapes: a
sub-range print param or two packet checkpoints inside the part. Out of
scope for Lab 01.

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
- Title: **Build Your Course Notebook**.
- Header states the contract up front: about 25 minutes; needs a laptop
  and a Google account.

## Structure: one arc, seven checkboxed steps

Copy always addresses the solo student. Club-session divergence (one demo
on the shared screen before students start) lives in the facilitator note,
never in app copy. The earlier Part A / Part B split is gone: everyone
builds the same notebook from the same source, so the demo and the build
are the same act.

Intro line sets the meta-loop: you just learned what a source-grounded
tutor is; now aim it at this course.

1. **Print your packet.** Open the Start Smarter packet (link to
   `?print=start-smarter`), save as PDF via the browser print dialog.
2. **Create the course notebook.** At notebooklm.google.com, new notebook,
   named after the course ("Be Smarter Than the Tool"). It grows with you:
   every part of the course will land in it.
3. **Add the packet as a source.** One part, one source: the filing system.
4. **Generate a blind quiz.** The exact prompt already shown in the
   lesson's "Quiz yourself blind" tip ("Generate a 10-question quiz from
   these sources only…").
5. **Take it cold.** Close the lesson tabs, answer all ten, get graded.
6. **Click one citation.** It lands on the exact passage of the course
   that taught it.
7. **Transfer it.** This week: a second notebook for whichever class has
   the next test, fed with real class materials. The course showed you the
   machine; your grades are where it pays.

**Wrap.** Your wrong answers are your study list for the next club
meeting. Keep this notebook: every lab from here adds the next part of the
course to it, and the quizzes grow as you go. (Plants the thread.)

## Completion behavior

- Checkbox state persists in `localStorage` (`llm-` prefixed key so the
  existing reset flow clears it) like other interactions.
- The lab does **not** gate the next lesson. The `NextLessonGate` stays
  keyed to the Pick the Better Move activity. Reasoning: the lab happens
  outside the app and cannot be verified, and in the club rhythm a student
  finishes the lesson a week before the lab session.

## Facilitator note

A short markdown doc at `docs/labs/lab-01-notebooklm.md`, outside the app:

- 30-minute session plan: short demo of steps 1-4 on the shared screen,
  then everyone builds; optional informal share-out coda (two volunteers:
  one quiz question and how they scored).
- Circulation tips for common stalls (print dialog confusion, PDF upload,
  quiz showing answers because the prompt was paraphrased).
- September pre-flight: **test NotebookLM on school Google accounts before
  the first meeting** (Workspace admins sometimes disable it); students'
  personal Google accounts are plan B (NotebookLM requires age 13+). Also
  run the full packet → PDF → upload → quiz chain once end to end.

## Out of scope

- The "Your Labs" summary page in Finish (build when 2-3 labs exist).
- Future installments of this lab thread (one per course part).
- Mid-part packets for Understand AI (see Known future need above).
- Any change to existing lesson copy beyond the three gate labels the
  reorder requires.
- A per-section "Closer" lesson pattern (considered and rejected: labs
  pair with lessons, not sections).
