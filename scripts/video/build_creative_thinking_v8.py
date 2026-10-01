#!/usr/bin/env python3
"""Approved October reroll production: roll 2 audio, canonical boards, drawn donors."""
import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from editspec_build import Build, Reader, fr, sha, readwav, writewav, SPF
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import resolve, rings_for, window, smoothstep, draw_ring, ring_px
from make_close_board import close_board_asset, compose_canonical_for_video

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'video-audit/creative-thinking-build-2026-10-01-v8'
DEST = ROOT/'Prompts/creative-thinking-v8.mp4'
SOURCES = [ROOT/f'Prompts/creative-thinking-{n}.mp4' for n in (1,2,3)]
EXPECTED = ['22f732522b0c52e0ce62fd9ebc48a7692909cbfa4283ad3b2f2fcb6b95c08515',
 'a241f485d1215763d0565112de3e60490b4ed85512dc6b14ccba43e55432186c',
 '320d0f15d629b73f5f03d74184611f2615deef78d7578ea2d26397318c36f7de']
BOUNDS = [(40,127,784,717),(816,127,1560,717),(40,750,784,1339),(816,750,1560,1339)]
COLORS = ['#4f2fc4','#1652f0','#0e8f86','#a9760c']
WHAT_IF_DONOR = (1560,1734)


