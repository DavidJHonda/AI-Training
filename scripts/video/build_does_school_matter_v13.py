#!/usr/bin/env python3
"""Tighten the approved Skills pickup and refresh the current two-card board."""
from pathlib import Path
import json
import subprocess
import cv2
import imageio_ffmpeg
import numpy as np
from editspec_build import Reader, sha, writewav
from build_understand_ai_opener_v12 import draw_ring

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'video-audit/does-school-matter-skills-v13-2026-11-02'
SOURCE = ROOT/'Prompts/does-school-matter-v12.mp4'
DONOR = ROOT/'Prompts/does-school-matter-4.mp4'
DEST = ROOT/'Prompts/does-school-matter-v13.mp4'
ASSET = ROOT/'course-assets/does-school-matter/what-school-helps-you-build.jpg'
FPS, SPF = 30, 1600
# Half-open frame intervals; speech cuts were measured on decoded audio.
SPANS = [('base',0,3373), ('pickup',165,498), ('pickup',838,906),
         ('pickup',987,1255), ('base',3835,4251)]
TOTAL = sum(z-a for _,a,z in SPANS)
TAIL = TOTAL-(4251-3835)
SHIFT = TAIL-3835
CLOSE = 3954+SHIFT
TAKEAWAY = 3844+SHIFT
CUTAWAYS = [(3158,3281,3158,'subject-microscope'),
            (3426,3506,3516,'skills-model'),
            (3570,3699,3676,'people-meeting')]

def pcm(p):
    return np.frombuffer(subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),
        '-v','error','-i',str(p),'-vn','-ac','1','-ar','48000',
        '-f','f32le','pipe:1']),np.float32).copy()

def states():
    im=cv2.imread(str(ASSET)); assert im.shape[:2]==(917,1600)
    scale=720/917; w=round(1600*scale); x=(1280-w)//2
    base=np.full((720,1280,3),255,np.uint8)
    base[:,x:x+w]=cv2.resize(im,(w,720),interpolation=cv2.INTER_AREA)
    result={'full':base}
    for key,rect,token in [('knowledge',(40,118,784,749),'#4f2fc4'),
                           ('skills',(816,118,1560,749),'#1652f0'),
                           ('takeaway',(40,789,1560,877),'#6e51ff')]:
        f=base.copy(); a,b,c,d=rect
        color=tuple(int(token[i:i+2],16) for i in (5,3,1))
        draw_ring(f,x+a*w/1600,b*scale,x+c*w/1600,d*scale,color,14*scale,4)
        result[key]=f
    return result

class Visuals:
    def __init__(self):
        self.source=Reader(SOURCE); self.close=Reader(SOURCE)
        self.art=states(); self.drawings={}
        for a,z,s,label in CUTAWAYS:
            r=Reader(SOURCE)
            self.drawings[label]=[r.at(n) for n in range(s,s+z-a)]
            r.c.release()
    def at(self,n):
        if n<3013:return self.source.at(n)
        if n>=CLOSE:return self.close.at(n-SHIFT)
        for a,z,s,label in CUTAWAYS:
            if a<=n<z:return self.drawings[label][n-a]
        key=('full' if n<3035 else 'knowledge' if n<3307 else
             'skills' if n<TAIL else 'full' if n<TAKEAWAY else 'takeaway')
        return self.art[key]

