"""One-second Gatsby hold and a closer continuous pan over the original feedback board."""
import json

import numpy as np

import build_flattery_trap_v18 as base
from build_flattery_trap_v20 import BoardPictures, GATSBY_CUT
from editspec_build import W, H, FPS


class FeedbackCamera(BoardPictures):
    def camera(self, key, region):
        if key != 'moves' or region is None:
            return super().camera(key,region)
        h,w = self.assets[key].shape[:2]
        # Fit the whole spoken row with clearance for its ring. Pan within
        # the intact artwork so adjoining rows appear naturally at the edges.
        (x0,y0,x1,y1),_ = base.REGIONS[region]
        scale = (W-40)/(x1-x0)
        half_height = H/(2*scale)
        cy = np.clip((y0+y1)/2, half_height, h-half_height)
        return np.array([w/2,cy,scale])


def main():
    previous = base.ROOT/'video-audit/flattery-trap-v20-2026-11-13/edit-manifest.json'
    rows = json.loads(previous.read_text())['segments']
    base.EDITS = [(r['source'],*r['source_frames'],r['gain_db'],r['label']) for r in rows]
    base.DEST = base.ROOT/'Prompts/flattery-trap-v21.mp4'
    base.AUDIT = base.ROOT/'video-audit/flattery-trap-v21-2026-11-13'
    base.Pictures = FeedbackCamera
    base.main(holds={('v2',GATSBY_CUT[0]):FPS})


if __name__=='__main__':
    main()
