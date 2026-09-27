#!/usr/bin/env python
"""Measure when each course board is on screen in a finished video.

Sequential decode only (seeks lie on these mp4s). Every --step seconds the frame
is matched against every board JPG with ORB features + RANSAC homography, which
survives the build's scaling, compact pushes, and dive-and-pan zooms. A frame
belongs to the board with the most inliers when that count clears --min-inliers.
Consecutive hits are merged into spans; gaps shorter than --gap seconds inside a
span are bridged (a ring change or a camera move can drop a sample or two).

Output: <out>/board-spans.txt with one line per span (board, start, end, length)
and a per-board total, plus <out>/board-spans.json.

Usage:
  .video-venv/bin/python scripts/video/board_spans.py course-assets/<slug>/<slug>.mp4 course-assets/<slug> video-audit/<review-dir> [--step 0.5]
      [--min-inliers 30] [--gap 1.5]
"""
import argparse, glob, json, os, sys
import cv2, numpy as np


def stamp(t):
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:05.2f}"


def prep(img, max_w=960):
    h, w = img.shape[:2]
    if w > max_w:
        img = cv2.resize(img, (max_w, int(h * max_w / w)), interpolation=cv2.INTER_AREA)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video"); ap.add_argument("boards_dir"); ap.add_argument("out")
    ap.add_argument("--step", type=float, default=0.5)
    ap.add_argument("--min-inliers", type=int, default=30)
    ap.add_argument("--gap", type=float, default=1.5)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    orb = cv2.ORB_create(nfeatures=2500, scaleFactor=1.2, nlevels=8)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    boards = {}
    for p in sorted(glob.glob(os.path.join(a.boards_dir, "*.jpg"))):
        name = os.path.basename(p)[:-4]
        g = prep(cv2.imread(p))
        kp, des = orb.detectAndCompute(g, None)
        if des is None or len(kp) < 50:
            print(f"skip {name}: {0 if des is None else len(kp)} features", file=sys.stderr); continue
        boards[name] = (kp, des)
    if not boards:
        sys.exit("no boards with features")

    cap = cv2.VideoCapture(a.video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    nframes = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = nframes / fps
    every = max(1, int(round(a.step * fps)))
    hits = []  # (t, board or None, inliers)
    i = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if i % every == 0:
            t = i / fps
            g = prep(frame)
            kp, des = orb.detectAndCompute(g, None)
            best, best_n = None, 0
            if des is not None and len(kp) >= 20:
                for name, (bkp, bdes) in boards.items():
                    m = bf.knnMatch(bdes, des, k=2)
                    good = [x[0] for x in m if len(x) == 2 and x[0].distance < 0.75 * x[1].distance]
                    if len(good) < a.min_inliers:
                        continue
                    src = np.float32([bkp[x.queryIdx].pt for x in good]).reshape(-1, 1, 2)
                    dst = np.float32([kp[x.trainIdx].pt for x in good]).reshape(-1, 1, 2)
                    H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
                    n = int(mask.sum()) if mask is not None else 0
                    if n > best_n:
                        best, best_n = name, n
            hits.append((t, best if best_n >= a.min_inliers else None, best_n))
        i += 1
    cap.release()

    # merge into spans, bridging short gaps of the same board
    spans = []
    cur = None
    for t, b, n in hits:
        if b is not None and cur and cur["board"] == b:
            cur["end"] = t + a.step; cur["samples"] += 1; cur["max"] = max(cur["max"], n); cur["last_hit"] = t
        elif b is not None and cur and cur["board"] != b and cur.get("last_hit", -9) >= t - a.gap and False:
            pass
        elif b is not None:
            if cur: spans.append(cur)
            cur = {"board": b, "start": t, "end": t + a.step, "samples": 1, "max": n, "last_hit": t}
        else:
            if cur and t - cur["last_hit"] > a.gap:
                spans.append(cur); cur = None
    if cur: spans.append(cur)
    # second pass: merge same-board spans separated by <= gap
    merged = []
    for s in spans:
        if merged and merged[-1]["board"] == s["board"] and s["start"] - merged[-1]["end"] <= a.gap:
            merged[-1]["end"] = s["end"]; merged[-1]["samples"] += s["samples"]; merged[-1]["max"] = max(merged[-1]["max"], s["max"])
        else:
            merged.append(dict(s))
    for s in merged:
        s["end"] = min(s["end"], duration); s["length"] = round(s["end"] - s["start"], 2)
        s.pop("last_hit", None)
    merged = [s for s in merged if s["samples"] >= 2]

    lines = [f"# {os.path.basename(a.video)}  duration={stamp(duration)}  step={a.step}s  min_inliers={a.min_inliers}",
             "# board                                   start     end       length   samples  max_inliers"]
    totals = {}
    for s in merged:
        lines.append(f"{s['board']:40s} {stamp(s['start']):>8}  {stamp(s['end']):>8}  {s['length']:6.1f}s  {s['samples']:4d}     {s['max']:4d}")
        totals[s["board"]] = totals.get(s["board"], 0) + s["length"]
    lines.append("")
    lines.append("# total seconds on screen per board (all spans):")
    for b, tot in sorted(totals.items(), key=lambda x: -x[1]):
        lines.append(f"  {b:40s} {tot:6.1f}s  ({100*tot/duration:4.1f}% of runtime)")
    boards_off = [b for b in boards if b not in totals]
    if boards_off:
        lines.append("# never detected: " + ", ".join(boards_off))
    txt = "\n".join(lines) + "\n"
    open(os.path.join(a.out, "board-spans.txt"), "w").write(txt)
    json.dump({"video": a.video, "duration": duration, "spans": merged}, open(os.path.join(a.out, "board-spans.json"), "w"), indent=1)
    print(txt)


if __name__ == "__main__":
    main()
