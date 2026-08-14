# r4 grading instructions — read fully before scoring

You are grading ONE Gemini Notebook lesson-overview video for an AI literacy course
aimed at 16-year-olds, under rubric r4. Your assignment names the slug, the
lesson file, and the bundle directory.

## Do this first

1. From the repository root, read `videos/video-rubric.csv`
   — the rubric is the authority, these instructions are the procedure.
2. Read the lesson file. This is the grounding source: the video is meant to
   substitute for THIS lesson. Do not presume the source is infallible; perform
   the Source QA check below before treating it as authoritative.
3. Read the whole bundle:
   - `transcript.txt` — the narration, with timestamps. This is the spine.
   - `holds.txt` — spans with no scene cut, paired with the narration underneath.
   - `scenes.txt` — scene-cut times.
   - `sheets/*.jpg` — contact sheets, one frame every 4s with a red timestamp.
     **Read every sheet.** They are your only view of what is on screen; a
     grade that skipped them is not a grade.
4. If `lessons/<slug>-*.jpg` files exist, those are the kit boards this video
   was built from. Read them.

## Anti-anchoring — this matters

Do NOT look up this video's previous grade. Do not read the tracker sheet, do
not grep memory files, do not read git log or commit messages about this video,
do not read its prompt in `Prompts/`. The whole point of this pass is a fresh
r4 result. If you happen to already know an old score, ignore it.

## What you score

Six numbers. **Do not compute a total** — totals are assembled centrally.

| Field | Max | What it measures |
|---|---|---|
| TEACHING_COVERAGE | 20 | Every teaching beat of the lesson reaches the viewer. A beat the lesson spends a paragraph on and the video spends a clause on is PARTIAL coverage, not full. |
| TEACHING_LESSON_MATERIAL | 15 | The video uses the lesson's own analogies, numbers, examples, and order. A correct explanation built from material we didn't write still costs points here. |
| TEACHING_TEACHES_VS_RECITES | 15 | The why lands. A viewer could explain the idea back in their own words. Reciting correct lines with no explanatory work is the MIDDLE of this band, not the top. |
| TEACHING_BOARD_CONTENT | 10 | Whether the kit boards' points get taught — not whether the jpg appears pixel-exact. Canon: why-learn-ai's everyday-apps board redrawn as five scenes = no deduction, because the content landed. If NO kit boards exist on disk, grade instead whether the lesson's key structured content (its tables, frameworks, enumerated lists) reaches the screen in some form, and say `board-source: none on disk` in your evidence. |
| CLEANLINESS | 20 | Gibberish/pseudo-text costs points ONLY on content-carrying visuals (a garbled label on a teaching chart); incidental b-roll props are forgiven. Also legibility, text containment, and white-on-light text (hard visual fail). |
| PACING | 20 | ALLOCATION and flow. Runtime is NOT scored. Is the time budget spent where the LESSON puts its weight? Charged both ways: dwelling past a beat's content, and rushing a beat the lesson dwells on. Plus no padding, no final-scene starvation, no dead time. |

### Pacing is allocation, not length (redefined 2026-07-29)

**Total runtime is not scored.** A lesson with more to teach should produce a
longer video, and one that earns its length takes full marks. The minute range
in `Prompts/` is generation steering; scoring against it is the exact thing the
"never grade against the prompt" rule below forbids, and it is where that rule
kept leaking.

What you are scoring is whether the time budget matches the lesson's own
weighting. Keep it distinct from Coverage:

- **Coverage** asks whether every beat reached the viewer *at all*.
- **Pacing** asks whether the *proportions* match.

A video can land every beat and still spend 60% of itself on the opening
anecdote while rattling through the four core moves. Nothing is missing, so
Coverage is intact, but the shape lies about what matters. That is charged here,
and it is charged in both directions: dwelling past a beat's content, and
rushing a beat the lesson dwells on.

**Read `sections.txt` in the bundle before scoring this.** It gives each beat's
share of the video's seconds against that beat's share of the lesson's words, so
"felt rushed" becomes a number. Treat it as evidence, not a verdict: a worked
example legitimately takes longer to say than to write, and a board that is
being walked row by row is doing its job.

### The dead-time rule (pacing)

A still frame costs NOTHING while the narration is still walking what is on
screen. A board held because each of its rows is being narrated is the lesson
working as designed, and is free. It costs only once the narration has moved
past what is displayed. A 47s dwell that outlasts its own content, or a 100s
pan across one illustration, is dead time and is charged. `holds.txt` pairs
every long hold with the narration underneath so you can tell these apart —
read both columns before deducting.

