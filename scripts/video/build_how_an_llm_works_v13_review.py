#!/usr/bin/env python3
"""V12 QA correction: start numerical donor after its prior labels vanish.

V12 remains untouched as a rejected intermediate. Still copy v11 AAC and
rebuild pristine visuals; output interval and all other treatment stay fixed.
"""
import build_how_an_llm_works_v12_review as repair

repair.OUT=repair.ROOT/'video-audit/how-an-llm-works-repair-2026-09-17-v13'
repair.DEST=repair.ROOT/'Prompts/how-an-llm-works-v13.mp4'
repair.DONORS[1].update(video_start=4980,video_rate=1/3)

if __name__=='__main__':repair.main()
