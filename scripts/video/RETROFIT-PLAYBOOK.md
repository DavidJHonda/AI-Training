# Board-retrofit playbook (v2 builds, 2026-08-07)

Read `EDIT-SPEC.md` first: it defines what a candidate must contain (every board,
full-view open, compact vs dense by text legibility, rings, pauses, close). This
playbook is the how.

You are building `videos/<slug>-v2.mp4`: replacing off-format board spans in a shipped
lesson video with legs built from CURRENT page captures, using the app's highlight
system. HARD RULES: never modify the shipped `videos/<slug>.mp4`; never run git
commands; narration/audio is untouchable (stream-copied). The house highlight system
uses outline rings popping at narration onsets, with no shaded text or heading fills — NEVER
reproduce the engine's yellow washes, marker circles, underlines, orange arrows or
corner brackets in any form.

Run everything from the repository root; do not change directories inside a compound
command because that breaks the relative `.video-venv/...` paths. Python:
`.video-venv/bin/python` (has cv2, faster_whisper, imageio_ffmpeg). ffmpeg:
`bash scripts/video/ffmpeg.sh ...`.
Shell is zsh: `for x in "a b"` does NOT word-split; write args explicitly.

## Preserve useful Notebook visuals (owner clarification, 2026-09-09)

Keep the original Notebook opening, illustrations, and motion graphics wherever
they support the narration accurately. A board repair should replace the actual
board walkthrough, not expand that board over the whole topic. Use original
visuals for the setup and transitions, then the current course board when its
rows or examples are being taught. A useful visual from a cut passage may be
reused under matching retained narration without restoring the removed audio.

Use outlines only for video highlights (owner correction, 2026-09-09). Do not add
shading, tinted fills, or chips behind column titles, card headings, labels, or
other text. Preserve the board’s existing colors and backgrounds. The outline
alone identifies the active item, including on the final board. This supersedes
the earlier heading-fill instruction.

## Canonical content-board walk (updated 2026-09-10; supersedes the 2026-08-07 text)

Use this treatment whenever narration walks two or more points on a current lesson
board:

- Replace only the span where the board's exact content is being taught. Enter at the
  first spoken beat that benefits from the board and exit when narration moves past its
  content. Keep useful Notebook graphics before and after; do not absorb the board-level
  introduction or the following transition merely because the board is available.
- Use the exact current app capture. Never an engine recreation or a recomposed
  approximation when the lesson board exists.
- Compact or lighter-text board (every item legible at 720p in whole-board framing):
  hold the whole board in fixed framing. Start unmarked while narration addresses the
  board as a whole, then ring exactly one active card or row at each spoken onset. A
  restrained whole-board push is allowed; no dives or pans between items.
- Dense or text-heavy board: establish the complete unmarked board, dive to the complete
  active card or section, and pan smoothly to the next complete area as narration moves.
  Never crop inside a card. Pull back when timing permits.
- Highlights replace one another; they accumulate only when narration explicitly
  combines or compares points.
- Static time while narration explains the displayed content is teaching, not dead
  time. End the span when narration moves to the next beat.

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

## 2. Capture the board ONCE from the CURRENT page (rects-only, 2026-09-10)

Rings are no longer baked into captures. Capture one unmarked board and export the
rectangles; `ken_burns_path.py` draws every ring after the camera crop at a constant
5px (grader rule: zooming a board must not thicken its border). Start your own
server+chrome on YOUR assigned ports (never 8768/9338), from the repository root:
```
python3 -m http.server PORT --bind 127.0.0.1 &
PROFILE=$(mktemp -d -t chromeprof)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --disable-gpu --user-data-dir="$PROFILE" --remote-debugging-port=DBG about:blank &
# poll: curl -s -m 1 http://127.0.0.1:DBG/json/version until it answers
```
Capture:
```
RECTS_ONLY=1 node scripts/video/capture_board_states.js PORT DBG <lessonId> "HEADLINE" \
  "Label1||Label2" 1600 900 0 OUTDIR TARGETS.json
```
- HEADLINE + labels: text that appears ONLY in the target component; the band is the
  innermost div containing all of them. Copy text EXACTLY from index.html source —
  curly apostrophes (’) and all. If the found band is wrong size (check printed
  rects.json band), adjust find strings; WRAP_UP=N env walks N ancestors up.
- TARGETS.json uses the STATES shape so every panel and element you will ring gets
  located: `{"states":[{"panels":["Label"],"elements":[{"text":"...","row":true}]}]}`.
  `"row": true` targets a bullet row including its dot; `"mark": true` targets a
  sentence inside a paragraph. With RECTS_ONLY only `state-0.png` is written, but
  `rects.json` carries `band`, `cards` (one per label, in label order) and
  `elements` (keyed by exact text), all in CSS px on the 1600×900 canvas.
- Verify `state-0.png` visually: the actual lesson board at the app column width,
  no reformatting, nothing clipped. Verify each rect in `rects.json` encloses the
  complete component (illustration, title, body, all four edges), not a text span.
