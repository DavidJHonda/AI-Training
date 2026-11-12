"""Render the approved three-roll Training Bias candidate. Source times are seconds."""
import json
import subprocess
import tempfile
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, W, H, FPS, SR, SPF, fr, sha
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, ring_px
from make_close_board import compose_canonical_for_video

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'course-assets/training-bias'
AUDIT = ROOT / 'video-audit/training-bias-v12-2026-11-12'
OUT = ROOT / 'Prompts/training-bias-v12.mp4'
ROLL = {i: ROOT / f'Prompts/training-bias-{i}.mp4' for i in (1, 2, 3)}
FF = imageio_ffmpeg.get_ffmpeg_exe()
# Each entry is continuous audio. Round each cut onto the 30 fps delivery grid.
SOUND = [(2, 0, 87.03), (2, 93.00, 117.22), (1, 118.48, 123.19),
         (2, 138.52, 171.03), (2, 177.46, 184.80)]
# Picture rows use the sound clip's source clock, independently of picture roll.
# Movie spans have independent start/end times to retime transitions to the words.
PICTURE = [
    [(0,       'student at desk', 3, 0, 6.30),
     (5.96,    'science teacher', 3, 6.30, 295/30),
     (8.40,    'mom and shift', 3, 295/30, 13.90),
     (11.63,   'best friend', 3, 13.90, 17.90),
     (15.63,   'three answers to teacher-only training', 2, 15.63, 50.50),
     (50.50,   'two types overview and first card', 'types'),
     (63.35,   'teacher-only input illustration', 1, 41.93, 51.23),
     (72.65,   'left-out students card', 'types')],
    [(93.00,   'student approaches laptop', 3, 114.64, 118.30),
     (96.63,   'ten entrepreneur results build', 1, 102.19, 108.55),
     (106.15,  'student questions the result', 3, 130.20, 136.75),
     (111.16,  'outside-tech follow-up', 3, 138.42, 145.02)],
    [(118.48,  'observable list under evidence line', 1, 105.42, 108.55)],
    [(138.52,  'three questions', 'questions'),
     (158.23,  'asking for other industries', 1, 114.90, 118.36),
     (163.28,  'missing perspectives in training', 1, 47.75, 55.50)],
    [(177.46,  'canonical close', 'close')],
]
ACCENTS = ['#4f2fc4', '#1652f0', '#a9760c']
BOARD = {
    'types': ('study-time', [(40,118,784,874),(816,118,1560,874)], [58.77,72.65]),
    'questions': ('when-you-suspect', [(40,128,525,652),(557,128,1042,652),(1075,128,1560,652)], [144.89,148.49,153.99]),
}


def pcm(roll):
    raw = subprocess.check_output([FF,'-v','error','-i',str(ROLL[roll]),'-vn','-ac','1','-ar',str(SR),'-f','f32le','-'])
    return np.frombuffer(raw, dtype='<f4')


