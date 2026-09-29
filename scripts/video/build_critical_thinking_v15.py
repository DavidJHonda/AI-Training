#!/usr/bin/env python3
"""Approved visual-only repairs; v14 audio and all timeline positions preserved."""
from pathlib import Path
import argparse, hashlib, json, subprocess, shutil
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/critical-thinking/critical-thinking.mp4'
SRC = Path('/private/tmp/critical-thinking-v15-source-194681a637a4.mp4')
EXPECTED = '194681a637a4b39c50aa7edcb6bb543cfad53c9febe301a2fc87eb6bdbeaead4'
OUT = ROOT / 'video-audit/critical-thinking-v15-2026-09-29'
ASSET = ROOT / 'scripts/video/assets/critical-thinking-v15'
DEST = ROOT / 'Prompts/critical-thinking-v15.mp4'
FPS, W, H, N = 30, 1280, 720, 5593
DIAGRAM = (2154, 2697)
HEADING = (2903, 3072)
PAPER = (3198, 3468)
SPANS = [(*DIAGRAM, 'revised-data-diagram'), (*HEADING, 'study-heading'), (*PAPER, 'corrected-article')]
FONT = ROOT / 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def smooth(v):
    v = np.clip(v, 0., 1.)
    return v*v*(3-2*v)

def font(sz, bold=False):
    f = ImageFont.truetype(str(FONT), sz*2)
    f.set_variation_by_axes([700 if bold else 450])
    return f

def layer():
    return Image.new('RGBA', (W*2, H*2))

def text(im, xy, value, size, color='#27332e', bold=False, anchor='mm'):
    ImageDraw.Draw(im).text((xy[0]*2, xy[1]*2), value, font=font(size, bold), fill=color, anchor=anchor)

def line(im, xy, color, width=2):
    ImageDraw.Draw(im).line([(x*2,y*2) for x,y in xy], fill=color, width=width*2)

def ellipse(im, xy, fill, outline=None, width=2):
    ImageDraw.Draw(im).ellipse(tuple(int(v*2) for v in xy), fill=fill, outline=outline, width=width*2)

