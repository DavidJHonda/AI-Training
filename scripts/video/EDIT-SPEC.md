# Edit spec: scope and production standards

Updated 2026-09-15. [README](README.md) is the shared workflow and shipping
checklist; [Narration Review](NARRATION-REVIEW.md) owns teaching verdicts;
[Technical Recipes](TECHNICAL-RECIPES.md) holds implementation details.
This file owns build scope and board/audio treatment.

## 1. Scope: full production or narrow repair

A **full production pass** prepares a raw roll or unfinished edit for shipping.
Apply the standards below throughout the candidate, preserving compliant spans
rather than rebuilding them unnecessarily.

A **narrow repair** fixes the named issue in an existing video. Keep unaffected
teaching, audio, visuals, and timing unchanged unless the requested fix requires
an identified dependency. A visual-only repair does not authorize new pauses,
audio cleanup, narration changes, or a course-wide redesign.

State the scope in the edit plan. If the request names a specific defect, treat
it as a narrow repair; if it asks for a complete production edit, apply the full
pass. Identify necessary related changes before building. Complete authorized
work and report unrelated defects separately; propose a broader pass instead of
silently expanding the task. Reuse approval already given for the same work.

Every changed span must meet the applicable standards below. A narrow candidate
may retain known pre-existing defects outside scope, but the review must list
them and must not label it ready to ship. All standard videos must satisfy the
whole-file ship checklist before publication. Passing that checklist is separate
from the owner's authorization to publish.

## 1b. Review the board plan before the first build (owner rule, 2026-09-16)

Include a brief board-highlighting and camera plan with the video evaluation.
Inspect the current assets and follow the actual narration. Present one row per
board in scope, using its exact title; for a narrow repair, list only affected
boards and preserve previously approved treatment elsewhere.

| Board | Highlighting sequence | Camera | Reason or exception |
|---|---|---|---|
| <exact title> | <whole card, then named sections as spoken; or whole card throughout; or unmarked> | <full board; or full view then complete-card zoom> | <brief reason, only where useful> |

- Brief examples supporting one idea normally use a whole-card outline throughout
  that card's explanation. Numbered items alone do not require separate rings.
- When narration meaningfully explains distinct sections, introduce the whole card
  with its outline, then replace that outline with one around the named section
  as it is spoken. Follow sections, not individual sentences. Use one outline at
  a time unless the narration explicitly compares multiple targets.
- Apply the full-board opening and compact/dense rules below. Zoom only when it
  materially improves readability, keeping the complete active card visible,
  including its illustration, title, and bottom section. Tall cards may gain little
  from a zoom. Flag uncertain framing for a preview rather than promising a benefit.
- Identify unusual treatments and their reasons. Do not add pauses to accommodate
  outline changes or camera motion.

Present this with proposed narration changes and selective pauses as ONE edit
plan for David's approval before the first build. Analysis, timing measurements,
and previews needed to make that plan reviewable can proceed. Once approved,
execute the plan without asking again unless a material change becomes necessary.
Existing approval of the same treatment remains valid. The plan is a production
proposal, not a factor in the narration verdict or authorization to publish.

## 2. Every course board is the current page asset

Wherever the roll shows a lesson board, the candidate shows the exact current
JPG asset from `course-assets/<lesson>/` as referenced by `index.html`, never
Notebook's rendering of it, however close it looks. The replacement starts at
the source's own visual cut into the board and ends where narration leaves it
(sequential frame decode; never narration timing alone). A face-free upload
variant is never the shipped visual; the illustrated page board replaces it.
Use the existing JPG directly; do not recreate its HTML or reflow its text.
A temporary padded video canvas may fit the asset to 16:9 without changing the
canonical file. Recheck highlight coordinates when an asset changes. Current
assets, rather than superseded copies retained for old videos, govern new inserts.

## 3. Open at full view

