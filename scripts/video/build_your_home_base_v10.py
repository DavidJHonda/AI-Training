#!/usr/bin/env python3
"""Approved photographic comparison scenes and centered ChatGPT home-base sign.

Review candidate only. Original audio packets and all unaffected source frames
are carried through; no canonical course files are modified.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import types

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build
from ken_burns_path import smoothstep, window

FF = imageio_ffmpeg.get_ffmpeg_exe()
ASSETS = ROOT / 'scripts/video/assets/your-home-base-scenes-2026-11-07'
AUDIT = ROOT / 'video-audit/your-home-base-scenes-v10-2026-11-07'
SOURCE = ROOT / 'Prompts/your-home-base-v9.mp4'
LIVE = ROOT / 'course-assets/your-home-base/your-home-base.mp4'
DEST = ROOT / 'Prompts/your-home-base-v10.mp4'
EXPECTED = '27fd288d9c1dc240ee3e34cc4d57223bdd26d42c4dbb2d8453ed181974428145'
FPS, TOTAL, W, H = 30, 5703, 1280, 720
SPANS = [
    (1404, 1591, 'chatgpt-art-night'),
    (1591, 1818, 'claude-compare-plans'),
    (1818, 2044, 'gemini-organize-event'),
    (2373, 2496, 'chatgpt-art-night'),
    (2849, 2964, 'claude-compare-plans'),
    (3390, 3544, 'gemini-organize-event'),
    (4507, 4873, 'home-base-chatgpt-center'),
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def audio_sha(p):
    data = subprocess.check_output([FF, '-v', 'error', '-i', str(p),
                                   '-map', '0:a:0', '-c', 'copy', '-f', 'data', '-'])
    return hashlib.sha256(data).hexdigest()


def fit_scene(p):
    im = cv2.imread(str(p))
    assert im is not None, p
    h, w = im.shape[:2]
    cw, ch = min(w, h * W / H), min(h, w * H / W)
    x, y = round((w-cw)/2), round((h-ch)/2)
    return cv2.resize(im[y:y+round(ch), x:x+round(cw)], (W,H), interpolation=cv2.INTER_AREA)


def prepare_board():
    # Format normalization only; semantic sign edit was produced with image_gen.
    board = cv2.imread(str(ASSETS / 'home-base-chatgpt-center.png'))
    board = cv2.resize(board, (1600,1150), interpolation=cv2.INTER_LANCZOS4)
    jpg = ASSETS / 'your-home-base-home-base-v10.jpg'
    cv2.imwrite(str(jpg), board, [cv2.IMWRITE_JPEG_QUALITY, 97])
    path,cw,ch,ox,oy = Build.compose(types.SimpleNamespace(out=AUDIT), jpg, 'home-base')
    assert (cw,ch,ox,oy) == (2208,1242,304,46)
    im = cv2.imread(str(path))
    full = np.array([cw/2,ch/2,float(cw)])
    pushed = np.array([cw/2,ch/2,cw*.97])
    # Complete students' faces and center sign share the selected photo window.
    center = np.array([1110.,465.,1100.])
    beats = [
        (100, full, pushed, 'establish'),
        (36, pushed, center, 'move-to-center-ChatGPT'),
        (67, center, center, 'hold-center-ChatGPT'),
        (45, center, full, 'return-to-full'),
        (118, full, full, 'hold-full'),
    ]
    return im, beats, jpg


def board_frame(im, beats, n):
    at = 0
    for count,frm,to,label in beats:
        if n < at+count:
            t = smoothstep((n-at)/max(1,count-1))
            cam = frm+(to-frm)*t
            x,y,w,h = window(*cam,W/H,im.shape[1],im.shape[0])
            matrix = np.array([[w/W,0,x],[0,h/H,y]],np.float32)
            return cv2.warpAffine(im,matrix,(W,H),flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP)
        at += count
    raise ValueError(n)


def main():
    assert not DEST.exists(), f'Never overwrite review candidate: {DEST}'
    assert sha(SOURCE) == EXPECTED and sha(LIVE) == EXPECTED
    protected_paths = [LIVE,ROOT/'index.html',ROOT/'lessons/your-home-base.md',
                       *sorted((ROOT/'course-assets/your-home-base').glob('*.jpg'))]
    protected = {str(p):sha(p) for p in protected_paths}
    scenes = {name:fit_scene(ASSETS/f'{name}.png') for _,_,name in SPANS if not name.startswith('home-base')}
    board,beats,jpg = prepare_board()
    previews = AUDIT/'previews';previews.mkdir(exist_ok=True)
    for name,im in scenes.items():cv2.imwrite(str(previews/f'{name}.jpg'),im)
    for n in [0,99,135,202,247,365]:
        cv2.imwrite(str(previews/f'home-base-{n:03d}.jpg'),board_frame(board,beats,n))
    cmd = [FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size',f'{W}x{H}',
           '-framerate',str(FPS),'-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0',
           '-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1',
           '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
    (AUDIT/'encode-command.json').write_text(json.dumps(cmd,indent=2)+'\n')
    process = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    cap=cv2.VideoCapture(str(SOURCE));n=0
    while True:
        ok,im=cap.read()
        if not ok:break
        for start,end,name in SPANS:
            if start<=n<end:
                im=board_frame(board,beats,n-start) if name.startswith('home-base') else scenes[name]
                break
        process.stdin.write(im.tobytes());n+=1
        if n%900==0:print(f'Rendered {n}/{TOTAL}',flush=True)
    cap.release();process.stdin.close()
    assert process.wait()==0 and n==TOTAL
    cap=cv2.VideoCapture(str(DEST));count=0
    while cap.grab():count+=1
    fps=cap.get(cv2.CAP_PROP_FPS);cap.release()
    assert count==TOTAL and fps==FPS
    before_audio,after_audio=audio_sha(SOURCE),audio_sha(DEST)
    assert before_audio==after_audio
    assert sha(SOURCE)==EXPECTED
    assert all(sha(p)==s for p,s in protected.items())
    manifest={
        'scope':'Approved narrow visual repair; review candidate only',
        'source':str(SOURCE),'source_sha256':EXPECTED,'candidate':str(DEST),'candidate_sha256':sha(DEST),
        'frames':count,'fps':fps,'duration':count/fps,'audio_packets_identical':True,
        'audio_payload_sha256':after_audio,'protected':protected,
        'assets':{str(p):sha(p) for p in sorted(ASSETS.glob('*')) if p.is_file()},
        'changed_spans':[{'frames':[a,b],'seconds':[a/FPS,b/FPS],'asset':name} for a,b,name in SPANS],
        'board':{'asset':str(jpg),'canvas':[2208,1242,304,46],
                 'beats':[{'frames':n,'from':a.tolist(),'to':b.tolist(),'label':label} for n,a,b,label in beats],
                 'rings':[],'density':'photographic illustration; center sign and students remain visible'},
        'source_limitation':'One video encode from retained finished v9; raw rolls unavailable.',
        'longest_unchanged_big_three_board_run_seconds':(4098-3544)/FPS,
        'publication':'Review only; installed course unchanged.'}
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    boundaries={}
    for a,b,name in SPANS:
        boundaries[a]=f'enter-{name}'
        boundaries.setdefault(b,f'exit-{name}')
    # Camera beat changes are continuous motion, not visual splices. Their
    # expected frames are checked separately; cut detection misreads fast zooms.
    args=[x for frame,label in sorted(boundaries.items()) for x in ['--boundary',f'{frame}:{label}']]
    subprocess.run([sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),
                    *args,'--outdir',str(AUDIT/'transitions-cuts')],check=True)
    print('Complete:',DEST,flush=True)


if __name__=='__main__':main()
