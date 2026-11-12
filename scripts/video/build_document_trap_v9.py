"""Repair the flash, narrate the canonical tip cards, and animate the two boards."""
import json
import subprocess
import tempfile
import wave
from shutil import copyfileobj
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, CLOSE_PREHOLD, CLOSE_PUSH, CLOSE_TAIL, FPS, H, SPF, SR, W, sha
from ken_burns_path import draw_ring, hex_bgr, ring_px, smoothstep
from make_close_board import compose_canonical_for_video

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'course-assets/document-trap'
AUDIT = ROOT / 'video-audit/document-trap-v9-2026-11-12'
BASE = ROOT / 'Prompts/document-trap-v8.mp4'
ROLL = ROOT / 'Prompts/document-trap-2.mp4'
OUT = ROOT / 'Prompts/document-trap-v9.mp4'
FF = imageio_ffmpeg.get_ffmpeg_exe()
# V8 frames. The spurious transition starts at 2524 and lasts through 2539.
FLASH, COMPARISON = 2524, 2540
OVERVIEW, FIRST_TIP, CAVEAT, CLOSE, END = 3262, 3533, 4366, 5026, 5208
# Original title readings in roll 2; subsequent WAVs read the corresponding canonical body.
CARDS = [
    ('Name the Section', 'Use the document’s own headings and keywords.',
     (139.26,142.19), (40,128,784,679), '#4f2fc4'),
    ('Ask One Thing', 'Give retrieval one clear target at a time.',
     (148.04,150.26), (816,128,1560,679), '#1652f0'),
    ('Share What Matters', 'Paste the exact passage or upload only the relevant section.',
     (157.30,159.54), (40,708,784,1259), '#0e8f86'),
    ('Ask for the Quote', 'Ask AI to quote the exact passage, then compare it with the original.',
     (166.09,168.83), (816,708,1560,1259), '#a9760c'),
]


def read_pcm(path):
    raw = subprocess.check_output([FF,'-v','error','-i',str(path),'-vn','-ac','1','-ar',str(SR),'-f','f32le','-'])
    return np.frombuffer(raw, dtype='<f4')


