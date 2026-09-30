#!/usr/bin/env python3
"""Replace two titles; remux all other v9 H.264 packets and all AAC packets."""
from pathlib import Path
import hashlib
import json
import subprocess
import av
import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/flattery-trap-labels-2026-09-30-v10'
SRC = ROOT / 'Prompts/flattery-trap-v9.mp4'
DEST = ROOT / 'Prompts/flattery-trap-v10.mp4'
SOURCE_HASH = '26a48f97db2ece2374d2849ac7730d39c68d19fe083f6cb709bc450d0ce5f4f0'
SPANS = [(396, 463, 'flattery-trap'), (3385, 3608, 'sycophancy')]
FF = imageio_ffmpeg.get_ffmpeg_exe()

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def patch(frame, edited, name):
    # Composite only the generated text areas. Keep the original notebook,
    # paper edges, dictionary definition, and remaining scene pixels.
    mask = np.zeros((720, 1280), np.uint8)
    if name == 'flattery-trap':
        points = np.array([(210,181),(1025,83),(1150,459),(276,625)], np.int32)
        cv2.fillConvexPoly(mask, points, 255)
        mask = cv2.GaussianBlur(mask,(21,21),4)
    else:
        mask[250:305,407:887] = 255
        mask = cv2.GaussianBlur(mask,(9,9),1.5)
    alpha = mask.astype(np.float32)[:,:,None] / 255
    return np.rint(frame*(1-alpha)+edited*alpha).astype(np.uint8)

def main():
    assert sha(SRC) == SOURCE_HASH
    assert not DEST.exists(), 'Never overwrite a review candidate'
    replacements = []
    for a,b,name in SPANS:
        edited = cv2.resize(cv2.imread(str(OUT/f'{name}.png')), (1280,720), interpolation=cv2.INTER_AREA)
        leg = OUT/f'leg-{name}.mp4'
        assert not leg.exists()
        cmd = [FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720',
               '-framerate','30','-i','-','-an','-c:v','libx264','-threads','2','-crf','16',
               '-preset','fast','-pix_fmt','yuv420p','-profile:v','high','-level:v','3.1',
               '-video_track_timescale','15360',str(leg)]
        c = cv2.VideoCapture(str(SRC)); c.set(cv2.CAP_PROP_POS_FRAMES,a)
        with (OUT/f'encode-{name}.log').open('w') as log:
            proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
            for f in range(a,b):
                ok, frame = c.read(); assert ok
                result = patch(frame,edited,name)
                if f in [a,(a+b)//2,b-1]:
                    cv2.imwrite(str(OUT/f'preview-{f:05}.png'),result)
                proc.stdin.write(result.tobytes())
            proc.stdin.close(); assert proc.wait() == 0
        c.release()
        replacements.append((a,b,leg))

    source = av.open(str(SRC)); video=source.streams.video[0]; audio=source.streams.audio[0]
    keys = []
    packets = []
    for packet in source.demux(video,audio):
        if packet.dts is None: continue
        isvideo = packet.stream.type == 'video'
        f = round(float(packet.pts*packet.time_base)*30) if isvideo else None
        if isvideo and packet.is_keyframe: keys.append(f)
        if isvideo and any(a<=f<b for a,b,_ in SPANS): continue
        packets.append((isvideo,packet))
    for a,b,_ in SPANS: assert a in keys and b in keys, 'Edits must align with complete GOPs'
    extradata = []
    legs = []
    for a,b,path in replacements:
        leg=av.open(str(path)); legs.append(leg)
        v=leg.streams.video[0]
        assert v.time_base == video.time_base
        extra=v.codec_context.extradata
        extradata.append({'span':[a,b], 'same_codec_extradata':extra == video.codec_context.extradata,
                          'source':video.codec_context.extradata.hex(),'replacement':extra.hex()})
        # Equal SPS/PPS keeps the original stream's decoder configuration valid.
        assert extra == video.codec_context.extradata, extradata[-1]
        count=0
        for p in leg.demux(v):
            if p.dts is None: continue
            p.pts += a*512; p.dts += a*512
            packets.append((True,p)); count+=1
        assert count==b-a
    packets.sort(key=lambda x: (x[1].dts*x[1].time_base, not x[0]))
    with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as output:
        ov=output.add_stream_from_template(video); oa=output.add_stream_from_template(audio)
        for isvideo,p in packets:
            p.stream = ov if isvideo else oa
            output.mux(p)
    manifest={'scope':'Two heading corrections only; no audio or timeline edits.',
              'source':str(SRC),'source_sha256':SOURCE_HASH,'candidate':str(DEST),
              'candidate_sha256':sha(DEST),'fps':30,'frames':9431,
              'spans':[{'start_frame':a,'end_frame_exclusive':b,'title':n} for a,b,n in SPANS],
              'codec_checks':extradata,
              'method':'Encode only two complete GOPs; remux all unaffected video and every audio packet unchanged.',
              'assets':{n:sha(OUT/f'{n}.png') for _,_,n in SPANS}}
    assert sha(SRC)==SOURCE_HASH
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__': main()
