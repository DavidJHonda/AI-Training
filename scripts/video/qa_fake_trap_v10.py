#!/usr/bin/env python3
"""Run encoded-candidate checks on the corrected shortening candidate."""
import qa_fake_trap_v9 as qa
from build_fake_trap_v10 import ROOT,OUT,DEST,CUTS
qa.ROOT,qa.OUT,qa.DEST,qa.CUTS=ROOT,OUT,DEST,CUTS
if __name__=='__main__':qa.main()
