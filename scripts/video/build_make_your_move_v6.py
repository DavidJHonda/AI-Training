#!/usr/bin/env python3
"""Approved Make Your Move pacing/wording build; review candidate only.

Keeps unchanged source pictures in planar YUV, rebuilding only the two career
boards and four supporting scenes. Uses a retained, hash-locked finished source.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

import av
import cv2
import imageio_ffmpeg
import numpy as np

from ken_burns_path import draw_ring, hex_bgr, ring_px

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT/'video-audit/make-your-move-note-cut/make-your-move-without-note.mp4'
EXPECTED = 'd2aeeba98a33c91657fe75368d46502671af1c47a35e51f2e32cd5b663951d60'
OUT = ROOT/'video-audit/make-your-move-build-2026-09-30-v6'
DEST = ROOT/'Prompts/make-your-move-v6.mp4'
ART = ROOT/'scripts/video/assets/make-your-move-cutaways-2026-09-30'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, SR, SPF, TOTAL = 30, 48000, 1600, 9045
CUT = (854, 1074)
GAIN_DB = -1.3
COLORS = ['#4f2fc4', '#1652f0', '#0e8f86']
BOARDS = [
    dict(key='careers-a', asset='make-your-move-doctors-teachers-lawyers.jpg',
         span=[1495, 3188], names=['Doctor', 'Teacher', 'Lawyer'],
         onsets=[[52.82,54.60,61.76],[72.72,75.03,79.30],[90.40,93.50,97.62]]),
    dict(key='careers-b', asset='make-your-move-electricians-designers-entrepreneurs.jpg',
         span=[3312,4726], names=['Electrician','Graphic Designer','Entrepreneur'],
         onsets=[[110.433333,112.14,116.60],[125.12,126.52,132.00],[140.78,142.50,147.22]]),
]
PHOTOS = [
    dict(key='patient-care', span=[1953,2136], purpose='Examining the patient and explaining choices'),
    dict(key='teacher-judgment', span=[2514,2688], purpose='Knowing students, motivation, adaptation and classroom community'),
    dict(key='electrical-diagnosis', span=[3615,3726], purpose='Diagnosing the actual physical environment and adapting on site'),
    dict(key='design-judgment', span=[4065,4200], purpose='Choosing purpose, audience, taste and final direction'),
]

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def mapped(n):
    return n-max(0,min(n,CUT[1])-CUT[0])

def yuv(im):
    return av.VideoFrame.from_ndarray(im,format='bgr24').to_ndarray(format='yuv420p')

def board_states(cfg):
    path=ROOT/'course-assets/make-your-move'/cfg['asset']
    im=cv2.imread(str(path));h,w=im.shape[:2]
    # Full current board plus 4% top/bottom stage. Exact asset aspect is preserved.
    scale=720/(h*1.08);nw,nh=round(w*scale),round(h*scale)
    ox,oy=(1280-nw)//2,(720-nh)//2
    frame=np.full((720,1280,3),im[4,4],dtype=np.uint8)
    frame[oy:oy+nh,ox:ox+nw]=cv2.resize(im,(nw,nh),interpolation=cv2.INTER_AREA)
    result={};states=[dict(at=cfg['span'][0],label='unmarked',rect=None,color=None)]
    boxes=[[40,126,525,940],[562,126,1044,940],[1080,126,1561,940]]
    for i,(name,onsets) in enumerate(zip(cfg['names'],cfg['onsets'])):
        x0,y0,x1,y1=boxes[i]
        sections=[('whole card',[x0,y0,x1,y1]),
                  ('AI may help',[x0+24,490,x1-24,681]),
                  ('People still own',[x0+24,699,x1-24,923])]
        for at,(part,rect) in zip(onsets,sections):
            states.append(dict(at=round(at*FPS),label=name+' — '+part,rect=rect,color=COLORS[i]))
    cfg.update(asset_sha256=sha(path),density='compact',camera='fixed full board',
               source_size=[w,h],placement=[ox,oy,nw,nh],states=states)
    for state in states:
        f=frame.copy()
        if state['rect']:
            x0,y0,x1,y1=state['rect'];t=ring_px(720);half=t/2
            draw_ring(f,ox+x0*scale-half,oy+y0*scale-half,
                      ox+x1*scale+half,oy+y1*scale+half,
                      hex_bgr(state['color']),12*scale+half,t)
        result[state['at']]=yuv(f)
        cv2.imwrite(str(OUT/'states'/f"{cfg['key']}-{state['at']:06d}.png"),f)
    return result

def photo_frame(im,n,total):
    q=n/max(1,total-1);z=1+.025*q*q*(3-2*q)
    h,w=im.shape[:2];cw=min(w,h*16/9)/z;ch=cw*9/16
    matrix=np.float32([[cw/1280,0,(w-cw)/2],[0,ch/720,(h-ch)/2]])
    return cv2.warpAffine(im,matrix,(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)

def audio():
    raw=subprocess.check_output([FF,'-v','error','-i',str(SRC),'-map','0:a:0',
                                 '-ar',str(SR),'-ac','1','-f','f32le','-'])
    pcm=np.frombuffer(raw,np.float32).copy()[:TOTAL*SPF]
    # Same-length same-speaker clause replacement, both boundaries in room tone.
    a,b=round(79.1*SR),round(82.2*SR)
    replacement=pcm[round(61.6*SR):round(64.7*SR)].copy()
    assert len(replacement)==b-a
    fade=round(.008*SR);ramp=np.linspace(0,1,fade)
    replacement[:fade]=pcm[a:a+fade]*(1-ramp)+replacement[:fade]*ramp
    replacement[-fade:]=replacement[-fade:]*(1-ramp)+pcm[b-fade:b]*ramp
    pcm[a:b]=replacement
    pcm=np.concatenate([pcm[:CUT[0]*SPF],pcm[CUT[1]*SPF:]])
    # The cut endpoints are quiet; blend only the last/first 5 ms to their shared floor.
    join=CUT[0]*SPF;fade=240;bed=float(np.mean(pcm[join-48:join+48]))
    ramp=np.linspace(0,1,fade)
    pcm[join-fade:join]=pcm[join-fade:join]*(1-ramp)+bed*ramp
    pcm[join:join+fade]=bed*(1-ramp)+pcm[join:join+fade]*ramp
    pcm*=10**(GAIN_DB/20)
    assert len(pcm)==(TOTAL-(CUT[1]-CUT[0]))*SPF
    p=OUT/'edited-audio.f32';pcm.astype(np.float32).tofile(p)
    return p

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    cv2.setNumThreads(2)
    for d in [OUT,OUT/'states',OUT/'preview']:d.mkdir(parents=True,exist_ok=True)
    assert sha(SRC)==EXPECTED
    protected_paths=[SRC,ROOT/'course-assets/make-your-move/make-your-move.mp4',ROOT/'lessons/make-your-move.md',
                     *sorted((ROOT/'course-assets/make-your-move').glob('*.jpg'))]
    protected={str(p):sha(p) for p in protected_paths}
    states={cfg['key']:board_states(cfg) for cfg in BOARDS}
    if args.prepare_only:
        (OUT/'board-plan.json').write_text(json.dumps(BOARDS,indent=2));return
    assert not DEST.exists(),'Never overwrite a review candidate'
    photos={p['key']:cv2.imread(str(ART/(p['key']+'.png'))) for p in PHOTOS}
    assert all(x is not None for x in photos.values())
    for p in PHOTOS:
        p.update(asset=str(ART/(p['key']+'.png')),sha256=sha(ART/(p['key']+'.png')),
                 output_span=[mapped(n) for n in p['span']])
    audiofile=audio()
    boundaries={CUT[0]:'opening-trim',mapped(round(79.1*FPS)):'teacher-clause-in',mapped(round(82.2*FPS)):'teacher-clause-out'}
    for cfg in BOARDS:
        boundaries.update({mapped(cfg['span'][0]):cfg['key']+'-in',mapped(cfg['span'][1]):cfg['key']+'-out'})
        for s in cfg['states'][1:]:boundaries.setdefault(mapped(s['at']),s['label'])
    for p in PHOTOS:
        boundaries[mapped(p['span'][0])]=p['key']+'-in';boundaries[mapped(p['span'][1])]=p['key']+'-out'
    wants={i for b in boundaries for i in [b-1,b,b+15]}|{TOTAL-(CUT[1]-CUT[0])-1}
    proc=subprocess.Popen([FF,'-v','error','-n','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30',
        '-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1','-i',str(audiofile),'-map','0:v:0','-map','1:a:0',
        '-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','16','-preset','fast','-threads','2',
        '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    written=0;freeze=None
    with av.open(str(SRC)) as c:
        c.streams.video[0].codec_context.thread_count=2
        for n,f in enumerate(c.decode(video=0)):
            if CUT[0]<=n<CUT[1]:continue
            picture=f.to_ndarray(format='yuv420p')
            if n==750:freeze=picture.copy()
            if 751<=n<CUT[0]:picture=freeze
            cfg=next((b for b in BOARDS if b['span'][0]<=n<b['span'][1]),None)
            if cfg:
                key=max(k for k in states[cfg['key']] if k<=n);picture=states[cfg['key']][key]
            photo=next((p for p in PHOTOS if p['span'][0]<=n<p['span'][1]),None)
            if photo:
                a,b=photo['span'];picture=yuv(photo_frame(photos[photo['key']],n-a,b-a))
            if written in wants:
                im=av.VideoFrame.from_ndarray(picture,format='yuv420p').to_ndarray(format='bgr24')
                cv2.imwrite(str(OUT/'preview'/f'{written:06d}.jpg'),im)
            proc.stdin.write(picture.tobytes());written+=1
            if written%1500==0:print(f'Rendered {written}/{TOTAL-(CUT[1]-CUT[0])}',flush=True)
    proc.stdin.close();assert proc.wait()==0
    assert written==TOTAL-(CUT[1]-CUT[0])
    assert all(sha(p)==h for p,h in protected.items())
    manifest=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),candidate_sha256=sha(DEST),
        fps=FPS,total_frames=written,duration=written/FPS,scope='Approved evaluation plan; new review candidate, not shipped',
        source_limitation='Original raw generation is unavailable; one visual encode from retained finished file. Unchanged pictures stay planar YUV.',
        cut=dict(source_frames=CUT,source_seconds=[n/FPS for n in CUT],output_frame=CUT[0],removed_seconds=(CUT[1]-CUT[0])/FPS),
        opening_picture_hold=dict(source_frame=750,span=[751,CUT[0]],reason='Remove intertitle while retaining complete preceding sentence'),
        graft=dict(source_seconds=[61.6,64.7],target_source_seconds=[79.1,82.2],
                   output_seconds=[79.1-(CUT[1]-CUT[0])/FPS,82.2-(CUT[1]-CUT[0])/FPS],
                   removed='Yet the human tasks remain untouched',replacement='But humans still own the core responsibilities',fade_ms=8),
        gain_db=GAIN_DB,boards=BOARDS,cutaways=PHOTOS,
        boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],
        protected_hashes=protected,protected_files_unchanged=True,listening='Not auditioned; requires listening review')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST)]
    for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
    subprocess.run(cmd+['--outdir',str(OUT/'transitions')],check=True)
    print('COMPLETE',DEST,flush=True)

if __name__=='__main__':main()
