#!/usr/bin/env python3
"""Encoded-candidate checks for the approved Flattery Trap repair."""
from pathlib import Path
import json
import subprocess
import sys
import wave
import cv2
import numpy as np
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_flattery_trap_v8 as build
OUT=build.OUT
FF=imageio_ffmpeg.get_ffmpeg_exe()


def main():
    global OUT
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--version',type=int,default=8);args=ap.parse_args()
    if args.version != 8:
        build.OUT=ROOT/f'video-audit/flattery-trap-repair-2026-09-29-v{args.version}'
        build.DEST=ROOT/f'Prompts/flattery-trap-v{args.version}.mp4'
        OUT=build.OUT
    manifest=json.loads((OUT/'edit-manifest.json').read_text())
    encoded=OUT/'encoded-frames';encoded.mkdir(exist_ok=True)
    points={463,475,480,500,600,689,690,867,1163,1199,1208,1364,1514,1604,
            1640,1677,1933,2027,2077,2119,2486,2487,4821,4822,4827,4828,
            4937,4938,4944,9429,9430}
    src=cv2.VideoCapture(str(build.SRC));dst=cv2.VideoCapture(str(build.DEST))
    i=j=0;errs=[];last=None
    while True:
        ok,s=src.read()
        if not ok:break
        if any(a<=i<b for a,b in build.CUTS):i+=1;continue
        ok,f=dst.read();assert ok,(i,j)
        if j in points:cv2.imwrite(str(encoded/f'f{j:05d}.jpg'),f,[cv2.IMWRITE_JPEG_QUALITY,96])
        if i%60==0 and not (463<=i<2487 or 4822<=i<4828 or 5080<=i<5083):
            errs.append({'source_frame':i,'output_frame':j,
                         'mae':float(np.abs(s.astype(np.float32)-f).mean())})
        last=f;j+=1;i+=1
    assert not dst.read()[0]
    fps=dst.get(cv2.CAP_PROP_FPS);src.release();dst.release()
    assert i==9881 and j==9431 and fps==30,(i,j,fps)
    assert max(r['mae'] for r in errs)<4, max(r['mae'] for r in errs)
    raw=subprocess.check_output([FF,'-v','error','-i',str(build.DEST),'-map','0:a',
        '-f','f32le','-acodec','pcm_f32le','-ar','48000','-ac','1','-'])
    got=np.frombuffer(raw,np.float32)
    with wave.open(str(OUT/'audio-edited.wav'),'rb') as w:
        expected=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
    assert len(got)>=len(expected)
    got=got[:len(expected)]
    rmse=float(np.sqrt(np.mean((got-expected)**2)))
    corr=float(np.corrcoef(got,expected)[0,1]);assert corr>.999 and rmse<.003,(corr,rmse)
    joins=[]
    for f in [4828,4938]:
        center=f*1600
        a=got[center-240:center+240]
        joins.append({'frame':f,'time':f/30,'peak_10ms':float(np.max(np.abs(a))),
                      'adjacent_sample_jump':float(abs(got[center]-got[center-1]))})
    silence=subprocess.run([FF,'-hide_banner','-i',str(build.DEST),'-vn','-af',
        'silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True)
    assert silence.returncode==0
    (OUT/'encoded-audio-silences.txt').write_text(silence.stderr)
    report={'decoded_source_frames':i,'decoded_output_frames':j,'fps':fps,
            'duration_seconds':j/fps,'unchanged_visual_sample_count':len(errs),
            'unchanged_visual_mae_mean':float(np.mean([r['mae'] for r in errs])),
            'unchanged_visual_mae_max':max(r['mae'] for r in errs),
            'audio_correlation_with_planned_pcm':corr,'audio_rmse':rmse,
            'audio_output_samples':len(expected),'joins':joins,
            'source_sha256_after':build.sha(build.SRC),
            'asset_sha256_after':build.sha(build.ASSET),
            'candidate_sha256':build.sha(build.DEST),
            'listening_performed':False,'continuous_motion_review_performed':False}
    assert report['source_sha256_after']==build.SOURCE_HASH
    assert report['asset_sha256_after']==build.ASSET_HASH
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'unchanged-visual-samples.json').write_text(json.dumps(errs,indent=2)+'\n')
    args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(build.DEST)]
    for b in manifest['boundaries']:args+=['--boundary',f"{b['frame']}:{b['label']}"]
    args+=['--outdir',str(OUT/'transitions')]
    result=subprocess.run(args)
    report['transition_guard_exit']=result.returncode
    # Preserve the raw guard outcome. An explicit, hash-bound manual review can
    # adjudicate only its recorded camera-motion alert, never an arbitrary fail.
    adjudicated=False
    manual_path=OUT/'manual-transition-review.json'
    if result.returncode and manual_path.exists():
        manual=json.loads(manual_path.read_text())
        guard=json.loads((OUT/'transitions/transition-guard.json').read_text())
        failed={b['frame'] for b in guard['boundaries'] if not b['pass']}
        adjudicated=(manual['candidate_sha256']==report['candidate_sha256']
                     and failed=={manual['camera_false_positive']['boundary']}
                     and manual['actual_splices_pass'])
        if adjudicated:report['manual_transition_review']=manual
    report['transition_review_accepted']=result.returncode==0 or adjudicated
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    assert report['transition_review_accepted']


if __name__=='__main__':main()
