#!/usr/bin/env python3
"""Approved three-roll assembly. New review candidate; never installs or overwrites.

Audio edits and visual cuts are independent: no audio processing at picture cuts.
All times in the plan are pristine-source times, rounded to 30 fps.
"""
from pathlib import Path
import json, subprocess, sys
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import Build, Reader, readwav, writewav, sha
from ken_burns_path import draw_ring, hex_bgr
from gemini_mark import clean_frame, glyph_mask

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/pace-of-change-build-2026-11-03-v11'
DEST=ROOT/'Prompts/pace-of-change-v11.mp4'
SRC={i:ROOT/f'Prompts/pace-of-change-{i}.mp4' for i in (1,2,3)}
EXPECTED={1:'bc39b6e0a0b90af47e940673830f8e684a846c626a37affe6a669d98b9b8da59',2:'ec5f817f7613783663f8d8c44a36ea55e0817efc02801b8ec987577a6bf41f8d',3:'439a7bfeebbb3b9f5bb19828b6f39df3649b58147bbdc75a6120dc91666fe884'}
ASSETS={k:ROOT/f'course-assets/pace-of-change/pace-of-change-{v}.jpg' for k,v in [('comparison','three-years'),('drivers','what-speeds-it-up'),('future','three-future-ideas'),('close','close')]}
FF=imageio_ffmpeg.get_ffmpeg_exe()
F=lambda t:round(t*30)
SPF=1600
CUTS=[(9.33,20.855),(92.02,105.295),(138.555,149.495),(205.045,220.07),(271.205,276.3)]
REPLACE=[(37.295,54.93,45.385,60.095,-.3308660387,'images'),(120.555,133.38,111.5,121.54,-.3493055741,'release-goals')]
END=F(283.8)
VIDEO_LIMITS={}  # Optional exclusive donor-frame caps for reviewed later builds.

def audio_plan():
    events=[(F(a),F(b),None) for a,b in CUTS]+[(F(a),F(b),(F(c),F(d),gain,label)) for a,b,c,d,gain,label in REPLACE]
    rows=[];cur=out=0
    def add(roll,a,b,gain=0,label='base'):
        nonlocal out
        rows.append(dict(roll=roll,source_start=a,source_end=b,start_frame=out,end_frame=out+b-a,gain_db=gain,label=label));out+=b-a
    for a,b,repl in sorted(events):
        if a>cur:add(1,cur,a)
        if repl:
            c,d,gain,label=repl;add(2,c,d,gain,label)
        cur=b
    add(1,cur,END)
    return rows

def output_frame(sf,rows):
    for r in rows:
        if r['roll']==1 and r['source_start']<=sf<r['source_end']:
            return r['start_frame']+sf-r['source_start']
    raise ValueError(sf)

def board_views():
    b=Build(ROOT,SRC[1],OUT,DEST)
    rects={'comparison':[(72,224,1528,382),(72,400,1528,560),(72,580,1528,781),(72,800,1528,928)],
           'drivers':[(40,127,525,692),(557,127,1043,692),(1075,127,1560,692)],
           'future':[(40,127,525,728),(557,127,1043,728),(1075,127,1560,728)]}
    colors={'comparison':['#4f2fc4']*4,'drivers':['#4f2fc4','#1652f0','#0e8f86'],'future':['#4f2fc4','#1652f0','#c41f28']}
    views={};metadata={}
    for key,rs in rects.items():
        p,cw,ch,ox,oy=b.compose(ASSETS[key],key)
        base=cv2.resize(cv2.imread(str(p)),(1280,720),interpolation=cv2.INTER_AREA)
        views[key,None]=base
        for i,(rect,color) in enumerate(zip(rs,colors[key])):
            x,y,z,v=rect;im=base.copy();sx=1280/cw;sy=720/ch
            draw_ring(im,(x+ox)*sx-2,(y+oy)*sy-2,(z+ox)*sx+2,(v+oy)*sy+2,hex_bgr(color),14*sx+2,4)
            views[key,i]=im
        metadata[key]=dict(asset=str(ASSETS[key].relative_to(ROOT)),sha256=sha(ASSETS[key]),density='compact',camera='static full view',canvas=[cw,ch],offset=[ox,oy],rectangles=rs,colors=colors[key],ring_pixels=4)
    return views,metadata

def picture_plan(rows):
    # Priority: these source-time cutaways override the canonical board beneath.
    inserts=[(0,4.6,3,0,'drawn conversation'),(31,35,3,10.5,'computer tools'),
             (62,65.5,2,22,'person working with context'),(85,89,2,167,'code and agent work'),
             (105.295,109.295,2,103.3,'competition'),(109.295,116.295,3,121.5,'company race'),
             (116.295,120.555,2,107.4,'frequent releases'),
             (133.38,138.555,1,133.8,'limitation can change'),
             (173.2,179.2,2,0,'compute infrastructure'),(193,197,2,167,'human-directed AI coding'),
             (231,235.5,1,207.5,'hypothetical recursive loop'),(243,246.5,3,147,'human work'),
             (264,271.205,3,264.9,'uncertain future')]
    inserts=[(F(a),F(b),roll,F(start),label) for a,b,roll,start,label in inserts]
    states=[]
    for r in rows:
        for f in range(r['start_frame'],r['end_frame']):
            sf=r['source_start']+f-r['start_frame']
            if r['roll']==2:
                state=('board','comparison',1) if r['label']=='images' else ('clip',2,sf,'release goals')
            else:
                ins=next((i for i in inserts if i[0]<=sf<i[1]),None)
                if ins:
                    a,b,roll,start,label=ins;state=('clip',roll,start+sf-a,label)
                elif sf>=F(276.3):state=('close',)
                elif sf>=F(220.07):
                    active=None if sf<F(225.32) or sf>=F(261.82) else 0 if sf<F(238.0) else 1 if sf<F(252.56) else 2
                    state=('board','future',active)
                elif sf>=F(149.495):
                    active=None if sf<F(157.92) else 0 if sf<F(169.60) else 1 if sf<F(185.68) else 2
                    state=('board','drivers',active)
                else:
                    active=None if sf<F(21.36) else 0 if sf<F(37.295) else 2 if sf<F(77.52) else 3
                    state=('board','comparison',active)
            states.append(state)
    # Compact adjacent states into inspectable picture spans, independent of audio.
    spans=[]
    for f,state in enumerate(states):
        continuation=False
        if spans:
            p=spans[-1];s=p['state'];continuation=(state==s if state[0]!='clip' else s[0]=='clip' and state[1]==s[1] and state[3]==s[3] and state[2]==s[2]+f-p['start_frame'])
        if continuation:spans[-1]['end_frame']=f+1
        else:spans.append(dict(start_frame=f,end_frame=f+1,state=state))
    return spans

