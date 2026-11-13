"""Revise v19 at the three requested speech edits and use intact board artwork."""
import json
import numpy as np

import build_flattery_trap_v18 as base
from build_flattery_trap_v19 import ReviewPictures, MOVE_CUES, TRAVEL
from editspec_build import W, H
from ken_burns_path import smoothstep

DEST = base.ROOT / 'Prompts/flattery-trap-v20.mp4'
AUDIT = base.ROOT / 'video-audit/flattery-trap-v20-2026-11-13'
# Original roll-2 frames. Edges sit between whole sentences and skip the entire
# Gatsby banner until the first frame of the following writing scene.
GATSBY_CUT = (2302, 2576)
TESTING_CUT = (5205, 5337)
RUBRIC_CUT = (7336, 7630)
RUBRIC_LENGTH = RUBRIC_CUT[1] - RUBRIC_CUT[0]


class BoardPictures(ReviewPictures):
    def stage(self, key, region):
        return self.assets[key]

    def camera(self, key, region):
        h,w = self.assets[key].shape[:2]
        if key == 'gatsby' and region == 'scenario':
            # Let the complete essay nearly fill the width, anchoring the top
            # of the original board near the top of frame.
            scale = (W-44)/w
            return np.array([w/2, (H/2-20)/scale, scale])
        if key != 'moves':
            return super().camera(key,region)
        overview_scale = (H-104)/h
        if region is None or region == 'moves-end':
            return np.array([w/2, h/2, overview_scale])
        scale = (H-52)/h
        (_,y0,_,y1),_ = base.REGIONS[region]
        # Clamp the camera so all four outside edges of the board remain visible.
        low,high = h-(H/2-10)/scale,(H/2-10)/scale
        cy = np.clip((y0+y1)/2,low,high)
        return np.array([w/2, cy, scale])

    def travel(self,key,old,new,step):
        if step <= 0:
            return self.settled(key,old)
        if step >= TRAVEL:
            return self.settled(key,new)
        t = smoothstep(step/TRAVEL)
        view = self.camera(key,old)*(1-t) + self.camera(key,new)*t
        return self.render_view(key,new,view)

    def frame(self,source,n):
        if source=='v1' and 726<=n<1207:
            # 27 seconds on the v19 timeline. Hold through the entire spoken essay.
            return self.travel('gatsby',None,'scenario', n-786)
        if source=='v2' and 1857<=n<GATSBY_CUT[0]:
            return self.board('gatsby','useful')
        if source=='v2' and 5578<=n<5706:
            clock=n+50
        elif source=='v1' and 5608<=n<6009:
            clock=n+148
        elif source=='v2' and 6284<=n<8278:
            clock=n-127-(RUBRIC_LENGTH if n>=RUBRIC_CUT[1] else 0)
        else:
            return super().frame(source,n)
        prior=None
        for arrival,target in MOVE_CUES:
            if target in ('tip','moves-end'):
                arrival-=RUBRIC_LENGTH
            if clock < arrival-TRAVEL:
                break
            if clock < arrival:
                return self.travel('moves',prior,target,clock-arrival+TRAVEL)
            prior=target
        return self.settled('moves',prior)


def main():
    manifest_path=base.ROOT/'video-audit/flattery-trap-v19-2026-11-13/edit-manifest.json'
    previous=json.loads(manifest_path.read_text())
    edits=[]
    deleted=[]
    for row in previous['segments']:
        src=row['source']
        first,last=row['source_frames']
        cursor=first
        for a,b in (GATSBY_CUT,TESTING_CUT,RUBRIC_CUT):
            if src=='v2' and first<a<b<last:
                edits.append((src,cursor,a,row['gain_db'],row['label']))
                deleted.append([v-first+row['output_frames'][0] for v in (a,b)])
                cursor=b
        edits.append((src,cursor,last,row['gain_db'],row['label']))
    assert len(deleted)==3
    base.DEST=DEST
    base.AUDIT=AUDIT
    base.EDITS=edits
    base.Pictures=BoardPictures
    base.main()
    path=AUDIT/'edit-manifest.json'
    manifest=json.loads(path.read_text())
    manifest.update(previous_cut=previous['output'],removed_v19_frames=deleted)
    path.write_text(json.dumps(manifest,indent=2)+'\n')


if __name__=='__main__':
    main()
