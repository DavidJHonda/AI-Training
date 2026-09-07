#!/usr/bin/env python3
"""Owner-approved five-move donor integration. Review candidate, never live."""
import json, subprocess, hashlib
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import build_work_changes_hybrid as v
import build_your_choices_reroll_review as common

ROOT=Path(__file__).resolve().parents[2]
AUDIT=ROOT/'video-audit/flattery-five-moves-hybrid-v3-2026-09-07'
OUT=ROOT/'Prompts/flattery-trap-five-moves-patched-v3.mp4'
RAW=ROOT/'Prompts/flattery-trap.mp4'
DONOR=ROOT/'Prompts/flattery-trap-5-moves.mp4'
FF=common.FFMPEG
at=common.at
P,A,B,T='#4f2fc4','#a9760c','#1652f0','#0e8f86'
sources=[RAW,DONOR]
boards={k:ROOT/'illustrations'/f'flattery-trap-{s}-v2.jpg' for k,s in [('gatsby','comparison'),('loop','praise-loop'),('quote','sycophancy'),('moves','five-moves')]}
states={0:[],1:[]}

def add(src,start,end,board,label,rect=None,color=P,camera=None,move=0):
    states[src].append(dict(start=at(start),end=at(end),board=board,label=label,rect=rect,color=color,camera=camera,move=move))

# First board: complete column rails with ink-specific vertical sections.
add(0,28.5,32.8,'gatsby','full')
add(0,32.8,47.4,'gatsby','essay',(40,112,1560,351),P,(800,232,1680),24)
add(0,47.4,52.6,'gatsby','flattery-response',(40,925,784,1030),A,(412,1090,1020),30)
add(0,52.6,57.0,'gatsby','praised',(40,1050,784,1150),A,(412,1090,1020))
add(0,57.0,64.5,'gatsby','false-praise-result',(40,1280,784,1400),A,(412,1250,1020),24)
add(0,64.5,67.8,'gatsby','useful-heading-and-response',(816,824,1560,1030),B,(1188,1100,1050),30)
add(0,67.8,71.9,'gatsby','missing-thesis',(816,1170,1560,1270),B,(1188,1100,1050))
add(0,71.9,80.6,'gatsby','banner',(40,1454,1560,1542),P,(800,1498,1680),24)
add(0,87.566667,101.5,'loop','full')
add(0,101.5,109.6,'loop','people-rank',(65,160,430,690),P,(248,425,1050),30)
add(0,109.6,119.1,'loop','agreement',(585,160,1015,690),B,(800,425,1050),36)
add(0,119.1,137.166667,'loop','numbers',(1170,160,1555,690),T,(1362,425,1050),36)
# Native definition shot is frozen from an approved clean source frame.
add(0,137.166667,145.333333,'mirror','definition')
add(0,162.066667,167.7,'quote','full')
add(0,167.7,173.9,'quote','absolutely-brilliant',(301,231,569,279),P,(800,280,1660),20)
add(0,173.9,176.35,'quote','performance-art',(485,313,1024,361),P,(800,337,1660))
add(0,176.35,179.8,'quote','viral-gold',(261,541,491,589),P,(800,510,1660),15)

# Donor rows use actual prompt-bubble geometry, not generic row rectangles.
add(1,0,26.7,'moves','establish')
rows=[(26.7,56.84,139,317,31.2,40.6,42.5),(56.84,90.4,317,536,60.3,70.5,71.6),(90.4,142.2,536,755,94.0,104.4,106.5),(142.2,186.5,755,974,145.3,153.1,154.8)]
for i,(start,end,y1,y2,weak,between,better) in enumerate(rows,1):
    cam=(800,(y1+y2)/2,1680)
    wr=(585,y1+12,1510,y1+76)
    br=(610,y1+85,1510,y2-26)
    add(1,start,weak,'moves',f'move-{i}-intro',(40,y1,1560,y2),P,cam,24 if i<3 else 0)
    add(1,weak,between,'moves',f'move-{i}-weak',wr,P,cam)
    add(1,between,end,'moves',f'move-{i}-better',br,T,cam)
