# Technical recipes for video editing

Implementation reference, separated from the shared workflow on 2026-09-15.
Read only the relevant section. [README](README.md) owns the workflow,
[Edit Spec](EDIT-SPEC.md) owns scope/treatment, and
[Board Retrofit](RETROFIT-PLAYBOOK.md) owns the current JPG-based board procedure.

Dated examples below explain specific past failures. Their file paths, frame
numbers, sizes, and command parameters are examples, not current asset inventories
or permission to edit/publish. Inspect the current scripts and source properties
before adapting a recipe. Use source hashes and an explicit candidate output path.
Existing boards are canonical JPGs; do not regenerate them from historical HTML.

## Setup (once per machine)

```
bash scripts/video/env.sh
```

Builds `.video-venv/` (gitignored) with opencv + the imageio-ffmpeg wheel — the
wheel ships a full ffmpeg binary, no system ffmpeg needed — and self-tests `tpad`
(silently broken in some wheel builds: zero padding, no error; the scripts here
use the loop substitute regardless).

The common delivery format is H.264 1280×720 at 30fps with AAC audio; inspect
actual inputs rather than assuming every roll is identical. Re-encode video once
per assembly. Copy audio for visual-only work; use AAC encoding only for approved
audio changes. A typical video encode is
`-c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p`.

## Tools

`PY=.video-venv/bin/python`

| Tool | Job |
|---|---|
| `ffmpeg.sh -i in.mp4 ...` | run the bundled ffmpeg (for hand-written graphs below) |
| `$PY frames.py in.mp4 outdir` | frame audit: quick pass (default), `--every N`, or `--sheet` contact sheets with red timestamps |
| `$PY scenes.py in.mp4` | scene cuts (frame-diff > 12 on 160×90 downscales); `--seam A B` prints per-frame diffs to catch leaked frames |
| `pauses.sh in.mp4` | candidate narration gaps via silencedetect (-30dB, 0.25s); verify word boundaries before cutting |
| `$PY freeze_finisher.py` | standard end repair: cut post-close junk, freeze the close board under trailing narration |
| `$PY add_close_motion.py` | standard-close enforcement: replace a frozen (or `--span-start` any) close span with the Ken Burns push-in, from the span's own frame or a `--board` render; verifies frames/audio/motion itself |
| `$PY graft_close_narration.py` | close-copy retrofit: swap the closing narration for a donor span (loudness-matched, trough-cut boundaries, mirror-tiled room tone) and rebuild the close as a board leg; duration may change. Donor spans with NO pause before/after the target words are the trap — the trough finder handles them, but always re-transcribe the tail (first batch leaked next-sentence syllables on 6 of 9) |
| `$PY patch_visual.py` | mid-video visual patch: freeze a good frame over a junk span, audio untouched, duration identical |
| `$PY excise_audio.py` | remove a stray spoken word from audio only (`--probe` RMS map first, then `--cut`) |
| `$PY graft_scene.py` | move a scene between videos: `--insert` (full graft, incl. replace-the-ending via `--resume-at` past the end) or `--replace-visual` (donor visuals over a base span, audio untouched, auto trim/freeze-fill) |
| `$PY splice_integrity.py` | compare a visual repair with its pristine source; enforce frames/FPS/audio, detect residual source-frame islands, and render every-frame boundary strips |
| `$PY transition_guard.py` | audit output-timeline splice frames after any hybrid/audio-changing edit; fail on 1-6-frame intermediate visuals and render mandatory every-frame strips |
| `$PY audio_gap_review.py` | build contextual WAV clips for manual KEEP / ATTENUATE / ROOM_TONE decisions; never edits the source |
| `$PY replace_audio_with_room_tone.py` | replace a confirmed blip or stray syllable with equal-duration nearby room tone; video stream is copied and verified bit-identical |
| `$PY make_standard_close_plan.py` | build the fixed standard close move: 48-frame full-board hold, 150-frame push to 1.2x, then a same-size settle for the remaining narration |

## Hard-won gotchas

