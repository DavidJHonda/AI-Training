#!/usr/bin/env python3
"""Narrow, owner-requested camera revision of One Answer. Two Endings."""
from pathlib import Path
import argparse, json, shutil, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw
import build_engagement_trap_v12 as b
from ken_burns_path import draw_ring, hex_bgr, ring_px, fit_window

OUT = b.ROOT/'video-audit/engagement-trap-build-2026-09-30-v14'
DEST = b.ROOT/'Prompts/engagement-trap-v14.mp4'
AUDIO = b.ROOT/'Prompts/engagement-trap-v13.mp4'
PRIOR = b.ROOT/'video-audit/engagement-trap-build-2026-09-29-v13/edit-manifest.json'
SPANS = [(908,1455),(1767,2121),(2309,2594)]
RECTS = dict(question=[607,253,1520,388], answer=[81,453,1001,669],
             stop=[41,741,784,1340], trap=[817,741,1560,1340],
             takeaway=[40,1380,1561,1469])
COLORS = dict(question=b.PURPLE, answer=b.PURPLE, stop=b.BLUE,
              trap=b.AMBER, takeaway=b.PURPLE)
FULL = np.array([800,754,1508*1280/704],dtype=float)
# Derive the single dive width from the largest complete target, with 30px
# output clearance. Bubble labels are also inside these centered windows.
WIDTH = max(fit_window({'fit':[r[0],r[1],r[2]-r[0],r[3]-r[1]],
                        'margin':30},16/9,1280,1)[2]
            for k,r in RECTS.items() if k!='takeaway')
CAM = {k:np.array([(r[0]+r[2])/2,(r[1]+r[3])/2,WIDTH])
       for k,r in RECTS.items() if k!='takeaway'}
PREVIEWS = [908,1003,1019,1034,1145,1160,1175,1440,
            1767,1780,1957,1972,1987,2110,2309,2324,2339,2340,2490]

def mix(a,z,t):
    return a+(z-a)*b.smooth(t)

def state(n):
    if 908<=n<1004:return FULL,None
    if n<1145:return mix(FULL,CAM['question'],(n-1004)/30),'question'
    if n<1455:return mix(CAM['question'],CAM['answer'],(n-1145)/30),('answer' if n>=1175 else None)
    if 1767<=n<1957:return CAM['stop'],('stop' if n>=1772 else None)
    if n<2121:return mix(CAM['stop'],CAM['trap'],(n-1957)/30),('trap' if n>=1987 else None)
    if 2309<=n<2339:return mix(CAM['trap'],FULL,(n-2309)/30),None
    return FULL,'takeaway'

class CameraBoard:
    def __init__(self):
        im=Image.open(b.A/'engagement-trap-comparison.jpg').convert('RGB')
        mask=Image.new('L',im.size,0)
        ImageDraw.Draw(mask).rounded_rectangle((0,0,im.width-1,im.height-1),radius=28,fill=255)
        matte=Image.new('RGB',im.size,'#ebe7fa');matte.paste(im,(0,0),mask)
        self.image=cv2.cvtColor(np.asarray(matte),cv2.COLOR_RGB2BGR)
    def frame(self,n):
        (cx,cy,width),target=state(n)
        scale=1280/width;ox=640-cx*scale;oy=360-cy*scale
        f=cv2.warpAffine(self.image,np.array([[scale,0,ox],[0,scale,oy]]),
                         (1280,720),flags=cv2.INTER_CUBIC,
                         borderMode=cv2.BORDER_CONSTANT,borderValue=hex_bgr('#ebe7fa'))
        if target:
            x0,y0,x1,y1=RECTS[target]
            bounds=[x0*scale+ox,y0*scale+oy,x1*scale+ox,y1*scale+oy]
            assert bounds[0]>=3 and bounds[1]>=3 and bounds[2]<=1277 and bounds[3]<=717,(n,bounds)
            draw_ring(f,*bounds,hex_bgr(COLORS[target]),max(5,18*scale),ring_px(720))
        return f

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    OUT.mkdir(exist_ok=True)
    board=CameraBoard()
    for n in PREVIEWS:cv2.imwrite(str(OUT/f'planned-{n:05d}.jpg'),board.frame(n))
    if args.preview:return
    assert not DEST.exists(),'Never overwrite a candidate.'
    prior=json.loads(PRIOR.read_text())
    assert b.sha(AUDIO)=='e53a9faa4e1fa1026d780f8846bc917c04f4456d3f444a4c1dfede1b2b3db044'
    assert b.sha(b.SRC)==b.EXPECTED
    protected=prior['protected']
    assert all(b.sha(Path(p))==h for p,h in protected.items())
    snapshot=OUT/'source-snapshot.mp4'
    if not snapshot.exists():shutil.copyfile(b.SRC,snapshot)
    assert b.sha(snapshot)==b.EXPECTED
    b.SRC=snapshot
    manifest=dict(prior)
    manifest.update(candidate=str(DEST),audio_source=str(AUDIO),
        video_source=str(snapshot),revision='v14: zoom and pan first comparison board only; copy v13 AAC.',
        approved_scope='2026-09-30: The board at :31. We should do the zoom and pan for this board.',
        density='User-requested dense treatment, including conversation bubbles; explicit exception to compact AI-chat default.',
        comparison_spans=SPANS,comparison_rects=RECTS,comparison_colors=COLORS,
        camera_full=FULL.tolist(),camera_uniform_dive_width=WIDTH,
        camera_targets={k:v.tolist() for k,v in CAM.items()},camera_move_frames=30,
        camera_timing='Full 908–1004; dive question 1004–1034; pan answer 1145–1175; return stop 1767; pan trap 1957–1987; return and pull back 2309–2339; full takeaway to 2594.',
        ring_timing='Question begins with dive; answer/trap rings appear after pan lands; stop ring 1772; takeaway ring 2339. Fixed 4px after crop.',
        unchanged='Audio stream, total frames, all cutaways and all visuals outside three comparison spans.',
        source_limitation='Raw rolls absent. Same verified finished source as v12, encoded once; direct canonical JPG for changed board; v13 audio copied without re-encoding.')
    manifest.pop('candidate_sha256',None)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    source=b.Stream();borrow=b.Stream()
    proc=subprocess.Popen([b.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30',
        '-i','pipe:0','-i',str(AUDIO),'-map','0:v','-map','1:a:0','-c:v','libx264','-crf','16',
        '-preset','fast','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    written=0
    try:
        for n in range(b.N):
            frame=source.at(n)
            if any(s<=n<e for s,e,_ in b.CUTS):continue
            if any(s<=n<e for s,e in SPANS):frame=board.frame(n)
            else:frame=b.changed_visual(n,frame,borrow)
            proc.stdin.write(frame.tobytes());written+=1
            if n%600==0:print('Rendered',n,'/',b.N,flush=True)
    finally:
        proc.stdin.close();source.close();borrow.close()
    assert proc.wait()==0 and written==7832
    assert all(b.sha(Path(p))==h for p,h in protected.items())
    manifest['candidate_sha256']=b.sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',DEST,written,flush=True)

if __name__=='__main__':main()
