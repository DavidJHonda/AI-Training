"""Replace the board visuals on the approved v17 narration timeline."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import (AMBER, BLUE, RED, PURPLE, TEAL, NEUTRAL, Build, FPS,
                            H, W, banner_rect, fr, sha)
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, ring_px, smoothstep
from make_close_board import compose_canonical_for_video

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'course-assets/support-trap'
BASE = ROOT / 'Prompts/support-trap-v17.mp4'
DEST = ROOT / 'Prompts/support-trap-v18.mp4'
AUDIT = ROOT / 'video-audit/support-trap-v18-2026-11-13'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FRAMES = 7082
# v17 returns to the roll-5 timeline 491 frames later after Sophie's story.
SHIFT = 491
CLOSE = 6312 + SHIFT
ASSET_PATHS = {k: ASSETS / f'support-trap-{k}.jpg' for k in ('comparison', 'jobs', 'danger', 'close')}

# Half-open output intervals. Changing the picture never moves an audio sample.
# For roll-4 cutaways each source frame is chosen inside an independent illustrated scene.
SHOTS = [
    (0, 'base', 0),
    (247, 'comparison', 0),
    (fr(27.90), 'installed', fr(29.97)),  # the sister makes room
    (fr(32.65), 'comparison', 0),
    (fr(46.20), 'roll4', 2108),           # confiding in the phone, then lunch alone
    (fr(54.18), 'roll4', 1411),           # supportive words versus the people who can help
    (fr(58.76), 'roll4', 1697),           # the uses of AI
    (fr(63.20), 'roll4', 1978),           # a caring hand
    (1992, 'jobs', 0),
    (fr(81.90), 'roll1', 2816),           # venting: agitated thoughts settle
    (fr(89.45), 'jobs', 0),
    (fr(94.62), 'roll4', 3262),           # practicing on the phone, then speaking to Mom
    (fr(103.40), 'jobs', 0),
    (3588, 'base', 3588),                 # owner-selected warning and entire roll-4 story
    (5317, 'danger', 0),
    (fr(175.36)+SHIFT, 'roll4', 3960),    # leaving the phone behind
    (fr(177.55)+SHIFT, 'danger', 0),
    (fr(196.48)+SHIFT, 'roll4', 6692),    # knocking on a counselor's door
    (fr(202.25)+SHIFT, 'danger', 0),
    (CLOSE, 'close', 0),
]
REGIONS = {
    'disclosure': ((40,112,1560,321), PURPLE),
    'sister': ((40,353,784,1229), BLUE),
    'sister truth': ((58,1017,766,1210), BLUE),
    'chatbot': ((816,353,1560,1229), AMBER),
    'chatbot truth': ((834,1017,1542,1210), AMBER),
    'venting': ((40,128,525,852), TEAL),
    'preparation': ((557,128,1043,852), BLUE),
    'danger card': ((1075,128,1560,852), RED),
    'leave': ((40,127,525,734), RED),
    'now': ((557,127,1043,734), RED),
    'tell': ((1075,127,1560,734), RED),
}
# Each card gets the whole outline first. In the lunch comparison, the outcome
# has a distinct printed section; keep the camera on the complete card for it.
CUES = {
    'comparison': [(0,None),(fr(15.12),'disclosure'),(fr(20.94),'sister'),
                   (fr(25.72),'sister truth'),(fr(32.65),None),(fr(33.68),'chatbot'),
                   (fr(39.74),'chatbot truth')],
    'jobs': [(0,None),(fr(76.12),'venting'),(fr(89.45),None),
             (fr(90.08),'preparation'),(fr(103.40),None),(fr(104.12),'danger card'),
             (fr(112.36),None),(fr(115.98),'jobs banner')],
    'danger': [(0,None),(fr(172.92)+SHIFT,'leave'),(fr(184.26)+SHIFT,'now'),
               (fr(193.82)+SHIFT,'tell'),(fr(205.16)+SHIFT,'danger banner')],
}

class Board:
    def __init__(self, build, key):
        path, cw, ch, ox, oy = build.compose(ASSET_PATHS[key], key)
        self.image = cv2.imread(str(path))
        self.full = np.array([cw/2, ch/2, W/cw])
        self.key, self.offset = key, (ox, oy)
        self.cache = {}
        self.regions = dict(REGIONS)
        self.regions[f'{key} banner'] = (banner_rect(cv2.imread(str(ASSET_PATHS[key]))), NEUTRAL)

    def camera(self, target):
        if not target or target.endswith('banner') or self.key == 'danger':
            return self.full
        parent = target.removesuffix(' truth')
        (l,t,r,b), _ = self.regions[parent]
        # Horizontal paths use one scale per card family; retain the full active card.
        s = min((W-72)/(r-l), (H-56)/(b-t))
        cx, cy = (l+r)/2+self.offset[0], (t+b)/2+self.offset[1]
        ih, iw = self.image.shape[:2]
        return np.array([np.clip(cx, W/(2*s), iw-W/(2*s)),
                         np.clip(cy, H/(2*s), ih-H/(2*s)), s])

    def frame(self, n):
        cues = CUES[self.key]
        i = max(i for i,(f,_) in enumerate(cues) if f <= n)
        at,target = cues[i]
        cam = self.camera(target)
        # Travel toward the next card during the spoken onset. If both cards
        # cannot fit on a pan, show a wide view during that transition.
        elapsed = n-at
        # After a cutaway, land on the full board before the next spoken cue.
        still_return = at in (fr(32.65), fr(89.45), fr(103.40))
        if i and elapsed < 21 and not still_return:
            prev = self.camera(cues[i-1][1])
            cam = prev + (cam-prev)*smoothstep(elapsed/21)
        cx,cy,s = cam
        if target:
            (l,t,r,b), color = self.regions[target]
            l,r = l+self.offset[0],r+self.offset[0]
            t,b = t+self.offset[1],b+self.offset[1]
            # Keep the entire new ring visible from its first spoken frame.
            cx = np.clip(cx, r-(W/2-9)/s, l+(W/2-9)/s)
            cy = np.clip(cy, b-(H/2-9)/s, t+(H/2-9)/s)
        signature = (target, cx,cy,s)
        if signature in self.cache:
            return self.cache[signature]
        tx,ty = W/2-cx*s, H/2-cy*s
        frame = cv2.warpAffine(self.image, np.float32([[s,0,tx],[0,s,ty]]), (W,H),
                               flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        if target:
            stroke = ring_px(H)
            draw_ring(frame,l*s+tx-stroke/2,t*s+ty-stroke/2,
                      r*s+tx+stroke/2,b*s+ty+stroke/2,hex_bgr(color),14*s+stroke/2,stroke)
        if elapsed>=21 or i==0:
            self.cache[signature]=frame
        return frame

def main():
    if DEST.exists():
        raise FileExistsError(DEST)
    assert sha(BASE)=='98639e00a74846a9de7922e7306ea5214b2978c0ced9adca2ed2d282ec5ced65'
    AUDIT.mkdir(parents=True,exist_ok=True)
    cv2.setNumThreads(2)
    files = {'base':BASE,'installed':ASSETS/'support-trap.mp4',
             'roll1':ROOT/'Prompts/support-trap-1.mp4','roll4':ROOT/'Prompts/support-trap-4.mp4'}
    with TemporaryDirectory(dir=DEST.parent) as tmp:
        work=Path(tmp)
        build=Build(ROOT,BASE,work,DEST)
        boards={key:Board(build,key) for key in CUES}
        compose_canonical_for_video(ASSET_PATHS['close'],work/'close.png','#ffffff')
        close=cv2.imread(str(work/'close.png'))
        mask=glyph_mask()
        candidate=work/'candidate.mp4'
        cmd=[FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30',
             '-i','pipe:0','-i',str(BASE),'-map','0:v','-map','1:a:0','-c:a','copy',
             '-c:v','libx264','-preset','veryfast','-crf','16','-threads','4','-pix_fmt','yuv420p',
             '-movflags','+faststart',str(candidate)]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for (start,key,source_start),end in zip(SHOTS,[r[0] for r in SHOTS[1:]]+[FRAMES]):
                print(start,end,key,flush=True)
                if key in files:
                    reader=cv2.VideoCapture(str(files[key]))
                    reader.set(cv2.CAP_PROP_POS_FRAMES,source_start)
                for n in range(start,end):
                    if key in boards:
                        frame=boards[key].frame(n)
                    elif key=='close':
                        progress=np.clip((n-start-48)/149,0.,1.)
                        scale=W/close.shape[1]*(1+.2*smoothstep(progress))
                        frame=cv2.warpAffine(close,np.float32([[scale,0,(W-close.shape[1]*scale)/2],
                            [0,scale,(H-close.shape[0]*scale)/2]]),(W,H),borderValue=(255,255,255))
                    else:
                        ok,frame=reader.read()
                        assert ok,(key,n)
                        if key!='installed':
                            frame=clean_frame(frame,mask)[0]
                    proc.stdin.write(frame.tobytes())
                if key in files:reader.release()
        finally:
            proc.stdin.close()
        if proc.wait():raise RuntimeError('Encoding failed')
        candidate.rename(DEST)
    result=dict(candidate=DEST.name,sha256=sha(DEST),fps=FPS,frames=FRAMES,
                sources={k:sha(v) for k,v in files.items()},boards={k:sha(v) for k,v in ASSET_PATHS.items()},
                regions=REGIONS,cues=CUES,shots=SHOTS,audio='v17 AAC stream copy',
                density={'comparison':'dense, entire active card','jobs':'dense, entire active card','danger':'compact, full board'})
    (AUDIT/'edit-manifest.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
