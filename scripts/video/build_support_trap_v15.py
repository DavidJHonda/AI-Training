#!/usr/bin/env python3
"""Approved recap deletion from the hash-pinned installed v14; review only."""
from pathlib import Path
import hashlib, json, subprocess
import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/support-trap-cut-plan-2026-10-27'
SOURCE = ROOT / 'Prompts/support-trap-v14.mp4'
DEST = ROOT / 'Prompts/support-trap-v15.mp4'
INSTALLED = ROOT / 'course-assets/support-trap/support-trap.mp4'
SHA = 'a465ed033c1139dbf61fb5404826d3f0d9c955c58b295ef1abe4977d7151d88e'
SPANS = [(0, 1721), (1849, 8159)]
FPS, SR, SPF = 30, 48000, 1600
FF = imageio_ffmpeg.get_ffmpeg_exe()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def pcm(path):
    return np.frombuffer(subprocess.check_output([
        FF, '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', str(SR),
        '-f', 'f32le', '-']), dtype='<f4')

def main():
    assert not DEST.exists(), 'Never overwrite a review candidate'
    assert sha(SOURCE) == sha(INSTALLED) == SHA
    OUT.mkdir(parents=True, exist_ok=True)
    protected = {str(p): sha(p) for p in [INSTALLED, ROOT/'index.html',
        *list((ROOT/'course-assets/support-trap').glob('*.jpg'))]}
    original = pcm(SOURCE)
    parts = [original[a*SPF:b*SPF].copy() for a,b in SPANS]
    # Fade only five milliseconds inside the measured quiet handles.
    ramp = np.linspace(0, 1, 240)
    parts[0][-240:] *= 1-ramp
    parts[1][:240] *= ramp
    edited = np.concatenate(parts)
    audio = OUT/'v15-edited-audio.f32'
    edited.tofile(audio)
    assert len(edited) == 8031*SPF
    prior = json.loads((ROOT/'video-audit/support-trap-tighten-2026-09-30-v13/edit-manifest.json').read_text())
    boundaries = {1721: 'Approved-recap-cut-to-comparison-board'}
    for item in prior['boundaries']:
        f = item['frame']
        if 1721 <= f < 1849:
            continue
        if f >= 1849:
            f -= 128
        boundaries[f] = item['label']
    for f in [3506,3572,3658,3746,3776,3848,3886]:
        boundaries[f-128] = 'Retained-v14-preparation-state'
    manifest = dict(source=str(SOURCE), source_sha256=SHA, candidate=str(DEST),
        approval='User: Build it please. Approved plan in this chat, October 27, 2026.',
        scope='Narrow removal of the repeated lunch-outcome recap; review candidate only.',
        source_frames=8159, output_frames=8031, fps=FPS, duration=267.7,
        saved_seconds=128/FPS, retained_source_frames=SPANS,
        cut_source_frames=[1721,1849], output_join_frame=1721,
        removed_words='but only one of these replies alters your day. The other cannot act.',
        boundaries=[dict(frame=f,label=label) for f,label in sorted(boundaries.items())],
        audio='Source mono audio, only approved deletion and 5 ms quiet-edge fades; no new pauses or gain changes.',
        source_limitation='Pristine assembled PCM was cleaned after earlier shipping. Hash-verified finished v14 used as approved fallback, with one additional H.264/AAC encode.',
        protected_files=protected,
        board_plan='Existing comparison board/highlights/camera retained. Empty-chair drawing shortened with narration. All later boards, v14 preparation insert, story, safety and close retained.',
        listening='Not performed; transcript/waveform checks do not certify perceptual audio quality.')
    (OUT/'v15-edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    cap = cv2.VideoCapture(str(SOURCE))
    assert cap.get(cv2.CAP_PROP_FPS) == FPS
    with (OUT/'v15-encode.log').open('w') as log:
        process = subprocess.Popen([FF,'-n','-v','error','-f','rawvideo','-pix_fmt','bgr24',
            '-s','1280x720','-r','30','-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1',
            '-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','2',
            '-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
            '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE,stderr=log)
        written = 0
        try:
            for a,b in SPANS:
                cap.set(cv2.CAP_PROP_POS_FRAMES,a)
                for f in range(a,b):
                    ok,im = cap.read()
                    assert ok,f
                    process.stdin.write(im.tobytes())
                    written += 1
                    if written % 1500 == 0:
                        print('Rendered',written,'/ 8031',flush=True)
        finally:
            cap.release()
            process.stdin.close()
        assert process.wait() == 0
    assert written == 8031
    assert all(sha(Path(p)) == h for p,h in protected.items())
    manifest.update(candidate_sha256=sha(DEST),protected_files_unchanged=True)
    (OUT/'v15-edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Built',DEST,flush=True)

if __name__ == '__main__':
    main()
