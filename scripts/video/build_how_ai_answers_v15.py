#!/usr/bin/env python3
"""Final review build: draw token emphasis behind the complete reply text."""
import build_how_ai_answers_v14 as previous

base=previous.base
base.OUT=base.ROOT/'video-audit/how-ai-answers-tighten-v15-2026-11-09'
base.DEST=base.ROOT/'Prompts/how-ai-answers-v15.mp4'
previous.scene.BACKGROUND_FIRST=True

if __name__=='__main__':base.main()
