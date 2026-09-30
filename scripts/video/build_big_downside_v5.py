#!/usr/bin/env python3
"""v5 refines the approved callback deletion after v4 retained a trailing 'is'.
Rebuild from the same hash-pinned finished source, not from v4.
"""
import build_big_downside_v4 as b

b.OUT=b.ROOT/'video-audit/big-downside-repair-2026-09-30-v5'
b.DEST=b.ROOT/'Prompts/big-downside-v5.mp4'
b.CUT_A,b.CUT_B=5413,5448
b.AUDIO_A,b.AUDIO_B=180+13/30,181.6
b.DROP=b.CUT_B-b.CUT_A
b.TOTAL=b.N-b.DROP
b.VOICE_B=5565-b.DROP
b.HISTORY_A,b.HISTORY_B=7538-b.DROP,7735-b.DROP
b.ONSETS=[4947,5061,5256,b.CUT_A]

if __name__=='__main__':b.main()