Every board appears first as the complete, unmarked board, filling the frame
with the house side bars if its shape needs them. Hold that full view for at
least two seconds, or until the first item-level beat if that comes later.
Never open a board already zoomed or already ringed.

The full view comes from arriving early, not from a pause. A board arrives at
the start of the narration that introduces it ("This chart maps out…", "Sometimes
a teacher will allow…", "Say you snap a photo…"), replacing Notebook's stock
for that sentence, so the whole board is on screen while the narrator sets it up.
If a board has no spoken introduction and the narrator names the first card
inside two seconds, the ring pops at the first item's onset in the full view and
the dive waits; the board is still seen whole first. (Owner rule 2026-09-12: a
pause is never inserted between a board's introduction and its first item; the
earlier rule that did so is withdrawn.)

## 4. Compact or dense: decided by text, not structure

Every board has cards. The treatment depends on whether the text is legible in
the full view on the delivered 1280x720 frame.

- **Compact** (all card text reads comfortably at full view): stay at full
  frame for the whole span. Rings pop card to card at spoken onsets. At most a
  restrained whole-board push (4 percent, reached at 30 seconds, never more, and capped so every ring stays inside the frame with a margin). No dives, no pans.
- **Dense** (text needs zoom to read): full view first (rule 3), then dive to
  the complete active card at its spoken onset, pan smoothly to the next
  complete card as narration moves, and pull back to the full view for the
  takeaway or summary. One uniform dive window for all cards on a board.
  Never crop inside a card.

Judge legibility by looking at the full-view frame, not by counting cards.
Record the decision in the manifest (`density`). Calibration from David's calls
(2026-09-11, How AI Answers): the four-card Before the Answer Begins board and the
two prediction tables are dense; the two-card Why the Final Token Matters board and
the four-step strip under the Inference illustration are compact, because their
text reads at full view. AI Chat boards are always compact (Next Level Moves,
2026-09-11): never dive into a conversation; ring each speech bubble in turn at
full view, and the ring traces the bubble's own border, not the text inside it.

## 5. Rings: ours only

- Outline only, drawn after the camera crop at a constant 5 px, rounded
  corners. No fills, tints, chips, or Notebook washes anywhere in the candidate.
- One ring per point being made. A whole-card ring traces the card's outer
  boundary. On a board whose cards are columns inside one white content box
  (Why Hallucinations Happen, Check the Claim), the ring runs the full height of
  that white box, top edge to bottom edge, not the height of the text (owner
  rule 2026-09-21, Hallucination v10). Navy refrain boards (Traps Ahead, the
  creeds) ring each line in the creed gold `#f2cf5b`, tight to the text
  (owner rule 2026-09-21, Avoid Traps opener v6). A component ring inside a card sits at least 16 px inside the card,
  clear of dividers and arrows, sharing the card's rails when sections stack.
- Color comes from the card's locked accent token (green `#0f7a4a`, teal
  `#0e8f86`, blue `#1652f0`, editorial purple `#4f2fc4`, amber `#a9760c`, red
  `#c41f28`). Titles, whole-board points, and takeaway banners use `#6e51ff`.
  The banner ring traces the full gold banner edge to edge.
- Rings start at the spoken onset of their target and replace one another
  unless narration explicitly combines points. A board discussed only as a
  whole stays unmarked.
- Mechanism: use the unmarked canonical JPG, record complete component bounds
  in its image coordinates, and let `ken_burns_path.py` draw rings after cropping.
  For a temporary padded canvas, translate bounds by the exact placement offset.
  Never bake rings into the asset. Browser capture is only a fallback for a live
  component that has no canonical image; see the retrofit playbook.

## 6. Pauses: selective breathing room (owner rule, 2026-09-15)

This replaces the automatic one-second pause at every major idea boundary.
Review transitions by listening: add a pause only when the narration moves on
before a student has time to absorb the preceding point. Preserve transitions
that already feel natural. A new heading, section, or board is a place to review,
not an instruction to add silence.

