# Video-edit toolkit

Tools and recipes for repairing Gemini Notebook lesson videos — splice/composite is a
standing repair option, so a bad section no longer forces a re-roll. Every recipe
here shipped on real videos (learn-with-ai, what-you-can-control, does-ai-think,
how-an-llm-works, why-learn-ai, does-school-matter, the what-is-ai three-source
composite, and the Work With AI challenger round).

## Evaluation

`videos/video-rubric.csv` is the r4 authority and
`scripts/video/GRADER-r4.md` is the required procedure. The primary ship test is
non-compensable: a student must be able to watch the video instead of reading
the lesson and lose no essential understanding. Source coherence and teaching
accuracy are separate gates; neither can be offset by cleanliness or pacing.

The tracker keeps the r3 numeric columns because r4 does not change the /100
calculation. Run—or rerun—`scripts/video-tracker-migrate-r4.gs` to add any missing
Source QA, Accuracy Gate, Substitute Gate, and Board Walk Gate columns without
altering old reviews.

## The standard content-board walk (owner rule, 2026-08-14)

**Whenever narration walks two or more points on a compact lesson board, the exact
current lesson board stays fully visible for the entire walkthrough and the active
card or row is highlighted at its spoken onset.** Do not substitute an invented
graphic, redraw the board, crop into it, or pan between its points. If narration first
addresses the board as a whole, begin with the unmarked state. Highlights replace one
another unless the narration explicitly combines points.

The only exception is a board whose text is genuinely unreadable at 720p in whole-board
framing. In that case, a camera dive may frame the whole active card—never a crop inside
the card—and every state still comes from the same current app capture. Background
animation is expendable during a board walk; keeping the teaching framework visible is
the priority. This is enforced at ship review by `GATE_BOARD_WALK`. Build and verify the
replacement leg with `scripts/video/RETROFIT-PLAYBOOK.md`.

## The standard close (owner rule, 2026-08-04 — applies to EVERY video)

**Every video ends on the APP's close board, inserted in post with the standard
Ken Burns push-in. The engine's own rendering of the close is ALWAYS replaced,
even when it looks close.** Gemini Notebook approximates the CloseBoard
differently every roll, so an engine close is an inconsistency by definition;
the post insert is what makes the catalogue read as one course. **`welcome.mp4`
is the reference experience.** `critical-thinking.mp4` was the counterexample
that triggered this rule (engine redraw: red marker underline on the sticky,
off pill proportions, white canvas).

Quiz videos are exempt (owner, 2026-08-04: transformers-quiz keeps its
illustration ending). And when a pre-close board runs a settle-out right into
a dissolved-in close (engagement-trap), the standard close takes over the
WHOLE span from that board's arrival cut — one board, one push-in, no
dissolve stack at the end.

Wrong-format tells — any ONE means the close gets replaced:

