#!/usr/bin/env python3
"""Approved three-source Unexpected Results edit; review candidate only."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import wave

import cv2
import imageio_ffmpeg
import numpy as np

import ken_burns_path as kb
from build_unexpected_results_v4 import Board
from editspec_build import Reader
from gemini_mark import clean_frame, glyph_mask

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/unexpected-results-combined-v5-2026-10-23'
DEST = ROOT / 'Prompts/unexpected-results-v5.mp4'
SOURCES = {'1': ROOT/'Prompts/unexpected-results-1.mp4',
           '3': ROOT/'Prompts/unexpected-results-3.mp4',
           'v4': ROOT/'Prompts/unexpected-results-v4.mp4'}
HASHES = {'1': 'e4a8c71745591423a1c7431fd2a3cf9eba41c89d20fe0c7dcbcbd03b938fc8fe',
          '3': 'c5a31827b8704a4e3f0f60ae5952b0bce2249bb8d77ffc8efd0ac56f9593d6d7',
          'v4': '523d86b547a86fbe0e0403fa78a1db1dad2fb33c1435f4ff0fa915151a687d13'}
BOARD = ROOT/'course-assets/unexpected-results/unexpected-results-plans.jpg'
CLOSE = ROOT/'course-assets/unexpected-results/unexpected-results-close.jpg'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, SR, SPF = 30, 48000, 1600
GAINS = {'1': 0., '3': .7, 'v4': -5.}
# Quiet frame boundaries measured from decoded PCM, with full speech handles.
PARTS = [
    ('1', 0, 297, 'opening'),
    ('1', 1143, 4385, 'hanoi'),
    ('1', 4539, 4701, 'examples-intro'),
    ('3', 4678, 5284, 'texting'),
    ('v4', 3354, 3608, 'cane-toads'),
    ('1', 6339, 6518, 'ai-handoff'),
    ('3', 6207, 6499, 'informed-forecasts'),
    ('v4', 3918, 4714, 'ai-takeaway'),
    ('1', 7915, 8175, 'close'),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def timeline():
    rows, cursor = [], 0
    for source, a, b, kind in PARTS:
        rows.append(dict(source=source, source_start=a, source_end=b,
                         start=cursor, end=cursor+b-a, kind=kind))
        cursor += b-a
    rows.append(dict(source='1', source_start=None, source_end=None,
                     start=cursor, end=cursor+60, kind='close-hold'))
    return rows


class Picture:
    def __init__(self, rows):
        self.rows = rows
        self.board = Board()
        self.close = cv2.imread(str(OUT/'close.png'))
        self.close_start = next(r['start'] for r in rows if r['kind']=='close')
        self.ai_start = next(r['start'] for r in rows if r['kind']=='ai-handoff')
        self.reader = None
        self.mask = glyph_mask()
        self.clean_counts = {}
        self.cached_native = {}

    def native(self, frame):
        if frame in self.cached_native:
            return self.cached_native[frame].copy()
        if self.reader is None or frame < self.reader.n:
            if self.reader:
                self.reader.c.release()
            self.reader = Reader(SOURCES['1'])
        result, method = clean_frame(self.reader.at(frame), self.mask)
        self.clean_counts[str(method)] = self.clean_counts.get(str(method), 0)+1
        # Stable frames used for a necessary chart replacement / lead-in cover.
        if frame in (1148, 3881):
            self.cached_native[frame] = result.copy()
        return result

    def draw(self, row, frame):
        off = frame-row['start']
        kind = row['kind']
        sf = (row['source_start'] or 0)+off
        if kind in ('close', 'close-hold'):
            u = np.clip((frame-self.close_start-48)/149, 0, 1)
            z = 1+.2*kb.smoothstep(u)
            h, w = self.close.shape[:2]
            ww = w/z
            hh = ww*9/16
            transform = np.float32([[ww/1280,0,(w-ww)/2], [0,hh/720,(h-hh)/2]])
            result = cv2.warpAffine(self.close, transform, (1280,720),
                flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            return result, 'canonical-close'
        if kind=='opening':
            return self.native(sf), 'opening-native'
        if kind=='hanoi':
            # Do not leak five frames of the discarded forecasting illustration.
            if sf<1148:
                return self.native(1148), 'hanoi-native'
            if 3882<=sf<4077:
                return self.native(3881), 'mountain-of-tails-chart-replacement'
            # Keep the complete moving rat/breeding diagram: it actually clips
            # the first rat's tail, then sends the next generation around again.
            return self.native(sf), 'hanoi-native'
        if kind=='examples-intro':
            return self.board.draw(), 'board-introduction'
        if kind=='texting':
            if 240<=off<450:
                return self.native(6069+off-240), 'phone-and-toad-illustration'
            target = 'texting' if sf>=round(156.2*FPS) else None
            return self.board.draw(target), 'board-texting'
        if kind=='cane-toads':
            target = 'toads' if sf>=round(111.98*FPS) else 'texting'
            return self.board.draw(target), 'board-cane-toads'
        if kind in ('ai-handoff', 'informed-forecasts'):
            return self.native(6362+frame-self.ai_start), 'ai-forecast-illustrations'
        if kind=='ai-takeaway':
            # Coherent original illustrations under the older, accurate audio.
            if off<297:
                return self.native(6835+off), 'ai-unanticipated-effects'
            if off<480:
                return self.native(7328+off-297), 'ai-curiosity'
            if off<637:
                return self.native(7539+off-480), 'ai-observation'
            return self.native(7753+off-637), 'ai-durable-skills'
        raise ValueError(kind)


def prepare():
    OUT.mkdir(exist_ok=True)
    (OUT/'previews').mkdir(exist_ok=True)
    assert all(sha(SOURCES[k])==v for k,v in HASHES.items())
    rows = timeline()
    audio = {}
    for k,path in SOURCES.items():
        raw = subprocess.check_output([FF,'-v','error','-i',str(path),'-vn',
            '-ac','1','-ar',str(SR),'-f','f32le','-'])
        audio[k] = np.frombuffer(raw, np.float32)
    parts, edges = [], []
    for r in rows:
        if r['kind']=='close-hold':
            seed = audio['1'][round(263.88*SR):round(264.02*SR)].copy()
            data = np.resize(np.r_[seed,seed[::-1]],60*SPF).copy()
        else:
            k = r['source']
            a,b = r['source_start']*SPF,r['source_end']*SPF
            data = audio[k][a:b].copy()*10**(GAINS[k]/20)
            for label,n in [('start',a),('end',b)]:
                q=audio[k][max(0,n-480):n+480]
                db=20*np.log10(max(float(np.sqrt(np.mean(q*q))),1e-12))
                edges.append(dict(kind=r['kind'],source=k,edge=label,
                                  seconds=n/SR,rms_db=db))
                assert n==0 or db<-48,(r['kind'],label,db)
        ramp = np.linspace(0,1,240)
        if r['start']:
            data[:240]*=ramp
        data[-240:]*=ramp[::-1]
        parts.append(data)
    pcm=np.concatenate(parts)
    assert len(pcm)==rows[-1]['end']*SPF and np.max(np.abs(pcm))<1
    with wave.open(str(OUT/'edited.wav'),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes(np.rint(pcm*32767).astype('<i2').tobytes())
    subprocess.run([sys.executable,str(ROOT/'scripts/video/make_close_board.py'),
        '--lesson','unexpected','--out',str(OUT/'close.png')],check=True)
    protected=[*SOURCES.values(),BOARD,CLOSE,
               ROOT/'course-assets/unexpected-results/unexpected-results.mp4']
    manifest=dict(candidate=str(DEST),fps=FPS,frames=rows[-1]['end'],
        duration_seconds=rows[-1]['end']/FPS,rows=rows,
        source_files={k:str(p) for k,p in SOURCES.items()},
        protected_hashes={str(p):sha(p) for p in protected},
        source_audio_edges=edges,gains_db=GAINS,
        loudness_measurement={'roll1_story_lufs':-19.64,'roll3_texting_lufs':-20.37,
                              'v4_ai_takeaway_lufs':-14.65},
        audio='Whole beats, quiet measured cuts, 5ms fades; no speed changes or inserted inter-beat pauses. Two-second room-tone close hold.',
        board_plan={'title':'The Biggest Results Were Never the Plan','density':'compact',
                    'camera':'Full view, full-card purple/teal outlines at spoken onsets',
                    'ring_px':kb.ring_px(720),'support_seconds':7},
        approval='User approved the combined version: roll 1 story/close, roll 3 texting, existing cane-toad and AI takeaway; prior best-of plan supplies informed-forecast beat.',
        source_limitation='Cane-toad and AI audio comes from the retained finished v4; original older raw narration is unavailable. All kept native picture comes directly from raw roll 1.',
        direct_listening_performed=False,continuous_audiovisual_playback_performed=False,
        status='Review candidate only; not installed, committed or published')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    board=Board()
    for target in (None,'texting','toads'):
        cv2.imwrite(str(OUT/'previews'/f'board-{target or "full"}.jpg'),board.draw(target))
    print('Prepared',manifest['duration_seconds'],'seconds',flush=True)
    return manifest


def render(m):
    assert not DEST.exists(),'Use a new candidate version; never overwrite one'
    picture=Picture(m['rows'])
    command=[FF,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
        '-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a',
        '-c:v','libx264','-threads','2','-preset','fast','-crf','17','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    runs=[]
    boundaries={r['start'] for r in m['rows'][1:]}
    previous=None
    for row in m['rows']:
        for f in range(row['start'],row['end']):
            im,kind=picture.draw(row,f)
            if kind!=previous:
                if runs:runs[-1]['end']=f
                runs.append(dict(start=f,kind=kind));boundaries.add(f);previous=kind
            proc.stdin.write(im.tobytes())
            if f==row['start']+30:
                cv2.imwrite(str(OUT/'previews'/f'output-{f:05d}.jpg'),im)
        print(row['kind'],row['end'],flush=True)
    proc.stdin.close()
    assert proc.wait()==0
    runs[-1]['end']=m['frames']
    assert all(sha(p)==h for p,h in m['protected_hashes'].items())
    board_runs=[]
    for r in runs:
        if r['kind'].startswith('board-'):
            if board_runs and board_runs[-1][1]==r['start']:
                board_runs[-1][1]=r['end']
            else:board_runs.append([r['start'],r['end']])
    m.update(candidate_sha256=sha(DEST),visual_runs=runs,boundaries=sorted(boundaries-{0}),
        corner_cleaning=picture.clean_counts,board_runs=board_runs,
        longest_board_run_seconds=max((b-a)/FPS for a,b in board_runs))
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(str(DEST),flush=True)


if __name__=='__main__':
    cv2.setNumThreads(2)
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    manifest=prepare()
    if not args.prepare_only:render(manifest)
