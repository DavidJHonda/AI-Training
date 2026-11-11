#!/usr/bin/env python3
"""Approved photographic rebuild. Narration and question/close packets preserved."""
from pathlib import Path
import argparse,hashlib,json,subprocess
import cv2,numpy as np,imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/understand-ai-opener-v19.mp4'
DEST=ROOT/'Prompts/understand-ai-opener-v20.mp4'
OUT=ROOT/'video-audit/understand-opener-v20-2026-11-11'
PHOTOS=ROOT/'previews/understand-ai-opener-visual-direction-2026-11-11'
FF=imageio_ffmpeg.get_ffmpeg_exe();W,H,FPS=1280,720,30
TOTAL=2307;TAIL_START=1658


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ease(x):return x*x*(3-2*x)
def run(args):subprocess.run([FF,'-hide_banner','-loglevel','warning',*map(str,args)],check=True)

def outline(frame,rect,color,radius=22):
    # Output-space signed distance field gives an actual four-pixel stroke.
    x0,y0,x1,y1=rect;half=2.;x0-=half;y0-=half;x1+=half;y1+=half
    xa=max(0,int(np.floor(x0-5)));xb=min(W,int(np.ceil(x1+6)))
    ya=max(0,int(np.floor(y0-5)));yb=min(H,int(np.ceil(y1+6)))
    yy,xx=np.mgrid[ya:yb,xa:xb].astype(float);xx+=.5;yy+=.5
    rad=min(radius+half,(x1-x0)/2,(y1-y0)/2)
    dx=np.abs(xx-(x0+x1)/2)-((x1-x0)/2-rad)
    dy=np.abs(yy-(y0+y1)/2)-((y1-y0)/2-rad)
    sdf=np.sqrt(np.maximum(dx,0)**2+np.maximum(dy,0)**2)+np.minimum(np.maximum(dx,dy),0)-rad
    alpha=np.clip(half+.5-np.abs(sdf),0,1)[:,:,None]
    col=np.array([int(color[i:i+2],16) for i in [5,3,1]],float)
    region=frame[ya:yb,xa:xb];frame[ya:yb,xa:xb]=(region*(1-alpha)+col*alpha).round().astype(np.uint8)

SCENES=[
 dict(key='contrast',file='frame-01-ai-contrast.png',start=0,end=659,zoom=1.03,focus=[.514,.50],purpose='Same AI: useful explanation and elementary error'),
 dict(key='driving',file='frame-02-driving.png',start=659,end=804,zoom=1.02,focus=[.50,.50],purpose='Use the controls without opening the hood'),
 dict(key='hood',file='frame-03-under-the-hood.png',start=804,end=1239,zoom=1.03,focus=[.514,.514],purpose='Look beneath the hood at the spoken comparison'),
 dict(key='words',file='frame-04-words-to-answer.png',start=1239,end=1658,zoom=1.02,focus=[.510,.50],purpose='The goal: your words become an answer'),
]
MARKS=[
 dict(scene='contrast',start=60,end=165,rect=[864,330,1462,398],color='#0f7a4a',label='Useful explanation at expert contrast'),
 dict(scene='contrast',start=172,end=288,rect=[864,504,1464,573],color='#c41f28',label='Intentionally incorrect decimal reply at six-year-old contrast'),
 dict(scene='words',start=1579,end=1616,rect=[843,285,1464,369],color='#4f2fc4',label='Your words'),
 dict(scene='words',start=1616,end=1658,rect=[840,433,1464,558],color='#0f7a4a',label='An answer'),
]


