#!/usr/bin/env python3
"""Approved three-row repair of v10. Review only; retain unaffected encoded media."""
import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
import wave

import av
import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build
from build_embeddings_v7 import Renderer

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/does-ai-think-three-rows-2026-10-23-v11'
SRC = ROOT / 'Prompts/does-ai-think-v10.mp4'
DST = ROOT / 'Prompts/does-ai-think-v11.mp4'
LIVE = ROOT / 'course-assets/does-ai-think/does-ai-think.mp4'
ASSET = LIVE.parent / 'does-ai-think-side-by-side.jpg'
EXPECTED = '098b77a5b70fbc9ba6bce99e6b2b2f345343792a34688c1a2d6245a29df3771f'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, RATE, SPF, SOURCE_FRAMES = 30, 48000, 1600, 6486
# All boundaries measured inside quiet gaps, not inferred from scene cuts/ASR alone.
CUTS = [(3825,4116),(4311,4370),(4581,4640),(4865,5176)]
REMOVED = sum(b-a for a,b in CUTS)
TOTAL = SOURCE_FRAMES - REMOVED
KEEP = [(0,CUTS[0][0]), *[(CUTS[i][1],CUTS[i+1][0]) for i in range(len(CUTS)-1)], (CUTS[-1][1],SOURCE_FRAMES)]
MAPPING = [n for a,b in KEEP for n in range(a,b)]
INVERSE = {n:i for i,n in enumerate(MAPPING)}
# Source keyframe-bounded intervals. The three supporting cutaways remain packet copies.
ENCODE = [(3555,4215),(4290,4761),(4845,5340),(5445,5803)]
BOARD = (3750,5697)
CUTAWAYS = [(4215,4290),(4761,4845),(5340,5445)]
# AAC replacement edges are in silence, and exactly on AAC packet boundaries.
AUDIO_START = 5967 * 1024  # 127.296 seconds, before first removal
AUDIO_END = 8095 * 1024    # 172.693333 seconds, after last removal, before 'Finally'
assert REMOVED == 720 and REMOVED*SPF % 1024 == 0

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inside(n,spans): return any(a<=n<b for a,b in spans)
def mapped(n): return INVERSE[n]
def is_board(n): return BOARD[0]<=n<BOARD[1] and not inside(n,CUTAWAYS)

