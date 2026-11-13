"""Build the approved five-passage Fake Trap review cut from the November 13 recordings."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np

from build_training_bias_v12 import camera, ease
from build_trust_trap_v7 import audio_track
from editspec_build import Build, CLOSE_PREHOLD, CLOSE_PUSH, FPS, H, SR, W, fr, sha
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, ring_px
from make_close_board import compose_canonical_for_video

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'video-audit/fake-trap-v13-2026-11-13'
DEST = ROOT / 'Prompts/fake-trap-v13.mp4'
ASSETS = ROOT / 'course-assets/fake-trap'
SOURCES = {key: ROOT / f'Prompts/fake-trap-{key}.mp4' for key in ('1', '2', '3', 'v12')}
SOUND = [
    ('hook', '3', 0, 14.30),
    ('comparison', '3', 26.52, 54.55),
    ('appearance', '3', 56.72, 60.55),
    ('definition', '2', 84.03, 87.17),
    ('inverse', '3', 65.02, 69.99),
    ('joke', '3', 71.75, 79.48),
    ('motives', '1', 85.93, 108.00),
    ('checks intro', '3', 98.62, 123.36),
    ('context', '2', 223.32, 232.04),
    ('corroboration and application', '3', 128.85, 155.65),
    ('rule', '2', 277.63, 281.15),
    ('impersonation', '3', 158.75, 171.76),
    ('image safety', '1', 209.89, 230.58),
    ('resources', '3', 185.10, 189.20),
    ('close', '3', 192.13, 200.20),
]

# Cue times refer to the sound source, not the picture source. Film intervals use
# only the intended illustration, including when a cutaway crosses a voice change.
PICTURE = [
    ('hook', 0, 'movie', '3', 0, 14.30),
    ('comparison', 26.52, 'comparison', 'full'),
    ('comparison', 30.94, 'comparison', 'before'),
    ('comparison', 41.24, 'comparison', 'before call'),
    ('comparison', 43.34, 'comparison', 'era'),
    ('comparison', 51.88, 'comparison', 'era call'),
    ('appearance', 56.72, 'comparison', 'banner'),
    ('definition', 84.03, 'movie', '2', 97.75, 104.1),
    ('inverse', 65.02, 'movie', '3', 66.85, 69.88),
    ('joke', 71.75, 'movie', '3', 72.0, 76.9),
    ('motives', 85.93, 'reasons', 'full'),
    ('motives', 89.84, 'reasons', 'money'),
    ('motives', 94.26, 'reasons', 'power'),
    ('motives', 98.72, 'reasons', 'fame'),
    ('motives', 104.06, 'reasons', 'cruelty'),
    ('checks intro', 98.62, 'movie', '1', 116.1, 124.30),
    ('checks intro', 105.10, 'movie', '1', 134.20, 141.85),
    ('checks intro', 108.68, 'movie', '2', 189.65, 194.45),
    ('checks intro', 115.16, 'checks', 'full'),
    ('checks intro', 118.94, 'checks', 'source'),
    ('context', 223.78, 'checks', 'context'),
    ('corroboration and application', 129.34, 'checks', 'corroboration'),
    ('corroboration and application', 134.17, 'movie', '3', 136.8, 145.2),
    ('corroboration and application', 146.24, 'movie', '1', 176.9, 183.28),
    ('corroboration and application', 153.18, 'checks', 'full'),
    ('rule', 278.14, 'checks', 'banner'),
    ('impersonation', 158.75, 'movie', '3', 160.45, 166.88),
    ('impersonation', 165.36, 'movie', '1', 204.8, 210.23),
    ('image safety', 209.89, 'movie', '1', 214.00, 216.00),
    ('image safety', 216.62, 'movie', '2', 302.75, 308.22),
    ('image safety', 224.35, 'movie', 'v12', 215.21, 218.7),
    ('resources', 185.10, 'movie', '1', 233.06, 236.84),
    ('close', 192.13, 'closing', 'full'),
]

REGIONS = {
    'comparison': {
        'before': ((40, 241, 784, 1035), '#a9760c'),
        'before call': ((57, 907, 767, 1016), '#a9760c'),
        'era': ((816, 241, 1560, 1035), '#1652f0'),
        'era call': ((833, 907, 1543, 1016), '#1652f0'),
        'banner': ((40, 1075, 1560, 1163), '#6e51ff')},
    'reasons': {label: ((x, 127, x+356, 622), color)
                for label, x, color in [('money', 40, '#4f2fc4'), ('power', 428, '#1652f0'),
                                         ('fame', 816, '#a9760c'), ('cruelty', 1204, '#c41f28')]},
    'checks': {'source': ((40, 127, 525, 651), '#4f2fc4'),
               'context': ((557, 127, 1043, 651), '#1652f0'),
               'corroboration': ((1075, 127, 1560, 651), '#0e8f86'),
               'banner': ((40, 691, 1560, 779), '#6e51ff')},
}


class LessonBoard:
    def __init__(self, build, key):
        path, width, height, self.ox, self.oy = build.compose(ASSETS / f'fake-trap-{key}.jpg', key)
        self.image = cv2.imread(str(path))
        self.wide = np.array([width/2, height/2, float(width)])
        self.key = key

    def view(self, state):
        if self.key != 'comparison' or state in ('banner', 'full'):
            return self.wide
        l,t,r,b = REGIONS[self.key][state.split()[0]][0]
        return np.array([self.ox+(l+r)/2, self.oy+(t+b)/2, Build.fit_w(r-l,b-t)])

    def frame(self, state, view):
        pic,x,y = camera(self.image, *view)
        if state != 'full':
            (l,t,r,b),color = REGIONS[self.key][state]
            scale = W/view[2]
            half = ring_px(H)/2
            draw_ring(pic, (l+self.ox-x)*scale-half, (t+self.oy-y)*scale-half,
                      (r+self.ox-x)*scale+half, (b+self.oy-y)*scale+half,
                      hex_bgr(color), 14*scale+half, ring_px(H))
        return pic


def movies(key, start, end, count, mask):
    cap = cv2.VideoCapture(str(SOURCES[key]))
    first, stop = fr(start), fr(end)
    cap.set(cv2.CAP_PROP_POS_FRAMES, first)
    last = first-1
    try:
        for i in range(count):
            target = first+(stop-first)*i//count
            if target != last:
                for _ in range(target-last-1):
                    assert cap.grab()
                ok, raw = cap.read()
                assert ok and raw.shape == (H,W,3)
                frame = raw if key == 'v12' else clean_frame(raw,mask)[0]
                last = target
            yield frame
    finally:
        cap.release()


def main():
    if DEST.exists():
        raise FileExistsError(DEST)
    AUDIT.mkdir(exist_ok=True)
    cv2.setNumThreads(2)
    with tempfile.TemporaryDirectory(dir=ROOT/'tmp') as scratch:
        work = Path(scratch)
        build = Build(ROOT,SOURCES['3'],work,DEST)
        audio,gains = audio_track(work,SOUND,SOURCES)
        starts = {r['name']:r['start']-r['source_frames'][0] for r in audio}
        shots = [(starts[beat]+fr(at),kind,params) for beat,at,kind,*params in PICTURE]
        count = audio[-1]['end']
        bounds = [s[0] for s in shots] + [count]
        assert bounds[0]==0 and all(a<b for a,b in zip(bounds,bounds[1:]))
        boards = {k:LessonBoard(build,k) for k in REGIONS}
        compose_canonical_for_video(ASSETS/'fake-trap-close.jpg',work/'close.png','#ffffff')
        close = cv2.imread(str(work/'close.png'))
        mask = glyph_mask()
        candidate = work/'review.mp4'
        args = [build.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),
                '-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1','-i',str(work/'mix.f32'),
                '-c:v','libx264','-preset','fast','-threads','4','-crf','16','-pix_fmt','yuv420p',
                '-c:a','aac','-b:a','192k','-movflags','+faststart',str(candidate)]
        process = subprocess.Popen(args,stdin=subprocess.PIPE)
        try:
            for i,(start,kind,params) in enumerate(shots):
                n = bounds[i+1]-start
                if kind=='movie':
                    for frame in movies(*params,n,mask):
                        process.stdin.write(frame.tobytes())
                elif kind=='closing':
                    for k in range(n):
                        zoom = 1+.2*ease((k-CLOSE_PREHOLD)/(CLOSE_PUSH-1))
                        frame,_,_ = camera(close,close.shape[1]/2,close.shape[0]/2,close.shape[1]/zoom)
                        process.stdin.write(frame.tobytes())
                else:
                    board,state = boards[kind],params[0]
                    current = board.view(state)
                    following = board.view(shots[i+1][2][0]) if i+1<len(shots) and shots[i+1][1]==kind else current
                    # Lead the next card when possible. Keep the current ring inside the frame
                    # during travel by using the wide view for a cross-column change.
                    moving = not np.array_equal(current,following)
                    hold = board.frame(state,current).tobytes()
                    for k in range(n):
                        encoded = hold
                        if moving and k>=n-24:
                            v = current+(following-current)*ease((k-n+24)/24)
                            encoded = board.frame('full',v).tobytes()
                        elif kind=='reasons' and state!='full':
                            elapsed = start+k-starts['motives']-fr(85.93)
                            view = current.copy()
                            view[2] *= 1-min(.014, .014*elapsed/(22*FPS))
                            encoded = board.frame(state,view).tobytes()
                        process.stdin.write(encoded)
                print(f'{start/FPS:7.2f} {kind} {params}',flush=True)
        finally:
            process.stdin.close()
            result = process.wait()
        if result:
            raise RuntimeError(f'Encoder exited {result}')
        cap=cv2.VideoCapture(str(candidate))
        assert round(cap.get(cv2.CAP_PROP_FRAME_COUNT))==count
        cap.release()
        assets=[ASSETS/f'fake-trap-{key}.jpg' for key in (*REGIONS,'close')]
        record=dict(frames=count, fps=FPS, duration=count/FPS, sound=audio,mix_gain_db=gains,shots=shots,
                    regions=REGIONS, added_pauses=[], sources={str(p.relative_to(ROOT)):sha(p) for p in [*SOURCES.values(),*assets]},
                    sha256=sha(candidate))
        (AUDIT/'edit-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
        os.link(candidate,DEST)


if __name__=='__main__':
    main()
