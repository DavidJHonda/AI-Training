#!/usr/bin/env python3
"""Build the five approved Support Trap deletions as a new review candidate."""
from pathlib import Path
import hashlib
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/support-trap-trim-v16-2026-11-02'
SOURCE = ROOT / 'Prompts/support-trap-v15.mp4'
INSTALLED = ROOT / 'course-assets/support-trap/support-trap.mp4'
DEST = ROOT / 'Prompts/support-trap-v16.mp4'
SHA = '70e787efac28dff7efa2fd5b439f30e4883eeb8e8edb59a34a4d955edd562b0a'
FPS, SR, SPF = 30, 48000, 1600
FF = imageio_ffmpeg.get_ffmpeg_exe()
CUTS = [
    (1839, 2508, 'Preparation preview and repeated limitations'),
    (4121, 4352, 'Repeated warning about polishing messages'),
    (5204, 5359, 'Abstract digital-space explanation'),
    (6918, 7133, 'Repeated chatbot limitations in safety section'),
    (7455, 7708, 'Repeated directive before closing'),
]
SOURCE_FRAMES = 8031
SPANS = list(zip([0] + [b for a, b, _ in CUTS], [a for a, b, _ in CUTS] + [SOURCE_FRAMES]))
FRAMES = sum(b-a for a, b in SPANS)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pcm(path):
    return np.frombuffer(subprocess.check_output([
        FF, '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', str(SR),
        '-f', 'f32le', '-']), dtype='<f4')


def output_frame(frame):
    offset = 0
    for a, b in SPANS:
        if a <= frame < b:
            return offset + frame-a
        offset += b-a
    return None


def main():
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SOURCE) == sha(INSTALLED) == SHA
    OUT.mkdir(parents=True, exist_ok=True)
    protected = {str(p): sha(p) for p in [INSTALLED, SOURCE, ROOT/'index.html',
        ROOT/'lessons/support-trap.md', ROOT/'course-assets/manifest.json',
        *list((ROOT/'course-assets/support-trap').glob('*.jpg'))]}
    original = pcm(SOURCE)
    parts = [original[a*SPF:b*SPF].copy() for a, b in SPANS]
    ramp = np.linspace(0, 1, 240)
    for i, part in enumerate(parts):
        if i:
            part[:240] *= ramp
        if i < len(parts)-1:
            part[-240:] *= 1-ramp
    audio = OUT/'edited-audio.f32'
    np.concatenate(parts).tofile(audio)
    handles = []
    for a, b, label in CUTS:
        for f in (a, b):
            samples = original[f*SPF-240:f*SPF+240]
            db = float(20*np.log10(np.sqrt(np.mean(samples*samples))+1e-12))
            assert db < -45, (f, db)
            handles.append(dict(source_frame=f, dbfs=db))
    prior = json.loads((ROOT/'video-audit/support-trap-cut-plan-2026-10-27/v15-edit-manifest.json').read_text())
    boundaries = {}
    for row in prior['boundaries']:
        if row['frame'] == 1832:
            continue  # Seven-frame phone flash is covered by the comparison board.
        f = output_frame(row['frame'])
        if f is not None and f > 0:
            boundaries[f] = row['label']
    joins = []
    for a, b, label in CUTS:
        f = output_frame(b)
        boundaries[f] = label
        joins.append(dict(frame=f, seconds=f/FPS, label=label))
    manifest = dict(source=str(SOURCE), source_sha256=SHA, candidate=str(DEST),
        authorization='User approved five suggested deletions, explicitly retained the 3:25–3:33 safety-board transition, then requested "Build it please."',
        source_frames=SOURCE_FRAMES, frames=FRAMES, fps=FPS,
        duration_seconds=FRAMES/FPS, saved_seconds=(SOURCE_FRAMES-FRAMES)/FPS,
        retained_source_frames=SPANS,
        cuts=[dict(source_frames=[a,b], source_seconds=[a/FPS,b/FPS], label=label) for a,b,label in CUTS],
        boundaries=[dict(frame=f,label=label) for f,label in sorted(boundaries.items())],
        audio_joins=joins, quiet_handles=handles,
        picture_repairs=[dict(source_frames=[1832,1839], hold_source_frame=1831,
            reason='Cover a seven-frame phone illustration flash after the retained definition; retain complete speech tail.'),
            dict(source_frames=[5359,5366],hold_source_frame=5203,
            reason='Hold the previous diagram state across the join until the family illustration, avoiding a seven-frame fragment of the deleted explanation.')],
        protected=protected,
        retained_safety_board_intro_source_seconds=[205.05,212.97],
        audio='Retained audio in order, five-millisecond fades inside quiet shoulders only; no added pauses, gain changes, or new words.',
        source_limitation='Finished hash-verified v15 used as source; one additional H.264/AAC encode. Original raw rolls remain available.',
        scope='Review candidate only; no installation or publishing.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    cap = cv2.VideoCapture(str(SOURCE))
    assert cap.get(cv2.CAP_PROP_FPS) == FPS
    cap.set(cv2.CAP_PROP_POS_FRAMES,1831)
    ok, board = cap.read()
    assert ok
    cap.set(cv2.CAP_PROP_POS_FRAMES,5203)
    ok, diagram = cap.read()
    assert ok
    with (OUT/'encode.log').open('w') as log:
        process = subprocess.Popen([FF,'-n','-v','error','-f','rawvideo','-pix_fmt','bgr24',
            '-s','1280x720','-r',str(FPS),'-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1',
            '-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','2',
            '-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
            '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE,stderr=log)
        written = 0
        try:
            for a,b in SPANS:
                cap.set(cv2.CAP_PROP_POS_FRAMES,a)
                for f in range(a,b):
                    ok, im = cap.read()
                    assert ok, f
                    if 1832 <= f < 1839:
                        im = board
                    if 5359 <= f < 5366:
                        im = diagram
                    process.stdin.write(im.tobytes())
                    written += 1
                    if written % 1500 == 0:
                        print('Rendered',written,'/',FRAMES,flush=True)
        finally:
            cap.release()
            process.stdin.close()
        assert process.wait() == 0
    assert written == FRAMES
    assert all(sha(p) == h for p,h in protected.items())
    manifest.update(candidate_sha256=sha(DEST), protected_files_unchanged=True)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Built',DEST,'duration',FRAMES/FPS,flush=True)


if __name__ == '__main__':
    main()
