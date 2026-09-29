#!/usr/bin/env python3
"""Refresh generated uploads from gemini-notebook/upload-sets.json.

Each lesson owns its PROMPT.txt, assets/, and optional notes or alternate kits.
Only upload/, README.txt, and the root MANIFEST.json are generated. Never delete
an entire lesson folder or rewrite its prompt. Canonical teaching and boards stay
in lessons/ and course-assets/; Prompts/ holds raw rolls and review candidates.

Usage:
  .video-venv/bin/python scripts/video/sync_gemini_notebook.py
  .video-venv/bin/python scripts/video/sync_gemini_notebook.py --lesson fake-trap
  .video-venv/bin/python scripts/video/sync_gemini_notebook.py --check
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "gemini-notebook"
REGISTRY = OUT / "upload-sets.json"
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def lesson_hash(lesson):
    return hashlib.sha256(json.dumps(lesson, sort_keys=True).encode()).hexdigest()


def load():
    registry = json.loads(REGISTRY.read_text())
    lessons = registry["lessons"]
    slugs = [lesson["slug"] for lesson in lessons]
    dupes = {slug for slug in slugs if slugs.count(slug) > 1}
    if dupes:
        sys.exit(f"duplicate slugs in registry: {sorted(dupes)}")
    inactive = {item['slug'] for key in ('needs_preparation', 'retired_kits')
                for item in registry.get(key, [])}
    if inactive.intersection(slugs):
        sys.exit(f"inactive kits cannot be registered: {sorted(inactive.intersection(slugs))}")
    for lesson in lessons:
        slug = lesson["slug"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            sys.exit(f"invalid lesson slug: {slug!r}")
        if lesson["prompt"] != f"gemini-notebook/{slug}/PROMPT.txt":
            sys.exit(f"{slug}: prompt must be owned by its lesson folder (PROMPT.txt)")
        prompt = ROOT / lesson['prompt']
        if prompt.is_file():
            headings = ['REQUIRED VERBATIM AUDIO', 'TEACH THE COMPLETE LESSON',
                        'VOICE', 'BOARDS AND VISUALS']
            text = prompt.read_text()
            matches = [re.search(r'^' + heading + r'\s*$', text, re.MULTILINE)
                       for heading in headings]
            if not all(matches) or [m.start() for m in matches] != sorted(m.start() for m in matches):
                sys.exit(f"{slug}: legacy or incomplete prompt; rebuild under scripts/video/PREPARATION.md")
    return lessons


def sources(lesson):
    files = [lesson["markdown"], *lesson["uploads"]]
    for board in lesson.get("post_only", []):
        if board["asset"] in files:
            sys.exit(f"{lesson['slug']}: post-only board must not be uploaded: {board['asset']}")
        if board.get("covers") and board["covers"] not in lesson["uploads"]:
            sys.exit(f"{lesson['slug']}: missing upload stand-in: {board['covers']}")
    required = files + [lesson["prompt"]] + [p["asset"] for p in lesson.get("post_only", [])]
    for f in required:
        resolved = (ROOT / f).resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve())
        except ValueError:
            sys.exit(f"{lesson['slug']}: source must be inside the repository: {f}")
        if rel.parts[0] == 'gemini-notebook' and 'upload' in rel.parts:
            sys.exit(f"{lesson['slug']}: generated upload copies cannot be sources: {f}")
    missing = [f for f in required if not (ROOT / f).is_file()]
    if missing:
        sys.exit(f"{lesson['slug']}: missing source files: {missing}")
    names = [Path(f).name for f in files]
    if len(set(names)) != len(names):
        sys.exit(f"{lesson['slug']}: two uploads share a filename: {names}")
    d = OUT / lesson["slug"]
    for p in (d, d / "upload", d / "README.txt"):
        if p.is_symlink():
            sys.exit(f"{lesson['slug']}: refusing to replace symlink: {p}")
    return files


def readme_text(lesson, files):
    n = len(files)
    lines = [
        f"{lesson['title']} — what to do", "",
        f"1. Upload every file in upload/ ({WORDS.get(n, n)} files). Nothing else goes in as a source.",
        "2. Paste PROMPT.txt into the video customization box; do not upload it.",
        f"3. Save the roll as {lesson['save_as']} (or the next unused -reroll-N name).",
        "   Never overwrite a raw roll or the finished video.", "", "upload/ contains:",
    ]
    lines += [f"  {Path(f).name}    <- {f}" for f in files]
    post = lesson.get("post_only", [])
    if post:
        lines += ["", "Post-only boards (the edit inserts these; do not upload):"]
        for p in post:
            cover = f"; replaces {Path(p['covers']).name}" if p.get("covers") else ""
            lines.append(f"  {p['asset']} ({p['why']}{cover})")
    lines += [
        "", "PROMPT.txt, assets/, and any notes or alternate kits here are editable source material.",
        "Edit lesson text in lessons/ and canonical boards in course-assets/.",
        "This README and upload/ are generated from gemini-notebook/upload-sets.json.",
        "Run scripts/video/sync_gemini_notebook.py after changing sources or registry fields; use --check before generating.",
        "Do not upload README, notes, checklists, manifests, prompts, or lesson PDFs.",
        "The watermark toggle does not take effect; the build removes the mark.",
    ]
    if lesson.get("kit"):
        lines += ["", f"Scene directions and status: {lesson['kit']}."]
    if lesson.get("notes"):
        lines += ["", f"Status: {lesson['notes']}"]
    return "\n".join(lines) + "\n"


def build(lesson, manifest):
    files = sources(lesson)
    d = OUT / lesson["slug"]
    d.mkdir(parents=True, exist_ok=True)
    entries = []
    # Stage all copies before replacing only the generated upload directory.
    with tempfile.TemporaryDirectory(prefix=".upload-sync-", dir=d) as tmp:
        staged = Path(tmp) / "upload"
        staged.mkdir()
        for f in files:
            src = ROOT / f
            dst = staged / src.name
            shutil.copy2(src, dst)
            entries.append({"upload": str((d / "upload" / src.name).relative_to(ROOT)),
                            "source": f, "sha256": sha(dst)})
        if (d / "upload").exists():
            shutil.rmtree(d / "upload")
        staged.rename(d / "upload")
    (d / "README.txt").write_text(readme_text(lesson, files))
    prompt = ROOT / lesson["prompt"]
    manifest[lesson["slug"]] = {
        "files": entries,
        "prompt": {"source": lesson["prompt"], "sha256": sha(prompt), "words": len(prompt.read_text().split())},
        "post_only": [p["asset"] for p in lesson.get("post_only", [])],
        "registry_sha256": lesson_hash(lesson),
    }
    return len(files)


def check(lessons):
    mpath = OUT / "MANIFEST.json"
    if not mpath.exists():
        sys.exit("no gemini-notebook/MANIFEST.json yet; run without --check first")
    manifest = json.loads(mpath.read_text())["lessons"]
    drift = 0
    for lesson in lessons:
        files = sources(lesson)
        slug = lesson["slug"]
        m = manifest.get(slug)
        if not m:
            print(f"{slug}: not built yet"); drift += 1; continue
        if lesson_hash(lesson) != m.get("registry_sha256"):
            print(f"{slug}: registry changed since sync"); drift += 1
        if files != [e["source"] for e in m["files"]]:
            print(f"{slug}: registry upload list changed"); drift += 1
        for e in m["files"]:
            src = ROOT / e["source"]
            if not src.is_file() or sha(src) != e["sha256"]:
                print(f"{slug}: source missing or changed: {e['source']}"); drift += 1
            cp = ROOT / e["upload"]
            if not cp.is_file() or sha(cp) != e["sha256"]:
                print(f"{slug}: copy missing or altered: {e['upload']}"); drift += 1
        prompt = m["prompt"]
        if lesson["prompt"] != prompt["source"] or sha(ROOT / lesson["prompt"]) != prompt["sha256"]:
            print(f"{slug}: prompt changed since sync"); drift += 1
        upload = OUT / slug / "upload"
        if not upload.is_dir() or {p.name for p in upload.iterdir()} != {Path(f).name for f in files}:
            print(f"{slug}: upload folder contents differ from the registry"); drift += 1
        readme = OUT / slug / "README.txt"
        if not readme.is_file() or readme.read_text() != readme_text(lesson, files):
            print(f"{slug}: generated README missing or stale"); drift += 1
    print("OK: gemini-notebook/ matches its sources" if not drift else f"{drift} problem(s); run the sync")
    return 1 if drift else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lesson", help="only this registered slug")
    ap.add_argument("--check", action="store_true", help="report drift; change nothing")
    a = ap.parse_args()
    lessons = load()
    if a.lesson:
        lessons = [l for l in lessons if l["slug"] == a.lesson]
        if not lessons:
            registry = json.loads(REGISTRY.read_text())
            inactive = [item for key in ('needs_preparation', 'retired_kits')
                        for item in registry.get(key, []) if item['slug'] == a.lesson]
            if inactive:
                sys.exit(f"{a.lesson}: no usable prep kit. {inactive[0]['reason']}")
            sys.exit(f"unknown lesson {a.lesson}; see gemini-notebook/upload-sets.json")
    # Validate the complete selection before changing any generated bundle.
    for lesson in lessons:
        sources(lesson)
    if a.check:
        sys.exit(check(lessons))
    mpath = OUT / "MANIFEST.json"
    manifest = json.loads(mpath.read_text())["lessons"] if mpath.exists() else {}
    for lesson in lessons:
        n = build(lesson, manifest)
        print(f"{lesson['slug']:24s} {n} uploads; preserved PROMPT.txt, assets, and notes")
    mpath.write_text(json.dumps({"generated": datetime.datetime.now().isoformat(timespec="seconds"),
                                "registry": "gemini-notebook/upload-sets.json", "lessons": manifest}, indent=1) + "\n")


if __name__ == "__main__":
    main()
