#!/usr/bin/env python
"""Pull the candidate BOARDS out of a video: one representative frame per scene.

Built for the 2026-07-28 sweep asking "which boards did the engine draw itself,
that the lesson has no board for?". A board is a built, held, text-bearing panel,
so the useful frame is the one at the END of a scene (the engine animates builds,
so the last frame is the finished state) rather than a fixed-interval sample.

Sequential decode only -- CAP_PROP_POS_MSEC seeks return wrong frames on these
mp4s (see README). Scene cuts use the same 160x90 mean-abs-diff > 12 rule as
scenes.py; note that on slow pans over dense art this over-splits (a cut count is
NOT a strobe measure), which is harmless here: extra samples cost a tile, missed
ones cost a finding.

Frames are scored for text density (Canny edges in small horizontal runs, which
is what lettering looks like and what loose sketch linework does not) so sheets
lead with the likeliest boards. The score ranks, it never filters -- every scene
lands on a sheet.

Usage:
  .video-venv/bin/python scripts/video/board_scan.py videos/tokens.mp4 outdir
      [--min-hold 0.8] [--cols 2] [--rows 3]
"""
import argparse
import os
import sys

import cv2
import numpy as np


def text_score(frame):
    """Rough lettering density: edge pixels that sit in short horizontal runs."""
    g = cv2.cvtColor(cv2.resize(frame, (640, 360)), cv2.COLOR_BGR2GRAY)
    e = cv2.Canny(g, 80, 200)
    # Lettering = many short horizontal edge runs. Dilating horizontally then
    # differencing suppresses long continuous strokes (panel borders, sketch arcs).
    wide = cv2.dilate(e, np.ones((1, 9), np.uint8))
    short_runs = cv2.erode(wide, np.ones((1, 25), np.uint8))
    return float((e > 0).mean() - (short_runs > 0).mean() * 0.5) * 1000


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("outdir")
    ap.add_argument("--threshold", type=float, default=12.0)
    ap.add_argument("--min-hold", type=float, default=0.8,
                    help="ignore scenes shorter than this (transition flicker)")
    ap.add_argument("--cols", type=int, default=2)
    ap.add_argument("--rows", type=int, default=3)
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    os.makedirs(args.outdir, exist_ok=True)

    # Pass 1: sequential decode, keeping the last frame of every scene.
    picks, prev, idx, scene_start, last = [], None, 0, 0, None
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        small = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY).astype("int32")
        if prev is not None and abs(small - prev).mean() > args.threshold:
            if last is not None and (idx - scene_start) / fps >= args.min_hold:
                picks.append((scene_start / fps, idx / fps, last))
            scene_start = idx
        prev, last, idx = small, frame.copy(), idx + 1
    if last is not None and (idx - scene_start) / fps >= args.min_hold:
        picks.append((scene_start / fps, idx / fps, last))
    cap.release()

    # Drop consecutive near-duplicates (a slow pan reads as many scenes).
    kept, prev_small = [], None
    for a, b, f in picks:
        s = cv2.cvtColor(cv2.resize(f, (160, 90)), cv2.COLOR_BGR2GRAY).astype("int32")
        if prev_small is not None and abs(s - prev_small).mean() < 4.0:
            continue
        kept.append((a, b, f))
        prev_small = s

    TW, TH = 640, 360
    per = args.cols * args.rows
    for n in range(0, len(kept), per):
        chunk = kept[n:n + per]
        sheet = np.full((TH * args.rows, TW * args.cols, 3), 255, np.uint8)
        for i, (a, b, f) in enumerate(chunk):
            tile = cv2.resize(f, (TW, TH))
            label = f"{int(a)//60}:{int(a)%60:02d}-{int(b)//60}:{int(b)%60:02d}  t{text_score(f):.0f}"
            cv2.rectangle(tile, (0, 0), (250, 26), (255, 255, 255), -1)
            cv2.putText(tile, label, (6, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 220), 2)
            r, c = divmod(i, args.cols)
            sheet[r * TH:(r + 1) * TH, c * TW:(c + 1) * TW] = tile
        out = os.path.join(args.outdir, f"sheet{n // per + 1:02d}.jpg")
        cv2.imwrite(out, sheet, [cv2.IMWRITE_JPEG_QUALITY, 86])
    print(f"{os.path.basename(args.input)}: {len(kept)} scene picks -> "
          f"{(len(kept) + per - 1) // per} sheet(s) in {args.outdir}")


if __name__ == "__main__":
    main()
