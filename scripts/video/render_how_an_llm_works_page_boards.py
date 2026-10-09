#!/usr/bin/env python3
"""Render the current One Word at a Time board as a canonical JPG.

The former numerical-odds board was retired by the owner on 2026-10-08.

The markup and CSS below preserve the approved page rendering at a 1600px
native board width. Chrome creates lossless captures; Pillow crops the board
geometry and writes the course JPGs without resampling.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
TMP = Path("/private/tmp/how-an-llm-works-page-boards")
FONT = ROOT / "scripts/video/assets/fonts/PlusJakartaSans-wght.ttf"
ASSETS = ROOT / "course-assets/whats-an-llm"


SHARED = f"""
@font-face {{ font-family:'Plus Jakarta Sans'; src:url('file://{FONT}') format('truetype'); font-weight:100 900; }}
* {{ box-sizing:border-box; }}
html,body {{ margin:0; width:880px; min-height:1200px; background:#fff; }}
body {{ overflow:hidden; }}
.board {{ position:relative; box-sizing:border-box; width:880px; padding:2.5%; border-radius:22px;
  background:#eae7fd; color:#0e0a1f; font-family:'Plus Jakarta Sans',sans-serif; overflow:hidden; }}
.board h1 {{ margin:0 0 2.6%; font-size:clamp(28px,3.684cqw,56px); line-height:1.04; letter-spacing:-.03em; font-weight:700; }}
.takeaway {{ min-height:0; margin-top:2.6%; border-radius:10px; display:flex; justify-content:center; align-items:center;
  gap:clamp(12px,1.579cqw,24px); padding:clamp(10px,1.447cqw,22px) 16px; background:#ffe39a;
  font-size:clamp(18px,2.105cqw,32px); line-height:1.4; font-weight:500; text-align:center; }}
.check {{ flex:0 0 auto; width:clamp(22px,2.895cqw,44px); height:clamp(22px,2.895cqw,44px); border-radius:50%; display:grid; place-items:center;
  color:#fff; background:#4f2fc4; }}
.check svg {{ width:65%; height:65%; display:block; }}
.credit {{ position:absolute; right:22px; bottom:5.5px; color:#625c7a; font-size:11px; font-weight:500; line-height:1; }}
"""




PREDICTION = """
.board { border-radius:20px; }
.board h1 { line-height:1.2; margin-bottom:26px; }
.content { display:grid; grid-template-columns:minmax(0,1fr) 26px minmax(0,1fr) 26px minmax(0,1fr);
  gap:12px; align-items:stretch; }
.step { background:#fff; border-radius:14px; padding:26px 22px; display:flex; flex-direction:column;
  justify-content:space-between; gap:26px; }
.sentence,.result { font-size:clamp(18px,1.908cqw,29px); font-weight:500; line-height:1.45; color:#3a3550; }
.result { display:flex; align-items:center; gap:12px; }
.flow-arrow { align-self:center; width:26px; height:32px; color:#4f2fc4; }
.prior,.predict-arrow { color:#4f2fc4; font-weight:700; }
.new-word { display:inline-block; color:#fff; background:#4f2fc4; padding:3px 14px; border-radius:9px;
  font-weight:700; line-height:1.5; }
.takeaway { margin-top:22px; }
"""


CHECK = """<span class="check" aria-hidden="true"><svg viewBox="0 0 32 32"><path d="M5 16L12 23L27 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>"""


def document(css: str, body: str) -> str:
    return f"<!doctype html><html><head><meta charset='utf-8'><style>{SHARED}{css}</style></head><body>{body}</body></html>"


def prepare() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    prediction = f"""<section class="board" aria-label="One Word at a Time"><h1>One Word at a Time</h1>
      <div class="content">
      <div class="step"><div class="sentence">I want to buy peanut butter and</div><div class="result"><span class="predict-arrow">→</span><span class="new-word">jelly</span></div></div>
      <svg class="flow-arrow" viewBox="0 0 26 32"><path d="M2 16H23 M15 8L23 16L15 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="step"><div class="sentence">I want to buy peanut butter and <span class="prior">jelly</span></div><div class="result"><span class="predict-arrow">→</span><span class="new-word">for</span></div></div>
      <svg class="flow-arrow" viewBox="0 0 26 32"><path d="M2 16H23 M15 8L23 16L15 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="step"><div class="sentence">I want to buy peanut butter and jelly <span class="prior">for</span></div><div class="result"><span class="predict-arrow">→</span><span class="new-word">lunch</span></div></div></div>
      <div class="takeaway">{CHECK}<span>Add a word. Use the updated sentence. Predict again.</span></div>
      <div class="credit">besmarterthanthetool.com</div></section>"""
    (TMP / "one-word-at-a-time.html").write_text(document(PREDICTION, prediction))
    print(TMP)


def finish_one(stem: str, filename: str) -> None:
    source = TMP / f"{stem}.png"
    image = Image.open(source).convert("RGB")
    center = image.width // 2
    bottom = max(y for y in range(image.height) if image.getpixel((center, y)) != (255, 255, 255)) + 1
    board = image.crop((0, 0, 1600, bottom))
    target = ASSETS / filename
    board.save(target, "JPEG", quality=95, subsampling=0, optimize=True)
    print(f"{target.relative_to(ROOT)} {board.width}x{board.height} {target.stat().st_size} bytes")


def finish() -> None:
    finish_one("one-word-at-a-time", "whats-an-llm-one-word-at-a-time.jpg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "finish"))
    args = parser.parse_args()
    prepare() if args.stage == "prepare" else finish()
