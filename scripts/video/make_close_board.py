#!/usr/bin/env python3
"""Prepare a full-frame close image for future video builds.

For --lesson, this uses the lesson's canonical white-background closing JPG—the
same asset shown on the course page—and centers it at its native 3x CSS scale on
a 3840x2160 video canvas. Existing finished videos are not rebuilt.

The legacy --pill mode remains available for one-off boards that are not course
lesson closings.

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
import os
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


INDEX = Path(__file__).resolve().parents[2] / "index.html"
ROOT = INDEX.parent


def close_board_copy(section_id):
    """Pill/sticky for a lesson, read straight out of index.html CLOSE_BOARDS.

    Hand-typing these into --pill/--sticky is how seven shipped closes ended up
    with STRAIGHT apostrophes where the app renders curly ones (caught
    2026-08-07, catalogue-wide audit). Typing the copy is the bug; quote the
    lesson id instead and the glyphs can never drift from the page.
    """
    import re
    src = INDEX.read_text(encoding="utf-8")
    m = re.search(r"CLOSE_BOARDS\s*=\s*\{(.*?)\n\};", src, re.S)
    if not m:
        sys.exit("could not locate CLOSE_BOARDS in index.html")
    row = re.search(
        r'\b%s:\s*\{\s*pill:\s*"(.*?)"\s*,\s*sticky:\s*"(.*?)"\s*\}' % re.escape(section_id),
        m.group(1))
    if not row:
        sys.exit(f"no CLOSE_BOARDS entry for '{section_id}'")
    return row.group(1), row.group(2)


def close_board_asset(section_id):
    """Read the canonical asset path from index.html's CLOSE_BOARD_ASSETS."""
    import re
    src = INDEX.read_text(encoding="utf-8")
    match = re.search(r"CLOSE_BOARD_ASSETS\s*=\s*\{(.*?)\n\};", src, re.S)
    if not match:
        sys.exit("could not locate CLOSE_BOARD_ASSETS in index.html")
    row = re.search(
        r'\b%s:\s*\{\s*src:\s*"([^"]+)"' % re.escape(section_id),
        match.group(1))
    if not row:
        sys.exit(f"no CLOSE_BOARD_ASSETS entry for '{section_id}'")
    asset_root = Path(os.environ.get("CLOSE_BOARD_ASSET_ROOT", ROOT))
    return asset_root / row.group(1)


def compose_canonical_for_video(source, output, bg):
    import cv2
    import numpy as np
    image = cv2.imread(str(source))
    if image is None:
        sys.exit(f"canonical closing image is missing: {source}")
    height, width = image.shape[:2]
    if width > 3840 or height > 2160:
        sys.exit(f"canonical closing image is too large for the video canvas: {width}x{height}")
    color = bg.lstrip("#")
    if len(color) != 6:
        sys.exit(f"invalid background color: {bg}")
    rgb = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
    # Scale the canonical JPG so its pill spans the house fraction of the frame (TARGET, the
    # same sizing the legacy renderer converged on), keeping the asset's own proportions. At
    # native size the 1206px page capture filled a third of the 4K frame (Why Learn AI v5,
    # 2026-09-16: the close came out at a third of the shipped v4's size).
    dark = (image.sum(axis=2) < 300); cols = dark.any(axis=0)
    if cols.any():
        x0, x1 = int(np.argmax(cols)), len(cols) - int(np.argmax(cols[::-1]))
        scale = TARGET * 3840 / (x1 - x0)
    else:
        scale = 1.0
    scale = min(scale, 3840 / width, 2160 / height)
    if abs(scale - 1.0) > 1e-3:
        image = cv2.resize(image, (round(width * scale), round(height * scale)), interpolation=cv2.INTER_CUBIC if scale > 1 else cv2.INTER_AREA)
        height, width = image.shape[:2]
    canvas = np.full((2160, 3840, 3), rgb[::-1], dtype=np.uint8)
    x = (3840 - width) // 2
    y = (2160 - height) // 2 - 60
    canvas[y:y + height, x:x + width] = image
    if not cv2.imwrite(str(output), canvas):
        sys.exit(f"could not write {output}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lesson", help="lesson id: take pill/sticky verbatim from "
                                     "index.html CLOSE_BOARDS (preferred — never retype copy)")
    ap.add_argument("--pill")
    ap.add_argument("--sticky", default="")
    ap.add_argument("--bg", default="#ffffff")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    if args.lesson:
        args.pill, args.sticky = close_board_copy(args.lesson)
        source = close_board_asset(args.lesson)
        compose_canonical_for_video(source, args.out, args.bg)
        print(f"canonical close from {source}\n  pill:   {args.pill}\n"
              f"  sticky: {args.sticky}\n  wrote:  {args.out}")
        return
    elif not args.pill:
        ap.error("either --lesson (preferred) or --pill is required")
    elif "'" in args.pill or "'" in args.sticky:
        print("WARNING: straight apostrophe (') in hand-typed copy — the app uses "
              "curly (\u2019). Use --lesson <id> to take the copy verbatim from the page.",
              file=sys.stderr)

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
