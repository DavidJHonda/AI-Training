#!/usr/bin/env python3
"""Unexpected Results v1 (2026-09-24): roll 2's two road animations without their label boxes.

Roll 2 source frames 4225-5256 (2:20.8-2:55.2) carry Notebook's road drawings under the road-pattern beat, and
label boxes with jargon and invented figures above and below them ("THE CAPACITY PARADOX | Induced Demand",
"Supply: 4 Lanes (2x Doubled)", "RESULT: Capacity Doubled", "Katy Freeway widened to 26 lanes", the Houston
"+100,000 residents" card). The paper stage is the same static texture in every frame, so everything outside the
road itself is replaced by the same pixels from one of the roll's own blank paper frames (4950; 4800 carries a speck) for both
animations. Cars and lanes are untouched. The corner mark is cleaned later by the render.

Writes <out>/road-patched.mkv (FFV1), frame k = roll 2 source frame 4225 + k.
"""
from pathlib import Path
import subprocess, sys
import cv2, numpy as np, imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/unexpected-results-2.mp4"
START, END = 4225, 5256
ROAD1_ROWS = (290, 646)          # first animation: full-width road band incl. its yellow edges (measured 4380-4760)
ROAD2_BOX = (148, 244, 1132, 528)  # second animation: dark lane box at its largest (measured 5000-5250)
BLANK1, BLANK2, SWITCH = 4950, 4950, 4966


def main(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(SRC)); frames = {}; i = -1
    while i + 1 < END:
        ok, im = cap.read(); assert ok, i; i += 1
        if i >= START or i in (BLANK1, BLANK2): frames[i] = im
    b1, b2 = frames[BLANK1], frames[BLANK2]
    ff = imageio_ffmpeg.get_ffmpeg_exe(); dst = out / "road-patched.mkv"
    p = subprocess.Popen([ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1280x720", "-r", "30",
                          "-i", "pipe:0", "-c:v", "ffv1", "-level", "3", str(dst)], stdin=subprocess.PIPE)
    resid = []
    for f in range(START, END):
        im = frames[f]
        if f < SWITCH:
            o = b1.copy(); y0, y1 = ROAD1_ROWS; o[y0:y1] = im[y0:y1]
        else:
            o = b2.copy(); x0, y0, x1, y1 = ROAD2_BOX; o[y0:y1, x0:x1] = im[y0:y1, x0:x1]
        if f in (4300, 4600, 5100):   # seam check: paper just outside the kept region should match the blank frame
            resid.append((f, float(np.abs(im[700:716, :1100].astype(int) - o[700:716, :1100].astype(int)).mean())))
        p.stdin.write(o.tobytes())
    p.stdin.close(); assert p.wait() == 0
    print(dst, "paper residual (mean abs, bottom band):", resid)


if __name__ == "__main__":
    main(sys.argv[1])
