# Work With AI — live video review, 2026-09-26: board holds and ring stroke

Scope: the nine live videos of the Work With AI section (`LESSON_VIDEOS` in `index.html`,
files under `course-assets/<slug>/<slug>.mp4`), checked for two things only, at David's
request: (1) boards held on screen too long (Edit Spec 8b: any single board over ~20 s
needs a planned break; any board run over ~60 s without a Notebook scene), and (2) the
highlight-ring stroke rule (Edit Spec 5, owner rule 2026-09-26: a fixed on-screen width,
6 px at 1080p = 4 px in the 1280x720 delivery, at any zoom). Not a narration review; no
video was changed. Nothing here is an edit plan or an authorization to build.

Measurement: `board_spans.py` (ORB match against each lesson's JPGs every 0.5 s) for holds;
`ring_stroke.py` (new, `scripts/video/`, documented in the README) for stroke — it thresholds
the eight Edit Spec colour tokens, keeps hollow rectangles, and takes the median run length
across the four sides every 0.5 s. Calibration: What Is AI? (20260926ship2, the first video
built under the fixed rule) reads 4.0 solid px on every ring. Narration under each hold from
faster-whisper base.en word timestamps (`_transcripts/`). Raw rolls: none survive in
`Prompts/` for any of the nine lessons (12 rolls there, none for this section), so the only
donor drawings available for hold-breaking are each live video's own Notebook scenes.

## Headline

- **Holds: 26 of the 43 content-board spans in the section run longer than 20 s.** Only the
  opener is clean (longest 19.5 s). Where AI Works Best and Evaluate the Results are boards
  almost end to end: 150 s and 214 s of back-to-back boards with no Notebook scene between.
  The single longest hold is Your Home Base's Big Three board at 68.5 s.
- **Rings: none of the nine videos carries the fixed stroke.** Every span built on 2026-09-16
  and 09-17 measures 6 to 7 solid px on screen (the old "constant 5 px" setting). The spans
  re-synced on 2026-09-21 measure 4 px at full view but 6 to 7 px on dives (the artwork-scaled
  rule), so three videos now mix widths inside one board (Evaluate the Results, Critical
  Thinking, Context Window). Only Questions Matter's re-synced first minute reads 4 px throughout.
- **Tool finding:** OpenCV draws only odd line widths. `draw_ring` with thickness 4 renders a
  5 px line (4 solid after encode, which is what the reference reads); thickness 5 renders 7 px.
  So the shipped "4 px" rule is really 5 px at 720p (about 7.5 px at 1080p), and the old "5 px"
  rule was really 7 px. The ratio the eye sees between old and new videos is 7:5, not 5:4. A
  true 4 px needs a different drawing method (filled outer minus inner rounded rectangle).

## A. Board holds

Per video (content boards only; the standard close is excluded from the counts):

| Video (ship key) | Runtime | Boards on screen | Notebook scenes | Holds > 20 s | Longest single | Longest back-to-back run |
|---|---|---|---|---|---|---|
| Work With AI opener (20260921ship14) | 2:37.9 | 86 s (54%) | 72 s | 0 of 6 | Refrain 19.5 s | 21.0 s (Same Tool > Section Map) |
| AI Is Different (20260921ship15) | 5:22.5 | 183 s (57%) | 139 s | 4 of 6 | Rules vs Patterns 46.5 s | 53.0 s (Rules vs Patterns > Structured) |
| Where AI Works Best (20260916ship1) | 4:20.1 | 205 s (79%) | 56 s | 5 of 5 | Built This Course 42.0 s | **150.0 s** (Reshape > Explore > Find > Problems, 1:01–3:31) |
| Your Home Base (20260921ship16) | 3:58.9 | 134 s (56%) | 105 s | 2 of 3 | **Big Three 68.5 s** | 68.5 s (Big Three alone) |
| Questions Matter (20260921ship17) | 3:42.9 | 129 s (58%) | 94 s | 2 of 6 | Answers Faster 56.0 s | 78.5 s (Answers Faster > Value Lives, 0:08–1:26) |
| Art of Prompting (20260916ship1) | 4:00.3 | 96 s (40%) | 144 s | 1 of 5 | Good Question 28.0 s | 28.0 s |
| Context Window (20260921ship6) | 4:25.5 | 180 s (68%) | 85 s | 4 of 4 | Head Start 58.0 s | 58.0 s (Head Start alone; 2.5 s gap then Outside 43.5 s) |
| Evaluate the Results (20260921ship18) | 4:16.9 | 214 s (83%) | 43 s | 5 of 5 | Dig 50.0 s | **214.4 s** (Quick Pass > Decide > Dig > Move > Check > close, 0:42.5 to the last frame) |
| Critical Thinking (20260921ship19) | 3:17.8 | 130 s (66%) | 68 s | 3 of 3 | Five Habits 53.5 s | 53.5 s |

Every hold over 20 s, with the narration under it (first words … last words; lead-in is
board arrival relative to the first word, tail is silence after the last word before the
board leaves). In every case the narration walks the board's own content; none of these
is a board left up past its beat. The problem is length, exactly as David described on
2026-09-23: a board alone for 40 to 70 s, with no Notebook drawing between its items.

| Video | Board | On screen | Length | Narration under it |
|---|---|---|---|---|
| AI Is Different | Rules | 0:28.5–0:55.0 | 26.5 s | "flowchart shows exactly what those rules look like…" … "same result every single time." |
| AI Is Different | Learn Once | 1:02.0–1:37.5 | 35.5 s | "infographic illustrates the new process…" … "the word after that." |
| AI Is Different | Rules vs Patterns | 2:11.0–2:57.5 | 46.5 s | "Let's ask a computer to recommend the best game…" … "construct a fresh response every time." (re-synced 09-21, rings 4 px) |
| AI Is Different | Weak Spots | 4:11.0–4:53.0 | 42.0 s | "graphic outlines severe risks from this lack of control…" … "lock down than a simple written rule." |
| Where AI Works Best | Built This Course | 0:12.0–0:54.0 | 42.0 s | "We saw this distinction clearly when building this very…" … "human judgment to shape the result." (unmarked, no rings) |
| Where AI Works Best | Reshape | 1:01.0–1:36.5 | 35.5 s | "Let's look at this graphic detailing our first strength…" … "translate dense technical jargon into plain language." |
| Where AI Works Best | Explore | 1:36.5–2:11.0 | 34.5 s | "Our second strength, as outlined in this next graphic…" … "a list of ideas for a fundraiser." |
| Where AI Works Best | Find | 2:11.0–2:51.5 | 40.5 s | "The third core strength is finding what matters…" … "different articles treat the exact same topic." |
| Where AI Works Best | Problems | 2:51.5–3:31.0 | 39.5 s | "Our fourth and final strength is working through problems…" … "science experiment gave you unexpected results." |
| Your Home Base | Big Three | 1:13.0–2:21.5 | 68.5 s | "This board breaks down the big three side by side…" … "do the job for most tasks." |
| Your Home Base | How We Used | 3:05.0–3:48.5 | 43.5 s | "how this looks in practice, multiple AI apps actually…" … "lesson videos with Gemini Notebook." |
| Questions Matter | Answers Faster | 0:08.0–1:04.0 | 56.0 s | "For decades, technology has steadily reduced the friction…" … "just changes where our value lives." (re-synced 09-21, rings 4 px; David's call: "highlighting but no zooming") |
| Questions Matter | Value Lives | 1:04.0–1:26.5 | 22.5 s | "Before AI, the sheer work of locating a good…" … "Answers got cheap. Questions didn't." |
| Art of Prompting | Good Question | 0:27.0–0:55.0 | 28.0 s | "question is always the foundation. Prompting adds the instructions…" … "use a specific framework of instructions, packaging" |
| Context Window | Same Question | 0:11.0–0:57.5 | 46.5 s | "Consider this scenario. Two different people ask AI the…" … "context, AI gives better answers." |
| Context Window | Five Sources | 1:21.0–1:42.5 | 21.5 s | "This illustration shows the five specific sources that feed…" … "saved memory, and specific projects." |
| Context Window | Head Start | 1:49.0–2:47.0 | 58.0 s | "Because we know exactly where the AI looks for…" … "time you ask a question." (dense: dive and pan) |
| Context Window | Outside the Window | 2:49.5–3:33.0 | 43.5 s | "also need to clearly outline what does not automatically…" … "context window, the model can't see it." (dense) |
| Evaluate the Results | Quick Pass | 0:42.5–1:29.0 | 46.5 s | "This is the quick pass. It is the mandatory…" … "Read, understand, and validate." |
| Evaluate the Results | Decide | 1:29.0–2:11.5 | 42.5 s | "you complete the quick pass, you move to this…" … "the answer the attention it deserves." |
| Evaluate the Results | Dig | 2:11.5–3:01.5 | 50.0 s | "When an answer does require a closer look, you…" … "are the final arbiter of reality." |
| Evaluate the Results | Move | 3:01.5–3:38.5 | 37.0 s | "After your evaluation is complete, you reach the final…" … "responsibility for the final product." |
| Evaluate the Results | Check Before Use | 3:38.5–4:06.0 | 27.5 s | "Let's apply this to a high-stakes scenario. Imagine…" … "is merely a claim that requires proof." (re-synced 09-21) |
| Critical Thinking | Equation | 0:00.0–0:47.5 | 47.5 s | Frame 0 is the board: "This graphic lays out a basic equation for how…" … "a claim to hold up." (no Notebook open; the video starts on a course board) |
| Critical Thinking | Two Reactions | 0:57.0–1:17.5 | 20.5 s | "One front page ran the headline slim by chocolate…" … "what you want to believe." (re-synced 09-21) |
| Critical Thinking | Five Habits | 2:08.0–3:01.5 | 53.5 s | "board outlines five habits you can build to sharpen…" … "especially critical when you use artificial intelligence." |

Short low-confidence detector hits (1.5–4 s at 31–54 inliers: opener 0:22.5 and 0:39.5,
Where AI Works Best 4:02 and 4:05.5, Art of Prompting 0:15, Evaluate 0:00.5, AI Is Different
3:35) were frame-checked (`_frames/sheet.jpg`): all are Notebook's own drawings, not
renderings of course boards. No rule-2 issue.

Donor material for breaks, per video (Notebook seconds in the live file, since no raw rolls
exist): Art of Prompting 144 s, AI Is Different 139 s, Your Home Base 105 s, Questions Matter
94 s, Context Window 85 s, opener 72 s, Critical Thinking 68 s, Where AI Works Best 56 s,
Evaluate the Results 43 s. Whether any of those drawings fit the beats inside the long boards
is a per-lesson job (Edit Spec 8b: never invent filler; when nothing fits, the dense
dive-and-pan carries the board). Where AI Works Best and Evaluate the Results have the least
to work with and the longest runs; the honest options there are re-timing their few drawings,
or a reroll to get fresh drawings (the kit workflow of `Prompts/README.md`).

## B. Ring stroke

Stroke = solid on-screen pixels at the tool's threshold (true width about +0.5 for the
anti-aliased edge). Reference: What Is AI? 20260926ship2 = 4.0 on 127 of 127 ring samples.
Gold detections other than the opener's navy-refrain rings are banner fills or Notebook
drawings and are excluded; so are detections under 3 px.

| Video | Ring samples | at 4 px | at 5 px | at 6–7 px | Where the widths sit | Rule era |
|---|---|---|---|---|---|---|
| Work With AI opener | 79 | 0% | 0% | 100% | Refrain gold 0:06–0:19 6 px; Section Map rings 1:05–2:26 6–7 px | 09-16 build (constant 5 → draws 7) |
| AI Is Different | 291 | 35% | 3% | 62% | Rules + Learn Once 0:32–1:37 6–7 px; **re-synced 2:12–3:23 at 4 px** (5 px on the 2:14–2:17 zoom); Weak Spots 4:15–4:52 6–7 px | mixed 09-16 / 09-21 |
| Where AI Works Best | 254 | 0% | 0% | 100% | every ring 1:06–3:30 at 6–7 px | 09-16 build |
| Your Home Base | 158 | 0% | 0% | 100% | Big Three 1:16–2:09 and How We Used 3:23–3:48 at 6–7 px (09-21 sync span has no rings) | 09-16 build |
| Questions Matter | 192 | 46% | 0% | 54% | **re-synced 0:19–1:03 at 4 px throughout**; every later ring 1:04–3:23 at 6–7 px | mixed 09-16 / 09-21 |
| Art of Prompting | 110 | 0% | 0% | 100% | every ring 0:29–2:59 at 6–7 px | 09-16 build |
| Context Window | 301 | 61% | 11% | 23% (+5% at 8+) | full-view rings 4 px (0:17–0:57, 1:56–2:27, 2:43–2:54); Head Start teal 2:28–2:42 5 px; **Outside the Window dives 2:55–3:29 at 6–7 px** (column rings at 7, section rings at 7.8) | 09-21 build, artwork-scaled rule (thickens on dives by design of that rule) |
| Evaluate the Results | 346 | 4% | 0% | 96% | every card ring 0:49–3:58 at 6–7 px, including the re-synced 3:42–3:58 cards; only the re-synced banner 3:59–4:05 at 4 px | mixed; the sync's own manifest says "5 px at the dive, 3 px for the banner" |
| Critical Thinking | 198 | 6% | 1% | 93% | Equation 0:12–0:47 and Five Habits 2:15–3:01 at 6–7 px; re-synced Two Reactions cards 1:00–1:11 at 6–7 px, its banner 1:12–1:17 at 4 px | mixed; sync manifest: "5 px at the dives, 4 px at full view" |

Reading: the section is at one of two widths everywhere, 7 px drawn (reads 6–7) or 5 px
drawn (reads 4), never the same width across a video, and in three videos not even across
one board (Evaluate's Check Before Use: cards at 7, banner at 4; Critical Thinking's Two
Reactions: cards at 7, banner at 4; Context Window's Outside the Window: 4 at full view,
7 on the dive). Teal and green read 7 where blue, purple, and violet read 6 in the same
build; the pixel profile shows the same 6 solid + 1 partial for both, so that is the
threshold, not a real difference.

Why the widths are what they are (`draw_ring` test, `cv2.line` with and without LINE_AA,
then x264 crf 18 yuv420p as the build uses): thickness 1 → 1 px, 2 → 3 px, 3 and 4 → 5 px,
5 and 6 → 7 px. Even thicknesses round up to the next odd. So `ring_px(720) = 4` draws a 5 px
line (encode leaves 4 solid + 1 blended, the reference's 4.0), and the old constant 5 drew
7 px (6 solid + 1 blended, the 6–7 readings). Consequences:
1. The 2026-09-26 rule as implemented is 5 px at 720p, about 7.5 px at 1080p, not 6 px.
2. It cannot be tuned to 4 px through the thickness argument (3 gives the same 5).
3. Old and new differ by 7:5, which is the visible weight jump David saw on What Is AI.
If David wants the literal 6 px at 1080p (4 px at 720p), `draw_ring` needs to render the ring
as a filled outer rounded rectangle minus a filled inner one (exact even widths), or draw at
the 3x upscale the render already keeps and downsample. That is a tooling change to
`ken_burns_path.py`, separate from any video rebuild, and it would shift every video built
since 09-26 (What Is AI?, Your Choices cutaways, Build Your Skills opener v5) by 1 px too.

## C. What this means for the section

1. No Work With AI video meets either current rule. Every one of the nine would need a
   rebuild to get the fixed stroke; seven of nine need hold-breaking as well (the opener needs
   neither on holds; Art of Prompting has one 28 s hold).
2. The rings are a mechanical rebuild: the same ring rects re-rendered at the fixed stroke
   over the same audio (visual-only retrofit, remux the live PCM per TECHNICAL-RECIPES). The
   build scripts for the 09-21 syncs exist; the 09-16 builds' scripts are in `scripts/video/`
   (`build_where_ai_works_best_v3.py`, `build_questions_matter_v5.py`, etc.), but each was a
   full assembly from raw rolls that no longer exist, so a ring-only rebuild has to work from
   the live file's own frames (one more encode generation, disclosed).
3. The holds need per-lesson plans (Edit Spec 1b tables with an "On screen / breaks" column),
   each approved before a build. Priority by severity: Evaluate the Results (214 s run, 43 s
   of drawings to break it with), Where AI Works Best (150 s run, 56 s of drawings), Your Home
   Base (68.5 s single hold), Context Window (58 s + 46.5 s + 43.5 s), Critical Thinking
   (53.5 s + 47.5 s, and it opens on a board), Questions Matter (56 s), AI Is Different (four
   holds of 26–46 s, 139 s of drawings available), Art of Prompting (one 28 s hold).
4. Two spec lines are stale against the 09-26 rule and still say the old number: README ship
   checklist "constant 5px outline rings" and Edit Spec 10.4 "5 px stroke at wide and dive
   cameras". Not changed here; flagged for David.

Files: `<slug>/board-spans.txt|json`, `<slug>/ring-stroke.txt|json`, `<slug>/crops/`
(4x crops of the thinnest and thickest ring found), `_calib/what-is-ai/` (reference),
`_transcripts/` (word timestamps), `_frames/sheet.jpg` (false-positive check),
`_frames/ring-crops.jpg` (6x ring crops used for the eye-check), `_hold_narration.py`.
Live videos and the lesson page unchanged.

## D. Narration review (added later on 2026-09-26, David's request)

All nine live files reviewed under `NARRATION-REVIEW.md` from the live page, the upload
Markdown, the prompt/kit, and the full word-level transcript (transcript only; no audio heard,
each block lists what an ear check must still cover). Per-lesson blocks: `<slug>/NARRATION.md`.
Section CSVs: `narration-review-summary.csv` (one row per video) and
`narration-review-points.csv` (567 rows: every teaching point, hard requirement, error,
addition, source-QA line, and editing note, with timestamps and the words actually spoken).

| Video | Verdict | Points (R/T/Th/M/W) | Hard reqs | What decides it |
|---|---|---|---|---|
| Work With AI opener | REROLL | 14 (2/9/2/1/0) | 11/20 | Refrain paraphrased, never read; camera line replaced; takeaway paraphrased; "capabilities"; no donor words in file |
| AI Is Different | REROLL | 35 (11/15/5/4/0) | 12/18 | Formal rewrite: superpowers hook, the catch, right-tool takeaway, Superman comparison, "own Kryptonite", no-one-can-predict never spoken; Board 4 never walked |
| Where AI Works Best | REROLL | 36 (7/24/1/4/0) | 28/32 | All four strength takeaway lines never spoken; prompt never listed them as verbatim (materials fix first) |
| Your Home Base | KEEP | 18 (13/5/0/0/0) | 18/18 | Complete; formal-word drift only |
| Questions Matter | KEEP | 30 (21/8/1/0/0) | 25/25 | Complete; one non-essential setup hook unspoken |
| Art of Prompting | REPAIR | 34 (22/12/0/0/0) | 17/18 | "framework" spoken twice; both whole sentences cuttable (0:49.14–0:54.06, 3:20.84–3:23.86) |
| Context Window | KEEP | 30 (23/6/1/0/0) | 22/22 | Complete; distrust-vs-strength paragraph THIN (shipped that way 9/21 on David's call) |
| Evaluate the Results | REROLL | 30 (10/20/0/0/0) | 12/17 | Content complete but "How much is riding on it?", three of five dig names, and the Dig takeaway never spoken; "capabilities" |
| Critical Thinking | REPAIR | 28 (19/7/2/0/0) | 16/17 | Habit 3 cut mid-word at 2:37.12 ("alternative ex…"); donor "alternative explanations" at 0:28.66 in the same file, under the Five Habits board |

Section: 3 KEEP, 2 REPAIR, 4 REROLL. Source QA PASS on all nine. Zero WRONG points anywhere.
