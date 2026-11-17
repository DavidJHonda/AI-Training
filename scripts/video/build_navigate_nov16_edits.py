"""Build Loudest Voices v16 or Where Will AI Land v7 from their approved cuts."""
import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from itertools import chain, islice, repeat

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

from build_training_bias_v12 import camera, ease
from editorial_typography import face
from editspec_build import Build, FPS, H, SR, W, sha
from ken_burns_path import draw_ring, hex_bgr, ring_px

ROOT = Path(__file__).resolve().parents[2]
NARRATION = ROOT / 'scripts/video/assets/navigate-nov16-narration'
ASSETS = ROOT / 'course-assets/where-will-ai-land'
MOVIES = {'voices': ROOT/'Prompts/loudest-voices-v15.mp4', 'land': ROOT/'Prompts/where-will-ai-land-v6.mp4'}
FF = imageio_ffmpeg.get_ffmpeg_exe()
SPF = SR // FPS

# Source boundaries are 30 fps frames in the gaps between spoken phrases.
# (label, audio source, first source frame, exclusive last frame, picture)
VOICES = [
    ('Experts', 'voices', 0, 3057, 'source'),
    ('Ten-year bet', 'bet', None, None, 'experts'),
    ('What can you do?', 'voices', 4222, 4453, 'experts'),
    ('In your hands', 'voices', 4453, 7194, 'source'),
]
LAND = [
    ('Where Will AI Land?', 'hanoi', None, None, 'title'),
    ('Hanoi, 1902', 'land', 410, 3390, 'hanoi-story'),
    ('Four stories', 'compare', None, None, 'full'),
    ('Online shopping', 'voices', 3391, 3669, 'shopping'),
    ('Flying cars', 'voices', 3669, 3960, 'cars'),
    ('Text messaging', 'land', 3728, 4307, 'texting'),
    ('Cane toads', 'land', 4307, 4561, 'toads'),
    ('An open question', 'question', None, None, 'forecasts'),
    ('What nobody predicted', 'land', 5032, 5828, 'source'),
    ('Stay curious', 'land', 5901, 6148, 'close'),
]
COLORS = {'shopping':'#4f2fc4','cars':'#a9760c','texting':'#1652f0','toads':'#0e8f86'}


def audio(path, channels):
    raw = subprocess.check_output([FF, '-v','error','-i',str(path),'-vn','-ar',str(SR),
                                   '-ac',str(channels),'-f','f32le','-'])
    return np.frombuffer(raw,'<f4').reshape(-1,channels)


