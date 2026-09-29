#!/usr/bin/env python3
"""v9 finishing plan with constrained catalog tracking; rebuilt from pristine roll 5."""
import json,shutil
import build_what_is_ai_v9 as build

PREVIOUS=build.OUT
build.OUT=build.ROOT/'video-audit/what-is-ai-build-2026-09-29-v10'
build.DEST=build.ROOT/'Prompts/what-is-ai-v10.mp4'
OUT,DEST=build.OUT,build.DEST
ROOT,SRC,TOTAL=build.ROOT,build.SRC,build.TOTAL

def main():
    OUT.mkdir(exist_ok=True);(OUT/'source').mkdir(exist_ok=True)
    if not (OUT/'assets').exists():shutil.copytree(PREVIOUS/'assets',OUT/'assets')
    shutil.copy2(PREVIOUS/'source/01815.png',OUT/'source/01815.png')
    rows=json.loads((PREVIOUS/'movie-tracking.json').read_text())
    fixed=[];last=0
    for frame,boxes in rows:
        # A bright scan line can split the middle tile. The right tile is then
        # the only component. Infer translation using either tile's origin.
        candidates=[x-origin for x,y,w,h,a in boxes for origin in [544,778] if 0<=x-origin<=146]
        if candidates:last=min(candidates,key=lambda x:abs(x-last))
        fixed.append([frame,[[544+last,186,190,186,30000]]])
    shifts=[boxes[0][0]-544 for _,boxes in fixed]
    assert min(shifts)==0 and 143<=max(shifts)<=146
    assert max(abs(b-a) for a,b in zip(shifts,shifts[1:]))<=12
    (OUT/'movie-tracking.json').write_text(json.dumps(fixed)+'\n')
    (OUT/'tracking-verification.json').write_text(json.dumps(dict(frames=len(fixed),min=min(shifts),max=max(shifts),
      max_adjacent_motion=max(abs(b-a) for a,b in zip(shifts,shifts[1:])),
      correction='Disambiguate middle and right tile detections during scan-line animation.'),indent=2)+'\n')
    (OUT/'PLAN.md').write_text((PREVIOUS/'PLAN.md').read_text().replace('version 9','version 10'))
    build.main()

if __name__=='__main__':main()
