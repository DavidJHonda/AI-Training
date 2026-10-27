#!/usr/bin/env python3
"""Move the approved pizza passage between two finished lesson edits.

Narrow review candidates only. Preserve the finished visual treatments, with one
additional encode; do not reconstruct the historical multi-generation assemblies.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib, json, subprocess
import cv2, imageio_ffmpeg, numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/pizza-story-move-2026-10-27'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, SR, SPF = 30, 48000, 1600
SOURCES = {
    'hallucination': ('312154b35f9c0bde4ec85c3d1b3f1f103d8fae8da7f7a7fe9c8b52fd05f953f1', 7839),
    'does-ai-think': ('5683aea0573ffc5fbe8fddaf2c6f3c2f2acfec1e8ee46913299d876c5d6f5049', 5272),
}
# Half-open frame ranges; all audio boundaries measured inside sentence gaps.
# A clean_head holds the destination scene during its existing quiet lead-in.
PLANS = {
    'hallucination': dict(version=20, spans=[
        ('hallucination', 0, 3732, None, 'Opening through real-source qualification'),
        ('hallucination', 4904, 6907, 4914, 'Checking method and Stanford application'),
        ('hallucination', 7521, 7839, None, 'Original standard close'),
    ]),
    'does-ai-think': dict(version=15, spans=[
        ('does-ai-think', 0, 2948, None, 'Opening and Chinese Room through learned-pattern explanation'),
        ('hallucination', 3732, 4598, 3747, 'Google pizza story, Reddit joke, and canonical illustration'),
        ('hallucination', 4677, 4793, None, 'The source existed, but the AI interpreted it incorrectly'),
        ('does-ai-think', 3192, 5272, 3204, 'Three comparisons, useful-AI qualification, and standard close'),
    ]),
}

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def source(slug):
    # Retained, byte-identical originals stay stable after the canonical ship.
    version = 19 if slug == 'hallucination' else 14
    return ROOT / f'Prompts/{slug}-v{version}.mp4'

def read_frame(cap, frame):
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    ok, im = cap.read()
    assert ok, frame
    return im

def build(slug):
    plan = PLANS[slug]
    dest = ROOT / f'Prompts/{slug}-v{plan["version"]}.mp4'
    assert not dest.exists(), dest
    work = OUT / slug
    work.mkdir(parents=True, exist_ok=True)
    audio = {}
    for key in {r[0] for r in plan['spans']}:
        assert sha(source(key)) == SOURCES[key][0]
        raw = subprocess.check_output([FF, '-v', 'error', '-i', str(source(key)),
            '-vn', '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'])
        audio[key] = np.frombuffer(raw, '<f4')
    parts, rows, boundaries, edges = [], [], [], []
    cursor = 0
    for key, a, b, clean, label in plan['spans']:
        part = audio[key][a*SPF:b*SPF].copy()
        assert len(part) == (b-a)*SPF
        for f, side in [(a, 'start'), (b, 'end')]:
            if f in (0, SOURCES[key][1]):
                continue
            samples = audio[key][f*SPF-480:f*SPF+480]
            db = float(20*np.log10(max(np.sqrt(np.mean(samples*samples)), 1e-12)))
            assert db < -45, (key, f, db)
            edges.append(dict(source=key, frame=f, side=side, rms_dbfs=db))
        if parts:
            # Five milliseconds entirely inside quiet handles; no added pause.
            parts[-1][-240:] *= np.linspace(1, 0, 240)
            part[:240] *= np.linspace(0, 1, 240)
            boundaries.append(dict(frame=cursor, label=label))
        parts.append(part)
        rows.append(dict(source=key, source_frames=[a,b], output_frames=[cursor,cursor+b-a],
                         clean_head=clean, label=label))
        cursor += b-a
    master = np.concatenate(parts)
    master.tofile(work/'edited.f32')
    manifest = dict(candidate=str(dest), fps=FPS, frames=cursor, duration=cursor/FPS,
        sources={k:dict(path=str(source(k)),sha256=v[0],frames=v[1]) for k,v in SOURCES.items()},
        timeline=rows, boundaries=boundaries, audio_edges=edges,
        scope='User-requested move of the pizza story from Hallucination to Does AI Think?',
        board_plan='Preserve the pizza illustration, camera and ring timing; preserve all remaining boards and closes. Clean destination-scene holds only in quiet lead-ins.',
        audio='Existing narration only. Cut complete sentences at measured quiet gaps; 5 ms fades; no inserted pauses or speech normalization.',
        limitations=['Finished approved MP4 sources receive one additional encode; pristine historical assemblies are not reconstructed.',
                      'No subjective listening or continuous playback claimed.',
                      'Review candidates only; no installation, commit, or publication.'])
    command = [FF, '-n', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
        '-s', '1280x720', '-r', str(FPS), '-i', 'pipe:0', '-f', 'f32le', '-ar', str(SR),
        '-ac', '1', '-i', str(work/'edited.f32'), '-map','0:v:0','-map','1:a:0',
        '-c:v','libx264','-threads','2','-crf','16','-preset','fast','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','192k','-movflags','+faststart',str(dest)]
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for row in rows:
            cap=cv2.VideoCapture(str(source(row['source'])))
            a,b=row['source_frames']; clean=row['clean_head']
            first=read_frame(cap,clean) if clean is not None else None
            cap.set(cv2.CAP_PROP_POS_FRAMES,a)
            for f in range(a,b):
                ok,im=cap.read(); assert ok,(slug,f)
                if clean is not None and f<clean: im=first
                proc.stdin.write(im.tobytes())
            cap.release()
            print(slug,row['label'],row['output_frames'][1],flush=True)
    finally:
        proc.stdin.close()
    assert proc.wait()==0
    assert all(sha(source(k))==v[0] for k,v in SOURCES.items())
    manifest['sha256']=sha(dest)
    (work/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

if __name__=='__main__':
    cv2.setNumThreads(2)
    OUT.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results=list(pool.map(build,PLANS))
    (OUT/'edit-manifest.json').write_text(json.dumps(results,indent=2)+'\n')
