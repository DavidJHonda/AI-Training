#!/usr/bin/env python3
"""Approved November 3 four-benefit assembly; never installs or overwrites."""
from pathlib import Path
import json, subprocess, sys
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont
from editspec_build import Build, Reader, readwav, writewav, sha
from ken_burns_path import draw_ring, hex_bgr
from gemini_mark import clean_frame, glyph_mask
from render_big_upside_benefits import BOARDS, wrap

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/big-upside-build-2026-11-03-v9'
DEST=ROOT/'Prompts/big-upside-v9.mp4'
SRC={i:ROOT/f'Prompts/big-upside-{i}.mp4' for i in (1,2,3)}
EXPECTED={1:'c3717ee1b9bc2d4b5aa8a28c3ccf493296bbe296a01610e8b9d0235d70225f3f',2:'d99a8f2879d469a9d670fcc07160c4b7bab0677dd3f6aa88d28ccd3de31c5029',3:'ccdca3d9cd922c15159aad7a86328c9d9d9aecd9a166ea5619bdf3b15942b99d'}
ASSETS={k:ROOT/f'course-assets/big-upside/big-upside-{k}.jpg' for k in ('protein','cancer','reading','flood','close')}
MENU=ROOT/'scripts/video/assets/big-upside-cutaways-2026-09-30/menu-reading.png'
FF=imageio_ffmpeg.get_ffmpeg_exe();F=lambda t:round(t*30);SPF=1600
FONT=ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
END=F(217.4)
CUTS=[(172.475,175.955)]
REPLACE=[(72.775,80.935,61.060,67.850,.0684245086179871,'testing-caveat')]

def audio_plan():
    a,b,c,d,gain,label=REPLACE[0];rows=[];out=0
    for roll,s,e,db,tag in [(1,0,F(a),0,'base'),(3,F(c),F(d),gain,label),(1,F(b),F(CUTS[0][0]),0,'base'),(1,F(CUTS[0][1]),END,0,'base')]:
        rows.append(dict(roll=roll,source_start=s,source_end=e,start_frame=out,end_frame=out+e-s,gain_db=db,label=tag));out+=e-s
    return rows

def board_views():
    b=Build(ROOT,SRC[1],OUT,DEST);views={};metadata={}
    colors=dict(protein='#4f2fc4',cancer='#a9760c',reading='#0e8f86',flood='#1652f0')
    for key in colors:
        # One complete illustrated card; distinct right-hand teaching sections.
        blocks=next(row[3] for row in BOARDS if row[0]==key)
        measure=ImageDraw.Draw(Image.new('RGB',(1600,662)))
        lines=[len(wrap(measure,body,558)) for title,body in blocks]
        second_y=151+62+lines[0]*41+36
        rects=[(40,127,1560,622),(940,137,1544,second_y-20),
               (940,second_y-14,1544,second_y+62+lines[1]*41+8)]
        p,cw,ch,ox,oy=b.compose(ASSETS[key],key)
        base=cv2.resize(cv2.imread(str(p)),(1280,720),interpolation=cv2.INTER_AREA)
        views[key,None]=base
        for i,rect in enumerate(rects):
            x,y,z,v=rect;im=base.copy();sx=1280/cw;sy=720/ch
            draw_ring(im,(x+ox)*sx,(y+oy)*sy,(z+ox)*sx,(v+oy)*sy,hex_bgr(colors[key]),12,4)
            views[key,i]=im
        metadata[key]=dict(asset=str(ASSETS[key].relative_to(ROOT)),sha256=sha(ASSETS[key]),density='compact',camera='static full view',canvas=[cw,ch],offset=[ox,oy],rectangles=rects,color=colors[key],ring_pixels=4)
    return views,metadata