def prepare_layers():
    title = layer()
    text(title,(640,87),'SMALL STUDY. MANY MEASUREMENTS.',34,bold=True)
    text(title,(640,136),'Testing many outcomes can produce chance findings.',24)
    people = layer()
    text(people,(310,240),'15 participants',30,bold=True)
    for i in range(15):
        x,y=182+(i%5)*64,320+(i//5)*67
        ellipse(people,(x-17,y-17,x+17,y+17),'#e5e9dc','#606759')
        ellipse(people,(x-5,y-5,x+5,y+5),'#606759')
    outcomes = layer()
    text(outcomes,(930,236),'18 measurements',30,bold=True)
    text(outcomes,(930,274),'per person',22)
    for i in range(18):
        x,y=780+(i%6)*60,326+(i//6)*64
        ellipse(outcomes,(x-14,y-14,x+14,y+14),'#dce4d7','#586c62')
    arrow = layer()
    line(arrow,[(526,390),(645,390),(692,390)],'#7b8e80',3)
    line(arrow,[(678,379),(692,390),(678,401)],'#7b8e80',3)
    highlight = layer()
    x,y=960,454
    ellipse(highlight,(x-21,y-21,x+21,y+21),None,'#ae4449',3)
    ellipse(highlight,(x-14,y-14,x+14,y+14),'#ae4449')
    line(highlight,[(960,478),(960,494),(875,494)],'#ae4449',2)
    text(highlight,(840,520),'One outcome appears to stand out',22,'#933c42',bold=True)
    conclusion = layer()
    text(conclusion,(640,613),'A chance result can look like a discovery.',29,bold=True)
    return [np.asarray(x.resize((W,H),Image.Resampling.LANCZOS)) for x in
            (title,people,outcomes,arrow,highlight,conclusion)]

def composite(base, rgba, amount=1.):
    a=rgba[:,:,3:4].astype(np.float32)*(amount/255)
    return np.clip(base*(1-a)+rgba[:,:,:3][:,:,::-1]*a+.5,0,255).astype(np.uint8)

def diagram_frame(idx, bg, layers):
    t=(idx-DIAGRAM[0])/FPS
    f=bg.copy()
    # Actual spoken beats: intro 71.88; participants 75.42; measurements 79.52;
    # design problem 83.84; chance finding 86.80.
    for lay,onset,duration in zip(layers,[0.10,3.50,7.55,8.25,12.05,14.65],[.45,.50,.50,.45,.65,.50]):
        a=float(smooth((t-onset)/duration))
        if a: f=composite(f,lay,a)
    return f

def title_assets(ref):
    # The source title stays at identical coordinates throughout its opacity animation.
    roi=ref[184:214,620:914]
    mask=(cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)<150).astype(np.uint8)
    mask=cv2.dilate(mask,np.ones((3,3),np.uint8),iterations=1)
    ink=ref[188:209,630:902][cv2.cvtColor(ref[188:209,630:902],cv2.COLOR_BGR2GRAY)<100].mean(axis=0)
    sample=cv2.cvtColor(ref[188:209,630:902],cv2.COLOR_BGR2GRAY)<100
    title=layer()
    text(title,(766,198),'DELIBERATELY FLAWED STUDY',18,'#30332b',bold=True)
    title=np.asarray(title.resize((W,H),Image.Resampling.LANCZOS))
    return mask,ink,sample,title

def fix_heading(f, assets):
    mask,ink,sample,title=assets
    bg=np.median(f[215:225,630:902],axis=(0,1))
    current=f[188:209,630:902][sample].mean(axis=0)
    opacity=float(np.clip(np.mean((bg-current)/(bg-ink)),0,1))
    f=f.copy()
    # Only remove the old letter shapes, leaving panel, paper, fades and moving
    # illustrations untouched. The flat panel's current color tracks its fade.
    roi=f[184:214,620:914]
    roi[mask.astype(bool)]=np.clip(bg+.5,0,255).astype(np.uint8)
    return composite(f,title,opacity),opacity

def paper_frame(idx, paper):
    # Maintain the source shot's gentle pullback; full corrected text stays in view.
    t=(idx-PAPER[0])/(PAPER[1]-PAPER[0]-1)
    z=1.025-.025*float(smooth(t))
    matrix=np.float32([[z,0,(1-z)*W/2],[0,z,(1-z)*H/2]])
    return cv2.warpAffine(paper,matrix,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT_101)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');a=ap.parse_args()
    assert sha(LIVE)==EXPECTED,'Source differs from evaluated v14.'
    if not SRC.exists():shutil.copyfile(LIVE,SRC)
    assert sha(SRC)==EXPECTED,'Active-build source snapshot does not match v14.'
    OUT.mkdir(parents=True,exist_ok=True);ASSET.mkdir(parents=True,exist_ok=True)
    if not a.preview: assert not DEST.exists(),'Never overwrite a review candidate.'
    protected={str(p.relative_to(ROOT)):sha(p) for p in [ROOT/'index.html',*sorted(LIVE.parent.glob('*'))] if p.is_file()}
    (OUT/'protected-before.json').write_text(json.dumps(protected,indent=2)+'\n')
    paper=cv2.imread(str(ASSET/'annotated-paper-corrected.png'));assert paper is not None
    paper=cv2.resize(paper,(W,H),interpolation=cv2.INTER_AREA)
    bg=cv2.imread(str(OUT/'diagram-background.png'));assert bg is not None
    ref=cv2.imread(str(OUT/'source-03030.jpg'));assert ref is not None
    heading=title_assets(ref);layers=prepare_layers()
    preview=OUT/'previews';preview.mkdir(exist_ok=True)
    selected={2154,2262,2376,2520,2670,2696,2903,2910,2915,2920,2940,3030,3050,3060,3071,3198,3270,3390,3467}
    proc=None
    if not a.preview:
        ff=imageio_ffmpeg.get_ffmpeg_exe()
        proc=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}',
          '-r',str(FPS),'-i','pipe:0','-i',str(SRC),'-map','0:v','-map','1:a:0',
          '-c:v','libx264','-crf','16','-preset','medium','-threads','4','-pix_fmt','yuv420p',
          '-c:a','copy','-video_track_timescale','15360','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    cap=cv2.VideoCapture(str(SRC));i=0;opacity=[]
    while True:
        ok,f=cap.read()
        if not ok:break
        if DIAGRAM[0]<=i<DIAGRAM[1]:f=diagram_frame(i,bg,layers)
        elif HEADING[0]<=i<HEADING[1]:
            f,alpha=fix_heading(f,heading);opacity.append([i,alpha])
        elif PAPER[0]<=i<PAPER[1]:f=paper_frame(i,paper)
        if i in selected:cv2.imwrite(str(preview/f'frame-{i:05d}.jpg'),f,[cv2.IMWRITE_JPEG_QUALITY,96])
        if proc:proc.stdin.write(f.tobytes())
        i+=1
        if proc and i%900==0:print(f'{i}/{N} frames',flush=True)
    cap.release();assert i==N,i
    if proc:proc.stdin.close();assert proc.wait()==0
    (OUT/'heading-opacity.json').write_text(json.dumps(opacity)+'\n')
    if not a.preview:
        after={p:sha(ROOT/p) for p in protected}
        # Other tasks may legitimately edit the shared page. Verify this lesson's
        # entire asset directory; report shared-page drift rather than undoing it.
        assert all(after[p]==h for p,h in protected.items() if p!='index.html')
        entry=lambda s:next(x.strip() for x in s.splitlines() if 'critical: { src:' in x)
        assert '20260927critical14' in entry((ROOT/'index.html').read_text())
        record={'source':str(SRC),'source_sha256':EXPECTED,'source_limitation':'Finished v14 source; original rolls unavailable in Prompts. One video encode, audio copied.',
          'output':str(DEST),'output_sha256':sha(DEST),'fps':FPS,'frames':N,'duration_seconds':N/FPS,
          'scope':'Three approved visual repairs; narration, pauses, board spans, opening and close preserved.',
          'approval':'User: Build it, following September 29 evaluation.',
          'changed_spans':[{'start_frame':s,'end_frame_exclusive':e,'label':label} for s,e,label in SPANS],
          'audio':'-c:a copy; verification pending','paper_asset':str(ASSET/'annotated-paper-corrected.png'),
          'paper_sha256':sha(ASSET/'annotated-paper-corrected.png'),'shared_page_changed_concurrently':after['index.html']!=protected['index.html'],
          'publication':'Review candidate only; not installed or published.'}
        (OUT/'edit-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps(record,indent=2),flush=True)

if __name__=='__main__':main()
