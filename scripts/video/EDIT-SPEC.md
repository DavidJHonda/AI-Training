# Edit spec: scope and production standards

Updated 2026-09-29. [README](README.md) is the shared workflow and shipping
checklist; [Narration Review](NARRATION-REVIEW.md) owns teaching verdicts;
[Technical Recipes](TECHNICAL-RECIPES.md) holds implementation details.
This file owns build scope and board/audio treatment.

**Shipping is local by default (owner rule, 2026-09-29).** “Ship it” authorizes
installing, verifying, and committing the approved video locally. GitHub pushes
and Vercel deployment require a separate batch-publishing request. Follow the
[local shipping and batch deployment rules](README.md#local-shipping-and-batch-deployment-owner-rule-2026-09-29).

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
whole-file ship checklist before local shipping. Passing that checklist is separate
from the owner's authorization to ship locally or publish a batch.

## 1b. Review the board plan before the first build (owner rule, 2026-09-16)

Include a brief board-highlighting and camera plan with the video evaluation.
Inspect the current assets and follow the actual narration. Present one row per
board in scope, using its exact title; for a narrow repair, list only affected
boards and preserve previously approved treatment elsewhere.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| <exact title> | <whole card, then named sections as spoken; or whole card throughout; or unmarked> | <full board; or full view then complete-card zoom> | <planned seconds on screen; where it cuts away and to what (rule 8b)> | <brief reason, only where useful> |

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
- Identify engaging Notebook graphics/animations to retain, with source timestamps
  and the teaching purpose they serve. For each proposed visual repair or
  replacement, identify the specific problem and how the change improves teaching;
  separate content corrections, production-standard cleanup, and optional polish.

Present this with proposed narration changes and selective pauses as ONE edit
plan for David's approval before the first build. Analysis, timing measurements,
and previews needed to make that plan reviewable can proceed. Once approved,
execute the plan without asking again unless a material change becomes necessary.
Existing approval of the same treatment remains valid. The plan is a production
proposal, not a factor in the narration verdict or authorization to ship or publish.

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

This applies to actual recreations of course boards, not every Notebook diagram
or animation that teaches the same idea. Independent supporting scenes are judged
under rule 8 and can remain within a board's topic block (rule 8b).

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

## 5. Course-board rings: ours only

- Outline only, drawn after the camera crop, rounded corners. No fills, tints,
  chips, or Notebook washes on course boards. Supporting Notebook scenes may
  retain their own effective emphasis and animation under rule 8.
- **Stroke weight is a fixed on-screen width** (owner rule 2026-09-26): 6 px at
  1080p, which is 4 px in the 1280x720 delivery frame, whatever the camera's zoom
  on the board — full view, dive, or pan. `ken_burns_path.ring_px(out_h)` is the
  single source of truth. This replaces the 2026-09-21 rule (stroke scaled with the
  artwork, 5 px at a full-width 1600 px board) and the earlier constant 5 px. Videos
  shipped under either earlier rule are not rebuilt; apply this from the next build
  onward.
- One ring per point being made. A whole-card ring traces the card's outer
  boundary. Two card layouts, two rules (owner, 2026-09-21): when the cards are
  columns inside one shared white box (Why Hallucinations Happen, Check the
  Claim), the ring runs the full height of that white box, top edge to bottom
  edge, never just the text (Hallucination v10); when the cards are separate
  rounded white cards on the stage (How Skewed Data Distorts the Picture, Three
  Questions That Reveal Bias, How RAG Works), the ring hugs that card's own
  measured edges on all four sides (Training Bias v6). Measure the card's own
  edges, not the stage colour: separate cards cast a soft drop shadow (4–8 px
  at the sides, ~14 px below) that a "not stage colour" test swallows, which
  floated every Training Bias v5 ring a shadow's width outside its card. Take
  the illustration tile's x extent and top for the card's left, right, and top,
  and the last near-white row above the shadow for its bottom. Do not reuse
  another board's rects. Navy refrain boards (Traps Ahead, the
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

## 8. Preserve engaging Notebook graphics and animations (owner rule 2026-09-29)

**Choose visuals for their teaching value.** Keep engaging Gemini Notebook
graphics and animations when they support the narrated point and do not contradict
the lesson. An animation may explain a process, relationship, or change more
effectively than an inserted still. Preserve its useful motion, sequence, and
timing; do not flatten it or replace it merely because we can create a cleaner
graphic, a course board exists, or its example is absent from the lesson text.

Added examples and visual analogies are acceptable when they make the lesson
clearer, remain consistent with its meaning and qualifiers, and do not introduce
misleading claims. Illustrative numbers and charts can express a lesson's point
without being sourced statistics. Do not reject them solely because the values
are unsupported; judge their role and meaning in the narrated scene. Distinguish
that use from a consequential factual claim or a false attribution to a source.
Clarify an example as illustrative only when needed for understanding.

Owner calibration (2026-09-29, Why Learn AI? Version 2): retain the animated
capability chart at 0:44–0:49 and cumulative project/experience chart at 1:46–1:51,
including their numbers. They express improvement and learning through projects;
the owner approved both as effective illustrations. No numerical cleanup or added
disclaimer is required for these spans. This does not approve every numerical
claim elsewhere; assess each in its teaching context.

Review the scene in motion with its narration, including revealed labels, arrows,
numbers, and the final state. Ask what the student will understand from it. If it
teaches the intended point accurately and engagingly, retain it. A still frame
alone cannot establish whether an animation works; disclose any unviewed motion.

When a scene has a specific problem, prefer the smallest effective repair that
preserves its teaching value: correct a label, remove a misleading number, or
retime a reveal before replacing the whole scene. Replace it when it contradicts
or misleads, obscures the point, distracts, or fails an applicable production
standard. Identify that reason separately from optional aesthetic preferences.
Use rule 8d when an existing scene cannot serve the teaching need effectively.

Actual course-board recreations still receive the canonical asset and treatment
(rules 2–5); independent supporting graphics are not board recreations merely
because they explain the same point. Keep useful scenes around and within board
topic blocks under rule 8b. Do not invent course-style boards for the video; a new
supporting image follows the owner’s photographic preference in rule 8d. The
Notebook stock-photo and mark cleanup rules still apply.

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

## 8b. Use supporting drawings to break up a board run (owner rule 2026-09-12)

A lesson whose boards would otherwise run back to back for minutes is less
engaging than one that breathes. Make Your Move v4 set the pattern: from the
first career board to the close, every board is interleaved with Notebook's own
drawings, and the narration and pauses did not change.

**When (owner call 2026-09-12, widened 2026-09-23):** apply this by default when a
run of boards would otherwise exceed about sixty seconds without a Notebook scene
between them, and, from 2026-09-23, whenever a single board would sit on screen
for more than about twenty seconds. David's note after the Where's the Line? pre-roll
review: the weakness in many shipped videos is boards held too long; a board plus
Notebook's drawings under the same narration engages, a board alone does not. The
hold is fixed here, in the edit plan, never at upload: the 2026-09-23 A/B on Where's
the Line? showed that removing the board images from the upload does not shorten
Notebook's holds (it holds its own diagram for the same topic block) and costs the
narration (1/7 required lines against 7/7). A lesson with short boards and Notebook's
own scenes between them is left alone. (Your Choices was the old example; its two
50-second board runs were broken with donor drawings from two rerolls, 2026-09-26.) The 1b board plan states each
board's planned on-screen time and where it breaks; every candidate's report states
the longest unbroken board run and lists every supporting illustration used and where, so David
can pull any of it back before shipping.

**Where the pictures come from (2026-09-23):** first the roll's own drawings (for
that beat, or re-timed from a beat whose narration was cut); then drawings from
OTHER ROLLS of the same lesson, used as `keep(..., video_src=<roll>, video_from=...,
video_end=...)` (Where's the Line? v2: a roulette table and a betting phone from two
other rolls under the base roll's invented-statistics slides, a keyboard drawing from
a third under a drawn person); then the live video's own drawings when a reroll
replaces it (Layers v3: the live animation under the scale beat). Donor drawings
carry the same bans as the roll's own (no photographs or photorealistic imagery,
logos, misleading numerical claims, recreated course boards;
illustrated, cartoon, and stylized people are allowed, owner rule 2026-09-26).
Independent examples and animations explaining a board's idea are allowed under
rule 8; matching the topic does not make a scene a recreated board.
When available drawings are weak, repetitive, misleading, or missing, propose a
custom supporting illustration under rule 8d. If no relevant illustration is
planned, say so in the report and let the dense dive-and-pan carry the board;
do not invent decorative filler.

