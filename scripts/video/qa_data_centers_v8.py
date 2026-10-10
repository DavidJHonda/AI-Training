#!/usr/bin/env python3
"""Run the graft QA on the corrected v8 boundary."""
import qa_data_centers_v7 as qa
from build_data_centers_v8 import build
qa.OUT=build.OUT
qa.DEST=build.DEST
qa.VISUAL_RESUME=build.VISUAL_RESUME
if __name__=='__main__':qa.main()
