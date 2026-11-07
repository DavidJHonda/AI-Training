#!/usr/bin/env python3
"""Illustrated planning/research passages; preserve v8 edits and copied AAC."""
import argparse
import json
import subprocess
import cv2
import numpy as np
import build_when_you_need_more_v8 as prior
from editspec_build import sha
from ken_burns_path import smoothstep

base=prior.base
ROOT=prior.ROOT
OUT=ROOT/'video-audit/when-you-need-more-build-v9-2026-11-07'
DEST=ROOT/'Prompts/when-you-need-more-v9.mp4'
LIVE=prior.DEST  # QA baseline and exact audio packet source.
ASSETS=ROOT/'scripts/video/assets/when-you-need-more-scenes-2026-11-07'
INSERTS=[dict(kind='business-planning',start=1852,end=2359),
         dict(kind='college-research',start=3476,end=3946)]

def setup():
    assert sha(LIVE)=='00c4017e56f02002441fbe5c55dfee5759a013a201b476a47a72f07b7b49445b'
    base.OUT=OUT; base.DEST=DEST

class Scenes:
    def __init__(self):
        self.images={r['kind']:cv2.imread(str(ASSETS/(r['kind']+'.png'))) for r in INSERTS}
        assert all(im is not None for im in self.images.values())
    def frame(self,r,f):
        im=self.images[r['kind']]; h,w=im.shape[:2]
        u=np.clip((f-r['start']-60)/(r['end']-r['start']-121),0,1)
        zoom=1+.04*smoothstep(float(u)); ww=min(w,h*16/9)/zoom;hh=ww*9/16
        return cv2.warpAffine(im,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),
                             (1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)

def prepare():
    setup();m=base.prepare()
    m.update(scope='User-approved illustrated planning and college-research scenes matching Your Home Base; review candidate only.',
             inserts=INSERTS,retained_v8_inserts=prior.INSERTS,
             audio='Exact AAC packets and timing copied from v8; original 5069-frame duration.',
             longest_unbroken_board_seconds=18.3666666667,
             illustration_motion='4 percent camera push after 2-second wide hold, ending with 2-second close hold; no object animation.')
    for p in [LIVE,prior.COLLEGE,*ASSETS.glob('*')]:m['protected_hashes'][str(p)]=sha(p)
    boundaries={r['start_frame']:r['label'] for r in m['visual_timeline'][1:]}
    for r in INSERTS:
        for f in list(boundaries):
            if r['start']<f<r['end']:del boundaries[f]
    for r in [*prior.INSERTS,*INSERTS]:
        boundaries[r['end']]='return to retained picture'
    for r in [*prior.INSERTS,*INSERTS]:boundaries[r['start']]=r['kind']
    m['boundaries']=[dict(frame=f,label=label) for f,label in sorted(boundaries.items())]
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');return m

def render(m,preview=False):
    setup();scenes=Scenes()
    if preview:
        for r in INSERTS:
            for f in [r['start'],(r['start']+r['end'])//2,r['end']-1]:
                cv2.imwrite(str(OUT/'preview'/f"{r['kind']}-{f:05d}.jpg"),scenes.frame(r,f))
        return
    assert not DEST.exists(),'Never overwrite a candidate'
    p=base.Pictures(m);old=prior.Inserts()
    proc=subprocess.Popen([base.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
        '-r','30','-i','pipe:0','-i',str(LIVE),'-map','0:v','-map','1:a','-c:v','libx264',
        '-preset','fast','-crf','17','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for row in m['visual_timeline']:
        for f in range(row['start_frame'],row['end_frame']):
            new=next((r for r in INSERTS if r['start']<=f<r['end']),None)
            retained=next((r for r in prior.INSERTS if r['start']<=f<r['end']),None)
            im=scenes.frame(new,f) if new else old.frame(retained,f) if retained else p.frame(row,f)
            proc.stdin.write(im.tobytes())
        print(row['end_frame'],m['frames'],row['label'],flush=True)
    proc.stdin.close();assert proc.wait()==0
    m.update(candidate_sha256=sha(DEST),insert_corner_cleaning=old.cleaning,
             source_corner_cleaning=p.counts,protected_unchanged={k:sha(k)==v for k,v in m['protected_hashes'].items()})
    assert all(m['protected_unchanged'].values()) and old.cleaning['declined']==0 and p.counts['declined']==0
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    (OUT/'label-tracking.json').write_text(json.dumps(old.thinking.matches,indent=2)+'\n')
    print('BUILT',DEST,flush=True)

if __name__=='__main__':
    cv2.setNumThreads(2);ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');ap.add_argument('--render-prepared',action='store_true');args=ap.parse_args()
    m=json.loads((OUT/'edit-manifest.json').read_text()) if args.render_prepared else prepare()
    render(m,args.preview)
