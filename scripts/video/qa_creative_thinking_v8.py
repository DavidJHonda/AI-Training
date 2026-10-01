#!/usr/bin/env python3
"""Verify and capture the actual October Creative Thinking build."""
import json
import subprocess

import av
import cv2
import numpy as np

import build_creative_thinking_v8 as b
from editspec_build import readwav, sha


def main():
    cv2.setNumThreads(2)
    out=b.OUT/'qa';out.mkdir(exist_ok=True)
    m=json.loads((b.OUT/'edit-manifest.json').read_text())
    assert sha(b.DEST)==m['render_sha256']
    assert all(sha(p)==h for p,h in m['protected_hashes'].items())
    total=m['total_frames'];close=m['close']['start_frame']
    boundaries={x['frame']:x['label'] for x in m['boundaries']}
    wanted=set(range(0,total,120))|{total-1,close,close+47,close+197,close+198}
    for f in boundaries:wanted.update([f-1,f,f+15])
    frames={};close_widths={}
    with av.open(str(b.DEST)) as container:
        stream=container.streams.video[0];stream.codec_context.thread_count=2
        assert str(stream.average_rate)=='30'
        assert (stream.width,stream.height)==(1280,720)
        for n,frame in enumerate(container.decode(video=0)):
            if n in wanted:
                im=frame.to_ndarray(format='bgr24');frames[n]=im
                cv2.imwrite(str(out/f'frame-{n:06d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,92])
                if n in [close,close+47,close+197,close+198,total-1]:
                    mask=(im[:430].max(axis=2)<80);xs=np.where(mask.any(axis=0))[0]
                    close_widths[n]=int(xs.max()-xs.min()+1)
    assert n+1==total,(n+1,total)
    assert close_widths[close]==close_widths[close+47]
    assert close_widths[close+197]==close_widths[total-1]
    assert abs(close_widths[total-1]/close_widths[close]-1.2)<.01
    cells=[]
    for f in sorted(set(range(0,total,120))|{total-1}):
        im=cv2.resize(frames[f],(480,270));cv2.putText(im,f'{f/30:.2f}s f{f}',(8,22),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,0,220),2);cells.append(im)
    for start in range(0,len(cells),12):
        x=cells[start:start+12]
        while len(x)%3:x.append(np.zeros_like(x[0]))
        cv2.imwrite(str(out/f'overview-{start//12}.jpg'),cv2.vconcat([cv2.hconcat(x[i:i+3]) for i in range(0,len(x),3)]))
    # Exact PCM conservation away from the three declared 5 ms splice shoulders.
    source=readwav(b.OUT/'source.wav');edited=readwav(b.OUT/'edited.wav')
    expected=np.concatenate([source[:3759*1600],source[3999*1600:5514*1600],source[5934*1600:6174*1600]])
    speech_end=len(expected);delta=edited[:speech_end]-expected
    allowed=np.zeros(speech_end,bool)
    for join in m['actual_audio_joins']:
        p=join['output_frame']*1600;allowed[max(0,p-240):min(speech_end,p+240)]=True
    assert np.count_nonzero(delta[~allowed])==0
    joins=[]
    for join in m['actual_audio_joins']:
        t=join['output_frame']/30;p=join['output_frame']*1600
        x=edited[p-480:p+480]/32768
        joins.append(dict(time=t,pcm_rms_dbfs=float(20*np.log10(max(np.sqrt(np.mean(x*x)),1e-9))),pcm_max_step=float(np.max(np.abs(np.diff(x))))))
    qa=dict(candidate=str(b.DEST),sha256=sha(b.DEST),decoded_frames=n+1,duration=(n+1)/30,fps=30,
        close_pill_widths=close_widths,standard_close_scale=close_widths[total-1]/close_widths[close],
        source_audio_preserved_outside_two_cuts_and_5ms_shoulders=True,pcm_joins=joins,
        protected_sources_and_boards_unchanged=True,listening='Not performed',realtime_motion_review='Not performed; sequential sampled frames inspected')
    (out/'verification.json').write_text(json.dumps(qa,indent=2))
    import imageio_ffmpeg
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    for i,j in enumerate(joins[:2],1):
        subprocess.run([ff,'-v','error','-y','-ss',str(j['time']-3),'-i',str(b.DEST),'-t','7','-vn','-c:a','pcm_s16le',str(out/f'listen-join-{i}.wav')],check=True)
    args=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST)]
    for f,label in boundaries.items():args+=['--boundary',f'{f}:{label}']
    subprocess.run(args+['--outdir',str(out/'transitions')],check=True)
    subprocess.run([str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/ring_stroke.py'),str(b.DEST),str(out)],check=True)
    print(json.dumps(qa),flush=True)


if __name__=='__main__':main()