- hand-drawn/marker strokes anywhere on the board (underlines, circles, arrows)
- pill or sticky proportions off the app render (engine pills drift wide/narrow)
- white/off-white canvas instead of the app page-background color
- fonts that aren't the app's (Plus Jakarta Sans pill, the sticky's italic)
- a dead-static freeze — the standard close MOVES: slow push-in, settled hold

How to do it — two shipped recipes, pick by situation:

- **CLOSE-BOARD REBUILD** (board exists in the app): capture `closeBoard()` at
  dsf4 and insert a ~5s single-beat full-frame push-in, buying timing with
  mirror-tiled room tone. Full recipe in the highlight-state bullet list below.
- **CLOSE-BOARD VARIANT** (compose the still from text): `make_close_board.py`
  renders the board in CloseBoard style; replace the frozen close span, zoom
  rate scaled to span length. Full recipe below under the Ken Burns section.

Prompt side: each video prompt still attaches a close board and requires the
narrator to speak both closing lines — that anchors the closing NARRATION
verbatim. But the engine's rendering of that board is expendable; the shipped
close visual always comes from this insert (see `Prompts/README.md`).

## Setup (once per machine)

```
bash scripts/video/env.sh
```

Builds `.video-venv/` (gitignored) with opencv + the imageio-ffmpeg wheel — the
wheel ships a full ffmpeg binary, no system ffmpeg needed — and self-tests `tpad`
(silently broken in some wheel builds: zero padding, no error; the scripts here
use the loop substitute regardless).

All Gemini Notebook mp4s are format-identical (h264 1280×720 30fps + AAC 44.1kHz mono),
so any splice needs exactly ONE re-encode pass:
`-c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 128k`.

## Tools

`PY=.video-venv/bin/python`

| Tool | Job |
|---|---|
| `ffmpeg.sh -i in.mp4 ...` | run the bundled ffmpeg (for hand-written graphs below) |
| `$PY frames.py in.mp4 outdir` | frame audit: quick pass (default), `--every N`, or `--sheet` contact sheets with red timestamps |
| `$PY scenes.py in.mp4` | scene cuts (frame-diff > 12 on 160×90 downscales); `--seam A B` prints per-frame diffs to catch leaked frames |
| `pauses.sh in.mp4` | narration pauses via silencedetect (-30dB, 0.25s) = safe audio cut points |
| `$PY freeze_finisher.py` | standard end repair: cut post-close junk, freeze the close board under trailing narration |
| `$PY add_close_motion.py` | standard-close enforcement: replace a frozen (or `--span-start` any) close span with the Ken Burns push-in, from the span's own frame or a `--board` render; verifies frames/audio/motion itself |
| `$PY graft_close_narration.py` | close-copy retrofit: swap the closing narration for a donor span (loudness-matched, trough-cut boundaries, mirror-tiled room tone) and rebuild the close as a board leg; duration may change. Donor spans with NO pause before/after the target words are the trap — the trough finder handles them, but always re-transcribe the tail (first batch leaked next-sentence syllables on 6 of 9) |
| `$PY patch_visual.py` | mid-video visual patch: freeze a good frame over a junk span, audio untouched, duration identical |
| `$PY excise_audio.py` | remove a stray spoken word from audio only (`--probe` RMS map first, then `--cut`) |
| `$PY graft_scene.py` | move a scene between videos: `--insert` (full graft, incl. replace-the-ending via `--resume-at` past the end) or `--replace-visual` (donor visuals over a base span, audio untouched, auto trim/freeze-fill) |

## Hard-won gotchas

- **cv2 `CAP_PROP_POS_MSEC` seeks return WRONG frames on these mp4s.** All mapping
  must be sequential decode (`cap.read()` loop). frames.py and scenes.py already
  comply — include this warning in every mapping-agent prompt.
- **Time-based `trim` can leak the boundary frame** (float compare let an exact
  frame-PTS end time through → 1-frame flash of the removed scene, caught by eye).
  Always cut seams with `trim=start_frame=A:end_frame=B` (end exclusive) and verify
  with `scenes.py --seam` — a clean freeze shows diff ≈ 0; any spike is a leak.
- **MKV legs carry a 1/1000 timebase — normalize BEFORE concat or the mux ships
  jittery video timestamps** (flattery-trap 2026-08-06: ms-rounded pts on every
  leg frame, audio perfectly uniform → players stalled the NARRATION at a
  different spot each play; frame count and audio MD5 were both clean, so the
  standard battery missed it). In any concat-filter assembly give EVERY input
  `settb=1/30004,setpts=N*1000` (frame duration = exactly 1000 ticks at 30.004
  fps) and mux with `-video_track_timescale 30004`. Verify with showinfo: the
  pts-delta histogram must be a single value; 33000/34000 mixtures are the bug.
- **`tpad` may be silently broken** in the wheel build (env.sh reports). Worse:
  the env.sh self-test can PASS while `tpad=stop_mode=clone` inside a concat
  graph still pads ZERO frames with no error (hit 2026-07-12 on the which-app
  burger patch — container duration looked right because audio carried it, but
  the video stream ran 4s short and desynced everything downstream; caught by
  counting decoded frames). Never trust tpad in a graph you haven't
  frame-counted. Working freeze substitute — loop the exact frame:
  `trim=start_frame=F:end_frame=F+1,setpts=PTS-STARTPTS,loop=loop=N-1:size=1:start=0,setpts=N/(30*TB)`
  then concat. The same trick replaces `tpad=start_mode=clone`.
- **Never `-c copy` concat FFV1 legs from different builders** (evaluate-the-results
  v6, 2026-08-04): ken_burns_path legs are bgr0, a zoompan-built leg is yuv420p —
  the concat DEMUXER joins them without error, then every frame after the junction
  decodes against the wrong stream parameters (full-frame macroblock garbage,
  caught by the owner in playback, not by frame counts or diff scans — the flicker
  even reads as plausible "transit motion" in a seam scan). Join mixed-builder
  legs through the concat FILTER (or feed them as separate inputs to the final
  graph) so pixel formats are negotiated; verify by EYEBALLING frames after the
  junction, never by count alone.
- **Never put `fps=30` after `loop`** — loop's cloned frames carry duplicate
  pts, and the fps filter silently DROPS every clone (same failure signature
  as broken tpad: container duration right, video stream short; hit 2026-07-24
  on the support-trap-v2 build, 322 frames gone, caught by frame count).
  Re-stamp with `settb=1/30,setpts=N/(30*TB)` directly after loop instead.
- **`-video_track_timescale` can silently eat the LAST frame** (ai-is-math v6,
  2026-08-08). A concat graph that measured 7,381 frames through `-f null -`
  muxed to 7,380 in the mp4 — every seam landed on its expected frame, so the
  loss was the tail, not a segment. Reproduced at timescale 15360, 30000 and
  90000; dropping the flag entirely gave 7,381. `-frames:v`, `apad`, `-shortest`
  and `-fps_mode passthrough` all failed to save it. **Diagnosis order that
  works: locate the seams first** (`scenes.py` on the output) — if they are all
  where you predicted, no segment is short and the frame went off the end, so
  stop auditing the filter and start removing output flags.
  You do not need the flag: without it these builds inherit a 1/1000000
  timebase whose `pts_time` deltas alternate 0.033333/0.033334, and **so do the
  source files** (ai-is-math-v3: 5140/2568; the shipped ai-is-math.mp4 is worse,
  with 166 frames at 0.033000). That microsecond alternation is NOT the
  flattery-trap bug — that one was millisecond rounding at 30.004 fps, a 1000×
  larger error. Compare the output's `pts_time` histogram against its own source
  before concluding anything about jitter.

## A cut count is NOT a strobe measure (learned the hard way, 2026-07-25)

`scenes.py` flags a frame whenever the 160x90 mean-abs-diff exceeds 12. On
content that pans slowly across high-contrast detail — handwritten numbers,
textured paper, dense boards — ordinary smooth motion clears 12 on *every*
frame, so a 7-second pan reports ~150 "cuts". Three spans were frozen on this
mistake and had to be reverted.

**These rolls are 24fps content in a 30fps container**, so the giveaway is a
repeating 5-frame cycle: four frames of real change, then one near-zero
duplicate.

Diagnose by DISTRIBUTION, never by count:

| | smooth motion misread | real strobe |
|---|---|---|
| diff magnitude | tight 12-20 band | 40-100+ |
| max diff | under ~25 | well over 40 |
| periodicity | regular ~0 dup every 5th frame | none |

```
# the check, before ever calling something a strobe
.video-venv/bin/python scripts/video/scenes.py in.mp4 --seam A B | head -20
```

**Measuring trap (hit twice on 2026-07-27):** `--seam` appends `  <-- SPIKE` to
any line over threshold, so `awk '{d=$NF}'` reads the word `SPIKE` as 0 and
every real spike silently counts as *no motion*. It reported "0 frames over 12"
and a "180-frame near-zero run" on a span that was in fact panning the whole
time. Always `sed 's/  <-- SPIKE//'` first, or take `$6`, before computing any
max / near-zero statistic.

Note too that a slow pan over **high-contrast line art** legitimately reaches
diffs of 25-30 — thick black strokes moving 2px change a lot of pixels. Judge it
by the shape of the curve (a smooth 6 → 13 → 25 → 30 → 25 → 18 → 6 ramp is an
ease-in/ease-out pan), not by the magnitude alone.
If max diff < 25 and you can see the every-fifth-frame duplicates, it is a pan
or a build. Leave it alone — and remember the current rubric does not score animation, so there
is nothing to win by freezing motion anyway.

## Recipes without a dedicated script (hand-written graphs via ffmpeg.sh)

**Cut-point discovery:** cut video at a scene cut (scenes.py) that falls inside a
narration pause (pauses.sh).

**START-CLONE** — destination board visible from the seam instant while its audio
starts earlier (fixes "board flashes in late"). Shipped example (why-learn-ai,
incumbent body + challenger close; use the loop substitute if tpad is broken):

```
ffmpeg -y -t 223.76 -i videos/why-learn-ai.mp4 -i Prompts/why-learn-ai-2.mp4 \
  -filter_complex "[1:v]trim=211.8:218.73,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=2.9[v1];[1:a]atrim=208.9:218.73,asetpts=PTS-STARTPTS[a1];[0:v][0:a][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 128k out.mp4
```

**MULTI-SOURCE CONCAT:** `-t`/`-ss` as INPUT options per source +
`filter_complex concat=n=N:v=1:a=1`.

**FREEZE-EXTEND** (too-short close: hold the last frame longer and pad audio with
silence via `apad`) — see which-app ship for the pattern.

**ILLUSTRATION INSERT (Ken Burns — the STANDARD for every still we add to a
video; owner call 2026-07-18, first shipped: ai-is-math Pascal & Fermat).** Drop
a lesson illustration over a span between two original scene cuts, audio
untouched, with a slow push-in so the still reads as a scene, not a freeze:

1. Pick the span: original scene cuts (scenes.py) bracketing the narration the
   illustration belongs to; both should sit inside narration pauses (pauses.sh).
2. Fit: our illustrations are 1200×800 vs the 1280×720 frame. NEVER crop-to-fill
   (clips headings/captions at the edges). Fit full-height, fill the side bars
   with a blurred darkened spill of the same image.
3. Ken Burns: zoom 1.00→1.08 across the span, anchored at y 40% (protects top
   headings; tune per image so no text leaves frame at full zoom). Upscale the
   composite 3× (lanczos) BEFORE zoompan or integer rounding makes it jitter.
4. Feed the jpg as a bare single-frame input and let zoompan mint the frames
   (`d=N:fps=30`) — a `-loop 1` image input runs at the demuxer's 25fps default
   and comes out short (bit us on the first ai-is-math build: 41 frames gone).

```
ffmpeg -y -i base.mp4 -i illo.jpg -filter_complex "
[1:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,boxblur=32:2,eq=brightness=-0.15[bg];
[1:v]scale=-2:720[fg];
[bg][fg]overlay=(W-w)/2:0[comp];
[comp]scale=3840:2160:flags=lanczos,zoompan=z='1+0.08*on/(N-1)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*0.40':d=N:s=1280x720:fps=30,format=yuv420p,setsar=1,settb=1/30,setpts=N/(30*TB),trim=start_frame=0:end_frame=N,setpts=PTS-STARTPTS[mid];
[0:v]trim=start_frame=0:end_frame=A,setpts=PTS-STARTPTS[pre];
[0:v]trim=start_frame=B,setpts=PTS-STARTPTS[post];
[pre][mid][post]concat=n=3:v=1:a=0[v]" \
  -map "[v]" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  -map 0:a -c:a copy out.mp4     # N = B - A frames
```

Verify: output frame count == input, `--seam` at both cuts (expect exactly two
spikes), mid-span per-frame diffs small and CONTINUOUS (~0.7–4.5 = smooth
motion; a 0.0 means the zoom didn't take, a spike means jitter), and eyeball
the LAST span frame for text still fully in frame at max zoom.

**SETTLE variant — run the zoom BACKWARDS on edge-to-edge dense illustrations**
(`z='1.06-0.06*on/(N-1)'`; first shipped: how-an-llm-works 2026-07-27). Fitting
full-height leaves side bars, so a push-in never clips left/right — the crop
always lands on the TOP and BOTTOM. On a dense infographic that means the title
and the bottom panel, and no y-anchor saves both at once. Settling out instead
puts the complete image on the LAST frame, which is the one that hands off to
the next scene. Same motion rate, and it reads as deliberate when the scene it
replaces was itself a push-in.

**MULTI-REGION PATH (`ken_burns_path.py`) — for a dense illustration whose
REGIONS answer successive narration beats** (first shipped: ai-is-different
2026-07-27, 31s of Getty-watermarked stock replaced by one illustration). The
single-region recipe above shows a still whole; this one tours it. The camera
crops 16:9 windows straight out of the image and glides between them, so the
frame is full-bleed the whole time — **no letterbox bars, because you never need
the entire image at once.** Beats are `(cx, cy, w)` in the image's own pixels;
height is derived from the output aspect, so windows stay 16:9 whatever shape
the source is.

1. Take the beat boundaries from the **original's own scene cuts** (scenes.py)
   where they already bracket the narration. Inheriting the roll's cut rhythm
   beats inventing one, and the region changes then land where the video always
   changed scene.
2. End each beat with a short **transit** (~24 frames) into the next region, so
   the camera ARRIVES as the narration reaches it. Without it, consecutive beats
   jump-cut between overlapping crops of one image, which reads as an editing
   error, not a cut.
3. Motion is smoothstepped per beat, so it settles at every narration boundary.
   Long beats with small moves go sub-pixel near the ends — check the near-zero
   run length, not just the max diff.
4. `--preview` writes every keyframe as a still. **Always eyeball those before
   rendering** — the failure mode is a window edge slicing through a heading
   ("AI Software" cut in half). Fix by moving the edge into a gap between rows.

**HIGHLIGHT-STATE VARIANT — N items on one board, each lighting up as it is
named** (first shipped: welcome five-step path, 2026-08-02). Capture the SAME
board N+1 times via CDP at deviceScaleFactor 4 (compose on a fixed wrapper,
inject per-state styles: 3px primary ring on the card + `#6e51ff22` chip behind
the label; export card rects for camera targets). Then run ken_burns_path ONCE
PER STATE, threading the camera across runs — each run's first beat carries an
explicit "from" equal to the previous run's final "to" — and concat the FFV1
legs with the concat demuxer (`-c copy`). Junction frames share the exact same
camera window, so the only change is the highlight popping on: reads as motion
graphics, not a cut (junction diffs land ~8-12, well under the cut threshold).
Time each junction to the narration onset of its item ("Step two is…") from
whisper word stamps, and put a ~30-frame transit + slow drift-hold inside each
state's run. Total leg frames must equal the replaced span exactly — plan the
per-run frame budget from the word stamps first.

Two extensions (what-is-ai, 2026-08-02):

- **ELEMENT STATES** — pass a states JSON as the script's 10th arg to highlight
  arbitrary sub-elements (chips, bubbles, list rows, single lines) per state:
  `{"states":[{"panels":["Label"],"elements":["exact textContent"]},...]}`.
  Elements get a 2.5px purple ring via box-shadow (zero layout shift, so pops
  are seam-free — junction diffs land 1-5), panels keep the card ring + chip.
  rects.json gains an "elements" map for camera targeting. One camera glide +
  many quick element states reads as the board lighting up as it is spoken.
  **Granularity rule (owner, 2026-08-02): one ring per point being made.** Use
  element states only when the narration walks sub-elements of the board; when
  each card/row IS the point (welcome's steps, why-learn-ai's rows), card-level
  highlighting is complete — finer rings add nothing.
- **BUY THE ZOOM-OUT** — when the pause before the exit cut is too short for a
  pullback (LLM board had 0.41s), INSERT 40-60 frames of room tone into the
  audio at the cut point and give the leg a pullback of the same length.
  Mirror-tile a clean ~0.35s pause for the tone (never anullsrc — room-tone
  cliff), 10ms fades at every joint. Works any time a board walk ends with no
  air; total video frames removed must equal audio seconds removed at fps.
- **OPEN FULL SCREEN (owner rule, what-you-can-control 2026-08-02):** every
  highlight tour STARTS on the whole board at full frame and only then zooms
  into sections. Early highlight states (e.g. two column intros) play at the
  wide framing with just the highlight switching; the first camera dive waits
  for the first item-level narration beat. A tour that opens pre-zoomed was
  rejected for exactly this.
- **COMPACT BOARDS GET NO DIVES (owner rule, learn-with-ai feed-in board,
  2026-08-02):** when every item on the board reads comfortably at the full
  view, camera dives are "actually distracting" — stay at the full framing the
  entire span (an imperceptible ~4%-per-30s push keeps it alive) and let the
  rings alone walk the narration. Judge by legibility at 720p, not by item
  count. Dives are for boards whose items need the zoom to be read.
- **Accent-colored boxes ring in their own accent, never the primary purple**
  (owner rule 2026-08-03, which-app big-three + how-we-built boards): when a
  card carries its own color (top border, colored label), pass panels as
  `{"label": "...", "ring": "#accent"}` in the states JSON — a purple ring on a
  green ChatGPT card was rejected. Element entries already took `ring`; panel
  entries now do too. Chips self-adopt the leaf's inline color as before.
- **Subgrid boards: capture ONE clean state, composite the rings in post**
  (which-app 2026-08-03). Cards that share row heights (`subgrid`) re-flow
  EVERY card when a chip pads one label, and the flex-centered band re-centers
  on top — a board-wide 2-3px text shift at every panel junction (read by the
  owner as "the image redraws / line wrap changes"). The chip now carries
  negative-margin compensation, but Chrome still drifts ~1px between repeated
  screenshots of a session, so DOM states can never be trusted pixel-stable:
  screenshot state-0 once, harvest rects (labels via a dummy element state),
  and draw card rings, element rings, and label-chip tints in post (cv2
  rounded rects at 4x). States are then identical-outside-the-highlight by
  construction — junction diffs land 1-3. Same idea as hallucination's
  rings-on-JPG composite.
- **Element rings are outline+offset, panel pills carry zIndex** (both in
  capture_board_states.js, owner-flagged 2026-08-02): a box-shadow element
  ring hugs the text box so glyphs touch the line, and a white panel pill can
  be painted over by the next sibling's background. Both fixed in the script —
  if a highlight ever renders crowded or half-hidden again, look there first.
- **Bullet-row rings enclose the dot (owner rule, evaluate-the-results
  2026-08-03): ring the ROW, not the inner text span.** When a list row is
  `[• span][content span]`, matching the content span's text rings the text
  alone and leaves the bullet outside the boundary — rejected. Match the row
  div by prefixing "•" to the concatenated text (rows whose bullet span has no
  text can't be targeted this way — the innermost-match rule picks the text
  span; those need the capture script if it ever matters).
- **Adjacent element rings that would overlap: ring the PARENT via its
  concatenated textContent** (ai-is-different acts-lines, 2026-08-02). Two
  stacked lines 6px apart each got an offset ring and the rings collided; the
  fix needs no script change — the element matcher takes exact textContent, and
  a container's textContent is its children's text concatenated with no
  separator ("Ask it twice: ...When it's wrong: ..."). One entry, one boundary.
- **When a lesson is prose-first, tour only what the lesson actually has**
  (ai-is-different, 2026-08-02): drawn engine scenes that visualize the page's
  PROSE are the video doing its job, not inconsistencies — do not invent app
  boards to replace them. The treatment applies only to spans rendering a real
  lesson component (there, one side-by-side board of eight scenes).
- **Capture preflight for the full-screen open:** before picking CANW/BANDW,
  check band aspect ≥ ~16:10 at the planned band width — a taller-than-wide
  board cannot fit a 16:9 window at any zoom, and a wide-flat board leaves no
  camera travel for dives. Tune BANDW (narrower = taller/more travel) together
  with CANW (wider canvas = room for the wide open); learn-with-ai's habits
  board needed 900-wide band on a 1360-wide canvas to get both.
- **Camera scope tracks the narration's referent** (owner, where-ai-works-best
  2026-08-03): when a line spans multiple cards ("In both of these cases…"),
  pull back far enough to show them — with a ring on each card named — rather
  than holding the last card's zoom. And the closing pullback waits for the
  words that actually widen the frame ("These *four* specific strengths…"); a
  wrap-up line that is still about the current card ("…synthesizes your
  constraints into a logical plan") keeps the card zoom and its ring.
- **2×2 grids: one uniform card window, sized to the gaps** (where-ai-works-best
  element retrofit, 2026-08-03): on a two-row grid the card window's top edge
  must clear the headline for TOP cards and land in the inter-row gap for BOTTOM
  cards — and the vertical space from headline-bottom to row-gap bounds the
  window height. A wider window that fits the rows alone will slice the other
  row's tagline. Solve once: pick the largest w whose 16:9 height fits between
  headline and row gap (there, w=3040 on a 6400×3600 dsf4 canvas, band 1000 on
  1600×900) and use it for all four cards — uniform zoom is also what reads as
  one camera.
- **CLOSE-BOARD REBUILD (same session):** when a roll's close is an engine
  redraw (marker strokes, off proportions), capture the app's closeBoard() at
  dsf4 (one state, `{"states":[{}]}`, LABELS = the sticky text) and replace the
  close span with a single-beat full-frame slow push-in (~5s). Buy the timing
  with mirror-tiled room tone on BOTH sides — ~1s before the close line (silent
  board pre-hold) and ~1s after (settled hold, 0.2s fade at the absolute end).
  Verify the insert by silencedetect: the pause must read as ONE continuous
  window, no blip at the joins.

**The source does not have to be an illustration — a frame of THIS VIDEO works**
(ai-is-different's second Getty span, replaced by a pan down the lesson's own
drawn spreadsheet grabbed from its static scene 90s later). Check the donor
scene is static first (`--seam`, mean diff under ~0.05) — then a still grab
loses nothing and you get to reframe. That reframing is the point: it crops out
the half of the donor you don't want (gibberish annotations, an unrelated phone
chat) and makes the reuse not read as a repeat. A 2x blow-up of a 640-wide
region of a 720p frame holds up fine on flat line art; it would not on a photo.

```
.video-venv/bin/python scripts/video/ken_burns_path.py spec.json --preview DIR
.video-venv/bin/python scripts/video/ken_burns_path.py spec.json leg.mkv   # lossless FFV1
ffmpeg -i base.mp4 -i leg.mkv -filter_complex \
  "[0:v]trim=start_frame=0:end_frame=A,setpts=PTS-STARTPTS[v1];
   [1:v]settb=1/30,setpts=N/(30*TB)[mid];
   [0:v]trim=start_frame=B,setpts=PTS-STARTPTS[v3];
   [v1][mid][v3]concat=n=3:v=1:a=0[v]" \
  -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a copy out.mp4
```

The FFV1 intermediate keeps the leg one lossy generation from the source, and
`-c:a copy` means the audio comes out **bit-identical** — verify it with
`-map 0:a -f md5 -` on both files, which is a stronger check than a waveform.

**CLOSE-BOARD VARIANT (the standard for composed closes; retrofit shipped
2026-07-18 across tokens, opener-understand, embeddings, does-school-matter,
how-ai-answers, one-more-thing).** Composed close stills used to render as a
small white card (pill ~39% of frame width); Gemini Notebook's native closes run the
pill at ~56% pushing to ~67% (measured on transformer). Recipe:

1. `make_close_board.py --lesson <sectionId> --bg <corner-sampled color of the
   existing close> --out board.png` — renders 3840×2160 in the app's CloseBoard
   style (Plus Jakarta Sans) and auto-sizes the pill toward 56% (short texts hit
   the font cap and land narrower, matching engine behavior).

   **Always pass `--lesson`, never hand-type `--pill`/`--sticky`.** Typing the
   copy is how SEVEN shipped closes ended up with straight apostrophes (') where
   the app renders curly ones (’) — why-learn-ai, ai-is-math, tokens, training,
   hallucination, flattery-trap, engagement-trap, caught 2026-08-07 by a
   catalogue-wide audit of every close whose copy contains an apostrophe. The
   flag reads pill+sticky verbatim out of `index.html`'s `CLOSE_BOARDS`, so the
   glyphs cannot drift from the page; the manual flags still exist for one-off
   boards and now warn when they see a straight apostrophe. Audit method, if it
   is ever needed again: grab the final frame, crop the apostrophe word, upscale
   ~8x with INTER_LANCZOS4 and look — a curly mark is comma-like and tapered, a
   straight one is a vertical tick.
2. Find the frozen close span (walk backward from the last frame while
   successive diffs < ~0.35) and replace exactly that span; audio untouched.
3. Zoom endpoint scales with span length to keep transformer's push rate:
   z_end = 1 + 0.2 × span_frames/210, capped at 1.2.
4. Board leg pts must be INTEGER ticks (`fps=30` + `setpts=N/(30*TB)`) —
   fractional per-frame pts get one frame dropped at concat (bit us twice).

Shell gotcha: this session shell is zsh — `$var:s=...` inside a filtergraph
string triggers zsh's `:s` history modifier and silently eats the graph up to
the next `=`; always write `${var}:s=...`.

## NotebookLM watermark removal (catalogue-wide, 2026-07-27)

**31 of 37 videos shipped with Google's NotebookLM corner mark burned in**, most
over 54-98% of their runtime. The six clean ones were the most recent rolls, so
the engine appears to have stopped adding it around late July. It is grey on
whatever it sits over, ~110px wide in a 1280px frame, bottom-right — small enough
that scrubbing does not reveal it.

```
$PY scripts/video/watermark_scan.py              # which videos, what % of runtime
$PY scripts/video/watermark_remove.py in.mp4 out.mp4 --auto
```

**Use the stroke mask, not `delogo`.** delogo interpolates inward from the box
border and discards everything inside. That is invisible on featureless paper
and wrong everywhere else — it smeared ai-is-math's chalkboard into vertical
bands and turned context-window's dot grid into stripes. `watermark_remove.py`
masks the logo's glyph pixels and inpaints only those, so background between and
around the glyphs survives.

Rejected, so nobody retries them: a fixed-offset clone patch (drags real content
in — the donor region carries chalk lines), and full alpha-inversion (the mark
IS alpha-blended, ~0.76 over a ~132 grey, but inversion leaves a readable ghost
because compression already destroyed the precision it needs). Also rejected: a
background-roughness triage meant to sort videos into delogo-safe and not. It
rated context-window flat, and delogo promptly striped it. **Roughness does not
predict the artefact; a regular pattern crossing the box does.**

### Three traps this pass fell into

- **Never derive the detector's reference from a file the pipeline edits.**
  watermark_scan.py originally extracted its template live from
  `videos/ai-is-math.mp4` frame 900. Repairing that video blanked the template,
  every video then scored 0 hits, `--auto` patched 0 frames, and the batch
  runner read "0 before -> 0 after" as a pass and installed re-encoded originals
  over good repairs. The template is now a committed `.npy`.
- **Guard the batch on a non-zero "before".** Every video in a repair list is
  known-defective, so a zero starting measurement means the detector broke, not
  that the video is clean. That one check catches the whole class.
- **Verify frame counts by DECODE, not `CAP_PROP_FRAME_COUNT`.** It reads
  container metadata and lies: what-you-can-control claims 5227 frames and
  decodes 5226, so a correct repair was rejected for losing a frame that never
  existed.

Verification per video is objective — decoded frame count identical, audio MD5
bit-identical (the stream is copied, never re-encoded), detector hits to zero.

## Composite workflow (multi-source best-of; first shipped: what-is-ai from 3 sources)

**Single-pass rule (training-bias ship, 2026-07-21):** when a build needs many
patches (training-bias took 7 visual patches + a close swap), build ONE
filter_complex concat graph from the pristine sources rather than chaining
patch passes — every leg stays one encode generation from the original, and a
late extra patch means re-running the graph with one more leg, not stacking a
second generation. 16 legs is fine.

**Profanity-in-gibberish rule (2026-07-21):** engine gibberish text can contain
real profanity — one roll batch shipped "fucking" in a highlighted opener
paragraph and a crude word in a phone chat mock-up, both graded "tolerated
pseudo-text" at first glance. During mapping, READ every legible or
semi-legible text span at full resolution; this is a course for 16-year-olds.


1. Parallel agents map EACH source: scene ranges + GOOD/TOLERATED/BAD flags, board
   map, silence list, sequential-decode-verified ending. Agent prompts must include
   the seek gotcha and: **white-on-light text = BAD, always** (an agent once graded
   it "GOOD (minor)"; David rejected the composite).
2. Plan seams on measured narration pauses.
3. One-pass concat re-encode.
4. Verify: waveform continuity + `scenes.py --seam` across each seam.
5. **David ear-tests every seam before ship** — waveforms are verifiable, audio
   content is not. Never skip this.

## Donor library

Every video in `videos/` plus every rejected challenger in `Prompts/` is a
potential scene donor for graft_scene.py. Rejected rolls often contain one great
scene (the close-graft pattern was born that way); `--replace-visual` harvests
them without touching the base narration. Pick all cut points at scene cuts
inside narration pauses, in both videos.

## Seam and grafting rules (owner preferences, learned the hard way)

- At a seam, land ON the destination board immediately — no transitional flash
  frames (a 1.5s bridge card was rejected; start-clone fixed it).
- Close grafts are the safe kind (one seam, nothing after it). Mid-video grafts
  across different rolls are the risky kind: topic hand-off both directions, style
  shift, possible voice/energy mismatch.
- Long content-bearing flaw spans (the white text IS the scene's meaning) cannot
  be clone-patched — graft or re-roll.
- **Dissolve-onset rule:** these rolls often dissolve between scenes (frame-diff
  never spikes). A donor/graft start taken from narration timing can land
  mid-blend and flash the PREVIOUS scene. Frame-check every donor onset past its
  dissolve before compositing.
- **Single-word splices: cut by phoneme profile, never by whisper stamps
  (what-you-can-control 2026-07-30):** whisper word boundaries ran ~200ms late
  around a stop consonant — its "skill" span actually held "[Develop]ing-sk",
  and splicing it produced a chirp/beep. Map the region in 5ms windows
  (fricative = dominant FFT bin >3.5kHz, voiced = <800Hz) and cut at the /s/
  onset and the next word's consonant onset. Watch for liaison: both narrators
  fuse word+"and" into continuous voicing, so the swappable unit was
  "scale and"→"skill and", not the word alone. Verify the landed splice by
  sliding cross-correlation AND by the output's phoneme shape — ASR cannot
  adjudicate a single spliced word (it re-hears it from phrase context).
- **Room-tone cliff + trailing sibilant (why-learn-ai 2026-07-30, three passes
  to get right):** never butt narration audio against digital-zero silence
  (anullsrc) — the noise-floor drop reads as a held-breath edit even when no
  content is clipped. Fade the tone out ~0.15s after speech, and fade the next
  leg's room tone back in. And whisper word-end times UNDERSHOOT trailing /s/:
  "once." marked ending 215.36 actually carried its sibilant 215.48-215.62
  after a ~100ms nasal dip — a cut in that dip turns "once" into "one". Cut
  after the sibilant (verify on the 5ms peak profile), never in the dip.
- **Word-inside-pause rule:** pauses.sh can flag a silence window that lives
  INSIDE a drawn-out word (a cut there clips mid-word). Verify every planned cut
  against word-level timestamps (faster-whisper, in the venv:
  `WhisperModel("base.en", device="cpu", compute_type="int8")` with
  `word_timestamps=True`), not pauses alone.
- **Orphan-beat rule:** carrying a sub-2s beat of never-before-seen material
  across a seam reads to the owner as "a flash of old content," even when the
  beat itself is clean. Land on the destination board instead (start-clone).
- **Word-mute recipe:** to delete one wrong spoken word without shifting sync,
  mute it in place: `volume=enable='between(t,A,B)':volume=0` on the audio leg,
  with A/B placed in RMS troughs (excise_audio.py --probe). Zero duration change.
- **Never overwrite a repair candidate in place** — the owner's player may have
  it open, and an underfoot rewrite plays as a broken file (frozen + silent).
  Version-suffix every rebuild (-v2, -v3, ...).
- **Breath-onset rule (questions-matter 2026-08-02):** when a cut deletes a
  sentence, the narrator's INHALE for that sentence starts inside the preceding
  pause — up to ~450ms before the whisper word onset. A cut placed after the
  breath onset ships a truncated inhale (the held-breath artifact with no
  anullsrc involved). Detect: silencedetect shows the planned pause SPLIT into
  two windows with a short energy blip ending exactly at your seam. Fix: move
  both A/V cuts before the blip. Confirming signal: whisper hallucinates a
  leading function word at the join ("Answers" heard as "Their answers") —
  re-transcribe after the fix and the phantom word disappears.
- **Deleting a mid-scene narration span (the sentence-cut recipe):** cut video
  and audio at the SAME frame-boundary timestamps, each end inside a measured
  silence, and check the re-entry frame for the source's own scene cuts —
  resuming 0.3s before one ships an orphan beat (found by a SECOND spike right
  after the seam in the output). If the source scene the audio resumes in
  started earlier than the audio cut allows, reconcile with a start-clone
  freeze of the destination's first settled frame (n_freeze = video span
  removed minus audio span removed).
- **EOF frame-count quirk:** an assembly can encode N frames (mux log says N)
  while BOTH cv2 and ffmpeg decode N-1. Before diagnosing, dump showinfo pts:
  if spacing is uniform 1/30 from 0, the loss is the terminal frame only —
  benign when the video ends on a freeze (hit twice, 2026-08-02). Any internal
  gap is a real drop: find it and rebuild.
- **zsh word-splitting trap:** `--seam $w` with `w="A B"` passes ONE argument
  in zsh (no implicit splitting) — argparse dies, stderr is easy to swallow in
  a pipe, and the check "passes" with empty output. Expand values literally or
  use explicit arrays; never loop measurement commands over unquoted vars.

## Highlight-state capture notes (see the variant recipe above)

- **Band disambiguation:** the innermost-div search can match a TRY IT quiz
  that reuses the board's item labels as options. Pass a HEADLINE string that
  exists only in the board (any unique body-text phrase works — questions-matter
  used "request for backup"); the quiz block fails the every-predicate filter.
- Whole-card solo states (ring moves card to card) measured junction pops of
  2.7-4.9 on the 160x90 diff — even gentler than welcome's 8-12. The pop can be
  small enough that a coarse threshold scan reports nothing; verify the junction
  by extracting the exact boundary frames, not by diff magnitude alone.
- The span being replaced does not need its own scene cuts at the junction
  times — only the OUTER edges must land on the original's cuts. Junctions are
  free to sit wherever the narration onsets are.
