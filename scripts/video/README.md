# Video-edit toolkit

Tools and recipes for repairing NotebookLM lesson videos — splice/composite is a
standing repair option, so a bad section no longer forces a re-roll. Every recipe
here shipped on real videos (learn-with-ai, what-you-can-control, does-ai-think,
how-an-llm-works, why-learn-ai, does-school-matter, the what-is-ai three-source
composite, and the Work With AI challenger round).

## Setup (once per machine)

```
bash scripts/video/env.sh
```

Builds `.video-venv/` (gitignored) with opencv + the imageio-ffmpeg wheel — the
wheel ships a full ffmpeg binary, no system ffmpeg needed — and self-tests `tpad`
(silently broken in some wheel builds: zero padding, no error; the scripts here
use the loop substitute regardless).

All NotebookLM mp4s are format-identical (h264 1280×720 30fps + AAC 44.1kHz mono),
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
- **`tpad` may be silently broken** in the wheel build (env.sh reports). Worse:
  the env.sh self-test can PASS while `tpad=stop_mode=clone` inside a concat
  graph still pads ZERO frames with no error (hit 2026-07-12 on the which-app
  burger patch — container duration looked right because audio carried it, but
  the video stream ran 4s short and desynced everything downstream; caught by
  counting decoded frames). Never trust tpad in a graph you haven't
  frame-counted. Working freeze substitute — loop the exact frame:
  `trim=start_frame=F:end_frame=F+1,setpts=PTS-STARTPTS,loop=loop=N-1:size=1:start=0,setpts=N/(30*TB)`
  then concat. The same trick replaces `tpad=start_mode=clone`.

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

**CLOSE-BOARD VARIANT (the standard for composed closes; retrofit shipped
2026-07-18 across tokens, opener-understand, embeddings, does-school-matter,
how-ai-answers, one-more-thing).** Composed close stills used to render as a
small white card (pill ~39% of frame width); NotebookLM's native closes run the
pill at ~56% pushing to ~67% (measured on transformer). Recipe:

1. `make_close_board.py --pill "..." --sticky "..." --bg <corner-sampled color
   of the existing close> --out board.png` — renders 3840×2160 in the app's
   CloseBoard style (Plus Jakarta Sans) and auto-sizes the pill toward 56%
   (short texts hit the font cap and land narrower, matching engine behavior).
2. Find the frozen close span (walk backward from the last frame while
   successive diffs < ~0.35) and replace exactly that span; audio untouched.
3. Zoom endpoint scales with span length to keep transformer's push rate:
   z_end = 1 + 0.2 × span_frames/210, capped at 1.2.
4. Board leg pts must be INTEGER ticks (`fps=30` + `setpts=N/(30*TB)`) —
   fractional per-frame pts get one frame dropped at concat (bit us twice).

Shell gotcha: this session shell is zsh — `$var:s=...` inside a filtergraph
string triggers zsh's `:s` history modifier and silently eats the graph up to
the next `=`; always write `${var}:s=...`.

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