def picture_plan(rows):
    states=[]
    for r in rows:
        for f in range(r['start_frame'],r['end_frame']):
            sf=r['source_start']+f-r['start_frame']
            if r['roll']==3:
                state=('board','protein',None) if sf<F(64.7) else ('clip',2,F(94)+sf-F(64.7),'testing laboratory')
            elif F(23.3666667)<=sf<F(29.1333333):
                state=('clip',2,F(239.8)+sf-F(23.3666667),'community benefits')
            elif F(50.4)<=sf<F(57.3666667):
                state=('clip',2,F(88)+sf-F(50.4),'slow experimental research')
            elif F(57.3666667)<=sf<F(81.3666667):
                active=None if sf<F(59.3666667) or sf>=F(72.775) else 0 if sf<F(60.96) else 1 if sf<F(66.98) else 2
                state=('board','protein',active)
            elif F(81.3666667)<=sf<F(90.6666667):
                state=('board','cancer',None if sf<F(83.3666667) else 0)
            elif F(99.4)<=sf<F(115.4):
                active=None if sf<F(101.4) else 0 if sf<F(102.68) else 1 if sf<F(109.38) else 2
                state=('board','cancer',active)
            elif F(115.4)<=sf<F(123.3333333):
                state=('menu',)
            elif F(130.3666667)<=sf<F(144.2333333):
                active=None if sf<F(132.3666667) else 0 if sf<F(132.92) else 1 if sf<F(137.24) else 2
                state=('board','reading',active)
            elif F(164.2)<=sf<F(183.1333333):
                active=None if sf<F(166.22) else 1 if sf<F(176.34) else 2
                state=('board','flood',active)
            elif sf>=F(208.7666667):state=('close',)
            else:state=('clip',1,sf,'forecast label correction' if F(158.9666667)<=sf<F(164.2) else 'retained supporting scene')
            states.append(state)
    spans=[]
    for f,state in enumerate(states):
        same=False
        if spans:
            p=spans[-1];s=p['state'];same=(state==s if state[0]!='clip' else s[0]=='clip' and state[1]==s[1] and state[3]==s[3] and state[2]==s[2]+f-p['start_frame'])
        if same:spans[-1]['end_frame']=f+1
        else:spans.append(dict(start_frame=f,end_frame=f+1,state=state))
    return spans

def correct_forecast(frame):
    """Track the existing moving forecast badge; replace only its text interior."""
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    roi=gray[80:350,820:1270]
    mask=(roi<185).astype(np.uint8)*255
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
    count,labels,stats,centers=cv2.connectedComponentsWithStats(mask)
    boxes=[]
    for x,y,w,h,area in stats[1:]:
        if w>130 and h>30 and area>w*h*.65:boxes.append((area,int(x+820),int(y+80),int(w),int(h)))
    if not boxes:return frame,None
    _,x,y,w,h=max(boxes)
    # The patch stays inside the original rounded card and preserves its outline.
    x0,x1=x+10,x+w-10;y0,y1=y+8,y+h-8
    bg=np.median(frame[y+8:y+15,x+10:x+35].reshape(-1,3),axis=0).astype(np.uint8)
    patch=Image.new('RGB',(x1-x0,y1-y0),tuple(int(v) for v in bg[::-1]));draw=ImageDraw.Draw(patch)
    # Follow the original fade-in contrast; do not introduce a bright flash.
    alpha=float(np.clip((220-float(bg.mean()))/160,0,1))
    for text,frac,size,color in [('EARLY FLOOD WARNING',.27,.105,(220,218,210)),('DAYS AHEAD',.60,.15,(218,92,75))]:
        font=ImageFont.truetype(str(FONT),max(10,round(w*size/2)))
        rgb=tuple(round(float(bg[::-1][i])*(1-alpha)+color[i]*alpha) for i in range(3))
        draw.text(((x1-x0)/2,(y1-y0)*frac),text,font=font,fill=rgb,anchor='mm')
    result=frame.copy();result[y0:y1,x0:x1]=cv2.cvtColor(np.array(patch),cv2.COLOR_RGB2BGR)
    return result,[x,y,w,h]

def still_frame(image,progress):
    h,w=image.shape[:2];z=1+.025*progress;ww=min(w,h*16/9)/z;hh=ww*9/16
    return cv2.warpAffine(image,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)

def close_frame(image,f,start):
    q=np.clip((f-start-48)/149,0,1);z=1+.2*q*q*(3-2*q)
    h,w=image.shape[:2];ww=w/z;hh=ww*9/16
    return cv2.warpAffine(image,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)

