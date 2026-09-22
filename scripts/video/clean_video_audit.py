#!/usr/bin/env python3
"""Delete regenerable render scratch from video-audit/, keeping everything git tracks.

Why this exists (2026-09-21): video-audit reached 93 GB and filled the disk mid-build. Only 1.88 GB of
it is tracked in git - the actual record: REVIEW.md, edit-manifest.json, contact sheets, transition
strips, board state sheets, transcripts. The other 91 GB is render scratch that every build writes and
nothing ever removes, dominated by lossless FFV1 leg files at 76 GB.

What it removes (all gitignored, all regenerable by re-running the lesson's build script):
  leg-*.mkv     the composited board/graft legs, FFV1 lossless - by far the largest
  *.wav         source.wav, edited.wav, graft-*.wav
  canvas-*.png  upscaled board canvases
  *-live.mp4    copies of live videos made only so grade_bundle could scan them

It never touches a tracked file: every candidate is checked against `git ls-files` first, so the record
survives even if a pattern is widened later.

  clean_video_audit.py                 report what would be freed, delete nothing
  clean_video_audit.py --delete        delete it
  clean_video_audit.py --delete --only <substr> [...]   restrict to matching audit folders
  clean_video_audit.py --delete --skip <substr> [...]   leave a build that is still in flight alone
"""
from pathlib import Path
import argparse, subprocess, sys

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "video-audit"
PATTERNS = ("leg-*.mkv", "*.wav", "canvas-*.png", "*-live.mp4")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--delete", action="store_true", help="actually remove the files")
    ap.add_argument("--only", nargs="*", default=None, help="restrict to audit folders containing these substrings")
    ap.add_argument("--skip", nargs="*", default=None, help="leave these audit folders alone - use for a build still in flight, whose legs --render-existing still needs")
    args = ap.parse_args()

    tracked = set(subprocess.run(["git", "-C", str(ROOT), "ls-files", "video-audit"],
                                 capture_output=True, text=True, check=True).stdout.splitlines())

    hits, total, kept_tracked = [], 0, 0
    for pattern in PATTERNS:
        for f in AUDIT.rglob(pattern):
            rel = f.relative_to(ROOT).as_posix()
            if rel in tracked:            # never delete the record, whatever the pattern says
                kept_tracked += 1
                continue
            if args.only and not any(s in rel for s in args.only):
                continue
            if args.skip and any(s in rel for s in args.skip):
                continue
            try:
                size = f.stat().st_size      # skips dangling symlinks and files that vanish mid-walk
            except OSError:
                continue
            hits.append((size, f)); total += size

    hits.sort(reverse=True)
    by_folder = {}
    for size, f in hits:
        key = f.relative_to(AUDIT).parts[0]
        by_folder[key] = by_folder.get(key, 0) + size
    for folder, size in sorted(by_folder.items(), key=lambda kv: -kv[1])[:12]:
        print("  %8.2f GB  %s" % (size / 1073741824, folder))
    if len(by_folder) > 12:
        print("  %8s      ... and %d more folders" % ("", len(by_folder) - 12))

    print("\n%d files, %.2f GB%s" % (len(hits), total / 1073741824,
                                     "" if args.delete else " (dry run; pass --delete)"))
    if kept_tracked:
        print("%d tracked files skipped - the committed record is untouched" % kept_tracked)
    if not args.delete:
        return
    freed = 0
    for size, f in hits:
        try:
            f.unlink(); freed += size
        except OSError as e:
            print("  could not remove %s: %s" % (f, e), file=sys.stderr)
    print("Freed %.2f GB" % (freed / 1073741824))


if __name__ == "__main__":
    main()
