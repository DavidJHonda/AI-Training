#!/usr/bin/env python3
"""Decode and inspect the finished v9 candidate; never modifies video sources."""
from pathlib import Path
import json, subprocess
import cv2, numpy as np
from build_does_ai_think_v9 import OUT, DEST, TOTAL, CLOSE, CUTAWAYS, BOARD_SPANS
from editspec_build import sha, readwav, writewav
import imageio_ffmpeg

def main():
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    m = json.loads((OUT/'edit-manifest.json').read_text())
    assert sha(DEST) == m['render_sha256']
    encoded = OUT/'encoded'; encoded.mkdir(exist_ok=True)
    wanted = {int(p.stem) for p in (OUT/'preview').glob('*.jpg')}
    for f in m['visual_boundaries']:
        wanted.update(range(f-2, f+3))
    cap = cv2.VideoCapture(str(DEST)); fps = cap.get(cv2.CAP_PROP_FPS)
    cells = []; samples = []; black = []; n = 0; maxrun = 0; run = 0
    while True:
        ok, im = cap.read()
        if not ok: break
        assert im.shape == (720,1280,3)
        if im.mean() < 5: black.append(n)
        if n in wanted:
            cv2.imwrite(str(encoded/f'{n:05d}.jpg'),im)
            p = OUT/'preview'/f'{n:05d}.jpg'
            if p.exists():
                ref = cv2.imread(str(p)); samples.append({'frame':n,'psnr_vs_preview_jpeg':float(cv2.PSNR(im,ref))})
        isboard = any(a <= n < z for a,z in BOARD_SPANS.values()) and not any(r['start'] <= n < r['end'] for r in CUTAWAYS)
        run = run+1 if isboard else 0; maxrun = max(run,maxrun)
        if n%120 == 0 or n==TOTAL-1:
            cell=cv2.resize(im,(480,270));cv2.putText(cell,f'{n/30:.2f}s',(8,24),cv2.FONT_HERSHEY_SIMPLEX,.7,(0,0,255),2);cells.append(cell)
        n += 1
    cap.release(); assert n==TOTAL and fps==30 and not black
    for j in range(0,len(cells),12):
        chunk=cells[j:j+12]
        while len(chunk)%3:chunk.append(np.zeros_like(chunk[0]))
        cv2.imwrite(str(OUT/f'encoded-sheet-{j//12}.jpg'),cv2.vconcat([cv2.hconcat(chunk[i:i+3]) for i in range(0,len(chunk),3)]))
    wav=OUT/'encoded.wav'
    subprocess.run([ff,'-y','-v','error','-i',str(DEST),'-vn','-ac','1','-ar','48000',str(wav)],check=True)
    a=readwav(wav); base=readwav(OUT/'base.wav'); expected=readwav(OUT/'edited.wav')
    correlations=[]
    for sec in range(1,208):
        i=sec*48000;correlations.append(float(np.corrcoef(a[i:i+48000],base[i:i+48000])[0,1]))
    assert min(correlations)>.99,min(correlations)
    donor_start=CLOSE*1600;donor_end=6408*1600
    donor_corr=float(np.corrcoef(a[donor_start:donor_end],expected[donor_start:donor_end])[0,1]);assert donor_corr>.99
    writewav(OUT/'encoded-closing-review.wav',a[round(201.5*48000):])
    r=subprocess.run([ff,'-hide_banner','-ss','207','-i',str(DEST),'-af','silencedetect=noise=-35dB:d=0.1','-f','null','-'],capture_output=True,text=True)
    (OUT/'encoded-close-silences.txt').write_text(r.stderr)
    guard=[str(Path('.video-venv/bin/python')),'scripts/video/transition_guard.py',str(DEST),'--outdir',str(OUT/'transitions')]
    for f in m['visual_boundaries']:guard.extend(['--boundary',f'{f}:edited-boundary'])
    result=subprocess.run(guard,capture_output=True,text=True);(OUT/'transition-run.txt').write_text(result.stdout+result.stderr)
    unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()};assert all(unchanged.values())
    report=dict(candidate=str(DEST),sha256=sha(DEST),frames=n,fps=fps,duration=n/fps,black_frames=black,preview_comparisons=samples,
                min_preview_psnr=min(x['psnr_vs_preview_jpeg'] for x in samples),base_audio_min_correlation=min(correlations),donor_audio_correlation=donor_corr,
                longest_unbroken_board_run_frames=maxrun,longest_unbroken_board_run_seconds=maxrun/30,transition_guard_exit=result.returncode,
                protected_unchanged=unchanged,listening_performed=False,continuous_playback_review_performed=False)
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['preview_comparisons','protected_unchanged']},indent=2))

if __name__=='__main__':main()
