#!/usr/bin/env python3
"""Verify encoded v8 timing, source protection, retained spans, and new donor audio."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/where-ai-works-best-v8-2026-09-29'
V8 = ROOT / 'Prompts/where-ai-works-best-v8.mp4'
V7 = ROOT / 'Prompts/where-ai-works-best-v7.mp4'


def pcm(path):
    return np.frombuffer(subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),
        '-v', 'error', '-i', str(path), '-vn', '-ac', '1', '-ar', '48000',
        '-f', 'f32le', '-']), np.float32)


def main():
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    assert m['total_frames'] == 6987
    assert all(m['protected_files_unchanged'].values())
    samples = set(range(0, 6987, 90))
    for board in m['boards'].values():
        samples.add(board['src_in'])
        for r in board['rings']:
            samples.add(board['src_in'] + min(r['start'] + 20, r['end'] - 1))
    samples |= {m['marks'][k] for k in ['reshape_examples','reshape_examples_return','reshape_back']}
    samples |= {6986}
    (OUT/'frames').mkdir(exist_ok=True)
    cap = cv2.VideoCapture(str(V8)); old = cv2.VideoCapture(str(V7))
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0; old_index = -1; comparisons = []; overview = []
    # Changed board picture spans in v7 time; exclude only named repairs.
    modified = [(2156,2516), (2696,2860), (4666,4875), (4875,5130), (5446,5564)]
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if count in samples:
            cv2.imwrite(str(OUT/'frames'/f'{count:05d}.jpg'), frame)
        if count % 90 == 0:
            tile = np.full((242,384,3),255,np.uint8)
            tile[26:] = cv2.resize(frame,(384,216))
            cv2.putText(tile, f'{count/30:.2f}s f{count}', (8,18),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,0),1)
            overview.append(tile)
        ref = count if count < 2156 else (count-26 if count >= 2542 else None)
        if ref is not None:
            while old_index < ref:
                ok_old, old_frame = old.read(); assert ok_old
                old_index += 1
            if count % 15 == 0 and not any(a-5 <= ref < b+5 for a,b in modified):
                comparisons.append({'v8_frame':count,'v7_frame':ref,
                    'mean_abs_diff':round(float(np.abs(frame.astype(float)-old_frame.astype(float)).mean()),4)})
        count += 1
    cap.release(); old.release()
    assert count == m['total_frames'], (count,m['total_frames'])
    for j in range(0,len(overview),24):
        page=overview[j:j+24]
        page += [np.full_like(overview[0],255)]*(24-len(page))
        cv2.imwrite(str(OUT/f'overview-{j//24+1}.jpg'),
                    np.vstack([np.hstack(page[k:k+4]) for k in range(0,24,4)]))

    a,b = pcm(V7),pcm(V8)
    # Compare the two unaffected PCM spans away from codec/seam boundaries.
    audio_checks=[]
    for label,start,end,shift in [('before_graft',0.1,71.6,0),('after_graft',84.2,231.8,26/30)]:
        x=a[round(start*48000):round(end*48000)]
        y=b[round((start+shift)*48000):round((end+shift)*48000)]
        audio_checks.append({'span':label,'correlation':float(np.corrcoef(x,y)[0,1]),
                             'rms_difference':float(np.sqrt(np.mean((x-y)**2)))})
    donor=pcm(ROOT/'Prompts/where-ai-works-best-1.mp4')
    x=donor[2257*1600+4800:2643*1600-4800] * 10**(-0.8/20)
    y=b[2156*1600+4800:2542*1600-4800]
    donor_check={'correlation':float(np.corrcoef(x,y)[0,1]),
                 'rms_difference':float(np.sqrt(np.mean((x-y)**2)))}
    report={'frames':count,'fps':fps,'duration':count/fps,
            'protected_files_unchanged':m['protected_files_unchanged'],
            'audio_unchanged_outside_repair':audio_checks,'donor_audio':donor_check,
            'retained_visual_comparisons':comparisons,
            'sha256':hashlib.sha256(V8.read_bytes()).hexdigest(),
            'listening':'Not heard; numeric checks do not certify subjective joins.'}
    (OUT/'qa.json').write_text(json.dumps(report,indent=2))
    assert all(c['correlation']>.999 for c in audio_checks), audio_checks
    assert donor_check['correlation']>.999, donor_check
    print(json.dumps({k:v for k,v in report.items() if k not in ['retained_visual_comparisons','protected_files_unchanged']},indent=2))
    print('Worst retained visual samples:',sorted(comparisons,key=lambda x:-x['mean_abs_diff'])[:5])
    cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(V8),'--outdir',str(OUT/'transitions')]
    for boundary in m['boundaries']:
        cmd += ['--boundary',str(boundary['frame'])+':'+boundary['label']]
    subprocess.run(cmd,check=True)


if __name__ == '__main__':
    main()
