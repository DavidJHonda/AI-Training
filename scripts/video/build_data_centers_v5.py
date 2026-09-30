#!/usr/bin/env python3
"""Two approved caption clarifications. Copy all audio and unaffected H.264 GOPs."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import av
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/data-centers-caption-repair-2026-09-30-v5'
SRC = ROOT / 'course-assets/data-centers/data-centers.mp4'
DEST = ROOT / 'Prompts/data-centers-v5.mp4'
EXPECTED = '239d5a26ee58a5e28322eadc364a15af27f946324c4fe4563bb96d9a659c4130'
SPANS = [(250, 500, 'assumption'), (5467, 5717, 'request')]
PATCHES = [(290, 494, 'assumption'), (5468, 5591, 'request')]
FF = imageio_ffmpeg.get_ffmpeg_exe()
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
cv2.setNumThreads(1)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def text_mask(text, y, size):
    im = Image.new('L', (1280*3, 720*3))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(FONT, size*3)
    d.text((640*3,y*3), text, font=font, fill=255, anchor='mm')
    return np.asarray(im.resize((1280,720), Image.Resampling.LANCZOS)).astype(np.float32)/255

MASKS = {
    'assumption': [(text_mask('In this example: one trillion weights used per token.',480,20), (225,232,232))],
    'request': [(text_mask('Our 1,000-token example:',563,21),(237,242,242)),
                (text_mask('~2 quadrillion calculations',596,21),(107,207,235))],
}

def patch(frame, n):
    spec = next((p for p in PATCHES if p[0]<=n<p[1]),None)
    if spec is None: return frame, None
    name=spec[2]
    if name=='assumption':
        # The caption moves by only a few pixels while its plate eases in.
        # This band includes every observed glyph position, including both fades.
        x0,x1,y0,y1=363,924,464,496
        sample=frame[391:406,600:680].astype(float)
        dark=51.0; paper=234.0
    else:
        x0,x1,y0,y1=450,830,564,599
        sample=frame[610:616,550:720].astype(float)
        dark=59.0; paper=235.0
    opacity=float(np.clip((paper-np.median(sample))/(paper-dark),0,1))
    if opacity < .012: return frame, {'frame':n,'caption':name,'opacity':opacity}
    result=frame.astype(np.float32)
    # Interpolate the current frame's plate through the old text. Sampling this
    # frame, rather than stamping an opaque panel, retains the source fades.
    top=cv2.GaussianBlur(frame[y0-3:y0,x0:x1].astype(np.float32).mean(axis=0)[None],(15,1),0)[0]
    bot=cv2.GaussianBlur(frame[y1:y1+3,x0:x1].astype(np.float32).mean(axis=0)[None],(15,1),0)[0]
    t=np.linspace(0,1,y1-y0)[:,None,None]
    clean=top[None]*(1-t)+bot[None]*t
    edge=np.ones((y1-y0,x1-x0),np.float32)
    for i in range(3):
        edge[i,:]=edge[-1-i,:]=(i+1)/4
        edge[:,i]=np.minimum(edge[:,i],(i+1)/4)
        edge[:,-1-i]=np.minimum(edge[:,-1-i],(i+1)/4)
    result[y0:y1,x0:x1]=result[y0:y1,x0:x1]*(1-edge[:,:,None])+clean*edge[:,:,None]
    for mask,color in MASKS[name]:
        a=mask[:,:,None]*opacity
        result=result*(1-a)+np.array(color,dtype=np.float32)*a
    return np.rint(np.clip(result,0,255)).astype(np.uint8), {'frame':n,'caption':name,'opacity':round(opacity,5)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');args=ap.parse_args()
    assert sha(SRC)==EXPECTED
    OUT.mkdir(exist_ok=True)
    if not args.preview_only: assert not DEST.exists(), 'Never overwrite a candidate'
    protected=[SRC,ROOT/'index.html',ROOT/'lessons/data-centers.md',*sorted((ROOT/'course-assets/data-centers').glob('*.jpg'))]
    hashes={str(p):sha(p) for p in protected}
    targets={289,292,298,300,307,315,360,465,474,480,489,494,5467,5470,5476,5485,5520,5545,5550,5560,5575,5591}
    processes={};legs=[];rows=[]
    if not args.preview_only:
        for a,b,name in SPANS:
            leg=OUT/f'leg-{name}.mp4'
            assert not leg.exists(), 'Use a fresh render directory for a rebuild'
            cmd=[FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','-',
                 '-an','-c:v','libx264','-threads','2','-crf','18','-preset','medium','-pix_fmt','yuv420p','-profile:v','high',
                 '-level:v','3.1','-video_track_timescale','15360',str(leg)]
            log=(OUT/f'encode-{name}.log').open('w')
            processes[name]=(subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log),log)
            legs.append((a,b,leg))
    with av.open(str(SRC)) as c:
        c.streams.video[0].codec_context.thread_count=1
        for n,fr in enumerate(c.decode(video=0)):
            span=next((s for s in SPANS if s[0]<=n<s[1]),None)
            if span:
                original=fr.to_ndarray(format='bgr24');edited,row=patch(original,n)
                if row:rows.append(row)
                if n in targets: cv2.imwrite(str(OUT/f'preview-{n:05}.png'),edited)
                if not args.preview_only: processes[span[2]][0].stdin.write(edited.tobytes())
            if n>=5717:break
    (OUT/'caption-opacity.json').write_text(json.dumps(rows,indent=2)+'\n')
    if args.preview_only:
        print('Previews ready',flush=True);return
    for proc,log in processes.values():
        proc.stdin.close();assert proc.wait()==0;log.close()
    source=av.open(str(SRC));v=source.streams.video[0];au=source.streams.audio[0]
    packets=[];keys=[]
    for p in source.demux(v,au):
        if p.dts is None:continue
        video=p.stream.type=='video';f=round(float(p.pts*p.time_base)*30) if video else None
        if video and p.is_keyframe:keys.append(f)
        if video and any(a<=f<b for a,b,_ in SPANS):continue
        packets.append((video,p))
    open_legs=[]
    for a,b,path in legs:
        assert a in keys and b in keys
        c=av.open(str(path));open_legs.append(c);s=c.streams.video[0]
        assert s.time_base==v.time_base
        assert s.codec_context.extradata==v.codec_context.extradata, (s.codec_context.extradata.hex(),v.codec_context.extradata.hex())
        count=0
        for p in c.demux(s):
            if p.dts is None:continue
            p.pts+=a*512;p.dts+=a*512;packets.append((True,p));count+=1
        assert count==b-a
    packets.sort(key=lambda t:(t[1].dts*t[1].time_base,not t[0]))
    with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as c:
        ov=c.add_stream_from_template(v);oa=c.add_stream_from_template(au)
        for video,p in packets:p.stream=ov if video else oa;c.mux(p)
    manifest=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),candidate_sha256=sha(DEST),
                  approval='User: Build it please. Two required caption clarifications; optional facility replacement excluded.',
                  source_limitation='Pristine raw rolls absent. Re-encode only two GOPs from SHA-locked finished video.',
                  frames=6694,fps=30,duration=6694/30,encoded_gops=SPANS,caption_windows=PATCHES,
                  method='Current-frame text-band interpolation and fade-matched text; copy all other video GOPs and all AAC packets.',
                  captions=['In this example: one trillion weights used per token.','Our 1,000-token example: ~2 quadrillion calculations'],
                  boundaries=[{'frame':f,'label':name+suffix} for a,b,name in SPANS for f,suffix in [(a,'-gop-in'),(b,'-gop-out')]],
                  protected_hashes=hashes,listening_performed=False)
    assert all(sha(p)==h for p,h in hashes.items())
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Built',DEST,sha(DEST),flush=True)

if __name__=='__main__':main()
