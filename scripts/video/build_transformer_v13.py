#!/usr/bin/env python3
"""Approved narrow repair: replace the brain's gibberish paper, audio copied.

Uses the stable v12 candidate, an ImageGen paper edit, and source-frame tracking.
Nothing is installed in course-assets or published by this script.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/transformer-v12.mp4'
EXPECTED = '0a972235e9fcaf619d8db34715243a7812a87569091e87092f866666586376b5'
OUT = ROOT / 'video-audit/transformer-repair-2026-09-29-v13'
ASSET = ROOT / 'scripts/video/assets/transformer-v13/brain-paper-imagegen.png'
DEST = ROOT / 'Prompts/transformer-v13.mp4'
START, END, REF = 1649, 1887, 1740
FPS, COUNT = 30, 7046


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    assert sha(SOURCE) == EXPECTED
    OUT.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(SOURCE))
    frames = []
    for i in range(END):
        ok, frame = cap.read()
        assert ok, i
        if i >= START:
            frames.append(frame)
    cap.release()
    reference = frames[REF - START]
    gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    feature_mask = np.zeros(gray.shape, np.uint8)
    feature_mask[40:690, 50:600] = 255
    points = cv2.goodFeaturesToTrack(gray, 500, .02, 8, mask=feature_mask)

    generated = cv2.imread(str(ASSET))
    assert generated is not None
    # Interior of ImageGen's paper, measured on its 1672 x 941 composition.
    # The original paper outline/shadow and all surrounding artwork remain source.
    gh, gw = generated.shape[:2]
    x1, y1, x2, y2 = [round(v * s) for v, s in zip(
        [204/1672, 218/941, 642/1672, 705/941], [gw, gh, gw, gh])]
    patch = cv2.resize(generated[y1:y2, x1:x2], (332, 366), interpolation=cv2.INTER_LANCZOS4)
    layer = np.zeros_like(reference)
    layer[168:534, 158:490] = patch
    alpha = np.zeros(gray.shape, np.float32)
    alpha[168:534, 158:490] = 1
    # Feather inward only, so no original writing can leak through the interior.
    alpha = np.minimum(cv2.distanceTransform((alpha > 0).astype(np.uint8), cv2.DIST_L2, 3) / 2, 1)
    repaired, tracking = [], []
    for local, frame in enumerate(frames):
        current = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        q, status, _ = cv2.calcOpticalFlowPyrLK(gray, current, points, None,
            winSize=(21, 21), maxLevel=3,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 40, .001))
        good = status.ravel().astype(bool)
        p = points[good].reshape(-1, 2)
        q = q[good].reshape(-1, 2)
        matrix, inliers = cv2.estimateAffinePartial2D(p, q, method=cv2.RANSAC,
            ransacReprojThreshold=.8, maxIters=2000, confidence=.999, refineIters=20)
        assert matrix is not None
        fraction = float(inliers.mean())
        assert fraction > .8, (local, fraction)
        scale = float(np.hypot(matrix[0, 0], matrix[0, 1]))
        assert .95 < scale < 1.05, scale
        projected = cv2.transform(p.reshape(-1, 1, 2), matrix).reshape(-1, 2)
        residual = float(np.median(np.linalg.norm(projected-q, axis=1)))
        assert residual < .5, (local, residual)
        warped = cv2.warpAffine(layer, matrix, (1280, 720), flags=cv2.INTER_LINEAR)
        mask = cv2.warpAffine(alpha, matrix, (1280, 720), flags=cv2.INTER_LINEAR)
        result = np.rint(warped * mask[..., None] + frame * (1-mask[..., None])).astype(np.uint8)
        assert np.array_equal(result[mask == 0], frame[mask == 0])
        repaired.append(result)
        tracking.append({'frame': START+local, 'affine': matrix.tolist(),
                         'inlier_fraction': fraction, 'median_residual_px': residual,
                         'scale': scale})
    for f in [START, START+30, REF, END-1]:
        cv2.imwrite(str(OUT/f'prepared-{f}.png'), repaired[f-START])
    manifest = dict(source=str(SOURCE), source_sha256=EXPECTED,
        generated_asset=str(ASSET), asset_sha256=sha(ASSET), output=str(DEST),
        approval='User: build it, following the one-scene visual repair recommendation.',
        scope='Narrow paper-interior repair. Source motion retained; audio stream copied.',
        source_limitation='Pristine raw roll unavailable. Stable finished v12 is the source; video receives one additional encode.',
        start_frame=START, end_frame=END, start_seconds=START/FPS, end_seconds=END/FPS,
        fps=FPS, frame_count=COUNT, expected_duration=COUNT/FPS,
        patch_rectangle_reference=[158,168,490,534], reference_frame=REF,
        tracking=tracking, boards='Unchanged', pauses='None', narration_changes='None')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return repaired, manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare-only', action='store_true')
    args = parser.parse_args()
    repaired, manifest = prepare()
    if args.prepare_only:
        print('Prepared all 238 repaired frames and tracked paper; no MP4 built.', flush=True)
        return
    assert not DEST.exists(), f'Do not overwrite a candidate: {DEST}'
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ff, '-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
        '-r','30','-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0',
        '-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',
        '-c:a','copy','-movflags','+faststart',str(DEST)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(SOURCE))
    count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if START <= count < END:
            frame = repaired[count-START]
        process.stdin.write(frame.tobytes())
        count += 1
        if count % 2000 == 0:
            print(f'Rendered {count}/{COUNT}', flush=True)
    cap.release()
    process.stdin.close()
    assert process.wait() == 0
    assert count == COUNT
    assert sha(SOURCE) == EXPECTED
    manifest['candidate_sha256'] = sha(DEST)
    manifest['encode_command'] = command
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(str(DEST), flush=True)


if __name__ == '__main__':
    main()
