#!/usr/bin/env python3
"""Check the exact v13 encode and render the changed-scene review sheet."""
from pathlib import Path
import hashlib
import json

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'video-audit/transformer-repair-2026-09-29-v13'
SOURCE = ROOT/'Prompts/transformer-v12.mp4'
VIDEO = ROOT/'Prompts/transformer-v13.mp4'
START, END = 1649, 1887


def main():
    manifest = json.loads((OUT/'edit-manifest.json').read_text())
    source = cv2.VideoCapture(str(SOURCE))
    candidate = cv2.VideoCapture(str(VIDEO))
    expected = cv2.imread(str(OUT/'prepared-1740.png'))
    # Central paper content: tracking residual < .008px and observed scale ~1.
    template = expected[175:525, 165:485]
    roi_errors, unchanged_errors, cells = [], [], []
    wanted = {START, START+30, START+60, START+90, START+120, START+150, START+180, END-1}
    count = 0
    while True:
        a, sf = source.read()
        b, cf = candidate.read()
        assert a == b, 'Frame count differs'
        if not a:
            break
        if START <= count < END:
            crop = cf[175:525, 165:485]
            roi_errors.append(float(np.abs(crop.astype(np.float32)-template).mean()))
            # All source pixels outside a 3px guard around the repaired paper.
            mask = np.ones((720,1280), bool)
            mask[164:538,154:494] = False
            unchanged_errors.append(float(np.abs(sf[mask].astype(np.float32)-cf[mask]).mean()))
        if count in wanted:
            cv2.imwrite(str(OUT/f'encoded-{count}.jpg'), cf, [cv2.IMWRITE_JPEG_QUALITY,95])
            tile = cv2.resize(cf, (640,360), interpolation=cv2.INTER_AREA)
            cv2.rectangle(tile,(0,0),(640,24),(255,255,255),-1)
            cv2.putText(tile,f'f{count} / {count/30:.3f}s',(8,17),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,0),1,cv2.LINE_AA)
            cells.append(tile)
        if count == 7045:
            cv2.imwrite(str(OUT/'last-frame.jpg'),cf)
        count += 1
    source.release()
    candidate.release()
    sheet = cv2.vconcat([cv2.hconcat(cells[i:i+2]) for i in range(0,len(cells),2)])
    cv2.imwrite(str(OUT/'encoded-repair-sheet.jpg'),sheet,[cv2.IMWRITE_JPEG_QUALITY,95])
    assert count == 7046, count
    assert len(roi_errors) == END-START
    assert max(roi_errors) < 3, max(roi_errors)
    assert max(unchanged_errors) < 3, max(unchanged_errors)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == manifest['source_sha256']
    assert hashlib.sha256(VIDEO.read_bytes()).hexdigest() == manifest['candidate_sha256']
    result = dict(pass_checks=True,frames=count,fps=30,duration_seconds=count/30,
        repaired_frames_checked=len(roi_errors),max_paper_template_mae=max(roi_errors),
        max_untouched_surround_mae=max(unchanged_errors),
        source_unchanged=True,candidate_hash_verified=True,
        visual_review='Encoded frame sheet and both transition strips require inspection.',
        audio='See splice-integrity.json for copied-stream hash comparison.')
    (OUT/'encoded-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
