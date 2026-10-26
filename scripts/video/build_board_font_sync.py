#!/usr/bin/env python3
"""Sync four approved board JPGs into three finished videos, preserving their treatments."""
import argparse
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

import av
import cv2
import imageio_ffmpeg

from editspec_build import Build
from build_wheres_the_line_v3 import Board
import ken_burns_path as kb

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/board-font-sync-2026-10-23'
FF = imageio_ffmpeg.get_ffmpeg_exe()
CONFIG = {
    'honesty-and-privacy': dict(version=7, frames=6900,
        sha='17e86f470823304a8e845797f32a109bd466b62473a849b9a1d8ec14269e504e',
        encode=[[656,1899]], boards=[dict(key='school', start=674, end=1676,
            asset='honesty-and-privacy-school.jpg', stroke=5,
            spec='honesty-and-privacy-repair-2026-09-12/leg-1-school.json')]),
    'wheres-the-line': dict(version=5, frames=6059,
        sha='d4717575e5acbe4beecd64e9347a1aef89197a31a0bc3944e9de982b2c03019f',
        encode=[[2898,3210],[3300,3690],[3780,3915],[4370,4710],[4830,5250],[5340,5798]],
        boards=[dict(key='uses', start=2898, end=3915, asset='wheres-the-line-two-uses.jpg', stroke=4,
            spec='wheres-the-line-board-edges-2026-10-01-v4/leg-uses.json'),
            dict(key='moves', start=4370, end=5798, asset='wheres-the-line-responsible-choice.jpg', stroke=4,
            spec='wheres-the-line-board-edges-2026-10-01-v4/leg-moves.json')]),
    'people-skills': dict(version=8, frames=3830,
        sha='2e811927fb1391ce5bb5a2eef961a9e610835b9f52b833ebc0f902923194cf8c',
        encode=[[798,1216]], boards=[dict(key='next-move', start=798, end=1071,
            asset='people-skills-why-people-matter.jpg', stroke=4,
            spec='people-skills-engagement-2026-09-26/build-v3/leg-nm.json')]),
}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def paths(slug):
    return (Path(f'/tmp/{slug}-font-sync-20261023-source.mp4'),
            ROOT / f'Prompts/{slug}-v{CONFIG[slug]["version"]}.mp4')

def inside(n, intervals):
    return any(a <= n < b for a,b in intervals)

def prepare(slug):
    out=OUT/slug; out.mkdir(parents=True, exist_ok=True)
    boards=[]
    for item in CONFIG[slug]['boards']:
        spec=json.loads((ROOT/'video-audit'/item['spec']).read_text())
        canvas,cw,ch,ox,oy=Build.compose(SimpleNamespace(out=out), ROOT/'course-assets'/slug/item['asset'], item['key'])
        assert spec['beats'][0]['from']==[cw/2,ch/2,float(cw)], 'Canvas geometry changed'
        assert sum(b['frames'] for b in spec['beats'])==item['end']-item['start']
        spec['image']=str(canvas)
        target=out/f'leg-{item["key"]}.json';target.write_text(json.dumps(spec,indent=2)+'\n')
        boards.append((item,Board(target)))
    return boards

def render(slug, boards, n):
    if not inside(n,CONFIG[slug]['encode']):return None
    for item,board in boards:
        if item['start']<=n<item['end']:
            # Honor the stroke weight of each finished source, including the legacy school ring.
            original=kb.ring_px
            try:
                kb.ring_px=lambda height: item['stroke']
                return board.frame(n-item['start'])
            finally:kb.ring_px=original
    return None

def boundaries(slug, boards):
    result={}
    for a,b in CONFIG[slug]['encode']:
        result[a]='replacement-start';result[b]='source-resumes'
    for item,board in boards:
        result[item['start']]=item['key']+'-in';result[item['end']]=item['key']+'-out'
        for ring in board.spec['rings']:
            for k in ('start','end'):result[item['start']+ring[k]]=item['key']+'-highlight-'+k
    return result

