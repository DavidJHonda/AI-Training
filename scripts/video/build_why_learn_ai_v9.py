#!/usr/bin/env python3
"""Approved Sept 29 best-of edit. Review candidate only; preserve raw/live files.

Audio: Version 2 with three complete Version 1 passages. Visual timeline is
independent of audio cuts so retained animations can be retimed to donor words.
Uses shared board geometry/ring/close conventions, one final H.264 encode.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, Reader, fr, sha, readwav, writewav, SR, SPF, W, H, FPS, PURPLE, BLUE, RED, GREEN, AMBER, TEAL
from ken_burns_path import resolve, window, rings_for, draw_ring, smoothstep
from gemini_mark import clean_frame, glyph_mask

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'video-audit/why-learn-ai-rerolls-2026-09-29'
OUT = AUDIT / 'build-v9'
DEST = ROOT / 'Prompts/why-learn-ai-v9.mp4'
SRC = ROOT / 'Prompts/why-learn-ai-2.mp4'
DONOR = ROOT / 'Prompts/why-learn-ai-1.mp4'
ASSETS = OUT / 'assets'
COURSE = ROOT / 'course-assets/why-learn-ai'
BOARDS = {k: COURSE / f'why-learn-ai-{k}.jpg' for k in ['press','everyday','thrive','close']}
GRAFTS = [('press',810,1002,762,1128),('practice-design',2878,4176,2105,3538),('history-quote',5813,6682,4628,5359)]

def active_db(audio, spans):
    levels=[]
    for s,e in spans:
        for i in range(fr(s)*SPF, fr(e)*SPF-2400,2400):
            a=audio[i:i+2400]; r=float(np.sqrt(np.mean(a*a)))
            if r>32768*10**(-35/20): levels.append(r*r)
    return float(20*np.log10(np.sqrt(np.mean(levels))/32768))

class BoardRenderer:
    def __init__(self,spec):
        self.spec=spec; self.im=cv2.imread(spec['image']); self.h,self.w=self.im.shape[:2]
        self.beats=resolve(spec,W/H,W,3); self.rings=rings_for(spec)
        self.big=cv2.resize(self.im,(self.w*3,self.h*3),interpolation=cv2.INTER_LANCZOS4)
        self.cached=None; self.last_key=None
    def at(self,f):
        cursor=0
        for _,n,a,b in self.beats:
            if f<cursor+n: break
            cursor+=n
        q=smoothstep((f-cursor)/(n-1)) if n>1 else 1
        cam=[a[j]+(b[j]-a[j])*q for j in range(3)]
        active=tuple(i for i,r in enumerate(self.rings) if r[0]<=f<r[1])
        key=tuple(cam)+active
        if key==self.last_key: return self.cached.copy()
        x,y,ww,hh=window(*cam,W/H,self.w,self.h)
        crop=self.big[round(y*3):round((y+hh)*3),round(x*3):round((x+ww)*3)]
        im=cv2.resize(crop,(W,H),interpolation=cv2.INTER_AREA)
        for i in active:
            _,_,(rx,ry,rw,rh),color,pad,radius=self.rings[i]; scale=W/ww
            draw_ring(im,(rx-pad-x)*scale-2,(ry-pad-y)*scale-2,
                      (rx+rw+pad-x)*scale+2,(ry+rh+pad-y)*scale+2,color,radius*scale+2,4)
        self.last_key=key; self.cached=im.copy(); return im

def text_patch(im,rect,text,size=20):
    x0,y0,x1,y1=rect
    # Source diagrams have a vertical paper gradient; clone clean side pixels
    # at the same y rather than replacing the entire animated scene.
    for y in range(y0,y1): im[y,x0:x1]=np.median(im[y,35:50],axis=0).astype(np.uint8)
    p=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)); d=ImageDraw.Draw(p)
    font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',size)
    d.text(((x0+x1)/2,(y0+y1)/2),text,font=font,fill='#344052',anchor='mm')
    return cv2.cvtColor(np.asarray(p),cv2.COLOR_RGB2BGR)

def repair_frame(im,sf,kind):
    if kind=='skill':
        im=text_patch(im,(280,128,1000,173),'A shorter path from idea to creation',20)
    elif kind=='art':
        mask=np.zeros((H,W),np.uint8)
        cv2.fillPoly(mask,[np.array([[288,467],[348,454],[352,482],[290,493]])],255)
        im=cv2.inpaint(im,mask,3,cv2.INPAINT_TELEA)
    elif kind=='quote' and sf>=fr(215.4):
        # Keep the native panel reveal and outer illustrations. Replace just the
        # unsupported numerical graph with a simple animated information symbol.
        x0,x1,y0,y1=490,799,302,600
        for y in range(y0,y1): im[y,x0:x1]=np.median(im[y,475:488],axis=0).astype(np.uint8)
        q=np.clip((sf-fr(215.4))/35,0,1)
        overlay=im.copy(); ink=(105,91,70); cyan=(175,177,61)
        for x,y in [(560,390),(675,355),(675,470)]:
            cv2.rectangle(overlay,(x-32,y-37),(x+32,y+37),ink,3,cv2.LINE_AA)
            for dy in [-15,0,15]: cv2.line(overlay,(x-19,y+dy),(x+19,y+dy),ink,2,cv2.LINE_AA)
        cv2.line(overlay,(592,390),(643,355),cyan,3,cv2.LINE_AA)
        cv2.line(overlay,(592,390),(643,470),cyan,3,cv2.LINE_AA)
        im=cv2.addWeighted(overlay,float(q),im,float(1-q),0)
    return im

def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    b=Build(ROOT,SRC,OUT,DEST,protected=[DONOR,ROOT/'Prompts/why-learn-ai-3.mp4',COURSE/'why-learn-ai.mp4',ROOT/'lessons/why-learn-ai.md',*BOARDS.values()])
    silence=json.loads((AUDIT/'silences-2.json').read_text())
    b.load_audio([(s+.03,e-.03) for s,e in silence if e-s>.35 and e<225])
    dw=OUT/'donor.wav'
    if not dw.exists(): subprocess.run([b.ff,'-y','-v','error','-i',str(DONOR),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(dw)],check=True)
    da=readwav(dw); gain=active_db(b.audio,[(5,26),(39,95),(146,193)])-active_db(da,[(26,37),(71,117),(155,178)])
    cursor=0; graft_out={}
    for key,s,e,ds,de in GRAFTS:
        b.keep(cursor,s,f'Version 2 narration {cursor/30:.2f}–{s/30:.2f}')
        graft_out[key]=b.cursor
        b.graft(DONOR,ds,de,f'Version 1: {key}',key,picture_from=s,gain_db=gain)
        cursor=e
    b.mark_close_start(); b.close(6682,6784,tail=120)
    b.finish_audio()
    # Fade only the post-speech room-tone tail after the standard close begins.
    audio=readwav(OUT/'edited.wav'); fade=round(.4*SR); start=6955*SPF
    audio[start:start+fade]*=np.linspace(1,0,fade); audio[start+fade:]=0; writewav(OUT/'edited.wav',audio)
    def base(t):
        f=fr(t)
        return f+(174 if 1002<=f<2878 else 309 if 4176<=f<5813 else 171 if f>=6682 else 0)
    def donor(key,t): return graft_out[key]+fr(t)-next(g[3] for g in GRAFTS if g[0]==key)
    ps,pe=810,base(34.1); es,ee=base(48.8333333),graft_out['practice-design']; ts,te=base(139.2),base(177.6666667)
    T=lambda label,at,rect,color:dict(label=label,at=at/30,rects=[rect],cam=rect,color=color,radius=18)
    c5=[[40,136,331,621],[347,136,638,621],[655,136,946,621],[962,136,1253,621],[1269,136,1560,621]]
    c3=[[40,137,530,790],[556,137,1045,790],[1071,137,1560,790]]
    b.board('press',BOARDS['press'],ps,pe,'compact',[],banner_at=donor('press',35.6)/30,push=False)
    b.board('everyday',BOARDS['everyday'],es,ee,'compact',[
        T(l,base(t),r,c) for l,t,r,c in zip(['Recommends','Navigation','Face Recognition','Voice Assistants','Chatbots'],[54,62.18,68.24,75.28,81.36],c5,[PURPLE,BLUE,RED,GREEN,AMBER])],banner_at=base(92.58)/30,push=False)
    b.board('thrive',BOARDS['thrive'],ts,te,'dense',[
        T(l,base(t),r,c) for l,t,r,c in zip(['This Is Your Time',"You’ll Move Faster",'Build Good Habits Early'],[146.14,155.56,163.96],c3,[PURPLE,BLUE,TEAL])],banner_at=base(173.62)/30,pullback_at=base(173)/30)
    b.make_close('whydeeper')
    timeline=[]
    def add(s,e,kind,**kw):
        assert e>s,(s,e,kind)
        if timeline: assert timeline[-1]['end']==s,(timeline[-1],s)
        timeline.append(dict(start=s,end=e,kind=kind,**kw))
    def vid(s,e,vs,ve,source=SRC,repair=None,label=''):
        add(s,e,'video',source=str(source),source_in=vs,source_out=ve,repair=repair,label=label)
    def board(s,e,key): add(s,e,'board',key=key,label=key)
    def still(s,e,key): add(s,e,'still',key=key,label=key)
    vid(0,ps,0,ps,label='Opening scribe and press drawings')
    board(ps,pe,'press')
    vid(pe,es,1023,1465,label='AI in daily life; approved capability animation retained')
    board(es,base(64.5),'everyday');still(base(64.5),base(67.5),'navigation')
    board(base(67.5),base(86),'everyday');still(base(86),base(91.5),'chatbot')
    board(base(91.5),ee,'everyday')
    d=lambda t:donor('practice-design',t)
    vid(ee,d(78.5),2115,fr(78.5),DONOR,label='Passive use to active practice: donor animation')
    vid(d(78.5),d(83.9),fr(78.5),fr(87.6333333),DONOR,label='Strengths, limits, deliberate practice: donor animation')
    vid(d(83.9),d(87.6333333),3180,3324,label='Approved cumulative experience chart retained with numbers')
    vid(d(87.6333333),d(91.9666667),2629,2759,DONOR,label='Bridge from ideas to creation')
    vid(d(91.9666667),d(99.1),3324,3523,label='Drafting before computers')
    vid(d(99.1),d(107.3666667),3523,3837,label='Teenager creating with desktop publishing')
    vid(d(107.3666667),d(114.1),3837,4048,repair='skill',label='Tool shortens the path; human skill remains')
    vid(d(114.1),ts,4048,4185,repair='art',label='Sketch to finished art; AI transfer')
    board(ts,base(157.9),'thrive');still(base(157.9),base(162.9),'feedback');board(base(162.9),te,'thrive')
    # Cover the three rejected Single Sector frames that precede the audio cut.
    hs=5810+309
    vid(te,hs,5330,5810,label='Steam, electricity, internet historical drawings')
    q=lambda t:donor('history-quote',t)
    vid(hs,q(159.6),fr(197.6666667),6031,label='AI across fields; no Single Sector contrast')
    still(q(159.6),q(170.9),'document')
    vid(q(170.9),q(173.0),fr(212.6),fr(215.4),repair='quote',label='Industrial revolution')
    vid(q(173.0),q(174.6),fr(215.4),fr(217.1),repair='quote',label='Information revolution; no 100x claim')
    vid(q(174.6),b.close_start,fr(217.1),6619,repair='quote',label='Renaissance and potential; retain three-part animation')
    add(b.close_start,b.total,'close',label='Canonical two-line close; no Notebook outro')
    m=b.manifest(dict(visual_timeline=timeline,gain_db=gain,added_midvideo_pauses=0,owner_approved_charts=[[44.333333,48.833333],[106,110.8]],listening_verified=False,build_script=str(Path(__file__).resolve())))
    (OUT/'build-plan.json').write_text(json.dumps(m,indent=2))
    return b,m

def render(b,m,preview=False,audio_source=None):
    boards={k:BoardRenderer(json.loads((OUT/f'leg-{k}.json').read_text())) for k in b.boards}
    readers={}; stills={}
    counts={'clone':0,'inpaint':0,'declined':[]}
    # Build the corner mask from a bounded sample of the actual source.
    cap=cv2.VideoCapture(str(SRC)); samples=[]; i=0
    while True:
        ok,im=cap.read()
        if not ok:break
        if i%120==0:samples.append(im)
        i+=1
    cap.release(); mask=glyph_mask(samples)
    if mask is not None:cv2.imwrite(str(OUT/'corner-mask.png'),mask*255)
    def frame(row,f):
        k=f-row['start'];n=row['end']-row['start'];kind=row['kind']
        if kind=='board':return boards[row['key']].at(f-b.boards[row['key']]['src_in'])
        if kind=='video':
            # One sequential reader per visual span; resample the whole source
            # animation when narration length differs, preserving its final state.
            key=row['start']
            if key not in readers: readers[key]=Reader(row['source'])
            r=readers[key]
            sf=row['source_in']+round(k*(row['source_out']-row['source_in']-1)/max(1,n-1))
            im=r.at(sf); im=repair_frame(im,sf,row.get('repair'))
            im,how=clean_frame(im,mask)
            if how in ['clone','inpaint']:counts[how]+=1
            else:counts['declined'].append(f)
            return im
        if kind=='still':
            key=row['key']
            if key not in stills:stills[key]=cv2.imread(str(ASSETS/f'{key}.png'))
            im=stills[key];assert im is not None,key
            h,w=im.shape[:2];ww=min(w,h*16/9);z=1+.025*smoothstep(k/max(1,n-1));ww/=z;hh=ww*9/16
        else:
            im=b.close_img;h,w=im.shape[:2];q=np.clip((k-48)/149,0,1);z=1+.2*smoothstep(q);ww=w/z;hh=ww*9/16
        return cv2.warpAffine(im,np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
    if preview:
        dest=OUT/'preview';dest.mkdir(exist_ok=True)
        for row in m['visual_timeline']:
            for f in sorted(set([row['start'],(row['start']+row['end'])//2,row['end']-1])):
                cv2.imwrite(str(dest/f'frame-{f:06}.jpg'),frame(row,f))
        for key,B in b.boards.items():
            for j,r in enumerate(B['rings']):
                f=min(r['start']+30,B['src_out']-B['src_in']-1)
                cv2.imwrite(str(dest/f'ring-{key}-{j}.jpg'),boards[key].at(f))
        print('Preview complete',b.total,b.total/30,flush=True);return
    assert not DEST.exists(),'Never overwrite a review candidate'
    audio_args=['-c:a','copy'] if audio_source else ['-c:a','aac','-b:a','192k']
    p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(audio_source or OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',*audio_args,'-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for row in m['visual_timeline']:
        print(f"Render {row['start']/30:.2f}–{row['end']/30:.2f}: {row['label']}",flush=True)
        for f in range(row['start'],row['end']):p.stdin.write(frame(row,f).tobytes())
    p.stdin.close();assert p.wait()==0
    m['render_sha256']=sha(DEST);m['corner_mark']=counts
    m['protected_files_unchanged']={k:sha(k)==v for k,v in b.hashes.items()}
    assert all(m['protected_files_unchanged'].values())
    m['boundaries']=[dict(frame=r['start'],label=r['label']) for r in m['visual_timeline'][1:]]
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    print(DEST,flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    b,m=prepare();render(b,m,args.preview)