### Explicitly NOT graded

- **Animation.** Decommissioned in r3 and still ungraded in r4. Never deduct for stills, for lack of
  motion, for static boards, or for "could have been more dynamic."
- **Style.** Dotted paper, paper-craft, live-action hands, photoreal spans,
  off-palette colors are all tolerated. Mention at most as a one-line note.

## Before you report ANY visual defect — two traps that produced false findings

The first r3 pass had roughly a 50% false-positive rate on visual claims. Both
causes come from the contact sheets sampling one frame every 4 seconds. Check
for these before you write down a visual deduction.

**Trap 1 — one frame of something that is MOVING.** These videos pan across
boards, build elements in, and animate counters. A single sampled frame of that
looks broken when it isn't. Real examples that were reported as defects and were
not: a board mid-pan reported as "a duplicated panel intruding at frame right";
a vocabulary counter caught mid-count reported as "wrong numbers" when it lands
on the lesson's exact figures; a 25%→50% bar animation reported as "24%/71%,
does not sum to 100" when the animation IS the lesson's teaching.
→ If the thing you are flagging could be mid-motion, say so, and check the
frames on either side in `scenes.txt` / `holds.txt` before deducting. A span
inside a long no-cut hold is safe to judge from one frame; a span at a scene
boundary or during a build is not.

**Trap 2 — reading horizontally across a multi-column board.** Comparison
boards put different text in left and right columns. Read across instead of
down and you get a garbled interleave that looks like corrupted rendering. Two
"scrambled text" and "duplicate-layer collision" findings were exactly this —
the boards were sharp. → When text looks scrambled on a board with columns,
re-read it column by column before calling it a defect.

**Claim types, by how much they can be trusted:**
- "gibberish text on a static prop" — reliable, this is the real repair work
- "cropped / clipped at the frame edge" — usually true but often resolved by a
  pan a second later; say whether it resolves
- "collided / scrambled / duplicated layers" — was false every time it was
  checked; treat with heavy suspicion

None of this applies to narration findings. Transcript-derived claims (missing
beats, register drift, mis-teaches) have no such failure mode.

## Scoring discipline — both directions

- **Cite or don't deduct.** Every deduction cites a timestamp or a quote.
- **Every full mark states what WOULD have cost a point.** A grader who can
  supply neither hasn't graded. This is the discipline that keeps a dimension
  from drifting to 95% of max.
- **Do not let the total compensate for failed teaching.** The /100 number ranks
  raw-material quality; it never overrides Source QA, Accuracy, Substitute, or
  Spine. Be willing to use the middle of every range; a catalog where everything
  scores 90 is a broken pass.

## Source QA — run before the video gates

The lesson grounds the video, but a source can carry a contradiction or a
materially wrong distinction. Read it once as an editor, not only as a matching
key.

SOURCE_QA passes only when the lesson's major claims and distinctions are
accurate and internally consistent. If two parts of the lesson conflict, or an
example undermines the rule it is supposed to teach, fail SOURCE_QA and cite the
exact lines. A video that faithfully repeats a source error is not a successful
alternative to reading. The sequence is: fix the lesson and its generation
prompt, then re-roll or repair the video.

Do not use this check for taste, wording preferences, or harmless compression.
It is for errors that could leave the learner with a wrong or self-contradictory
model.

## Instructional equivalence — an overriding gate, not a bonus

The primary job of every video is to replace the reading without losing
essential understanding. Evaluate this after the six scores, but never average
it into them.

GATE_ACCURACY passes only when the video teaches accurately and consistently.
Any material contradiction, reversal, or misleading distinction fails it,
whether the engine invented the error or inherited it from the source. If it
inherited the error, SOURCE_QA fails too.

GATE_SUBSTITUTE passes only when all of the following are true:

- every major teaching beat is meaningfully taught, not merely mentioned;
- essential examples, frameworks, and distinctions survive;
- the why lands well enough that a learner could explain the idea back;
- the central idea is understandable and usable without opening the lesson; and
- a student watching instead of reading would lose no essential understanding.

A high total cannot compensate for either failed gate. Minor optional detail may
be compressed; a major beat, essential example, core distinction, or explanatory
link may not. Failure normally means RE-ROLL. A donor graft is acceptable only
when it restores the whole beat coherently.

## Ship gates — binary, scored separately from the number