- **A visual-only retrofit must not ship `editspec_build`'s audio (2026-09-16, Training v3→v4):** `Build.keep()`
  crossfades 5 ms of room tone at BOTH ends of every timeline row, and a board retrofit splits rows at the
  board cuts, which land mid-sentence. Training's row edge at source 7212 sat inside the word "packaged"
  and measured a 14,000-sample dip against the live track. When the audio is supposed to be untouched,
  render with the framework, then remux: `-c:v copy` the candidate's video and supply the live track's
  decoded PCM (plus any approved tail from `edited.wav`) as the audio; encode AAC once. Verify with a
  sample-level diff against the live track (Training v4: corr 0.99999, no 10 ms window above codec noise).
- **Never borrow drawings from `course-assets/<lesson>/<lesson>.mp4` (2026-09-14, Why Learn AI v4):** `keep(..., video_src=)`
  frame numbers are tied to one specific file. The live filename changes contents at every ship, so a
  build that borrowed from "the live video" on 2026-09-13 borrowed from v3 itself a day later and put the
  Winning the Race drawing under the steam-engine narration. Use a stable, explicitly selected source for the active edit, record its hash,
  assert it exists at the top of the build, and list it in `protected`. If an old
  tracked version is needed, recover that specific version from Git into a temporary
  working directory. Do not recreate `archive/` or retain old donor copies after
  the authorized cleanup. Use current lesson boards for new board inserts.

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
ffmpeg -y -t 223.76 -i course-assets/why-learn-ai/why-learn-ai.mp4 -i Prompts/why-learn-ai-2.mp4 \
  -filter_complex "[1:v]trim=211.8:218.73,setpts=PTS-STARTPTS,tpad=start_mode=clone:start_duration=2.9[v1];[1:a]atrim=208.9:218.73,asetpts=PTS-STARTPTS[a1];[0:v][0:a][v1][a1]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 128k out.mp4
