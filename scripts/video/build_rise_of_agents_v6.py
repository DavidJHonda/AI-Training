#!/usr/bin/env python3
"""Approved narrow correction: one finished-source encode; remove withdrawn Gemini story."""
from pathlib import Path
import hashlib,json,subprocess,wave
import cv2,numpy as np
from PIL import Image,ImageDraw
import imageio_ffmpeg
from editorial_typography import face
from render_rise_of_agents_rogue import QUOTE

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'course-assets/rise-of-agents/rise-of-agents.mp4'
OUT=ROOT/'video-audit/rise-of-agents-repair-2026-09-30-v6'
DEST=ROOT/'Prompts/rise-of-agents-v6.mp4'
BOARD=SRC.parent/'rise-of-agents-rogue.jpg'
EXPECTED='d27f50d630ccae490c6d6c9511d6694d638e65dc073e8dd4ff9a4887ebfe8dcd'
FPS,RATE,N=30,48000,5634
CUT_A,CUT_B=4414,4749
TOTAL=N-(CUT_B-CUT_A)
FF=imageio_ffmpeg.get_ffmpeg_exe()

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wav(path,a):
    with wave.open(str(path),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(RATE);w.writeframes(np.clip(np.rint(a),-32768,32767).astype('<i2').tobytes())

def patch_scene(frame,f):
    """Replace unsupported labels only, retaining the agent, key, server, trash and reveals."""
    t=f/FPS
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    im=Image.fromarray(rgb);d=ImageDraw.Draw(im)
    dark=(47,53,47);amber=(209,138,74)
    # Fixed label regions are stationary in this supporting scene. Replace from
    # before the first reveal through the last fade to avoid original-text flashes.
    if 132.35<=t<139.15:
        # Flatten only the text interior, using the current dark-card intensity
        # to carry its existing dissolve. Golden key pixels are restored below.
        sample=np.median(rgb[302:310,595:610].reshape(-1,3),axis=0)
        alpha=float(np.clip((244-float(sample.mean()))/195,0,1))
        fill=tuple(int(v) for v in sample)
        d.rectangle((594,310,865,375),fill=fill)
        fg=tuple(int(fill[i]*(1-alpha)+amber[i]*alpha) for i in range(3))
        sub=tuple(int(fill[i]*(1-alpha)+245*alpha) for i in range(3))
        d.text((730,327),'PERMISSION PROBLEM',font=face('heavy',19),fill=fg,anchor='mm')
        d.text((730,358),'Access restricted',font=face('medium',17),fill=sub,anchor='mm')
    if 136.4<=t<139.15:
        # Replace the invented .env/config.bak filename with the narrated fact.
        d.rounded_rectangle((409,142,655,253),radius=17,fill=(249,255,251),outline=(141,115,166),width=2)
        d.text((532,183),'KEY FOUND',font=face('heavy',20),fill=dark,anchor='mm')
        d.text((532,216),'Broad access',font=face('medium',18),fill=amber,anchor='mm')
    if t>=139.15:
        # Cover the command and its unsupported total-purge claim inside the
        # existing label, leaving its boundary and trash animation visible.
        sample=np.median(rgb[300:308,440:470].reshape(-1,3),axis=0)
        fill=tuple(int(v) for v in sample)
        alpha=float(np.clip((244-float(sample.mean()))/190,0,1))
        d.rectangle((480,310,824,369),fill=fill)
        fg=tuple(int(fill[i]*(1-alpha)+v*alpha) for i,v in enumerate((239,247,243)))
        d.text((651,331),'DELETION REQUEST',font=face('heavy',21),fill=fg,anchor='mm')
        d.text((651,357),'Database and backups',font=face('medium',16),fill=fg,anchor='mm')
        # Original byte-count caption replaced across its fade-in.
        sample=np.median(rgb[538:544,851:871].reshape(-1,3),axis=0)
        fill=tuple(int(v) for v in sample)
        alpha=float(np.clip((244-float(sample.mean()))/110,0,1))
        d.rectangle((859,548,1108,575),fill=fill)
        fg=tuple(int(fill[i]*(1-alpha)+255*alpha) for i in range(3))
        d.text((984,562),'DATABASE DELETED',font=face('heavy',17),fill=fg,anchor='mm')
    arr=np.asarray(im).copy()
    # Restore the moving key foreground where it crosses the permission label.
    if 136.4<=t<139.15:
        hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        key=(cv2.inRange(hsv,(19,70,65),(40,255,255)))
        roi=np.zeros_like(key);roi[260:440,420:1090]=key[260:440,420:1090]
        n, labels, stats, _ = cv2.connectedComponentsWithStats(roi, 8)
        # Orange lettering produces tiny components; only the large moving key
        # is foreground. Restoring all gold pixels would restore old text flecks.
        clean=np.zeros_like(roi)
        if n>1:
            k=1+int(np.argmax(stats[1:,cv2.CC_STAT_AREA]))
            if stats[k,cv2.CC_STAT_AREA]>150:
                clean[labels==k]=255
        roi=cv2.dilate(clean,np.ones((5,5),np.uint8),iterations=1)
        arr[roi>0]=rgb[roi>0]
    return cv2.cvtColor(arr,cv2.COLOR_RGB2BGR)

def board_frames():
    im=cv2.imread(str(BOARD));h,w=im.shape[:2]
    # Whole current board fitted with margins; no crop or camera change.
    scale=680/h;bw=round(w*scale);bh=680;ox=(1280-bw)//2;oy=20
    bg=tuple(int(v) for v in im[4,4]);canvas=np.full((720,1280,3),bg,np.uint8)
    canvas[oy:oy+bh,ox:ox+bw]=cv2.resize(im,(bw,bh),interpolation=cv2.INTER_AREA)
    ring=Image.fromarray(cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(ring)
    rect=tuple(round(v*scale+(ox if i%2==0 else oy)) for i,v in enumerate(QUOTE))
    d.rounded_rectangle(rect,radius=11,outline='#4f2fc4',width=4)
    return canvas,cv2.cvtColor(np.asarray(ring),cv2.COLOR_RGB2BGR),dict(scale=scale,offset=[ox,oy],quote_rect=rect,stroke_px=4)

def main():
    cv2.setNumThreads(2)
    assert sha(SRC)==EXPECTED,'Source changed; old frame coordinates are unsafe'
    assert not DEST.exists(),'Never overwrite a review candidate'
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    protected={str(p):sha(p) for p in [SRC,BOARD,ROOT/'index.html',ROOT/'lessons/rise-of-agents.md']}
    # Decode original audio once. Outside a four-ms quiet splice bridge, all
    # PCM samples are retained exactly, with no new pauses or level changes.
    pcm=subprocess.check_output([FF,'-v','error','-i',str(SRC),'-vn','-ac','1','-ar',str(RATE),'-f','s16le','-'])
    a=np.frombuffer(pcm,dtype='<i2').astype(np.float64)[:N*1600]
    edited=np.r_[a[:CUT_A*1600],a[CUT_B*1600:]]
    join=CUT_A*1600;edited[join-96:join+96]=np.linspace(edited[join-96],edited[join+95],192)
    assert len(edited)==TOTAL*1600
    wav(OUT/'edited.wav',edited);wav(OUT/'join-context.wav',edited[(CUT_A-165)*1600:(CUT_A+180)*1600])
    board,ring,geom=board_frames()
    decode=subprocess.Popen([FF,'-v','error','-threads','2','-i',str(SRC),'-an','-f','rawvideo','-pix_fmt','bgr24','pipe:1'],stdout=subprocess.PIPE)
    temp=OUT/'rendering.mp4';assert not temp.exists()
    cmd=[FF,'-v','warning','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-threads','2','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)]
    encode=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    wants={3633,3800,3885,3990,4050,4110,4140,4160,4180,4200,4250,4283,4300,4400,4413,4749,4758,4759,5633}
    count=0
    for f in range(N):
        buf=decode.stdout.read(1280*720*3)
        assert len(buf)==1280*720*3,(f,len(buf))
        if CUT_A<=f<CUT_B:continue
        frame=np.frombuffer(buf,np.uint8).reshape(720,1280,3)
        if 3633<=f<3885:frame=board
        elif 3885<=f<4283:frame=patch_scene(frame,f)
        elif 4283<=f<4759:frame=ring if f>=4286 else board
        if f in wants:cv2.imwrite(str(OUT/'preview'/f'source-{f:06d}-output-{count:06d}.jpg'),frame)
        encode.stdin.write(frame.tobytes());count+=1
        if f%900==0:print(f'Rendered source {f/30:.0f}s',flush=True)
    decode.stdout.close();assert decode.wait()==0
    encode.stdin.close();assert encode.wait()==0 and count==TOTAL
    assert all(sha(p)==h for p,h in protected.items()),'Source or lesson changed during build'
    temp.rename(DEST)
    manifest=dict(candidate=str(DEST),candidate_sha256=sha(DEST),source=str(SRC),source_sha256=EXPECTED,
        source_limitation='Only finished v4 survives; decoded once and final H264 encoded once at CRF16.',
        approval='User approved repair plan and said Build it please.',fps=30,total_frames=TOTAL,duration=TOTAL/30,
        cut=dict(source_frames=[CUT_A,CUT_B],source_seconds=[CUT_A/30,CUT_B/30],words='In 2025, a Google Gemini agent wiped out a user’s project files ... I have failed you completely and catastrophically.',output_join_frame=CUT_A),
        picture_changes=[dict(source_frames=[3633,3885],kind='corrected canonical board'),dict(source_frames=[3885,4283],kind='label corrections preserving original animation'),dict(source_frames=[4283,4759],kind='corrected board and quote ring, minus removed interval')],
        boundary_frames=[3633,3885,4283,CUT_A,4759-(CUT_B-CUT_A)],board=geom,board_sha256=sha(BOARD),
        audio=dict(rate=RATE,channels=1,join_smoothing_ms=4,added_pauses=False,gain_changes=False,listening='Not auditioned; join-context.wav provided'),protected_hashes=protected,
        scope='Review candidate only; canonical MP4 and lesson video reference unchanged. Local lesson and prep factual correction included.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',DEST,TOTAL/30,flush=True)

if __name__=='__main__':main()
