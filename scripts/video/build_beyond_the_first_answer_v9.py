#!/usr/bin/env python3
"""Restore the spoken four-way introduction; retain v8's cinematic edit.

Narrow owner-requested repair, 2026-11-09. Rebuild pristine sources, insert
eight seconds at a measured silent point (27 + 2/24 seconds). Same narrator's
four exact names are copied from their original section introductions.
"""
from pathlib import Path
import argparse, json, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps
import build_beyond_the_first_answer_v8 as v8
from editorial_typography import face

ROOT=v8.ROOT
AUDIT=ROOT/'video-audit/beyond-the-first-answer-overview-v9-2026-11-09'
DEST=ROOT/'Prompts/beyond-the-first-answer-v9.mp4'
CUT,INSERT,FPS=650,192,24
TOTAL=v8.TOTAL+INSERT
NAMES=['Thought Partner','Learn With AI','Find a Place to Start','Iterate With AI']
ART=[('3',800),('5',2700),('3',4230),('3',5320)]
ONSET=[.6,2.1,3.9,5.9]
CLIPS=[(29.77,30.65),(88.24,89.28),(145.99,147.25),(183.38,184.75)]

def decode_audio(p):
    return np.frombuffer(subprocess.check_output([v8.base.FF,'-v','error','-i',str(p),'-f','f32le','-ar','48000','-ac','1','-']),np.float32)

def audio():
    x=decode_audio(v8.SOURCE)[:243*48000];y=np.zeros(8*48000,np.float32)
    rows=[]
    for (a,z),t,name in zip(CLIPS,ONSET,NAMES):
        c=x[round(a*48000):round(z*48000)].copy();k=240
        c[:k]*=np.linspace(0,1,k);c[-k:]*=np.linspace(1,0,k)
        p=round(t*48000);y[p:p+len(c)]=c
        rows.append(dict(name=name,source_seconds=[a,z],output_seconds=[CUT/FPS+t,CUT/FPS+t+len(c)/48000],gain_db=0,edge_fades_ms=5))
    cut=CUT*2000;full=np.concatenate([x[:cut],y,x[cut:]])
    assert np.array_equal(full[:cut],x[:cut]) and np.array_equal(full[cut+len(y):],x[cut:])
    assert len(full)==TOTAL*2000
    dest=AUDIT/'assembled-audio.wav'
    subprocess.run([v8.base.FF,'-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(dest)],input=full.tobytes(),check=True)
    return dest,rows

def art():
    result={};mask=v8.glyph_mask()
    for roll in ('3','5'):
        needed={f for r,f in ART if r==roll};cap=cv2.VideoCapture(str(v8.ROLLS[roll]));n=0
        while cap.grab():
            if n in needed:
                ok,im=cap.retrieve();assert ok
                im,_=v8.clean_frame(im,mask)
                result[roll,n]=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
            n+=1
            if n>max(needed):break
        cap.release()
    return [result[x] for x in ART]

def overview(n,images):
    canvas=Image.new('RGB',(1280,720),'#f5f3eb');d=ImageDraw.Draw(canvas)
    d.text((640,38),'Four ways to work with AI',font=face('bold',43),anchor='ma',fill='#263844')
    active=max([-1]+[i for i,t in enumerate(ONSET) if n/FPS>=t])
    for i,im in enumerate(images):
        x=54+(i%2)*612;y=115+(i//2)*286
        # Full cinematic scenes remain visible; no subject or diagram is cropped.
        thumb=ImageOps.contain(im,(564,225),Image.Resampling.LANCZOS)
        canvas.paste(thumb,(x+(564-thumb.width)//2,y))
        d.text((x+282,y+237),f'{i+1}. {NAMES[i]}',font=face('bold',28),anchor='ma',fill='#263844')
        if i==active:d.rounded_rectangle((x-7,y-7,x+571,y+275),radius=12,outline='#4f2fc4',width=4)
    return cv2.cvtColor(np.asarray(canvas),cv2.COLOR_RGB2BGR)

def old_frame(n,boards,close,cache):
    if n>=v8.base.CLOSE_IN:return v8.base.close_frame(close,n)
    for b in boards.values():
        if b['span'][0]<=n<b['span'][1]:return v8.base.board_frame(b,n)
    scene=next(s for s in v8.SCENES if s[0]<=n<s[1])
    return v8.scene_frame(scene,n,cache)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    AUDIT.mkdir(exist_ok=True)
    assert v8.base.sha(v8.SOURCE)==v8.base.EXPECTED
    for k,p in v8.ROLLS.items():assert v8.base.sha(p)==v8.EXPECTED[k]
    protected={str(p):v8.base.sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/manifest.json',ROOT/'lessons/beyond-the-first-answer.md',*v8.base.ASSETS.glob('*')] if p.is_file()}
    (AUDIT/'protected-before.json').write_text(json.dumps(protected,indent=2))
    audiofile,rows=audio();images=art()
    for n in (0,24,60,108,156,191):cv2.imwrite(str(AUDIT/f'overview-{n:03d}.jpg'),overview(n,images))
    cv2.imwrite(str(AUDIT/'poster.jpg'),overview(24,images))
    plan=dict(scope='Restore the four-way spoken and visual overview in the intro',insertion_frame=CUT,insertion_seconds=CUT/FPS,insert_frames=INSERT,insert_seconds=8,frames=TOTAL,duration_seconds=TOTAL/FPS,narration=rows,visual='Four cinematic scene thumbnails; all exact lesson names visible throughout; one outline follows the spoken name; full view, no camera dive.',unchanged='Every original video frame and audio sample remains in original order. All later material shifts by exactly 8 seconds. Original scenes rebuilt from pristine sources.',source_hashes={str(v8.SOURCE):v8.base.sha(v8.SOURCE),**{str(p):v8.base.sha(p) for p in v8.ROLLS.values()}},limitations=['Phrase joins have transcript and signal checks only; no listening pass claimed.'],publication='Review candidate only; installed video unchanged')
    (AUDIT/'edit-plan.json').write_text(json.dumps(plan,indent=2))
    if args.prepare_only:return
    assert not DEST.exists(),DEST
    v8.base.AUDIT=AUDIT
    boards,close=v8.base.prepare();cache,methods=v8.load_donors()
    cmd=[v8.base.FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','24','-i','pipe:0','-i',str(audiofile),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(TOTAL):
        if CUT<=n<CUT+INSERT:im=overview(n-CUT,images)
        else:im=old_frame(n if n<CUT else n-INSERT,boards,close,cache)
        p.stdin.write(im.tobytes())
        if (n+1)%720==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    p.stdin.close();assert p.wait()==0
    assert all(v8.base.sha(p)==h for p,h in protected.items()),'Protected files changed'
    plan.update(candidate=str(DEST),candidate_sha256=v8.base.sha(DEST),protected_files_unchanged=True)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(plan,indent=2))
    print('Complete:',DEST,flush=True)

if __name__=='__main__':main()
