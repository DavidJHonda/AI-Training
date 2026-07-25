# r3 grading instructions — read fully before scoring

You are grading ONE NotebookLM lesson-overview video for an AI literacy course
aimed at 16-year-olds, under rubric r3. Your assignment names the slug, the
lesson file, and the bundle directory.

## Do this first

1. Read `/Users/davidobrien/Documents/GitHub/AI-Training/videos/video-rubric.csv`
   — the rubric is the authority, these instructions are the procedure.
2. Read the lesson file. This is the ground truth: the video is meant to
   substitute for THIS lesson.
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
r3 number. If you happen to already know an old score, ignore it.

## What you score

Six numbers. **Do not compute a total** — totals are assembled centrally.

| Field | Max | What it measures |
|---|---|---|
| TEACHING_COVERAGE | 20 | Every teaching beat of the lesson reaches the viewer. A beat the lesson spends a paragraph on and the video spends a clause on is PARTIAL coverage, not full. |
| TEACHING_LESSON_MATERIAL | 15 | The video uses the lesson's own analogies, numbers, examples, and order. A correct explanation built from material we didn't write still costs points here. |
| TEACHING_TEACHES_VS_RECITES | 15 | The why lands. A viewer could explain the idea back in their own words. Reciting correct lines with no explanatory work is the MIDDLE of this band, not the top. |
| TEACHING_BOARD_CONTENT | 10 | Whether the kit boards' points get taught — not whether the jpg appears pixel-exact. Canon: why-learn-ai's everyday-apps board redrawn as five scenes = no deduction, because the content landed. If NO kit boards exist on disk, grade instead whether the lesson's key structured content (its tables, frameworks, enumerated lists) reaches the screen in some form, and say `board-source: none on disk` in your evidence. |
| CLEANLINESS | 20 | Gibberish/pseudo-text costs points ONLY on content-carrying visuals (a garbled label on a teaching chart); incidental b-roll props are forgiven. Also legibility, text containment, and white-on-light text (hard visual fail). |
| PACING | 20 | Runtime fit and flow: no padding, no final-scene starvation, no dead time. |

### The dead-time rule (pacing)

A still frame costs NOTHING while the narration is still walking what is on
screen. A board held because each of its rows is being narrated is the lesson
working as designed, and is free. It costs only once the narration has moved
past what is displayed. A 47s dwell that outlasts its own content, or a 100s
pan across one illustration, is dead time and is charged. `holds.txt` pairs
every long hold with the narration underneath so you can tell these apart —
read both columns before deducting.

### Explicitly NOT graded

- **Animation.** Decommissioned in r3. Never deduct for stills, for lack of
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
- **Anchor the top.** A video enters the top teaching band only if a student
  could watch it INSTEAD of reading the lesson and lose nothing. "Covered the
  concepts" is the MIDDLE of the band, not the top. Be willing to use the
  middle of every range; a catalog where everything scores 90 is a broken pass.

## Ship gates — binary, scored separately from the number

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
GATE_SPINE: PASS|FAIL — <evidence>
GATE_RESTRAINT: PASS|FAIL — <evidence>
GATE_STOCK: PASS|FAIL — <evidence>
GATE_ENDING: PASS|FAIL — <evidence>
GATE_SYNC: PASS|FAIL — <evidence>
TOP_BAND: YES|NO — <could a student watch this INSTEAD of reading and lose nothing? one sentence>
BIGGEST_LEVER: <the single highest-value fix, and whether it needs a RE-ROLL or a REPAIR>
NOTES: <at most two lines, or "none">
```

Your final message is the return value and must be that block alone.
