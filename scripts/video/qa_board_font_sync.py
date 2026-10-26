#!/usr/bin/env python3
"""Verify board-only video candidates against frozen source and canonical renders."""
import argparse
import hashlib
import itertools
import json
import subprocess
import sys

import av
import cv2
import numpy as np

from build_board_font_sync import CONFIG, OUT, ROOT, FF, paths, prepare, render, inside, boundaries, sha

def packets(path,kind):
    with av.open(str(path)) as source:
        stream=next(s for s in source.streams if s.type==kind)
        return [(p.pts,p.dts,p.duration,str(p.time_base),hashlib.sha256(bytes(p)).hexdigest())
                for p in source.demux(stream) if p.dts is not None]

def frames(path):
    with av.open(str(path)) as source:
        source.streams.video[0].codec_context.thread_count=1
        yield from source.decode(video=0)

def qa(slug, reviewed_motion=False):
    cfg=CONFIG[slug];src,dst=paths(slug);boards=prepare(slug);out=OUT/slug
    evidence=out/'encoded';evidence.mkdir(exist_ok=True)
    aa,ab=packets(src,'audio'),packets(dst,'audio');assert aa==ab,'Audio packets/timestamps differ'
    def untouched(rows):return [p for p in rows if not inside(p[0]/512,cfg['encode'])]
    assert untouched(packets(src,'video'))==untouched(packets(dst,'video')),'Untouched video packets differ'
    for path in (src,dst):
        with av.open(str(path)) as source:
            v=source.streams.video[0]
            assert v.average_rate==30 and v.width==1280 and v.height==720
    joins=boundaries(slug,boards)
    selected={0,cfg['frames']-1}
    selected.update(f+d for f in joins for d in (-1,0,1,15))
    exact=new=handles=0;min_render=min_handle=100
    for n,(before,after) in enumerate(itertools.zip_longest(frames(src),frames(dst))):
        assert before is not None and after is not None,'Frame count mismatch'
        assert before.pts*before.time_base==after.pts*after.time_base,'Frame timing mismatch'
        a=before.to_ndarray(format='yuv420p');b=after.to_ndarray(format='yuv420p')
        if not inside(n,cfg['encode']):
            assert np.array_equal(a,b),f'Untouched frame differs: {n}'
            exact+=1
        else:
            expected=render(slug,boards,n)
            if expected is None:
                score=cv2.PSNR(a,b);min_handle=min(score,min_handle);handles+=1
                assert score>38,(n,score,'Unchanged handle')
            else:
                score=cv2.PSNR(expected,after.to_ndarray(format='bgr24'));min_render=min(score,min_render);new+=1
                assert score>32,(n,score,'Incorrect board render')
        if n in selected:cv2.imwrite(str(evidence/f'{n:05}.jpg'),after.to_ndarray(format='bgr24'),[cv2.IMWRITE_JPEG_QUALITY,96])
    assert n+1==cfg['frames']
    decoded=[]
    for path in (src,dst):
        raw=subprocess.check_output([FF,'-v','error','-i',str(path),'-map','0:a:0','-f','s16le','-'])
        decoded.append(dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    assert decoded[0]==decoded[1],'Decoded audio differs'
    cmd=[sys.executable,'-c','import cv2,runpy;cv2.setNumThreads(1);runpy.run_path("scripts/video/transition_guard.py",run_name="__main__")',str(dst),'--outdir',str(out/'transitions')]
    for f,label in sorted(joins.items()):cmd+=['--boundary',f'{f}:{label}']
    result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    (out/'transition-command.log').write_text(result.stdout+result.stderr)
    guard=json.loads((out/'transitions/transition-guard.json').read_text())
    flags=[b['frame'] for b in guard['boundaries'] if not b['pass']]
    if flags and reviewed_motion:
        assert slug=='wheres-the-line',result.stdout+result.stderr
        assert flags==[4569,4907,5132,5408,5681],flags
        # These exact strips were inspected: continuous original camera moves, no visual islands.
        assert all(render(slug,boards,f) is not None for f in flags)
    if not flags:assert result.returncode==0,result.stdout+result.stderr
    manifest=json.loads((out/'manifest.json').read_text())
    assert all(sha(p)==h for p,h in manifest['protected_hashes'].items())
    report=dict(candidate=str(dst),candidate_sha256=sha(dst),frames=n+1,duration=(n+1)/30,fps=30,
        changed_frames=new,untouched_frames_pixel_identical=exact,preserved_reencoded_frames=handles,
        preserved_reencoded_min_psnr_db=min_handle if handles else None,changed_render_min_psnr_db=min_render,
        unchanged_video_packets_identical=True,all_frame_timestamps_identical=True,audio_packets_identical=True,
        audio_packet_count=len(aa),decoded_audio=decoded[0],transition_guard_passed=not flags,
        transition_flags=flags,reviewed_continuous_camera_motion_flags=flags if reviewed_motion else [],
        protected_files_unchanged=True,visual_review_completed=False,direct_listening_performed=False,
        full_realtime_playback_performed=False)
    (out/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
    assert not flags or reviewed_motion,'Transition flags require visual review; completed frame/audio results saved in qa.json.'

if __name__=='__main__':
    cv2.setNumThreads(1)
    parser=argparse.ArgumentParser();parser.add_argument('slug',choices=CONFIG)
    parser.add_argument('--reviewed-motion-flags',action='store_true',help='Use only after inspecting all five flagged camera-move strips.')
    args=parser.parse_args();qa(args.slug,args.reviewed_motion_flags)