def build(slug, preview=False):
    cfg=CONFIG[slug];src,dst=paths(slug);boards=prepare(slug);out=OUT/slug
    if preview:
        for item,board in boards:
            for n in [0,*[r['start'] for r in board.spec['rings']],item['end']-item['start']-1]:
                im=render(slug,boards,item['start']+n)
                if im is not None:cv2.imwrite(str(out/f'{item["key"]}-{n:04}.jpg'),im)
        return
    assert not dst.exists(),dst
    live=ROOT/f'course-assets/{slug}/{slug}.mp4'
    assert sha(src)==sha(live)==cfg['sha']
    protected={str(p):sha(p) for p in [src,live,ROOT/'index.html',ROOT/f'lessons/{slug}.md',*live.parent.glob('*.jpg')]}
    legs=[]
    with av.open(str(src)) as source:
        source.streams.video[0].codec_context.thread_count=2
        decoded=iter(enumerate(source.decode(video=0)))
        for i,(start,end) in enumerate(cfg['encode']):
            leg=out/f'replacement-{i}.mp4';legs.append(leg)
            with (out/f'encode-{i}.log').open('w') as log:
                preset=cfg.get('preset','medium' if slug=='people-skills' else 'fast')
                crf=str(cfg.get('crf','18' if slug=='people-skills' else '16'))
                aspect=['-vf','setsar=1'] if slug=='honesty-and-privacy' else []
                cmd=[FF,'-v','error','-y','-f','rawvideo','-pixel_format','yuv420p','-video_size','1280x720','-framerate','30','-i','-','-an','-c:v','libx264','-threads','2','-preset',preset,'-crf',crf,'-profile:v','high','-level:v','3.1',*aspect,'-video_track_timescale','15360',str(leg)]
                proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
                for n,frame in decoded:
                    if n<start:continue
                    replacement=render(slug,boards,n)
                    if replacement is not None:frame=av.VideoFrame.from_ndarray(replacement,format='bgr24')
                    proc.stdin.write(frame.to_ndarray(format='yuv420p').tobytes())
                    if n==end-1:break
                proc.stdin.close();assert proc.wait()==0
            print(slug,'encoded',start,end,flush=True)
    with av.open(str(src)) as source:
        v=source.streams.video[0];a=source.streams.audio[0];packets=[];keys=[]
        for packet in source.demux(v,a):
            if packet.dts is None:continue
            video=packet.stream.type=='video'
            n=round(packet.pts*packet.time_base*30) if video else None
            if video and packet.is_keyframe:keys.append(n)
            if video and inside(n,cfg['encode']):continue
            packets.append((video,packet))
        for leg,(start,end) in zip(legs,cfg['encode']):
            assert start in keys and end in keys
            with av.open(str(leg)) as replacement:
                rv=replacement.streams.video[0]
                assert v.time_base==rv.time_base
                assert v.codec_context.extradata==rv.codec_context.extradata,('codec mismatch',v.codec_context.extradata.hex(),rv.codec_context.extradata.hex())
                offset=round(Fraction(start,30)/v.time_base);count=0
                for packet in replacement.demux(rv):
                    if packet.dts is None:continue
                    packet.pts+=offset;packet.dts+=offset;packets.append((True,packet));count+=1
                assert count==end-start
        packets.sort(key=lambda x:(x[1].dts*x[1].time_base,not x[0]))
        with av.open(str(dst),'w',options={'movflags':'+faststart'}) as output:
            ov=output.add_stream_from_template(v);oa=output.add_stream_from_template(a)
            for video,packet in packets:
                packet.stream=ov if video else oa;output.mux(packet)
    assert all(sha(p)==h for p,h in protected.items())
    manifest=dict(cfg,source=str(src),candidate=str(dst),candidate_sha256=sha(dst),protected_hashes=protected,
        boundaries=boundaries(slug,boards),scope='Only current approved board assets; original highlights, cameras, cutaways, timing and audio retained.',
        source_limitation='Finished video source. Only listed GOP intervals re-encoded; all other video packets and all audio packets copied.',
        status='Review candidate; not installed or published')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('BUILT',dst,flush=True)

if __name__=='__main__':
    cv2.setNumThreads(2)
    parser=argparse.ArgumentParser();parser.add_argument('slug',choices=CONFIG);parser.add_argument('--preview',action='store_true')
    args=parser.parse_args();build(args.slug,args.preview)