def main():
    cv2.setNumThreads(2);OUT.mkdir(exist_ok=True);assert not DEST.exists(),'Never overwrite a candidate'
    for k,p in SRC.items():assert sha(p)==EXPECTED[k]
    protected={str(p):sha(p) for p in [*SRC.values(),*ASSETS.values(),MENU,ROOT/'course-assets/big-upside/big-upside.mp4',ROOT/'index.html',ROOT/'lessons/big-upside.md']}
    rows=audio_plan();total=rows[-1]['end_frame'];seams=[r['start_frame'] for r in rows[1:]];audio={}
    for k in (1,3):
        p=OUT/f'source-{k}.wav'
        if not p.exists():subprocess.run([FF,'-v','error','-i',str(SRC[k]),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(p)],check=True)
        audio[k]=readwav(p)
    original=np.concatenate([audio[r['roll']][r['source_start']*SPF:r['source_end']*SPF]*10**(r['gain_db']/20) for r in rows]);edited=original.copy()
    for f in seams:
        n=f*SPF;edited[n-240:n]*=np.linspace(1,0,240);edited[n:n+240]*=np.linspace(0,1,240)
    writewav(OUT/'edited.wav',edited)
    for i,f in enumerate(seams):writewav(OUT/f'join-{i+1:02d}-{f/30:.2f}s.wav',edited[max(0,f-120)*SPF:min(total,f+180)*SPF])
    views,boards=board_views();spans=picture_plan(rows);close_start=next(r['start_frame'] for r in spans if r['state'][0]=='close')
    subprocess.run([sys.executable,str(ROOT/'scripts/video/make_close_board.py'),'--lesson','bigupside','--out',str(OUT/'close.png')],check=True)
    close=cv2.imread(str(OUT/'close.png'));menu=cv2.imread(str(MENU));mask=glyph_mask();cleaned={'clone':0,'inpaint':0,'declined':[]};patches=[]
    m=dict(candidate=str(DEST.relative_to(ROOT)),scope='Approved full production pass; review candidate only',fps=30,frames=total,duration=total/30,audio_timeline=rows,visual_timeline=spans,boards=boards,cuts_source_seconds=CUTS,replacements_source_seconds=REPLACE,protected_hashes=protected,audio_joins=seams,
           audio='Pristine roll 1 plus one complete roll 3 beat; +0.068 dB donor gain; 5ms quiet-endpoint ramps only at three audio seams. No added internal pauses or speed changes.',
           close=dict(start_frame=close_start,prehold_frames=48,push_frames=150,zoom=1.2,settle_frames=total-close_start-198),listening_completed=False,continuous_playback_review_completed=False)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    for (key,i),im in views.items():cv2.imwrite(str(OUT/f'state-{key}-{i}.jpg'),im)
    temp=OUT/'rendering.mp4';assert not temp.exists()
    cmd=[FF,'-v','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)]
    (OUT/'command.json').write_text(json.dumps(cmd,indent=2)+'\n');proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);readers={};written=0
    for span in spans:
        kind,*args=span['state']
        for f in range(span['start_frame'],span['end_frame']):
            if kind=='board':im=views[tuple(args)]
            elif kind=='close':im=close_frame(close,f,close_start)
            elif kind=='menu':im=still_frame(menu,(f-span['start_frame'])/(span['end_frame']-span['start_frame']-1))
            else:
                roll,start,label=args;n=start+f-span['start_frame']
                # Community shot is already fully visible at 239.8s; cap before next close.
                if label=='community benefits':n=min(n,F(244.5)-1)
                if roll not in readers or readers[roll].n>n:
                    if roll in readers:readers[roll].c.release()
                    readers[roll]=Reader(SRC[roll])
                im=readers[roll].at(n)
                if label=='forecast label correction':
                    im,rect=correct_forecast(im)
                    if rect:patches.append(dict(output_frame=f,source_frame=n,rect=rect))
                im,how=clean_frame(im,mask)
                if how:cleaned[how]+=1
                else:cleaned['declined'].append(f)
            proc.stdin.write(im.tobytes());written+=1
        print(f'Rendered {written}/{total} frames ({written/30:.1f}s)',flush=True)
    proc.stdin.close();assert proc.wait()==0;assert written==total
    for r in readers.values():r.c.release()
    assert all(sha(p)==h for p,h in protected.items());temp.rename(DEST)
    m.update(sha256=sha(DEST),corner_cleanup=cleaned,forecast_patch_frames=patches,protected_files_unchanged=True)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(f'Created {DEST}: {total/30:.3f}s',flush=True)

if __name__=='__main__':main()
