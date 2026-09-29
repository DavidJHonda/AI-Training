#!/usr/bin/env python3
"""Approved narrow repair of verified Flattery Trap live v7; one video encode.

The raw rolls no longer exist locally. Source identity is enforced before and
after rendering. Rebuild the comparison from its canonical JPG, patch only the
RLHF label in the moving source scene, and remove two whole sentences at silence.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import wave

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ken_burns_path as kb

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'course-assets/flattery-trap/flattery-trap.mp4'
ASSET = ROOT / 'course-assets/flattery-trap/flattery-trap-comparison.jpg'
OUT = ROOT / 'video-audit/flattery-trap-repair-2026-09-29-v8'
DEST = ROOT / 'Prompts/flattery-trap-v8.mp4'
SOURCE_HASH = '9c926d2868c198ec14ef3b3cec206f4c00a2f0549e8fa2e74b1505e7cec6fb31'
ASSET_HASH = 'acc368d0445a88c73253f6c17b6c417e091893013f87d08717c7933d290ebe2d'
FPS, N, W, H, SR = 30, 9881, 1280, 720, 48000
CUTS = [(4828, 5080), (5190, 5388)]
FF = imageio_ffmpeg.get_ffmpeg_exe()


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def output_frame(f):
    return f - sum(max(0, min(f, b) - a) for a, b in CUTS)


def prepare_board():
    # Reproduce the full-view canvas of the approved live board. White stage
    # comes from the same corner of the existing asset; do not change the JPG.
    board = cv2.imread(str(ASSET))
    canvas = np.full((1710, 3040, 3), board[4, 4], np.uint8)
    canvas[64:1646, 720:2320] = board
    cv2.imwrite(str(OUT / 'canvas-comparison.png'), canvas)
    full = [1520, 855, 3040]
    left = [1135, 969, 2063]
    right = [1910, 969, 2063]
    stages = [
        (690, 1163, full, full, 'full-introduction-and-scenario'),
        (1163, 1199, full, left, 'dive-flattery'),
        (1199, 1564, left, left, 'flattery'),
        (1564, 1604, left, full, 'return-for-comparison'),
        (1604, 1640, full, right, 'dive-useful-feedback'),
        (1640, 2077, right, right, 'useful-feedback'),
        (2077, 2119, right, full, 'return-for-takeaway'),
        (2119, 2487, full, full, 'takeaway-and-positive-feedback-limit'),
    ]
    # Rectangles are native JPG x,y,w,h, transformed onto the canvas below.
    states = [
        (867, 1163, [40, 112, 1520, 239], '#6e51ff', 'scenario'),
        (1163, 1208, [40, 383, 744, 1030], '#a9760c', 'whole-flattery-card'),
        (1208, 1364, [56, 935, 718, 105], '#a9760c', 'flattery-response'),
        (1364, 1514, [56, 1057, 718, 91], '#a9760c', 'flattery-no-evidence'),
        (1514, 1604, [56, 1176, 718, 91], '#a9760c', 'flattery-could-fit'),
        (1604, 1677, [816, 383, 744, 1030], '#1652f0', 'whole-useful-card'),
        (1677, 1933, [832, 935, 716, 105], '#1652f0', 'useful-response'),
        (1933, 2027, [832, 1176, 716, 91], '#1652f0', 'missing-thesis'),
        (2027, 2119, [832, 1295, 716, 90], '#1652f0', 'specific-next-move'),
        (2119, 2487, [40, 1454, 1520, 88], '#6e51ff', 'takeaway'),
    ]
    spec = {'image': str(OUT / 'canvas-comparison.png'), 'fps': FPS,
            'out_w': W, 'out_h': H, 'upscale': 2, 'density': 'dense',
            'beats': [{'label': name, 'frames': b-a, 'from': start, 'to': end}
                      for a, b, start, end, name in stages],
            'rings': [{'start': a-690, 'end': b-690,
                       'rect': [r[0]+720, r[1]+64, r[2], r[3]],
                       'color': color, 'radius': 18 if 'whole' in name else 14,
                       'label': name} for a, b, r, color, name in states]}
    (OUT / 'comparison-spec.json').write_text(json.dumps(spec, indent=2)+'\n')
    return canvas, stages, states, spec


class BoardRenderer:
    def __init__(self):
        canvas, self.stages, self.states, self.spec = prepare_board()
        self.big = cv2.resize(canvas, None, fx=2, fy=2, interpolation=cv2.INTER_LANCZOS4)
        self.cache = {}

    def render(self, f):
        a, b, start, end, _ = next(s for s in self.stages if s[0] <= f < s[1])
        t = kb.smoothstep((f-a)/(b-a-1)) if b-a > 1 else 1
        cx, cy, width = [start[j]+(end[j]-start[j])*t for j in range(3)]
        state = next((s for s in self.states if s[0] <= f < s[1]), None)
        key = (*start, state[0] if state else -1)
        if start == end and key in self.cache:
            return self.cache[key]
        x, y, ww, hh = kb.window(cx, cy, width, W/H, 3040, 1710)
        X, Y, CW, CH = [round(v*2) for v in (x, y, ww, hh)]
        frame = cv2.resize(self.big[Y:Y+CH, X:X+CW], (W,H), interpolation=cv2.INTER_AREA)
        if state:
            _, _, (rx, ry, rw, rh), color, name = state
            rx += 720; ry += 64
            scale = W/ww; half = kb.ring_px(H)/2
            box = [(rx-x)*scale-half, (ry-y)*scale-half,
                   (rx+rw-x)*scale+half, (ry+rh-y)*scale+half]
            # Every active ring must fit throughout camera motion, not just at rest.
            assert min(box[:2]) >= 0 and box[2] < W and box[3] < H, (f, box, name)
            kb.draw_ring(frame, *box, kb.hex_bgr(color), 14*scale+half, kb.ring_px(H))
        if start == end:
            self.cache[key] = frame
        return frame


class LabelPatch:
    def __init__(self, reference):
        self.template = cv2.cvtColor(reference[150:285,170:540], cv2.COLOR_BGR2GRAY)
        self.ref_contrast = self.contrast(reference, 0, 0)
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 16*4)
        mask = Image.new('L', (W*4,H*4), 0)
        d = ImageDraw.Draw(mask)
        d.text((352*4,323*4), 'Training can reward agreeable answers.',
               font=font, anchor='mm', fill=255)
        self.mask = np.asarray(mask.resize((W,H), Image.Resampling.LANCZOS)).astype(np.float32)/255

    @staticmethod
    def contrast(frame, dx, dy):
        bg = np.median(frame[307+dy:312+dy,220+dx:480+dx])
        ink = np.percentile(frame[316+dy:330+dy,228+dx:479+dx], 12)
        return max(0, bg-ink)

    def apply(self, frame):
        search = cv2.cvtColor(frame[135:300,145:565], cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(search, self.template, cv2.TM_CCOEFF_NORMED)
        _, score, _, (xx, yy) = cv2.minMaxLoc(result)
        dx, dy = xx-25, yy-15
        if score < .5:
            return frame, {'score': score, 'opacity': 0}
        alpha = min(1., self.contrast(frame,dx,dy)/self.ref_contrast)
        out = frame.copy()
        # Interpolate the blank interior paper above/below the original text.
        # Keep the rounded box, original reveal opacity and camera translation.
        x0,x1,y0,y1 = 178+dx,526+dx,311+dy,335+dy
        top = frame[y0-3:y0,x0:x1].astype(np.float32).mean(axis=0)
        bottom = frame[y1:y1+3,x0:x1].astype(np.float32).mean(axis=0)
        for y in range(y0,y1):
            t=(y-y0)/(y1-y0-1)
            out[y,x0:x1] = np.rint(top*(1-t)+bottom*t).astype(np.uint8)
        m = cv2.warpAffine(self.mask,np.float32([[1,0,dx],[0,1,dy]]),(W,H))[:,:,None]*alpha
        out = np.rint(out*(1-m)+np.array([84,84,84])*m).astype(np.uint8)
        return out, {'score': round(score,4), 'opacity': round(alpha,4), 'dx': dx, 'dy': dy}


def audio():
    raw = subprocess.check_output([FF,'-v','error','-i',str(SRC),'-map','0:a:0',
        '-f','f32le','-acodec','pcm_f32le','-ac','1','-ar',str(SR),'-'])
    samples = np.frombuffer(raw, np.float32).copy()[:N*1600]
    ranges = [(0,CUTS[0][0]),(CUTS[0][1],CUTS[1][0]),(CUTS[1][1],N)]
    chunks = [samples[a*1600:b*1600].copy() for a,b in ranges]
    fade = np.linspace(0,1,240,dtype=np.float32)
    for i in range(len(chunks)-1):
        chunks[i][-240:] *= fade[::-1]
        chunks[i+1][:240] *= fade
    joined = np.concatenate(chunks)
    assert len(joined) == (N-450)*1600
    path = OUT/'audio-edited.wav'
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
        w.writeframes(np.rint(np.clip(joined,-1,1)*32767).astype('<i2').tobytes())
    return path


def main():
    global OUT, DEST
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true')
    ap.add_argument('--version',type=int,default=8);args=ap.parse_args()
    if args.version != 8:
        import shutil
        original_out=OUT
        OUT=ROOT/f'video-audit/flattery-trap-repair-2026-09-29-v{args.version}'
        DEST=ROOT/f'Prompts/flattery-trap-v{args.version}.mp4'
        OUT.mkdir(parents=True,exist_ok=True)
        for p in original_out.glob('source-*.jpg'):
            shutil.copyfile(p,OUT/p.name)
    OUT.mkdir(parents=True,exist_ok=True)
    assert sha(SRC)==SOURCE_HASH and sha(ASSET)==ASSET_HASH
    board=BoardRenderer()
    for f in [690,867,1163,1199,1208,1364,1514,1604,1640,1677,1933,2027,2119,2486]:
        cv2.imwrite(str(OUT/f'preview-board-{f:05d}.jpg'),board.render(f))
    reference=cv2.imread(str(OUT/'source-00689.jpg'))
    assert reference is not None, 'prepare source frame 689 first'
    patch=LabelPatch(reference)
    for f in [463,480,689]:
        image=cv2.imread(str(OUT/f'source-{f:05d}.jpg'))
        fixed,log=patch.apply(image);cv2.imwrite(str(OUT/f'preview-label-{f:05d}.jpg'),fixed)
    if args.preview:return
    assert not DEST.exists(), 'Version candidates; never overwrite an existing candidate'
    wav=audio()
    cmd=[FF,'-hide_banner','-loglevel','error','-threads','2','-f','rawvideo','-pix_fmt','bgr24',
         '-s','1280x720','-r','30','-i','-','-i',str(wav),'-map','0:v','-map','1:a',
         '-c:v','libx264','-threads','2','-crf','16','-preset','fast','-pix_fmt','yuv420p',
         '-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
    logpath=OUT/'encode.log'
    label_log=[];written=0
    with logpath.open('w') as log:
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
        cap=cv2.VideoCapture(str(SRC));i=0
        while True:
            ok,frame=cap.read()
            if not ok:break
            if i==4821: before_cut_picture=frame.copy()
            if not any(a<=i<b for a,b in CUTS):
                if 690<=i<2487:frame=board.render(i)
                elif 463<=i<690:
                    frame,info=patch.apply(frame);label_log.append({'frame':i,**info})
                elif 4822<=i<4828:
                    frame=before_cut_picture
                # At the first audio splice the board begins 3 frames later in
                # the old picture. Show its opening frame for those 3 frames to
                # prevent a stale speech-bubble flash before the table intro.
                elif 5080<=i<5083:
                    if i==5080:
                        # Frame 5083 extracted during sequential source preparation.
                        bridge=cv2.imread(str(OUT/'source-05083.jpg'))
                        assert bridge is not None
                    frame=bridge
                proc.stdin.write(frame.tobytes());written+=1
            i+=1
            if i%1500==0:print('source frames',i,'output frames',written,flush=True)
        cap.release();proc.stdin.close();rc=proc.wait()
    assert rc==0 and i==N and written==N-450,(rc,i,written)
    assert sha(SRC)==SOURCE_HASH and sha(ASSET)==ASSET_HASH
    boundaries={463:'label-scene',690:'new-comparison',2487:'comparison-exit',
                4828:'sentence-cut-1',5190:'sentence-cut-2'}
    for a,b,_,_,name in board.stages:boundaries[a]='camera-'+name
    for a,b,_,_,name in board.states:boundaries[a]='ring-'+name
    manifest={'candidate':str(DEST),'candidate_sha256':sha(DEST),'source':str(SRC),
        'source_sha256':SOURCE_HASH,'source_limitation':'Only finished live file available; one new encode',
        'asset':str(ASSET),'asset_sha256':ASSET_HASH,'scope':'Approved three-part narrow repair',
        'fps':FPS,'source_frames':N,'output_frames':written,'duration':written/FPS,
        'cuts_source_frames':CUTS,'audio_splices_output_frames':[4828,4938],
        'audio_fades':'5 ms fades within measured silence; no added time',
        'label_source_span':[463,690],'label_new_text':'Training can reward agreeable answers.',
        'picture_bridge_source_frames':[5080,5083],'picture_bridge_uses_source_frame':5083,
        'orphan_scene_prevented':{'source_span':[4822,4828],'held_source_frame':4821},
        'board_spec':board.spec,'boundaries':[{'frame':output_frame(f),'label':name}
          for f,name in sorted(boundaries.items())],
        'source_and_asset_unchanged':True,'not_auditioned':True,'not_published':True}
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (OUT/'label-tracking.json').write_text(json.dumps(label_log,indent=2)+'\n')
    print('COMPLETE',DEST,written,'frames',written/FPS,'seconds',flush=True)


if __name__=='__main__':main()
