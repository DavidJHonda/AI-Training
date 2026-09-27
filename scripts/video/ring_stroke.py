#!/usr/bin/env python
"""Measure the on-screen stroke width of highlight rings in a finished video.

Audit for Edit Spec section 5 (owner rule 2026-09-26): rings are a FIXED on-screen
stroke, 6 px at 1080p = 4 px in the 1280x720 delivery frame, at any camera zoom.
Videos built under the earlier rules show 5 px (constant, 2026-09-10 to 09-21) or a
stroke that thickens on dives (artwork-scaled, 2026-09-21 to 09-26).

Method (sequential decode, every --step seconds): for each of the eight ring colours
in Edit Spec section 5, threshold the frame by colour distance, take the connected
components, and keep the hollow rectangles (bounding box at least --min-w x --min-h,
component area well under the box area). For each one the stroke is the median run
length of ring pixels across its four sides, sampled along the middle third of each
side, so rounded corners and gaps do not bias it. Card fills, banners, and text are
rejected as not hollow / not rectangular. Reported widths are at the threshold
--thr; calibrate against a video built under a known rule before reading absolute
values (What Is AI? 20260926ship2 is the fixed-4 px reference).

Output in <out>/: ring-stroke.txt (one line per detected ring per sample, then a
histogram and per-run summary), ring-stroke.json, and crops/ with a 4x zoomed corner
of the thinnest and thickest ring found so the number can be checked by eye.

Usage:
  .video-venv/bin/python scripts/video/ring_stroke.py course-assets/<slug>/<slug>.mp4 <out> [--step 0.5] [--thr 80]
"""
import argparse, json, os, sys
import cv2, numpy as np

COLORS = {  # Edit Spec section 5 tokens
    "green": "#0f7a4a", "teal": "#0e8f86", "blue": "#1652f0", "purple": "#4f2fc4",
    "amber": "#a9760c", "red": "#c41f28", "violet": "#6e51ff", "gold": "#f2cf5b",
}


def hex_bgr(h):
    h = h.lstrip("#"); return np.array([int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)], dtype=np.int32)


def stamp(t):
    m, s = divmod(t, 60); return f"{int(m)}:{s:05.2f}"


