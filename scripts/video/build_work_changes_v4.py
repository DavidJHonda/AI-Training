#!/usr/bin/env python3
"""Approved narrow visual pacing pass. Finished source only; AAC is packet-copied."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'course-assets/work-changes/work-changes.mp4'
EXPECTED = 'd020a42466b4ee9039a14dc26cc4edbe11c1508af5857f96d3c47b146b7aa68e'
ASSET = ROOT / 'scripts/video/assets/work-changes-cutaways-2026-09-30/check-reviews.png'
OUT = ROOT / 'video-audit/work-changes-cutaways-2026-09-30-v4'
DEST = ROOT / 'Prompts/work-changes-v4.mp4'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, TOTAL, W, H = 30, 9848, 1280, 720
PHOTO = (4710, 4830)  # 2:37–2:41; return before the result.
ANIMATION = (6360, 6540)  # 3:32–3:38; return for the ownership setup.
DONOR = (5436, 5582)  # 3:01.20–3:06.0667; no empty lead-in or following shot.
BOUNDARIES = {PHOTO[0]: 'assignment-to-source-review-check',
              PHOTO[1]: 'source-review-check-to-assignment',
              ANIMATION[0]: 'augmentation-to-human-judgment',
              ANIMATION[1]: 'human-judgment-to-ownership-board'}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def audio_hash(path, decoded=False):
    cmd = [FF, '-v', 'error', '-i', str(path), '-map', '0:a:0']
    cmd += ['-c:a', 'pcm_s16le'] if decoded else ['-c:a', 'copy']
    return subprocess.check_output(cmd + ['-f', 'hash', '-hash', 'sha256', '-'], text=True).strip()


def photo_frame(im, n):
    q = n / (PHOTO[1] - PHOTO[0] - 1)
    zoom = 1 + .02 * q * q * (3 - 2 * q)
    ih, iw = im.shape[:2]
    crop_w = min(iw, ih * W / H) / zoom
    crop_h = crop_w * H / W
    transform = np.float32([[crop_w / W, 0, (iw - crop_w) / 2],
                            [0, crop_h / H, (ih - crop_h) / 2]])
    return cv2.warpAffine(im, transform, (W, H),
                          flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)


def main():
    cv2.setNumThreads(2)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    assert not DEST.exists(), 'Never overwrite a candidate; choose a new version.'
    assert sha(SOURCE) == EXPECTED, 'Live source changed after evaluation.'
    protected_paths = [SOURCE, ASSET, ROOT / 'index.html', ROOT / 'lessons/work-changes.md',
                       *sorted((ROOT / 'course-assets/work-changes').glob('*.jpg'))]
    protected = {str(p): sha(p) for p in protected_paths}
    photo = cv2.imread(str(ASSET)); assert photo is not None
    cap = cv2.VideoCapture(str(SOURCE))
    assert (round(cap.get(cv2.CAP_PROP_FPS)), int(cap.get(cv2.CAP_PROP_FRAME_COUNT))) == (FPS, TOTAL)
    donor = []
    # One visual encode from the surviving finished file; audio copied without encoding.
    proc = subprocess.Popen([
        FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}',
        '-r', str(FPS), '-i', 'pipe:0', '-i', str(SOURCE), '-map', '0:v:0', '-map', '1:a:0',
        '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '3.1', '-crf', '16',
        '-preset', 'fast', '-threads', '2', '-pix_fmt', 'yuv420p', '-c:a', 'copy',
        '-movflags', '+faststart', str(DEST)], stdin=subprocess.PIPE)
    preview_frames = {x for b in BOUNDARIES for x in [b - 1, b, b + 15]}
    preview_frames |= {4770, 6420, 6510, TOTAL - 1}
    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        assert frame.shape == (H, W, 3)
        if DONOR[0] <= count < DONOR[1]:
            donor.append(frame.copy())
        if PHOTO[0] <= count < PHOTO[1]:
            frame = photo_frame(photo, count - PHOTO[0])
        elif ANIMATION[0] <= count < ANIMATION[1]:
            assert len(donor) == DONOR[1] - DONOR[0]
            # Preserve all source animation frames in order, gently slowed to six seconds.
            idx = round((count - ANIMATION[0]) * (len(donor) - 1) /
                        (ANIMATION[1] - ANIMATION[0] - 1))
            frame = donor[idx]
        if count in preview_frames:
            cv2.imwrite(str(OUT / 'preview' / f'{count:06d}.jpg'), frame)
        proc.stdin.write(frame.tobytes())
        count += 1
        if count % 1500 == 0:
            print(f'Rendered {count}/{TOTAL}', flush=True)
    cap.release(); proc.stdin.close()
    assert proc.wait() == 0 and count == TOTAL
    assert audio_hash(SOURCE) == audio_hash(DEST)
    assert audio_hash(SOURCE, True) == audio_hash(DEST, True)
    assert all(sha(p) == h for p, h in protected.items())
    m = dict(candidate=str(DEST), candidate_sha256=sha(DEST), source=str(SOURCE),
             source_sha256=EXPECTED, source_limitation='Original rolls absent; one visual encode from the verified finished live file.',
             approval='User: Build it please, following September 30 evaluation. Narrow visual pacing pass.',
             fps=FPS, total_frames=count, duration=count/FPS,
             audio_packets_identical=True, decoded_audio_identical=True,
             protected_files_unchanged=True, protected_hashes=protected,
             narration_changes=[], added_pauses=[], board_asset_changes=[],
             visual_changes=[dict(output_frames=list(PHOTO), output_seconds=[x/FPS for x in PHOTO],
                                  asset=str(ASSET), asset_sha256=sha(ASSET), treatment='2 percent eased push; hard cuts',
                                  purpose='Student compares source reviews with an AI draft before recommending a fix.'),
                             dict(output_frames=list(ANIMATION), output_seconds=[x/FPS for x in ANIMATION],
                                  donor_file=str(SOURCE), donor_sha256=EXPECTED, donor_frames=list(DONOR),
                                  treatment='Monotonic frame retiming; all source animation frames retained; hard cuts',
                                  purpose='Human judgment expands the first pass into investigation, recommendation, and presentation.')],
             boundaries=[dict(frame=f, label=s) for f,s in BOUNDARIES.items()],
             board_runs_after=dict(assignment_last=[dict(start=143.433333, end=157, seconds=13.566667),
                                                    dict(start=161, end=168.2, seconds=7.2)],
                                   two_ways=[dict(start=193.233333, end=212, seconds=18.766667),
                                             dict(start=218, end=227.066667, seconds=9.066667)],
                                   whole_video_longest_seconds=23.7,
                                   whole_video_longest_board='Four AI Strengths at Work (unchanged)'),
             retained_exceptions=['Previously approved assignment section camera',
                                  'Legacy ring widths outside narrow repair',
                                  '23.7-second Strengths board run outside narrow repair'],
             listening='No new audio edits. Full-file auditory review remains unperformed.',
             status='Candidate only; not installed, committed, or published.')
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2) + '\n')
    args = [sys.executable, str(ROOT / 'scripts/video/transition_guard.py'), str(DEST)]
    for f,label in BOUNDARIES.items():
        args += ['--boundary', f'{f}:{label}']
    subprocess.run(args + ['--outdir', str(OUT / 'transitions')], check=True)
    print('COMPLETE', DEST, flush=True)


if __name__ == '__main__':
    main()
