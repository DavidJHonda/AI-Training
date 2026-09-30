#!/usr/bin/env python3
"""Run the same final-export checks against v11's cleared board entries."""
import qa_support_trap_v10 as qa
import build_support_trap_v11
import json

if __name__=='__main__':
    qa.main()
    m=json.loads((qa.b.OUT/'edit-manifest.json').read_text())
    board=m['boards']['jobs']
    for frame in [2773,3341,3886]:
        at=frame-board['src_in']
        assert not any(r['start']<=at<r['end'] for r in board['rings'])
    print('All three board entries open unmarked.',flush=True)
