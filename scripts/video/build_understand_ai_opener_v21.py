#!/usr/bin/env python3
"""Approved roll-1 animated hybrid. Edited AAC and existing ending copied."""
from pathlib import Path
import argparse,hashlib,json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw,ImageFont
from gemini_mark import BOX,PAD,BAND,FEATHER,THRESH,clean_corner,inpaint_corner,glyph_mask,_band

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/understand-ai-opener-v20.mp4'
DONOR=ROOT/'Prompts/Understand-opener-1.mp4'
DEST=ROOT/'Prompts/understand-ai-opener-v21.mp4'
OUT=ROOT/'video-audit/understand-opener-v21-2026-11-11'
FF=imageio_ffmpeg.get_ffmpeg_exe();FPS=30;TOTAL=2307;TAIL_START=1239
FONT=ImageFont.truetype(str(ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'),17)
# Half-open source/output frame intervals. All source motion is played, retimed
# only enough to follow the approved narration. No inserted freeze frames.
SHOTS=[
 dict(key='expert-error-animation',start=0,end=298,source_start=0,source_end=271,reason='Complex construction versus square block at round hole'),
 dict(key='central-question',start=298,end=377,source_start=271,source_end=362,reason='Question mark at How can the same tool do both'),
 dict(key='three-exclusions',start=377,end=502,source_start=468,source_end=633,reason='Not magic, a person, or ordinary software'),
 dict(key='look-inside',start=502,end=659,source_start=640,source_end=865,reason='Simple animated internal-network illustration'),
 dict(key='steering',start=659,end=724,source_start=865,source_end=956,reason='Think about driving a car'),
 dict(key='pedals',start=724,end=804,source_start=956,source_end=1078,reason='Using the controls without opening the hood'),
 dict(key='breakdown',start=804,end=879,source_start=1078,source_end=1236,reason='Failure gives the analogy a concrete problem'),
 dict(key='warning-light',start=879,end=960,source_start=1236,source_end=1356,reason='Knowing limits and why something goes wrong'),
 dict(key='under-the-hood',start=960,end=1239,source_start=1356,source_end=1572,reason='Inspecting underneath; connects car to AI and Be Smarter benefit'),
]


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(args):subprocess.run([FF,'-hide_banner','-loglevel','warning',*map(str,args)],check=True)
def source_frame(shot,f):
 q=(f-shot['start'])/max(1,shot['end']-shot['start']-1)
 return shot['source_start']+round(q*(shot['source_end']-shot['source_start']-1))


def correct_label(frame):
    # Targeted code-native video caption correction; source card/reveals stay.
    # Follow the source caption's slight camera motion and fade using its ink.
    out=frame.copy();x0,y0,x1,y1=890,456,1050,512
    patch=out[y0:y1,x0:x1].copy();gray=cv2.cvtColor(patch,cv2.COLOR_BGR2GRAY)
    lo,hi=np.percentile(gray,[5,95]);mask=gray<(lo+hi)/2
    yy,xx=np.where(mask)
    cx=x0+float(np.mean(xx)) if len(xx) else 968.;cy=y0+float(np.mean(yy)) if len(yy) else 479.
    ink=tuple(int(v) for v in np.percentile(patch.reshape(-1,3),5,axis=0))
    donor=out[y0:y1,1054:1090].copy()
    out[y0:y1,x0:x1]=cv2.resize(donor,(x1-x0,y1-y0),interpolation=cv2.INTER_LINEAR)
    if hi-lo>3:
        pil=Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(pil)
        d.text((cx,cy),'ORDINARY SOFTWARE',font=FONT,anchor='mm',fill=ink[::-1])
        out=cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)
    return out


class CornerCleaner:
    """Reuse a verified paper donor offset; search again only when it fails."""
    def __init__(self):
        self.mask=glyph_mask();self.offsets={};self.counts=dict(cloned=0,inpainted=0,reused_verified_offset=0)
        self.alpha=np.ones((BOX[3]-BOX[1],BOX[2]-BOX[0]),np.float32)
        ramp=np.linspace(0,1,FEATHER,dtype=np.float32)
        self.alpha[:FEATHER]*=ramp[:,None];self.alpha[-FEATHER:]*=ramp[::-1][:,None]
        self.alpha[:,:FEATHER]*=ramp[None,:];self.alpha[:,-FEATHER:]*=ramp[None,::-1]
    def clean(self,frame,key):
        padded=cv2.copyMakeBorder(frame,PAD,PAD,PAD,PAD,cv2.BORDER_REFLECT)
        x0,y0,x1,y1=(v+PAD for v in BOX);off=self.offsets.get(key)
        if off is not None:
            dx,dy=off
            score=float(np.abs(_band(padded,x0,y0,x1,y1)-_band(padded,x0+dx,y0+dy,x1+dx,y1+dy)).mean())
            if score<=THRESH:
                donor=padded[y0+dy:y1+dy,x0+dx:x1+dx].astype(float)
                original=padded[y0:y1,x0:x1].astype(float);alpha=self.alpha[:,:,None]
                padded[y0:y1,x0:x1]=(donor*alpha+original*(1-alpha)).round().astype(np.uint8)
                self.counts['cloned']+=1;self.counts['reused_verified_offset']+=1
                return padded[PAD:-PAD,PAD:-PAD]
        cleaned,score,off=clean_corner(frame)
        if off is not None:
            self.offsets[key]=off;self.counts['cloned']+=1;return cleaned
        assert self.mask is not None
        self.counts['inpainted']+=1;return inpaint_corner(frame,self.mask)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');a=ap.parse_args()
    assert not DEST.exists(),'Never overwrite a review candidate.'
    assert sha(SRC)=='442a61c664222582db9869fad4e1bd12aa686450f61283a7314f3c0045197eb9'
    assert sha(DONOR)=='6f38be6458fe2f5e894f17aabb8ff60b41634e402194bb606bb605cb617acfd5'
    OUT.mkdir(exist_ok=True);(OUT/'states').mkdir(exist_ok=True)
    protected=[SRC,DONOR,ROOT/'index.html',ROOT/'lessons/Opener-Understand.md',ROOT/'course-assets/understand-ai-opener/understand-ai-opener.mp4',ROOT/'course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg',ROOT/'course-assets/understand-ai-opener/understand-ai-opener-close.jpg']
    hashes={str(p):sha(p) for p in protected}
    mapping=[]
    for f in range(TAIL_START):
        shot=next(s for s in SHOTS if s['start']<=f<s['end']);mapping.append(source_frame(shot,f))
    assert all(b>=a for a,b in zip(mapping,mapping[1:]))
    manifest=dict(source=str(SRC),picture_donor=str(DONOR),output=str(DEST),fps=30,width=1280,height=720,total_frames=TOTAL,duration=TOTAL/30,
        authorization='User: Go ahead with the hybrid. Use version 1’s opening and car sequences with the edited narration, keeping the question board and standard close. Prepare a new version for review.',
        scope='Visual-only animated hybrid; review only, no installation or publishing',shots=SHOTS,changed_picture_frames=[0,1239],retained_picture_frames=[1239,2307],retained_words_to_answer=[1239,1658],retained_question_board=[1658,1989],retained_standard_close=[1989,2307],
        audio='Entire v20 AAC stream copied with no changes',label_correction='SOFTWARE -> ORDINARY SOFTWARE; source caption position, ink and fade followed',
        protected_hashes=hashes,boundaries=[dict(frame=s['start'],label=s['key']) for s in SHOTS[1:]]+[dict(frame=1239,label='Retained words-to-answer scene'),dict(frame=1658,label='Retained question board'),dict(frame=1989,label='Retained standard close')],
        narration_cuts_added=0,pauses_added=0,direct_listening_repeated=False,continuous_real_time_motion_review_performed=False,installed=False)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    np.save(OUT/'donor-frame-map.npy',np.array(mapping,dtype=np.int32))
    if a.prepare_only:print('Prepared hybrid timeline',flush=True);return
    head=OUT/'animated-hybrid-head.mp4';tail=OUT/'retained-ending.mp4';assert not head.exists() and not tail.exists()
    p=subprocess.Popen([FF,'-hide_banner','-loglevel','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-video_track_timescale','15360',str(head)],stdin=subprocess.PIPE)
    cap=cv2.VideoCapture(str(DONOR));source_idx=-1;source_im=None;last_source=-1;last_clean=None;cleaner=CornerCleaner()
    selected={0,90,180,270,297,298,376,377,420,480,501,502,570,658,659,723,724,803,804,878,879,959,960,1100,1238}
    for f,sf in enumerate(mapping):
        shot=next(s for s in SHOTS if s['start']<=f<s['end'])
        while source_idx<sf:
            ok,source_im=cap.read();assert ok;source_idx+=1
        if sf==last_source:im=last_clean.copy()
        else:
            im=source_im.copy()
            if shot['key']=='three-exclusions':im=correct_label(im)
            im=cleaner.clean(im,shot['key']);last_clean=im.copy();last_source=sf
        p.stdin.write(im.tobytes())
        if f in selected:cv2.imwrite(str(OUT/'states'/f'f{f:04d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,95])
        if f%500==0:print('Rendered animated frame',f,'of',TAIL_START,flush=True)
    cap.release();p.stdin.close();assert p.wait()==0
    # v20 frame 1239 is an IDR at 41.3 seconds: retain the later pictures exactly.
    run(['-ss','41.300000','-i',SRC,'-map','0:v:0','-an','-c:v','copy',tail])
    playlist=OUT/'video-concat.txt';playlist.write_text("file 'animated-hybrid-head.mp4'\nduration 41.300000000000\nfile 'retained-ending.mp4'\n")
    run(['-f','concat','-safe','0','-i',playlist,'-i',SRC,'-map','0:v:0','-map','1:a:0','-c','copy','-video_track_timescale','15360','-movflags','+faststart',DEST])
    manifest['candidate_sha256']=sha(DEST);manifest['bytes']=DEST.stat().st_size;manifest['corner_cleanup']=cleaner.counts
    manifest['protected_files_unchanged']={str(p):sha(p)==hashes[str(p)] for p in protected};assert all(manifest['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Built',DEST,flush=True)

if __name__=='__main__':main()
