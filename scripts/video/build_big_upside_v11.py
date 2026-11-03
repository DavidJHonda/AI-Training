#!/usr/bin/env python3
"""Final v9 assembly with the lab bridge corrected from pristine video frames."""
import build_big_upside_v10 as repair

def configure():
    repair.OUT=repair.b.ROOT/'video-audit/big-upside-build-2026-11-03-v11'
    repair.DEST=repair.b.ROOT/'Prompts/big-upside-v11.mp4'
    repair.configure()

if __name__=='__main__':
    configure()
    repair.main()
