#!/usr/bin/env python3
"""Run actual-file QA for the final camera-smoothed review candidate."""
import qa_flattery_engagement_v5 as qa
qa.OUT=qa.ROOT/'video-audit/flattery-engagement-build-v6-2026-11-02'
qa.DEST=qa.ROOT/'Prompts/flattery-engagement-v6.mp4'
if __name__=='__main__':qa.main()
