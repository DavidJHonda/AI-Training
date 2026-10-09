#!/usr/bin/env python3
"""Inspect the encoded review candidate; transcripts are not a listening pass."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import wave
import cv2
import numpy as np
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/ai-is-different-build-2026-10-09-v13'
VIDEO = ROOT / 'Prompts/ai-is-different-v13.mp4'


def main():
    m = json.loads((OUT / 'edit-manifest.json').read_text())
    assert hashlib.sha256(VIDEO.read_bytes()).hexdigest() == m['render_sha256']
    encoded = OUT / 'encoded'
    encoded.mkdir(exist_ok=True)
    wanted = {0, m['total_frames']-1, m['close']['start_frame']}
    for board in m['boards'].values():
        wanted.add(board['src_in'])
        for state in board['states']:
            f = state['spoken_onset_source_frame']
            wanted.update([f-1, f, f+1, f+25])
    for row in m['timeline']:
        wanted.update([row['start_frame']-1, row['start_frame'], row['start_frame']+1])
    cap = cv2.VideoCapture(str(VIDEO))
    assert [cap.get(k) for k in (3,4,5)] == [1280,720,30]
    n, cells, page, dark = 0, [], 0, []
    last = None
    while True:
        ok, im = cap.read()
        if not ok:
            break
        if n in wanted:
            cv2.imwrite(str(encoded / f'{n:05d}.jpg'), im)
        if n % 60 == 0:
            cell = cv2.resize(im, (480,270))
            cv2.putText(cell, f'{n/30//60:.0f}:{n/30%60:05.2f}', (8,26),0,.7,(0,0,230),2)
            cells.append(cell)
            if len(cells) == 24:
                cv2.imwrite(str(OUT / f'encoded-sheet-{page}.jpg'),
                            cv2.vconcat([cv2.hconcat(cells[k:k+4]) for k in range(0,24,4)]))
                page += 1
                cells = []
        if im.mean() < 5:
            dark.append(n)
        last = im
        n += 1
    cap.release()
    if cells:
        while len(cells)%4:
            cells.append(np.full_like(cells[0],255))
        cv2.imwrite(str(OUT / f'encoded-sheet-{page}.jpg'),
                    cv2.vconcat([cv2.hconcat(cells[k:k+4]) for k in range(0,len(cells),4)]))
    assert n == m['total_frames'] and not dark
    close = cv2.imread(str(OUT / 'close.png'))
    h,w = close.shape[:2]
    ww = w/1.2
    hh = ww*9/16
    expected = cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),
                              (1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
    close_mae = float(np.abs(last.astype(float)-expected).mean())
    assert close_mae < 3, close_mae
    with wave.open(str(OUT / 'edited.wav')) as w:
        assert w.getnframes() == n*1600
    protected = {p:hashlib.sha256(Path(p).read_bytes()).hexdigest()==s
                 for p,s in m['protected_hashes'].items()}
    assert all(protected.values())
    board_runs = []
    for row in m['timeline']:
        if row['visual'] not in m['boards']:
            continue
        if board_runs and board_runs[-1]['end_frame']==row['start_frame'] and board_runs[-1]['board']==row['visual']:
            board_runs[-1]['end_frame'] = row['end_frame']
        else:
            board_runs.append(dict(board=row['visual'], start_frame=row['start_frame'], end_frame=row['end_frame']))
    longest = max((r['end_frame']-r['start_frame'])/30 for r in board_runs)
    args = [sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(VIDEO),
            '--outdir',str(OUT/'guard')]
    for boundary in m['boundaries']:
        args.extend(['--boundary',f"{boundary['frame']}:{boundary['label']}"])
    guard = subprocess.run(args,capture_output=True,text=True)
    (OUT/'transition-command.txt').write_text(guard.stdout+guard.stderr)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    audio = subprocess.run([ff,'-v','error','-i',str(VIDEO),'-f','null','-'],capture_output=True,text=True)
    assert audio.returncode==0 and not audio.stderr, audio.stderr
    silence = subprocess.run([ff,'-hide_banner','-i',str(VIDEO),'-af','silencedetect=noise=-40dB:d=0.12',
                              '-f','null','-'],capture_output=True,text=True)
    (OUT/'encoded-silences.txt').write_text(silence.stderr)
    excerpts = []
    for row in m['timeline']:
        if row.get('graft_audio'):
            start = max(0,row['start_frame']/30-3)
            end = min(n/30,row['end_frame']/30+3)
            name = 'rules' if 'consistency' in row['label'] else 'chef'
            p = OUT/f'{name}-join-review.mp3'
            subprocess.run([ff,'-y','-v','error','-ss',str(start),'-i',str(VIDEO),'-t',str(end-start),
                            '-vn','-c:a','libmp3lame','-q:a','2',str(p)],check=True)
            excerpts.append({'path':str(p),'output_seconds':[start,end]})
    result = dict(decoded_frames=n,duration=n/30,dimensions=[1280,720],fps=30,
                  decoder_errors=audio.stderr,final_close_mean_pixel_error=close_mae,
                  longest_unbroken_board_seconds=longest,board_runs=board_runs,
                  protected_files_unchanged=protected,corner_mark=m['corner_mark'],
                  transition_guard_exit=guard.returncode,review_audio_excerpts=excerpts,
                  listening='Not performed. Review the donor joins for narrator and cadence compatibility.')
    (OUT/'qa.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('protected_files_unchanged','corner_mark')},indent=2))


if __name__ == '__main__':
    main()
