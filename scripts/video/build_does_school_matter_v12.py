#!/usr/bin/env python3
"""Complete the approved two-card working cut with the exact roll-3 ending."""
from pathlib import Path
import json, subprocess, sys
import cv2, numpy as np, imageio_ffmpeg
import build_does_school_matter_working_v11 as base
from editspec_build import Reader, sha, writewav
from build_understand_ai_opener_v12 import draw_ring
from make_close_board import close_board_asset, compose_canonical_for_video
ROOT=base.ROOT
OUT=ROOT/'video-audit/does-school-matter-build-v12-2026-10-22'
DEST=ROOT/'Prompts/does-school-matter-v12.mp4'
DONOR=ROOT/'Prompts/does-school-matter-3.mp4'
DONOR_HASH='bb8c1fa29a960d0e439a3df0a18e2f136b6ce89c720660dc6b3b887cd0e8771b'
START,END=5619,6036
BODY=3834; TOTAL=4251; BANNER=3844; CLOSE=3954; GAIN=2.7

def pcm(path):return base.pcm(path)
class Visuals:
    def __init__(self):
        self.mapping=base.mapping();self.reader=Reader(base.SOURCE);self.states=base.states()
        self.banner=self.states['full'].copy()
        draw_ring(self.banner,40*.8,(748+12)*.8,1560*.8,(836+12)*.8,(255,81,110),11.2,4)
        self.close=cv2.imread(str(OUT/'close.png'))
    def at(self,n):
        if n<BODY:
            s=self.mapping[n];im=self.reader.at(s);state=base.state_for(s)
            return self.states[state] if state else im
        if n<CLOSE:return self.banner if n>=BANNER else self.states['full']
        q=float(np.clip((n-CLOSE-48)/149,0,1));z=1+.2*q*q*(3-2*q)
        h,w=self.close.shape[:2];cw,ch=round(w/z),round(h/z);x,y=(w-cw)//2,(h-ch)//2
        return cv2.resize(self.close[y:y+ch,x:x+cw],(1280,720),interpolation=cv2.INTER_LANCZOS4)

def main():
    assert sha(base.SOURCE)==base.EXPECTED and sha(DONOR)==DONOR_HASH
    assert not DEST.exists(),'Use a new candidate version.'
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    close_asset=close_board_asset('whybother')
    protected={str(p):sha(p) for p in [base.SOURCE,DONOR,base.ASSET,close_asset,ROOT/'index.html',ROOT/'lessons/does-school-matter.md',ROOT/'course-assets/beyond-the-new-average/beyond-the-new-average.mp4',base.DEST]}
    compose_canonical_for_video(close_asset,OUT/'close.png','#ffffff')
    source=pcm(base.SOURCE);parts=[source[a*1600:z*1600].copy() for a,z in base.KEEP]
    for i,part in enumerate(parts):
        if i:part[:240]*=np.linspace(0,1,240)
        part[-240:]*=np.linspace(1,0,240)
    tail=pcm(DONOR)[START*1600:END*1600].copy()*10**(GAIN/20)
    tail[:240]*=np.linspace(0,1,240);tail[-240:]*=np.linspace(1,0,240)
    audio=np.concatenate(parts+[tail]);assert len(audio)==TOTAL*1600 and abs(tail).max()<1
    writewav(OUT/'edited.wav',audio*32768)
    old=json.loads((base.OUT/'edit-manifest.json').read_text())
    boundaries=old['boundaries']+[dict(frame=BODY,label='roll-3-audio-join'),dict(frame=BANNER,label='takeaway-outline'),dict(frame=CLOSE,label='current-closing')]
    plan=dict(candidate=str(DEST),frames=TOTAL,fps=30,duration=TOTAL/30,body_source=str(base.SOURCE),body_sha256=base.EXPECTED,body_keep_frames=base.KEEP,donor=str(DONOR),donor_sha256=DONOR_HASH,donor_frames=[START,END],donor_gain_db=GAIN,protected=protected,boundaries=boundaries,board=old['board'],takeaway=dict(start=BODY,ring_start=BANNER,end=CLOSE,rect_xyxy=[40,748,1560,836],color='#6e51ff',stroke_px=4),close=dict(asset=str(close_asset),start=CLOSE,prehold=48,push=150,settle=TOTAL-CLOSE-198,zoom=1.2),audio='Continuous roll-3 ending; no internal speech cuts. Source silence retained; 5ms edge ramps. Donor +2.7dB for approximate active-RMS match, without clipping.',scope='Review candidate only; installed video and lesson unchanged.',limitation='Frame, transcript, and signal review; direct listening unavailable.')
    (OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    v=Visuals();cv2.imwrite(str(OUT/'preview/board-full.png'),v.states['full'])
    ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for n in range(TOTAL):
        im=v.at(n);p.stdin.write(im.tobytes())
        if n%900==0:print(f'Rendered {n}/{TOTAL}',flush=True)
    p.stdin.close();assert p.wait()==0;v.reader.c.release()
    assert all(sha(Path(p))==h for p,h in protected.items())
    plan['candidate_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    print(DEST,flush=True)
if __name__=='__main__':main()
