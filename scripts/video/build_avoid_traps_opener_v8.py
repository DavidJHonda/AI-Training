#!/usr/bin/env python3
"""Approved visual-only v7 refresh: roadmap interleaves and tracked panel label.

Uses the hash-verified finished v7 because the original raw rolls are unavailable.
Copies its audio stream verbatim. No narration, timing, or pause changes.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from editspec_build import Build
from ken_burns_path import ring_px

cv2.setNumThreads(2)
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'course-assets/avoid-traps-opener/avoid-traps-opener.mp4'
MAP = SRC.parent / 'avoid-traps-opener-section-map.jpg'
OUT = ROOT / 'video-audit/avoid-traps-opener-build-2026-09-29-v8'
DEST = ROOT / 'Prompts/avoid-traps-opener-v8.mp4'
EXPECTED = '00b231583030d5f83dcd730907ac2d2e148febb26acc0f46fbe5a2fcbb7ca239'
FPS, N = 30, 6458
LABEL_IN, LABEL_OUT = 2777, 3019
MAP_IN, MAP_OUT = 3730, 5666
# Half-open output and source ranges, all on the verified v7 timeline.
CUTAWAYS = [
    dict(start=4080, end=4260, source_start=1106, source_end=1286,
         label='Plausible false fact: preserve semantic-failure reveal and final state'),
    dict(start=4860, end=5070, source_start=1287, source_end=1497,
         label='Relaxed computer user: human vulnerability to agreeable responses'),
]
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
PROTECTED = [SRC, *sorted(SRC.parent.glob('*.jpg')), ROOT/'lessons/opener-avoid.md']

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def ring_state(frame):
    # Return from a cutaway unmarked; resume the already-introduced first row
    # after two seconds. Third-category name arrives 1.5 s after return #2.
    if 4260 <= frame < 4320 or 5070 <= frame < 5115:
        return None
    if frame < 3832:
        return None
    return 0 if frame < 4494 else 1 if frame < 5115 else 2

def board_states():
    b = Build(ROOT, SRC, OUT, DEST)
    p,cw,ch,ox,oy = b.compose(MAP, 'roadmap')
    assert (cw,ch,ox,oy) == (1600,900,0,14)
    canonical = Image.open(p).convert('RGB').resize((1280,720), Image.Resampling.LANCZOS)
    states = {None: cv2.cvtColor(np.asarray(canonical),cv2.COLOR_RGB2BGR)}
    # Draw after scaling; supersampling avoids OpenCV's odd/even stroke expansion.
    rows = [(100,148,1520,305),(100,340,1520,497),(100,532,1520,690)]
    colors = ['#4f2fc4','#1652f0','#0e8f86']
    for k,(x0,y0,x1,y1) in enumerate(rows):
        overlay = Image.new('RGBA',(3840,2160),(0,0,0,0));d=ImageDraw.Draw(overlay)
        rect=[round(v*3) for v in (x0*.8-ring_px(),(y0+oy)*.8-ring_px(),x1*.8+ring_px(),(y1+oy)*.8+ring_px())]
        d.rounded_rectangle(rect,radius=round(18*.8*3),outline=colors[k],width=ring_px()*3)
        im=Image.alpha_composite(canonical.convert('RGBA'),overlay.resize((1280,720),Image.Resampling.LANCZOS)).convert('RGB')
        states[k]=cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)
        im.save(OUT/f'map-state-{k}.png')
    canonical.save(OUT/'map-unmarked.png')
    return states

def label_overlay():
    im=Image.new('RGBA',(3840,2160),(0,0,0,0));d=ImageDraw.Draw(im)
    font=ImageFont.truetype(FONT,42*3)
    d.multiline_text((637*3,355*3),'Looks helpful.\nHides the risk.',font=font,
                     anchor='mm',align='center',spacing=9*3,fill='#1b2153')
    return np.asarray(im.resize((1280,720),Image.Resampling.LANCZOS))

def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    assert sha(SRC)==EXPECTED, 'Source changed; review new source before building.'
    wanted=set(range(1106,1286))|set(range(1287,1497))|set(range(LABEL_IN,LABEL_OUT))
    cap=cv2.VideoCapture(str(SRC));cache={};i=0
    while i<LABEL_OUT:
        ok,frame=cap.read();assert ok,i
        if i in wanted:cache[i]=frame
        i+=1
    cap.release()
    ref=cache[LABEL_IN]
    orb=cv2.ORB_create(nfeatures=2500)
    kp0,de0=orb.detectAndCompute(cv2.cvtColor(ref,cv2.COLOR_BGR2GRAY),None)
    matcher=cv2.BFMatcher(cv2.NORM_HAMMING)
    overlay=label_overlay(); label_frames={};tracks=[]
    for i in range(LABEL_IN,LABEL_OUT):
        frame=cache[i]
        kp,de=orb.detectAndCompute(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),None)
        matches=[m for m,n in matcher.knnMatch(de0,de,k=2) if m.distance<.72*n.distance]
        a=np.float32([kp0[m.queryIdx].pt for m in matches]);b=np.float32([kp[m.trainIdx].pt for m in matches])
        mat,inliers=cv2.estimateAffinePartial2D(a,b,method=cv2.RANSAC,ransacReprojThreshold=1.5)
        assert mat is not None and int(inliers.sum())>100,(i,len(matches))
        scale=float(np.linalg.norm(mat[:,0]));assert .95<scale<1.05,(i,scale)
        layer=cv2.warpAffine(overlay,mat,(1280,720),flags=cv2.INTER_LINEAR)
        alpha=layer[:,:,3:4].astype(np.float32)/255
        color=layer[:,:,:3][:,:,::-1]
        result=np.clip(frame*(1-alpha)+color*alpha,0,255).astype(np.uint8)
        label_frames[i]=result
        tracks.append(dict(frame=i,affine=mat.tolist(),inliers=int(inliers.sum()),scale=scale))
    (OUT/'label-tracking.json').write_text(json.dumps(tracks,indent=2))
    boards=board_states()
    for i in (2777,2820,2880,2940,3018):cv2.imwrite(str(OUT/f'label-preview-{i}.png'),label_frames[i])
    manifest=dict(candidate=str(DEST),source=str(SRC),source_sha256=EXPECTED,fps=FPS,
                  total_frames=N,duration=N/FPS,scope='Approved visual-only repair; review candidate, not installed or published',
                  authorization='User: I agree, even with the smaller issue. Let\'s build it with the improvements.',
                  source_limitation='Raw rolls no longer present. One video encode from verified v7; source AAC copied unchanged.',
                  cutaways=CUTAWAYS,label=dict(start=LABEL_IN,end=LABEL_OUT,text='Looks helpful. Hides the risk.',tracking='affine camera tracking; original scene retained'),
                  board=dict(asset=str(MAP),density='compact',camera='full view, still',ring_width=ring_px(),
                             row_onsets=[3832,4494,5115],unmarked_returns=[[4260,4320],[5070,5115]],
                             visible_spans=[[3730,4080],[4260,4860],[5070,5666],[5894,5982]],
                             note='Main roadmap rebuilt; existing short banner return is preserved outside scope.'),
                  audio='Stream copied from v7; no edits, pauses, or re-encoding',
                  longest_unbroken_board_seconds=20.0,
                  changed_spans=[[LABEL_IN,LABEL_OUT],[MAP_IN,MAP_OUT]],
                  boundaries=[393,2212,2777,3019,3730,3830,4080,4260,4860,5070,5666,5894,5982,6160],
                  protected={str(p):sha(p) for p in PROTECTED})
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return cache,label_frames,boards,manifest

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    cache,labels,boards,m=prepare()
    if args.prepare_only:
        print('Previews and exact plan:',OUT,flush=True);return
    assert not DEST.exists(),'Never overwrite a candidate; select a new version.'
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    cmd=[ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
         '-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','medium','-crf','17',
         '-threads','2','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
    with (OUT/'encode.log').open('w') as log:
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        cap=cv2.VideoCapture(str(SRC));i=0
        try:
            while True:
                ok,frame=cap.read()
                if not ok:break
                if i in labels:frame=labels[i]
                elif MAP_IN<=i<MAP_OUT:
                    cut=next((c for c in CUTAWAYS if c['start']<=i<c['end']),None)
                    frame=cache[cut['source_start']+i-cut['start']] if cut else boards[ring_state(i)]
                proc.stdin.write(frame.tobytes());i+=1
                if i%900==0:print(f'Rendered {i}/{N} frames',flush=True)
        finally:
            cap.release();proc.stdin.close()
        assert proc.wait()==0,(OUT/'encode.log').read_text()
    assert i==N,i
    assert all(sha(p)==h for p,h in m['protected'].items()),'Protected source changed during build.'
    m['candidate_sha256']=sha(DEST);m['protected_unchanged']=True
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print('Candidate:',DEST,flush=True)

if __name__=='__main__':main()
