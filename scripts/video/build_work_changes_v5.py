#!/usr/bin/env python3
"""V4 approved cutaways, preserving decoded source YUV instead of an RGB round trip."""
import json
import subprocess
import sys

import av
import cv2

import build_work_changes_v4 as b

b.OUT = b.ROOT / 'video-audit/work-changes-cutaways-2026-09-30-v5'
b.DEST = b.ROOT / 'Prompts/work-changes-v5.mp4'


def main():
    cv2.setNumThreads(2)
    b.OUT.mkdir(parents=True, exist_ok=True)
    (b.OUT/'preview').mkdir(exist_ok=True)
    assert not b.DEST.exists(), 'Never overwrite a review candidate.'
    assert b.sha(b.SOURCE) == b.EXPECTED
    protected={str(p):b.sha(p) for p in [b.SOURCE,b.ASSET,*sorted((b.ROOT/'course-assets/work-changes').glob('*.jpg'))]}
    photo=cv2.imread(str(b.ASSET)); assert photo is not None
    proc=subprocess.Popen([
        b.FF,'-v','error','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30',
        '-i','pipe:0','-i',str(b.SOURCE),'-map','0:v:0','-map','1:a:0',
        '-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','16',
        '-preset','fast','-threads','2','-pix_fmt','yuv420p','-c:a','copy',
        '-movflags','+faststart',str(b.DEST)],stdin=subprocess.PIPE)
    donor=[];written=0
    wants={x for f in b.BOUNDARIES for x in [f-1,f,f+15]}|{4770,6420,6510,b.TOTAL-1}
    with av.open(str(b.SOURCE)) as container:
        stream=container.streams.video[0];stream.codec_context.thread_count=2
        assert str(stream.average_rate)=='30'
        for n,frame in enumerate(container.decode(video=0)):
            assert frame.format.name=='yuv420p' and (frame.width,frame.height)==(1280,720)
            # Already yuv420p: this copies planar samples without any color conversion.
            raw=frame.to_ndarray(format='yuv420p')
            if b.DONOR[0]<=n<b.DONOR[1]:donor.append(raw.copy())
            if b.PHOTO[0]<=n<b.PHOTO[1]:
                insert=b.photo_frame(photo,n-b.PHOTO[0])
                raw=av.VideoFrame.from_ndarray(insert,format='bgr24').to_ndarray(format='yuv420p')
            elif b.ANIMATION[0]<=n<b.ANIMATION[1]:
                assert len(donor)==b.DONOR[1]-b.DONOR[0]
                idx=round((n-b.ANIMATION[0])*(len(donor)-1)/(b.ANIMATION[1]-b.ANIMATION[0]-1))
                raw=donor[idx]
            if n in wants:
                im=av.VideoFrame.from_ndarray(raw,format='yuv420p').to_ndarray(format='bgr24')
                cv2.imwrite(str(b.OUT/'preview'/f'{n:06d}.jpg'),im)
            proc.stdin.write(raw.tobytes());written+=1
            if written%1500==0:print(f'Rendered {written}/{b.TOTAL}',flush=True)
    proc.stdin.close();assert proc.wait()==0 and written==b.TOTAL
    assert b.audio_hash(b.SOURCE)==b.audio_hash(b.DEST)
    assert b.audio_hash(b.SOURCE,True)==b.audio_hash(b.DEST,True)
    assert all(b.sha(p)==h for p,h in protected.items())
    m=json.loads((b.ROOT/'video-audit/work-changes-cutaways-2026-09-30-v4/edit-manifest.json').read_text())
    m.update(candidate=str(b.DEST),candidate_sha256=b.sha(b.DEST),
             builder=str(b.ROOT/'scripts/video/build_work_changes_v5.py'),
             repair_from_v4='Retains identical creative edit. Source and donor frames stay planar YUV420P through encode; avoids cumulative RGB conversion darkening.',
             protected_hashes=protected,protected_files_unchanged=True,
             audio_packets_identical=True,decoded_audio_identical=True)
    (b.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    args=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST)]
    for f,label in b.BOUNDARIES.items():args+=['--boundary',f'{f}:{label}']
    subprocess.run(args+['--outdir',str(b.OUT/'transitions')],check=True)
    print('COMPLETE',b.DEST,flush=True)


if __name__=='__main__':main()
