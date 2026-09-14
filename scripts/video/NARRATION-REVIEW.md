# Narration review (owner rule, 2026-09-10)

Read this file completely before reviewing a lesson video. It replaces the r5
grader and every numeric rubric. There are no scores, dimensions, or totals.

The course is for 16-year-olds. A video's job is to replace the lesson reading.

## The one question

**Does the narration teach the current lesson accurately, clearly, and
completely?** A student who watches instead of reading must lose no essential
understanding. Everything else about a roll is editing work.

## Required inputs

1. The current lesson. **The live page in `index.html` is the authority**: the
   essential teaching points are what a student reads there. Read it as an
   editor; it is the grounding source, not presumed infallible. The Markdown
   under `lessons/` is the upload source and tells you what the roll was asked
   to teach. It may carry more than the page (video-prep nuance such as Support
   Trap's activity detail); teaching taken from it is an accurate addition, not
   an error. If the Markdown lacks something the page teaches, that is a
   materials bug: fix it before the next roll and say so in EDITING NOTES.
2. The complete timestamped transcript of the candidate
   (`grade_bundle.py` writes `transcript.txt`). Listen to the audio wherever the
   wording matters or the transcript is uncertain.
3. For a finished edit, watch the whole file end to end.

A review that skips the lesson or the full transcript is not a review.

## Procedure

1. List the lesson's teaching points in lesson order: the hook or problem, each
   explanation, every worked example and its numbers, the distinctions, the
   hard requirements (full terms such as "Retrieval-Augmented Generation",
   verbatim lines, the two closing lines), and the takeaway.
2. Walk the transcript and mark each point:
   - **RICH**: taught with the lesson's own example, reason, or comparison intact,
     in words a student can follow; the beat a teacher would keep.
   - **TAUGHT**: reaches the viewer with enough substance to preserve its meaning.
   - **THIN**: named or shown but not explained; a paragraph reduced to a clause.
   - **MISSING**: not spoken. Displaying a sentence or table is not teaching it.
   - **WRONG**: contradicts the lesson, reverses a distinction, or misstates a number.
   RICH and TAUGHT both pass; the distinction exists so that two rolls can be
   compared beat by beat (owner rule 2026-09-14: presence is not quality).
3. Note additions. An accurate addition that improves clarity is welcome and may
   be a candidate lesson edit. Weaker or distracting outside material is flagged.
4. Read worked examples aloud in your head against the transcript: the narration
   must actually read or explain the sentence, values, or comparison.
5. Give the verdict.

## Verdict

- **KEEP**: every essential point TAUGHT, no WRONG. Proceed to production.
- **REPAIR**: the teaching is complete but one of these applies: removable
  excess or repetition, a misplaced beat, or a single wrong word or phrase that
  a coherent donor phrase from existing course narration can replace.
- **REROLL**: any essential point MISSING or WRONG, or a hard requirement
  missed. A corrected graphic never fixes spoken teaching.

## Comparing rolls: beat by beat, then a best-of plan (owner rule 2026-09-14)

Presence is not quality. Two rolls of the same lesson are compared per teaching
point, not by their totals: AI Is Different roll 1 covered more points and won,
while roll 2 explained the Kryptonite board far better, and the build shipped
the weak explanation. That is the failure this section prevents.

For every teaching point, rate each roll (RICH / TAUGHT / THIN / MISSING / WRONG)
and quote the sentence each roll actually speaks, with its timestamps. Where the
rolls differ, name the better one. The result is a **best-of plan**: the base roll
that carries the spine (usually the one with the most complete coverage and the
verbatim close), plus the beats to take from the other roll.

Rules for the plan:

- A beat is taken from the alternate roll only when it is a whole beat between
  silences (a sentence or a coherent run of sentences), not a phrase.
- The safe place for a mid-video graft is under a course board: the picture is
  ours during a board walk, the rolls share the Notebook voice, and levels are
  matched, so only the audio seam is at risk. Beats that sit under Notebook's own
  drawings are grafted only when the drawing's scene can carry the longer or
  shorter audio without an orphan beat; otherwise note them as "richer in roll N,
  not grafted" so the owner can decide.
- The board leg stretches or shrinks to the grafted audio; its rings follow the
  alternate roll's spoken onsets.
- Complete and slightly overlong still beats concise and incomplete for the base
  roll, because excess can be cut and missing narration cannot be added. Visual
  defects never decide the choice; list them as editing notes.
- The owner reads the quoted pairs and arbitrates ties. He does not need to watch
  both rolls; the table is the comparison.

## Source QA

If the lesson itself contains a material error or contradiction, say so with
the exact lesson line and the correction. Fix the lesson and the generation
materials before repairing or rerolling the video. Taste, wording preference,
and harmless compression are not Source QA failures.

## Not evaluated here

Visual quality, Notebook highlighting, the engine's close, gibberish props,
animation, style, and runtime. Those belong to the ship checklist in
`scripts/video/README.md`, which the editor verifies on the finished file.

## Output

Return exactly this block and nothing else:

When two or more rolls are reviewed, add one block after the per-roll blocks:

```text
BEST-OF PLAN: <slug>
BASE: <file> (<why>)
  <teaching point> — roll 1 RICH|TAUGHT|THIN|MISSING @<m:ss> "<quote>" | roll 2 … @<m:ss> "<quote>" — TAKE roll N (under <board> | Notebook scene | not grafted: <why>)
  ...
GRAFTS: <count>, all under boards | <exceptions>
```

Per-roll block:

```text
LESSON: <slug>
CANDIDATE: <file> (<m:ss>)
VERDICT: KEEP | REPAIR | REROLL
TEACHING POINTS:
  <point> — TAUGHT|THIN|MISSING|WRONG — <timestamp or quote>
  ...
HARD REQUIREMENTS:
  <full term or verbatim line> — MET|MISSED — <timestamp or quote>
ERRORS: <timestamp — what was said — what the lesson says> | none
SOURCE_QA: PASS | FAIL — <lesson line and correction>
ADDITIONS: <accurate additions worth keeping or adding to the lesson> | none
EDITING NOTES: <replaceable visual defects, excess to cut, pause points> | none
LISTENING: <what was heard rather than read; anything still unheard>
```
