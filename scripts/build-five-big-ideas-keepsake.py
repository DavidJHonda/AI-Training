#!/usr/bin/env python3
"""Locate retained finished artwork.

The owner approved removing the intermediate artwork on 2026-09-15.
Finished boards are now the source of truth; this legacy entry point verifies
and reports them without rebuilding or re-encoding them.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FINISHED = ['course-assets/finish-smarter-opener/finish-smarter-opener-five-big-ideas.jpg', 'packets/finish-smarter-opener-five-big-ideas.pdf']

def main():
    for relative in FINISHED:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(f"Missing finished artwork: {path}")
        print(path)

if __name__ == "__main__":
    main()
