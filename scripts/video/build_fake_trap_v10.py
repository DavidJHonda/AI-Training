#!/usr/bin/env python3
"""Final shortening: prevent a three-frame deleted-scene flash before join two."""
import build_fake_trap_v9 as build
build.DEST=build.ROOT/'Prompts/fake-trap-v10.mp4'
build.OUT=build.ROOT/'video-audit/fake-trap-shorten-2026-09-30-v10'
build.FREEZES=[(6735,6738,6734)]
ROOT,OUT,DEST,CUTS=build.ROOT,build.OUT,build.DEST,build.CUTS
if __name__=='__main__':build.main()
