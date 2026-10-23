#!/usr/bin/env python3
"""Approved donor repair: roll 6 prompt, edited roll 7 close, +1 s topic pause."""
from pathlib import Path
import json,subprocess,sys,functools
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader,sha,writewav
from build_embeddings_v7 import Renderer
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/what-is-ai-build-v14-2026-10-22'
DEST=ROOT/'Prompts/what-is-ai-v14.mp4'
SOURCES={'base':ROOT/'Prompts/what-is-ai-v11.mp4','everyday':ROOT/'Prompts/why-learn-ai-v10.mp4','six':ROOT/'Prompts/What-is-ai-6.mp4','seven':ROOT/'Prompts/what-is-ai-7.mp4'}
HASHES={'base':'e7713536d479f329277efacfd6d052efcdb66852c50eca83b26b6e5e44905785','everyday':'f7cab5a37d9c1f8ae141f1f2bcfadb441dd4341dedad782eb1684b63e9c6bd79','six':'0ea948aee5ccae77726d64f8ce665cb3b4955292c196c94428e7acef70b00166','seven':'f8b2a0606fb2ff52b9fe02ea9119573f2c24e74ebbbfe398d1e36c40448595c3'}
PLAN=[('base',0,1284,0),('everyday',1197,3048,0),('pause',0,30,0),('base',1284,2196,0),('six',921,1182,1.7),('base',2427,2838,0),('seven',4716,4773,-1.3),('seven',5433,5502,3.9),('tail',0,120,0)]
TOTAL=4995;GEN=3936;SUMMARY=4581;CLOSE=4749
BOUNDARIES=[1284,3135,3165,3319,3756,3936,4077,4338,4581,4749,4806,4875]
def setup():
    OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    b=Build.__new__(Build);b.out=OUT
    asset=ROOT/'course-assets/what-is-ai/what-is-ai-types.jpg'
    canvas,cw,ch,ox,oy=b.compose(asset,'types');assert (cw,ch,ox,oy)==(2500,1408,450,53)
    specs={}
    old=ROOT/'video-audit/what-is-ai-working-v13-2026-10-22'
    for key in ['types-rec','types-summary']:
        s=json.loads((old/f'leg-{key}.json').read_text());s['image']=str(canvas);specs[key]=s
    full=[1250,704,2500];right=[1640,683.5,2039.493670886076]
    specs['types-gen']={'image':str(canvas),'fps':30,'out_w':1280,'out_h':720,'upscale':3,
      'beats':[{'label':'whole-board','frames':69,'from':full,'to':full},{'label':'complete-card-dive','frames':24,'to':right},{'label':'hold-complete-card','frames':552,'to':right}],
      'rings':[{'start':a,'end':z,'rect':r,'color':'#4f2fc4','pad':0,'radius':14} for a,z,r in [(69,151,[1287,678,705,96]),(151,416,[1287,798,705,181]),(416,645,[1287,1008,705,160])]]}
    for k,s in specs.items():(OUT/f'leg-{k}.json').write_text(json.dumps(s,indent=2)+'\n')
    close=OUT/'close.png'
    if not close.exists():subprocess.run([sys.executable,str(ROOT/'scripts/video/make_close_board.py'),'--lesson','llms','--out',str(close)],check=True)
    return specs,{k:Renderer(s) for k,s in specs.items()},cv2.imread(str(close))

def mapping():return [(k,n) for k,a,z,gain in PLAN for n in range(a,z)]
class Visuals:
    def __init__(self):
        self.specs,self.renderers,self.close=setup();self.readers={k:Reader(p) for k,p in SOURCES.items() if k in ['base','everyday']};self.hold=None
    @functools.lru_cache(maxsize=8)
    def closing(self,n):
        q=float(np.clip((n-48)/149,0,1));z=1+.2*q*q*(3-2*q)
        h,w=self.close.shape[:2];cw,ch=round(w/z),round(h/z);x,y=(w-cw)//2,(h-ch)//2
        return cv2.resize(self.close[y:y+ch,x:x+cw],(1280,720),interpolation=cv2.INTER_LANCZOS4)
    def at(self,out,k,n):
        if out>=CLOSE:return self.closing(out-CLOSE)
        if out>=SUMMARY:return self.renderers['types-summary'].at(out-SUMMARY)[0]
        if out>=GEN:return self.renderers['types-gen'].at(out-GEN)[0]
        if k=='pause':return self.hold.copy()
        if k=='base' and 1438<=n<1875:return self.renderers['types-rec'].at(n-1438)[0]
        im=self.readers[k].at(n)
        if k=='everyday' and n==3047:self.hold=im.copy()
        return im

