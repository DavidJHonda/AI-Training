#!/usr/bin/env python
"""KEN BURNS PATH — a multi-region camera move over ONE still, timed to narration.

The single-region recipe in README.md (fit full-height + blurred side bars +
zoompan) is for a still that is shown whole. This is for the other case: a dense
illustration whose REGIONS answer successive narration beats. The camera crops
16:9 windows straight out of the image and glides between them, so the frame is
always full-bleed (no bars) and each beat lands on the thing being said.

Beats are given in the image's own pixel coordinates as (cx, cy, w) — the window
centre and its WIDTH; height is derived from the output aspect, so a window is
always 16:9 no matter what shape the source is. Within a beat the move is
smoothstepped, i.e. it eases out of rest and back to rest, so the camera settles
at every narration boundary instead of sliding through it.

Pick the beat boundaries from scenes.py cuts that already bracket the narration —
inheriting the original's cut rhythm beats inventing one.

Spec (JSON):
  {"image": "...jpg", "fps": 30, "out_w": 1280, "out_h": 720, "upscale": 3,
   "beats": [{"label": "title", "frames": 219,
              "from": [701, 395, 1402], "to": [701, 282, 1000]}, ...]}

A beat may omit "from" to continue from the previous beat's "to" (the usual case
— that is what makes the path continuous).

Rings (post-crop highlights, owner rule 2026-09-10): capture the board ONCE,
unmarked, and let this tool draw every highlight AFTER the crop so the stroke is
a constant RING_PX (5) on the delivery frame however far the camera dives. The
capture's rects.json supplies the rectangles; the spec lists them on the LEG's
own frame timeline (half-open [start, end)):

  "rings": [{"start": 0, "end": 219, "rect": [x, y, w, h], "color": "#1652f0",
             "pad": 0, "radius": 14}, ...]

`rect` is in image pixels (rects.json CSS px x 4 for a dsf4 capture). The
stroke's INNER edge sits `pad` image px outside the rect (0 = trace the outer
component boundary, the whole-card case); `radius` is the corner radius in
image px. Overlapping ring spans draw together, so combined states need no
special handling: list both.

A beat's "from"/"to" may be {"fit": [x, y, w, h], "margin": 24, "pad": 0}
instead of [cx, cy, w]: the camera window is derived from that padded ring
rectangle so the whole ring sits inside the frame with `margin` output px of
clearance (grader rule: never choose ring and camera coordinates
independently). Widen `margin` to hold a wider view.

Usage:
  ken_burns_path.py spec.json out.mkv          # lossless FFV1 leg for the concat
  ken_burns_path.py spec.json --preview DIR    # just the keyframe stills, to eyeball framing
"""
import argparse
import json
import subprocess
import sys

import cv2

RING_PX = 5  # constant stroke weight on the delivery frame (grader: never thicker when zoomed)

FFMPEG = subprocess.run(
    [sys.executable, "-c", "import imageio_ffmpeg,sys; sys.stdout.write(imageio_ffmpeg.get_ffmpeg_exe())"],
    capture_output=True, text=True, check=True).stdout.strip()


def smoothstep(t):
    return t * t * (3.0 - 2.0 * t)


def window(cx, cy, w, aspect, iw, ih):
    """Clamp a (centre, width) window into the image, keeping its size."""
    h = w / aspect
    if w > iw or h > ih:
        sys.exit(f"window {w:.0f}x{h:.0f} is larger than the {iw}x{ih} image")
    cx = min(max(cx, w / 2), iw - w / 2)
    cy = min(max(cy, h / 2), ih - h / 2)
    return cx - w / 2, cy - h / 2, w, h


def hex_bgr(h):
    h = h.lstrip("#")
    return (int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16))


def fit_window(fit, aspect, ow, up):
    """Camera (cx, cy, w) whose 16:9 window holds the padded ring rect with
    `margin` output px of clearance on every side. The ring's outer edge is the
    rect grown by pad (image px) plus RING_PX (output px, converted at the
    resulting scale), so the clearance is measured from the visible stroke."""
    x, y, w, h = fit["fit"]
    pad, margin = float(fit.get("pad", 0)), float(fit.get("margin", 24))
    # Solve for the window width W: scale = ow / W; need
    #   (w + 2 pad) * scale + 2 RING_PX + 2 margin <= ow   and the same for height.
    inner_w = ow - 2 * (RING_PX + margin)
    inner_h = ow / aspect - 2 * (RING_PX + margin)
    W = max((w + 2 * pad) * ow / inner_w, (h + 2 * pad) * (ow / aspect) / inner_h)
    return [x + w / 2, y + h / 2, W]


def resolve(spec, aspect, ow, up):
    """Expand beats into (label, frames, from, to), threading omitted 'from'
    and resolving {"fit": ...} keyframes into (cx, cy, w)."""
    def key(k):
        return fit_window(k, aspect, ow, up) if isinstance(k, dict) else list(k)
    out, prev = [], None
    for b in spec["beats"]:
        src = b.get("from", prev)
        if src is None:
            sys.exit("first beat needs an explicit 'from'")
        to = key(b["to"])
        out.append((b.get("label", "?"), int(b["frames"]), key(src), to))
        prev = to
    return out


