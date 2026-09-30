#!/usr/bin/env python3
"""Final tightening: hold before even the first native red-outline pixel."""
import build_support_trap_v12 as edit
edit.b.OUT=edit.b.ROOT/'video-audit/support-trap-tighten-2026-09-30-v13'
edit.b.DEST=edit.b.ROOT/'Prompts/support-trap-v13.mp4'
edit.HOLD_A=3840
if __name__=='__main__':edit.main()
