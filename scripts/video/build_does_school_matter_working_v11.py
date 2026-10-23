#!/usr/bin/env python3
"""Approved two-card working cut, ending before the pending narration pickup."""
from pathlib import Path
import json, subprocess, sys
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import Reader, sha, writewav
from build_understand_ai_opener_v12 import draw_ring
from ken_burns_path import ring_px

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/does-school-matter-working-v11-2026-10-22'
SOURCE = ROOT / 'Prompts/beyond-the-new-average-v10.mp4'
DEST = ROOT / 'Prompts/does-school-matter-v11.mp4'
ASSET = ROOT / 'course-assets/beyond-the-new-average/what-school-helps-you-build.jpg'
EXPECTED = '646b062e8b2f59d62a241e47f606c6765f1f71a698cc49d6e205b129e93d41a9'
KEEP = [(0, 3028), (3230, 3820), (4202, 4418)]
CUTAWAYS = [(3360, 3483, 'subject-microscope'), (3718, 3798, 'skills-model'), (4260, 4389, 'people-meeting')]
RECTS = {'knowledge': [40, 118, 784, 708], 'skills': [816, 118, 1560, 708]}
COLORS = {'knowledge': '#4f2fc4', 'skills': '#1652f0'}

def mapping(): return [n for a, z in KEEP for n in range(a, z)]

def pcm(path):
    return np.frombuffer(subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', '48000', '-f', 'f32le', 'pipe:1']), np.float32).copy()

def states():
    image = cv2.imread(str(ASSET)); assert image.shape[:2] == (876, 1600)
    canvas = np.full((900, 1600, 3), 255, np.uint8)
    canvas[12:888] = image
    base = cv2.resize(canvas, (1280, 720), interpolation=cv2.INTER_AREA)
    result = {'full': base}
    for key, (x0, y0, x1, y1) in RECTS.items():
        frame = base.copy(); token = COLORS[key]
        color = tuple(int(token[i:i+2], 16) for i in (5, 3, 1))
        draw_ring(frame, x0*.8, (y0+12)*.8, x1*.8, (y1+12)*.8, color, 11.2, ring_px(720))
        result[key] = frame
    return result

def state_for(n):
    if n < 3013 or any(a <= n < z for a, z, _ in CUTAWAYS): return None
    if n < 3237 or n >= 4412: return 'full'
    return 'knowledge' if n < 3510 else 'skills'

def main():
    assert sha(SOURCE) == EXPECTED
    assert not DEST.exists(), 'Use a new candidate version.'
    OUT.mkdir(parents=True, exist_ok=True); (OUT/'preview').mkdir(exist_ok=True)
    protected = {str(p): sha(p) for p in [SOURCE, ASSET, ROOT/'index.html', ROOT/'lessons/does-school-matter.md', ROOT/'course-assets/beyond-the-new-average/beyond-the-new-average.mp4', ROOT/'course-assets/beyond-the-new-average/beyond-the-new-average-close.jpg']}
    frames = mapping(); artwork = states()
    for k, im in artwork.items(): cv2.imwrite(str(OUT/'preview'/f'board-{k}.png'), im)
    audio = pcm(SOURCE); parts = [audio[a*1600:z*1600].copy() for a, z in KEEP]
    for i, part in enumerate(parts):
        if i: part[:240] *= np.linspace(0, 1, 240)
        part[-240:] *= np.linspace(1, 0, 240)
    edited = np.concatenate(parts); assert len(edited) == len(frames)*1600
    writewav(OUT/'edited.wav', edited*32768)
    source_to_output = {n:i for i,n in enumerate(frames)}
    boundaries = [(3013, 'new-board'), (3028, 'remove-four-pillars-intro'), (3618, 'skills-to-people-skills')]
    for a,z,label in CUTAWAYS:
        boundaries += [(source_to_output[a], label), (source_to_output[z], label+'-return')]
    boundaries.sort()
    plan = dict(scope='Approved working cut: two categories, current board, old takeaway and closing removed. New ending pending.', source=str(SOURCE), source_sha256=EXPECTED, candidate=str(DEST), keep_source_frames=KEEP, output_frames=len(frames), fps=30, duration=len(frames)/30, boundaries=[dict(frame=f,label=l) for f,l in boundaries], protected=protected, board=dict(path=str(ASSET), sha256=sha(ASSET), density='compact', canvas=[1600,900], image_offset=[0,12], output_scale=.8, rectangles_xyxy=RECTS, colors=COLORS, stroke_px=4, camera='Full view throughout; no zoom.', source_ring_onsets=dict(knowledge=3237,skills=3510), cutaways=CUTAWAYS), audio='Retained source audio; two cuts in measured silence, 5ms edge ramps. No new pauses or gain changes.', join_speech_gaps_seconds=[.379312,.360417], source_limitation='Original generation unavailable; single assembly from finished v10.', pending='New takeaway and complete current closing; direct listening review.', installed=False)
    (OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    p = subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    source=Reader(SOURCE)
    for out,n in enumerate(frames):
        frame=source.at(n); state=state_for(n)
        if state: frame=artwork[state]
        p.stdin.write(frame.tobytes())
        if out%900==0: print(f'Rendered {out}/{len(frames)}',flush=True)
    p.stdin.close(); assert p.wait()==0; source.c.release()
    assert all(sha(Path(p))==h for p,h in protected.items())
    plan['candidate_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    command=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
    for f,l in boundaries: command+=['--boundary',f'{f}:{l}']
    subprocess.run(command,check=True)
    print(DEST,flush=True)

if __name__=='__main__': main()