- **Under a board's introduction.** Where Notebook drew a scene for the sentences
  that introduce a board, keep that scene and bring the board in about three
  seconds before its first item rings (the full-view rule still holds). Where the
  intro's own picture was a Notebook rendering of the board, re-time a Notebook
  drawing from elsewhere in the roll under it, typically one drawn for narration
  that was cut (`keep(..., video_from=<source frame>)`).
- **Inside a long board.** After an item's ring has held for a few seconds, cut to
  the drawing Notebook made for that item's narration, and return to the board
  about one second before the next item's title so the cut back lands on a
  still view, not on a moving dive. Use a relevant existing drawing or a custom
  illustration included in the approved edit plan under rule 8d; never invent filler.
- **Never** a Notebook rendering of a course board, with or without its
  highlight, even for a second (rule 2). Check every in-time span against the
  roll's scene cuts: Notebook often cuts from a drawing back to its board render
  mid-sentence.
- **Between boards.** Keep Notebook's hand-off scenes (Curious & Flexible kept
  the Weekly AI Updates sketch rather than jumping board to board).
- Everything still passes rule 10: transition guard at every seam, corner mark
  cleaned on re-timed frames, and the audio untouched.

## 8c. Notebook stock photographs never ship (owner rule 2026-09-13)

Notebook drops stock photographs into its rolls: people, machines, buildings,
old computers. None of them ship, whether or not a watermark is visible and
whether or not a person is in frame. Two earlier rolls surfaced Getty watermarks
mid-span, so the source and license of any Notebook photograph is unknowable
from the frames, and a public course video cannot carry that question.