```

**MULTI-SOURCE CONCAT:** `-t`/`-ss` as INPUT options per source +
`filter_complex concat=n=N:v=1:a=1`.

**FREEZE-EXTEND** — extend the last frame only within the approved timing plan.
If audio needs extending, use matched room tone rather than digital-zero padding.

**ILLUSTRATION INSERT (historical recipe for non-board stills; course boards
follow Edit Spec; owner call 2026-07-18, first shipped: ai-is-math Pascal & Fermat).** Drop
a lesson illustration over a span between two original scene cuts, audio
untouched, with a slow push-in so the still reads as a scene, not a freeze:

1. Pick the span: original scene cuts (scenes.py) bracketing the narration the
   illustration belongs to; both should sit inside narration pauses (pauses.sh).
2. Fit: this example used a 1200×800 illustration in a 1280×720 frame. NEVER crop-to-fill
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
frame is full-bleed the whole time — **no letterbox bars in this historical non-board example.**
Course boards still require the full-view opening and complete-card framing in Edit Spec. Beats are `(cx, cy, w)` in the image's own pixels;
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

**Course-board highlights:** use the canonical JPG and post-crop 5px rings in
[Board Retrofit](RETROFIT-PLAYBOOK.md). Retired multi-state DOM captures, fixed
902px wrappers, heading fills, and width changes are not the current method.
Do not insert audio pauses to buy camera-motion time. Fit the move to the approved
narration timing; selective teaching pauses are governed by Edit Spec section 6.

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

**Standard close:** use the canonical JPG through
`make_close_board.py --lesson <lesson-id> --out <temporary-canvas.png>` and the
fixed motion in Edit Spec section 7. Do not sample a stale video's background or
recreate the text. Preserve the current white-background asset and its composition.

Shell gotcha: use `${var}:s=...`, not `$var:s=...`, in zsh filtergraph strings.

## NotebookLM watermark removal (catalogue-wide, 2026-07-27)

Historical July detector notes follow. They do not describe current engine behavior.
For current builds, use the engine-mark handling in Edit Spec section 8 and inspect
all declined frames. These older detector commands are troubleshooting references,
not a substitute for checking the actual candidate.

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
  `course-assets/ai-is-math/ai-is-math.mp4` frame 900. Repairing that video blanked the template,
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


1. Map EACH source: scene ranges + GOOD/TOLERATED/BAD flags, board
   map, silence list, sequential-decode-verified ending. Mapping notes must include
   the seek gotcha and: **white-on-light text = BAD, always** (an agent once graded
   it "GOOD (minor)"; David rejected the composite).
2. Plan seams on measured narration pauses.
3. One-pass concat re-encode.
4. Verify: waveform continuity + `scenes.py --seam` across each seam.
5. Listen to each seam and record what was heard. List joins still requiring
   David's listening review; waveform checks alone do not verify audio quality.

## Donor library

During an active edit, a selected stable snapshot of a current video or retained source in `Prompts/` may supply a useful scene for graft_scene.py. Record its hash; do not bind frame numbers to a live file that shipping may overwrite. Do not keep rejected rolls as a permanent donor library. `--replace-visual` reuses a scene without changing the base narration. Pick all cut points at scene cuts inside narration pauses in both videos.

## Seam and grafting rules (owner preferences, learned the hard way)

- **Visual-cut boundary rule (owner, 2026-09-01): never set a replacement
  boundary from narration timing alone.** Narration determines which visual
  belongs; the source video's exact visual transition determines the splice
  frame. Whisper timestamps, spoken sentence endings, and second-based seeks
  can land several frames before or after the source edit and leave a brief
  flash of old content. Locate the visual transition by sequential frame
  decoding, then cover every frame of the outdated graphic through the first
  frame of the next approved shot. When the transition is ambiguous, extend
  the replacement a few safe frames rather than expose an orphan beat. Record
  all splice boundaries as integer frame numbers, not decimal seconds.
  Mandatory handoff QA: inspect the final replaced frame and the first restored
  frame individually at full resolution, plus a short frame sequence on both
  sides. The first restored frame must already be the approved destination
  shot; zero frames from the superseded graphic may remain.
- At a seam, land ON the destination board immediately — no transitional flash
  frames (a 1.5s bridge card was rejected; start-clone fixed it).
- Close grafts are the safe kind (one seam, nothing after it). Mid-video grafts
  across different rolls are the risky kind: topic hand-off both directions, style
  shift, possible voice/energy mismatch.
  **Board-anchored grafts are the safe mid-video kind (2026-09-14):** under a
  course board the picture is ours, so a whole beat from the alternate roll can
  replace the base roll's beat with only two audio seams at silences; match
  levels (loudnorm or speech-RMS, both rolls within ~1 dB after gain) and let the
  leg's rings follow the grafted roll's onsets.
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
- **Measured-pause rule (updated 2026-09-15):** pause placement is selective,
  governed by the approved edit plan and EDIT-SPEC section 6, not an automatic
  one-second requirement. Count the existing natural gap toward the planned total
  gap. An edited teaching pause is an audio change, not merely a visual hold. Hold
  the preceding idea onscreen until the next narration idea begins. Measure the
  final encoded interval with `silencedetect`, report it against the plan, and
  listen to the transition for natural pacing. Use clean matched room tone and
  preserve complete words and natural breaths; remove an inhale only when it
  belongs to approved deleted narration. No audible noise-floor cliffs.
- **Word-inside-pause rule:** pauses.sh can flag a silence window that lives
  INSIDE a drawn-out word (a cut there clips mid-word). Verify every planned cut
  against word-level timestamps (faster-whisper, in the venv:
  `WhisperModel("base.en", device="cpu", compute_type="int8")` with
  `word_timestamps=True`), not pauses alone.
- **Orphan-beat rule:** carrying a sub-2s beat of never-before-seen material
  across a seam reads to the owner as "a flash of old content," even when the
  beat itself is clean. Land on the destination board instead (start-clone).
- **Historical word-mute diagnostic (not an approved narration-repair plan):**
  to test removing a stray sound without shifting sync,
  mute it in place: `volume=enable='between(t,A,B)':volume=0` on the audio leg,
  with A/B placed in RMS troughs (excise_audio.py --probe). Zero duration change.
  For production, use approved coherent narration edits and matched room tone;
  deleting a wrong word alone may leave incomplete or misleading teaching.
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

## Browser-capture fallback notes

These apply only to a live component without a canonical JPG. Existing image
boards use the geometry procedure in the retrofit playbook, not DOM text matching.

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
