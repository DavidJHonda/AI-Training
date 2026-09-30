#!/usr/bin/env python3
"""Verify the encoded candidate, audio identity, retained artwork and transitions."""
from pathlib import Path
import json,subprocess
import cv2,numpy as np,imageio_ffmpeg
from build_hallucination_v16 import ROOT,SRC,DEST,OUT,BOARDS,CLOSE,TOTAL,sha

ff=imageio_ffmpeg.get_ffmpeg_exe()
def audio_hash(p):
    return subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],text=True).strip()
def audio_packets(p):
    data=subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','framehash','-hash','sha256','-'],text=True)
    return [line for line in data.splitlines() if line and not line.startswith('#')]

def visual_error(actual,expected):
    delta=actual.astype(float)-expected.astype(float)
    bias=np.median(delta.reshape(-1,3),axis=0)
    return dict(mae=float(abs(delta).mean()),channel_bias=bias.tolist(),detail_mae=float(abs(delta-bias).mean()))

def main():
    manifest=json.loads((OUT/'edit-manifest.json').read_text());results={}
    results['audio_packet_sha256']={str(p):audio_hash(p) for p in [SRC,DEST]}
    assert len(set(results['audio_packet_sha256'].values()))==1,'Audio changed'
    original_packets,candidate_packets=audio_packets(SRC),audio_packets(DEST)
    results['audio_timestamps_and_packets_identical']=original_packets==candidate_packets
    results['audio_packet_count']=len(candidate_packets)
    assert results['audio_timestamps_and_packets_identical'],'Audio packet timing changed'
    results['protected_inputs_unchanged']=all(sha(Path(p))==h for p,h in manifest['protected_hashes'].items());assert results['protected_inputs_unchanged']
    run=subprocess.run([ff,'-v','error','-xerror','-i',str(DEST),'-f','null','-'],capture_output=True,text=True)
    (OUT/'decode.log').write_text(run.stderr);assert run.returncode==0,run.stderr
    cap=cv2.VideoCapture(str(DEST));src=cv2.VideoCapture(str(SRC))
    assert cap.get(cv2.CAP_PROP_FPS)==30
    assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
    previews={int(p.stem):p for p in (OUT/'preview').glob('*.png') if p.stem.isdigit()}
    (OUT/'encoded-preview').mkdir(exist_ok=True)
    measures=[];preview_mae=[];thumbs=[];n=0
    while True:
        ok,im=cap.read();ok2,original=src.read();assert ok==ok2,(n,ok,ok2)
        if not ok:break
        if n in previews:
            expected=cv2.imread(str(previews[n]));error=visual_error(im,expected);preview_mae.append(dict(frame=n,**error));assert error['mae']<5 and error['detail_mae']<2.5,(n,error)
            cv2.imwrite(str(OUT/'encoded-preview'/f'{n:05d}.png'),im)
        if n%30==0 and n<CLOSE and not any(b['start']<=n<b['end'] for b in BOARDS):
            mask=np.ones((720,1280),bool);mask[666:716,1128:1279]=False
            if 1640<=n<1861:
                for x0,y0,x1,y1 in [(207,240,623,364),(657,240,1074,364),(207,388,623,512),(657,388,1074,512)]:mask[y0:y1,x0:x1]=False
            if 2022<=n<2243:
                for x0,y0,x1,y1 in [(280,212,1002,292),(703,380,956,412),(702,438,957,472)]:mask[y0:y1,x0:x1]=False
            if 6255<=n<6574:mask[489:518,301:478]=False
            if 6550<=n<7092:mask[76:141,489:791]=False
            error=visual_error(im[mask],original[mask]);measures.append(dict(frame=n,**error));assert error['mae']<5 and error['detail_mae']<2.5,(n,error)
        if n%150==0 or n==TOTAL-1:
            tile=cv2.resize(im,(320,180));tile=cv2.copyMakeBorder(tile,24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255));cv2.putText(tile,f'{n/30:.2f}s / f{n}',(6,17),cv2.FONT_HERSHEY_SIMPLEX,.45,(20,20,20),1,cv2.LINE_AA);thumbs.append(tile)
        n+=1
    assert n==TOTAL,(n,TOTAL)
    results.update(visual_tolerance='Raw RGB MAE <5/255 and median-channel-bias-adjusted detail MAE <2.5/255; calibrated against both FFmpeg and OpenCV decode of frame1740 (same result, detail MAE0.91)',total_decoded_frames=n,fps=30,video_seconds=n/30,resolution=[1280,720],decode_errors=run.stderr,retained_visual_samples=measures,encoded_preview_mae=preview_mae)
    for k in range(0,len(thumbs),24):
        group=thumbs[k:k+24]
        while len(group)%4:group.append(np.full_like(group[0],255))
        cv2.imwrite(str(OUT/f'encoded-contact-{k//24+1}.jpg'),cv2.vconcat([cv2.hconcat(group[i:i+4]) for i in range(0,len(group),4)]))
    boundaries=[(1483,'example-exit'),(1640,'mixed-repair-start'),(1861,'mixed-exit'),(2022,'paper-start'),(2243,'why-start'),(3532,'why-exit'),(4274,'pizza-start'),(4615,'pizza-exit'),(4914,'check-start'),(6179,'check-exit'),(6255,'study-label-start'),(6550,'search-status-start'),(6574,'study-label-end'),(6820,'source-not-found'),(7092,'search-reset'),(CLOSE,'standard-close')]
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
    for f,label in boundaries:cmd+=['--boundary',f'{f}:{label}']
    guard=subprocess.run(cmd,capture_output=True,text=True)
    results['transition_guard_exit']=guard.returncode;results['transition_guard_output']=guard.stdout
    (OUT/'qa.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(dict(frames=n,audio_identical=True,protected_unchanged=results['protected_inputs_unchanged'],retained_visual_samples=len(measures),max_retained_mae=max(x['mae'] for x in measures),max_preview_mae=max(x['mae'] for x in preview_mae),transition_exit=guard.returncode,transition_output=guard.stdout),indent=2))
if __name__=='__main__':main()
