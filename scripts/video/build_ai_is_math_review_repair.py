#!/usr/bin/env python3
"""Repair the selected AI Is Math generation into a separate review candidate.

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
OUT = ROOT / 'video-audit/ai-is-math-repair-2026-09-09'
SOURCE = ROOT / 'Prompts/AI_is_Math__The_Secret_of_Conditional_Probability.mp4'
DEST = ROOT / 'videos/ai-is-math-v2.mp4'
FPS, SR, W, H = 30, 48000, 1280, 720
PURPLE, EDITORIAL, BLUE, TEAL, GREEN = '#6e51ff', '#4f2fc4', '#1652f0', '#0e8f86', '#0f7a4a'
BG = (251, 245, 246)


def frame(t): return round(t * FPS)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def overview():
    from editorial_takeaway import draw_takeaway_band
    for name, mode in [('bridge',0),('loop-start',1),('loop-added',2),('loop-next',3)]:
        im=Image.new('RGB',(1600,900),'#eae7fd');d=ImageDraw.Draw(im)
        draw_board_title(d,'The Conversation Shapes the Odds' if mode==0 else 'The Prediction Continues')
        d.rounded_rectangle((40,127,1560,712),radius=18,fill='white')
        if mode==0:
            for x,title,lines,col,pale in [(85,'CONVERSATION SO FAR',('Your question','+','Words already written'),EDITORIAL,'#f2effd'),(925,'WHAT COMES NEXT',('Next-word','probabilities'),TEAL,'#e8f5f2')]:
                d.rounded_rectangle((x,200,x+590,635),radius=16,fill=pale)
                d.text((x+295,264),title,font=face('heavy',25),fill=col,anchor='mm')
                for i,line in enumerate(lines):d.text((x+295,385+i*66),line,font=face('bold' if line!='+' else 'medium',37),fill='#3a3550',anchor='mm')
            d.line((717,416,878,416),fill=EDITORIAL,width=6)
            d.polygon([(878,416),(852,401),(852,431)],fill=EDITORIAL)
            takeaway='The words so far shape the probabilities for what comes next.'
        else:
            d.text((100,187),'AI’S REPLY SO FAR',font=face('heavy',25),fill=EDITORIAL,anchor='la')
            d.rounded_rectangle((85,247,1515,407),radius=15,fill='#f2effd')
            text='You could name him'
            font=face('bold',49);tw=d.textlength(text,font=font);left=(1600-tw-24-180)/2
            d.text((left,325),text,font=font,fill='#0e0a1f',anchor='lm')
            x=left+tw+24
            d.rounded_rectangle((x,280,x+180,370),radius=12,fill=EDITORIAL if mode>=2 else 'white')
            d.text((x+90,325),'Spot' if mode>=2 else '____',font=face('bold',43),fill='white' if mode>=2 else EDITORIAL,anchor='mm')
            if mode==1:
                d.text((800,540),'Choose a word.',font=face('bold',43),fill=EDITORIAL,anchor='mm')
            elif mode==2:
                d.text((800,540),'The chosen word joins the text.',font=face('bold',43),fill=EDITORIAL,anchor='mm')
            else:
                d.line((800,440,800,488),fill=TEAL,width=6)
                d.polygon([(800,495),(786,474),(814,474)],fill=TEAL)
                d.rounded_rectangle((325,523,1275,636),radius=15,fill='#e8f5f2')
                d.text((800,579),'Calculate what comes next.',font=face('bold',43),fill=TEAL,anchor='mm')
            takeaway='Each new word becomes part of the next prediction.'
        draw_takeaway_band(im,top=752,left=40,right=1560,text=takeaway,font=face('medium',30))
        im.save(OUT/f'{name}.png')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    OUT.mkdir(exist_ok=True);(OUT/'states').mkdir(exist_ok=True)
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    protected=[ROOT/'videos/ai-is-math.mp4', ROOT/'Prompts/AI_is_Math.mp4', SOURCE, ROOT/'index.html', ROOT/'lessons/ai-is-math.md']
    protected_hashes={str(p.relative_to(ROOT)):sha(p) for p in protected}
    if not (OUT/'source.wav').exists():
        subprocess.run([ff,'-y','-loglevel','error','-i',str(SOURCE),'-vn','-ac','1','-ar',str(SR),str(OUT/'source.wav')],check=True)
    with wave.open(str(OUT/'source.wav')) as wav:
        assert wav.getframerate()==SR and wav.getnchannels()==1
        audio=np.frombuffer(wav.readframes(wav.getnframes()),np.int16).copy()
    # Speech-free, low-level room tone from the candidate itself.
    seed=audio[round(59.0*SR):round(59.4*SR)].astype(float);seed-=seed.mean()
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

    keep(0,43.533333,'Notebook opening and probability history')
    pause(1,'Pause before standard probability',43.5)
    keep(43.533333,59.133333,'Equally likely outcomes and counting formula')
    pause(1,'Pause before two-coin example; ratio overreach removed',59.1)
    keep(66.966667,99.4,'Four outcomes and 25 percent')
    pause(1,'Pause before new evidence',99.366667)
    keep(99.4,153.166667,'Conditional probability and changed knowledge')
    pause(1,'Pause before connection to AI',153.133333)
    keep(153.166667,170.333333,'Conversation conditions next-word probabilities')
    pause(1,'Pause before dog-name example',170.3)
    keep(170.333333,193.833333,'Question, reply, and three probabilities')
    pause(1,'Pause before prediction loop; database claim removed',193.8)
    keep(203.7,213.033333,'Chosen word joins the text; next prediction')
    pause(1,'Pause before exact closing',213)
    close_start=cursor
    keep(213.033333,217.466667,'Exact lesson closing narration')
    pause(3.566667,'Settled closing hold',217.433333)
    total=cursor
    edited=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
    assert len(edited)==total*1600
    with wave.open(str(OUT/'edited.wav'),'wb') as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(SR);wav.writeframes(edited.tobytes())

    overview()
    assert close_board_copy('aiismath')==('AI builds answers with probabilities.','One prediction at a time.')
    assets={
        'formula':ROOT/'lessons/ai-is-math-the-math-editorial.jpg',
        'coins':ROOT/'lessons/ai-is-math-two-coins-editorial.jpg',
        'clue':ROOT/'lessons/ai-is-math-conditional-probability-editorial.jpg',
        'dog':ROOT/'lessons/ai-is-math-what-comes-next-editorial.jpg',
        'bridge':OUT/'bridge.png',
        'loop-start':OUT/'loop-start.png',
        'loop-added':OUT/'loop-added.png',
        'loop-next':OUT/'loop-next.png',
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
    event(0,'native','notebook-opening-and-history')
    event(43.533333,'formula','formula-establish')
    event(53.34,'formula','ways-to-get-result',mark([378,207,922,270],EDITORIAL))
    event(56.28,'formula','total-outcomes',mark([360,307,940,367],EDITORIAL))
    event(58.8,'formula','formula-settle')
    event(66.966667,'coins','coins-establish')
    event(69.0,'coins','coin-scenario',mark([40,127,1560,255],PURPLE))
    event(74.8,'coins','four-equally-likely-outcomes',mark([70,325,1530,598],PURPLE))
    event(77.36,'coins','heads-heads',mark([65,332,425,594],GREEN))
    event(79.0,'coins','heads-tails',mark([435,332,795,594],BLUE))
    event(80.28,'coins','tails-heads',mark([805,332,1165,594],BLUE))
    event(81.68,'coins','tails-tails',mark([1175,332,1535,594],BLUE))
    event(83.9,'coins','one-matching-outcome',mark([65,332,425,594],GREEN))
    event(85.6,'coins','one-out-of-four',mark([238,692,1308,872],EDITORIAL))
    event(92.4,'native','notebook-four-outcomes-summary')
    event(99.733333,'native','notebook-new-evidence-and-peek')
    event(123.133333,'clue','clue-board-establish')
    event(125.02,'clue','rule-out-tails-first',mark([805,372,1535,634],'#c41f28'))
    event(131.1,'clue','two-remaining-outcomes',mark([65,372,795,634],PURPLE))
    event(134.95,'clue','one-remaining-double-heads',mark([65,372,425,634],GREEN))
    event(139.55,'clue','one-out-of-two',mark([238,732,1308,912],GREEN))
    event(143.32,'clue','unchanged-coins-changed-knowledge')
    event(148.2,'clue','fifty-percent-takeaway',mark([40,1027,1560,1115],PURPLE))
    event(153.166667,'bridge','conversation-to-probabilities')
    event(162.53,'bridge','question-and-written-words',mark([85,200,675,635],EDITORIAL))
    event(165.62,'bridge','conditioned-probabilities',mark([925,200,1515,635],TEAL))
    event(170.333333,'dog','dog-board-establish')
    event(171.44,'dog','dog-question',mark([40,127,1560,255],PURPLE))
    event(175.7,'dog','reply-so-far',mark([490,305,1110,442],EDITORIAL))
    event(180.38,'dog','possible-next-words',mark([295,451,1305,665],PURPLE))
    event(187.1,'dog','spot-probability',mark([320,518,600,648],EDITORIAL))
    event(190.06,'dog','max-probability',mark([660,518,940,648],EDITORIAL))
    event(191.78,'dog','buddy-probability',mark([1000,518,1280,648],EDITORIAL))
    event(203.7,'loop-start','choose-next-word')
    event(204.96,'loop-added','word-joins-text')
    event(206.64,'loop-next','new-evidence-for-next-prediction')

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
        audio=dict(sample_rate=SR,channels=1,room_tone_source=[59.0,59.4],join_fade_ms=5),
        cuts=[dict(start=59.133333,end=66.966667,reason='Counting-ratio overreach'),
              dict(start=193.833333,end=203.7,reason='Other names in model database claim'),
              dict(start=217.466667,end=220.8,reason='Notebook outro replaced')],
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
    glyph_mask=cv2.imread(str(OUT/'notebook-glyph-mask.png'),0)
    for f in range(total):
        if f<close_start:
            while f>=schedule[idx]['end_frame']:idx+=1
            e=schedule[idx]
            if e['board']=='native':
                sf=source_at(f)
                if source_cursor==sf+1:
                    im=previous_native
                else:
                    if source_cursor is None:source_cursor=0
                    assert source_cursor<=sf
                    while source_cursor<sf:
                        assert cap.grab();source_cursor+=1
                    ok,im=cap.read();assert ok,sf;source_cursor=sf+1
                    if im.shape[:2]!=(H,W):im=cv2.resize(im,(W,H),interpolation=cv2.INTER_AREA)
                    im=im.copy()
                    roi=im[694:716,1148:1280]
                    roi[:]=cv2.inpaint(roi,glyph_mask,3,cv2.INPAINT_TELEA)
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
    after_hashes={str(p.relative_to(ROOT)):sha(p) for p in protected}
    changed=[name for name,value in protected_hashes.items() if after_hashes[name]!=value]
    assert not [name for name in changed if name!='index.html'],changed
    assert close_board_copy('aiismath')==('AI builds answers with probabilities.','One prediction at a time.')
    manifest['concurrent_changes']=changed
    manifest['protected_hashes_after']=after_hashes
    manifest['native_video_frames']=native_frames
    manifest['native_engine_mark_repair']='Fixed source-derived glyph mask, 1148:1280 x 694:716, 3px inpaint; no rectangular fill'
    manifest['render_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Rendered {DEST}; native footage {native_frames/FPS:.2f}s',flush=True)


if __name__=='__main__':main()
