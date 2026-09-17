#!/usr/bin/env python3
"""Locate retained finished artwork.

The owner approved removing the intermediate artwork on 2026-09-15.
Finished boards are now the source of truth; this legacy entry point verifies
and reports them without rebuilding or re-encoding them.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FINISHED = ['course-assets/understand-ai-opener/understand-ai-opener-under-hood.jpg']

def main():
    for relative in FINISHED:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(f"Missing finished artwork: {path}")
        print(path)

if __name__ == "__main__":
    main()