def spoken_rms(samples):
    blocks = samples[:len(samples)//480*480].reshape(-1,480)
    energy = np.mean(blocks**2,axis=1)
    return float(np.sqrt(np.mean(energy[energy > 10**(-38/10)])))


def render_audio(work):
    src={r:pcm(r) for r in (1,2)}
    ref=src[2][fr(111.23)*SPF:fr(116.79)*SPF]
    donor=src[1][fr(118.86)*SPF:fr(122.78)*SPF]
    gain=min(spoken_rms(ref)/spoken_rms(donor),.96/max(abs(donor)))
    pieces=[]
    for r,a,b in SOUND:
        buf=src[r][fr(a)*SPF:fr(b)*SPF].copy()
        if r==1: buf*=gain
        # Fade only at cut boundaries in existing speech gaps. Preserve the opening consonant.
        ramp=np.linspace(0,1,240)
        if pieces: buf[:240]*=ramp
        buf[-240:]*=ramp[::-1]
        pieces.append(buf)
    samples=np.concatenate(pieces)
    samples.tofile(work/'mix.f32')
    return len(samples)//SPF,float(20*np.log10(gain))


def camera(image,cx,cy,width):
    height=width*H/W
    x=np.clip(cx-width/2,0,max(0,image.shape[1]-width))
    y=np.clip(cy-height/2,0,max(0,image.shape[0]-height))
    matrix=np.float32([[width/W,0,x],[0,height/H,y]])
    return cv2.warpAffine(image,matrix,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE),x,y


def ease(q):
    q=np.clip(q,0,1)
    return q*q*(3-2*q)


class IllustratedBoard:
    def __init__(self,build,key):
        stem,rects,onsets=BOARD[key]
        path,w,h,ox,oy=build.compose(ASSETS/f'training-bias-{stem}.jpg',key)
        self.image=cv2.imread(str(path))
        self.rects=np.array(rects)+np.array([ox,oy,ox,oy])
        self.starts=[fr(t) for t in onsets]
        self.full=np.array([w/2,h/2,float(w)])
        # The example cards benefit from a modest dive. Keep the three short prompts at full view.
        zoom=min(w,max(Build.fit_w(x1-x0,y1-y0) for x0,y0,x1,y1 in self.rects))
        self.views=[np.array([(x0+x1)/2,(y0+y1)/2,zoom]) for x0,y0,x1,y1 in self.rects]
        self.key=key
        self.cache={}
    def frame(self,sf):
        i=sum(s<=sf for s in self.starts)-1
        step=min(24,sf-self.starts[i]) if i>=0 else 0
        if self.key=="questions" or (self.key=="types" and i==1):
            step=24
        key=(i,step)
        if key not in self.cache:
            view=self.full
            if i>=0 and self.key!="questions":
                prior=self.views[i-1] if i else self.full
                view=prior+(self.views[i]-prior)*ease(step/24)
            pic,x,y=camera(self.image,*view)
            if i>=0:
                x0,y0,x1,y1=self.rects[i]; scale=W/view[2]; half=ring_px(H)/2
                draw_ring(pic,(x0-x)*scale-half,(y0-y)*scale-half,(x1-x)*scale+half,(y1-y)*scale+half,hex_bgr(ACCENTS[i]),14*scale+half,ring_px(H))
            # Cache only the sustained views; moving frames are visited once.
            if i<0 or step==24: self.cache[key]=pic
            return pic
        return self.cache[key]


def main():
    if OUT.exists(): raise FileExistsError(OUT)
    cv2.setNumThreads(2)
    AUDIT.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        work=Path(temp)
        build=Build(ROOT,ROLL[2],work,OUT)
        boards={k:IllustratedBoard(build,k) for k in BOARD}
        compose_canonical_for_video(ASSETS/'training-bias-close.jpg',work/'close.png','#ffffff')
        close=cv2.imread(str(work/'close.png'))
        total,db=render_audio(work)
        args=[FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
              '-f','f32le','-ar',str(SR),'-ac','1','-i',str(work/'mix.f32'),'-c:v','libx264','-pix_fmt','yuv420p',
              '-crf','17','-preset','fast','-threads','4','-c:a','aac','-b:a','192k','-movflags','+faststart',str(work/'encoded.mp4')]
        proc=subprocess.Popen(args,stdin=subprocess.PIPE)
        mask=glyph_mask(); frame=0; rows=[]
        try:
            for (audio,a,b),shots in zip(SOUND,PICTURE):
                assert fr(shots[0][0])==fr(a)
                for j,(t,label,src,*movie) in enumerate(shots):
                    end=fr(shots[j+1][0]) if j+1<len(shots) else fr(b)
                    n=end-fr(t); assert n>0
                    rows.append(dict(start=frame,end=frame+n,label=label,sound=audio,sound_in=fr(t)/FPS,visual=src,source_picture=movie))
                    if movie:
                        lo,hi=map(fr,movie);cap=cv2.VideoCapture(str(ROLL[src]))
                        cap.set(cv2.CAP_PROP_POS_FRAMES,lo); current=lo-1
                    for k in range(n):
                        if movie:
                            goal=lo+k*(hi-lo)//n
                            while current<goal:
                                ok,raw=cap.read();assert ok;current+=1
                            pic,_=clean_frame(raw,mask)
                        elif src=='close':
                            z=1+.2*ease((k-48)/149)
                            pic,_,_=camera(close,close.shape[1]/2,close.shape[0]/2,close.shape[1]/z)
                        else: pic=boards[src].frame(fr(t)+k)
                        proc.stdin.write(pic.tobytes())
                    if movie: cap.release()
                    frame+=n
                    print(f'{frame/30:.2f}s  {label}',flush=True)
        finally: proc.stdin.close()
        if proc.wait() or frame!=total: raise RuntimeError('Incomplete encode')
        # Publish candidate only after the complete temporary encode exists.
        import shutil
        with OUT.open('xb') as target, (work/'encoded.mp4').open('rb') as source: shutil.copyfileobj(source,target)
        manifest=dict(candidate=str(OUT.relative_to(ROOT)),frames=total,seconds=total/FPS,sha256=sha(OUT),
                      sources={str(p.relative_to(ROOT)):sha(p) for p in [*ROLL.values(),*(ASSETS/f'training-bias-{stem}.jpg' for stem in ('study-time','when-you-suspect','close'))]},
                      donor_gain_db=db,sound=SOUND,rows=rows)
        (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__': main()