def main():
    cv2.setNumThreads(2);OUT.mkdir(exist_ok=True)
    assert not DEST.exists(),'Never overwrite a review candidate'
    for k,p in SRC.items():assert sha(p)==EXPECTED[k],p
    protected={str(p):sha(p) for p in [*SRC.values(),*ASSETS.values(),ROOT/'course-assets/pace-of-change/pace-of-change.mp4']}
    rows=audio_plan();total=rows[-1]['end_frame'];seams=[r['start_frame'] for r in rows[1:]]
    audio={}
    for k in (1,2):
        p=OUT/f'source-{k}.wav'
        if not p.exists():subprocess.run([FF,'-v','error','-i',str(SRC[k]),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(p)],check=True)
        audio[k]=readwav(p)
    pieces=[audio[r['roll']][r['source_start']*SPF:r['source_end']*SPF]*10**(r['gain_db']/20) for r in rows]
    original=np.concatenate(pieces);edited=original.copy()
    for f in seams:
        n=f*SPF
        edited[n-240:n]*=np.linspace(1,0,240)
        edited[n:n+240]*=np.linspace(0,1,240)
    writewav(OUT/'edited.wav',edited)
    for i,f in enumerate(seams):writewav(OUT/f'join-{i+1:02d}-{f/30:.2f}s.wav',edited[max(0,f-120)*SPF:min(total,f+180)*SPF])
    views,boards=board_views();spans=picture_plan(rows)
    close_start=next(r['start_frame'] for r in spans if r['state'][0]=='close')
    assert total-close_start>198
    subprocess.run([sys.executable,str(ROOT/'scripts/video/make_close_board.py'),'--lesson','paceofchange','--out',str(OUT/'close.png')],check=True)
    close=cv2.imread(str(OUT/'close.png'))
    mask=glyph_mask();cleaned={'clone':0,'inpaint':0,'declined':[]}
    manifest=dict(candidate=str(DEST.relative_to(ROOT)),scope='Full production pass; review only',fps=30,frames=total,duration=total/30,audio_timeline=rows,visual_timeline=spans,boards=boards,
                  cuts_source_seconds=CUTS,replacements_source_seconds=REPLACE,protected_hashes=protected,
                  audio='Two roll-2 grafts level matched with active-speech RMS. Five-ms fades only at actual narration joins. No added pauses; retained natural ending through source 283.8s.',
                  audio_joins=seams,video_limits=VIDEO_LIMITS,close=dict(start_frame=close_start,prehold_frames=48,push_frames=150,zoom=1.2,settle_frames=total-close_start-198),
                  listening_completed=False,continuous_playback_review_completed=False)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    for (key,i),im in views.items():cv2.imwrite(str(OUT/f'state-{key}-{i}.jpg'),im)
    temp=OUT/'rendering.mp4';assert not temp.exists()
    cmd=[FF,'-v','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)]
    (OUT/'command.json').write_text(json.dumps(cmd,indent=2)+'\n')
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    readers={};written=0
    for span in spans:
        kind,*args=span['state']
        for f in range(span['start_frame'],span['end_frame']):
            if kind=='board':im=views[tuple(args)]
            elif kind=='close':
                q=np.clip((f-close_start-48)/149,0,1);z=1+.2*q*q*(3-2*q)
                h,w=close.shape[:2];ww=w/z;hh=ww*9/16
                im=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            else:
                roll,start,label=args;n=start+f-span['start_frame']
                if label in VIDEO_LIMITS:n=min(n,VIDEO_LIMITS[label]-1)
                if roll not in readers or readers[roll].n>n:
                    if roll in readers:readers[roll].c.release()
                    readers[roll]=Reader(SRC[roll])
                im=readers[roll].at(n);im,how=clean_frame(im,mask)
                if how:cleaned[how]+=1
                else:cleaned['declined'].append(f)
            proc.stdin.write(im.tobytes());written+=1
        print(f'Rendered {written}/{total} frames ({written/30:.1f}s)',flush=True)
    proc.stdin.close();assert proc.wait()==0;assert written==total
    for r in readers.values():r.c.release()
    assert all(sha(p)==v for p,v in protected.items())
    temp.rename(DEST)
    manifest.update(sha256=sha(DEST),corner_cleanup=cleaned,protected_files_unchanged=True)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Created {DEST} — {total/30:.3f}s',flush=True)

if __name__=='__main__':main()
