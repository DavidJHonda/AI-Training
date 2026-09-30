#!/usr/bin/env python3
"""Verify the encoded narrow repair, alignment, PCM scope and edited boundaries."""
import json,subprocess
import cv2,numpy as np
import build_big_downside_v6 as config
from editspec_build import readwav,sha,writewav,Reader
b=config.b

def main():
    m=json.loads((b.OUT/'edit-manifest.json').read_text())
    assert sha(b.DEST)==m['render_sha256']
    source=readwav(b.OUT/'source.wav')[:b.N*b.SPF]
    edited=readwav(b.OUT/'edited.wav')
    a,z=round(b.AUDIO_A*b.SR),round(b.AUDIO_B*b.SR)
    baseline=np.r_[source[:a],source[z:]]
    unchanged=np.ones(len(edited),dtype=bool)
    unchanged[a-240:a+240]=False
    for _,_,start,end in config.PATCHES: unchanged[round(start*b.SR):round(end*b.SR)]=False
    assert np.array_equal(edited[unchanged],baseline[unchanged])
    assert len(edited)==b.TOTAL*b.SPF
    subprocess.run([b.Build(b.ROOT,b.SRC,b.OUT,b.DEST).ff,'-v','error','-y','-i',str(b.DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(b.OUT/'encoded.wav')],check=True)
    encoded=readwav(b.OUT/'encoded.wav')[:len(edited)]
    assert len(encoded)==len(edited)
    corr=float(np.corrcoef(encoded,edited)[0,1]);assert corr>.995,corr
    writewav(b.OUT/'callback-encoded.wav',encoded[174*b.SR:187*b.SR])
    for start,end,_,_ in config.PATCHES: writewav(b.OUT/f'encoded-{start}.wav',encoded[start*b.SR:end*b.SR])
    cap=cv2.VideoCapture(str(b.DEST));fps=cap.get(cv2.CAP_PROP_FPS);assert fps==30
    source_reader=Reader(b.SRC);i=0;diffs=[];frames=[]
    samples={b.VOICE_A,b.VOICE_B-1,b.HISTORY_A,b.HISTORY_A+30,b.HISTORY_A+90,b.HISTORY_B-1,b.TOTAL-1}
    samples.update(x+15 for x in b.ONSETS)
    samples.update([config.GUARD_A-1,config.GUARD_A,2280,config.GUARD_B-1,config.GUARD_B])
    (b.OUT/'encoded-preview').mkdir(exist_ok=True)
    while True:
        ok,im=cap.read()
        if not ok:break
        changed=(b.VOICE_A<=i<b.VOICE_B) or (b.HISTORY_A<=i<b.HISTORY_B) or (config.GUARD_A<=i<config.GUARD_B)
        if i%60==0 or i==b.TOTAL-1:
            ref=source_reader.at(i if i<b.CUT_A else i+b.DROP)
            if not changed:
                d=float(np.abs(im.astype(np.float32)-ref.astype(np.float32)).mean());diffs.append(d)
                assert d<4,(i,d)
        if i in samples:
            cv2.imwrite(str(b.OUT/'encoded-preview'/f'{i:06d}.jpg'),im);frames.append(i)
        i+=1
    cap.release();source_reader.c.release();assert i==b.TOTAL,(i,b.TOTAL)
    results=dict(decoded_frames=i,fps=fps,duration=i/fps,PCM_outside_declared_audio_repairs_exact=True,encoded_audio_correlation=corr,unchanged_visual_samples=len(diffs),max_reencode_MAD=max(diffs),encoded_previews=frames,source_hash_unchanged=sha(b.SRC)==b.EXPECTED,live_hash_unchanged=sha(b.LIVE)==b.EXPECTED,listening='Not performed; ASR and waveform checks do not certify listening.')
    (b.OUT/'qa.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2),flush=True)
    cmd=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'transitions'),'--cut-threshold','8']
    for r in m['boundaries']:cmd+=['--boundary',str(r['frame'])+':'+r['label']]
    subprocess.run(cmd,check=True)

if __name__=='__main__':main()