def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    p,cw,ch,ox,oy = Build.compose(SimpleNamespace(out=OUT),ASSET,'compare')
    full = [cw/2,ch/2,float(cw)]
    start,end = mapped(BOARD[0]),mapped(BOARD[1])
    # Complete comparison rows, both columns; source JPG coordinates, measured anew.
    rects = [[60,672,1480,160],[60,860,1480,113],[60,1003,1480,125]]
    onsets = [mapped(4123),mapped(4646),mapped(5185)]
    pull, banner = mapped(5537),mapped(5567)
    camera_width = 1720.0
    def cam(rect):
        x,y,w,h=rect
        return [ox+x+w/2, min(ch-camera_width*9/32,max(camera_width*9/32,oy+y+h/2)),camera_width]
    beats = [dict(label='full-unmarked-opening',frames=onsets[0]-start,**{'from':full},to=full)]
    for i,rect in enumerate(rects):
        stop = onsets[i+1] if i<2 else pull
        beats += [dict(label='move-to-row-'+str(i+1),frames=30,to=cam(rect)),
                  dict(label='hold-row-'+str(i+1),frames=stop-onsets[i]-30,to=cam(rect))]
    beats += [dict(label='pullback-for-takeaway',frames=30,to=full),dict(label='takeaway',frames=end-pull-30,to=full)]
    rings=[]
    for i,(rect,onset) in enumerate(zip(rects,onsets)):
        x,y,w,h=rect
        rings.append(dict(start=onset-start,end=(onsets[i+1] if i<2 else banner)-start,
                          rect=[x+ox,y+oy,w,h],color='#0f7a4a',pad=0,radius=18))
    rings.append(dict(start=banner-start,end=end-start,rect=[40+ox,1185+oy,1520,88],color='#6e51ff',pad=0,radius=18))
    spec=dict(image=str(p),fps=30,out_w=1280,out_h=720,upscale=3,beats=beats,rings=rings)
    assert sum(b['frames'] for b in beats)==end-start
    (OUT/'leg-compare.json').write_text(json.dumps(spec,indent=2)+'\n')
    boundaries={mapped(a):'replacement-start' for a,b in ENCODE}
    boundaries.update({mapped(b):'source-resumes' for a,b in ENCODE})
    boundaries.update({mapped(BOARD[0]):'three-row-board-in',mapped(BOARD[1]):'three-row-board-out'})
    boundaries.update({mapped(b):'audio-cut-'+str(i+1) for i,(a,b) in enumerate(CUTS)})
    boundaries.update({n:label for n,label in zip(onsets,['experience-and-meaning','word-choice','uncertainty'])})
    boundaries[pull]='takeaway-pullback';boundaries[banner]='takeaway-highlight'
    for a,b in CUTAWAYS:boundaries[mapped(a)]='retained-cutaway-in';boundaries[mapped(b)]='retained-cutaway-out'
    protected={str(p):sha(p) for p in [SRC,LIVE,ASSET,ROOT/'index.html',ROOT/'lessons/does-ai-think.md',ROOT/'gemini-notebook/does-ai-think/PROMPT.txt']}
    assert protected[str(SRC)]==protected[str(LIVE)]==EXPECTED
    manifest=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DST),source_frames=SOURCE_FRAMES,
                  frames=TOTAL,fps=30,duration=TOTAL/30,cuts=CUTS,keep=KEEP,removed_seconds=REMOVED/30,
                  reencoded_source_intervals=ENCODE,board_source_interval=BOARD,board_output_interval=[start,end],
                  board_asset=str(ASSET),board_asset_sha256=sha(ASSET),canvas_size=[cw,ch],canvas_offset=[ox,oy],
                  row_rectangles=rects,row_onsets_output=onsets,retained_cutaways=CUTAWAYS,
                  boundaries=boundaries,protected_hashes=protected,audio_source_replacement_samples=[AUDIO_START,AUDIO_END],
                  audio_output_replacement_samples=[AUDIO_START,AUDIO_END-REMOVED*SPF],
                  audio_cut_ramp_samples=240,status='review-candidate; not installed',
                  scope='Approved four cuts, current three-row board, combined first highlight. Remaining source timeline retained.',
                  source_treatment='Unchanged video GOPs and audio outside the edited comparison passage are packet copied from stable v10. Only replacement intervals and their required codec handles are re-encoded. Original cutaway GOPs are retained exactly.',
                  listening_performed=False,continuous_playback_performed=False)
    return Renderer(spec),manifest

def board_frame(renderer,n): return renderer.at(mapped(n)-mapped(BOARD[0]))[0]

