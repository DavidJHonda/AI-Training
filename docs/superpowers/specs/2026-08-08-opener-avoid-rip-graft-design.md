# opener-avoid: graft two rip-current visuals from the 7/31 reject

**Date:** 2026-08-08
**Base:** `videos/opener-avoid.mp4` (5340 frames, 2:58.0, shipped 2026-08-07 as commit 5650213)
**Donor:** `Prompts/donors/2026-07-31/opener-avoid-66-REJECT-donated-nothing.mp4` (6887 frames, 3:49.6)
**Output:** `videos/opener-avoid-v2.mp4` — never modify the shipped file in place

## Goal

The donor's rip-current sequence is the best footage either roll produced. Take the
two spans that fit the incumbent's own cuts frame-exactly, leave everything else
alone. Narration is untouchable: the audio stream is copied, so the required lines,
the section bridge, and the runtime are all preserved by construction.

## What is NOT changing, and why

- **Audio.** Stream-copied. MD5 must match the input exactly.
- **Runtime.** 5340 frames in, 5340 frames out. 2:58.0.
- **`1:48.9–1:57.1` READ THE WATER illustration** (frames 3267–3512) — the owner's own
  call from 1e2f39a, rebuilt full-frame in 5650213. Stays.
- **`2:04.1–2:41.8` section-board ring tour** and **`2:41.8–2:58.0` standard close** —
  both rebuilt 2026-08-07. Stays.
- **`1:31.5–1:43.1` SHORELINE diagram.** The donor's voxel wave was considered and
  rejected: it covers only 6.6s of an 11.5s span, would need an off-cut junction at a
  word onset, and would put a paper-craft wave one cut after the incumbent's
  hand-drawn ink waves — same subject, clashing register.

## The two grafts

### Span B — lifeguard tower

| | |
|---|---|
| Base span | frames **3092–3267** (1:43.07–1:48.90), 175 frames |
| Narration | "Lifeguards spot these currents all day because they know the specific shape a rip current makes in the water." |
| Replaces | thin sketched tower on dotted-grid cream |
| Donor source | frames **4005–4180** (2:13.50–2:19.33), 175 frames — the TAIL of the donor's tower shot (full span 3963–4180) |
| Build | `graft_scene.py --replace-visual`. The shot carries its own motion (mean per-frame diff 2.28, only 47/217 frames near-zero: camera drift plus animating swimmers), so it needs no Ken Burns. |

Taking the tail rather than the head lands the span on the donor shot's own settle and
gives the most developed swimmer motion. Verify by eye; if the head reads better,
use 3963–4138 instead — either is frame-exact.

Known cosmetic flaw, accepted: a hard grey wall shadow behind the tower on the right
third reads as studio lighting rather than sky.

### Span C — red-T rip current

| | |
|---|---|
| Base span | frames **3512–3723** (1:57.07–2:04.10), 211 frames |
| Narration | "AI has its own rip currents. Surviving them requires the same proactive recognition of deceptive shapes." |
| Replaces | a sketched chat-window filler scene |
| Donor source | ONE frame from **3699–3872** (2:03.30–2:09.07); take frame **3780** (t=126.0) |
| Build | ILLUSTRATION INSERT recipe, **SETTLE variant** — `z='1.06-0.06*on/(N-1)'`, N=211 |

The donor shot is effectively a still (169/173 frames near-zero), so a single frame plus
our own Ken Burns is cleaner than carrying 173 real frames and freeze-filling 38.

Settle-out rather than push-in, for two reasons the README already gives: the image is
edge-to-edge dense, so a push-in crops the T's crossbar at the top and the figure on the
sand at the bottom with no y-anchor that saves both; and the span hands off on a hard cut
to the section board, so the complete shape wants to be on the LAST frame — arriving
exactly as the narration reaches "deceptive shapes."

The donor frame is already 1280×720 and frame-filling, so there is no fit step and no
blurred side bars. Upscale 3× lanczos before zoompan regardless, or integer rounding
jitters.

## Verification battery

Every item is a gate, not a nice-to-have. Report each with its measured value.

1. Output frame count **== 5340** exactly.
2. Audio stream **MD5-identical** to `videos/opener-avoid.mp4`.
3. `scenes.py --seam` at frames **3092, 3267, 3512, 3723** — exactly one spike each, no
   leaked boundary frame. Cut with `trim=start_frame=A:end_frame=B` (end exclusive),
   never time-based trim.
4. Span C mid-span per-frame diffs **continuous, ~0.7–4.5**. A 0.0 means the zoom did not
   take; a spike means jitter.
5. Span C **first** frame (most zoomed): confirm nothing essential is already cropped.
   Span C **last** frame: the T's crossbar and the figure on the sand both fully in frame.
6. pts-delta histogram **single-valued**. This base is exactly 30fps (tbn 15360), not
   the 30.004 variant, so normalize every concat input with `settb=1/30,setpts=N/(30*TB)`
   — do not apply the 30004 recipe from the flattery-trap note.
7. **Eyeball** frames on both sides of all four junctions. Frame counts alone have
   missed pixel-format garbage before.

## Risks

- **Register.** With both grafts in, 1:31–2:04 runs cream schematic → paper-craft →
  photographic → paper-craft → app board. Accepted: the incumbent already breaks
  register at READ THE WATER, and the whole stretch is one chapter about the sea.
- **Span B head-vs-tail** is a judgment call to settle by eye during the build, not a
  blocker.
- Nothing here touches `index.html`, any lesson board, or any close board, so
  design-check and board-parity rules do not apply to this change.
