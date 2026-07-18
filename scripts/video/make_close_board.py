#!/usr/bin/env python3
"""Render a full-scale close board png for the Ken Burns close treatment
(owner standard 2026-07-18; first shipped: tokens, then the composed-close
retrofit). Reproduces the app's CloseBoard (index.html) at 3840x2160 — 3x of
frame size, so zoompan up to 1.2x never upscales — with the pill auto-sized
toward the NotebookLM native close scale (pill ~56% of frame width, measured
from the transformer close). Short pill texts hit the font cap first and land
narrower, matching how the engine renders its own short closes (which-app).

Usage:
  .video-venv/bin/python scripts/video/make_close_board.py \
      --pill "A token ID is an address, not a meaning." \
      --sticky "Turning that number into meaning comes next." \
      --bg "#f6f5fb" --out board.png

Then Ken Burns it over the close span (N = span frames, integer-tick pts —
fractional pts drop a frame at concat):
  [1:v]zoompan=z='1+0.2*on/(N-1)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'
      :d=N:s=1280x720:fps=30,format=yuv420p,setsar=1,setpts=N/(30*TB)
"""
import argparse
import html
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TARGET = 0.563          # pill width as fraction of frame width (transformer scale)
BASE_FONT = 101         # 3x px; all other measurements scale with font/BASE_FONT
FONT_MIN, FONT_MAX = 76, 156

PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<style>
  html,body {{ margin:0; padding:0; }}
  body {{ width:3840px; height:2160px; background:{bg};
    font-family:"Plus Jakarta Sans",sans-serif; box-sizing:border-box;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    padding-bottom:120px; }}
  .pill {{ background:#252a33; color:#fff; border-radius:999px;
    padding:{pill_pad_v}px {pill_pad_h}px; font-size:{pill_font}px; font-weight:800;
    letter-spacing:-0.02em; line-height:1.3; text-align:center; }}
  .sticky {{ margin-top:{gap}px; background:#f9eda6; color:#4a4426;
    transform:rotate(-2.5deg); padding:{st_pad_v}px {st_pad_h}px;
    font-size:{st_font}px; font-weight:600; font-style:italic;
    box-shadow:0 40px 96px rgba(14,10,31,0.10); text-align:center; line-height:1.45; }}
</style></head>
<body><div class="pill">{pill}</div>{sticky_div}</body></html>
"""


def render(font, args, out_png):
    r = font / BASE_FONT
    sticky_div = ""
    if args.sticky:
        sticky_div = f'<div class="sticky">{html.escape(args.sticky)}</div>'
    doc = PAGE.format(
        bg=args.bg, pill=html.escape(args.pill), sticky_div=sticky_div,
        pill_font=round(font), pill_pad_v=round(72 * r), pill_pad_h=round(150 * r),
        gap=round(88 * r), st_font=round(68 * r),
        st_pad_v=round(49 * r), st_pad_h=round(104 * r))
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(doc)
        page = f.name
    subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                    "--window-size=3840,2160", "--hide-scrollbars",
                    "--virtual-time-budget=8000",
                    f"--screenshot={out_png}", f"file://{page}"],
                   check=True, capture_output=True)
    Path(page).unlink()


def pill_frac(png):
    import cv2
    import numpy as np
    img = cv2.imread(png)
    dark = (img.sum(axis=2) < 300)
    cols = dark.any(axis=0)
    if not cols.any():
        sys.exit("no pill found in render")
    x0, x1 = int(np.argmax(cols)), len(cols) - int(np.argmax(cols[::-1]))
    return (x1 - x0) / img.shape[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pill", required=True)
    ap.add_argument("--sticky", default="")
    ap.add_argument("--bg", default="#f6f5fb")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    font = BASE_FONT
    for i in range(3):
        render(font, args, args.out)
        frac = pill_frac(args.out)
        capped = font in (FONT_MIN, FONT_MAX)
        print(f"pass {i + 1}: font={font} pill={frac * 100:.1f}%"
              + (" (font cap)" if capped else ""))
        if 0.53 <= frac <= 0.585 or capped:
            break
        font = min(max(round(font * TARGET / frac), FONT_MIN), FONT_MAX)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