def draw_ring(frame, x0, y0, x1, y1, color, radius):
    """Anti-aliased rounded-rect stroke of RING_PX centred on the given box
    (output px). Corner radius is clamped so tiny boxes still close."""
    t = RING_PX
    r = max(0.0, min(radius, (x1 - x0) / 2, (y1 - y0) / 2))
    if r < 1:
        cv2.rectangle(frame, (int(round(x0)), int(round(y0))), (int(round(x1)), int(round(y1))),
                      color, t, cv2.LINE_AA)
        return
    R = int(round(r))
    X0, Y0, X1, Y1 = (int(round(v)) for v in (x0, y0, x1, y1))
    cv2.line(frame, (X0 + R, Y0), (X1 - R, Y0), color, t, cv2.LINE_AA)
    cv2.line(frame, (X0 + R, Y1), (X1 - R, Y1), color, t, cv2.LINE_AA)
    cv2.line(frame, (X0, Y0 + R), (X0, Y1 - R), color, t, cv2.LINE_AA)
    cv2.line(frame, (X1, Y0 + R), (X1, Y1 - R), color, t, cv2.LINE_AA)
    for (cx, cy, a0) in ((X0 + R, Y0 + R, 180), (X1 - R, Y0 + R, 270),
                         (X1 - R, Y1 - R, 0), (X0 + R, Y1 - R, 90)):
        cv2.ellipse(frame, (cx, cy), (R, R), 0, a0, a0 + 90, color, t, cv2.LINE_AA)


def rings_for(spec):
    out = []
    for r in spec.get("rings", []):
        out.append((int(r["start"]), int(r["end"]), [float(v) for v in r["rect"]],
                    hex_bgr(r.get("color", "#6e51ff")), float(r.get("pad", 0)),
                    float(r.get("radius", 0))))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--preview", metavar="DIR",
                    help="write the first/last frame of each beat here and stop")
    args = ap.parse_args()

    spec = json.load(open(args.spec))
    ow, oh = spec.get("out_w", 1280), spec.get("out_h", 720)
    fps, up = spec.get("fps", 30), spec.get("upscale", 3)
    aspect = ow / oh

    img = cv2.imread(spec["image"])
    if img is None:
        sys.exit(f"cannot read {spec['image']}")
    ih, iw = img.shape[:2]
    beats = resolve(spec, aspect, ow, up)
    total = sum(b[1] for b in beats)
    rings = rings_for(spec)
    for (a, b, *_rest) in rings:
        if not (0 <= a < b <= total):
            sys.exit(f"ring span [{a}, {b}) is outside the leg's {total} frames")

    # Upscale once; every crop is taken from this so integer rounding of the crop
    # rect costs 1/up of a source pixel instead of a whole one (the jitter the
    # single-region recipe's 3x upscale exists to kill).
    big = cv2.resize(img, (iw * up, ih * up), interpolation=cv2.INTER_LANCZOS4)

    def render(cx, cy, w, frame_no=None):
        x, y, ww, hh = window(cx, cy, w, aspect, iw, ih)
        X, Y = int(round(x * up)), int(round(y * up))
        W, H = int(round(ww * up)), int(round(hh * up))
        crop = big[Y:Y + H, X:X + W]
        interp = cv2.INTER_AREA if W > ow else cv2.INTER_LANCZOS4
        frame = cv2.resize(crop, (ow, oh), interpolation=interp)
        if frame_no is not None and rings:
            scale = ow / ww  # output px per image px at this camera
            frame = frame.copy()
            for (a, b, rect, color, pad, radius) in rings:
                if not (a <= frame_no < b):
                    continue
                rx, ry, rw, rh = rect
                # stroke centreline = rect grown by pad (image px) + half a stroke
                # (output px), so the INNER edge of the stroke sits at rect+pad.
                half = RING_PX / 2.0
                x0 = (rx - pad - x) * scale - half
                y0 = (ry - pad - y) * scale - half
                x1 = (rx + rw + pad - x) * scale + half
                y1 = (ry + rh + pad - y) * scale + half
                draw_ring(frame, x0, y0, x1, y1, color, radius * scale + half)
        return frame

    if args.preview:
        f0 = 0
        for i, (label, n, a, b) in enumerate(beats):
            for tag, kf, fn in (("in", a, f0), ("out", b, f0 + n - 1)):
                p = f"{args.preview}/kb{i + 1}-{label}-{tag}.jpg"
                cv2.imwrite(p, render(*kf, frame_no=fn), [cv2.IMWRITE_JPEG_QUALITY, 95])
                print(f"{p}  frame={fn} cx={kf[0]:.1f} cy={kf[1]:.1f} w={kf[2]:.1f}")
            f0 += n
        print(f"# {len(beats)} beats, {total} frames, {total / fps:.3f}s, {len(rings)} rings")
        return

    if not args.out:
        sys.exit("need an output path (or --preview)")

    proc = subprocess.Popen(
        [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
         "-s", f"{ow}x{oh}", "-r", str(fps), "-i", "-",
         "-c:v", "ffv1", "-level", "3", args.out],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    written = 0
    for label, n, a, b in beats:
        for k in range(n):
            # smoothstep across the beat: eases out of rest, settles back to rest,
            # so the camera stops on every narration boundary.
            t = smoothstep(k / (n - 1)) if n > 1 else 1.0
            cx, cy, w = (a[j] + (b[j] - a[j]) * t for j in range(3))
            proc.stdin.write(render(cx, cy, w, frame_no=written).tobytes())
            written += 1
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit("ffmpeg failed")
    print(f"{args.out}: {written} frames, {written / fps:.3f}s")


if __name__ == "__main__":
    main()
