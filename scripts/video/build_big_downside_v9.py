#!/usr/bin/env python3
"""Finish the approved Roll 2 pass without a brief return to the old action shot."""
import json
import build_big_downside_v8 as build
from editspec_build import fr

build.OUT=build.ROOT/'video-audit/big-downside-build-2026-10-10-v9'
build.DEST=build.ROOT/'Prompts/big-downside-v9.mp4'

def prepare():
    m=build.prepare()
    old_end=fr(162.4);new_end=fr(163.0666667)
    insert=next(r for r in m['inserts'] if r['label']=='Complete unintended-route sequence')
    anchors=[[insert['start_frame'],insert['video_start']],
             [old_end-1,insert['video_end']-1],[new_end-1,insert['video_end']-1]]
    insert.update(end_frame=new_end,anchors=anchors)
    insert['why']+=' Hold its final state until the actual server-scene cut, avoiding a 20-frame return to the old execute image.'
    for r in m['timeline']:
        if r['label']=='Complete unintended-route sequence':
            r.update(end_frame=new_end,map_end=new_end,anchors=anchors)
        elif r['start_frame']==old_end:r['start_frame']=new_end
    for b in m['boundaries']:
        if b['frame']==old_end:b['frame']=new_end
    m['boundaries'].sort(key=lambda x:x['frame'])
    for a,b in zip(m['timeline'],m['timeline'][1:]):assert a['end_frame']==b['start_frame']
    (build.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    return m

if __name__=='__main__':build.render(prepare())
