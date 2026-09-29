#!/usr/bin/env python3
"""Run complete actual-file QA on the corrected v10 candidate."""
import qa_what_is_ai_v9 as qa
from build_what_is_ai_v10 import OUT,DEST
qa.OUT=OUT
qa.DEST=DEST
if __name__=='__main__':qa.main()
