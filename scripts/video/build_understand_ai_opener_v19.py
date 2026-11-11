#!/usr/bin/env python3
"""Approved November 11 Understand roll 3 edit. Review candidate only."""
from pathlib import Path
import argparse,json,subprocess
import cv2,numpy as np
from editspec_build import Build,Reader,fr,sha,SPF,FPS,W,H,CLOSE_PREHOLD,CLOSE_PUSH,CLOSE_TAIL

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/Understand-opener-3.mp4'
DEST=ROOT/'Prompts/understand-ai-opener-v19.mp4'
OUT=ROOT/'video-audit/understand-opener-v19-2026-11-11'
ASSETS=ROOT/'course-assets/understand-ai-opener'
HOOD=ASSETS/'understand-ai-opener-under-hood.jpg'
MAP=ASSETS/'understand-ai-opener-section-map.jpg'
CLOSE=ASSETS/'understand-ai-opener-close.jpg'
LIVE=ASSETS/'understand-ai-opener.mp4'


def split_visual(b,point):
    rows=[]
    for row in b.rows:
        if row['kind']!='source' or not row['source_start']<point<row['source_end']:
            rows.append(row);continue
        delta=point-row['source_start'];cut=row['start_frame']+delta
        left=dict(row,source_end=point,end_frame=cut)
        right=dict(row,source_start=point,start_frame=cut)
        if 'video_start' in right:right['video_start']+=delta
        rows.extend([left,right])
    b.rows=rows


def cover(b,s,e,visual,video_from=None,video_end=None,video_src=None):
    split_visual(b,s);split_visual(b,e)
    for row in b.rows:
        if row['kind']=='source' and s<=row['source_start']<e:
            row['visual']=visual
            if video_from is not None:
                row['video_start']=video_from+row['source_start']-s
                if video_end is not None: row['video_end']=video_end
                if video_src is not None:row['video_src']=str(video_src)


def reassurance_leg(b):
    """Retime the removed illustrated presentation scene, picture only, lossless.

    Slow its existing camera/reveal motion across the reassurance passage. No
    retained narration is slowed and no voice from this discarded beat is used.
    """
    path=OUT/'reassurance-picture.mkv'
    if path.exists():return path
    n=1895-1476
    start,end=2250,2439
    c=cv2.VideoCapture(str(SRC));ims=[];i=0
    while i<end:
        ok,im=c.read();assert ok
        if i>=start:ims.append(im)
        i+=1
    c.release()
    p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-an','-c:v','ffv1','-level','3',str(path)],stdin=subprocess.PIPE)
    for k in range(n):
        j=round(k*(len(ims)-1)/max(1,n-1));p.stdin.write(ims[j].tobytes())
    p.stdin.close();assert p.wait()==0
    return path


def exact_compact_legs(b):
    # Rasterize the fixed on-screen stroke from a rounded-rectangle distance
    # field. OpenCV integer-thickness lines can cover five solid pixels at t=4.
    # This build-local fix changes no common renderer or unrelated lesson.
    for key,board in b.boards.items():
        spec=json.loads((OUT/f'leg-{key}.json').read_text())
        im=cv2.imread(spec['image']);base=cv2.resize(im,(W,H),interpolation=cv2.INTER_AREA)
        ih,iw=im.shape[:2];scale=W/iw;yy,xx=np.mgrid[0:H,0:W].astype(float);xx+=.5;yy+=.5
        states={():base};n=board['src_out']-board['src_in']
        p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-an','-c:v','ffv1','-level','3',str(OUT/f'leg-{key}.mkv')],stdin=subprocess.PIPE)
        for f in range(n):
            active=tuple(j for j,r in enumerate(spec['rings']) if r['start']<=f<r['end'])
            if active not in states:
                frame=base.astype(float).copy()
                for j in active:
                    r=spec['rings'][j];x,y,w,h=r['rect'];pad=r.get('pad',0);half=2.
                    x0=(x-pad)*scale-half;y0=(y-pad)*scale-half
                    x1=(x+w+pad)*scale+half;y1=(y+h+pad)*scale+half
                    rad=min(r.get('radius',0)*scale+half,(x1-x0)/2,(y1-y0)/2)
                    dx=np.abs(xx-(x0+x1)/2)-((x1-x0)/2-rad)
                    dy=np.abs(yy-(y0+y1)/2)-((y1-y0)/2-rad)
                    sdf=np.sqrt(np.maximum(dx,0)**2+np.maximum(dy,0)**2)+np.minimum(np.maximum(dx,dy),0)-rad
                    alpha=np.clip(half+.5-np.abs(sdf),0,1)[:,:,None]
                    color=r['color'].lstrip('#');bgr=np.array([int(color[i:i+2],16) for i in [4,2,0]],float)
                    frame=frame*(1-alpha)+bgr*alpha
                states[active]=frame.round().astype(np.uint8)
            p.stdin.write(states[active].tobytes())
        p.stdin.close();assert p.wait()==0