class BoardRenderer:
    """Render the shared board specification directly, avoiding lossless scratch legs."""
    def __init__(self, path):
        self.spec=json.loads(path.read_text());self.im=cv2.imread(self.spec['image'])
        self.rings=rings_for(self.spec);self.beats=[];at=0
        for label,n,a,z in resolve(self.spec,16/9,1280,3):
            self.beats.append((at,at+n,a,z));at+=n
        self.cache={}

    def frame(self,n):
        s,e,a,z=next(b for b in self.beats if b[0]<=n<b[1])
        q=smoothstep((n-s)/(e-s-1)) if e-s>1 else 1
        cam=[a[i]+q*(z[i]-a[i]) for i in range(3)]
        active=tuple(i for i,r in enumerate(self.rings) if r[0]<=n<r[1])
        key=tuple(cam)+active
        if key in self.cache:return self.cache[key].copy()
        h,w=self.im.shape[:2];x,y,ww,hh=window(*cam,16/9,w,h)
        im=cv2.warpAffine(self.im,np.float32([[ww/1280,0,x],[0,hh/720,y]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
        scale=1280/ww;t=ring_px(720)
        for i in active:
            _,_,(rx,ry,rw,rh),color,pad,radius=self.rings[i]
            draw_ring(im,(rx-pad-x)*scale-t/2,(ry-pad-y)*scale-t/2,
                (rx+rw+pad-x)*scale+t/2,(ry+rh+pad-y)*scale+t/2,color,radius*scale+t/2,t)
        if a==z:self.cache[key]=im.copy()
        return im


class PlannerRepair:
    """Track three malformed note interiors; keep the source drawing and camera motion."""
    def __init__(self):
        self.ref=cv2.imread(str(OUT/'source-2-3450.jpg'))
        self.orb=cv2.ORB_create(nfeatures=2000)
        self.kp,self.des=self.orb.detectAndCompute(self.ref,None)
        self.matcher=cv2.BFMatcher(cv2.NORM_HAMMING)
        rects=[(941,131,1092,287),(991,340,1107,408),(885,402,991,479)]
        mask=np.zeros((720,1280),np.uint8)
        for x0,y0,x1,y1 in rects:mask[y0:y1,x0:x1]=255
        dark=(cv2.cvtColor(self.ref,cv2.COLOR_BGR2GRAY)<130).astype(np.uint8)*255
        dark=cv2.dilate(dark,np.ones((3,3),np.uint8));dark=cv2.bitwise_and(dark,mask)
        fixed=cv2.inpaint(self.ref,dark,5,cv2.INPAINT_TELEA)
        pic=Image.fromarray(cv2.cvtColor(fixed,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(pic)
        font='/System/Library/Fonts/Supplemental/Arial.ttf'
        for xy,txt,size in [((950,145),'Notice gaps\n\nConnect ideas\n\nChoose a path',19),((998,349),'New\nconnections',17),((891,410),'Different\npatterns',19)]:
            d.multiline_text(xy,txt,font=ImageFont.truetype(font,size),fill=(53,45,30),spacing=5)
        self.fixed=cv2.cvtColor(np.array(pic),cv2.COLOR_RGB2BGR)
        self.alpha=cv2.GaussianBlur(mask,(9,9),1.4).astype(np.float32)/255
        self.stats=[]

    def frame(self,im,sf):
        kp,des=self.orb.detectAndCompute(im,None)
        matches=self.matcher.knnMatch(self.des,des,k=2)
        good=[m for m,n in matches if m.distance<.7*n.distance]
        assert len(good)>30,(sf,len(good))
        a=np.float32([self.kp[m.queryIdx].pt for m in good]);z=np.float32([kp[m.trainIdx].pt for m in good])
        matrix,keep=cv2.estimateAffinePartial2D(a,z,method=cv2.RANSAC,ransacReprojThreshold=2)
        assert matrix is not None and int(keep.sum())>20,sf
        fixed=cv2.warpAffine(self.fixed,matrix,(1280,720),flags=cv2.INTER_CUBIC)
        alpha=cv2.warpAffine(self.alpha,matrix,(1280,720))[:,:,None]
        if sf%30==0:self.stats.append(dict(source_frame=sf,inliers=int(keep.sum()),matrix=matrix.tolist()))
        return np.clip(im*(1-alpha)+fixed*alpha,0,255).astype(np.uint8)


def prepare():
    cv2.setNumThreads(2)
    for p,h in zip(SOURCES,EXPECTED):assert sha(p)==h,p
    assets=ROOT/'course-assets/creative-thinking'
    b=Build(ROOT,SOURCES[1],OUT,DEST,protected=[SOURCES[0],SOURCES[2],ROOT/'lessons/creative-thinking.md',*assets.glob('*.jpg')])
    b.load_audio([(125.34,125.56),(133.28,133.62),(197.8,198.03)])
    def keep(s,e,label,visual='source',donor=None,start=None,end=None):
        b.keep(s,e,label,visual,video_from=start,video_src=donor,video_end=end)
        # Preserve uninterrupted source audio across picture-only row boundaries.
        b.parts[-1]=b.audio[s*SPF:e*SPF].copy()
    keep(0,869,'Opening and definition')
    keep(869,1043,'Drawn technologist replaces Jobs photo',donor=SOURCES[2],start=920,end=1095)
    keep(1043,1208,'Drawn complicated hardware',donor=SOURCES[0],start=1202,end=1344)
    keep(1208,1342,'Drawn accessible home computer',donor=SOURCES[0],start=1344,end=1553)
    keep(1342,1830,'Creativity across professions')
    keep(1830,2556,'Professions overview and first cards','professions')
    keep(2556,2658,'Engineer workshop cutaway',donor=SOURCES[0],start=1740,end=1842)
    keep(2658,2898,'Doctor and professions finish','professions')
    keep(2898,3378,'Performance comparison and AI answer')
    keep(3378,3563,'Human judgment drawing; repaired labels')
    keep(3563,3759,'Not a magic gift and practice reveal')
    keep(3999,4620,'Four habits overview and first two habits','practice')
    keep(4620,4794,'What-if alternative-path cutaway',donor=SOURCES[1],start=WHAT_IF_DONOR[0],end=WHAT_IF_DONOR[1])
    keep(4794,5010,'Return to what-if and connect card','practice')
    keep(5010,5133,'Connect ideas wall cutaway',donor=SOURCES[1],start=5740,end=5863)
    keep(5133,5514,'Step away and practice takeaway','practice')
    keep(5934,6006,'Habits widen options diagram',donor=SOURCES[1],start=5580,end=5660)
    keep(6006,6076,'Judgment selects the star',donor=SOURCES[1],start=5970,end=6079)
    b.mark_close_start()
    keep(6076,6174,'Two-line canonical close','close')
    # Total closing visual 228 frames: 48 hold + 150 push + 30 settled.
    b.pause(130,'Settled canonical close tail')
    # Smooth only true audio discontinuities, never every visual cut.
    joins=[];r=np.linspace(0,1,240)
    for i in range(len(b.rows)-1):
        left,right=b.rows[i:i+2]
        if left.get('source_end')!=right.get('source_start') or right['kind']=='room_tone':
            b.parts[i][-240:]=b.parts[i][-240:]*(1-r)+b.tone(240)*r
            b.parts[i+1][:240]=b.parts[i+1][:240]*r+b.tone(240)*(1-r)
            joins.append(dict(output_frame=right['start_frame'],left_source_end=left.get('source_end'),right_source_start=right.get('source_start'),fade_ms=5))
    b.finish_audio()
    names=[['A Lawyer','An Entrepreneur','An Engineer','A Doctor'],['Generate Before You Judge','Ask What If','Connect Unrelated Things','Step Away Then Return']]
    onsets=[[65.26,74.22,82.4,89.74],[138.62,151.88,161.70,172.16]]
    for key,asset,s,e,ns,ats,pull in [('professions','creative-professions',1830,2898,names[0],onsets[0],None),('practice','practice-creativity',3999,5514,names[1],onsets[1],182.4)]:
        targets=[dict(label=n,at=t,rects=[r],cam=r,color=c,radius=18) for n,t,r,c in zip(ns,ats,BOUNDS,COLORS)]
        b.board(key,assets/f'creative-thinking-{asset}.jpg',s,e,'dense',targets,pullback_at=pull)
    compose_canonical_for_video(close_board_asset('creativethinking'),OUT/'close.png','#ffffff')
    b.close_img=cv2.imread(str(OUT/'close.png'))
    m=b.manifest(dict(narration_cuts=[dict(source_frames=[3759,3999],words='In a world overflowing ... sets you apart.'),dict(source_frames=[5514,5934],words='By deliberately practicing ... final decision.')],
        actual_audio_joins=joins,added_instructional_pause_frames=0,donor_audio_grafts=0,
        close_asset=str(close_board_asset('creativethinking')),listening='Not performed; two narration joins require owner listening review.',
        longest_unbroken_board_seconds=24.2))
    boards={k:BoardRenderer(OUT/f'leg-{k}.json') for k in b.boards}
    for k,renderer in boards.items():
        spec=renderer.spec;want=[0]+[x['start']+26 for x in spec['rings']]+[sum(x['frames'] for x in spec['beats'])-1]
        tiles=[]
        for f in want:
            im=renderer.frame(f);cv2.imwrite(str(OUT/'preview'/f'{k}-{f:04d}.jpg'),im)
            tile=cv2.resize(im,(640,360));cv2.putText(tile,f'{k} f{f}',(10,25),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,220),2);tiles.append(tile)
        cv2.imwrite(str(OUT/f'preview-{k}.jpg'),cv2.vconcat([cv2.hconcat(tiles[i:i+2]) for i in range(0,len(tiles),2)]))
    patch=PlannerRepair();cv2.imwrite(str(OUT/'preview-planner.jpg'),patch.frame(patch.ref,3450))
    return b,boards,patch


def render(b,boards,patch):
    assert not DEST.exists(),'Never overwrite a review candidate'
    proc=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    mask=glyph_mask();counts={'clone':0,'inpaint':0,'declined':0};main=Reader(b.src)
    for row in b.rows:
        n=row['end_frame']-row['start_frame'];reader=None
        if 'video_start' in row:reader=Reader(row.get('video_src',b.src))
        for k in range(n):
            f=row['start_frame']+k
            if f>=b.close_start:
                u=np.clip((f-b.close_start-48)/149,0,1);z=1+.2*smoothstep(u)
                h,w=b.close_img.shape[:2];ww=w/z;hh=ww*9/16
                im=cv2.warpAffine(b.close_img,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            elif row['visual'] in boards:
                im=boards[row['visual']].frame(row['source_start']+k-b.boards[row['visual']]['src_in'])
            else:
                sf=row['source_start']+k
                if reader:
                    start=row['video_start'];end=row['video_end']
                    vf=start+round(k*(end-start-1)/max(1,n-1));im=reader.at(vf)
                else:im=main.at(sf)
                if not reader and 3378<=sf<3563:im=patch.frame(im,sf)
                im,how=clean_frame(im,mask);counts[how or 'declined']+=1
            proc.stdin.write(im.tobytes())
        if reader:reader.c.release()
        print(f'Rendered {row["end_frame"]}/{b.total}: {row["label"]}',flush=True)
    proc.stdin.close();assert proc.wait()==0
    m=json.loads((OUT/'edit-manifest.json').read_text());m.update(render_sha256=sha(DEST),corner_mark=counts,planner_label_tracking=patch.stats,
        protected_files_unchanged={p:sha(p)==h for p,h in b.hashes.items()})
    assert all(m['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    print('COMPLETE',DEST,b.total/30,flush=True)


if __name__=='__main__':
    import sys
    b,boards,patch=prepare()
    print('Prepared',b.total,'frames',b.total/30,'seconds',flush=True)
    if '--preview' not in sys.argv:render(b,boards,patch)
