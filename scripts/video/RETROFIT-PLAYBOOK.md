# Board-retrofit playbook (v2 builds, 2026-08-07)

You are building `videos/<slug>-v2.mp4`: replacing off-format board spans in a shipped
lesson video with legs built from CURRENT page captures, using the app's highlight
system. HARD RULES: never modify the shipped `videos/<slug>.mp4`; never run git
commands; narration/audio is untouchable (stream-copied). The house highlight system
is thin purple rings + tinted label chips popping at narration onsets — NEVER
reproduce the engine's yellow washes, marker circles, underlines, orange arrows or
corner brackets in any form.

Run everything from the repository root; do not change directories inside a compound
command because that breaks the relative `.video-venv/...` paths. Python:
`.video-venv/bin/python` (has cv2, faster_whisper, imageio_ffmpeg). ffmpeg:
`bash scripts/video/ffmpeg.sh ...`.
Shell is zsh: `for x in "a b"` does NOT word-split; write args explicitly.

## Canonical content-board walk (mandatory)

Use this treatment whenever narration walks two or more points on a current lesson
board that remains legible in whole-board framing:

- Replace the complete narrated board span, including its board-level introduction,
  with the exact current app capture. Never use an engine recreation or a recomposed
  approximation when the lesson board exists.
- Hold the whole board in fixed framing throughout. Start unmarked when narration
  addresses the board as a whole, then show exactly one active card or row at each
  spoken onset. Highlights replace one another; they accumulate only when narration
  explicitly combines or compares points.
- No camera dive, crop, zoom, or pan between items. Background animation is not a
  reason to leave the board: the board is the teaching scene while it is being walked.
- Exception: if text is genuinely unreadable at 720p in whole-board framing, a dive
  may frame the whole active card. Never crop inside a card, and return to the same
  board rather than introducing a substitute visual.
- End the board span only when narration moves to the next teaching beat. Static time
  while narration is explaining the board is intentional teaching, not dead time.

## 1. Map the spans
- Scene cuts: `.video-venv/bin/python scripts/video/scenes.py videos/<slug>.mp4`
  (frame + seconds per cut). Replace spans ON THE ORIGINAL'S OWN CUTS.
- Word stamps for each board-walk window:
  ```python
  from faster_whisper import WhisperModel
  m = WhisperModel("base.en", device="cpu", compute_type="int8")
  segs, _ = m.transcribe("videos/<slug>.mp4", word_timestamps=True)
  # print w.start, w.end, w.word for words inside your windows
  ```
  Junction frames = word-onset × 30, rounded.

## 2. Capture boards from the CURRENT page
Start your own server+chrome on YOUR assigned ports (never 8768/9338), from the
repository root:
```
python3 -m http.server PORT --bind 127.0.0.1 &
PROFILE=$(mktemp -d -t chromeprof)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --disable-gpu --user-data-dir="$PROFILE" --remote-debugging-port=DBG about:blank &
# poll: curl -s -m 1 http://127.0.0.1:DBG/json/version until it answers
```
Capture:
```
node scripts/video/capture_board_states.js PORT DBG <lessonId> "HEADLINE" \
  "Label1||Label2" 1600 900 0 OUTDIR STATES.json
```
- HEADLINE + labels: text that appears ONLY in the target component; the band is the
  innermost div containing all of them. Copy text EXACTLY from index.html source —
  curly apostrophes (’) and all. If the found band is wrong size (check printed
  rects.json band), adjust find strings; WRAP_UP=N env walks N ancestors up.
- STATES.json: `{"states":[{}, {"panels":[{"label":"...","ring":"#hex"}]},
  {"elements":[{"text":"...","ring":"#hex"}]}, ...]}`. Element entries accept
  `"row": true` (ring a bullet row incl. its dot) and `"mark": true` (tinted
  sentence-highlight inside a paragraph). Accent-colored cards ring in their OWN
  accent color, not purple. One ring per point the narration makes.
- Verify every state PNG visually (sips -Z 1100 + Read). If a chip highlight SHIFTS
  a centered heading or reflows anything (compare state-N vs state-0), fall back to
  post-compositing: keep state-0, draw the 12px (3px CSS) rounded ring +
  `#6e51ff` 13%-alpha chip pill behind the label text with cv2 at 4x (measure text
  extent from dark pixels in the label strip; rects.json gives label rects — harvest
  element rects with a dummy element state if needed). States must be pixel-identical
  outside the highlight.
- Match highlight granularity to the narration. Ring the whole board or card while the
  narration addresses it as a whole; move to an item or row ring when the narration
  names that part. If the narration walks several sections, the ring walks them too.
