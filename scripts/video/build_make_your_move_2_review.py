#!/usr/bin/env python3
"""Approved Make Your Move 2 hybrid. Pristine input; review output only.

Preserve the 3:04–3:15 breather. Interleave exact lesson career cards with
five short source-graphic cutaways. Geometry is in the actual asset's pixels,
and audio edits are independent of picture cuts, inside measured room tone.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

import cv2
import imageio_ffmpeg
import numpy as np
from build_work_changes_hybrid import (
    build_canvas, crop_frame, map_camera, map_rect, project_rect,
    rounded_ring, hex_bgr, smoothstep,
)

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/make-your-move-2.mp4'
OUTPUT = ROOT / 'Prompts/make-your-move-2-patched.mp4'
AUDIT = ROOT / 'video-audit/make-your-move-2-review'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
FPS = 30
END = 9189
# Centers of measured silence: 126.0166–126.6134 / 138.5520–139.1428;
# 291.9338–292.6634 / 296.2168–296.8734;
# 299.0324–299.7750 / 301.4034–302.0051.
CUTS = ((3789, 4164), (8769, 8895), (8982, 9051))
BOARDS = {key: ROOT / f'lessons/make-your-move-{suffix}.jpg' for key, suffix in (
    ('a', '1-careers-a'), ('b', '1-careers-b'),
    ('skills', '2-skills'), ('actions', '3-actions'), ('close', '4-close'))}
BOARDS['note'] = ROOT / 'illustrations/make-your-move-note-v1.png'
COLORS = ('#4f2fc4', '#1652f0', '#0e8f86', '#a9760c')
CAREERS = ((40, 127, 525, 941), (557, 127, 1043, 941), (1075, 127, 1560, 941))
CARDS = ((40, 127, 784, 718), (816, 127, 1560, 718),
         (40, 750, 784, 1340), (816, 750, 1560, 1340))

def at(seconds):
    return round(seconds * FPS)

def mapped(frame):
    return frame - sum(max(0, min(frame, b) - a) for a, b in CUTS)

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

# (source start, end, board, column, human-responsibility onset, label)
# The exact source graphic cuts, not approximate narration times, delimit
# restoration. The electrician board starts in the cut's audio shoulder.
CAREER_SPANS = (
    (2255, 2692, 'a', 0, at(84.44), 'doctor'),
    (2807, 3091, 'a', 1, at(99.36), 'teacher'),
    (3216, 3576, 'a', 2, at(112.06), 'lawyer'),
    (4164, 4522, 'b', 0, at(148.04), 'electrician'),
    (4779, 5106, 'b', 1, at(161.88), 'designer'),
    (5106, 5432, 'b', 2, at(177.48), 'entrepreneur'),
)
CUTAWAYS = ((2692, 2807, 'doctor-patient'), (3091, 3216, 'classroom'),
            (4522, 4682, 'electrician-on-site'), (4682, 4779, 'design-variations'),
            (5432, 5537, 'founder-team'))

def make_states():
    states = []
    assets={key:cv2.imread(str(BOARDS[key])) for key in ('a','b')}
    def section_bounds(board,col,top,bottom):
        x1,_,x2,_=CAREERS[col]
        # Only vertical ink bounds are measured. Horizontal rails ALWAYS
        # remain the exact outer card boundaries, not text-derived insets.
        roi=assets[board][top:bottom,x1+28:x2-28]
        rows=np.flatnonzero(np.count_nonzero(np.min(roi,axis=2)<180,axis=1)>3)
        assert len(rows)>10
        return (x1,top+int(rows[0])-18,x2,top+int(rows[-1])+18)
    def add(start, end, board, label, rect=None, color=None, camera=None, move=0, focus=None):
        states.append(dict(start=start, end=end, board=board, label=label,
                           rect=rect, color=color, camera=camera, move=move,focus=focus))
    for start, end, board, col, human, label in CAREER_SPANS:
        x1, y1, x2, y2 = CAREERS[col]
        camera = ((x1+x2)/2, (y1+y2)/2, 1510)
        move = 0
        # Brief full-board orientation once per board, not on every return.
        if label in ('doctor', 'electrician'):
            intro_end=at(77.02 if label=='doctor' else 140.86)
            add(start, intro_end, board, label+'-orientation')
            start = intro_end
            move = 30
        elif label in ('teacher','lawyer','entrepreneur'):
            intro_end=at({'teacher':94.96,'lawyer':108.84,'entrepreneur':172.38}[label])
            add(start,intro_end,board,label+'-intro',CAREERS[col],COLORS[col],camera,
                move=30 if label=='entrepreneur' else 0)
            start=intro_end
        ai = section_bounds(board,col,490,680)
        people = section_bounds(board,col,695,933)
        add(start, human, board, label+'-ai', ai, COLORS[col], camera,move=move)
        add(human, end, board, label+'-people', people, COLORS[col], camera)
    for key, start, end, onsets in (
        ('skills', 6168, 6800, (209.10, 213.74, 219.58, 223.40)),
        ('actions', 7436, 8769, (250.26, 260.74, 271.34, 281.98))):
        points = [at(x) for x in onsets]+[end]
        add(start, points[0], key, key+'-orientation')
        for i, rect in enumerate(CARDS):
            x1,y1,x2,y2 = rect
            add(points[i], points[i+1], key, key+f'-{i+1}', rect, COLORS[i],
                ((x1+x2)/2, (y1+y2)/2, 1140),move=30)
    add(877, 1119, 'note', 'nate-and-luke-note')
    # This starts immediately after the final action, bypassing the removed
    # screen-introduction line. The close never exposes a source frame.
    add(8895, END, 'close', 'standard-close')
    return sorted(states, key=lambda x:x['start'])

def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(SOURCE))
    assert int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) == 9245
    assert abs(cap.get(cv2.CAP_PROP_FPS)-FPS) < .001
    source_hash = sha(SOURCE)
    states = make_states()
    canvases = {key: build_canvas(path) for key,path in BOARDS.items() if key!='close'}
    # Keep the complete board under every camera move. Never isolate cards.
    close = cv2.imread(str(BOARDS['close']))
    assert close.shape[:2] == (900,1600)
    boundaries = {mapped(s['start']):s['label'] for s in states}
    for a,b,label in CUTAWAYS:
        boundaries.setdefault(mapped(a), label)
        boundaries.setdefault(mapped(b), label+'-end')
    for f,label in ((1119,'note-to-original-graphics'),
                    (3576,'career-a-to-native-bridge'),(4164,'bridge-to-electrician'),
                    (5537,'preserved-breather'),(6800,'skills-to-native'),
                    (8895,'standard-close'),(9051,'closing-audio-join')):
        boundaries[mapped(f)] = label
    manifest = dict(source=str(SOURCE.relative_to(ROOT)),source_sha256=source_hash,
        output=str(OUTPUT.relative_to(ROOT)),fps=FPS,source_frame_cuts=CUTS,
        source_end_frame=END,output_frames=mapped(END),
        preserve_breather_source_frames=[5537,5861],
        cutaways=CUTAWAYS,states=states,
        card_bounds=CAREERS,grid_bounds=CARDS,
        highlight_rule='Canonical full component width; full card fits camera; constant 5px ring',
        highlight_source='card_locked_accent',
        boards={k:dict(path=str(v.relative_to(ROOT)),sha256=sha(v)) for k,v in BOARDS.items()},
        output_boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())])
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    previews = AUDIT/'highlight-previews';previews.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='make-your-move-2-',dir='/private/tmp') as tmp:
        silent = Path(tmp)/'picture.mp4'
        proc = subprocess.Popen([FFMPEG,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24',
            '-s','1280x720','-r','30','-i','-','-c:v','libx264','-crf','18',
            '-preset','medium','-pix_fmt','yuv420p',str(silent)],stdin=subprocess.PIPE)
        written=0;previous_state=None;previous_camera=None;cached=None
        for n in range(END):
            ok, frame=cap.read()
            if not ok:raise RuntimeError(f'Source ended at {n}')
            if any(a<=n<b for a,b in CUTS):continue
            state=next((s for s in states if s['start']<=n<s['end']),None)
            if state:
                if state['board']=='close':
                    i=mapped(n)-mapped(8895)
                    amount=smoothstep(min(1.,max(0.,(i-48)/149)))
                    frame=crop_frame(close,(800,450,1600+(1600/1.2-1600)*amount))
                else:
                    canvas,ox,oy,full=canvases[state['board']]
                    target=map_camera(state['camera'],ox,oy) if state['camera'] else full
                    if state is not previous_state:
                        origin=previous_camera if previous_state and previous_state['board']==state['board'] else full
                        cached=None
                    i=n-state['start'];move=state['move']
                    camera=target
                    if move and i<move:
                        amount=smoothstep(i/(move-1))
                        camera=tuple(origin[j]+(target[j]-origin[j])*amount for j in range(3))
                    if cached is None or i<=move:
                        frame=crop_frame(canvas,camera)
                        if state['rect']:
                            rect=project_rect(map_rect(state['rect'],ox,oy),camera)
                            rounded_ring(frame,rect,hex_bgr(state['color']),radius=18,thickness=5)
                        if i>=move:
                            cached=frame
                            cv2.imwrite(str(previews/(state['label']+'.jpg')),frame)
                    else:frame=cached
                    previous_camera=camera
                previous_state=state
            else:
                previous_state=None;previous_camera=None;cached=None
            proc.stdin.write(frame.tobytes());written+=1
        cap.release();proc.stdin.close()
        assert proc.wait()==0 and written==mapped(END)
        # Picture is encoded once. Audio is assembled independently with only
        # 5ms endpoint fades in the measured quiet shoulders, no breath ripple.
        ranges=((0,3789),(4164,8769),(8895,8982),(9051,END))
        graph=[]
        for i,(a,b) in enumerate(ranges):
            d=(b-a)/FPS
            graph.append(f'[1:a]atrim=start_sample={a*1470}:end_sample={b*1470},'
                f'asetpts=PTS-STARTPTS,afade=t=in:d=0.005,afade=t=out:st={d-.005:.9f}:d=0.005[a{i}]')
        graph.append(''.join(f'[a{i}]' for i in range(len(ranges)))+'concat=n=4:v=0:a=1[a]')
        subprocess.run([FFMPEG,'-y','-v','error','-i',str(silent),'-i',str(SOURCE),
            '-filter_complex',';'.join(graph),'-map','0:v','-map','[a]',
            '-c:v','copy','-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUTPUT)],check=True)
    assert sha(SOURCE)==source_hash
    check=cv2.VideoCapture(str(OUTPUT)); count=0
    while check.read()[0]:count+=1
    check.release();assert count==mapped(END),(count,mapped(END))
    manifest['verified_output_frames']=count;manifest['output_sha256']=sha(OUTPUT)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # Motion creates deliberate frame differences, not source-graphic flashes.
    # Test actual splices automatically; generate separate motion strips for
    # visual review rather than lowering flash-detection sensitivity globally.
    motion = {mapped(s['start']) for s in states if s['move']}
    for name, selected in (
        ('transitions-current', {f:l for f,l in boundaries.items() if f not in motion}),
        ('motion-review', {f:l for f,l in boundaries.items() if f in motion})):
        command=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(OUTPUT),
                 '--outdir',str(AUDIT/name)]
        for f,label in sorted(selected.items()):command += ['--boundary',f'{f}:{label}']
        subprocess.run(command,check=name=='transitions-current')
    print(f'{OUTPUT}: {count} frames, {count/FPS:.2f}s',flush=True)

if __name__=='__main__':main()
