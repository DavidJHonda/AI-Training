#!/usr/bin/env python3
"""Verify the actual encoded narrow repair and its unchanged spans."""
import json,subprocess
import numpy as np,cv2
import build_rise_of_agents_v6 as b

def decoder(p):
    return subprocess.Popen([b.FF,'-v','error','-threads','2','-i',str(p),'-an','-f','rawvideo','-pix_fmt','bgr24','pipe:1'],stdout=subprocess.PIPE)

def main():
    cv2.setNumThreads(2)
    m=json.loads((b.OUT/'edit-manifest.json').read_text())
    assert b.sha(b.DEST)==m['candidate_sha256'] and b.sha(b.SRC)==b.EXPECTED
    source=decoder(b.SRC);output=decoder(b.DEST);n=0;maes=[];selected=[]
    boundaries=m['boundary_frames'];want={f for a in boundaries for f in range(a-2,a+3)}
    want.update(range(3885,4283,15));want.update([4400,5298])
    (b.OUT/'encoded-frames').mkdir(exist_ok=True)
    for f in range(b.N):
        raw=source.stdout.read(1280*720*3);assert len(raw)==1280*720*3
        if b.CUT_A<=f<b.CUT_B:continue
        encoded=output.stdout.read(1280*720*3);assert len(encoded)==len(raw),(f,n)
        im=np.frombuffer(encoded,np.uint8).reshape(720,1280,3)
        if f<3633 or f>=4759:
            original=np.frombuffer(raw,np.uint8).reshape(720,1280,3)
            error=float(np.abs(im[::4,::4].astype(np.int16)-original[::4,::4]).mean())
            maes.append(error)
        if n in want:cv2.imwrite(str(b.OUT/'encoded-frames'/f'{n:06d}.jpg'),im)
        n+=1
    extra=output.stdout.read();assert len(extra)==0 and n==b.TOTAL
    source.stdout.close();output.stdout.close();assert source.wait()==0 and output.wait()==0
    assert max(maes)<3.0, max(maes)
    # AAC check against the intended sample-exact assembled PCM.
    def pcm(p):
        return np.frombuffer(subprocess.check_output([b.FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','s16le','-']),dtype='<i2').astype(np.float64)
    ref=pcm(b.OUT/'edited.wav');actual=pcm(b.DEST)[:len(ref)]
    corr=float(np.corrcoef(ref,actual)[0,1]);assert corr>.999
    # Verify the board/animation repair did not alter retained original PCM.
    original=pcm(b.SRC)[:b.N*1600]
    unchanged=np.r_[original[:b.CUT_A*1600],original[b.CUT_B*1600:]]
    splice=b.CUT_A*1600
    assert np.array_equal(ref[:splice-96],unchanged[:splice-96])
    assert np.array_equal(ref[splice+96:],unchanged[splice+96:])
    result=dict(decoded_frames=n,fps=30,duration=n/30,source_sha256=b.sha(b.SRC),candidate_sha256=b.sha(b.DEST),
        unchanged_video_frames_compared=len(maes),unchanged_video_mean_absolute_error=float(np.mean(maes)),unchanged_video_max_frame_mean_absolute_error=max(maes),
        encoded_audio_correlation=corr,retained_PCM_exact_outside_4ms_join=True,
        literal_final_frame='encoded-frames/005298.jpg',listening='Not auditioned; automated checks do not certify listening.')
    (b.OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    args=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'transitions')]
    for frame,label in zip(boundaries,['corrected board in','PocketOS animation','corrected quotation board','Gemini removal audio join','goal warning']):args += ['--boundary',f'{frame}:{label}']
    subprocess.run(args,check=True)

if __name__=='__main__':main()