A substantial conclusion, a demanding example, or a clear change of subject may
benefit from breathing room. Closely connected points usually do not. Do not
routinely pause between a board's introduction and its first item, between its
cards, or before its takeaway. Judge comprehension and flow, not box structure.

Before building, include proposed pause locations in the edit plan for David's
review. For each, give the source timestamp, a brief reason, the existing natural
gap, the proposed total gap, and how much time would be added. Account for the
natural gap already present; never automatically add a full second on top of it.
There is no universal one-second minimum. Once the plan is approved, execute it
without asking again unless the pause plan materially changes.

- Use matched room tone from the source with short crossfades, not digital zero.
  Preserve complete words and natural breaths.
- Hold the relevant preceding visual through the pause; begin the next visual
  with the next spoken idea.
- Measure edited pauses in the final encoded file with `silencedetect` and
  report their actual intervals against the approved plan. Listen through each
  transition to confirm it helps comprehension without dragging or creating an
  audible noise-floor cliff. State any listening that remains undone.

## 7. The standard close

Use the current canonical closing JPG referenced by the page. For a video canvas,
`make_close_board.py --lesson <lesson-id>` reads that asset through
`CLOSE_BOARD_ASSETS` and reads its matching closing copy from `CLOSE_BOARDS`; do not retype or
recreate the pill/sticky, change the white background, or alter its proportions.
The standard motion is a 48-frame hold, 150-frame push to 1.2x, and a settled hold
at 30fps. Longer narration adds hold time, not more zoom. Preserve compliant closes
in narrow repairs. Replace Notebook's close/outro in full production; the course
close is the literal final frame. The AI Brain Break activity is exempt.

## 8. Everything else stays Notebook

Outside the board spans, keep Notebook's graphics and motion. Do not replace an
engaging, accurate scene because a board exists. Do not invent course-style
boards for the video; a new replacement graphic is Notebook-style.

The engine burns a "Gemini Notebook" mark into the bottom-right corner of every
scene it renders (present on the September 4–9 rolls too; the audit of 2026-09-11
found it on seven of eight Build Your Skills videos). Owner decision 2026-09-11: it never ships, for
one reason: in a repaired video it blinks on at every cut back to Notebook and off
at every board, which reads as a glitch. Google makes the visible mark optional
(its help page: AI Pro and Ultra users can turn off "Visible watermarking" in the
Gemini Notebook profile menu; SynthID stays embedded regardless, and nothing in
Google's generative-AI terms requires the visible mark). David's account is Ultra
and the toggle is off, **but it does not take effect** (verified 2026-09-20: both
Fake Trap materials-test rolls carried the mark on every frame). So every roll is
assumed to carry the mark, and a marked roll is not a generation mistake. The
render loop in `editspec_build.py`
removes it on every kept Notebook frame (`gemini_mark.py`): paper cloned from the
same frame where the surround is paper, otherwise an inpaint of only the mark's
glyph strokes, using a mask learned from that roll's own paper frames. Frames it
declines are listed in the manifest and must be looked at. Board legs and the
close never carry it.

## 8b. Use Notebook's drawings to break up a board run (owner rule 2026-09-12)

A lesson whose boards would otherwise run back to back for minutes is less
engaging than one that breathes. Make Your Move v4 set the pattern: from the
first career board to the close, every board is interleaved with Notebook's own
drawings, and the narration and pauses did not change.

**When (owner call 2026-09-12):** apply this by default when a run of boards would
otherwise exceed about sixty seconds without a Notebook scene between them, and
never otherwise. A lesson with two boards and Notebook's own scenes between them
(Your Choices) is left alone. Every candidate's report states the longest
unbroken board run and lists every Notebook span used and where, so David can
pull any of it back before shipping.

- **Under a board's introduction.** Where Notebook drew a scene for the sentences
  that introduce a board, keep that scene and bring the board in about three
  seconds before its first item rings (the full-view rule still holds). Where the
  intro's own picture was a Notebook rendering of the board, re-time a Notebook
  drawing from elsewhere in the roll under it, typically one drawn for narration
  that was cut (`keep(..., video_from=<source frame>)`).
- **Inside a long board.** After an item's ring has held for a few seconds, cut to
  the drawing Notebook made for that item's narration, and return to the board
  about one second before the next item's title so the cut back lands on a
  still view, not on a moving dive. Do this only where Notebook drew something
  for that span; never invent a filler.
- **Never** a Notebook rendering of a course board, with or without its
  highlight, even for a second (rule 2). Check every in-time span against the
  roll's scene cuts: Notebook often cuts from a drawing back to its board render
  mid-sentence.
- **Between boards.** Keep Notebook's hand-off scenes (Curious & Flexible kept
  the Weekly AI Updates sketch rather than jumping board to board).
