#!/usr/bin/env python3
"""Repair Training generation 2 into a separate review candidate.

Keep current board pixels and useful Notebook scenes. Authorized narration cuts
and measured room-tone pauses use a frame/sample-aligned edit timeline.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import wave
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw
from editorial_typography import draw_board_title, face
from build_one_more_thing_review_repair import ring
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/training-repair-2026-09-09'
SOURCE = ROOT / 'Prompts/training-2.mp4'
DEST = ROOT / 'videos/training-v2.mp4'
FPS, SR, W, H = 30, 48000, 1280, 720
PURPLE, EDITORIAL, BLUE, TEAL, GREEN = '#6e51ff', '#4f2fc4', '#1652f0', '#0e8f86', '#0f7a4a'
BG = (251, 245, 246)


def frame(t): return round(t * FPS)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def overview():
    """A new code-native transition graphic using the lesson's exact terms."""
    im = Image.new('RGB', (1600, 900), '#eae7fd'); d = ImageDraw.Draw(im)
    draw_board_title(d, 'Three Phases of Training')
    d.rounded_rectangle((40, 127, 1560, 860), radius=18, fill='white')
    d.rounded_rectangle((80, 170, 1520, 298), radius=12, fill='#f5f2ff')
    d.text((800, 205), 'THE SAME QUESTION', font=face('heavy', 24), fill=EDITORIAL, anchor='mm')
    d.text((800, 257), 'How do I shoot a basketball?', font=face('bold', 40), fill='#0e0a1f', anchor='mm')
    for x, n, title, color, pale, lines in [
        (80, '1', 'Pretraining', EDITORIAL, '#f3f0fc', ('Learn patterns', 'from data.')),
        (572, '2', 'Instruction Tuning', BLUE, '#edf2fe', ('Learn to follow', 'instructions.')),
        (1064, '3', 'Preference Tuning', GREEN, '#edf6f0', ('Improve responses', 'through feedback.')),
    ]:
        cx=x+228
        d.rounded_rectangle((x,350,x+456,797),radius=16,fill=pale)
        d.ellipse((cx-35,392,cx+35,462),fill=color)
        d.text((cx,427),n,font=face('bold',36),fill='white',anchor='mm')
        d.text((cx,533),title,font=face('bold',36),fill=color,anchor='mm')
        for i,line in enumerate(lines):
            d.text((cx,638+i*48),line,font=face('medium',34),fill='#3a3550',anchor='mm')
    im.save(OUT/'phase-overview.png')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    OUT.mkdir(exist_ok=True);(OUT/'states').mkdir(exist_ok=True)
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    protected=[ROOT/'videos/training.mp4', ROOT/'Prompts/training-1.mp4', SOURCE, ROOT/'index.html', ROOT/'lessons/training.md']
    protected_hashes={str(p.relative_to(ROOT)):sha(p) for p in protected}
    if not (OUT/'source.wav').exists():
        subprocess.run([ff,'-y','-loglevel','error','-i',str(SOURCE),'-vn','-ac','1','-ar',str(SR),str(OUT/'source.wav')],check=True)
    with wave.open(str(OUT/'source.wav')) as wav:
        assert wav.getframerate()==SR and wav.getnchannels()==1
        audio=np.frombuffer(wav.readframes(wav.getnframes()),np.int16).copy()
    # Speech-free, low-level room tone from the candidate itself.
    seed=audio[round(180.4*SR):round(180.9*SR)].astype(float);seed-=seed.mean()
    loop=np.r_[seed,seed[::-1]]
    def tone(n):return np.resize(loop,n).copy()
    timeline=[];parts=[];cursor=0
    def keep(a,b,label):
        nonlocal cursor
        start,end=frame(a),frame(b);n=end-start
        arr=audio[start*1600:end*1600].astype(float).copy()
        fade=240;ramp=np.linspace(0,1,fade);bed=tone(len(arr))
        arr[:fade]=arr[:fade]*ramp+bed[:fade]*(1-ramp)
        arr[-fade:]=arr[-fade:]*(1-ramp)+bed[-fade:]*ramp
        timeline.append(dict(kind='source',label=label,source_start=start,source_end=end,start_frame=cursor,end_frame=cursor+n))
        parts.append(arr);cursor+=n
    def pause(seconds,label,hold):
        nonlocal cursor
        n=frame(seconds);parts.append(tone(n*1600))
        timeline.append(dict(kind='room_tone',label=label,source_hold_frame=frame(hold),start_frame=cursor,end_frame=cursor+n))
        cursor+=n

    keep(0,28.266667,'Opening and basketball analogy')
    keep(31.066667,38.866667,'Numerical adjustments; hard-drive aside removed')
    pause(1,'Pause before setup',38.833333)
    keep(38.866667,57.266667,'Set up the model and gather data')
    pause(1,'Pause before training example',57.233333)
    keep(57.266667,85.533333,'Guess, check, adjust with cloud and jelly')
    pause(1,'Pause before three phases',85.5)
    keep(85.533333,98.333333,'Three training jobs and common basketball prompt')
    pause(1,'Pause before pretraining',98.3)
    keep(98.333333,139.933333,'Pretraining')
    pause(1,'Pause before instruction tuning',139.9)
    keep(139.933333,180.366667,'Instruction tuning and limitation')
    pause(1,'Pause before preference tuning; reflection question removed',180.333333)
    keep(196.266667,213,'Preference feedback and weight updates')
    pause(.166667,'Brief natural join after weights',212.966667)
    keep(214.333333,248.033333,'Preferred answers and remaining risk')
    pause(1,'Pause after remaining-risk explanation',248)
    keep(251.1,259.166667,'Training ends and the model is ready')
    pause(1,'Pause before normal-chat distinction',259.133333)
    keep(259.166667,280.9,'New information can be used without changing weights')
    pause(1,'Pause before closing message',280.866667)
    close_start=cursor
    keep(281.1,286.966667,'Exact approved closing narration')
    pause(2.133333,'Settled closing hold',286.933333)
    total=cursor
    edited=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
    assert len(edited)==total*1600
    with wave.open(str(OUT/'edited.wav'),'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(SR);wav.writeframes(edited.tobytes())

    overview()
    assert close_board_copy('training')==('AI learns from examples and feedback.','Guess. Check. Adjust. Repeat.')
    assets={
        'setup':ROOT/'lessons/training-before-starts-editorial.jpg',
        'loop':ROOT/'lessons/training-loop-editorial.jpg',
        'overview':OUT/'phase-overview.png',
        'pretraining':ROOT/'lessons/training-pretraining-editorial.jpg',
        'instruction':ROOT/'lessons/training-instruction-tuning-editorial.jpg',
        'preference':ROOT/'lessons/training-preference-tuning-editorial.jpg',
        'close':OUT/'close.png',
    }
    bases={};layouts={};boards={}
    for key,path in assets.items():
        im=cv2.imread(str(path));assert im is not None,path;boards[key]=im
        h,w=im.shape[:2];scale=min(1220/w,680/h);nw,nh=round(w*scale),round(h*scale)
        x,y=(W-nw)//2,(H-nh)//2
        base=np.full((H,W,3),BG,np.uint8);base[y:y+nh,x:x+nw]=cv2.resize(im,(nw,nh),interpolation=cv2.INTER_AREA)
        bases[key]=base;layouts[key]=(scale,x,y)

    def mark(rect,color):return dict(rect=rect,color=color,highlight_source='neutral_video_purple' if color==PURPLE else 'card_locked_accent')
    events=[]
    def event(t,board,label,*marks):events.append(dict(source_frame=frame(t),board=board,label=label,marks=list(marks)))
    event(0,'native','notebook-opening')
    event(38.866667,'setup','setup-establish')
    event(45.46,'setup','system-starting-values',mark([40,127,783,717],EDITORIAL))
    event(50.12,'setup','gather-data',mark([817,127,1559,717],BLUE))
    event(56.6,'setup','setup-settle')
    event(57.266667,'loop','loop-establish')
    event(60.32,'loop','peanut-butter-example',mark([66,151,1532,218],PURPLE))
    event(63.8,'loop','guess-cloud',mark([76,247,540,781],EDITORIAL))
    event(67.66,'loop','check-jelly',mark([568,247,1031,781],BLUE))
    event(73.2,'loop','adjust-numbers',mark([1059,247,1523,781],TEAL))
    event(81.36,'loop','repeat-builds-patterns',mark([40,967,1560,1055],PURPLE))
    event(85.533333,'overview','three-phases-overview')
    event(91.88,'overview','same-basketball-question',mark([80,170,1520,298],PURPLE))
    event(97.7,'overview','overview-settle')
    event(98.333333,'pretraining','pretraining-establish')
    event(101.5,'pretraining','pretraining-learns-patterns',mark([74,165,1526,467],EDITORIAL))
    event(114.42,'pretraining','pretraining-answer-example',mark([74,500,1526,664],EDITORIAL))
    event(129.08,'pretraining','pretraining-limitation',mark([74,697,1526,861],EDITORIAL))
    event(139.933333,'instruction','instruction-establish')
    event(144.64,'instruction','instruction-example-pairs',mark([74,165,1526,412],BLUE))
    event(155.74,'instruction','instruction-answer-example',mark([74,444,1526,650],BLUE))
    event(170.38,'instruction','instruction-limitation',mark([74,683,1526,847],BLUE))
    event(196.266667,'preference','preference-establish')
    event(200.44,'preference','preference-feedback',mark([74,165,1526,412],GREEN))
    event(219.66,'preference','preference-answer-example',mark([74,444,1526,691],GREEN))
    event(236.28,'preference','preference-limitation',mark([74,724,1526,888],GREEN))
    event(251.233333,'native','notebook-training-complete-and-normal-chat')

    def source_at(f):
        p=next(p for p in timeline if p['start_frame']<=f<p['end_frame'])
        return p['source_start']+f-p['start_frame'] if p['kind']=='source' else p['source_hold_frame']
    def choice(sf):return next(e for e in reversed(events) if e['source_frame']<=sf)
    schedule=[];last=None
    for f in range(close_start):
        e=choice(source_at(f))
        if e['label']!=last:
            if schedule:schedule[-1]['end_frame']=f
            schedule.append(dict(e,start_frame=f));last=e['label']
    schedule[-1]['end_frame']=close_start
    states={};outline_checks=[]
    for e in schedule:
        if e['board']=='native':continue
        base=bases[e['board']];im=base.copy();s,x,y=layouts[e['board']]
        allowed=np.zeros((H,W),np.uint8)
        for m in e['marks']:
            rect=m['rect'];rr=[x+rect[0]*s,y+rect[1]*s,x+rect[2]*s,y+rect[3]*s]
            ring(im,rr,m['color']);m['output_rect']=rr;m['ring_width']=5
            # Geometric border band; the full interior is protected from fills.
            x0,y0,x1,y1=map(round,rr)
            cv2.rectangle(allowed,(x0-5,y0-5),(x1+5,y1+5),255,-1)
            cv2.rectangle(allowed,(x0+15,y0+15),(x1-15,y1-15),0,-1)
        changed=np.any(im!=base,axis=2)
        assert not np.any(changed & (allowed==0)),e['label']
        states[e['label']]=im;cv2.imwrite(str(OUT/'states'/f"{e['label']}.png"),im)
        outline_checks.append(dict(label=e['label'],changed_pixels=int(changed.sum()),outside_border_changes=0))

    manifest=dict(source=str(SOURCE),output=str(DEST),fps=FPS,total_frames=total,duration=total/FPS,
        timeline=timeline,states=schedule,close_start_frame=close_start,
        highlight_style='outline_only',outline_checks=outline_checks,
        protected_hashes=protected_hashes,
        assets={k:dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for k,p in assets.items()},
        audio=dict(sample_rate=SR,channels=1,room_tone_source=[180.4,180.9],join_fade_ms=5),
        cuts=[dict(start=28.266667,end=31.066667,reason='Hard-drive aside'),
              dict(start=180.366667,end=196.266667,reason='Reflection question'),
              dict(start=213,end=214.333333,reason='One final time'),
              dict(start=248.033333,end=251.1,reason='Unsupported causal hallucination clause'),
              dict(start=280.9,end=281.1,reason='Normalize closing transition'),
              dict(start=286.966667,end=290.1,reason='Notebook ending replaced')],
        close_camera=dict(prehold_frames=48,push_frames=150,settled_frames=total-close_start-198,zoom_endpoint=1.2))
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    labels=list(states)
    for offset in range(0,len(labels),9):
        cells=[]
        for label in labels[offset:offset+9]:
            im=cv2.copyMakeBorder(cv2.resize(states[label],(426,240)),24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
            cv2.putText(im,label,(5,16),cv2.FONT_HERSHEY_SIMPLEX,.4,(45,35,30),1,cv2.LINE_AA);cells.append(im)
        while len(cells)%3:cells.append(np.full_like(cells[0],255))
        cv2.imwrite(str(OUT/f'states-sheet-{offset//9}.jpg'),cv2.vconcat([cv2.hconcat(cells[j:j+3]) for j in range(0,len(cells),3)]))
    print(f'Prepared {total} frames, {total/FPS:.2f} seconds, {len(states)} board states.',flush=True)
    if args.prepare_only:return
    # Never overwrite a preview that might already be open in the user's player.
    assert not DEST.exists(),f'Review output already exists: {DEST}'
    proc=subprocess.Popen([ff,'-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
        '-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    cap=cv2.VideoCapture(str(SOURCE));source_cursor=None;previous_native=None;idx=0;native_frames=0
    for f in range(total):
        if f<close_start:
            while f>=schedule[idx]['end_frame']:idx+=1
            e=schedule[idx]
            if e['board']=='native':
                sf=source_at(f)
                if source_cursor==sf+1:
                    im=previous_native
                else:
                    if source_cursor!=sf:cap.set(cv2.CAP_PROP_POS_FRAMES,sf)
                    ok,im=cap.read();assert ok,sf;source_cursor=sf+1
                    if im.shape[:2]!=(H,W):im=cv2.resize(im,(W,H),interpolation=cv2.INTER_AREA)
                    previous_native=im
                native_frames+=1
            else:im=states[e['label']]
        else:
            local=f-close_start;p=min(1,max(0,(local-48)/149));eased=p*p*(3-2*p);z=1+.2*eased
            close=boards['close'];h,w=close.shape[:2];ww=w/z;hh=ww*9/16
            matrix=np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]])
            im=cv2.warpAffine(close,matrix,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            if local in (0,48,197,total-close_start-1):cv2.imwrite(str(OUT/'states'/f'close-{local}.png'),im)
        proc.stdin.write(im.tobytes())
        if f%1800==0:print(f'Rendered {f}/{total} frames',flush=True)
    proc.stdin.close();assert proc.wait()==0;cap.release()
    assert protected_hashes=={str(p.relative_to(ROOT)):sha(p) for p in protected}
    manifest['native_video_frames']=native_frames
    manifest['render_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Rendered {DEST}; native footage {native_frames/FPS:.2f}s',flush=True)


if __name__=='__main__':main()
