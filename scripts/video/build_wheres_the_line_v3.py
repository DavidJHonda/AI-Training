#!/usr/bin/env python3
"""Approved September 30 visual review repair. Audio and installed file untouched."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

import av
import cv2
import numpy as np
import imageio_ffmpeg

from editspec_build import Build, sha
import ken_burns_path as kb

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT/'course-assets/wheres-the-line/wheres-the-line.mp4'
SOURCE = Path('/private/tmp/wheres-the-line-v3-source-848ac733.mp4')
EXPECTED = '848ac733051b1a1ad1856fbb60099b54e2978ce7651027d5f7e7575cad47ff51'
OUT = ROOT/'video-audit/wheres-the-line-repair-2026-09-30-v3'
DEST = ROOT/'Prompts/wheres-the-line-v3.mp4'
ASSETS = ROOT/'scripts/video/assets/wheres-the-line-v3'
TOTAL = 6059
FF = imageio_ffmpeg.get_ffmpeg_exe()
BOARDS = ROOT/'course-assets/wheres-the-line'
SPANS = {
    'offer': [3210, 3300], 'help': [3690, 3780],
    'response': [4023, 4251], 'affected': [4710, 4830],
    'protection': [5250, 5340],
}
DONORS = {'offer': [2130, 2220], 'help': [2640, 2730]}
BOUNDARIES = {2898:'Canonical two uses board',3915:'Return to retained phone',
              4370:'Canonical responsible choices board',5798:'Retained canonical close'}
for key,(a,b) in SPANS.items():
    BOUNDARIES[a] = key+' begins'
    BOUNDARIES[b] = key+' ends'


def audio_hash(path, decoded=False):
    args = ['-acodec','pcm_s16le','-f','s16le'] if decoded else ['-c:a','copy','-f','adts']
    p=subprocess.run([FF,'-v','error','-i',str(path),'-map','0:a:0','-vn',*args,'pipe:1'],check=True,capture_output=True)
    return hashlib.sha256(p.stdout).hexdigest()


def prepare():
    b=Build(ROOT,SOURCE,OUT,DEST)
    def target(label,frame,rect,color,dense=False):
        v=dict(label=label,at=frame/30,rects=[rect],color=color,radius=18)
        if dense:v['cam']=rect
        return v
    b.board('uses',BOARDS/'wheres-the-line-two-uses.jpg',2898,3915,'compact',[
        target('Targeted Promotions',3044,[40,127,783,917],'#4f2fc4'),
        target('Targeted Promotions outcome',3316,[56,762,767,901],'#4f2fc4'),
        target('Customer Protection',3522,[816,127,1559,917],'#0f7a4a'),
        target('Customer Protection outcome',3786,[832,762,1543,901],'#0f7a4a'),
    ],push=False)
    b.board('moves',BOARDS/'wheres-the-line-responsible-choice.jpg',4370,5798,'dense',[
        target('Consider Everyone Affected',4569,[40,127,783,716],'#4f2fc4',True),
        target('Be Clear With People',4907,[815,127,1559,716],'#1652f0',True),
        target('Build In Protection',5132,[40,750,783,1339],'#0e8f86',True),
        target('Own The Outcome',5408,[815,750,1559,1339],'#a9760c',True),
    ],pullback_at=5681/30,lead_camera=True)
    return b


class Board:
    def __init__(self,path):
        self.spec=json.loads(path.read_text())
        self.img=cv2.imread(self.spec['image']);self.h,self.w=self.img.shape[:2]
        self.big=cv2.resize(self.img,(self.w*3,self.h*3),interpolation=cv2.INTER_LANCZOS4)
        self.beats=kb.resolve(self.spec,16/9,1280,3)
        self.rings=kb.rings_for(self.spec);self.cache={}

    def frame(self,n):
        k=n
        for _,length,a,b in self.beats:
            if k<length:break
            k-=length
        else:raise ValueError(n)
        t=kb.smoothstep(k/(length-1)) if length>1 else 1
        cam=tuple(a[j]+(b[j]-a[j])*t for j in range(3))
        active=tuple(i for i,r in enumerate(self.rings) if r[0]<=n<r[1])
        key=cam+active
        if key in self.cache:return self.cache[key]
        x,y,w,h=kb.window(*cam,16/9,self.w,self.h)
        X,Y,W,H=[round(v*3) for v in (x,y,w,h)]
        frame=cv2.resize(self.big[Y:Y+H,X:X+W],(1280,720),interpolation=cv2.INTER_AREA)
        scale=1280/w;stroke=kb.ring_px(720)
        for i in active:
            _,_,(rx,ry,rw,rh),color,pad,radius=self.rings[i]
            half=stroke/2
            kb.draw_ring(frame,(rx-pad-x)*scale-half,(ry-pad-y)*scale-half,
                         (rx+rw+pad-x)*scale+half,(ry+rh+pad-y)*scale+half,
                         color,radius*scale+half,stroke)
        if a==b:self.cache[key]=frame
        return frame


def photo_frame(im,k,length):
    h,w=im.shape[:2]
    # Gentle push, all generation prompts use a safe area. No narrative timing changes.
    factor=1+0.015*kb.smoothstep(k/max(1,length-1))
    cw=min(w,h*16/9)/factor;ch=cw*9/16
    x=(w-cw)/2;y=(h-ch)/2
    matrix=np.array([[cw/1280,0,x],[0,ch/720,y]],dtype=np.float32)
    return cv2.warpAffine(im,matrix,(1280,720),flags=cv2.INTER_LANCZOS4|cv2.WARP_INVERSE_MAP)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    cv2.setNumThreads(2)
    assert sha(LIVE)==EXPECTED,'Installed source changed; re-evaluate before building.'
    if not SOURCE.exists():
        with SOURCE.open('wb') as f:
            subprocess.run(['git','show','000722b8:course-assets/wheres-the-line/wheres-the-line.mp4'],cwd=ROOT,stdout=f,check=True)
    assert sha(SOURCE)==EXPECTED,'Frozen source mismatch.'
    OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    b=prepare();boards={k:Board(OUT/f'leg-{k}.json') for k in ('uses','moves')}
    for key,frames in {'uses':[0,146,418,624,888],'moves':[0,199,537,762,1038,1311]}.items():
        for n in frames:cv2.imwrite(str(OUT/'preview'/f'{key}-{n:04}.jpg'),boards[key].frame(n))
    if args.prepare_only:return
    assert not DEST.exists(),'Never overwrite a review candidate.'
    photos={k:cv2.imread(str(ASSETS/(k+'.png'))) for k in ('affected','protection','response')}
    assert all(v is not None for v in photos.values()),'Generated assets missing.'
    protected={str(p):sha(p) for p in [SOURCE,LIVE,ROOT/'index.html',ROOT/'lessons/wheres-the-line.md',*BOARDS.glob('*.jpg'),*ASSETS.glob('*.png')]}
    proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30',
        '-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-profile:v','high',
        '-level:v','3.1','-crf','16','-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy',
        '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    donors={key:[] for key in DONORS};written=0
    wants={f+d for f in BOUNDARIES for d in (-1,0,15)}|{3044,3316,3522,3786,4569,4907,5132,5408,5681,TOTAL-1}
    with av.open(str(SOURCE)) as c:
        stream=c.streams.video[0];stream.codec_context.thread_count=2
        assert str(stream.average_rate)=='30'
        for n,frame in enumerate(c.decode(video=0)):
            assert frame.format.name=='yuv420p' and (frame.width,frame.height)==(1280,720)
            raw=frame.to_ndarray(format='yuv420p')
            for key,(a,z) in DONORS.items():
                if a<=n<z:donors[key].append(raw.copy())
            insert=None
            if 2898<=n<3915:insert=boards['uses'].frame(n-2898)
            elif 4370<=n<5798:insert=boards['moves'].frame(n-4370)
            for key,(a,z) in SPANS.items():
                if a<=n<z:
                    if key in donors:
                        assert len(donors[key])==z-a
                        raw=donors[key][n-a];insert=None
                    else:insert=photo_frame(photos[key],n-a,z-a)
                    break
            if insert is not None:raw=av.VideoFrame.from_ndarray(insert,format='bgr24').to_ndarray(format='yuv420p')
            if n in wants:
                im=av.VideoFrame.from_ndarray(raw,format='yuv420p').to_ndarray(format='bgr24')
                cv2.imwrite(str(OUT/'preview'/f'{n:06}.jpg'),im)
            proc.stdin.write(raw.tobytes());written+=1
            if written%1500==0:print(f'Rendered {written}/{TOTAL}',flush=True)
    proc.stdin.close();assert proc.wait()==0 and written==TOTAL
    assert audio_hash(SOURCE)==audio_hash(DEST)
    assert audio_hash(SOURCE,True)==audio_hash(DEST,True)
    assert all(sha(Path(p))==v for p,v in protected.items())
    manifest=dict(candidate=str(DEST),candidate_sha256=sha(DEST),source=str(SOURCE),source_sha256=EXPECTED,
        scope='Approved visual repair; original audio preserved. Wording at 2:22 unresolved: no available donor.',
        source_limitation='Only finished source survives; one video encode, source YUV preserved outside changed spans.',
        fps=30,total_frames=TOTAL,duration=TOTAL/30,spans=SPANS,donors=DONORS,boards=b.boards,
        boundaries=[dict(frame=f,label=s) for f,s in sorted(BOUNDARIES.items())],protected_hashes=protected,
        protected_files_unchanged=True,audio_packets_identical=True,decoded_audio_identical=True,
        longest_board_run_seconds={'uses':13.0,'moves':15.2666666667},
        generated_assets={k:str(ASSETS/(k+'.png')) for k in photos},
        listening='Not auditioned. Exact source audio retained; source issues not certified fixed.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',DEST,flush=True)


if __name__=='__main__':main()
