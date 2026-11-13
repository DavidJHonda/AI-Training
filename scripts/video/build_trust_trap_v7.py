"""Build the November 13 Trust Trap review cut using the accepted pickup assembly."""
import json
import os
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, CLOSE_PREHOLD, CLOSE_PUSH, FPS, H, SPF, SR, W, fr, sha
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, ring_px
from make_close_board import compose_canonical_for_video
from build_training_bias_v12 import camera, ease, spoken_rms

ROOT = Path(__file__).resolve().parents[2]
PROMPTS = ROOT / 'Prompts'
ASSETS = ROOT / 'course-assets/trust-trap'
OUT = PROMPTS / 'trust-trap-v7.mp4'
AUDIT = ROOT / 'video-audit/trust-trap-v7-2026-11-13'
FF = imageio_ffmpeg.get_ffmpeg_exe()
SOURCES = {k: PROMPTS / f'trust-trap-{k}.mp4'
           for k in ('1', '2', '3', 'opener', 'college-1', 'college-2', 'v6')}

# Original source seconds. First twelve cuts follow the approved audition.
SOUND = [
    ('aside', 'opener', 24.87, 30.74), ('stakes', 'opener', 40.53, 44.45),
    ('college', '1', 17.62, 21.20), ('settings', '1', 28.66, 35.80),
    ('question', 'college-1', 37.25, 39.34), ('mom', '1', 38.79, 49.64),
    ('mom-truth', '1', 52.40, 56.67), ('chatbot', '1', 58.38, 65.68),
    ('prompt', 'college-1', 111.25, 114.44), ('unseen', 'college-1', 116.56, 120.89),
    ('no-stake', 'college-1', 125.73, 128.07), ('reflection', 'college-1', 152.13, 153.60),
    ('generic', '1', 85.52, 99.86), ('definition', '2', 104.57, 110.09),
    ('why', 'v6', 89.37, 113.83), ('practical', '1', 147.33, 178.40),
    ('close', '1', 182.85, 192.40),
]

# Each picture starts relative to its named audio passage; source movie intervals
# are independent of the sound. A board state can span several audio joins.
PICTURE = [
    ('aside', 0, 'movie', '1', 0.0, 3.7),
    ('stakes', 0, 'movie', '1', 11.7, 16.8),
    ('college', 0, 'movie', '1', 17.85, 21.40),
    ('settings', 0, 'movie', 'college-1', 14.95, 18.25),
    ('settings', 3.45, 'movie', '1', 32.3, 36.0),
    ('settings', 6.25, 'compare', 'full'),
    ('mom', 0.18, 'compare', 'mom'),
    ('mom', 6.62, 'movie', 'college-2', 58.8, 63.72),
    ('mom-truth', 0, 'compare', 'mom-truth'),
    ('chatbot', 0.1, 'compare', 'ai'),
    ('prompt', 0.15, 'compare', 'ai-truth'),
    ('reflection', 0, 'compare', 'full'),
    ('generic', 2.85, 'movie', '1', 115.9, 122.1),
    ('generic', 8.9, 'movie', '1', 92.4, 96.6),
    ('definition', 0, 'movie', '2', 103.8, 109.1),
    ('definition', 3.27, 'why-board', 'full'),
    ('why', 0.25, 'why-board', 'language'),
    ('why', 10.5, 'movie', 'v6', 119.2, 122.9),
    ('why', 15.39, 'why-board', 'person'),
    ('why', 18.55, 'movie', '2', 128.15, 132.7),
    ('why', 23.0, 'why-board', 'banner'),
    ('practical', 1.3, 'movie', '1', 149.7, 156.1),
    ('practical', 8.9, 'movie', '1', 156.7, 161.0),
    ('practical', 13.5, 'movie', '3', 178.6, 186.5),
    ('practical', 21.5, 'movie', '2', 172.45, 175.16),
    ('practical', 25.3, 'movie', '1', 173.25, 178.1),
    ('close', 0, 'closing', 'full'),
]
# Native image bounds for the two full cards, their captions, and the banner.
REGIONS = {
    'mom': ((40,271,784,1188), '#1652f0'),
    'mom-truth': ((58,983,768,1167), '#1652f0'),
    'ai': ((816,271,1560,1188), '#a9760c'),
    'ai-truth': ((834,983,1544,1167), '#a9760c'),
    'language': ((40,128,784,677), '#4f2fc4'),
    'person': ((816,128,1560,677), '#0e8f86'),
    'banner': ((40,717,1560,805), '#6e51ff'),
}


def audio_track(work, sound, sources):
    parts = []
    timeline = []
    cursor = 0
    for name, source, start, end in sound:
        a, b = fr(start), fr(end)
        raw = subprocess.check_output([FF, '-v', 'error', '-ss', str(a/FPS), '-i', str(sources[source]),
                                      '-t', str((b-a)/FPS), '-vn', '-ac', '1', '-ar', str(SR),
                                      '-f', 'f32le', '-'])
        pcm = np.frombuffer(raw, '<f4')[:(b-a)*SPF].copy()
        assert pcm.size == (b-a)*SPF, name
        parts.append(pcm)
        timeline.append(dict(name=name, source=source, source_frames=[a,b], start=cursor, end=cursor+b-a))
        cursor += b-a
    levels = {}
    for source in {s[1] for s in sound}:
        samples = np.concatenate([p for p,t in zip(parts,timeline) if t['source']==source])
        levels[source] = spoken_rms(samples)
    gains = {s:levels['1']/v for s,v in levels.items()}
    peak = max(float(np.max(np.abs(p)))*gains[t['source']] for p,t in zip(parts,timeline))
    headroom = min(1., .95/peak)
    ramp = np.linspace(0,1,240)
    for p,t in zip(parts,timeline):
        p *= gains[t['source']] * headroom
        p[:240] *= ramp
        p[-240:] *= ramp[::-1]
    np.concatenate(parts).tofile(work/'mix.f32')
    return timeline, {k:round(float(20*np.log10(v*headroom)),2) for k,v in gains.items()}


