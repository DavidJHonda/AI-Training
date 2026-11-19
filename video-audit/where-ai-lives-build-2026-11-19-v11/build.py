"""Create the rack push-in from the original hall illustration and the v10 review cut."""
import hashlib
import json
import subprocess
from pathlib import Path

import av
import cv2
import imageio_ffmpeg
import numpy as np

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
SOURCE = ROOT/'Prompts/where-ai-lives-v10.mp4'
DEST = ROOT/'Prompts/where-ai-lives-v11.mp4'
PHOTO = ROOT/'course-assets/where-ai-lives/where-ai-lives-data-center.jpg'
START, SETTLE, END = 5038, 5122, 5291
LEFT, TOP, WIDTH = 145., 342., 730.


def frame_at(photo, frame):
    progress = min(1., max(0., (frame-START)/(SETTLE-START)))
    ease = progress**2*(3-2*progress)
    full_width = photo.shape[0]*16/9
    initial_left = (photo.shape[1]-full_width)/2
    width = full_width+(WIDTH-full_width)*ease
    left = initial_left+(LEFT-initial_left)*ease
    matrix = np.float32([[width/1280,0,left],[0,width/1280,TOP*ease]])
    return cv2.warpAffine(photo,matrix,(1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_CONSTANT,borderValue=(245,245,245))


def main():
    if DEST.exists():
        raise SystemExit(f'Already exists: {DEST}')
    reference = json.loads((OUT.parent/'where-ai-lives-build-2026-11-19-v10/edit-manifest.json').read_text())
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==reference['render_sha256']
    with av.open(str(SOURCE)) as src:
        v = src.streams.video[0]
        ticks = int(1/(30*v.time_base))
        keys = [p.pts//ticks for p in src.demux(v) if p.is_keyframe]
        scale = int(1/v.time_base)
    first = max(i for i in keys if i<=START)
    assert END in keys
    patch = OUT/'rack-span.mp4'
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
           '-vf','scale=out_range=full:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int',
           '-color_range','pc','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
           '-c:v','libx264','-crf','18','-preset','fast','-threads','4','-pix_fmt','yuv420p',
           '-video_track_timescale',str(scale),str(patch)]
    photo = cv2.imread(str(PHOTO))
    wide = np.full((720,1280,3),245,np.uint8)
    wide[:,100:1180] = cv2.resize(photo,(1080,720),interpolation=cv2.INTER_AREA)
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for i in range(first,END):
            proc.stdin.write((wide if i<=START else frame_at(photo,i)).tobytes())
        proc.stdin.close()
        assert proc.wait()==0

    with av.open(str(SOURCE)) as src, av.open(str(patch)) as leg:
        v,a = src.streams.video[0],src.streams.audio[0]
        pv = leg.streams.video[0]
        assert pv.time_base==v.time_base and pv.codec_context.extradata==v.codec_context.extradata
        packets = [p for p in src.demux(v,a) if p.dts is not None and
                   (p.stream.type=='audio' or not first<=p.pts//ticks<END)]
        for p in leg.demux(pv):
            if p.dts is not None:
                p.pts+=first*ticks
                p.dts+=first*ticks
                packets.append(p)
        temp = OUT/'candidate.tmp.mp4'
        with av.open(str(temp),'w',options={'movflags':'+faststart'}) as dest:
            streams = {s.type:dest.add_stream_from_template(s) for s in (v,a)}
            for p in sorted(packets,key=lambda p:p.dts*p.time_base):
                p.stream = streams[p.stream.type]
                dest.mux(p)
        temp.rename(DEST)
    print(f'Created {DEST.name}; replaced frames {first}–{END-1}.')


if __name__=='__main__':
    main()
