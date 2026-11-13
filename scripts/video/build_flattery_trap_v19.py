"""Trim v18's opening and revise only the requested board camera moves and flash."""
import json
from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np

import build_flattery_trap_v18 as previous
from editspec_build import H, W
from ken_burns_path import draw_ring, hex_bgr, ring_px, smoothstep

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'Prompts/flattery-trap-v19.mp4'
AUDIT = ROOT / 'video-audit/flattery-trap-v19-2026-11-13'

# Continuous v18 output-frame clock. A voice change between rows 1 and 2
# must not restart the camera, even though the source file and its clock change.
MOVE_CUES = [(5756, 'opinion'), (6179, 'gaps'), (6788, 'rubric'),
             (7507, 'tip'), (7886, 'moves-end')]
TRAVEL = 32


class ReviewPictures(previous.Pictures):
    @lru_cache(maxsize=None)
    def stage(self, key, region):
        """Keep the surrounding board in motion; retire neighboring copy at rest."""
        original = self.assets[key]
        if region is None or region == 'useful':
            return original
        rect, _ = previous.REGIONS[region]
        outside = np.full_like(original, (255, 255, 255))
        x0,y0,x1,y1 = rect
        pad = 7
        outside[y0-pad:y1+pad, x0-pad:x1+pad] = original[y0-pad:y1+pad, x0-pad:x1+pad]
        return outside

    def camera(self, key, region):
        h,w = self.assets[key].shape[:2]
        if region is None:
            return np.array([w/2, h/2, min((W-60)/w, (H-32)/h)])
        (x0,y0,x1,y1), _ = previous.REGIONS[region]
        scale = min((W-32)/(x1-x0), (H-40)/(y1-y0))
        if region == 'useful':
            scale = min((W-64)/(x1-x0), (H-48)/(y1-y0), .93)
        return np.array([(x0+x1)/2,(y0+y1)/2,scale])

    def render_view(self, key, region, view):
        cx,cy,scale = view
        tx,ty = W/2-cx*scale,H/2-cy*scale
        frame = cv2.warpAffine(self.stage(key,region),np.float32([[scale,0,tx],[0,scale,ty]]),
                               (W,H),flags=cv2.INTER_LINEAR,borderValue=(255,255,255))
        if region:
            (x0,y0,x1,y1),color = previous.REGIONS[region]
            half = ring_px(H)/2
            draw_ring(frame,x0*scale+tx-half,y0*scale+ty-half,x1*scale+tx+half,y1*scale+ty+half,
                      hex_bgr(color),max(6,14*scale),ring_px(H))
        return frame

    @lru_cache(maxsize=None)
    def settled(self, key, region):
        return self.render_view(key,region,self.camera(key,region))

    def travel(self,key,old,new,step):
        if step >= TRAVEL:
            return self.settled(key,new)
        if step <= 0:
            return self.settled(key,old)
        u = smoothstep(step/TRAVEL)
        view = (1-u)*self.camera(key,old)+u*self.camera(key,new)
        # Both layers use the identical moving viewport, keeping the pan spatially continuous.
        return cv2.addWeighted(self.render_view(key,old,view),1-u,self.render_view(key,new,view),u,0)

    def frame(self,source,n):
        if source=='v2' and 2312-TRAVEL <= n < 2575:
            return self.travel('gatsby','useful','takeaway',n-(2312-TRAVEL))
        if source=='v2' and 5338 <= n < 5340:
            return self.board('quote',None)
        if source=='v2' and 5578 <= n < 5706:
            clock=n+50
        elif source=='v1' and 5608 <= n < 6009:
            clock=n+148
        elif source=='v2' and 6284 <= n < 8278:
            clock=n-127
        else:
            return super().frame(source,n)
        prior=None
        for arrival,target in MOVE_CUES:
            if clock < arrival-TRAVEL:
                break
            if clock < arrival:
                return self.travel('moves',prior,target,clock-(arrival-TRAVEL))
            prior=target
        return self.settled('moves',prior)


if __name__=='__main__':
    previous.DEST=DEST
    previous.AUDIT=AUDIT
    previous.Pictures=ReviewPictures
    # Delete exactly [25.00,36.00) on the v18 timeline. The second take has
    # quiet pre-roll until 24.65 source seconds, so its first word is preserved.
    previous.EDITS[0]=('v2',0,750,0,'Opening through the trap definition')
    previous.EDITS[1]=('v1',726,1720,-1.3,'Gatsby introduction and flattering reply')
    previous.main()
    p=AUDIT/'edit-manifest.json'
    manifest=json.loads(p.read_text())
    manifest.update(previous_cut='Prompts/flattery-trap-v18.mp4',deleted_v18_frames=[750,1080],
                    flash_v18_frames=[5388,5390],camera_transition_frames=TRAVEL,
                    moves_arrivals_v19_frames={target:arrival-330 for arrival,target in MOVE_CUES})
    p.write_text(json.dumps(manifest,indent=2)+'\n')
