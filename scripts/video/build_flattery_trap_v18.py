"""Assemble the version 2 review cut with two version 1 examples and the live response."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Reader, FPS, H, W, SR, SPF, sha
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, ring_px
from make_close_board import compose_canonical_for_video

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'course-assets/flattery-trap'
DEST = ROOT / 'Prompts/flattery-trap-v18.mp4'
AUDIT = ROOT / 'video-audit/flattery-trap-v18-2026-11-13'
FF = imageio_ffmpeg.get_ffmpeg_exe()
SOURCES = {'v2': ROOT / 'Prompts/flattery-trap-2.mp4', 'v1': ROOT / 'Prompts/flattery-trap-1.mp4',
           'live': ASSETS / 'flattery-trap.mp4'}
# Source frames at 30 fps. Every change of voice falls in a measured speech pause.
EDITS = [
    ('v2', 0, 1075, 0, 'Opening'),
    ('v1', 721, 1720, -1.3, 'Gatsby introduction and flattering reply'),
    ('v2', 1857, 4259, 0, 'Useful feedback, training and sycophancy'),
    ('live', 3031, 3616, -1.7, 'Live April pitch and ChatGPT response'),
    ('v2', 5011, 5706, 0, 'Testing and introduction to the moves'),
    ('v1', 5608, 6009, 1, 'Share Your Opinion Last: weak and better plan prompts'),
    ('v2', 6284, 8750, 0, 'Gaps, rubric, standing instruction and close'),
]
BOARDS = {key: ASSETS / f'flattery-trap-{name}.jpg' for key, name in
          [('gatsby','feedback-comparison'), ('training','cycle-of-praise'), ('quote','sycophancy'),
           ('moves','three-moves'), ('close','close')]}
# Each rectangle follows the corresponding piece of artwork, in its native coordinates.
REGIONS = {
    'scenario': ((40,112,1560,321),'#4f2fc4'), 'praise': ((40,353,784,1352),'#a9760c'),
    'useful': ((816,353,1560,1352),'#1652f0'), 'takeaway': ((40,1390,1560,1480),'#6e51ff'),
    'rank': ((40,191,525,756),'#4f2fc4'), 'win': ((557,191,1043,756),'#1652f0'),
    'numbers': ((1075,191,1560,756),'#0e8f86'),
    'opinion': ((74,139,1526,316),'#0e8f86'), 'gaps': ((74,319,1526,535),'#0e8f86'),
    'rubric': ((74,538,1526,754),'#0e8f86'), 'tip': ((74,767,1526,919),'#0e8f86'),
    'moves-end': ((40,973,1560,1061),'#6e51ff'),
}
# Source cut frames from the originals, independent of the audio splice frames.
# Brief roll-1 writing and sticky-note illustrations interrupt the Gatsby comparison.
PICTURE = {
    'v1': [(721,998,'gatsby',[(808,'scenario')]), (1207,1471,'gatsby',[(1207,'praise')]),
           (5608,6009,'moves',[(5608,'opinion')])],
    'v2': [(1857,2575,'gatsby',[(1857,'useful'),(2312,'takeaway')]),
           (3308,4163,'training',[(3377,'rank'),(3566,'win'),(3878,'numbers')]),
           (5011,5338,'quote',[]),
           (5578,5706,'moves',[]),
           (6284,8278,'moves',[(6306,'gaps'),(6915,'rubric'),(7634,'tip'),(8013,'moves-end')]),
           (8278,8750,'close',[])],
    'live': [(3239,3616,'quote',[])],
}


class Pictures:
    def __init__(self, work):
        self.assets = {k: cv2.imread(str(p)) for k,p in BOARDS.items()}
        close = work / 'close.png'
        compose_canonical_for_video(BOARDS['close'], close, '#ffffff')
        self.assets['close'] = cv2.imread(str(close))
        self.readers = {k: Reader(str(p)) for k,p in SOURCES.items()}
        self.mask = glyph_mask()
        self.cache = {}

    def board(self, key, region):
        if (key, region) in self.cache:
            return self.cache[key, region]
        im = self.assets[key]
        h,w = im.shape[:2]
        scale = min((W-60)/w,(H-32)/h)
        cx,cy = w/2,h/2
        if region:
            (x0,y0,x1,y1),color = REGIONS[region]
            if key == 'gatsby' and region in ('scenario','praise','useful'):
                scale = min((W-64)/(x1-x0), (H-48)/(y1-y0), 0.93)
                cx,cy = (x0+x1)/2,(y0+y1)/2
            elif key == 'moves':
                scale = (W-66)/(x1-x0)
                cy = (y0+y1)/2
        tx,ty = W/2-cx*scale,H/2-cy*scale
        frame = cv2.warpAffine(im,np.float32([[scale,0,tx],[0,scale,ty]]),(W,H),
                               flags=cv2.INTER_AREA,borderValue=(255,255,255))
        if region:
            half = ring_px(H)/2
            draw_ring(frame,x0*scale+tx-half,y0*scale+ty-half,x1*scale+tx+half,y1*scale+ty+half,
                      hex_bgr(color),max(6,14*scale),ring_px(H))
        self.cache[key,region] = frame
        return frame

    def frame(self, source, n):
        for a,b,key,marks in PICTURE[source]:
            if not a <= n < b:
                continue
            if key == 'close':
                return self.closing(n-a)
            region = next((name for time,name in reversed(marks) if time<=n),None)
            return self.board(key,region)
        frame = self.readers[source].at(n)
        return frame if source=='live' else clean_frame(frame,self.mask)[0]

    def closing(self, n):
        # The voice runs longer than the push; hold its final position through the tail.
        progress = float(np.clip((n-48)/149,0,1))
        if progress in (0.,1.) and ('close', progress) in self.cache:
            return self.cache['close',progress]
        im = self.assets['close']
        scale = (W/im.shape[1])*(1+.2*progress**2*(3-2*progress))
        tx,ty = (W-im.shape[1]*scale)/2,(H-im.shape[0]*scale)/2
        frame = cv2.warpAffine(im,np.float32([[scale,0,tx],[0,scale,ty]]),(W,H),
                               flags=cv2.INTER_AREA,borderValue=(255,255,255))
        if progress in (0.,1.):
            self.cache['close',progress] = frame
        return frame


def main(holds=None):
    holds = holds or {}
    if DEST.exists():
        raise FileExistsError(DEST)
    AUDIT.mkdir(parents=True,exist_ok=True)
    cv2.setNumThreads(2)
    sources = {k: np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','1',
                '-ar',str(SR),'-f','f32le','-']),dtype='<f4') for k,p in SOURCES.items()}
    pieces, rows, cursor = [],[],0
    for source,a,b,gain,label in EDITS:
        part = sources[source][a*SPF:b*SPF].copy()
        assert len(part)==(b-a)*SPF
        part *= 10**(gain/20)
        edge = np.linspace(0,1,240)
        part[:240] *= edge
        part[-240:] *= edge[::-1]
        rows.append(dict(label=label,source=source,source_frames=[a,b],output_frames=[cursor,cursor+b-a],gain_db=gain))
        pieces.append(part)
        cursor += b-a
        hold = holds.get((source,b),0)
        if hold:
            # Mirror a quiet shoulder to extend the local room tone without a click.
            seed = sources[source][b*SPF-2400:b*SPF].copy()
            assert np.sqrt(np.mean(seed**2)) < .002
            tone = np.resize(np.concatenate([seed,seed[::-1]]),hold*SPF)
            tone[:240] *= edge
            tone[-240:] *= edge[::-1]
            pieces.append(tone)
            rows.append(dict(label='Pause before the next sentence',source='room tone',
                             output_frames=[cursor,cursor+hold],held_source_frame=b-1))
            cursor += hold
    tail = 75
    pieces.append(np.zeros(tail*SPF,dtype='<f4'))
    with TemporaryDirectory(dir=DEST.parent) as tmp:
        work = Path(tmp)
        pcm = work/'audio.f32'
        np.concatenate(pieces).astype('<f4').tofile(pcm)
        pictures = Pictures(work)
        candidate = work/'candidate.mp4'
        proc = subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
                '-r',str(FPS),'-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1','-i',str(pcm),
                '-c:v','libx264','-preset','veryfast','-crf','17','-threads','4','-pix_fmt','yuv420p',
                '-c:a','aac','-b:a','192k','-movflags','+faststart',str(candidate)],stdin=subprocess.PIPE)
        with proc:
            try:
                for src,a,b,gain,label in EDITS:
                    print(label,flush=True)
                    for frame in range(a,b):
                        picture = pictures.frame(src,frame).tobytes()
                        proc.stdin.write(picture)
                    for _ in range(holds.get((src,b),0)):
                        proc.stdin.write(picture)
                last = pictures.closing(8750-8278).tobytes()
                for _ in range(tail):
                    proc.stdin.write(last)
            finally:
                proc.stdin.close()
        if proc.returncode:
            raise RuntimeError(f'Encoder exited {proc.returncode}')
        candidate.rename(DEST)
    manifest = dict(output=str(DEST.relative_to(ROOT)),fps=FPS,frames=cursor+tail,tail_frames=tail,segments=rows,
                    sources={k:dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for k,p in SOURCES.items()},
                    boards={k:sha(p) for k,p in BOARDS.items()},sha256=sha(DEST))
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')


if __name__=='__main__':
    main()
