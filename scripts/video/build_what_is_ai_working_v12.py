#!/usr/bin/env python3
"""Approved working assembly: everyday AI graft, updated types, no closing."""
from pathlib import Path
import json, subprocess, sys
import cv2, numpy as np, imageio_ffmpeg
from editspec_build import Build, Reader, sha, writewav
from build_embeddings_v7 import Renderer

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/what-is-ai-working-v12-2026-10-22'
DEST=ROOT/'Prompts/what-is-ai-v12.mp4'
SOURCES={'base':ROOT/'Prompts/what-is-ai-v11.mp4','donor':ROOT/'Prompts/why-learn-ai-v10.mp4'}
HASHES={'base':'e7713536d479f329277efacfd6d052efcdb66852c50eca83b26b6e5e44905785','donor':'f7cab5a37d9c1f8ae141f1f2bcfadb441dd4341dedad782eb1684b63e9c6bd79'}
KEEP=[('base',0,1272),('donor',1197,3048),('base',1272,2196),('base',2313,2838)]
OLD=ROOT/'video-audit/what-is-ai-build-2026-09-29-v11'
ASSET=ROOT/'course-assets/what-is-ai/what-is-ai-types.jpg'

def setup():
    OUT.mkdir(exist_ok=True); (OUT/'preview').mkdir(exist_ok=True)
    b=Build.__new__(Build); b.out=OUT
    canvas,cw,ch,ox,oy=b.compose(ASSET,'types')
    assert (cw,ch,ox,oy)==(2500,1408,450,53)
    specs={}
    for key in ['types-rec','types-summary']:
        s=json.loads((OLD/f'leg-{key}.json').read_text()); s['image']=str(canvas); specs[key]=s
    full=[1250,704,2500]; right=[1640,683.5,2039.493670886076]
    specs['types-gen']={'image':str(canvas),'fps':30,'out_w':1280,'out_h':720,'upscale':3,
      'beats':[{'label':'return-whole','frames':69,'from':full,'to':full},
               {'label':'to-complete-generative-card','frames':24,'to':right},
               {'label':'hold-complete-card','frames':522,'to':right}],
      'rings':[{'start':a,'end':z,'rect':rect,'color':'#4f2fc4','pad':0,'radius':14}
               for a,z,rect in [(69,141,[1287,678,705,96]),
                                (141,385,[1287,798,705,181]),(385,615,[1287,1008,705,160])]]}
    renderers={k:Renderer(s) for k,s in specs.items()}
    for k,s in specs.items(): (OUT/f'leg-{k}.json').write_text(json.dumps(s,indent=2)+'\n')
    return specs,renderers

def visual(n):
    if 1438<=n<1875:return 'types-rec',n-1438
    if 2055<=n<2670:return 'types-gen',n-2055
    if 2670<=n<2838:return 'types-summary',n-2670
    return None

def main():
    assert not DEST.exists(),'Do not overwrite review candidates'
    assert all(sha(SOURCES[k])==v for k,v in HASHES.items())
    specs,renderers=setup()
    protected={str(p):sha(p) for p in [ROOT/'index.html',ROOT/'lessons/what-is-ai.md',
        ROOT/'course-assets/what-is-ai/what-is-ai.mp4',ROOT/'course-assets/why-learn-ai/why-learn-ai.mp4',
        ASSET,ROOT/'course-assets/why-learn-ai/why-learn-ai-everyday.jpg']}
    ff=imageio_ffmpeg.get_ffmpeg_exe(); audio={}
    for k,p in SOURCES.items():
        raw=subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1'])
        audio[k]=np.frombuffer(raw,np.float32).copy()
    parts=[]; timeline=[]; cursor=0
    for i,(k,a,z) in enumerate(KEEP):
        part=audio[k][a*1600:z*1600].copy(); assert len(part)==(z-a)*1600
        if i:part[:240]*=np.linspace(0,1,240)
        if i<len(KEEP)-1:part[-240:]*=np.linspace(1,0,240)
        parts.append(part); timeline.append(dict(source=k,source_start=a,source_end=z,start_frame=cursor,end_frame=cursor+z-a)); cursor+=z-a
    edited=np.concatenate(parts); writewav(OUT/'edited.wav',edited*32768)
    mapping=[(k,n) for k,a,z in KEEP for n in range(a,z)]
    previews=[]
    for out,(k,n) in enumerate(mapping):
        item=visual(n) if k=='base' else None
        if item and (item[1] in [0,59,68,83,108,140,166,200,271,300,384,400,500,614]):
            im=renderers[item[0]].at(item[1])[0]; name=f'{out:05d}-{item[0]}.jpg'
            cv2.imwrite(str(OUT/'preview'/name),im); previews.append(name)
    manifest=dict(candidate=str(DEST),sources={k:dict(path=str(p),sha256=HASHES[k]) for k,p in SOURCES.items()},
        fps=30,frames=cursor,duration=cursor/30,timeline=timeline,protected=protected,
        board=dict(asset=str(ASSET),sha256=sha(ASSET),offset=[450,53],specs=specs),
        board_source_spans=[[1438,1875,'types-rec'],[2055,2670,'types-gen'],[2670,2838,'types-summary']],
        boundaries=[1272,3123,3289,3726,3906,4047,4404],previews=previews,
        approval='Approved working version: insert everyday AI, update types, omit obsolete comparison and closing. No ship.',
        source_limitation='Assembled from verified finished v11 and v10 sources; one additional video/audio encode.',
        audio='48 kHz mono; 5 ms ramps within measured silence at three new joins; no gain change or added pauses.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if '--prepare-only' in sys.argv:return
    p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
        '-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','18',
        '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    readers={k:Reader(v) for k,v in SOURCES.items()}
    for out,(k,n) in enumerate(mapping):
        item=visual(n) if k=='base' else None
        im=renderers[item[0]].at(item[1])[0] if item else readers[k].at(n)
        p.stdin.write(im.tobytes())
        if out%900==899:print('Rendered',out+1,flush=True)
    p.stdin.close();assert p.wait()==0
    for r in readers.values():r.c.release()
    assert all(sha(Path(p))==h for p,h in protected.items())
    manifest['render_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':main()