Notebook people rule (owner rule 2026-09-26): "No photos or photorealistic imagery. Illustrated, cartoon, and stylized people are allowed." A drawn,
cartoon, or stylized person in a Notebook scene ships; a photographed or
photorealistic one from Notebook never does. Every Notebook video prompt carries
that sentence verbatim. The owner’s 2026-09-29 preference for newly generated
supporting images is different: realistic high school students, under rule 8d.
That preference does not authorize unknown-source Notebook stock photographs.

Cover every Notebook photograph span with a suitable supporting image: its own drawing from
elsewhere in the roll (`keep(..., video_from=)`), a drawing from another roll or
the previous live video of the same lesson (`keep(..., video_from=, video_src=)`),
or a custom supporting illustration under rule 8d. A still from the roll's own
next drawn scene may also fit. Match the
narration where a drawing exists for it: Why Learn AI v3 borrowed the live
video's Macintosh, gear-bolt-globe, and Winning the Race drawings under exactly
the lines they were drawn for. The candidate's report lists every photograph
replaced and what covers it. Course boards that contain the course's own
photographs (the career boards, the study boards) are page assets and are not
affected by this rule.

## 8d. Custom supporting illustrations (owner rule 2026-09-29)

When Notebook graphics are weak, repetitive, misleading, or missing, propose a
purpose-built illustration that supports the specific narrated idea. First apply
rule 8: preserve effective Notebook graphics and animations, and consider a
targeted repair before a replacement. State the teaching benefit of the new
illustration; visual consistency or polish alone is not a reason to replace an
effective animation. Use canonical assets for actual course boards (rule 2).

**Style for graphics we create (owner direction 2026-09-29):**

- **People and settings:** use realistic, photographic-looking high-school-age
  students with natural proportions, expressions, and poses in believable school,
  home, or study settings. Avoid cartoon, anime, exaggerated features, and a
  childish illustration style. Use realistic objects for accompanying scene inserts.
- **Course fit:** take current course imagery as the visual reference for maturity,
  color, lighting, and level of realism. Keep related custom scenes visually
  consistent. Do not default to a sketchbook or cartoon style merely because the
  surrounding Notebook scenes are drawn.
- **Clothing:** ordinary student clothing is appropriate. Video-only supporting
  images do not need Dallas Stars jerseys or the exact characters used on lesson
  pages. Actual course boards still use their canonical assets.
- **Show the intended action:** the picture must make the narrated idea clear.
  For “make something real with AI,” show a student using AI to create a usable
  result, with the AI interaction and resulting work visible. Drawing or crafting
  by hand alone does not communicate that point. Choose the scene for what it
  teaches, not just an attractive person at a laptop.
- **Explanatory graphics:** use clear diagrams, charts, or process visuals when
  those explain the idea better. They need not contain a person or imitate a
  photograph. Keep them readable at the final video size, with minimal text.

Purpose-generated photographic-looking assets are allowed; rule 8c still excludes
unknown-source Notebook photographs. Preserve effective existing Notebook drawings
and animations under rule 8. This style rule governs new custom graphics and is
not a reason to replace useful existing motion.

Keep text minimal, and avoid misleading numerical
claims or diagram relationships. Illustrative values follow rule 8. Each new graphic should help explain
that moment, not merely decorate the break.

Include the illustration's purpose and placement in the edit plan (rule 1b),
reusing approval already given for the same work. Preserve approved narration
and timing for visual-only replacements. Inspect the final encoded result for
accuracy, readability, cropping, and transitions; the source illustration alone
is not sufficient verification. Retain the final asset and its generation/edit
prompts with the build record, and list its output span in the review.

Layers v9 is the reference example: replace repeated stack imagery with a long
number row showing the two tracked values, then a separate illustration of “it”
through successive updates. Both pictures support their narrated beats while
the approved audio and duration stay unchanged. Custom illustrations supplement
the canonical boards; they do not replace or restate them as newly designed boards.

## 9. Narration changes and targeted repairs

Outside approved pauses and narration repairs, audio is untouched. Narration
cuts, moves, and grafts follow the approved scope and edit plan: identify exact
source/replacement words, files, and timestamps. Reuse approval already given
for the same repair; do not ask again. Approved grafts use coherent course
narration from existing video rolls, level-matched and listed for listening.

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
