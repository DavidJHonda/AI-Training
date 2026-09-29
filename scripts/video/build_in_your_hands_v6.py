#!/usr/bin/env python3
"""Authorized visual refresh. One encode, untouched audio, review candidate only."""
from pathlib import Path
import sys, json, hashlib, subprocess, types
import cv2
import numpy as np
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
import ken_burns_path as kb
from editspec_build import Build

OUT = ROOT / 'video-audit/in-your-hands-build-2026-09-29-v6'
SRC = ROOT / 'course-assets/in-your-hands/in-your-hands.mp4'
DEST = ROOT / 'Prompts/in-your-hands-v6.mp4'
EXPECTED = 'da5e5302dc17c0243d3071360e30122e581a19bc52409e20a473899a84fab842'
FPS, TOTAL = 30, 5508
CUTS = [(2340,2526,'testing-tools'), (3030,3114,'make-something'),
        (3870,4038,'testing-tools'), (4290,4500,'think-first'),
        (4710,4860,'make-something')]
FF = imageio_ffmpeg.get_ffmpeg_exe()

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def audiohash(p):
    data = subprocess.check_output([FF,'-v','error','-i',str(p),'-map','0:a','-c','copy','-f','data','-'])
    return hashlib.sha256(data).hexdigest()

class Board:
    def __init__(self, asset, old_spec, key, n):
        canvas, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=OUT,tall_margin=False),asset,key)
        self.spec = json.loads(old_spec.read_text())
        self.spec['image'] = str(canvas)
        if key == 'moves':
            assert (cw,ch,ox,oy)==(1686,950,43,1)
            self.spec['beats'][0]['frames'] = n
            self.spec['rings'][-1]['end'] = n
        else:
            assert (cw,ch,ox,oy)==(2382,1340,391,0)
        self.image=cv2.imread(str(canvas))
        self.big=cv2.resize(self.image,(cw*3,ch*3),interpolation=cv2.INTER_LANCZOS4)
        self.beats=kb.resolve(self.spec,16/9,1280,3)
        self.rings=kb.rings_for(self.spec)
        self.cache={}
        (OUT/f'leg-{key}.json').write_text(json.dumps(self.spec,indent=2)+'\n')
    def render(self,f):
        offset=0
        for _,n,a,b in self.beats:
            if f<offset+n:
                t=kb.smoothstep((f-offset)/(n-1)) if n>1 else 1
                camera=tuple(a[j]+(b[j]-a[j])*t for j in range(3))
                break
            offset+=n
        else:
            raise ValueError(f)
        active=tuple(i for i,r in enumerate(self.rings) if r[0]<=f<r[1])
        key=(camera,active)
        if key in self.cache:return self.cache[key]
        ih,iw=self.image.shape[:2]
        x,y,w,h=kb.window(*camera,16/9,iw,ih)
        X,Y,W,H=[round(z*3) for z in (x,y,w,h)]
        # Supersample the post-camera ring, keeping its width fixed at 4 output pixels.
        frame=cv2.resize(self.big[Y:Y+H,X:X+W],(2560,1440),interpolation=cv2.INTER_AREA)
        scale=2560/w
        thick=kb.ring_px(1440)
        for i in active:
            _,_,rect,color,pad,radius=self.rings[i]
            rx,ry,rw,rh=rect; half=thick/2
            kb.draw_ring(frame,(rx-pad-x)*scale-half,(ry-pad-y)*scale-half,
                         (rx+rw+pad-x)*scale+half,(ry+rh+pad-y)*scale+half,
                         color,radius*scale+half,thick)
        frame=cv2.resize(frame,(1280,720),interpolation=cv2.INTER_AREA)
        if len(self.cache)<160:self.cache[key]=frame
        return frame

def illustration(img, local, n):
    h,w=img.shape[:2]
    fit_w=min(w,h*16/9)
    # Modest 2% push. Subject-safe framing is checked in the preview and encoded output.
    width=fit_w/(1+.02*kb.smoothstep(local/max(1,n-1)))
    height=width*9/16
    x,y=(w-width)/2,(h-height)/2
    M=np.array([[1280/width,0,-x*1280/width],[0,720/height,-y*720/height]],np.float32)
    return cv2.warpAffine(img,M,(1280,720),flags=cv2.INTER_CUBIC)

