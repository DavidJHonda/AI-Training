#!/usr/bin/env python3
"""Run the full encoded-file checks on v6, including corrected visual expectations."""
import build_where_will_ai_land_v6 as build
import qa_where_will_ai_land_v5 as qa

qa.OUT = build.base.OUT
qa.DEST = build.base.DEST
qa.Picture = build.Picture

if __name__=='__main__':qa.main()
