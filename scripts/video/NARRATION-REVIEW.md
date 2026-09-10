# Narration review (owner rule, 2026-09-10)

Read this file completely before reviewing a lesson video. It replaces the r5
grader and every numeric rubric. There are no scores, dimensions, or totals.

The course is for 16-year-olds. A video's job is to replace the lesson reading.

## The one question

**Does the narration teach the current lesson accurately, clearly, and
completely?** A student who watches instead of reading must lose no essential
understanding. Everything else about a roll is editing work.

## Required inputs

1. The current lesson: the live page in `index.html` and its Markdown under
   `lessons/`. Read it as an editor. It is the grounding source, not presumed
   infallible.
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
   - **TAUGHT**: reaches the viewer with enough substance to preserve its meaning.
   - **THIN**: named or shown but not explained; a paragraph reduced to a clause.
   - **MISSING**: not spoken. Displaying a sentence or table is not teaching it.
   - **WRONG**: contradicts the lesson, reverses a distinction, or misstates a number.
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

When comparing rolls, choose the one whose narration teaches most completely.
Complete and slightly overlong beats concise and incomplete, because excess can
be cut and missing narration cannot be added. Visual defects never decide the
choice; list them as editing notes.

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