def efficient_render(b):
    # Avoid constructing an unused VideoCapture on every setdefault call in the
    # common renderer. Keep the native and retimed readers independent.
    import editspec_build as machinery
    original=machinery.Reader;cache={};native_created=False
    def reader(path):
        nonlocal native_created
        key=str(path)
        if key==str(SRC) and not native_created:
            native_created=True;return original(path)
        if key not in cache:cache[key]=original(path)
        return cache[key]
    machinery.Reader=reader
    try:b.render()
    finally:machinery.Reader=original


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    assert not DEST.exists(),'Never overwrite a review candidate.'
    assert sha(SRC)=='78f3d1ac3e057f2e2e6ae975ba7cb992c4d2db9f0aad92e44750a8d5827a5068'
    b=Build(ROOT,SRC,OUT,DEST,protected=[HOOD,MAP,CLOSE,LIVE,ROOT/'index.html',ROOT/'lessons/Opener-Understand.md'])
    b.load_audio([(40.99,41.29),(73.97,74.19),(83.61,83.91)])
    # Both cuts occur within measured quiet runs, independently of picture cuts.
    keeps=[(0,1239,'Opening, car analogy, under the hood and Be Smarter benefit'),
           (1476,2226,'Accepted paraphrase, reassurance, goal and three exact questions')]
    for s,e,label in keeps:b.keep(s,e,label)
    b.mark_close_start();b.keep(2436,2559,'Both exact closing lines','close')
    b.pause(max(CLOSE_TAIL,CLOSE_PREHOLD+CLOSE_PUSH+CLOSE_TAIL-(b.cursor-b.close_start)),'Standard closing settled hold')
    b.finish_audio()

    # Only picture rows are split here, AFTER assembly, to avoid word-level fades.
    # f512 begins the unwanted technical scene. Reuse the settled expert/error drawing.
    cover(b,512,659,'source',video_from=285,video_end=286)
    # The AI mechanism diagram starts dissolving at f998, just before "The same goes for AI".
    cover(b,998,1239,'hood')
    # The diagram beneath reassurance is replaced by the existing learning scene.
    # Prepare-only records the planned path; the lossless picture leg is made on build.
    leg=OUT/'reassurance-picture.mkv'
    cover(b,1476,1895,'source',video_from=0,video_end=419,video_src=leg)
    cover(b,1895,2226,'map')
    b.board('hood',HOOD,998,1239,'compact',[],banner_at=37.88,push=False)
    b.tall_margin=False
    b.board('map',MAP,1895,2226,'compact',[
        dict(label='Where does AI get all that knowledge?',at=66.72,rects=[[128,229,1473,389]],color='#4f2fc4'),
        dict(label='How does AI seem to understand what I ask?',at=68.86,rects=[[128,409,1473,569]],color='#1652f0'),
        dict(label='How does AI come up with its answers?',at=72.02,rects=[[128,589,1473,749]],color='#0e8f86'),
    ],push=False)
    b.make_close('openerfoundations')
    m=b.manifest(dict(
        authorization='User: Go ahead with version 3. Make the proposed cuts and prepare an edited version for review. The paraphrased sentence is fine.',
        accepted_paraphrase='We are going to take you inside the machine, one piece at a time.',
        narration_source='November 11 roll 3 only; zero audio grafts',
        source_audio_keep_frames=[[0,1239],[1476,2226],[2436,2559]],
        removed_source_audio_frames=[[1239,1476],[2226,2436],[2559,2653]],
        instructional_pauses_added=0,
        picture_retime=dict(source=str(SRC),source_frames=[2250,2439],output_frames=419,purpose='Existing illustrated learning scene beneath reassurance; no mechanism diagram',path=str(leg)),
        source_picture_retained=[[0,512],[659,998]],
        source_picture_frozen=dict(source_frame=285,under_source_audio=[512,659],purpose='Expert/error illustration replaces premature technical diagram'),
        measured_quiet_runs_seconds=[[40.92,41.59],[48.83,49.51],[73.87,74.54],[80.83,81.45],[85.01,88.49]],
        planned_retained_join_gaps_seconds=[.60,.57],
        direct_listening_performed=False,continuous_motion_review_performed=False,installed=False,ring_rasterizer='Build-local rounded-rectangle signed-distance alpha mask; exact four-pixel output stroke',
    ))
    print(f'Prepared {b.total} frames ({b.total/30:.3f}s); close at {b.close_start/30:.3f}s',flush=True)
    if args.prepare_only:return
    reassurance_leg(b)
    exact_compact_legs(b)
    efficient_render(b)
    for key in b.boards:b.state_sheet(key)
    print(f'Completed {DEST}',flush=True)

if __name__=='__main__':main()