- Resolve every highlight color in the repair manifest before capture. A target inside
  an Editorial Explainer card or flow step inherits that component's stored locked
  accent: green `#0f7a4a`, teal `#0e8f86`, blue `#1652f0`, editorial purple
  `#4f2fc4`, amber `#a9760c`, or red `#c41f28`. Use the exact same token for the ring
  and any title chip. Never infer color from column position, sample the illustration,
  or default an accented component to purple. A neutral title or board-wide target may
  use standard video purple `#6e51ff`. Write both `highlight_color` and
  `highlight_source` in the board sync manifest; acceptable sources are
  `card_locked_accent`, `neutral_video_purple`, and `none`.
- If one spoken point explicitly combines differently colored components, preserve
  each component's own accent when showing multiple rings. If the narration is only
  summarizing the board, remove the rings and show the complete unmarked board.
- Close boards: only touch if your span plan says so; closes were standardized 8/4.

## 3. Build legs (ken_burns_path.py)
- PNGs are 6400×3600 (dsf4). rects.json coords are CSS px on 1600×900 → multiply by 4.
- FRAMING STANDARD (owner rule 8/7): the wide/"full board" window is sized to the
  BAND, not the canvas: `w = band.w*4/0.90`, centered on the band (board fills ~90%
  of frame width). NEVER frame the whole 1600×900 canvas.
- Spec per STATE (one run per highlight state, on that state's PNG):
  `{"image": ..., "fps":30, "out_w":1280, "out_h":720, "upscale":3, "beats":[...]}`
  beats = {frames, from?, to} with (cx, cy, w) in image px. Thread camera ACROSS runs:
  each run's first beat needs explicit "from" = previous run's final "to" (the tool
  errors otherwise). Sum of beat frames per run = that state's frame budget; total
  across runs = replaced span length EXACTLY (end_frame - start_frame, end exclusive).
- Motion: open at the wide framing; ~24-30 frame transit into a dive, then drift-hold
  (shrink w ~3% over the hold). Compact boards (everything legible at 720p wide view):
  NO dives — rings pop at word onsets, ≤4%-per-30s push only. Dives are for boards
  whose item text needs zoom to read. A dive frames the whole card; never crop or pan
  inside it. Sequential-step boards stay full-frame while the ring walks the steps.
  Never let a window edge slice a heading; check the state PNG geometry (rects) when
  picking windows.
- Render: `.video-venv/bin/python scripts/video/ken_burns_path.py spec.json out.mkv`
  (FFV1). Concat the state runs: concat demuxer list + `-c copy` → leg.mkv. Verify
  each leg's decoded frame count == span length (decode loop, not metadata).

## 4. Splice (ONE re-encode)
```
bash scripts/video/ffmpeg.sh -y -i videos/<slug>.mp4 -i leg1.mkv [...] -filter_complex "
[0:v]trim=start_frame=0:end_frame=A1,setpts=N/(30*TB)[s0];
[1:v]setpts=N/(30*TB)[l1];
[0:v]trim=start_frame=B1:end_frame=A2,setpts=N/(30*TB)[s1];
... [s0][l1][s1]...concat=n=K:v=1:a=0,setpts=N/(30*TB),format=yuv420p[v]" \
 -map "[v]" -map 0:a -r 30 -c:v libx264 -crf 18 -preset medium -c:a copy videos/<slug>-v2.mp4
```
CRITICAL: `setpts=N/(30*TB)` on EVERY branch BEFORE concat (a missing one silently
drops a frame).

## 5. Verify (mandatory — report every result)
1. Decoded frame count (cv2 read loop) of -v2 == original. EXACT.
2. Audio md5 identical: `ffmpeg -i X -map 0:a -c copy -f data -` piped to md5.
3. `scenes.py <v2> --seam A B` around EVERY splice boundary: exactly one diff spike
   at the boundary frame, flat (<5) neighbors — no leaked frames.
4. **Visual handoff check:** narration selects the intended visual, but the source's
   exact visual cut selects the integer splice frame. Inspect the final replaced
   frame and first restored frame individually at full resolution, then inspect a
   short sequence on both sides. The first restored frame must already be the next
   approved shot; no frame from an old graphic may survive. Never approve a seam
   from Whisper or second-based timing alone.
5. Junction smoothness inside legs: state-pop junctions should diff <12 (motion
   continuous, only the ring/chip changes).
6. Save review frames to /tmp/retrofit-review/<slug>/: for each replaced span, the
   original frame and the -v2 frame at span start+1s and span midpoint, full res.
7. Eyeball (Read) each leg's dive/hold framing: text legible, nothing sliced, ring on
   the right item.

## Report format (your final message, nothing else)
VIDEO: <slug>
SPANS_REPLACED: <start_frame-end_frame (mm:ss-mm:ss) | board | states count> per line
CAPTURE_NOTES: <find-strings used, any post-composite fallback, any surprises>
VERIFY: frames <n>/<n> | audio IDENTICAL/DIFFER | seams <k>/<k> single-spike | junctions max diff <x>
REVIEW_FRAMES: /tmp/retrofit-review/<slug>/
CONCERNS: <anything the owner must look at, or "none">