def pcm(p):
    raw=subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1'])
    return np.frombuffer(raw,np.float32).copy()
def roomtone(seed,count):
    # Loop a measured quiet source segment with a short overlap at each repeat.
    overlap=240;out=seed.copy();ramp=np.linspace(0,1,overlap)
    while len(out)<count:
        out[-overlap:]=out[-overlap:]*(1-ramp)+seed[:overlap]*ramp
        out=np.concatenate([out,seed[overlap:]])
    return out[:count].copy()
def prepare_audio():
    aud={k:pcm(p) for k,p in SOURCES.items()};parts=[];rows=[];cursor=0
    for i,(k,a,z,gain) in enumerate(PLAN):
        if k=='pause':part=roomtone(aud['everyday'][round(101.32*48000):round(101.55*48000)],(z-a)*1600)
        elif k=='tail':part=roomtone(aud['seven'][round(183.2*48000):round(183.5*48000)],(z-a)*1600)*10**(3.9/20)
        else:part=aud[k][a*1600:z*1600].copy()*10**(gain/20)
        assert len(part)==(z-a)*1600
        fade=96 if k=='seven' and a==5433 else 240
        if i:part[:fade]*=np.linspace(0,1,fade)
        if i<len(PLAN)-1:part[-240:]*=np.linspace(1,0,240)
        parts.append(part);rows.append(dict(source=k,source_start=a,source_end=z,gain_db=gain,start_frame=cursor,end_frame=cursor+z-a));cursor+=z-a
    assert cursor==TOTAL
    x=np.concatenate(parts);assert np.max(np.abs(x))<1
    writewav(OUT/'edited.wav',x*32768)
    return rows
def main():
    assert not DEST.exists(),'Never overwrite a candidate'
    assert all(sha(SOURCES[k])==h for k,h in HASHES.items())
    v=Visuals();rows=prepare_audio()
    protected={str(p):sha(p) for p in [ROOT/'index.html',ROOT/'lessons/what-is-ai.md',ROOT/'course-assets/what-is-ai/what-is-ai.mp4',ROOT/'course-assets/what-is-ai/what-is-ai-types.jpg',ROOT/'course-assets/what-is-ai/what-is-ai-close.jpg',ROOT/'course-assets/why-learn-ai/why-learn-ai.mp4']}
    m=dict(candidate=str(DEST),frames=TOTAL,fps=30,duration=TOTAL/30,sources={k:dict(path=str(p),sha256=HASHES[k]) for k,p in SOURCES.items()},timeline=rows,boundaries=BOUNDARIES,protected=protected,specs=v.specs,close=dict(start=CLOSE,prehold=48,push=150,settle=TOTAL-CLOSE-198,zoom=1.2),approval='Owner explicitly authorized roll 6 prompt explanation and editing roll 7 closing instead of rerolling, plus the previously approved additional one-second topic pause.',scope='Review candidate only; no installation or publication.',audio_note='Source-matched room tone for additional pause and final tail. Donor gains match active RMS approximately. Second closing line starts at 181.100 s within the initial s consonant, removing you need to; 2 ms ramp.',source_limitation='Reassembled from v11 and Why Learn v10 finished sources plus raw rolls 6/7, avoiding another encode of v13. Direct listening unavailable.')
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    wanted={3319,3428,3486,3591,3936,4005,4030,4087,4150,4352,4450,4581,4641,4749,4797,4806,4875,4947,4994}
    ff=imageio_ffmpeg.get_ffmpeg_exe();p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for out,(k,n) in enumerate(mapping()):
        im=v.at(out,k,n);p.stdin.write(im.tobytes())
        if out in wanted:cv2.imwrite(str(OUT/'preview'/f'planned-{out:05d}.jpg'),im)
        if out%900==899:print('Rendered',out+1,flush=True)
    p.stdin.close();assert p.wait()==0
    assert all(sha(Path(p))==h for p,h in protected.items())
    m['render_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
