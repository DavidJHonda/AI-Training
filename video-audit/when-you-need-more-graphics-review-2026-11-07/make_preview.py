"""Muted donor audition: original timing, with review labels outside the picture."""
from pathlib import Path
import json
import subprocess
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
FONT = ROOT / 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
CLIPS = [
    dict(name='Web pages become a report', roll=9, start=184.8, end=192.2,
         note='Best direct fit: Deep Research explanation at about 2:22 in the current edit.'),
    dict(name='Steps develop before an answer', roll=7, start=119.0, end=129.0,
         note='Needs simpler labels and removal of the "Verified Output" claim.'),
    dict(name='Tasks rearrange on a schedule', roll=5, start=163.5, end=170.0,
         note='Adaptation candidate: technical labels and three tracks need reworking for the lesson.'),
]

def main():
    dest = OUT / 'animated-donor-preview.mp4'
    assert not dest.exists()
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    proc = subprocess.Popen([ff, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
        '-s', '1280x840', '-r', '30', '-i', 'pipe:0', '-an', '-c:v', 'libx264',
        '-preset', 'fast', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
        str(dest)], stdin=subprocess.PIPE)
    title_font = ImageFont.truetype(str(FONT), 25)
    note_font = ImageFont.truetype(str(FONT), 18)
    frame_total = 0
    for number, clip in enumerate(CLIPS, 1):
        source = ROOT / f'Prompts/when-you-need-more-{clip["roll"]}.mp4'
        cap = cv2.VideoCapture(str(source))
        assert abs(cap.get(cv2.CAP_PROP_FPS) - 30) < .01
        first, last = round(clip['start']*30), round(clip['end']*30)
        canvas = Image.new('RGB', (1280, 840), '#14202c')
        draw = ImageDraw.Draw(canvas)
        draw.text((24, 12), f'{number}. {clip["name"]}  |  Donor {clip["roll"]}  |  {clip["start"]:.1f}-{clip["end"]:.1f}s',
                  font=title_font, fill='white')
        draw.text((24, 784), clip['note'], font=note_font, fill='white')
        draw.text((24, 812), 'MUTED SOURCE EXCERPT - native speed - review only', font=note_font, fill='#b2c2d2')
        start_out = frame_total
        for frame in range(last):
            ok, im = cap.read()
            assert ok, (source, frame)
            if frame < first:
                continue
            im = cv2.resize(im, (1280, 720))
            canvas.paste(Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)), (0, 54))
            proc.stdin.write(np.asarray(canvas).tobytes())
            frame_total += 1
        cap.release()
        clip.update(source=str(source), preview_start=start_out/30, preview_end=frame_total/30)
        print(clip['name'], flush=True)
    proc.stdin.close()
    assert proc.wait() == 0
    cap = cv2.VideoCapture(str(dest))
    decoded = 0
    while True:
        ok, im = cap.read()
        if not ok:
            break
        assert im.shape[:2] == (840,1280)
        decoded += 1
    cap.release()
    assert decoded == frame_total
    (OUT/'preview-manifest.json').write_text(json.dumps(dict(clips=CLIPS, frames=decoded,
        duration=decoded/30, audio=False, installed_video_changed=False), indent=2)+'\n')
    print(f'Validated {decoded} frames, {decoded/30:.1f} seconds', flush=True)

if __name__ == '__main__':
    main()
