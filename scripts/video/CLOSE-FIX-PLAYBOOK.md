# Close-board apostrophe fix (2026-08-07)

Some shipped closes render STRAIGHT apostrophes (') because make_close_board.py takes
pill/sticky text as hand-typed CLI args. The app's copy uses CURLY (’). Fix = re-render
the close board with text copied VERBATIM from index.html CLOSE_BOARDS and replace the
close span. Nothing else about the video changes.

HARD RULES: never modify `videos/<slug>.mp4` (deliver `videos/<slug>-v2.mp4`); never run
git; audio is stream-copied and must come out bit-identical; run from
/Users/davidobrien/Developer/GitHub/AI-Training with ABSOLUTE paths (a `cd` breaks the
relative venv path). zsh: no word-splitting on unquoted vars; and inside filtergraph
strings always write `${var}:s=...` never `$var:s=...`.

PY=/Users/davidobrien/Developer/GitHub/AI-Training/.video-venv/bin/python
ffmpeg = `bash scripts/video/ffmpeg.sh ...`

## Steps

1. **Get the exact text.** From index.html `CLOSE_BOARDS`, the entry for the lesson id:
   `{ pill: "...", sticky: "..." }`. Extract it PROGRAMMATICALLY (python read + regex),
   write it to a file or pass via a python-built argv — do NOT retype it, that is the
   very bug you are fixing. Confirm the curly chars are present (`'’' in pill`).

2. **Find the close span.** Walk backward from the last frame while successive frame
   diffs stay < ~0.35 (the frozen/settled close). Also run
   `$PY scripts/video/scenes.py videos/<slug>.mp4` and prefer the actual cut where the
   close board arrives — replace from THAT cut to the last frame. Decode sequentially
   (never trust CAP_PROP_POS_FRAMES seeks; they drift at high frame numbers).

3. **Sample the background color** of the existing close (corner pixel, e.g. (8,8)) so
   the new board sits on the same ground: `--bg "#rrggbb"`.

4. **Render the board:**
   `$PY scripts/video/make_close_board.py --pill "<verbatim>" --sticky "<verbatim>" --bg <hex> --out board.png`
   Then READ board.png (crop + upscale the apostrophe words with cv2 INTER_LANCZOS4) and
   confirm the glyphs are curly. If the tool mangles them, fix the tool's HTML escaping
   rather than the text.

**COLOR RULE (learned the hard way 2026-08-07, found independently by two builds).**
Do NOT render the Ken Burns leg to an intermediate leg.mkv and then splice it: that puts
the board through two RGB→YUV roundtrips and, because plain `format=yuv420p` uses the
bt601 matrix while these mp4s are tagged bt709, the close ground lands 4-6 levels off
(the app's lavender #f6f5fb decodes grey). Do the zoompan INSIDE the splice filtergraph
with board.png as input 1 — one pass, exact match. With the single-pass form `-loop 1`
is unnecessary and harmful; a plain 1-frame image input plus `zoompan d=N` yields exactly
N frames with no `-frames:v`. If you ever must use an intermediate, add
`scale=out_color_matrix=bt709:out_range=tv` and `-colorspace bt709`.
Also: render at the app value `--bg "#f6f5fb"` unless the video's own close clearly sits
on a different ground. Sampling the shipped close's decoded corner and feeding THAT back
in compounds the encode shift. VERIFY by comparing the v2 close's background median
against the original close's — they should differ by ≤2 levels.

5. **Ken Burns leg**, N = span frames:
   `zoompan=z='1+Z*on/(N-1)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=N:s=1280x720:fps=30`
   with `Z = min(0.2 * N/210, 0.2)` (zoom endpoint scales with span length, cap 1.2 total).
   Follow with `format=yuv420p,setsar=1,settb=1/30,setpts=N/(30*TB)` — INTEGER ticks, or
   concat drops a frame. Render via `-loop 1 -i board.png` with an explicit
   `-frames:v N` (a -loop image input defaults to 25fps and comes out short).

6. **Splice, one re-encode:**
   ```
   bash scripts/video/ffmpeg.sh -y -i videos/<slug>.mp4 -i leg.mkv -filter_complex "
   [0:v]trim=start_frame=0:end_frame=A,setpts=N/(30*TB)[pre];
   [1:v]settb=1/30,setpts=N/(30*TB)[mid];
   [pre][mid]concat=n=2:v=1:a=0,setpts=N/(30*TB),format=yuv420p[v]" \
    -map "[v]" -map 0:a -r 30 -c:v libx264 -crf 18 -preset medium -c:a copy videos/<slug>-v2.mp4
   ```
   (A = close span start frame; the close runs to the end so there is no post segment.)

7. **Verify — report every number:**
   - decoded frame count (cv2 read loop) of -v2 == original, EXACT
   - audio md5 identical (`-map 0:a -c copy -f data -` | md5)
   - `scenes.py <v2> --seam` around the splice: exactly one spike, flat neighbors
   - the LAST frame is the close board, fully settled, text complete in frame
   - crop+upscale the apostrophe word(s) from the final frame and READ it: curly, matching
     the page
   - board text matches CLOSE_BOARDS verbatim (pill AND sticky, wording and punctuation)
   - save review frames to /tmp/close-fix/<slug>/: last frame, span-start frame, and the
     apostrophe crop

## Report (final message, nothing else)
VIDEO: <slug>
CLOSE_SPAN: <start_frame>-<end_frame> (<mm:ss>-<mm:ss>), N=<frames>
TEXT: pill "<...>" | sticky "<...>"  (verbatim from CLOSE_BOARDS)
VERIFY: frames <n>/<n> | audio IDENTICAL/DIFFER | seam single-spike yes/no (<diff>) | apostrophes CURLY/STRAIGHT | last-frame close yes/no
REVIEW: /tmp/close-fix/<slug>/
CONCERNS: <or "none">
