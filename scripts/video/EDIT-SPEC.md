# Edit spec: what every repair candidate must contain (owner rules, 2026-09-11)

Read this before building any candidate. It is the contract for a finished edit;
`README.md` holds the recipes and tooling, `NARRATION-REVIEW.md` judges the
narration, and the ship checklist in `README.md` is the final verification.
When these disagree, this file wins for build scope and board treatment.

## 1. Scope: a candidate is a complete edit

A repair request names what prompted the build ("the inference board and the
pauses"). The build still applies every rule below to the whole video: every
course board, every idea boundary, the close. Never hand over a candidate with
one board fixed and the others left as Gemini Notebook rendered them. If a rule
cannot be met, say so in the review record; do not silently narrow the scope.

"Every board" means every board complies, not every board is rebuilt. Boards that
already shipped under this spec stay as they are when a later build only touches
audio or another span. What is never allowed is a Notebook rendering or a
Notebook highlight on any board in the candidate.

## 2. Every course board is the current page asset

Wherever the roll shows a lesson board, the candidate shows the exact current
asset from `illustrations/` or `lessons/` as referenced by `index.html`, never
Notebook's rendering of it, however close it looks. The replacement starts at
the source's own visual cut into the board and ends where narration leaves it
(sequential frame decode; never narration timing alone). A face-free upload
variant is never the shipped visual; the illustrated page board replaces it.

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
  boundary. A component ring inside a card sits at least 16 px inside the card,
  clear of dividers and arrows, sharing the card's rails when sections stack.
- Color comes from the card's locked accent token (green `#0f7a4a`, teal
  `#0e8f86`, blue `#1652f0`, editorial purple `#4f2fc4`, amber `#a9760c`, red
  `#c41f28`). Titles, whole-board points, and takeaway banners use `#6e51ff`.
  The banner ring traces the full gold banner edge to edge.
- Rings start at the spoken onset of their target and replace one another
  unless narration explicitly combines points. A board discussed only as a
  whole stays unmarked.
- Mechanism: capture once, unmarked (`RECTS_ONLY=1`), and let
  `ken_burns_path.py` draw rings from the rectangles. Never bake rings into a
  capture.

## 6. Pauses: one second between ideas

Gemini Notebook runs ideas together. Insert one second of matched room tone at
each boundary between distinct ideas. Not after every sentence.

Judge the boundary from the lesson's structure, not from the Markdown's board
blocks (owner rule 2026-09-12): a pause belongs where the page starts a new
section or a new idea (a new heading, the hook giving way to the teaching, the
move from one board's subject to the next, the move into the summary, before the
closing lines). Inside a board there are no pauses: not between its introduction
and its first item, not between items, not before its takeaway banner. Those are
parts of one box, and the narrator's own breath is enough. When in doubt, the
question is "is a different idea starting here?", not "is a different part of the
board starting here?".

- Tone is mirror-tiled from the roll's own pause, seeded at the median level of
  the source's pauses, with short crossfades. Never digital zero.
- The current visual holds through the pause; the next visual begins with the
  next spoken idea.
- Measure each pause in the final encoded file with `silencedetect`; the quiet
  interval must be at least one second.

## 7. The standard close

Every video ends on the app close board inserted in post: copy taken
programmatically from `CLOSE_BOARDS` (`make_close_board.py --lesson`), 48-frame
hold, 150-frame push to 1.2x, settled hold. Notebook's close and outro are
always removed. The close board is the literal last frame.

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
Google's generative-AI terms requires the visible mark). David's account is Ultra,
so: **turn Visible watermarking off before generating**; new rolls arrive clean.
For rolls that already carry the mark, the render loop in `editspec_build.py`
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

## 9. Audio outside the pauses is untouched

No narration is cut, moved, or grafted without David's approval of the exact
source words and timestamps. Approved grafts use coherent phrases from course
narration, level-matched, and are listed for listening.

## 10. Before handing over

The review record (`video-audit/<slug>-repair-<date>/REVIEW.md`) states:

1. Decoded frame count equals the plan; each leg decodes its span exactly.
2. `transition_guard.py` passed every declared boundary, and the strips were
   inspected: the first frame after each boundary is already the destination.
3. Every pause measured in the final file.
4. Every settled ring frame inspected at full resolution: right card, complete
   card inside the ring, nothing clipped, 5 px stroke at wide and dive cameras.
5. Every board's density decision and full-view open confirmed by frame.
6. What was not auditioned. Transcripts and correlations never certify audio;
   the joins David must listen to are listed with timestamps.
7. Anything left undone, with the reason. Live video and lesson unchanged.
