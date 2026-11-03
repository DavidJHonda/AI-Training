#!/usr/bin/env python3
"""Remove the 13-frame science-board return; preserve v9 audio and other packets.

The replacement GOP is rendered from pristine sources. --full reproduces the
same approved assembly directly from the raw rolls when no v9 is available.
"""
import json, subprocess, sys
import av, cv2
import build_big_upside_v9 as b
from gemini_mark import clean_frame, glyph_mask

SOURCE=b.DEST
OLD_OUT=b.OUT
OUT=b.ROOT/'video-audit/big-upside-build-2026-11-03-v10'
DEST=b.ROOT/'Prompts/big-upside-v10.mp4'
FIX_RANGE=(2386,2399)
REASON="Continue lab illustration directly into cancer board; remove 13-frame science-board return."
original_plan=b.picture_plan

def corrected_plan(rows):
    spans=original_plan(rows);result=[]
    for span in spans:
        span=dict(span)
        if span['start_frame']==2386 and span['end_frame']==2399:
            assert span['state']==('board','protein',None)
            span['state']=('clip',2,2914,'testing laboratory')
        if result:
            prev=result[-1];a=prev['state'];s=span['state']
            if a[0]=='clip' and s[0]=='clip' and a[1]==s[1] and a[3]==s[3] and a[2]+prev['end_frame']-prev['start_frame']==s[2]:
                prev['end_frame']=span['end_frame'];continue
        result.append(span)
    return result

def configure():
    b.OUT=OUT;b.DEST=DEST;b.picture_plan=corrected_plan

def main():
    configure()
    if '--full' in sys.argv:return b.main()
    assert SOURCE.exists() and not DEST.exists()
    OUT.mkdir(exist_ok=True);cv2.setNumThreads(2)
    m=json.loads((OLD_OUT/'edit-manifest.json').read_text())
    assert b.sha(SOURCE)==m['sha256']
    assert all(b.sha(p)==h for p,h in m['protected_hashes'].items())
    src=av.open(str(SOURCE));v=src.streams.video[0]
    ticks=round(1/(30*v.time_base));keys=[]
    for p in src.demux(v):
        if p.dts is not None and p.is_keyframe:keys.append(round(p.pts/ticks))
    timescale=v.time_base.denominator
    src.close()
    A=max(k for k in keys if k<=FIX_RANGE[0]);B=min(k for k in keys if k>=FIX_RANGE[1])
    rows=b.audio_plan();spans=corrected_plan(rows);views,boards=b.board_views()
    cmd=[b.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-an','-c:v','libx264','-crf','18','-preset','medium','-threads','4','-pix_fmt','yuv420p','-video_track_timescale',str(timescale),str(OUT/'replacement-gop.mp4')]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE);readers={};mask=glyph_mask()
    for f in range(A,B):
        span=next(s for s in spans if s['start_frame']<=f<s['end_frame']);kind,*args=span['state']
        if kind=='board':im=views[tuple(args)]
        elif kind=='clip':
            roll,start,label=args;n=start+f-span['start_frame']
            if label=='community benefits':n=min(n,b.F(244.5)-1)
            if roll not in readers or readers[roll].n>n:
                if roll in readers:readers[roll].c.release()
                readers[roll]=b.Reader(b.SRC[roll])
            im,method=clean_frame(readers[roll].at(n),mask)
        else:raise AssertionError((f,span))
        p.stdin.write(im.tobytes())
    p.stdin.close();assert p.wait()==0
    for r in readers.values():r.c.release()
    leg=OUT/'replacement-gop.mp4'
    src=av.open(str(SOURCE));v=src.streams.video[0];a=src.streams.audio[0]
    patch=av.open(str(leg));pv=patch.streams.video[0]
    assert pv.time_base==v.time_base
    assert pv.codec_context.extradata==v.codec_context.extradata
    packets=[];retained=0;audio_packets=0
    for p in src.demux(v,a):
        if p.dts is None:continue
        if p.stream.type=='video':
            if A<=round(p.pts/ticks)<B:continue
            retained+=1;packets.append((True,p))
        else:audio_packets+=1;packets.append((False,p))
    for p in patch.demux(pv):
        if p.dts is None:continue
        p.pts+=A*ticks;p.dts+=A*ticks;packets.append((True,p))
    packets.sort(key=lambda item:(item[1].dts*item[1].time_base,not item[0]))
    with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as dest:
        ov=dest.add_stream_from_template(v);oa=dest.add_stream_from_template(a)
        for video,p in packets:p.stream=ov if video else oa;dest.mux(p)
    src.close();patch.close()
    for name in ['source-1.wav','source-3.wav','edited.wav','close.png']:
        (OUT/name).symlink_to(OLD_OUT/name)
    for (key,i),im in views.items():cv2.imwrite(str(OUT/f'state-{key}-{i}.jpg'),im)
    m.update(candidate=str(DEST.relative_to(b.ROOT)),sha256=b.sha(DEST),visual_timeline=spans,
             picture_repair=dict(source=str(SOURCE.relative_to(b.ROOT)),source_sha256=b.sha(SOURCE),corrected_output_frames=list(FIX_RANGE),rerendered_gop=[A,B],retained_video_packets=retained,copied_audio_packets=audio_packets,reason=REASON+' Replacement GOP rendered from pristine sources.'),boards=boards)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(f'Created {DEST}: {m["duration"]}s. Corrected frames {FIX_RANGE}; pristine GOP {A}–{B}; all audio copied.',flush=True)

if __name__=='__main__':main()
