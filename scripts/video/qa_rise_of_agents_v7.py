#!/usr/bin/env python3
"""Check encoded frames, intended audio edits and every changed boundary."""
import json, subprocess
import numpy as np, cv2
import build_rise_of_agents_v7 as b

def decoder(p):return subprocess.Popen([b.FF,'-v','error','-threads','2','-i',str(p),'-an','-f','rawvideo','-pix_fmt','bgr24','pipe:1'],stdout=subprocess.PIPE)
def pcm(p):return np.frombuffer(subprocess.check_output([b.FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','s16le','-']),dtype='<i2').astype(np.float64)

def main():
    cv2.setNumThreads(2)
    m=json.loads((b.OUT/'edit-manifest.json').read_text())
    assert b.sha(b.DEST)==m['candidate_sha256'] and b.sha(b.SRC)==b.EXPECTED
    assert b.sha(b.BOARD)==m['board_sha256']
    src,out=decoder(b.SRC),decoder(b.DEST);n=0;maes=[];board_errors=[]
    board,ring,_=b.board_frames()
    want={f for a in m['boundary_frames'] for f in range(a-2,a+3)}
    want.update(range(3885,4283,15));want.update([3800,4300,b.TOTAL-1])
    (b.OUT/'encoded-frames').mkdir(exist_ok=True)
    for f in range(b.N):
        raw=src.stdout.read(1280*720*3);assert len(raw)==1280*720*3
        if b.removed(f):continue
        enc=out.stdout.read(1280*720*3);assert len(enc)==len(raw)
        im=np.frombuffer(enc,np.uint8).reshape(720,1280,3)
        altered=3633<=f<4759 or 4899<=f<5095
        if not altered:
            original=np.frombuffer(raw,np.uint8).reshape(720,1280,3)
            maes.append(float(np.abs(im[::4,::4].astype(np.int16)-original[::4,::4]).mean()))
        if 3633<=f<3885 or 4283<=f<4759:
            ref=ring if f>=4286 else board
            board_errors.append(float(np.abs(im.astype(np.int16)-ref.astype(np.int16)).mean()))
        if n in want:cv2.imwrite(str(b.OUT/'encoded-frames'/f'{n:06d}.jpg'),im)
        n+=1
    assert not out.stdout.read() and n==b.TOTAL
    src.stdout.close();out.stdout.close();assert src.wait()==0 and out.wait()==0
    assert max(maes)<3.0,max(maes)
    assert max(board_errors)<3.0,max(board_errors)
    ref=pcm(b.OUT/'edited.wav');actual=pcm(b.DEST)[:len(ref)]
    corr=float(np.corrcoef(ref,actual)[0,1]);assert corr>.999
    original=pcm(b.SRC)[:b.N*1600];parts=[];start=0
    for lo,hi in b.CUTS:parts.append(original[start*1600:lo*1600]);start=hi
    parts.append(original[start*1600:]);unchanged=np.concatenate(parts)
    mask=np.ones(len(ref),bool)
    for lo,hi in b.CUTS:
        j=b.output_frame(lo)*1600;mask[j-96:j+96]=False
    assert np.array_equal(ref[mask],unchanged[mask])
    for lo,hi in b.CUTS:
        j=b.output_frame(lo);b.wav(b.OUT/f'encoded-join-{j}.wav',actual[(j-100)*1600:(j+140)*1600])
    result=dict(decoded_frames=n,fps=30,duration=n/30,candidate_sha256=b.sha(b.DEST),unchanged_video_frames_compared=len(maes),unchanged_video_mean_absolute_error=float(np.mean(maes)),unchanged_video_max_frame_mean_absolute_error=max(maes),canonical_board_frames_compared=len(board_errors),canonical_board_max_mean_absolute_error=max(board_errors),encoded_audio_correlation=corr,retained_PCM_exact_outside_4ms_joins=True,literal_final_frame=f'encoded-frames/{n-1:06d}.jpg',listening='Not directly auditioned; automated tests do not certify cadence.')
    (b.OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
    args=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'transitions')]
    for f,label in zip(m['boundary_frames'],m['boundary_labels']):args+=['--boundary',f'{f}:{label}']
    subprocess.run(args,check=True)

if __name__=='__main__':main()