class Board:
    def __init__(self, build, asset, key, fixed_camera=False):
        self.fixed_camera = fixed_camera
        path, w, h, self.x, self.y = build.compose(asset,key)
        self.canvas = cv2.imread(str(path))
        self.full = np.array([w/2,h/2,w])

    def view(self, state):
        if self.fixed_camera or state in ('full','banner'):
            return self.full
        # Keep the active card complete even when the ring singles out its caption.
        rect = REGIONS[state.split('-')[0]][0]
        l,t,r,b = rect
        return np.array([self.x+(l+r)/2,self.y+(t+b)/2,Build.fit_w(r-l,b-t)])

    @lru_cache(maxsize=12)
    def frame(self, state, previous, step):
        start, finish = self.view(previous), self.view(state)
        view = start + (finish-start)*ease(step/48)
        pic,x,y = camera(self.canvas,*view)
        if state!='full':
            rect,color = REGIONS[state]
            scale = W/view[2]
            l,t,r,b = rect
            half = ring_px(H)/2
            draw_ring(pic,(l+self.x-x)*scale-half,(t+self.y-y)*scale-half,
                      (r+self.x-x)*scale+half,(b+self.y-y)*scale+half,
                      hex_bgr(color),14*scale+half,ring_px(H))
        return pic


def movie_frames(source, begin, end, count, mask, sources):
    cap = cv2.VideoCapture(str(sources[source]))
    first, last = fr(begin), fr(end)
    cap.set(cv2.CAP_PROP_POS_FRAMES,first)
    current = first-1
    try:
        for k in range(count):
            target = first + k*(last-first)//count
            while current < target:
                ok,raw = cap.read()
                if not ok:
                    raise RuntimeError(f'Missing frame {target} in {source}')
                current += 1
                pic = raw if source=='v6' else clean_frame(raw,mask)[0]
            yield pic
    finally:
        cap.release()


def build_review(output, audit, sound, picture, sources, fixed_boards=()):
    if output.exists():
        raise FileExistsError(output)
    audit.mkdir(parents=True,exist_ok=True)
    cv2.setNumThreads(2)
    with tempfile.TemporaryDirectory(dir=ROOT/'tmp') as tmp:
        work = Path(tmp)
        timeline,gains = audio_track(work, sound, sources)
        starts = {row['name']:row['start'] for row in timeline}
        build = Build(ROOT,sources['1'],work,output)
        boards = {key:Board(build,ASSETS/f'trust-trap-{slug}.jpg',key,key in fixed_boards)
                  for key,slug in [('compare','comparison'),('why-board','eliza')]}
        compose_canonical_for_video(ASSETS/'trust-trap-close.jpg',work/'close.png','#ffffff')
        close = cv2.imread(str(work/'close.png'))
        count = timeline[-1]['end']
        shots = [(starts[name]+fr(offset),kind,params) for name,offset,kind,*params in picture]
        mask = glyph_mask()
        temp = work/'review.mp4'
        args = [FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),
                '-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1','-i',str(work/'mix.f32'),
                '-c:v','libx264','-pix_fmt','yuv420p','-preset','fast','-crf','16','-threads','4',
                '-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)]
        proc = subprocess.Popen(args,stdin=subprocess.PIPE)
        try:
            for i,(start,kind,params) in enumerate(shots):
                duration = (shots[i+1][0] if i+1<len(shots) else count)-start
                assert duration>0
                if kind=='movie':
                    for frame in movie_frames(*params,duration,mask,sources):
                        proc.stdin.write(frame.tobytes())
                elif kind=='closing':
                    for k in range(duration):
                        zoom = 1+.2*ease((k-CLOSE_PREHOLD)/(CLOSE_PUSH-1))
                        frame,_,_ = camera(close,close.shape[1]/2,close.shape[0]/2,close.shape[1]/zoom)
                        proc.stdin.write(frame.tobytes())
                else:
                    state = params[0]
                    prev = shots[i-1][2][0] if i and shots[i-1][1]==kind else state
                    for k in range(duration):
                        step = min(48,k) if state!=prev else 48
                        proc.stdin.write(boards[kind].frame(state,prev,step).tobytes())
                print(f'{(start+duration)/FPS:.1f}s  {kind} {params}',flush=True)
        finally:
            proc.stdin.close()
            result = proc.wait()
        if result:
            raise RuntimeError(f'Encoder exited {result}')
        cap = cv2.VideoCapture(str(temp))
        actual = round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()
        assert actual==count
        used = {sources[k] for k in gains} | {sources[p[0]] for _,s,p in shots if s=='movie'}
        used.update(ASSETS.glob('*.jpg'))
        record = dict(candidate=str(output.relative_to(ROOT)),frames=count,fps=FPS,seconds=count/FPS,
                      audio=timeline,mix_gain_db=gains,shots=shots,
                      sources={str(p.relative_to(ROOT)):sha(p) for p in sorted(used)},sha256=sha(temp))
        os.link(temp,output)
        (audit/'edit-manifest.json').write_text(json.dumps(record,indent=2)+'\n')


if __name__=='__main__':
    build_review(OUT, AUDIT, SOUND, PICTURE, SOURCES)
