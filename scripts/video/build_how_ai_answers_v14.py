#!/usr/bin/env python3
"""Same approved cut; correct punctuation baseline and smooth the loop entrance."""
import build_how_ai_answers_v13 as base
import render_how_ai_answers_wide_v14 as scene

base.OUT=base.ROOT/'video-audit/how-ai-answers-tighten-v14-2026-11-09'
base.DEST=base.ROOT/'Prompts/how-ai-answers-v14.mp4'
base.scene=scene
# The probability-explanation cut otherwise exposes 16 frames of an old
# question drawing. Hold the preceding keyboard until the existing loop starts.
base.EXTRA_HOLDS=[(2803,2819,2576)]

if __name__=='__main__':base.main()
