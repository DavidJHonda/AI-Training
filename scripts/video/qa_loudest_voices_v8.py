#!/usr/bin/env python3
"""Verify the actual encoded review candidate and emit visual evidence."""
import hashlib
import itertools
import json
import subprocess
import sys
import av
import cv2
import numpy as np
from build_loudest_voices_v8 import ROOT,OUT,SOURCE,DEST,SPANS,EVENTS,SUMMARY,FF,sha,frames,Boards

def packets(path,kind):
    with av.open(str(path)) as c:
        stream=next(s for s in c.streams if s.type==kind)
        return [(p.pts,p.dts,p.duration,str(p.time_base),hashlib.sha256(bytes(p)).hexdigest())
                for p in c.demux(stream) if p.dts is not None]

def main():
    cv2.setNumThreads(1)
    audio_a,audio_b=packets(SOURCE,'audio'),packets(DEST,'audio')
    assert audio_a==audio_b,'AAC bytes/timestamps changed'
    va,vb=packets(SOURCE,'video'),packets(DEST,'video')
    def untouched(rows):
        return [p for p in rows if not any(a<=p[0]/512<b for a,b,_ in SPANS)]
    assert untouched(va)==untouched(vb),'Untouched video packets changed'
    for path in (SOURCE,DEST):
        with av.open(str(path)) as c:
            v=c.streams.video[0]
            assert v.average_rate==30 and v.width==1280 and v.height==720
    selected={0,712,872,3611,3629,3630,4142,4482,6069,6120,6270,6360,6440,6495,6501,6883}
    selected.update(a+30 for a,_,_ in EVENTS)
    selected.update(a+12 for a,_ in SUMMARY)
    selected.update(f for a,b,_ in SPANS for f in [a-1,a,a+1,b-1,b])
    images=OUT/'encoded';images.mkdir(exist_ok=True)
    unchanged=0;edited=0;checks=[]
    boards=Boards()
    for pair in itertools.zip_longest(frames(SOURCE),frames(DEST)):
        first,second=pair
        assert first is not None and second is not None
        n,a=first;nn,b=second;assert n==nn
        changed=any(lo<=n<hi for lo,hi,_ in SPANS)
        if not changed:
            assert np.array_equal(a,b),f'Unchanged frame differs: {n}'
            unchanged+=1
        else:edited+=1
        if n in selected:
            cv2.imwrite(str(images/f'frame-{n:05}.png'),b)
            if any(lo<=n<hi for lo,hi,name in SPANS if name.startswith('experts')):
                psnr=cv2.PSNR(boards.render(n),b)
                # CRF 18 and YUV420 chroma subsampling soften saturated tiny
                # text edges; use this only to catch a wrong scene, then
                # inspect the saved encoded state for actual visual quality.
                assert psnr>30,('Board rendered incorrectly',n,psnr)
                checks.append(dict(frame=n,render_psnr_db=psnr))
    assert n+1==6884
    # AAC identity is already a stronger check than a listening comparison;
    # decode too, to catch container/decoder differences.
    audio=[]
    for path in (SOURCE,DEST):
        raw=subprocess.check_output([FF,'-v','error','-i',str(path),'-map','0:a:0','-f','s16le','-'])
        audio.append(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    assert audio[0]==audio[1]
    manifest=json.loads((OUT/'edit-manifest.json').read_text())
    boundaries={r['frame']:r['label'] for r in manifest['boundaries']}
    boundaries.update({a:f'expert-{k}-section-{s}' for a,k,s in EVENTS})
    boundaries[3611]='return-to-full-board-synthesis'
    boundaries.update({a:'synthesis-highlight-'+','.join(map(str,ks)) for a,ks in SUMMARY})
    # Set OpenCV to one thread inside the existing transition checker.
    cmd=[sys.executable,'-c',
         'import cv2,runpy;cv2.setNumThreads(1);runpy.run_path("scripts/video/transition_guard.py",run_name="__main__")',
         str(DEST),'--outdir',str(OUT/'transitions')]
    for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    (OUT/'transition-command.log').write_text(result.stdout+result.stderr)
    assert result.returncode==0,result.stdout+result.stderr
    report=dict(candidate=str(DEST),candidate_sha256=sha(DEST),frames=n+1,fps=30,duration_seconds=(n+1)/30,
                edited_span_frames=edited,unaffected_frames_pixel_identical=unchanged,
                audio_packets_identical=True,audio_packet_count=len(audio_a),decoded_audio=audio[0],
                untouched_video_packets_identical=True,board_render_checks=checks,
                transition_boundaries=boundaries,transition_guard_passed=True,
                encoded_evidence_frames=sorted(selected),direct_listening_performed=False,
                pronunciation='David confirmed correct; unchanged audio.')
    (OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['board_render_checks','transition_boundaries','encoded_evidence_frames']},indent=2))

if __name__=='__main__':main()
