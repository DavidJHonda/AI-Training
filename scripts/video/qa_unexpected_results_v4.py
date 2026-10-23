#!/usr/bin/env python3
"""Verify the encoded two-example edit, retained picture, audio joins and transitions."""
import hashlib,json,subprocess,sys,wave
import av,cv2,numpy as np
from build_unexpected_results_v4 import OUT,SRC,DEST,PREFIX,TOTAL,FPS,SR,SPF,FF,RANGES,sha


def packets(path):
    with av.open(str(path)) as c:
        v=c.streams.video[0]
        return [(p.pts,p.dts,p.duration,hashlib.sha256(bytes(p)).hexdigest()) for p in c.demux(v)
                if p.dts is not None and p.pts<PREFIX*512]


def main():
    cv2.setNumThreads(2)
    m=json.loads((OUT/'edit-manifest.json').read_text())
    assert sha(DEST)==m['candidate_sha256'] and packets(SRC)==packets(DEST)
    frames=OUT/'encoded-frames';frames.mkdir(exist_ok=True)
    wanted={PREFIX-1,PREFIX,2631,2716,2728,2900,3160,3356,3370,3611,3629,3670,m['frames']-1}
    wanted.update(range(0,m['frames'],180))
    for b in m['boundaries']:wanted.update([b['frame']-1,b['frame'],b['frame']+1])
    source=av.open(str(SRC));source.streams.video[0].codec_context.thread_count=2
    native=iter(source.decode(video=0));source_index=-1;ref=None
    errors=[];pts=[];n=0
    with av.open(str(DEST)) as c:
        v=c.streams.video[0];v.codec_context.thread_count=2
        assert v.average_rate==FPS and (v.width,v.height)==(1280,720)
        for n,decoded in enumerate(c.decode(video=0)):
            frame=decoded.to_ndarray(format='bgr24');pts.append(decoded.pts)
            segment=next(s for s in m['segments'] if s['output_frames'][0]<=n<s['output_frames'][1])
            f=segment['source_frames'][0]+n-segment['output_frames'][0]
            while source_index<f:
                ref=next(native).to_ndarray(format='bgr24');source_index+=1
            if n<PREFIX:assert np.array_equal(frame,ref),n
            elif f<2631 or 3086<=f<3389 or f>=5813:
                error=float(cv2.absdiff(frame,ref).mean());assert error<5,(n,error);errors.append(error)
            if n in wanted:cv2.imwrite(str(frames/f'{n:05d}.jpg'),frame)
    source.close();assert n+1==m['frames'] and set(np.diff(pts))=={512}
    def audio(path):
        return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(path),'-map','0:a:0',
            '-f','f32le','-ac','1','-ar',str(SR),'-']),np.float32)
    encoded=audio(DEST)
    with wave.open(str(OUT/'audio-edited.wav')) as w:
        expected=np.frombuffer(w.readframes(w.getnframes()),'<i2').astype(np.float32)/32768
    assert 0<=len(encoded)-len(expected)<1024
    joins=[]
    for s in m['segments'][1:]:
        n=s['output_frames'][0];lo,hi=n*SPF-SR,n*SPF+SR
        corr=float(np.corrcoef(encoded[lo:hi],expected[lo:hi])[0,1]);assert corr>.99,(n,corr)
        joins.append(dict(output_frame=n,output_seconds=n/FPS,correlation=corr))
    assert all(sha(p)==h for p,h in m['protected_hashes'].items())
    report=dict(candidate_sha256=sha(DEST),decoded_frames=m['frames'],fps=FPS,pts_delta=[512],
        opening_frames_packet_and_pixel_identical=PREFIX,retained_picture_frames_compared=len(errors),
        retained_picture_max_mean_absolute_error=max(errors),encoded_audio_join_correlations=joins,
        source_audio_cut_edges=m['source_audio_cut_edges'],protected_files_unchanged=True,
        direct_listening_performed=False,continuous_audiovisual_playback_performed=False)
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    cmd=[sys.executable,str(OUT.parents[1]/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
    for f in sorted({b['frame'] for b in m['boundaries']}):cmd+=['--boundary',f'{f}:edited-transition']
    subprocess.run(cmd,check=True)

if __name__=='__main__':main()
