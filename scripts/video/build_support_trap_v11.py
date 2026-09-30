#!/usr/bin/env python3
"""Final lesson-board update: clear old highlights before board returns."""
import json
import build_support_trap_v10 as edit
b=edit.b
b.OUT=b.ROOT/'video-audit/support-trap-board-update-2026-09-30-v11'
b.DEST=b.ROOT/'Prompts/support-trap-v11.mp4'
original_setup=edit.setup

def setup():
    build,rows=original_setup()
    # A return waits unmarked for the new point; never carry a hidden prior ring.
    board=build.boards['jobs']
    board['rings'][0]['end']=3065-board['src_in']
    board['rings'][1]['end']=3506-board['src_in']
    p=b.OUT/'leg-jobs.json';spec=json.loads(p.read_text())
    spec['rings']=board['rings'];p.write_text(json.dumps(spec,indent=2)+'\n')
    return build,rows

edit.setup=setup
if __name__=='__main__':edit.main()