# Keep native explanatory artwork as a visual break, never the native board.
native_windows=[(83.7,90.4),(115.0,134.0),(168.433333,179.9),(221.166667,233.2)]
add(1,186.5,203.3,'moves','standing-intro',(40,974,1560,1150),P,(800,1062,1680),24)
add(1,203.3,242.0,'moves','standing-prompt',(610,1000,1510,1108),T,(800,1062,1680))
add(1,242.0,246.0,'moves','takeaway',(40,1190,1560,1278),P,(800,1234,1680),24)

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def main():
    AUDIT.mkdir(parents=True,exist_ok=True)
    (AUDIT/'qa').mkdir(exist_ok=True)
    protected={str(p):sha(p) for p in [RAW,DONOR,ROOT/'videos/flattery-trap.mp4']}
    # Atomic shot replacement: inspect source sequentially, no timestamp seeks.
    cap=cv2.VideoCapture(str(RAW)); mirror=None; title=None
    for f in range(at(136.5)+1):
        ok,im=cap.read(); assert ok
        if f==at(21):title=im.copy()
        if f==at(136.5):mirror=im.copy()
    cap.release()
    # Code-native typography replacement; retain the source's paper surround.
    im=Image.fromarray(cv2.cvtColor(title,cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((100,90,1170,645),radius=18,fill='#53647a',outline='#f5f0df',width=10)
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',172)
    for text,y in [('FLATTERY',158),('TRAP',355)]:
        box=d.textbbox((0,0),text,font=font); x=(1280-(box[2]-box[0]))/2
        d.text((x+5,y+5),text,font=font,fill='#f19c8c',stroke_width=11,stroke_fill='#181a25')
        d.text((x,y),text,font=font,fill='#f19c8c',stroke_width=5,stroke_fill='#f5f0df')
    title=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
    cv2.imwrite(str(AUDIT/'title.png'),title)
    canvases={k:v.build_canvas(p) for k,p in boards.items()}
    # Half-open frame selections. Retain optional gaps explanation for this review.
    chunks=[]
    def keep(src,a,b):chunks.append(dict(src=src,a=at(a),b=at(b)))
    keep(0,0,42.5);keep(0,47.4,127.8);keep(0,136.95,179.8)
    chunks.append(dict(src=-1,a=0,b=30)) # Exact 1s silent/room-tone pause.
    keep(0,183.466667,202.6)
    keep(1,0,5.95);keep(1,26.7,48.95);keep(1,57.05,64.55)
    keep(1,70.5,134.0);keep(1,142.2,167.75);keep(1,186.5,233.2)
    chunks.append(dict(src=-1,a=0,b=30)) # Owner-requested pause before the closing message.
    keep(0,275.35,283.7)
    total=sum(c['b']-c['a'] for c in chunks)
    # Render each source-mapped state with geometry tied to its exact asset.
    def render_state(s,frame):
        if s['board']=='mirror':return mirror.copy()
        canvas,ox,oy,full=canvases[s['board']]
        cam=v.map_camera(s['camera'],ox,oy) if s['camera'] else full
        arr=states[0] if s in states[0] else states[1]
        idx=arr.index(s)
        if s['move'] and frame-s['start']<s['move']:
            prev=arr[idx-1] if idx else None
            start=v.map_camera(prev['camera'],ox,oy) if prev and prev['board']==s['board'] and prev['camera'] else full
            t=v.smoothstep(max(0,(frame-s['start'])/max(1,s['move']-1)))
            cam=tuple(a+(b-a)*t for a,b in zip(start,cam))
        out=v.crop_frame(canvas,cam)
        if s['rect']:
            rect=v.project_rect(v.map_rect(s['rect'],ox,oy),cam)
            v.rounded_ring(out,rect,v.hex_bgr(s['color']),radius=18,thickness=5)
        return out
    close=cv2.imread(str(ROOT/'lessons/flattery-trap-5-close.jpg'))
    close=cv2.resize(close,(1600,900),interpolation=cv2.INTER_AREA)
    def render_close(frame):
        # Same fixed close framing and timing as common.render_close.
        index=frame-at(275.35)
        if index<48:width=1600.0
        elif index<198:
            amount=v.smoothstep((index-48)/149)
            width=1600+(1600/1.2-1600)*amount
        else:width=1600/1.2
        return v.crop_frame(close,(800,450,width))
    temp=AUDIT/'picture-only.mp4'
    process=subprocess.Popen([FF,'-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','-','-an','-c:v','libx264','-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-crf','18','-preset','fast',str(temp)],stdin=subprocess.PIPE)
    captures={};positions={}; boundaries={}; settled=[]; seen=set();cursor=0;last=None;lastlabel=None
    for n,c in enumerate(chunks):
        if cursor:boundaries[cursor]=f'chunk-{n}'
        c['output_start']=cursor
        print('Render chunk',n,'source',c['src'],c['a']/30,c['b']/30,'output',cursor/30,flush=True)
        src=c['src']
        if src>=0:
            if src not in captures:
                captures[src]=cv2.VideoCapture(str(sources[src]));positions[src]=0
            cap=captures[src]
            while positions[src]<c['a']:
                assert cap.grab();positions[src]+=1
        for f in range(c['a'],c['b']):
            if src==-1:out=last.copy();label='inserted-pause'
            else:
                ok,native=cap.read();assert ok;positions[src]+=1
                active=next((s for s in states[src] if s['start']<=f<s['end']),None)
                if src==0 and f>=at(275.35):out=render_close(f);label='standard-close'
                elif src==0 and 598<=f<687:out=title.copy();label='flattery-trap-title'
                elif src==1 and any(at(a)<=f<at(b) for a,b in native_windows):out=native;label='donor-native'
                elif active:out=render_state(active,f);label=active['board']+'/'+active['label']
                else:out=native;label=f'native-{src}'
                if active and label not in seen and f>=active['start']+max(30,active['move']+5):
                    settled.append(dict(frame=cursor,label=label,source_frame=f,rect=active['rect'],camera=active['camera']))
                    cv2.imwrite(str(AUDIT/'qa'/f'{cursor:06d}-{label.replace("/","-")}.jpg'),out)
                    seen.add(label)
            if lastlabel is not None and label!=lastlabel:boundaries[cursor]=label
            process.stdin.write(out.tobytes());cursor+=1;last=out;lastlabel=label
        c['output_end']=cursor
    process.stdin.close();assert process.wait()==0
    for cap in captures.values():cap.release()
    assert cursor==total
    # All audio comes from the approved source takes. Tiny edge ramps only.
    graph=[];labels=[]
    for i,c in enumerate(chunks):
        dur=(c['b']-c['a'])/30
        if c['src']==-1:
            graph.append(f'anullsrc=r=44100:cl=mono,atrim=duration=1,asetpts=PTS-STARTPTS[a{i}]')
        else:
            graph.append(f'[{c["src"]+1}:a]atrim=start={c["a"]/30:.9f}:end={c["b"]/30:.9f},asetpts=PTS-STARTPTS,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,afade=t=in:d=0.003,afade=t=out:st={dur-.003:.9f}:d=0.003,apad,atrim=duration={dur:.9f}[a{i}]')
        labels.append(f'[a{i}]')
    graph.append(''.join(labels)+f'concat=n={len(labels)}:v=0:a=1[a]')
    subprocess.run([FF,'-y','-hide_banner','-loglevel','error','-i',str(temp),'-i',str(RAW),'-i',str(DONOR),'-filter_complex',';'.join(graph),'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUT)],check=True)
    assert common.frame_count(OUT)==total
    media_info=subprocess.run([FF,'-hide_banner','-i',str(OUT)],stderr=subprocess.PIPE,text=True).stderr
    assert 'yuv420p' in media_info and 'High 4:4:4' not in media_info, media_info
    for p,h in protected.items():assert sha(p)==h,p
    manifest=dict(output=str(OUT),frames=total,duration=total/30,chunks=chunks,states=settled,boundaries=boundaries,protected=protected,output_sha256=sha(OUT))
    (AUDIT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(OUT),'--outdir',str(AUDIT/'transitions')]
    for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
    subprocess.run(cmd,check=False) # Motion alerts require the recorded manual strip review.
    print('COMPLETE',OUT,total/30,flush=True)

if __name__=='__main__':main()
