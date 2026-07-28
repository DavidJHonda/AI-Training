#!/usr/bin/env python
"""Rank a video's scenes by how much each looks like a FLAT-UI BOARD.

The 2026-07-28 sweep needs the engine's drawn *boards* separated from its drawn
*b-roll*. In this catalogue the two look nothing alike:

  board   near-white / pale-lavender ground, crisp thin sans text, rounded-rect
          cards, almost no saturated colour, no paper grain
  b-roll  marker and watercolour art, saturated pigment, visible paper texture,
          thick ink linework

So the discriminator is: how much of the frame is bright AND desaturated, times
how much crisp small-scale text-like edge sits on top of it. Both are cheap.

This RANKS, it does not decide -- output is a contact sheet ordered best-first so
the boards are read in the first sheet or two instead of hunting through five.
Scenes below --floor are still written, to a separate `rest` sheet, because a
missed board costs a finding and a wrong tile costs nothing.

Sequential decode only (CAP_PROP_POS_MSEC seeks lie on these mp4s).

Usage:
  .video-venv/bin/python scripts/video/board_filter.py videos/tokens.mp4 outdir
"""
import argparse
import os
import sys

import cv2
import numpy as np


def board_score(frame):
    small = cv2.resize(frame, (640, 360))
    hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
    sat, val = hsv[:, :, 1].astype(float) / 255, hsv[:, :, 2].astype(float) / 255
    # Flat pale ground: bright and nearly grey.
    pale = ((val > 0.80) & (sat < 0.18)).mean()
    # Crisp fine detail (text) rather than thick ink strokes: Canny edges that
    # survive at full scale but vanish under a 3x3 blur are small-scale marks.
    g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    fine = cv2.Canny(g, 100, 220)
    coarse = cv2.Canny(cv2.GaussianBlur(g, (5, 5), 0), 100, 220)
    crisp = max(0.0, (fine > 0).mean() - (coarse > 0).mean())
    # Paper grain / pigment texture kills it: high local variance in the ground.
    grain = float(cv2.Laplacian(g, cv2.CV_64F).var())
    return pale * 100 + crisp * 900 - min(grain / 60.0, 25.0)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("outdir")
    ap.add_argument("--threshold", type=float, default=12.0)
    ap.add_argument("--min-hold", type=float, default=0.8)
    ap.add_argument("--floor", type=float, default=28.0, help="board-score cutoff")
    ap.add_argument("--cols", type=int, default=2)
    ap.add_argument("--rows", type=int, default=4)
    args = ap.parse_args()

    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        sys.exit(f"cannot open {args.input}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    os.makedirs(args.outdir, exist_ok=True)

    picks, prev, idx, scene_start, last = [], None, 0, 0, None
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        s = cv2.cvtColor(cv2.resize(frame, (160, 90)), cv2.COLOR_BGR2GRAY).astype("int32")
        if prev is not None and abs(s - prev).mean() > args.threshold:
            if last is not None and (idx - scene_start) / fps >= args.min_hold:
                picks.append((scene_start / fps, idx / fps, last))
            scene_start = idx
        prev, last, idx = s, frame.copy(), idx + 1
    if last is not None and (idx - scene_start) / fps >= args.min_hold:
        picks.append((scene_start / fps, idx / fps, last))
    cap.release()

    kept, prev_small = [], None
    for a, b, f in picks:
        s = cv2.cvtColor(cv2.resize(f, (160, 90)), cv2.COLOR_BGR2GRAY).astype("int32")
        if prev_small is not None and abs(s - prev_small).mean() < 4.0:
            continue
        kept.append((a, b, f, board_score(f)))
        prev_small = s

    hits = sorted([k for k in kept if k[3] >= args.floor], key=lambda k: -k[3])
    rest = sorted([k for k in kept if k[3] < args.floor], key=lambda k: -k[3])

    TW, TH, per = 640, 360, args.cols * args.rows
    def emit(items, tag):
        for n in range(0, len(items), per):
            chunk = items[n:n + per]
            sheet = np.full((TH * args.rows, TW * args.cols, 3), 255, np.uint8)
            for i, (a, b, f, sc) in enumerate(chunk):
                tile = cv2.resize(f, (TW, TH))
                lab = f"{int(a)//60}:{int(a)%60:02d}-{int(b)//60}:{int(b)%60:02d} s{sc:.0f} {int(b-a)}s"
                cv2.rectangle(tile, (0, 0), (300, 26), (255, 255, 255), -1)
                cv2.putText(tile, lab, (6, 19), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 220), 2)
                r, c = divmod(i, args.cols)
                sheet[r*TH:(r+1)*TH, c*TW:(c+1)*TW] = tile
            cv2.imwrite(os.path.join(args.outdir, f"{tag}{n//per+1:02d}.jpg"), sheet,
                        [cv2.IMWRITE_JPEG_QUALITY, 86])
    emit(hits, "board")
    emit(rest, "rest")
    print(f"{os.path.basename(args.input)}: {len(hits)} board-like / {len(kept)} scenes")


if __name__ == "__main__":
    main()