def main():
    preview='--preview' in sys.argv
    OUT.mkdir(exist_ok=True)
    assert sha(SRC)==EXPECTED,'Source changed; do not build against stale timings'
    if not preview:assert not DEST.exists(),'Never overwrite an existing review candidate'
    assets=ROOT/'course-assets/in-your-hands'
    b1=Board(assets/'in-your-hands-in-or-out.jpg',ROOT/'video-audit/in-your-hands-column-walk-2026-09-25/leg-1-hands.json','hands',2445)
    b2=Board(assets/'in-your-hands-three-choices.jpg',ROOT/'video-audit/what-you-can-control-repair-2026-09-16/leg-2-three-moves.json','moves',1542)
    images={name:cv2.imread(str(OUT/'assets'/f'{name}.png')) for name in {c[2] for c in CUTS}}
    assert all(im is not None for im in images.values()),'Missing generated illustration'
    def render(f,original):
        for a,b,name in CUTS:
            if a<=f<b:return illustration(images[name],f-a,b-a)
        if 1059<=f<3504:return b1.render(f-1059)
        if 3504<=f<5046:return b2.render(f-3504)
        return original
    boundaries={1059:'board1',3504:'board2',5046:'close'}
    for a,b,name in CUTS:boundaries[a]=f'{name}-in';boundaries[b]=f'{name}-out'
    for start,board in [(1059,b1),(3504,b2)]:
        for r in board.spec['rings']:
            f=start+r['start']
            if not any(a<=f<b for a,b,_ in CUTS):boundaries.setdefault(f,'ring-change')
    selected={0,768,5507}
    for f in boundaries:selected.update([f-1,f,f+1,f+20])
    for a,b,_ in CUTS:selected.add((a+b)//2)
    cap=cv2.VideoCapture(str(SRC)); idx=0
    target=OUT/('preview' if preview else 'encoded');target.mkdir(exist_ok=True)
    proc=None
    if not preview:
        proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-',
                               '-i',str(SRC),'-map','0:v','-map','1:a','-c:v','libx264','-crf','16','-preset','medium',
                               '-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    while True:
        ok,original=cap.read()
        if not ok:break
        if not preview or idx in selected:
            frame=render(idx,original)
            if preview and idx in selected:cv2.imwrite(str(target/f'{idx:05d}.jpg'),frame)
            if proc:proc.stdin.write(frame.tobytes())
        idx+=1
        if idx%900==0:print('frame',idx,flush=True)
    cap.release();assert idx==TOTAL
    if proc:
        proc.stdin.close();assert proc.wait()==0
    manifest={'source':str(SRC),'source_sha256':EXPECTED,'candidate':str(DEST),'fps':FPS,'frames':TOTAL,'duration':TOTAL/FPS,
              'scope':'visual-only review build; audio unchanged; not shipped',
              'cutaways':[{'start_frame':a,'end_frame':b,'start':a/30,'end':b/30,'asset':str(OUT/'assets'/f'{name}.png')} for a,b,name in CUTS],
              'assets':{str(p):sha(p) for p in [assets/'in-your-hands-in-or-out.jpg',assets/'in-your-hands-three-choices.jpg',*[OUT/'assets'/f'{k}.png' for k in images]]},
              'boundaries':[{'frame':f,'label':label} for f,label in sorted(boundaries.items())],
              'longest_unbroken_board_seconds':42.7,'ring_output_pixels':4,'density':{'hands':'dense, owner-approved white-column framing','moves':'compact'},
              'retained_notebook_seconds':[0,35.3],'close_preserved_seconds':[168.2,183.6]}
    if proc:
        cap=cv2.VideoCapture(str(DEST)); count=0
        while True:
            ok,frame=cap.read()
            if not ok:break
            if count in selected:cv2.imwrite(str(target/f'{count:05d}.jpg'),frame)
            count+=1
        cap.release();assert count==TOTAL
        manifest.update(candidate_sha256=sha(DEST),decoded_frames=count,audio_payload_sha256=audiohash(DEST),audio_packets_identical=audiohash(SRC)==audiohash(DEST))
        assert manifest['audio_packets_identical']
        assert sha(SRC)==EXPECTED
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('PREVIEW COMPLETE' if preview else 'BUILD COMPLETE',str(DEST),flush=True)

if __name__=='__main__':main()
