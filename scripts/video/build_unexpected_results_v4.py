#!/usr/bin/env python3
"""Trim the finished lesson to texting and cane toads. Review candidate only."""
from pathlib import Path
import hashlib
import json
import subprocess
import wave

import av
import cv2
import imageio_ffmpeg
import numpy as np
import ken_burns_path as kb

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/unexpected-results-two-examples-v4-2026-10-23'
SRC = ROOT / 'Prompts/unexpected-results-v3.mp4'
DEST = ROOT / 'Prompts/unexpected-results-v4.mp4'
BOARD = ROOT / 'course-assets/unexpected-results/unexpected-results-plans.jpg'
SOURCE_HASH = '051361422c95c73c7d7127cc5b9908f8652f9b4b8b1a068bb1300c5a5f5bffdc'
FPS, SR, SPF, PREFIX, TOTAL = 30, 48000, 1600, 2469, 7172
FF = imageio_ffmpeg.get_ffmpeg_exe()
RANGES = [
    (0, 2716, 'Rat story, moral, and Once you see that shape, you find it everywhere'),
    (2846, 3483, 'Text messaging: small secondary service becomes an everyday habit'),
    (3924, 4182, 'Cane toads: pest-control plan backfires'),
    (4707, 4766, 'The biggest results were never the plan'),
    (5801, TOTAL, 'AI uncertainty, curiosity, durable skills, and standard close'),
]
RECTS = {'texting': (40, 127, 784, 758), 'toads': (816, 127, 1560, 758)}
COLORS = {'texting': '#4f2fc4', 'toads': '#0e8f86'}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Board:
    def __init__(self):
        image = cv2.imread(str(BOARD))
        assert image.shape[:2] == (798, 1600)
        canvas = np.full((900, 1600, 3), image[20, 100], np.uint8)
        canvas[51:849] = image
        self.full = cv2.resize(canvas, (1280, 720), interpolation=cv2.INTER_AREA)
        self.states = {None: self.full}
        for target, (a, b, c, d) in RECTS.items():
            frame = self.full.copy()
            kb.draw_ring(frame, a*.8-2, (b+51)*.8-2, c*.8+2, (d+51)*.8+2,
                         kb.hex_bgr(COLORS[target]), 14*.8+2, kb.ring_px(720))
            self.states[target] = frame

    def draw(self, target=None):
        return self.states[target]


def picture(f, native, board):
    if 2631 <= f < 2846:
        return board.draw(), 'board-introduction'
    if 2846 <= f < 3483:
        if 3086 <= f < 3389:
            return native, 'retained-texting-animation'
        return board.draw('texting' if f >= 2858 else None), 'board-texting'
    if 3924 <= f < 4182:
        return board.draw('toads' if f >= 3927 else None), 'board-cane-toads'
    if 4707 <= f < 4766 or 5801 <= f < 5813:
        return board.draw(), 'board-summary'
    return native, 'retained-source'


