#!/usr/bin/env python3
"""Approved opening-only visual repair, 2026-09-29. Audio packet-copied.

Two purpose-generated research scenes interrupt the long first board; the
canonical value board arrives during its introduction. All other decoded
pictures are passed through unchanged into one final H.264 encode. Original
raw rolls no longer survive; the exact, hash-locked shipped v8 is the source.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import types

import cv2
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build
from ken_burns_path import window

AUDIT = ROOT / 'video-audit/questions-matter-repair-2026-09-29-v9'
ASSETS = ROOT / 'scripts/video/assets/questions-matter-research-2026-09-29'
LIVE = ROOT / 'course-assets/questions-matter/questions-matter.mp4'
SOURCE = ROOT / 'Prompts/questions-matter-v8-source.mp4'
EXPECTED = '2c4fe76bbeb84aee589be758a27d29309945e44605df694d91de61c8d62dc039'
VALUE = ROOT / 'course-assets/questions-matter/questions-matter-value-lives.jpg'
VALUE_HASH = 'a786ac949fc17e2a376a5f9390401998994315e11f97924cf93aa00fe9f46bed'
DEST = ROOT / 'Prompts/questions-matter-v9.mp4'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, TOTAL, W, H = 30, 6674, 1280, 720
SPANS = [
    (738, 918, 'library-research', 'Student reads reference books and takes handwritten notes'),
    (1095, 1280, 'web-research', 'Student compares web sources and collects useful research'),
    (1808, 1903, 'value-introduction', 'Canonical unmarked value board during its spoken introduction'),
]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def payload_sha(path, stream='a'):
    return hashlib.sha256(subprocess.check_output([
        FF, '-v', 'error', '-i', str(path), '-map', f'0:{stream}',
        '-c', 'copy', '-f', 'data', '-',
    ])).hexdigest()


def fit_photo(path):
    im = cv2.imread(str(path))
    assert im is not None, path
    h, w = im.shape[:2]
    # Static full-bleed framing. No added camera treatment or timing changes.
    crop_w, crop_h = min(w, h * W / H), min(h, w * H / W)
    x, y = int(round((w - crop_w) / 2)), int(round((h - crop_h) / 2))
    return cv2.resize(im[y:y+int(round(crop_h)), x:x+int(round(crop_w))],
                      (W, H), interpolation=cv2.INTER_AREA)


def value_frame():
    # Same canonical asset, canvas, crop and interpolation as shipped v8.
    p, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT), VALUE, 'value-introduction')
    assert (cw, ch, ox, oy) == (1836, 1034, 118, 39)
    img = cv2.imread(str(p)); up = 3
    big = cv2.resize(img, (cw * up, ch * up), interpolation=cv2.INTER_LANCZOS4)
    x, y, ww, hh = window(cw / 2, ch / 2, float(cw), W / H, cw, ch)
    x, y, ww, hh = [int(round(v * up)) for v in (x, y, ww, hh)]
    return cv2.resize(big[y:y+hh, x:x+ww], (W, H), interpolation=cv2.INTER_AREA)


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a review candidate; use a new version.'
    assert sha(LIVE) == EXPECTED and sha(VALUE) == VALUE_HASH
    if not SOURCE.exists():
        shutil.copy2(LIVE, SOURCE)
    assert sha(SOURCE) == EXPECTED
    protected = {str(p.relative_to(ROOT)): sha(p) for p in [LIVE, SOURCE, VALUE, ASSETS/'library-research.png', ASSETS/'web-research.png']}
    frames = {'library-research': fit_photo(ASSETS/'library-research.png'),
              'web-research': fit_photo(ASSETS/'web-research.png'),
              'value-introduction': value_frame()}
    for key, frame in frames.items():
        cv2.imwrite(str(AUDIT / f'preview-{key}.jpg'), frame)
    command = [FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
               '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', str(SOURCE),
               '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264',
               '-profile:v', 'high', '-level:v', '3.1', '-crf', '16', '-preset', 'fast',
               '-threads', '4', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
               '-movflags', '+faststart', str(DEST)]
    (AUDIT/'encode-command.json').write_text(json.dumps(command, indent=2)+'\n')
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(SOURCE)); count = 0
    assert cap.get(cv2.CAP_PROP_FPS) == FPS
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            for a, b, key, _ in SPANS:
                if a <= count < b:
                    frame = frames[key]
                    break
            proc.stdin.write(frame.tobytes()); count += 1
            if count % 900 == 0:
                print(f'Encoded {count}/{TOTAL} frames', flush=True)
    finally:
        cap.release(); proc.stdin.close()
    assert proc.wait() == 0 and count == TOTAL
    check = cv2.VideoCapture(str(DEST)); decoded = 0
    while check.grab(): decoded += 1
    fps = check.get(cv2.CAP_PROP_FPS); check.release()
    assert (decoded, fps) == (TOTAL, float(FPS))
    assert payload_sha(SOURCE) == payload_sha(DEST)
    assert all(sha(ROOT/p) == h for p, h in protected.items())
    manifest = {
        'scope': 'Approved 2026-09-29 narrow visual repair, no audio or duration changes',
        'candidate': str(DEST.relative_to(ROOT)), 'candidate_sha256': sha(DEST),
        'source': str(SOURCE.relative_to(ROOT)), 'source_sha256': EXPECTED,
        'source_limitation': 'Pristine raw rolls unavailable; one encode from hash-locked finished v8',
        'protected_hashes': protected, 'total_frames': decoded, 'fps': fps,
        'duration': decoded/fps, 'audio_packets_identical': True,
        'audio_payload_sha256': payload_sha(DEST),
        'changed_spans': [{'frames': [a,b], 'seconds': [a/FPS,b/FPS], 'asset':key, 'purpose':reason} for a,b,key,reason in SPANS],
        'value_board_unmarked_frames': 95,
        'longest_single_board_seconds': 414/30,
        'longest_continuous_board_run_seconds': 700/30,
        'new_pauses': [], 'narration_changes': [],
        'unchanged': 'All source frames outside changed_spans, including prior graphics, board rings, dense cameras and standard close, passed directly to the encoder',
    }
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    boundaries = {f: f'{key}-{edge}' for a,b,key,_ in SPANS for f,edge in ((a,'in'),(b,'out'))}
    # Also check removal of the old value-board cut at 63.067 s.
    boundaries[1892] = 'former-value-entry-now-continuous'
    cmd = [sys.executable, str(ROOT/'scripts/video/transition_guard.py'), str(DEST), '--outdir', str(AUDIT/'transitions')]
    for f,label in sorted(boundaries.items()): cmd += ['--boundary',f'{f}:{label}']
    subprocess.run(cmd,check=True)
    print('COMPLETE',DEST,'frames',decoded,'audio payload identical',flush=True)


if __name__ == '__main__':
    main()