def render_frame(scene,image,f):
    h,w=image.shape[:2];q=ease((f-scene['start'])/max(1,scene['end']-scene['start']-1))
    z=1+(scene['zoom']-1)*q;vw=min(w,h*16/9)/z;vh=vw*9/16
    cx=w*(.5+(scene['focus'][0]-.5)*q);cy=h*(.5+(scene['focus'][1]-.5)*q)
    cx=np.clip(cx,vw/2,w-vw/2);cy=np.clip(cy,vh/2,h-vh/2)
    x,y=cx-vw/2,cy-vh/2
    mat=np.float32([[vw/W,0,x],[0,vh/H,y]])
    im=cv2.warpAffine(image,mat,(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
    for mark in MARKS:
        if mark['scene']==scene['key'] and mark['start']<=f<mark['end']:
            a,b,c,d=mark['rect'];s=W/vw;rect=[(a-x)*s,(b-y)*s,(c-x)*s,(d-y)*s]
            assert min(rect[0],rect[1],W-rect[2],H-rect[3])>10
            outline(im,rect,mark['color'],radius=22*s)
    return im


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    assert not DEST.exists(),'Use a new version, never overwrite a candidate.'
    assert sha(SRC)=='25854c16711cf75ab98d517a23bcc27a4d36def3f7cc139e6883b65e7ef91692'
    OUT.mkdir(exist_ok=True);(OUT/'states').mkdir(exist_ok=True)
    record=json.loads((PHOTOS/'generation-record.json').read_text())
    for row in record['artifacts']:assert sha(PHOTOS/row['name'])==row['sha256']
    protected=[SRC,*(PHOTOS/s['file'] for s in SCENES),PHOTOS/'generation-record.json',ROOT/'course-assets/understand-ai-opener/understand-ai-opener.mp4',ROOT/'index.html',ROOT/'lessons/Opener-Understand.md',ROOT/'course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg',ROOT/'course-assets/understand-ai-opener/understand-ai-opener-close.jpg']
    hashes={str(p):sha(p) for p in protected};images={s['key']:cv2.imread(str(PHOTOS/s['file'])) for s in SCENES}
    state_frames={0,90,210,420,658,659,732,803,804,1020,1238,1239,1450,1590,1630,1657}
    for f in sorted(state_frames):
        s=next(s for s in SCENES if s['start']<=f<s['end']);cv2.imwrite(str(OUT/'states'/f'f{f:04d}.jpg'),render_frame(s,images[s['key']],f),[cv2.IMWRITE_JPEG_QUALITY,95])
    manifest=dict(
        source=str(SRC),output=str(DEST),scope='Approved visual-only photographic rebuild; review candidate, no installation or publication',
        authorization='User: These look good. Rebuild the opener with this visual direction, keeping the edited narration, question board, and standard close. Prepare a new version for review.',
        fps=FPS,width=W,height=H,total_frames=TOTAL,duration=TOTAL/FPS,
        changed_picture_frames=[0,TAIL_START],scenes=SCENES,marks=MARKS,
        retained_picture_frames=[TAIL_START,TOTAL],retained_question_board=[1658,1989],retained_standard_close=[1989,2307],
        audio='Entire original v19 AAC stream copied; no processing, edits, pauses, or timing changes',
        approved_photo_provenance=str(PHOTOS/'generation-record.json'),protected_hashes=hashes,
        boundaries=[dict(frame=s['start'],label=s['key']) for s in SCENES[1:]]+[dict(frame=1658,label='Retained question board'),dict(frame=1989,label='Retained standard close')],
        motion='Gentle 2–3% photographic push; screen emphasis at narration onsets; no generated person/object animation',
        direct_listening_performed=False,continuous_real_time_motion_review_performed=False,installed=False,
    )
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if args.prepare_only:print('Prepared visual-only edit plan and states',flush=True);return
    head=OUT/'new-photographic-head.mp4';tail=OUT/'retained-board-and-close.mp4'
    assert not head.exists() and not tail.exists(),'Scratch exists; inspect before reusing.'
    p=subprocess.Popen([FF,'-hide_banner','-loglevel','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-video_track_timescale','15360',str(head)],stdin=subprocess.PIPE)
    for f in range(TAIL_START):
        s=next(s for s in SCENES if s['start']<=f<s['end']);p.stdin.write(render_frame(s,images[s['key']],f).tobytes())
        if f%600==0:print('Rendered photographic frame',f,'of',TAIL_START,flush=True)
    p.stdin.close();assert p.wait()==0
    # v19 frame 1658 is an IDR frame at PTS 848896 / 15360. Start 2/3 microseconds
    # before it so no floating timestamp rounding can skip its first packet.
    run(['-ss','55.266666','-i',SRC,'-map','0:v:0','-an','-c:v','copy',tail])
    playlist=OUT/'video-concat.txt';playlist.write_text("file 'new-photographic-head.mp4'\nduration 55.266666666667\nfile 'retained-board-and-close.mp4'\n")
    run(['-f','concat','-safe','0','-i',playlist,'-i',SRC,'-map','0:v:0','-map','1:a:0','-c','copy','-video_track_timescale','15360','-movflags','+faststart',DEST])
    manifest['candidate_sha256']=sha(DEST);manifest['bytes']=DEST.stat().st_size
    manifest['protected_files_unchanged']={str(p):sha(p)==hashes[str(p)] for p in protected}
    assert all(manifest['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Built',DEST,flush=True)

if __name__=='__main__':main()
