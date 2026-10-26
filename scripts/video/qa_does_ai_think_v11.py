#!/usr/bin/env python3
"""Check the actual v11 encoding, exact retained packets, mapped frames and audio."""
import hashlib
import json
import subprocess
import sys
import wave

import av
import cv2
import numpy as np
import build_does_ai_think_v11 as b

def packet_rows(path,kind):
    with av.open(str(path)) as c:
        s=next(s for s in c.streams if s.type==kind)
        return [(p.pts,p.dts,p.duration,str(p.time_base),hashlib.sha256(bytes(p)).hexdigest()) for p in c.demux(s) if p.dts is not None]

def decode(path):
    with av.open(str(path)) as c:
        c.streams.video[0].codec_context.thread_count=1
        yield from c.decode(video=0)

def pcm(path):
    raw=subprocess.check_output([b.FF,'-v','error','-i',str(path),'-vn','-ac','1','-ar','48000','-f','s16le','-'])
    return np.frombuffer(raw,dtype='<i2')

def main():
    m=json.loads((b.OUT/'edit-manifest.json').read_text());assert b.sha(b.DST)==m['candidate_sha256']
    renderer,_=b.prepare()
    # Compare every copied packet including its mapped DTS, PTS and duration.
    source_video=packet_rows(b.SRC,'video');candidate_video=packet_rows(b.DST,'video')
    expected=[]
    for row in source_video:
        p,d,duration,tb,h=row;n=p//512
        if b.inside(n,b.ENCODE):continue
        shift=(n-b.mapped(n))*512
        expected.append((p-shift,d-shift,duration,tb,h))
    retained=[r for r in candidate_video if not b.inside(b.MAPPING[r[0]//512],b.ENCODE)]
    assert expected==retained,'Retained video packets or times changed'
    source_audio=packet_rows(b.SRC,'audio');candidate_audio=packet_rows(b.DST,'audio')
    expected=[]
    for p,d,duration,tb,h in source_audio:
        if b.AUDIO_START<=p<b.AUDIO_END:continue
        shift=b.REMOVED*b.SPF if p>=b.AUDIO_END else 0
        expected.append((p-shift,d-shift,duration,tb,h))
    end=b.AUDIO_END-b.REMOVED*b.SPF
    retained_a=[r for r in candidate_audio if not b.AUDIO_START<=r[0]<end]
    assert expected==retained_a,'Retained audio packets or times changed'
    assert len(candidate_video)==b.TOTAL
    assert all(r[0]==i*1024-1024 for i,r in enumerate(candidate_audio)),'AAC timestamp gap'
    assert all(r[1]==r[0] for r in candidate_audio)
    out=b.OUT/'encoded';out.mkdir(exist_ok=True)
    selected={0,b.TOTAL-1}
    for n in map(int,m['boundaries']):selected.update([n-1,n,n+1,n+15,n+30])
    src=iter(enumerate(decode(b.SRC)));source_n=-1;exact=boards=handles=0;board_min=handle_min=100.0
    actual_count=0
    for n,actual in enumerate(decode(b.DST)):
        actual_count+=1;want=b.MAPPING[n]
        while source_n<want:source_n,original=next(src)
        assert actual.pts*actual.time_base==n/30 or float(actual.pts*actual.time_base)==n/30
        assert actual.width==1280 and actual.height==720
        yuv=actual.to_ndarray(format='yuv420p')
        if not b.inside(want,b.ENCODE):
            assert np.array_equal(original.to_ndarray(format='yuv420p'),yuv),(n,want,'copied pixels')
            exact+=1
        elif b.is_board(want):
            score=cv2.PSNR(b.board_frame(renderer,want),actual.to_ndarray(format='bgr24'))
            assert score>32,(n,want,score,'board render')
            board_min=min(board_min,score);boards+=1
        else:
            score=cv2.PSNR(original.to_ndarray(format='yuv420p'),yuv)
            assert score>38,(n,want,score,'retained handles')
            handle_min=min(handle_min,score);handles+=1
        if n in selected:cv2.imwrite(str(out/f'{n:05d}.jpg'),actual.to_ndarray(format='bgr24'),[cv2.IMWRITE_JPEG_QUALITY,96])
    assert actual_count==b.TOTAL
    before,after=pcm(b.SRC),pcm(b.DST)
    expected_pcm=np.concatenate([before[a*b.SPF:z*b.SPF] for a,z in b.KEEP])
    assert len(after)>=b.TOTAL*b.SPF and len(after)-b.TOTAL*b.SPF<1024
    after=after[:b.TOTAL*b.SPF]
    # AAC overlap state can affect one adjacent packet; outside two packet handles PCM must be exact.
    assert np.array_equal(after[:b.AUDIO_START-2048],expected_pcm[:b.AUDIO_START-2048])
    assert np.array_equal(after[end+2048:],expected_pcm[end+2048:])
    with wave.open(str(b.OUT/'edited.wav')) as f:master=np.frombuffer(f.readframes(f.getnframes()),dtype='<i2').astype(float)
    a=master[b.AUDIO_START:end];z=after[b.AUDIO_START:end].astype(float)
    snr=float(10*np.log10(np.sum(a*a)/max(np.sum((a-z)**2),1)))
    assert snr>25,('edited audio SNR',snr)
    joins=[]
    for i,(_,source_b) in enumerate(b.CUTS):
        at=b.mapped(source_b)*b.SPF
        # One-ms RMS gap around actual encoded join, measured at -40 dBFS.
        local=after[at-b.RATE:at+b.RATE].astype(float)/32768
        rms=np.sqrt(np.mean(local.reshape(-1,48)**2,axis=1));db=20*np.log10(rms+1e-12)
        left=np.where(db[:1000]>-40)[0][-1]+1;right=1000+np.where(db[1000:]>-40)[0][0]
        joins.append(dict(number=i+1,source_cut_frames=b.CUTS[i],output_frame=b.mapped(source_b),output_seconds=at/b.RATE,
                          encoded_gap_seconds=(right-left)/1000,threshold_dbfs=-40,
                          seam_10ms_rms_dbfs=float(20*np.log10(np.sqrt(np.mean((after[at-240:at+240].astype(float)/32768)**2))+1e-12))))
        clip=after[at-3*b.RATE:at+4*b.RATE]
        with wave.open(str(b.OUT/f'join-{i+1}-encoded.wav'),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(b.RATE);f.writeframes(clip.tobytes())
    assert all(b.sha(p)==h for p,h in m['protected_hashes'].items())
    report=dict(candidate=str(b.DST),candidate_sha256=b.sha(b.DST),frames=actual_count,duration=b.TOTAL/30,
                exact_retained_video_packets=len(retained),exact_retained_audio_packets=len(retained_a),
                exact_retained_frames=exact,updated_board_frames=boards,reencoded_handle_frames=handles,
                minimum_board_psnr_db=board_min,minimum_handle_psnr_db=handle_min,edited_audio_snr_db=snr,
                retained_audio_pcm_exact_outside_two_packet_codec_handles=True,all_frame_timestamps_correct=True,
                all_aac_timestamps_contiguous=True,audio_joins=joins,protected_files_unchanged=True,
                listening_performed=False,continuous_playback_performed=False,visual_review_completed=False)
    (b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
    cmd=[sys.executable,'-c','import cv2,runpy;cv2.setNumThreads(1);runpy.run_path("scripts/video/transition_guard.py",run_name="__main__")',str(b.DST),'--outdir',str(b.OUT/'transitions')]
    for n,label in sorted((int(k),v) for k,v in m['boundaries'].items()):cmd+=['--boundary',f'{n}:{label}']
    result=subprocess.run(cmd,cwd=b.ROOT,capture_output=True,text=True)
    (b.OUT/'transition-command.log').write_text(result.stdout+result.stderr)
    guard=json.loads((b.OUT/'transitions/transition-guard.json').read_text())
    report['transition_flags']=[r['frame'] for r in guard['boundaries'] if not r['pass']]
    report['transition_guard_exit']=result.returncode
    (b.OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Transition flags',report['transition_flags'],flush=True)

if __name__=='__main__':
    cv2.setNumThreads(1)
    main()
