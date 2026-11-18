#!/usr/bin/env python3
"""Run the graft QA on the corrected v8 boundary."""
import qa_where_ai_lives_v7 as qa
from build_where_ai_lives_v8 import build
qa.OUT=build.OUT
qa.DEST=build.DEST
qa.VISUAL_RESUME=build.VISUAL_RESUME
if __name__=='__main__':qa.main()