def main():
    cv2.setNumThreads(2)
    OUT.mkdir(parents=True, exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SRC) == SOURCE_HASH
    protected = {str(p): sha(p) for p in [SRC, BOARD,
        ROOT / 'course-assets/unexpected-results/unexpected-results.mp4']}
    board = Board()
    previews = OUT / 'previews'; previews.mkdir(exist_ok=True)
    for name in [None, 'texting', 'toads']:
        cv2.imwrite(str(previews / ((name or 'full')+'.jpg')), board.draw(name))
    raw = subprocess.check_output([FF, '-v', 'error', '-i', str(SRC), '-map', '0:a:0',
        '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'])
    pcm = np.frombuffer(raw, np.float32)[:TOTAL*SPF]
    chunks, segments, boundaries, cursor = [], [], [], 0
    edge_levels=[]
    for i, (a, b, label) in enumerate(RANGES):
        chunk=pcm[a*SPF:b*SPF].copy()
        fade=np.linspace(0,1,240)
        for edge, f in ([('in',a)] if i else []) + ([('out',b)] if i<len(RANGES)-1 else []):
            around=pcm[f*SPF-240:f*SPF+240]
            db=20*np.log10(max(float(np.sqrt(np.mean(around*around))),1e-12))
            assert db < -40, (f,db)
            edge_levels.append(dict(source_frame=f,edge=edge,rms_db=float(db)))
        if i:
            chunk[:240]*=fade
            boundaries.append(dict(frame=cursor,label='audio-splice-'+str(i)))
        if i < len(RANGES)-1: chunk[-240:]*=fade[::-1]
        chunks.append(chunk)
        segments.append(dict(source_frames=[a,b],output_frames=[cursor,cursor+b-a],label=label))
        cursor+=b-a
    samples=np.concatenate(chunks)
    wav=OUT/'audio-edited.wav'
    with wave.open(str(wav),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes(np.rint(np.clip(samples,-1,1)*32767).astype('<i2').tobytes())
    aac=OUT/'audio-edited.m4a'
    subprocess.run([FF,'-v','error','-y','-i',str(wav),'-c:a','aac','-b:a','192k',str(aac)],check=True)
    tail=OUT/'tail-picture.mp4'
    proc=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
        '-r','30','-i','-','-an','-c:v','libx264','-threads','2','-preset','medium','-crf','18',
        '-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1','-video_track_timescale','15360',str(tail)],stdin=subprocess.PIPE)
    runs, previous, written, part = [], None, PREFIX, 0
    with av.open(str(SRC)) as c:
        c.streams.video[0].codec_context.thread_count=2
        for f, decoded in enumerate(c.decode(video=0)):
            if f<PREFIX: continue
            while part<len(RANGES) and f>=RANGES[part][1]:part+=1
            if part>=len(RANGES):break
            if f<RANGES[part][0]:continue
            frame,kind=picture(f,decoded.to_ndarray(format='bgr24'),board)
            if kind!=previous:
                if previous is not None:boundaries.append(dict(frame=written,label=kind))
                runs.append(dict(kind=kind,start=written,end=written+1))
                previous=kind
            else:runs[-1]['end']=written+1
            proc.stdin.write(frame.tobytes());written+=1
    proc.stdin.close();assert proc.wait()==0 and written==cursor
    source,tailc,audioc=av.open(str(SRC)),av.open(str(tail)),av.open(str(aac))
    v,tv,ta=source.streams.video[0],tailc.streams.video[0],audioc.streams.audio[0]
    assert tv.codec_context.extradata==v.codec_context.extradata
    assert tv.frames==cursor-PREFIX
    packets=[]
    for p in source.demux(v):
        if p.dts is not None and p.pts<PREFIX*512:packets.append(('video',p))
    for p in tailc.demux(tv):
        if p.dts is not None:
            p.pts+=PREFIX*512;p.dts+=PREFIX*512;packets.append(('video',p))
    for p in audioc.demux(ta):
        if p.dts is not None:packets.append(('audio',p))
    packets.sort(key=lambda x:x[1].dts*x[1].time_base)
    with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as output:
        ov,oa=output.add_stream_from_template(v),output.add_stream_from_template(ta)
        for kind,p in packets:
            p.stream=ov if kind=='video' else oa;output.mux(p)
    for c in [source,tailc,audioc]:c.close()
    assert all(sha(p)==h for p,h in protected.items())
    board_runs=[]
    for run in runs:
        if run['kind'].startswith('board'):
            if board_runs and board_runs[-1][1]==run['start']:board_runs[-1][1]=run['end']
            else:board_runs.append([run['start'],run['end']])
    boundaries.append(dict(frame=PREFIX,label='packet-copy-to-encode'))
    manifest=dict(source=str(SRC),source_sha256=SOURCE_HASH,candidate=str(DEST),candidate_sha256=sha(DEST),
        board=str(BOARD),board_sha256=sha(BOARD),frames=cursor,fps=FPS,duration_seconds=cursor/FPS,
        removed_seconds=(TOTAL-cursor)/FPS,copied_prefix_frames=PREFIX,segments=segments,
        boundaries=sorted(boundaries,key=lambda x:x['frame']),visual_runs=runs,board_runs=board_runs,
        longest_changed_board_run_seconds=max((b-a)/FPS for a,b in board_runs),
        board_plan=dict(title='The Biggest Results Were Never the Plan',density='compact',
            camera='Full view throughout; one complete-card outline at each spoken onset; unmarked introduction and summary.',
            rectangles=RECTS,colors=COLORS,ring_px=kb.ring_px(720),
            supporting_animation_source_frames=[3086,3389]),
        source_audio_cut_edges=edge_levels,added_pause_seconds=0,protected_hashes=protected,
        source_limitation='Original raw rolls unavailable. Stable finished v3; first 2469 picture frames copied, remaining picture encoded once. Narration trimmed and encoded once.',
        narration_scope='Retain the existing SMS explanation of a secondary feature becoming everyday communication; not a verbatim reading of the newly revised board or its youth-adoption detail.',
        direct_listening_performed=False,continuous_audiovisual_playback_performed=False,
        status='Review candidate only; not installed, committed or published')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:manifest[k] for k in ['candidate','frames','duration_seconds','removed_seconds','longest_changed_board_run_seconds']},indent=2),flush=True)

if __name__=='__main__':main()