- SOURCE_QA: is the grounding lesson accurate and internally consistent? FAIL
  means fix the lesson and prompt before deciding how to repair the video.
- GATE_ACCURACY: is the video's teaching accurate and internally consistent,
  with no material contradiction or misleading distinction?
- GATE_SUBSTITUTE: can a student watch this instead of reading and lose no
  essential understanding? This is the non-compensable primary-goal gate.
- GATE_SPINE: does the narration miss a hard lesson requirement? (e.g.
  document-trap must say "Retrieval-Augmented Generation" in full; any verbatim
  line the lesson demands). FAIL here is the roll-killer.
- GATE_RESTRAINT: profanity legible on screen, depiction of a real person
  against a by-name ban, or banned imagery (self-harm, medical, red-staining).
  This is a course for 16-year-olds. Read every legible text span you can.
- GATE_STOCK: Getty/watermarked stock can never ship. Engine-generated
  photoreal is a STYLE call, not stock — note it, don't fail it. The lesson's
  own illustrations shown in-video are NEVER a violation of any kind.
- GATE_ENDING: ships only if it ends on the close board as the literal final
  frame — no outro, no engine-drawn sign restating the message.
- GATE_SYNC: elements appear as the narration mentions them; narration leads,
  visuals follow.
- GATE_BOARD_WALK: when narration walks two or more points on a kit board that
  is legible at whole-board scale, does the exact current lesson board remain
  fully visible for the complete walk, with the active card or row highlighted
  in spoken order? A substitute graphic, redraw, crop, zoom, or pan between
  points fails and needs a visual repair. Dense-board exception: a dive may
  frame the whole active card only when the text is genuinely unreadable at
  720p; never crop inside a card.

## Output format — exactly this, nothing before or after

```
SLUG: <slug>
RUNTIME: <m:ss>
TEACHING_COVERAGE: <n>/20 — <evidence with timestamp or quote>
TEACHING_LESSON_MATERIAL: <n>/15 — <evidence>
TEACHING_TEACHES_VS_RECITES: <n>/15 — <evidence>
TEACHING_BOARD_CONTENT: <n>/10 — <evidence>
CLEANLINESS: <n>/20 — <evidence>
PACING: <n>/20 — <evidence>
SOURCE_QA: PASS|FAIL — <lesson-line evidence; if FAIL, identify the source fix before rerolling>
GATE_ACCURACY: PASS|FAIL — <timestamp or quote; material teaching errors are non-compensable>
GATE_SUBSTITUTE: PASS|FAIL — <could a student watch instead of reading and lose no essential understanding? cite the decisive beats>
GATE_SPINE: PASS|FAIL — <evidence>
GATE_RESTRAINT: PASS|FAIL — <evidence>
GATE_STOCK: PASS|FAIL — <evidence>
GATE_ENDING: PASS|FAIL — <evidence>
GATE_SYNC: PASS|FAIL — <evidence>
GATE_BOARD_WALK: PASS|FAIL|N/A — <evidence; N/A when no qualifying multi-point kit board is walked>
BIGGEST_LEVER: <the single highest-value fix, and whether it needs a RE-ROLL or a REPAIR>
NOTES: <at most two lines, or "none">
```

Your final message is the return value and must be that block alone.

## Grade against THIS file, never against the prompt (added 2026-07-26)

The per-lesson prompts in `Prompts/` are **steering for generation**. They are
deliberately stricter than the rubric, because it is cheap to over-fence a
generator and expensive to repair a roll. They are NOT the grading standard.

Grading a roll against its prompt inflates the defect count and makes good rolls
look rejectable. This happened on the does-school-matter re-roll: five "rule
violations" were logged, and on re-check under the rubric, three of them were
not scoreable at all.

The two that catch people out:

- **Gibberish.** The rubric forgives incidental b-roll props outright. A phone
  with nonsense on it while the narration says "a draft appears in seconds" is
  incidental — the teaching point is that a draft appeared, not what it says.
  Gibberish costs points only on a visual the narration is teaching FROM.
- **Marks on boards.** There is no marks dimension in the current rubric. Zero. An engine
  highlight that tracks the narration through a board is a teaching aid, and on
  the layers re-roll it was correctly read as evidence the board was working.
  The original complaint that produced the blanket ban was close-board-specific
  ("fine on content boards, not on the close").

If a prompt rule is broken but the rubric does not score it, note it under SPEC
and move on. It does not touch the number.