def audio_master():
    raw=OUT/'source.wav'
    if not raw.exists():subprocess.run([FF,'-v','error','-i',str(SRC),'-vn','-ar','48000','-ac','1','-c:a','pcm_s16le',str(raw)],check=True)
    with wave.open(str(raw)) as f:
        assert f.getframerate()==RATE and f.getnchannels()==1
        source=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').copy()
    parts=[source[a*SPF:b*SPF].copy() for a,b in KEEP]
    # Five-ms de-click ramps only inside already measured silence, no added time.
    for i,part in enumerate(parts):
        if i:part[:240]=np.rint(part[:240]*np.linspace(0,1,240)).astype('<i2')
        if i<len(parts)-1:part[-240:]=np.rint(part[-240:]*np.linspace(1,0,240)).astype('<i2')
    master=np.concatenate(parts);assert len(master)==TOTAL*SPF
    def save(path,x):
        with wave.open(str(path),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(x.tobytes())
    save(OUT/'edited.wav',master)
    for i,(a,b) in enumerate(CUTS):
        at=mapped(b)*SPF
        save(OUT/f'join-{i+1}-preview.wav',master[at-3*RATE:at+4*RATE])
    subprocess.run([FF,'-v','error','-y','-i',str(OUT/'edited.wav'),'-c:a','aac','-b:a','192k',str(OUT/'edited-audio.m4a')],check=True)

def build(preview=False):
    assert not DST.exists(),'Never overwrite a review candidate'
    renderer,m=prepare(); (OUT/'preview').mkdir(exist_ok=True)
    wanted=set(m['boundaries'])
    for n in list(wanted):wanted.update([n-1,n+1,n+30])
    for o in sorted(wanted):
        if 0<=o<TOTAL and is_board(MAPPING[o]):
            cv2.imwrite(str(OUT/'preview'/f'{o:05d}.jpg'),board_frame(renderer,MAPPING[o]),[cv2.IMWRITE_JPEG_QUALITY,96])
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    if preview:return
    audio_master();legs=[]
    with av.open(str(SRC)) as src:
        src.streams.video[0].codec_context.thread_count=2
        decoded=iter(enumerate(src.decode(video=0)))
        for i,(a,b) in enumerate(ENCODE):
            path=OUT/f'replacement-{i}.mp4';legs.append(path)
            cmd=[FF,'-v','error','-y','-f','rawvideo','-pixel_format','yuv420p','-video_size','1280x720','-framerate','30','-i','-',
                 '-an','-c:v','libx264','-threads','2','-preset','fast','-crf','17','-profile:v','high','-level:v','3.1','-video_track_timescale','15360',str(path)]
            with (OUT/f'encode-{i}.log').open('w') as log:
                proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log);count=0
                for n,frame in decoded:
                    if n<a:continue
                    if not inside(n,CUTS):
                        if is_board(n):frame=av.VideoFrame.from_ndarray(board_frame(renderer,n),format='bgr24')
                        proc.stdin.write(frame.to_ndarray(format='yuv420p').tobytes());count+=1
                    if n==b-1:break
                proc.stdin.close();assert proc.wait()==0
                assert count==mapped(b)-mapped(a)
            print('Encoded replacement',i,a,b,count,'frames',flush=True)
    with av.open(str(SRC)) as src:
        v=src.streams.video[0];a=src.streams.audio[0];packets=[];keys=[]
        for packet in src.demux(v,a):
            if packet.dts is None:continue
            video=packet.stream.type=='video'
            if video:
                n=round(packet.pts*packet.time_base*FPS)
                if packet.is_keyframe:keys.append(n)
                if inside(n,ENCODE):continue
                delta=(n-mapped(n))*512
                packet.pts-=delta;packet.dts-=delta
            else:
                if AUDIO_START<=packet.pts<AUDIO_END:continue
                if packet.pts>=AUDIO_END:packet.pts-=REMOVED*SPF;packet.dts-=REMOVED*SPF
            packets.append((video,packet))
        for path,(start,end) in zip(legs,ENCODE):
            assert start in keys and end in keys
            with av.open(str(path)) as leg:
                rv=leg.streams.video[0]
                assert rv.time_base==v.time_base and rv.codec_context.extradata==v.codec_context.extradata
                for packet in leg.demux(rv):
                    if packet.dts is None:continue
                    packet.pts+=mapped(start)*512;packet.dts+=mapped(start)*512;packets.append((True,packet))
        with av.open(str(OUT/'edited-audio.m4a')) as ac:
            ra=ac.streams.audio[0]
            assert ra.time_base==a.time_base and ra.codec_context.extradata==a.codec_context.extradata
            for packet in ac.demux(ra):
                if packet.dts is not None and AUDIO_START<=packet.pts<AUDIO_END-REMOVED*SPF:packets.append((False,packet))
        packets.sort(key=lambda row:(row[1].dts*row[1].time_base,not row[0]))
        with av.open(str(DST),'w',options={'movflags':'+faststart'}) as dest:
            ov=dest.add_stream_from_template(v);oa=dest.add_stream_from_template(a)
            for video,packet in packets:packet.stream=ov if video else oa;dest.mux(packet)
    assert all(sha(p)==h for p,h in m['protected_hashes'].items())
    m['candidate_sha256']=sha(DST)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(DST,flush=True)

if __name__=='__main__':
    cv2.setNumThreads(2)
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    build(args.preview)
