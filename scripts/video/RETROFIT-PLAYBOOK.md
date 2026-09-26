# Board retrofit: current JPG assets

Updated 2026-09-15. Read [Edit Spec](EDIT-SPEC.md) for scope and visual/audio rules.
This procedure replaces board spans without rebuilding the canonical artwork.
Use [Technical Recipes](TECHNICAL-RECIPES.md) only for a relevant rendering problem.

## 1. Identify scope and sources

A visual-only retrofit preserves narration, duration, FPS, and the copied audio
stream. New pauses or narration changes are a separate approved audio scope.
Use a fresh `Prompts/<lesson>-vN.mp4` output and leave the finished video unchanged.
Do not require every existing board to be rebuilt for a narrow repair; report
unrelated defects under Edit Spec section 1.

Run commands from the repository root. Use `.video-venv/bin/python` and
`bash scripts/video/ffmpeg.sh`. Record source paths, hashes, and the manifest.
If borrowing from a finished video, use an identified stable snapshot for the
active edit rather than a live path that another ship may overwrite.

## 2. Map narration and exact visual cuts

Use `scenes.py` and sequential frame decoding to identify replacement boundaries.
Do not choose cuts from Whisper timestamps or time-based seeks alone. Record
half-open frame intervals `[start_frame, end_frame)` on source and output timelines.
Use word timestamps to time rings within those intervals, verifying actual speech.
Preserve useful Notebook drawings around the board; a board's availability is not
an instruction to cover the whole topic. Follow Edit Spec's full-view opening rule.

## 3. Use the canonical JPG and record geometry

Resolve the exact JPG path referenced by the current lesson in `index.html`.
Inspect that image and record its pixel dimensions and hash. Do not recreate HTML,
change text wrapping, alter the board's proportions, or overwrite it for video use.

Record complete card, bubble, row, and banner rectangles in source-image pixels.
Reuse older geometry only when the asset and coordinate transform still match.
Text recognition can help locate content, but each ring must follow the complete
component's boundary, not just its words. Inspect those bounds against the image.
Record each target's accent color and provenance in the manifest, following Edit
Spec section 5; do not infer colors from card order or unrelated illustration pixels.

`ken_burns_path.py` needs a 16:9 camera window within its input image. When the
canonical JPG's shape needs surrounding space, prepare a temporary lossless padded
canvas using the established house background/side-bar treatment. Preserve the
JPG content and aspect ratio. Record scale and placement offsets; transform all
rectangles with exactly the same values. Do not assume a 1600x900 source, a 902px
HTML wrapper, or a 4x coordinate multiplier. These are not universal asset sizes.

Browser capture is a fallback only for a verified live component with no canonical
image. Use `capture_board_states.js` with `RECTS_ONLY=1`, inspect its unmarked output
and rectangle metadata, and record the actual capture scale. Do not regenerate an
existing JPG merely to recover old DOM selectors. Use task-specific browser/server
ports; do not take over another task's session or the reserved 8768/9338 ports.

## 4. Build one board leg

Use one `ken_burns_path.py` specification per continuous board span:

```json
{
  "image": "temporary-board-canvas.png",
  "fps": 30, "out_w": 1280, "out_h": 720, "upscale": 3,
  "beats": [], "rings": []
}
```

Fill `beats` with `{label, frames, from?, to}`. Camera coordinates `[cx, cy, w]`
are in the input image's pixels; `to` can instead use
`{"fit": [x, y, w, h], "margin": 24, "pad": 0}` to keep a complete component visible.
Beat frames must sum to the exact planned leg length.

Rings use `{start, end, rect: [x,y,w,h], color, pad, radius}` on the leg's half-open
frame timeline. Coordinates use the same input image as the camera. Whole-component
rings use `pad: 0`; the renderer draws the fixed 4 px (6 px at 1080p) outline after cropping.
Keep compact boards whole; dense boards tour complete cards. Do not invent pauses
to fit camera moves. AI Chat boards remain compact. See Edit Spec sections 3–6.

```sh
.video-venv/bin/python scripts/video/ken_burns_path.py spec.json --preview PREVIEW_DIR
.video-venv/bin/python scripts/video/ken_burns_path.py spec.json leg.mkv
```

Inspect preview frames before rendering. Verify the leg's frame count by decoding.
Temporary PNG canvases and lossless FFV1 legs are build intermediates, not new
canonical course assets.

## 5. Assemble once and verify

Use the concat filter for mixed-source legs, normalize each branch's timestamps,
and encode video once from the selected source and lossless intermediates. At
30fps, each branch uses `setpts=N/(30*TB)` before concat. Copy the original audio
for a visual-only repair; never silently re-encode or clean it up.

For the final encoded candidate:

- Decode and compare frame count, FPS, duration, and audio stream hash with the
  base for a visual-only repair. An approved audio-changing build follows its
  explicit duration/frame plan instead.
- Run `transition_guard.py` on every declared output boundary and inspect the
  strips. The first restored frame must already be the approved destination,
  with no stale scene tail. A detector pass alone is insufficient.
- Inspect settled frames at each changed ring state: complete component, correct
  color/onset, fixed 4 px stroke (6 px at 1080p), readable text, and no clipped edges.
- Confirm changed boards open whole and their compact/dense treatment is correct.
- If audio edits were approved, measure selected pauses against the plan and listen
  to affected joins. Report what was not heard rather than claiming verification.

Record source/asset paths and hashes, geometry transforms, replacement spans,
manifest and commands, review-frame paths, completed checks, and remaining issues
in the active review. For narrow repairs, identify broader checks not performed.
The whole-file ship checklist and publication approval remain separate.