def level(samples):
    mono = samples.mean(axis=1)
    blocks = mono[:len(mono)//960*960].reshape(-1,960)
    energies = np.sqrt(np.mean(blocks**2,axis=1))
    return np.percentile(energies[energies>.008],55)


def movie_frames(path, start, count):
    capture = cv2.VideoCapture(str(path))
    try:
        capture.set(cv2.CAP_PROP_POS_FRAMES,start)
        for _ in range(count):
            ok, frame = capture.read()
            if not ok:
                raise ValueError(f'Short source at {start}+{count} in {path}')
            yield frame
    finally:
        capture.release()


def title_frames(count):
    image = Image.open(ASSETS/'rat-story/hanoi-street.jpg').convert('RGB').resize((W,H),Image.Resampling.LANCZOS)
    overlay = Image.new('RGBA',(W,H))
    draw = ImageDraw.Draw(overlay)
    draw.rounded_rectangle((50,482,762,640),radius=18,fill=(24,21,44,239))
    draw.text((82,512),'Where Will AI Land?',font=face('bold',66),fill='white')
    draw.text((85,598),'Hanoi, 1902',font=face('medium',26),fill=(225,218,253))
    background = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    titled = cv2.cvtColor(np.array(Image.alpha_composite(image.convert('RGBA'),overlay).convert('RGB')),cv2.COLOR_RGB2BGR)
    for frame in range(count):
        blend = ease((frame-150)/24)
        yield titled if blend==0 else background if blend==1 else cv2.addWeighted(titled,1-blend,background,blend,0)


class Board:
    def __init__(self,tmp):
        build = Build(ROOT,MOVIES['land'],tmp,ROOT/'Prompts/where-will-ai-land-v7.mp4')
        path,w,h,ox,oy = build.compose(ASSETS/'where-will-ai-land-plans.jpg','four-stories')
        self.canvas = cv2.imread(str(path))
        self.views = {'full':np.array([w/2,h/2,float(w)])}
        self.boxes = {}
        for i,key in enumerate(COLORS):
            left = ox + (40,816)[i%2]
            top = oy + (127,790)[i//2]
            self.boxes[key] = (left,top,left+744,top+631)
            self.views[key] = np.array([left+372,top+315.5,Build.fit_w(744,631)])

    def frames(self,key,count,following):
        start=self.views[key]
        end=self.views.get(following,start)
        hold,x,y=camera(self.canvas,*start)
        if key in COLORS:
            scale=W/start[2]
            l,t,r,b=self.boxes[key]
            draw_ring(hold,(l-x)*scale-2,(t-y)*scale-2,(r-x)*scale+2,(b-y)*scale+2,
                      hex_bgr(COLORS[key]),14*scale+2,ring_px(H))
        for i in range(count):
            if np.array_equal(start,end) or i < count-25:
                yield hold
            else:
                view=start+(end-start)*ease((i-count+25)/24)
                yield camera(self.canvas,*view)[0]


def render(lesson):
    cv2.setNumThreads(2)
    voices = lesson=='voices'
    name = 'loudest-voices-v16' if voices else 'where-will-ai-land-v7'
    output = ROOT/'Prompts'/f'{name}.mp4'
    if output.exists():
        raise FileExistsError(output)
    dest = ROOT/'video-audit'/f'{name}-2026-11-16'
    dest.mkdir(exist_ok=True)
    channels = 2 if voices else 1
    source = {key:audio(path,channels) for key,path in MOVIES.items()}
    # Use the exact decoded video length at the original tail.
    parts = list(VOICES if voices else LAND)
    if not voices:
        cap=cv2.VideoCapture(str(MOVIES['land']))
        end=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); cap.release()
        parts[-1]=(*parts[-1][:3],end,'close')
    reference = level(source['voices'][142*SR:151*SR]) if voices else level(source['land'][14*SR:39*SR])
    with tempfile.TemporaryDirectory(dir=ROOT/'tmp') as td:
        work=Path(td)
        rows=[]; cursor=0
        with (work/'sound.f32').open('wb') as wav:
            for label,src,a,b,visual in parts:
                if src in source:
                    buf=source[src][a*SPF:b*SPF].copy()
                    assert len(buf)==(b-a)*SPF
                else:
                    buf=audio(NARRATION/(src+'.wav'),channels).copy()
                    buf=np.pad(buf,((0,(-len(buf))%SPF),(0,0)))
                gain=1.
                if src not in source or (not voices and src=='voices'):
                    gain=min(reference/level(buf),.95/np.max(abs(buf)))
                    buf*=gain
                if rows: buf[:240]*=np.linspace(0,1,240)[:,None]
                buf[-240:]*=np.linspace(1,0,240)[:,None]
                wav.write(buf.astype('<f4').tobytes())
                count=len(buf)//SPF
                rows.append(dict(label=label,source=src,source_frames=[a,b],visual=visual,start=cursor,end=cursor+count,gain=float(gain)))
                cursor+=count
        candidate=work/'candidate.mp4'
        proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size',f'{W}x{H}',
                               '-framerate',str(FPS),'-i','pipe:0','-f','f32le','-ar',str(SR),'-ac',str(channels),
                               '-i',str(work/'sound.f32'),'-c:v','libx264','-crf','16','-threads','3','-preset','fast',
                               '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(candidate)],stdin=subprocess.PIPE)
        board=None if voices else Board(work)
        experts=next(movie_frames(MOVIES['voices'],3056,1)) if voices else None
        try:
            for i,row in enumerate(rows):
                start,end=row['source_frames']; count=row['end']-row['start']; key=row['visual']
                if key=='source':
                    frames=movie_frames(MOVIES[row['source']],start,count)
                elif key=='hanoi-story':
                    # The voice begins five frames before the sewer illustration.
                    # Extend the opening street shot through the end of the superseded rat shot.
                    street = next(islice(title_frames(175),174,None))
                    frames = chain(repeat(street,5),movie_frames(MOVIES['land'],start+5,count-5))
                elif key=='experts':
                    frames=(experts for _ in range(count))
                elif key=='title':
                    frames=title_frames(count)
                elif key=='forecasts':
                    frames=movie_frames(MOVIES['land'],4584,count)
                elif key=='close':
                    # Restore the original close composition and camera movement after trimming the spoken lead-in.
                    frames=movie_frames(MOVIES['land'],5828,count)
                else:
                    frames=board.frames(key,count,rows[i+1]['visual'])
                    if key=='texting':
                        # Keep the seven-second animated phone illustration from the prior cut.
                        # Its original output positions are frames 3941 through 4150.
                        before,after=3941-start,4151-start
                        states=frames
                        def texting_with_cutaway():
                            yield from islice(states,before)
                            yield from movie_frames(MOVIES['land'],3941,210)
                            yield from islice(states,after-before,None)
                        frames=texting_with_cutaway()
                for frame in frames:
                    proc.stdin.write(frame.tobytes())
        finally:
            proc.stdin.close()
            status=proc.wait()
        if status: raise RuntimeError(f'Encoder exited {status}')
        cap=cv2.VideoCapture(str(candidate)); assert int(cap.get(cv2.CAP_PROP_FRAME_COUNT))==cursor; cap.release()
        record={'output':output.name,'frames':cursor,'fps':FPS,'duration':cursor/FPS,'rows':rows,'sha256':sha(candidate)}
        (dest/'edit-manifest.json').write_text(json.dumps(record,indent=2)+'\n')
        os.link(candidate,output)
        print(output, cursor/FPS,flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('lesson',choices=('voices','land'))
    render(parser.parse_args().lesson)
