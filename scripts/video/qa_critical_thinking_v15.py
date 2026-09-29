#!/usr/bin/env python3
"""Verify encoded v15 timing, copied audio, unedited frames and corrected boundaries."""
import hashlib, json, re, subprocess
from pathlib import Path
import cv2, numpy as np, imageio_ffmpeg
import build_critical_thinking_v15 as b

ff=imageio_ffmpeg.get_ffmpeg_exe()
out=b.OUT/'verification';out.mkdir(exist_ok=True)
assert b.sha(b.SRC)==b.EXPECTED
manifest=json.loads((b.OUT/'edit-manifest.json').read_text())
assert b.sha(b.DEST)==manifest['output_sha256']

def audio_hash(path):
    cmd=[ff,'-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']
    return subprocess.check_output(cmd,text=True).strip()

source_audio=audio_hash(b.SRC);output_audio=audio_hash(b.DEST)
assert source_audio==output_audio,'Encoded audio stream changed.'

boundaries=[{'frame':v,'label':f'{label}-{side}'} for s,e,label in b.SPANS for side,v in [('start',s),('end',e)]]
selected={0,b.N-1,2262,2376,2520,2670,2910,2915,2920,2940,3030,3050,3060,3270,3390}
for row in boundaries:selected.update(range(row['frame']-2,row['frame']+3))

source=cv2.VideoCapture(str(b.SRC));video=cv2.VideoCapture(str(b.DEST))
assert source.get(cv2.CAP_PROP_FPS)==video.get(cv2.CAP_PROP_FPS)==b.FPS
rows=[];outside=[];heading_outside=[];motion=[];cells=[];idx=0;prev=None
while True:
    oks,s=source.read();okf,f=video.read()
    assert oks==okf,f'Decoded lengths differ at {idx}'
    if not oks:break
    small=cv2.resize(f,(320,180)).astype(np.float32)
    original=cv2.resize(s,(320,180)).astype(np.float32)
    changed=any(start<=idx<end for start,end,_ in b.SPANS)
    mad=float(abs(small-original).mean())
    if not changed:outside.append(mad)
    if b.HEADING[0]<=idx<b.HEADING[1]:
        delta=cv2.absdiff(f,s);delta[175:225,580:960]=0
        heading_outside.append(float(delta.mean()))
    if b.PAPER[0]<idx<b.PAPER[1] and prev is not None:motion.append(float(abs(small-prev).mean()))
    if idx in selected:
        cv2.imwrite(str(out/f'frame-{idx:05d}.jpg'),f,[cv2.IMWRITE_JPEG_QUALITY,96])
    if changed and idx%30==0:
        cell=cv2.resize(f,(480,270));cv2.putText(cell,f'{idx} / {idx/b.FPS:.2f}s',(10,24),0,.6,(0,0,210),2)
        cells.append(cell)
    prev=small;idx+=1
source.release();video.release()
assert idx==b.N,(idx,b.N)
assert max(outside)<5, max(outside)
assert max(heading_outside)<3,max(heading_outside)
for i in range(0,len(cells),9):
    batch=cells[i:i+9]
    while len(batch)<9:batch.append(np.zeros((270,480,3),np.uint8))
    cv2.imwrite(str(out/f'repaired-sequence-{i//9}.jpg'),cv2.vconcat([cv2.hconcat(batch[j:j+3]) for j in range(0,9,3)]))

# Independently decode through ffmpeg and verify every presentation timestamp.
r=subprocess.run([ff,'-hide_banner','-i',str(b.DEST),'-map','0:v:0','-vf','showinfo','-an','-f','null','-'],capture_output=True,text=True)
assert r.returncode==0
(out/'ffmpeg-decode.log').write_text(r.stderr)
pts=[int(x) for x in re.findall(r'\bn:\s*\d+\s+pts:\s*(-?\d+)',r.stderr)]
assert len(pts)==b.N,len(pts)
deltas=np.diff(pts);assert pts[0]==0 and np.all(deltas==512),set(deltas)

cmd=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(out/'transitions')]
for row in boundaries:cmd.extend(['--boundary',f"{row['frame']}:{row['label']}"])
guard=subprocess.run(cmd,capture_output=True,text=True)
(out/'transition-command.log').write_text(guard.stdout+guard.stderr)
assert guard.returncode==0,guard.stdout+guard.stderr
report={'output':str(b.DEST),'sha256':b.sha(b.DEST),'decoded_frames':idx,'fps':b.FPS,'video_duration_seconds':idx/b.FPS,
        'timestamp_ticks_per_frame':512,'video_timescale':15360,'audio_source_hash':source_audio,'audio_output_hash':output_audio,
        'audio_bit_identical':True,'unchanged_spans_thumbnail_MAD_mean':float(np.mean(outside)),
        'unchanged_spans_thumbnail_MAD_max':max(outside),'heading_outside_patch_full_frame_MAD_max':max(heading_outside),
        'paper_motion_frame_differences':{'mean':float(np.mean(motion)),'max':max(motion),'min':min(motion)},
        'transition_guard_exit_code':guard.returncode,'boundaries':boundaries,
        'live_source_unchanged':b.sha(b.LIVE)==b.EXPECTED,'listening':'Not directly auditioned; original compressed audio stream copied exactly.',
        'visual_review':'Encoded frame sheets and every-frame boundary strips require manual inspection.'}
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
