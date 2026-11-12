"""Build the v22 review cut from v21 and the approved roll 5 narration pickup."""
from pathlib import Path
import json
import subprocess
from tempfile import TemporaryDirectory

import cv2
import numpy as np
from PIL import Image, ImageDraw

from editorial_typography import face
from editspec_build import Build, Reader, banner_rect, sha
from ken_burns_path import draw_ring, hex_bgr, ring_px

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'course-assets/hallucination'
BASE = ASSETS / 'hallucination.mp4'
DONOR = ROOT / 'Prompts/hallucination-5.mp4'
DEST = ROOT / 'Prompts/hallucination-v22.mp4'
AUDIT = ROOT / 'video-audit/hallucination-v22-2026-11-12'
FPS, RATE, WIDTH, HEIGHT = 30, 48000, 1280, 720
BASE_FRAMES = 5771
# Sample-accurate review-preview edits. The return to v21 is on a video frame.
STUDY_IN = 114.95
DONOR_IN, DONOR_OUT = 125.35, 138.80
RESUME = 3556
CAPTION_START = 3449
CAPTION_END = round((STUDY_IN + DONOR_OUT - DONOR_IN) * FPS)
SHIFT = CAPTION_END - RESUME
TOTAL = BASE_FRAMES + SHIFT
CAPTION = 'About half as likely on the study’s questions'


def board(build, filename):
    path, width, height, ox, oy = build.compose(ASSETS / filename, Path(filename).stem)
    stage = cv2.imread(str(path))
    def scaled(pixels):
        return cv2.resize(pixels, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
    def ring(frame, box, color):
        x0, y0, x1, y1 = box
        result = frame.copy()
        draw_ring(result, (ox+x0)*WIDTH/width-2, (oy+y0)*HEIGHT/height-2,
                  (ox+x1)*WIDTH/width+2, (oy+y1)*HEIGHT/height+2,
                  hex_bgr(color), 12, ring_px(HEIGHT))
        return result
    return stage, ox, oy, scaled, ring


def picture_states(build):
    stage, ox, oy, scale, outline = board(build, 'hallucination-playlist-study.jpg')
    original = cv2.imread(str(ASSETS / 'hallucination-playlist-study.jpg'))
    x0, y0, x1, y1 = banner_rect(original)
    shown = outline(scale(stage), [x0,y0,x1,y1], '#4f2fc4')
    # Cover only the reveal, retaining the complete card illustrations and web credit.
    stage[oy+y0-4:oy+y1+5, ox+x0-4:ox+x1+5] = original[y0-7, 100]
    hidden = scale(stage)
    open_states = [(0, hidden),
                   (round(2.42*FPS), outline(hidden,[40,127,784,830],'#4f2fc4')),
                   (round(8.26*FPS), outline(hidden,[816,127,1560,830],'#1652f0')),
                   (round(25.36*FPS), shown)]
    stage, _, _, scale, outline = board(build, 'hallucination-suspect.jpg')
    full = scale(stage)
    # v21 frame numbers, derived from the spoken onsets. The source board
    # starts at 3826 after the live-action cutaway and exits at 4414.
    check_states = [(3826,full),
                    (3914,outline(full,[40,127,540,738],'#4f2fc4')),
                    (4088,outline(full,[540,127,1060,738],'#1652f0')),
                    (4349,outline(full,[1060,127,1560,738],'#0e8f86'))]
    return open_states, check_states


def caption_frame():
    im = Image.new('RGB',(WIDTH,HEIGHT),'#eae7fd')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((100,163,1180,557), radius=26, fill='white')
    d.text((640,269),'2024  →  2026',font=face('bold',35),anchor='mm',fill='#4f2fc4')
    d.text((640,353),'About half as likely',font=face('bold',67),anchor='mm',fill='#15112a')
    d.text((640,431),'on the study’s questions',font=face('medium',48),anchor='mm',fill='#39334f')
    return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)


def audio(build):
    def pcm(file):
        data = subprocess.check_output([build.ff,'-v','error','-i',str(file),'-vn','-ac','1',
                                        '-ar',str(RATE),'-f','f32le','-'])
        return np.frombuffer(data,dtype='<f4')
    src = pcm(BASE)[:BASE_FRAMES*(RATE//FPS)]
    pickup = pcm(DONOR)[round(DONOR_IN*RATE):round(DONOR_OUT*RATE)].copy()
    pickup *= 10**(.7/20)
    result = np.concatenate((src[:round(STUDY_IN*RATE)], pickup, src[RESUME*(RATE//FPS):]))
    assert len(result) == TOTAL*(RATE//FPS)
    assert np.max(np.abs(pickup)) < 1
    path = build.out/'narration.f32'
    result.astype('<f4').tofile(path)
    return path


def main():
    if DEST.exists():
        raise SystemExit(f'Review candidate already exists: {DEST}')
    assert sha(BASE) == '908f9f35f8db306378223643752f7e9697b13b70110dca3a89ed069cdf6014c2'
    assert sha(DONOR) == '934166a3f1923c60aa2f0347635bf7b9abfc3db31d490b24d6e9e4774de8cea3'
    AUDIT.mkdir(parents=True,exist_ok=True)
    cv2.setNumThreads(2)
    with TemporaryDirectory() as tmp:
        build = Build(ROOT,BASE,Path(tmp),DEST,protected=[DONOR,ASSETS/'hallucination-playlist-study.jpg',ASSETS/'hallucination-suspect.jpg'])
        opening, checking = picture_states(build)
        caption = caption_frame()
        narration = audio(build)
        reader = Reader(BASE)
        tmp_video = build.out/'candidate.mp4'
        cmd = [build.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
               '-r','30','-i','pipe:0','-f','f32le','-ar',str(RATE),'-ac','1','-i',str(narration),
               '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16',
               '-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(tmp_video)]
        proc = subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for frame in range(TOTAL):
                source = frame if frame < CAPTION_START else frame-SHIFT
                if frame < 834:
                    pic = next(im for t,im in reversed(opening) if t<=frame)
                elif CAPTION_START <= frame < CAPTION_END:
                    pic = caption
                elif 3826 <= source < 4414:
                    pic = next(im for t,im in reversed(checking) if t<=source)
                else:
                    pic = reader.at(source)
                proc.stdin.write(pic.tobytes())
        finally:
            proc.stdin.close()
        if proc.wait(): raise RuntimeError('Video encode failed')
        assert all(sha(path)==digest for path,digest in build.hashes.items())
        import shutil
        shutil.copyfile(tmp_video,DEST)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(dict(
        candidate=str(DEST.relative_to(ROOT)),sha256=sha(DEST),frames=TOTAL,fps=FPS,
        duration=TOTAL/FPS,protected_hashes=build.hashes,roll5_seconds=[DONOR_IN,DONOR_OUT],
        gain_db=.7,base_audio_cut=[STUDY_IN,RESUME/FPS],caption=CAPTION,
        caption_frames=[CAPTION_START,CAPTION_END],opener_state_starts=[t for t,_ in opening],
        checking_state_starts=[t+SHIFT for t,_ in checking],checking_end=4414+SHIFT,
        status='Review candidate'),indent=2)+'\n')
    print(f'{DEST}: {TOTAL} frames, {TOTAL/FPS:.3f} s')

if __name__ == '__main__':
    main()