- Everything still passes rule 10: transition guard at every seam, corner mark
  cleaned on re-timed frames, and the audio untouched.

## 8c. Photographs never ship (owner rule 2026-09-13)

Notebook drops stock photographs into its rolls: people, machines, buildings,
old computers. None of them ship, whether or not a watermark is visible and
whether or not a person is in frame. Two earlier rolls surfaced Getty watermarks
mid-span, so the source and license of any Notebook photograph is unknowable
from the frames, and a public course video cannot carry that question.

Cover every photograph span with a drawing: Notebook's own drawing from
elsewhere in the roll (`keep(..., video_from=)`), a drawing from another roll or
the previous live video of the same lesson (`keep(..., video_from=, video_src=)`),
or, when nothing fits, a still from the roll's own next drawn scene. Match the
narration where a drawing exists for it: Why Learn AI v3 borrowed the live
video's Macintosh, gear-bolt-globe, and Winning the Race drawings under exactly
the lines they were drawn for. The candidate's report lists every photograph
replaced and what covers it. Course boards that contain the course's own
photographs (the career boards, the study boards) are page assets and are not
affected by this rule.

## 9. Audio outside the pauses is untouched

No narration is cut, moved, or grafted without David's approval of the exact
source words and timestamps. Approved grafts use coherent phrases from course
narration, level-matched, and are listed for listening.

**Best-of grafts (owner rule 2026-09-14).** When the review's best-of plan
names a beat that the alternate roll teaches better, the candidate carries that
beat as an audio graft from the alternate roll, by default under the course board
that beat belongs to: the board leg is sized to the grafted audio and its rings
follow the alternate roll's onsets. David's approval of the plan (quoted pairs,
timestamps, and selected roll) authorizes these grafts. The report lists every
graft with its output timestamps
for listening. A beat that would have to sit under Notebook's own drawing is
grafted only when the scene can carry it without an orphan beat; otherwise it is
reported as richer-but-not-grafted.

## 10. Before handing over

The review record (`video-audit/<slug>-repair-<date>/REVIEW.md`) states the scope,
source identities, changed spans, and whether it is a narrow repair or a full pass.
For a narrow repair, apply the checks below to the changed spans and affected joins;
report broader checks not performed and any known pre-existing defects. A full pass
also completes the whole-file ship checklist.

1. Decoded frame count equals the plan; each leg decodes its span exactly.
2. `transition_guard.py` passed every declared boundary, and the strips were
   inspected: the first frame after each boundary is already the destination.
3. Each edited pause measured against the approved selective-pause plan, with
   listening checks and any unverified transitions reported.
4. Every settled ring frame inspected at full resolution: right card, complete
   card inside the ring, nothing clipped, 5 px stroke at wide and dive cameras.
5. Every board's density decision and full-view open confirmed by frame.
6. What was not auditioned. Transcripts and correlations never certify audio;
   the joins David must listen to are listed with timestamps.
7. Anything left undone, with the reason. Live video and lesson unchanged.