def active_rms(samples):
    blocks = samples[:len(samples)//480*480].reshape(-1,480)
    energies = np.mean(blocks**2,axis=1)
    return np.sqrt(np.mean(energies[energies > 10**(-36/10)]))


def assemble_voice():
    base, roll = read_pcm(BASE), read_pcm(ROLL)
    pieces = [base[:FIRST_TIP*SPF]]
    cursor = FIRST_TIP
    rows = []
    for index, (title,body,(a,b),_,_) in enumerate(CARDS,1):
        heading = roll[round(a*SR):round(b*SR)].copy()
        pickup_path = AUDIT / 'pickups' / f'body-{index}.wav'
        speech = read_pcm(pickup_path).copy()
        # Preserve consonants and add the same short breathing space after each tip.
        energy = np.sqrt(np.mean(speech[:len(speech)//480*480].reshape(-1,480)**2,axis=1))
        voiced = np.where(energy > .003)[0]
        assert voiced.size
        speech = speech[max(0,(voiced[0]-6)*480):min(len(speech),(voiced[-1]+11)*480)]
        source_level = active_rms(roll[round(139.55*SR):round(147.77*SR)])
        gain = min(source_level / active_rms(speech), .975/max(abs(speech)))
        speech *= gain
        fade = np.linspace(0,1,240)
        for part in (heading,speech):
            part[:240] *= fade
            part[-240:] *= fade[::-1]
        sound = np.concatenate([heading,speech])
        length = int(np.ceil(len(sound)/SPF)) + 12
        rows.append(dict(title=title,body=body,start=cursor,body_at=cursor+len(heading)/SPF,
                         end=cursor+length,original_heading_seconds=[a,b],
                         pickup=str(pickup_path.relative_to(ROOT)),gain_db=float(20*np.log10(gain))))
        pieces.append(np.pad(sound,(0,length*SPF-len(sound))))
        cursor += length
    pieces.append(base[CAVEAT*SPF:END*SPF])
    # Production close: 48 frames full size + 150 pushing + 120 at its settled size.
    close_frames = CLOSE_PREHOLD + CLOSE_PUSH + CLOSE_TAIL
    pieces.append(np.zeros((close_frames-(END-CLOSE))*SPF,np.float32))
    return np.concatenate(pieces),rows,cursor+(CLOSE-CAVEAT)


def crop(image,view):
    cx,cy,width = view
    height=width*H/W
    left,top = cx-width/2,cy-height/2
    affine = np.float32([[width/W,0,left],[0,height/H,top]])
    frame=cv2.warpAffine(image,affine,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_CUBIC,
                         borderMode=cv2.BORDER_REPLICATE)
    return frame,left,top


class TipsCamera:
    def __init__(self,work,rows):
        build=Build(ROOT,BASE,work,OUT)
        path,w,h,ox,oy=build.compose(ASSETS/'document-trap-moves.jpg','four-tips')
        self.board=cv2.imread(str(path))
        self.rows=rows
        self.layout=np.array([w/2,h/2,float(w)])
        self.views=[self.layout]
        self.stages=[self.board]
        self.rects=[]
        self.settled={}
        for _,_,_,bounds,_ in CARDS:
            x0,y0,x1,y1=np.array(bounds)+[ox,oy,ox,oy]
            self.rects.append((x0,y0,x1,y1))
            self.views.append(np.array([(x0+x1)/2,(y0+y1)/2,Build.fit_w(x1-x0,y1-y0)]))
            stage=np.empty_like(self.board)
            stage[:]=self.board[oy+100,ox+12]
            stage[y0-5:y1+5,x0-5:x1+5]=self.board[y0-5:y1+5,x0-5:x1+5]
            self.stages.append(stage)

    def frame(self,number):
        # Start in the space before each numbered cue. Settle on its label
        # before the narrator starts the explanatory sentence.
        index=sum(number>=r['start']-5 for r in self.rows)
        if index==0:
            return self.hold(0)
        start=self.rows[index-1]['start']-5
        u=min(1.,(number-start)/34)
        if u==1: return self.hold(index)
        progress=smoothstep(u)
        view=self.views[index-1]+progress*(self.views[index]-self.views[index-1])
        frame,_,_=crop(self.board,view)
        # Neighbouring cards are visible during the pan. Fade their cropped
        # edges away on arrival so only complete instructional text stays up.
        if u<.30 and index>1:
            prior=self.render_card(index-1,view)
            q=smoothstep(u/.30)
            frame=cv2.addWeighted(prior,1-q,frame,q,0)
        if u>.62:
            target=self.render_card(index,view)
            q=smoothstep((u-.62)/.38)
            frame=cv2.addWeighted(frame,1-q,target,q,0)
        return frame

    def render_card(self,index,view):
        frame,left,top=crop(self.stages[index],view)
        if index:
            x0,y0,x1,y1=self.rects[index-1]
            scale=W/view[2]
            stroke=ring_px(H)
            half=stroke/2
            draw_ring(frame,(x0-left)*scale-half,(y0-top)*scale-half,(x1-left)*scale+half,
                      (y1-top)*scale+half,hex_bgr(CARDS[index-1][4]),14*scale+half,stroke)
        return frame

    def hold(self,index):
        if index not in self.settled:
            self.settled[index]=self.render_card(index,self.views[index])
        return self.settled[index]


def main():
    if OUT.exists(): raise FileExistsError(OUT)
    cv2.setNumThreads(2)
    voice,rows,close_start=assemble_voice()
    # A standalone audition of the final mix lets the editor hear each original
    # heading followed by its matched pickup without scrubbing the whole movie.
    audition=voice[FIRST_TIP*SPF:rows[-1]['end']*SPF]
    with wave.open(str(AUDIT/'four-tips-narration.wav'),'wb') as wav:
        wav.setparams((1,2,SR,0,'NONE','not compressed'))
        wav.writeframes(np.round(np.clip(audition,-1,1)*32767).astype('<i2').tobytes())
    total=len(voice)//SPF
    assert len(voice)==total*SPF
    with tempfile.TemporaryDirectory() as temp:
        work=Path(temp)
        tips=TipsCamera(work,rows)
        compose_canonical_for_video(ASSETS/'document-trap-close.jpg',work/'close.png','#ffffff')
        close=cv2.imread(str(work/'close.png'))
        height,width=close.shape[:2]
        raw=work/'voice.f32'
        voice.tofile(raw)
        encoded=work/'candidate.mp4'
        args=[FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:',
              '-f','f32le','-ar',str(SR),'-ac','1','-i',str(raw),'-c:v','libx264','-crf','17',
              '-threads','4','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(encoded)]
        proc=subprocess.Popen(args,stdin=subprocess.PIPE)
        cap=cv2.VideoCapture(str(BASE))
        cap.set(1,COMPARISON+2)
        ok,comparison=cap.read()
        assert ok
        cap.set(1,0)
        try:
            for number in range(total):
                if number<OVERVIEW or rows[-1]['end']<=number<close_start:
                    if number==rows[-1]['end']:
                        cap.set(1,CAVEAT)
                    ok,frame=cap.read()
                    assert ok,number
                    if FLASH<=number<COMPARISON:
                        frame=comparison
                elif number<close_start:
                    frame=tips.frame(number)
                else:
                    k=number-close_start
                    u=np.clip((k-CLOSE_PREHOLD)/(CLOSE_PUSH-1),0,1)
                    zoom=1+.2*smoothstep(u)
                    frame,_,_=crop(close,[width/2,height/2,width/zoom])
                proc.stdin.write(frame.tobytes())
        finally:
            cap.release()
            proc.stdin.close()
        if proc.wait(): raise RuntimeError('Video encode failed')
        with OUT.open('xb') as dest, encoded.open('rb') as source:
            copyfileobj(source,dest)
    manifest=dict(candidate=str(OUT.relative_to(ROOT)),seconds=total/FPS,frames=total,
                  sha256=sha(OUT),flash_removed_frames=[FLASH,COMPARISON],tips=rows,
                  close_start=close_start,close_frames=[CLOSE_PREHOLD,CLOSE_PUSH,CLOSE_TAIL],
                  sources={str(p.relative_to(ROOT)):sha(p) for p in [BASE,ROLL,ASSETS/'document-trap-close.jpg',
                           ASSETS/'document-trap-moves.jpg',*sorted((AUDIT/'pickups').glob('*.wav'))]})
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'{OUT} {total/FPS:.2f}s')

if __name__=='__main__': main()