def main():
    assert not DEST.exists(),'Never overwrite a review candidate'
    assert sha(SOURCE)=='4bad47278f8bdcd1e01b6dff6dfd6eb2a085b0493e10d8dec2a34a3170d5ade1'
    (OUT/'preview').mkdir(parents=True,exist_ok=True)
    if not (OUT/'pickup-matched.wav').exists():
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-n',
            '-i',str(DONOR),'-vn','-ac','1','-ar','48000','-af',
            'volume=4.8dB,alimiter=limit=0.94:level=false:latency=true',
            '-c:a','pcm_f32le',str(OUT/'pickup-matched.wav')],check=True)
    protected={str(p):sha(p) for p in [SOURCE,DONOR,ASSET,ROOT/'index.html',
        ROOT/'lessons/does-school-matter.md',ROOT/'course-assets/does-school-matter/does-school-matter.mp4']}
    audio={'base':pcm(SOURCE),'pickup':pcm(OUT/'pickup-matched.wav')}
    parts=[]; seams=[]; timeline=[]; cursor=0
    for i,(key,a,z) in enumerate(SPANS):
        part=audio[key][a*SPF:z*SPF].copy()
        if i:part[:240]*=np.linspace(0,1,240)
        if i<len(SPANS)-1:part[-240:]*=np.linspace(1,0,240)
        timeline.append(dict(source=key,start=a,end=z,output_start=cursor))
        cursor+=z-a
        if i<len(SPANS)-1:seams.append(cursor)
        parts.append(part)
    edited=np.concatenate(parts); assert len(edited)==TOTAL*SPF
    assert np.max(np.abs(audio['pickup']))<=.941
    # Float PCM preserves the existing AAC decoder's seven tiny >0 dBFS
    # overshoots without introducing integer clipping in unchanged audio.
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-y',
        '-f','f32le','-ar','48000','-ac','1','-i','pipe:0',
        '-c:a','pcm_f32le',str(OUT/'edited.wav')],input=edited.tobytes(),check=True)
    boundaries=[dict(frame=n,label=label) for n,label in
        [(3013,'updated-board'),(3035,'knowledge-highlight'),(3307,'skills-highlight'),
         (TAIL,'return-to-original-takeaway'),(TAKEAWAY,'takeaway-highlight'),(CLOSE,'original-close')]]
    boundaries += [dict(frame=n,label=f'audio-join-{i}') for i,n in enumerate(seams)]
    for a,z,s,label in CUTAWAYS:
        boundaries += [dict(frame=a,label=label),dict(frame=z,label=label+'-return')]
    plan=dict(scope='User-approved Skills narration tightening and updated board; local video replacement.',
        source=str(SOURCE),donor=str(DONOR),candidate=str(DEST),frames=TOTAL,fps=30,
        duration=TOTAL/30,timeline=timeline,audio_seam_frames=seams,tail_shift_frames=SHIFT,
        board=dict(path=str(ASSET),sha256=sha(ASSET),density='compact',
        source_dimensions=[1600,917],fit='Complete asset fitted to 720px height, white side bars',
        card_rectangles=[[40,118,784,749],[816,118,1560,749]],banner=[40,789,1560,877],
        ring_px=4,highlight_sequence=['Knowledge','Skills','takeaway']),
        cutaways=CUTAWAYS,boundaries=boundaries,protected=protected,
        audio='Pickup +4.8 dB to match measured -15.8 LUFS existing Skills; latency-compensated peak limiter at .94. 5ms edge ramps only at real audio cuts; no added pauses.',
        retained='Existing lead-in, Knowledge narration, school takeaway, closing and earlier video; supporting source drawings retained/retimed.',
        removed='Pickup intro, both abstract explanations, prerequisite clause, mechanical-step wording, duplicate takeaway and generated outro.',
        limitation='Direct listening unavailable; verify waveform, encoded transcription, frames and source preservation. Source body is existing finished v12.')
    (OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    v=Visuals()
    for name,im in v.art.items():cv2.imwrite(str(OUT/'preview'/f'board-{name}.png'),im)
    p=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-n',
        '-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
        '-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264',
        '-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for n in range(TOTAL):
        p.stdin.write(v.at(n).tobytes())
        if n%900==0:print(f'Rendered {n}/{TOTAL}',flush=True)
    p.stdin.close();assert p.wait()==0
    assert all(sha(Path(p))==h for p,h in protected.items())
    plan['candidate_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':main()
