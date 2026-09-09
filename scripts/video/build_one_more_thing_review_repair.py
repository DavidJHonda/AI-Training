#!/usr/bin/env python3
"""Repair the 2026-09-09 One More Thing candidate; never replace the live video.

Uses current source-board pixels, output-space 5px rings, and a measured audio
edit timeline. Review evidence and the source-to-output mapping are saved beside
the render. Run with .video-venv/bin/python from the repository root.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, wave
import cv2
import numpy as np
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/one-more-thing-repair-2026-09-09'
FPS, SR, WIDTH, HEIGHT = 30, 48000, 1280, 720
PURPLE, EDITORIAL, BLUE, RED, TEAL = '#6e51ff', '#4f2fc4', '#1652f0', '#c41f28', '#0e8f86'
BG = (251,245,246)  # BGR #f6f5fb

def frame(t): return round(t * FPS)
def bgr(h): return tuple(int(h[i:i+2],16) for i in (5,3,1))

def ring(img, rect, color, radius=10):
    x0,y0,x1,y1=map(round,rect); c=bgr(color); r=min(radius,(x1-x0)//2,(y1-y0)//2)
    for a,b in [((x0+r,y0),(x1-r,y0)),((x0+r,y1),(x1-r,y1)),((x0,y0+r),(x0,y1-r)),((x1,y0+r),(x1,y1-r))]:
        cv2.line(img,a,b,c,5,cv2.LINE_AA)
    for center,start in [((x0+r,y0+r),180),((x1-r,y0+r),270),((x1-r,y1-r),0),((x0+r,y1-r),90)]:
        cv2.ellipse(img,center,(r,r),0,start,start+90,c,5,cv2.LINE_AA)

def main():
    global OUT
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true')
    ap.add_argument('--engaging-visuals',action='store_true',help='Preserve Notebook motion graphics between current-board walkthroughs.')
    args=ap.parse_args()
    if args.engaging_visuals:OUT=ROOT/'video-audit/one-more-thing-outline-only-2026-09-09'
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'states').mkdir(exist_ok=True)
    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
    source=ROOT/'Prompts/one-more-thing-2.mp4'
    wav=OUT/'source.wav'
    if not wav.exists():
        subprocess.run([ffmpeg,'-y','-loglevel','error','-i',str(source),'-vn','-ac','1','-ar',str(SR),str(wav)],check=True)
    with wave.open(str(wav)) as w:
        assert w.getframerate()==SR and w.getnchannels()==1
        audio=np.frombuffer(w.readframes(w.getnframes()),np.int16).copy()
    # A quiet decay from this exact recording, mirror-tiled to avoid a loop edge.
    seed=audio[round(237.3*SR):round(237.7*SR)].astype(np.float64)
    seed-=seed.mean(); loop=np.concatenate([seed,seed[::-1]])
    def tone(samples): return np.resize(loop,samples).copy()
    timeline=[];parts=[];cursor=0
    def keep(a,b,label):
        nonlocal cursor
        start,end=frame(a),frame(b);count=end-start
        arr=audio[start*1600:end*1600].astype(np.float64).copy()
        # Short fades only in preselected quiet handles; speech interiors remain intact.
        n=240; ramp=np.linspace(0,1,n); bed=tone(len(arr))
        arr[:n]=bed[:n]*(1-ramp)+arr[:n]*ramp
        arr[-n:]=arr[-n:]*(1-ramp)+bed[-n:]*ramp
        timeline.append(dict(kind='source',label=label,source_start=start,source_end=end,start_frame=cursor,end_frame=cursor+count))
        parts.append(arr);cursor+=count
    def pause(seconds,label,source_hold):
        nonlocal cursor
        count=frame(seconds);parts.append(tone(count*1600))
        timeline.append(dict(kind='room_tone',label=label,source_hold=source_hold,start_frame=cursor,end_frame=cursor+count))
        cursor+=count
    keep(0,98.233333,'Probability explanation')
    pause(1,'Pause before temperature',98.2)
    keep(98.233333,119,'Temperature and low-temperature example')
    pause(1,'Pause before high temperature',118.95)
    keep(133.966667,161.933333,'High temperature and fixed weights')
    pause(1,'Pause before computation',161.9)
    keep(170.966667,205.7,'Computation example')
    pause(.366667,'Join after repeated one-word calculation cut',205.65)
    keep(212.233333,234.9,'Scale to 100 and 1000 newly written tokens')
    pause(1,'Pause before closing message',234.85)
    close_start=cursor
    keep(237.8,243,'Approved closing narration')
    pause(2.8,'Closing settled hold',243)
    total=cursor
    final_audio=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
    assert len(final_audio)==total*1600
    with wave.open(str(OUT/'edited.wav'),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(final_audio.tobytes())

    assets={
        'probability':ROOT/'lessons/one-more-thing-1-draws.jpg',
        'temperature':ROOT/'lessons/one-more-thing-2-temperature.jpg',
        'math':ROOT/'lessons/one-more-thing-3-bill.jpg',
        'close':ROOT/'archive/video-materials/understand-ai-2026-09-09/obsolete/lessons/one-more-thing-4-close.jpg',
    }
    # Archived standalone closing capture visually verified against current CLOSE_BOARDS.
    from make_close_board import close_board_copy
    assert close_board_copy('inference')==('Not a mind. Math, at a scale nobody can picture.','Every time you hit send.')
    boards={k:cv2.imread(str(p)) for k,p in assets.items()}
    layouts={};bases={}
    for k,im in boards.items():
        assert im is not None
        h,w=im.shape[:2];s=min(1220/w,680/h);nw,nh=round(w*s),round(h*s)
        x,y=(WIDTH-nw)//2,(HEIGHT-nh)//2
        canvas=np.full((HEIGHT,WIDTH,3),BG,np.uint8)
        canvas[y:y+nh,x:x+nw]=cv2.resize(im,(nw,nh),interpolation=cv2.INTER_AREA)
        bases[k]=canvas;layouts[k]=(s,x,y)
    def mark(rect,color=EDITORIAL):
        return dict(rect=rect,color=color,
                    highlight_source='neutral_video_purple' if color==PURPLE else 'card_locked_accent')
    # All rectangles are measured from the current source boards or their renderer
    # geometry. Inner cards keep their locked color; neutral titles/banners use purple.
    events=[]
    def event(t,board,label,*marks):events.append(dict(source_time=t,board=board,label=label,marks=list(marks)))
    event(0,'probability','probability-overview')
    event(23.3,'probability','answer-so-far',mark([80,150,1520,236],PURPLE))
    event(27.7,'probability','probability-list',mark([76,266,676,710],EDITORIAL))
    event(38.75,'probability','spot-22',mark([96,362,650,410],EDITORIAL))
    event(47.35,'probability','not-guaranteed',mark([40,782,1560,870],PURPLE))
    event(50.04,'probability','expected-frequency',mark([96,362,650,410],EDITORIAL))
    event(56.3,'probability','five-separate-tries',mark([936,266,1540,694],EDITORIAL))
    for t,n in [(66.65,0),(67.2,1),(67.78,2),(68.33,3),(68.95,4)]:
        y=362+n*64;event(t,'probability',f'try-{n+1}',mark([956,y,1520,y+52],EDITORIAL))
    event(70.34,'probability','separate-outcomes',mark([936,266,1540,694],EDITORIAL))
    event(78,'probability','why-variety')
    event(80.36,'probability','always-top-choice',mark([96,362,650,410],EDITORIAL))
    event(85.3,'probability','other-likely-choices',mark([80,418,670,637],EDITORIAL))
    event(90.14,'probability','choice-shapes-context',mark([80,150,1520,236],PURPLE))
    event(97.9,'probability','probability-settle')
    event(98.4,'temperature','temperature-title',mark([29,33,999,116],PURPLE))
    event(106.6,'temperature','starting-versus-low',mark([330,283,715,826],EDITORIAL),mark([733,283,1118,826],BLUE))
    event(113.2,'temperature','spot-temperature-comparison',mark([330,383,715,456],EDITORIAL),mark([733,383,1118,456],BLUE))
    event(134.1,'temperature','high-temperature',mark([1135,283,1520,826],RED))
    event(145.1,'temperature','other-combined-comparison',mark([330,748,715,826],EDITORIAL),mark([1135,748,1520,826],RED))
    event(154.32,'temperature','temperature-takeaway',mark([40,905,1560,994],PURPLE))
    event(161.9,'temperature','temperature-settle')
    event(171.1,'math','math-title',mark([26,16,632,98],PURPLE))
    event(178.4,'math','weights-per-token',mark([40,118,525,722],BLUE))
    event(194.24,'math','one-token-cost',mark([40,118,525,722],BLUE))
    event(212.3,'math','scaling-overview')
    event(216.48,'math','short-answer',mark([557,118,1043,722],EDITORIAL))
    event(221.46,'math','longer-conversation',mark([1075,118,1560,722],TEAL))
    event(230.12,'math','new-output-tokens')
    event(234.8,'math','math-settle')

    if args.engaging_visuals:
        events=[e for e in events if e['label']!='starting-versus-low']
        # Let the complete board establish before the first emphasis.
        event(34.466667,'probability','probability-establish')
        event(35.1,'probability','probability-list-on-return',mark([76,266,676,710],EDITORIAL))
        event(106.566667,'temperature','temperature-establish')
        event(106.95,'temperature','starting-versus-low-on-return',mark([330,283,715,826],EDITORIAL),mark([733,283,1118,826],BLUE))
        event(191.333333,'math','math-establish')
        events.sort(key=lambda e:e['source_time'])

    def source_at(f):
        for part in timeline:
            if part['start_frame']<=f<part['end_frame']:
                if part['kind']=='source':return (part['source_start']+f-part['start_frame'])/FPS
                return part['source_hold']
        raise ValueError(f)
    def choice(t): return next(e for e in reversed(events) if frame(e['source_time'])<=frame(t))
    schedule=[];last=None
    for f in range(close_start):
        e=choice(source_at(f));key=e['label']
        if key!=last:
            if schedule:schedule[-1]['end_frame']=f
            schedule.append(dict(e,start_frame=f));last=key
    schedule[-1]['end_frame']=close_start
    states={}
    for row in schedule:
        k=row['board'];im=bases[k].copy();s,x,y=layouts[k]
        def xy(rect):return [x+rect[0]*s,y+rect[1]*s,x+rect[2]*s,y+rect[3]*s]
        for m in row['marks']:
            rr=xy(m['rect']);assert min(rr[:2])>=24 and rr[2]<=WIDTH-24 and rr[3]<=HEIGHT-24,(row['label'],rr)
            ring(im,rr,m['color'])
            m['output_rect']=[round(v,2) for v in rr];m['ring_width']=5
        name=row['label'];states[name]=im
        cv2.imwrite(str(OUT/'states'/f'{name}.png'),im)
    dest=ROOT/('videos/one-more-thing-v4.mp4' if args.engaging_visuals else 'videos/one-more-thing-v2.mp4')
    visual_clips=[]
    if args.engaging_visuals:
        # Ranges use original narration time; the dial is borrowed from an
        # already-cut visual span without restoring its redundant narration.
        for a,b,donor,label in [(0,34.466667,0,'Original opening and dog-prompt animation'),
                                (98.233333,106.566667,162.233333,'Notebook temperature dial'),
                                (171.066667,191.333333,171.066667,'Original weights and computation animation')]:
            indices=[f for f in range(close_start) if any(p['kind']=='source' and p['start_frame']<=f<p['end_frame'] for p in timeline) and frame(a)<=frame(source_at(f))<frame(b)]
            visual_clips.append(dict(start_frame=min(indices),end_frame=max(indices)+1,source_start=frame(donor),label=label))
    manifest=dict(source=str(source),output=str(dest),fps=FPS,total_frames=total,duration=total/FPS,
                  timeline=timeline,states=schedule,close_start_frame=close_start,
                  visual_clips=visual_clips,
                  highlight_style='outline_only',
                  close_camera=dict(prehold_frames=48,push_frames=150,settled_frames=total-close_start-198,zoom_endpoint=1.2),
                  assets={k:dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for k,p in assets.items()},
                  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  audio=dict(sample_rate=SR,channels=1,room_tone_source=[237.3,237.7],join_fade_ms=5),
                  cuts=[dict(start=119,end=133.966667,reason='Low-temperature restatement and prediction aside'),dict(start=161.933333,end=170.966667,reason='Direct-control/safe-text restatement'),dict(start=205.7,end=212.233333,reason='Repeated one-word calculation'),dict(start=234.9,end=237.8,reason='Repeating old work aside'),dict(start=243,end=246.133333,reason='Notebook tail replaced by standard close hold')])
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # Compact contact sheets of every actual highlight state for human inspection.
    labels=list(states)
    for page in range(0,len(labels),9):
        cells=[]
        for name in labels[page:page+9]:
            tile=cv2.copyMakeBorder(cv2.resize(states[name],(426,240)),24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
            cv2.putText(tile,name,(7,16),cv2.FONT_HERSHEY_SIMPLEX,.42,(50,35,25),1,cv2.LINE_AA);cells.append(tile)
        while len(cells)%3:cells.append(np.full_like(cells[0],255))
        cv2.imwrite(str(OUT/f'states-sheet-{page//9}.jpg'),cv2.vconcat([cv2.hconcat(cells[n:n+3]) for n in range(0,len(cells),3)]))
    print(f'Prepared {len(schedule)} states; {total} frames; {total/FPS:.2f}s',flush=True)
    if args.prepare_only:return
    audio_input=ROOT/'videos/one-more-thing-v2.mp4' if args.engaging_visuals else OUT/'edited.wav'
    audio_codec=['-c:a','copy'] if args.engaging_visuals else ['-c:a','aac','-b:a','192k']
    proc=subprocess.Popen([ffmpeg,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(audio_input),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',*audio_codec,'-movflags','+faststart',str(dest)],stdin=subprocess.PIPE)
    capture=cv2.VideoCapture(str(source)) if visual_clips else None
    source_cursor=None
    idx=0
    for f in range(total):
        if f<close_start:
            while f>=schedule[idx]['end_frame']:idx+=1
            im=states[schedule[idx]['label']]
            active=next((c for c in visual_clips if c['start_frame']<=f<c['end_frame']),None)
            if active:
                source_frame=active['source_start']+f-active['start_frame']
                if source_cursor!=source_frame:capture.set(cv2.CAP_PROP_POS_FRAMES,source_frame)
                ok,im=capture.read();assert ok,source_frame
                source_cursor=source_frame+1
                if im.shape[:2]!=(HEIGHT,WIDTH):im=cv2.resize(im,(WIDTH,HEIGHT),interpolation=cv2.INTER_AREA)
                if f==active['start_frame']:cv2.imwrite(str(OUT/'states'/f"notebook-{f}.png"),im)
        else:
            local=f-close_start;progress=min(1,max(0,(local-48)/149));eased=progress*progress*(3-2*progress);zoom=1+.2*eased
            close=boards['close'];h,w=close.shape[:2];ww=w/zoom;hh=ww*9/16
            matrix=np.float32([[ww/WIDTH,0,(w-ww)/2],[0,hh/HEIGHT,(h-hh)/2]])
            im=cv2.warpAffine(close,matrix,(WIDTH,HEIGHT),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            if local in (0,48,197,total-close_start-1):cv2.imwrite(str(OUT/'states'/f'close-{local}.png'),im)
        proc.stdin.write(im.tobytes())
    proc.stdin.close();assert proc.wait()==0
    if capture:capture.release()
    print('Rendered '+str(dest),flush=True)

if __name__=='__main__':main()
