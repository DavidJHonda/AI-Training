#!/usr/bin/env python3
"""Run the full encoded-file checks on v6, including corrected visual expectations."""
import build_unexpected_results_v6 as build
import qa_unexpected_results_v5 as qa

qa.OUT = build.base.OUT
qa.DEST = build.base.DEST
qa.Picture = build.Picture

if __name__=='__main__':qa.main()