def side_runs(lab, k, x, y, w, h):
    """Median run length of label k crossing each side, sampled along the middle third."""
    widths = {}
    ys = range(y + h // 3, y + 2 * h // 3, max(1, h // 30))
    xs = range(x + w // 3, x + 2 * w // 3, max(1, w // 30))
    def run(seq):
        # length of the first run of True in seq
        hit = np.flatnonzero(seq)
        if hit.size == 0: return None
        i = hit[0]; n = 0
        while i + n < seq.size and seq[i + n]: n += 1
        return n
    L = [run(lab[yy, x:x + w] == k) for yy in ys]
    R = [run((lab[yy, x:x + w] == k)[::-1]) for yy in ys]
    T = [run(lab[y:y + h, xx] == k) for xx in xs]
    B = [run((lab[y:y + h, xx] == k)[::-1]) for xx in xs]
    for name, v in (("left", L), ("right", R), ("top", T), ("bottom", B)):
        v = [q for q in v if q is not None and q > 0]
        widths[name] = float(np.median(v)) if v else None
    vals = [v for v in widths.values() if v is not None]
    return (float(np.median(vals)) if vals else None), widths


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video"); ap.add_argument("out")
    ap.add_argument("--step", type=float, default=0.5)
    ap.add_argument("--thr", type=float, default=45.0, help="max RGB distance to a ring colour (solid pixels only; the anti-aliased edge pixel adds ~0.5 px to the true width)")
    ap.add_argument("--min-w", type=int, default=100); ap.add_argument("--min-h", type=int, default=50)
    ap.add_argument("--max-stroke", type=int, default=16)
    a = ap.parse_args()
    os.makedirs(os.path.join(a.out, "crops"), exist_ok=True)

    cols = {n: hex_bgr(h) for n, h in COLORS.items()}
    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    nframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); duration = nframes / fps
    every = max(1, int(round(a.step * fps)))
    H, W = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    rows = []
    i = 0
    thin = thick = None
    while True:
        ok, frame = cap.read()
        if not ok: break
        if i % every == 0:
            t = i / fps
            f32 = frame.astype(np.int32)
            names = list(cols)
            dists = np.stack([np.sqrt(((f32 - cols[n_]) ** 2).sum(axis=2)) for n_ in names])
            nearest = dists.argmin(axis=0)            # each pixel counts for ONE colour only
            for ci, cname in enumerate(names):
                mask = ((dists[ci] < a.thr) & (nearest == ci)).astype(np.uint8)
                if mask.sum() < 400: continue
                n, lab, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
                for k in range(1, n):
                    x, y, w, h, area = stats[k]
                    if w < a.min_w or h < a.min_h: continue
                    if area > 0.45 * w * h: continue                       # filled shape, not a ring
                    if area < 2 * (w + h) * 1.5: continue                   # too sparse to be a closed outline
                    stroke, sides = side_runs(lab, k, x, y, w, h)
                    if stroke is None or stroke > a.max_stroke: continue
                    # a ring's area is about stroke * perimeter; reject shapes far from that
                    est = area / max(1.0, 2.0 * (w + h) - 4 * stroke)
                    if not (0.5 * stroke <= est <= 1.8 * stroke): continue
                    touch = (mask[y, x:x + w].sum() + mask[y + h - 1, x:x + w].sum()) / (2.0 * w)
                    if touch < 0.25: continue                               # top/bottom edges barely populated
                    row = {"t": round(t, 3), "color": cname, "bbox": [int(x), int(y), int(w), int(h)],
                           "stroke": round(stroke, 2), "sides": {kk: (None if v is None else round(v, 2)) for kk, v in sides.items()},
                           "area_est": round(est, 2)}
                    rows.append(row)
                    crop = frame[max(0, y - 20):y + 80, max(0, x - 20):x + 120]
                    if thin is None or stroke < thin[0]: thin = (stroke, t, crop.copy(), cname)
                    if thick is None or stroke > thick[0]: thick = (stroke, t, crop.copy(), cname)
        i += 1
    cap.release()

    lines = [f"# {os.path.basename(a.video)}  {W}x{H}  duration={stamp(duration)}  step={a.step}s  thr={a.thr}",
             "# target: fixed 4 px at 720p (6 px at 1080p), Edit Spec section 5 (2026-09-26); widths are SOLID pixels at thr, true width is about +0.5",
             "# time      color    stroke   L    R    T    B    bbox(x,y,w,h)"]
    for r in rows:
        s = r["sides"]; f = lambda v: "  - " if v is None else f"{v:4.1f}"
        lines.append(f"{stamp(r['t']):>8}  {r['color']:7s}  {r['stroke']:5.1f}  {f(s['left'])} {f(s['right'])} {f(s['top'])} {f(s['bottom'])}   {tuple(r['bbox'])}")
    # runs: consecutive samples with a ring of the same colour and a similar box
    runs = []   # one track per colour, so two rings on screen at once do not break each other's run
    for r in rows:
        prev = [u for u in runs if u["color"] == r["color"]]
        u = prev[-1] if prev else None
        if u and r["t"] - u["end"] <= a.step * 1.01 and all(abs(p - q) < 40 for p, q in zip(r["bbox"], u["bbox"])):
            u["end"] = r["t"]; u["strokes"].append(r["stroke"])
        else:
            runs.append({"color": r["color"], "start": r["t"], "end": r["t"], "bbox": r["bbox"], "strokes": [r["stroke"]]})
    runs.sort(key=lambda u: u["start"])
    hist = {}
    for r in rows: hist[round(r["stroke"])] = hist.get(round(r["stroke"]), 0) + 1
    lines += ["", f"# {len(rows)} ring samples in {len(runs)} runs; stroke histogram (rounded px): " +
              ", ".join(f"{k} px: {v}" for k, v in sorted(hist.items())),
              "# runs (start, end, color, median stroke, min-max, samples)"]
    for u in runs:
        st = u["strokes"]
        lines.append(f"{stamp(u['start']):>8} - {stamp(u['end']):>8}  {u['color']:7s}  {np.median(st):4.1f}  {min(st):4.1f}-{max(st):4.1f}  {len(st):3d}")
    open(os.path.join(a.out, "ring-stroke.txt"), "w").write("\n".join(lines) + "\n")
    json.dump({"video": a.video, "thr": a.thr, "step": a.step, "rows": rows, "runs": runs, "hist": hist},
              open(os.path.join(a.out, "ring-stroke.json"), "w"), indent=1)
    for tag, v in (("thinnest", thin), ("thickest", thick)):
        if v is None: continue
        s, t, crop, cname = v
        big = cv2.resize(crop, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(os.path.join(a.out, "crops", f"{tag}-{stamp(t).replace(':', 'm')}-{cname}-{s:.1f}px.png"), big)
    print("\n".join(lines[-(len(runs) + 3):]))


if __name__ == "__main__":
    main()
