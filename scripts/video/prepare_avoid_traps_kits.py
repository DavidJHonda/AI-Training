#!/usr/bin/env python3
"""Sync Avoid Traps video JPGs to current lesson assets and record provenance.

Run --sync --render-closes after exporting the nine lesson Markdown files.
Run --archive-obsolete after inspecting the resulting manifest and contact sheets.
No live lesson, illustration, or video is changed. Old unused lesson JPGs move to
archive/video-materials/avoid-traps-2026-09-04, with a recoverable move manifest.
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "archive/video-materials/avoid-traps-2026-09-04"
REPORT = ROOT / "Prompts/AVOID-TRAPS-SOURCE-MANIFEST.json"
# Entries: video filename suffix, current page asset, safe for Notebook upload.
KITS = [
    ("opener-avoid", "openerprotect", "Opener-Avoid", [
        ("1-traps", None, True),
        ("2-read-water", "opener-avoid-editorial-v2.jpg", False),
        ("3-map", "opener-avoid-section-map.jpg", True),
        ("4-close", "close", True),
    ]),
    ("hallucination", "hallucination", "hallucination", [
        ("1-example", "hallucination-example-v2.jpg", True),
        ("2-why", "hallucination-why-v2.jpg", True),
        ("3-real-text", "hallucination-real-text-v2.jpg", False),
        ("4-close", "close", True),
    ]),
    ("training-bias", "trainingbias", "training-bias", [
        ("1-wrong-pattern", "training-bias-pattern-v2.jpg", False),
        ("2-mechanisms", "training-bias-mechanisms-v2.jpg", True),
        ("3-questions", "training-bias-questions-v2.jpg", True),
        ("4-stale", "training-bias-stale-chat-v2.jpg", True),
        ("5-rag", "training-bias-rag-v2.jpg", True),
        ("6-close", "close", True),
    ]),
    ("document-trap", "documenttrap", "document-trap", [
        ("1-uploaded", "document-trap-uploaded-v2.jpg", False),
        ("2-flow", "document-trap-flow-v2.jpg", True),
        ("3-moves", "document-trap-moves-v2.jpg", True),
        ("4-close", "close", True),
    ]),
    ("mind-trap", "mindtrap", "mind-trap", [
        ("1-comparison", "mind-trap-comparison-v2.jpg", False),
        ("2-eliza", "mind-trap-eliza-effect-v2.jpg", True),
        ("3-close", "close", True),
    ]),
    ("flattery-trap", "flattery", "flattery-trap", [
        ("1-comparison", "flattery-trap-comparison-v2.jpg", False),
        ("2-praise-loop", "flattery-trap-praise-loop-v2.jpg", True),
        ("3-sycophancy", "flattery-trap-sycophancy-v2.jpg", True),
        ("4-five-moves", "flattery-trap-five-moves-v2.jpg", True),
        ("5-close", "close", True),
    ]),
    ("engagement-trap", "engagementtrap", "engagement-trap", [
        ("1-comparison", "engagement-trap-comparison-v2.jpg", True),
        ("2-scroll", "engagement-trap-scroll-v2.jpg", True),
        ("3-stop", "engagement-trap-stop-v2.jpg", False),
        ("4-close", "close", True),
    ]),
    ("support-trap", "supporttrap", "support-trap", [
        ("1-comparison", "support-trap-comparison-v2.jpg", False),
        ("2-role", "support-trap-real-vs-missing-v2.jpg", True),
        ("3-danger", "support-trap-danger-v2.jpg", True),
        ("4-close", "close", True),
    ]),
    ("fake-trap", "faketrap", "fake-trap", [
        ("1-comparison", "fake-trap-comparison-v2.jpg", False),
        ("2-reasons", "fake-trap-four-reasons-v3.png", True),
        ("3-source", "fake-trap-source-v2.jpg", False),
        ("4-checks", "fake-trap-three-checks-v2.jpg", True),
        ("5-close", "close", True),
    ]),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def backup(path):
    if path.exists():
        target = ARCHIVE / "replaced" / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            shutil.copy2(path, target)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sync", action="store_true")
    ap.add_argument("--render-closes", action="store_true")
    ap.add_argument("--archive-obsolete", action="store_true")
    args = ap.parse_args()
    html = (ROOT / "index.html").read_text()
    rows, canonical, panels = [], set(), []
    for slug, section, md, boards in KITS:
        prompt = ROOT / f"Prompts/{slug}-video-prompt.txt"
        markdown = ROOT / f"lessons/{md}.md"
        entry = {"lesson": slug, "section_id": section,
                 "markdown": str(markdown.relative_to(ROOT)),
                 "markdown_sha256": sha(markdown),
                 "prompt": str(prompt.relative_to(ROOT)),
                 "prompt_words": len(prompt.read_text().split()), "boards": []}
        for suffix, source_name, upload in boards:
            target = ROOT / f"lessons/{slug}-{suffix}.jpg"
            canonical.add(target)
            source = ROOT / "illustrations" / source_name if source_name not in (None, "close") else None
            if source:
                assert str(source.relative_to(ROOT)) in html, f"Not used on page: {source}"
                assert source.is_file(), source
                if args.sync and (source.suffix.lower() != ".jpg" or not target.exists() or sha(source) != sha(target)):
                    backup(target)
                    if source.suffix.lower() == ".jpg":
                        shutil.copy2(source, target)
                    else:
                        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "94", str(source), "--out", str(target)], check=True, capture_output=True)
            if source_name == "close" and args.render_closes:
                backup(target)
                with tempfile.TemporaryDirectory(prefix="avoid-close-") as temp:
                    png = Path(temp) / "close.png"
                    subprocess.run([sys.executable, str(ROOT / "scripts/video/make_close_board.py"), "--lesson", section, "--out", str(png)], check=True)
                    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", str(png), "--out", str(target)], check=True, capture_output=True)
            assert target.is_file(), target
            if upload:
                assert target.name in prompt.read_text(), f"Upload board missing from prompt: {target.name}"
            else:
                assert target.name in (ROOT / "Prompts/AVOID-TRAPS-VIDEO-KITS.md").read_text(), f"Post-only board missing from checklist: {target.name}"
            with Image.open(target) as im:
                im.verify()
            im = Image.open(target).convert("RGB")
            item = {"file": str(target.relative_to(ROOT)), "notebook_upload": upload,
                    "source": str(source.relative_to(ROOT)) if source else (f"index.html:CLOSE_BOARDS.{section}" if source_name == "close" else "index.html:OpenerProtectSection/OpenerCreed"),
                    "sha256": sha(target), "width": im.width, "height": im.height}
            if source:
                item["source_sha256"] = sha(source)
                item["source_match"] = "byte-identical" if sha(source) == sha(target) else "PNG-to-JPEG, same dimensions"
                assert im.size == Image.open(source).size
                if source.suffix == ".jpg":
                    assert sha(source) == sha(target), f"Stale JPG: {target}"
            if source_name == "close":
                item["pill"], item["sticky"] = close_board_copy(section)
                assert item["pill"] in markdown.read_text() and item["sticky"] in markdown.read_text(), f"Close text drift: {slug}"
            entry["boards"].append(item)
            panel = Image.new("RGB", (640, 470), "#eeeeee")
            im.thumbnail((620, 420))
            panel.paste(im, ((640-im.width)//2, 45))
            ImageDraw.Draw(panel).text((12, 8), target.name, fill="black")
            ImageDraw.Draw(panel).text((12, 24), "UPLOAD" if upload else "POST ONLY - VISIBLE FACES", fill="black" if upload else "red")
            panels.append(panel)
        assert entry["prompt_words"] <= 500, f"Prompt over 500 words: {slug}"
        rows.append(entry)
    obsolete, retained = [], []
    prefixes = tuple(x[0] + "-" for x in KITS) + ("avoid-traps-",)
    for path in sorted((ROOT / "lessons").iterdir()):
        if path.suffix.lower() not in (".jpg", ".jpeg", ".png") or not path.name.startswith(prefixes) or path in canonical:
            continue
        if path.name in html:
            retained.append(str(path.relative_to(ROOT)))
            continue
        destination = ARCHIVE / "obsolete" / "lessons" / path.name
        obsolete.append({"from": str(path.relative_to(ROOT)), "to": str(destination.relative_to(ROOT)), "sha256": sha(path)})
        if args.archive_obsolete:
            destination.parent.mkdir(parents=True, exist_ok=True)
            assert not destination.exists(), destination
            shutil.move(str(path), str(destination))
    move_manifest = ARCHIVE / "MOVED-FILES.json"
    moved = json.loads(move_manifest.read_text()) if move_manifest.exists() else []
    if args.archive_obsolete and obsolete:
        moved.extend(obsolete)
        move_manifest.write_text(json.dumps(moved, indent=2)+"\n")
    REPORT.write_text(json.dumps({"prepared": "2026-09-04", "authority": "index.html and its current referenced illustrations", "lessons": rows, "obsolete_candidates": [] if args.archive_obsolete else obsolete, "archived_obsolete": moved, "retained_page_dependencies": retained}, ensure_ascii=False, indent=2)+"\n")
    qa = Path("/private/tmp/avoid-traps-kit-review")
    qa.mkdir(exist_ok=True)
    for start in range(0, len(panels), 6):
        sheet = Image.new("RGB", (1280, 1410), "white")
        for i, panel in enumerate(panels[start:start+6]):
            sheet.paste(panel, ((i%2)*640, (i//2)*470))
        sheet.save(qa / f"sheet-{start//6+1:02}.jpg", quality=92)
    print(json.dumps({"lessons":len(rows), "boards":len(canonical), "upload":sum(b[2] for k in KITS for b in k[3]), "post_only":sum(not b[2] for k in KITS for b in k[3]), "obsolete":len(obsolete), "retained_page_dependencies":retained, "contact_sheets":str(qa)}))


if __name__ == "__main__":
    main()
