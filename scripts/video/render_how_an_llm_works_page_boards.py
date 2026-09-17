#!/usr/bin/env python3
"""Render the two former HTML-only How an LLM Works boards as canonical JPGs.

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
ASSETS = ROOT / "course-assets/how-an-llm-works"


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


ODDS = """
.odds-grid { display:grid; grid-template-columns:1fr 1fr; gap:2.6%; min-height:350px; }
.odds-panel { display:flex; flex-direction:column; min-width:0; border-radius:17px; background:#fff;
  overflow:hidden; box-shadow:0 8px 18px rgba(28,19,82,.08); }
.phrase { min-height:92px; margin:3.7% 5.2% 0; padding:3.5% 4%; display:flex; align-items:center;
  border-radius:12px; font:500 clamp(18px,1.908cqw,29px)/1.45 'Plus Jakarta Sans',sans-serif; color:#3a3550; }
.purple .phrase { background:#e5defe; border:2px solid #c8baf6; }
.teal .phrase { background:#e1f5f1; border:2px solid #b5ded8; }
.rows { flex:1; display:grid; grid-template-rows:repeat(4,minmax(54px,1fr)); padding:3.4% 5.2% 4.2%; }
.row { display:grid; grid-template-columns:minmax(82px,.85fr) 2.5fr 56px; align-items:center; gap:3.2%;
  border-bottom:1px solid #e5e2ed; }
.row:last-child { border-bottom:0; }
.word,.percent { font-size:clamp(18px,1.908cqw,29px); font-weight:700; color:#3a3550; }
.percent { text-align:right; }
.track { height:clamp(12px,1.447cqw,22px); border-radius:999px; background:#efedf4; overflow:hidden; }
.fill { height:100%; border-radius:inherit; }
.purple .fill { background:#4f2fc4; }
.teal .fill { background:#0e8f86; }
.teal .jelly .fill { background:#4f2fc4; }
.teal .jelly .word,.teal .jelly .percent { color:#4f2fc4; }
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
    odds = f"""<section class="board" aria-label="Same Word. Different Odds.">
      <h1>Same Word. Different Odds.</h1><div class="odds-grid">
      <section class="odds-panel purple"><div class="phrase">I’d like to buy peanut butter and _____.</div><div class="rows">
      <div class="row jelly"><div class="word">jelly</div><div class="track"><div class="fill" style="width:41%"></div></div><div class="percent">41%</div></div>
      <div class="row"><div class="word">bread</div><div class="track"><div class="fill" style="width:27%"></div></div><div class="percent">27%</div></div>
      <div class="row"><div class="word">bananas</div><div class="track"><div class="fill" style="width:16%"></div></div><div class="percent">16%</div></div>
      <div class="row"><div class="word">honey</div><div class="track"><div class="fill" style="width:5%"></div></div><div class="percent">5%</div></div></div></section>
      <section class="odds-panel teal"><div class="phrase">I’d like to buy a peanut butter and banana _____.</div><div class="rows">
      <div class="row"><div class="word">sandwich</div><div class="track"><div class="fill" style="width:54%"></div></div><div class="percent">54%</div></div>
      <div class="row"><div class="word">smoothie</div><div class="track"><div class="fill" style="width:16%"></div></div><div class="percent">16%</div></div>
      <div class="row"><div class="word">toast</div><div class="track"><div class="fill" style="width:9%"></div></div><div class="percent">9%</div></div>
      <div class="row jelly"><div class="word">jelly</div><div class="track"><div class="fill" style="width:2%"></div></div><div class="percent">2%</div></div></div></section></div>
      <div class="takeaway">{CHECK}<span>The surrounding words change the odds.</span></div>
      <div class="credit">besmarterthanthetool.com</div></section>"""
    prediction = f"""<section class="board" aria-label="One Word at a Time"><h1>One Word at a Time</h1>
      <div class="content">
      <div class="step"><div class="sentence">I want to buy peanut butter and</div><div class="result"><span class="predict-arrow">→</span><span class="new-word">jelly</span></div></div>
      <svg class="flow-arrow" viewBox="0 0 26 32"><path d="M2 16H23 M15 8L23 16L15 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="step"><div class="sentence">I want to buy peanut butter and <span class="prior">jelly</span></div><div class="result"><span class="predict-arrow">→</span><span class="new-word">for</span></div></div>
      <svg class="flow-arrow" viewBox="0 0 26 32"><path d="M2 16H23 M15 8L23 16L15 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="step"><div class="sentence">I want to buy peanut butter and jelly <span class="prior">for</span></div><div class="result"><span class="predict-arrow">→</span><span class="new-word">lunch</span></div></div></div>
      <div class="takeaway">{CHECK}<span>Add a word. Use the updated sentence. Predict again.</span></div>
      <div class="credit">besmarterthanthetool.com</div></section>"""
    (TMP / "same-word-different-odds.html").write_text(document(ODDS, odds))
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
    finish_one("same-word-different-odds", "how-an-llm-works-same-word-different-odds.jpg")
    finish_one("one-word-at-a-time", "how-an-llm-works-one-word-at-a-time.jpg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("prepare", "finish"))
    args = parser.parse_args()
    prepare() if args.stage == "prepare" else finish()