- Resolve every ring color in the board sync manifest before building. A target
  inside an Editorial Explainer card or flow step inherits that component's stored
  locked accent: green `#0f7a4a`, teal `#0e8f86`, blue `#1652f0`, editorial purple
  `#4f2fc4`, amber `#a9760c`, or red `#c41f28`. A neutral title or board-wide
  target may use standard video purple `#6e51ff`. Never sample the illustration,
  infer color from column position, or default an accented component to purple.
  Write `highlight_color` and `highlight_source` (`card_locked_accent`,
  `neutral_video_purple`, `none`) in the manifest.
- Match granularity to the narration: a whole-component ring while it addresses the
  card, bubble, or banner; a component ring when it names a section, row, or element.
  One ring per point being made; rings replace one another unless the narration
  explicitly combines points, in which case list both spans.
- AI Chat boards: a turn ring traces the complete speech bubble. Takeaway rings trace
  the complete gold banner. The first settled frame of an active bubble or banner
  already carries its ring; never open an active state with an unmarked camera move.
- Close boards: only touch if your span plan says so; closes were standardized 8/4.

## 3. Build the leg (ken_burns_path.py, one run per board span)
- `state-0.png` is 6400×3600 (dsf4). rects.json coords are CSS px on 1600×900 →
  multiply by 4 for `rect` and `fit` values.
- FRAMING STANDARD (owner rule 8/7): the wide/"full board" window is sized to the
  BAND, not the canvas: `w = band.w*4/0.90`, centered on the band (board fills ~90%
  of frame width). NEVER frame the whole 1600×900 canvas.
- One spec for the whole span:
  `{"image": "state-0.png", "fps":30, "out_w":1280, "out_h":720, "upscale":3,
    "beats":[...], "rings":[...]}`.
  Beats are `{label, frames, from?, to}`; `to` is `[cx, cy, w]` in image px, or
  `{"fit": [x, y, w, h], "margin": 24, "pad": 0}` to derive the settled camera from
  the ring rectangle itself (the ring stays inside the frame with `margin` output px
  of clearance; the grader forbids choosing ring and camera independently). Sum of
  beat frames = replaced span length EXACTLY (end_frame - start_frame, end exclusive).
- Rings are `{"start", "end", "rect": [x, y, w, h], "color": "#hex", "pad", "radius"}`
  on the leg's own frame timeline, half-open. `start` = the spoken onset frame of
  that target minus the leg's first frame. Whole-component ring: `rect` = the card,
  bubble, or banner rect ×4, `pad` 0, so the stroke's inner edge traces the outer
  boundary. Component ring: `rect` = the element's ink rect ×4 with balanced `pad`;
  for stacked sections inside one card, set x and w from the card's rails inset by
  the 16px clearance so every section ring shares the same horizontal edges.
  `radius` matches the component's corner radius (image px).
- Motion: open at the wide framing; ~24-30 frame transit into a dive, then drift-hold
  (shrink w ~3% over the hold). Compact boards (everything legible at 720p wide view):
  NO dives — rings pop at word onsets, ≤4%-per-30s push only. Dives are for boards
  whose item text needs zoom to read. A dive frames the whole card via `fit`; never
  crop or pan inside it. Sequential-step boards stay full-frame while the ring walks
  the steps. Never let a window edge slice a heading; check rects when picking windows.
- `--preview DIR` writes the first and last frame of every beat WITH the rings
  active at those frames. Eyeball every one before rendering: ring on the right
  component, all four edges inside the frame, nothing sliced.
- Render: `.video-venv/bin/python scripts/video/ken_burns_path.py spec.json leg.mkv`
  (FFV1). Verify the leg's decoded frame count == span length (decode loop, not
  metadata).

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
5. Ring onsets inside legs: at each ring `start`/`end` frame the diff should stay
   <12 (motion continuous, only the ring changes). Measure the stroke on a settled
   full-resolution frame at the widest and the tightest camera: 5px core at both.
6. Save review frames to /tmp/retrofit-review/<slug>/: for each replaced span, the
   original frame and the -v2 frame at span start+1s and span midpoint, full res.
7. Eyeball (Read) each leg's dive/hold framing: text legible, nothing sliced, ring on
   the right item.
8. For every requested editorial pause, run `silencedetect` on the final encoded
   output and report the measured interval. The prior teaching visual must hold until
   the pause ends; the next visual begins with the next spoken idea. Confirm the pause
   uses matched room tone with no orphan inhale or noise-floor cliff.

## Report format (your final message, nothing else)
VIDEO: <slug>
SPANS_REPLACED: <start_frame-end_frame (mm:ss-mm:ss) | board | states count> per line
CAPTURE_NOTES: <find-strings used, any post-composite fallback, any surprises>
VERIFY: frames <n>/<n> | audio IDENTICAL/DIFFER | seams <k>/<k> single-spike | junctions max diff <x>
REVIEW_FRAMES: /tmp/retrofit-review/<slug>/
CONCERNS: <anything the owner must look at, or "none">
