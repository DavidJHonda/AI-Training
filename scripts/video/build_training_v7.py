#!/usr/bin/env python3
"""Approved Training visual repair: four drawing breaks and 4px highlights.
The published v6 is the only surviving source. Audio is stream-copied.
No canonical file is changed. --prepare-only writes inspection frames.
"""
from pathlib import Path
import argparse, functools, hashlib, json, shutil, subprocess, tempfile
import cv2
import imageio_ffmpeg
import numpy as np
from editspec_build import Build
from ken_burns_path import resolve, rings_for, window, smoothstep, ring_px
from build_understand_ai_opener_v12 import draw_ring

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/training/training.mp4'
EXPECTED='01a8b51a707a59d6c29288ee9d86c5500aa5546882dc45c26b307f80d1755ebe'
OLD=ROOT/'video-audit/training-comparison-2026-09-22/build-v6'
OUT=ROOT/'video-audit/training-repair-2026-09-27-v7'
DEST=ROOT/'Prompts/training-v7.mp4'
FPS,TOTAL=30,8696
# Output frames are on the current published timeline. Donor ranges are half-open.
BREAKS=[dict(key='weights',start=1470,end=1680,donor_start=750,donor_end=867),
        dict(key='basketball-pre',start=4200,end=4440,donor_start=327,donor_end=557),
        dict(key='basketball-inst',start=5490,end=5760,donor_start=327,donor_end=557),
        dict(key='basketball-pref',start=6960,end=7350,donor_start=327,donor_end=557)]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def mapping(old):
    result=[None]*TOTAL
    for row in old['timeline']:
        for f in range(row['start_frame'],min(row['end_frame'],TOTAL)):
            if f>=old['close']['start_frame']:continue
            if row['kind']=='room_tone':result[f]=result[f-1]
            elif row.get('visual') in old['boards']:
                key=row['visual']; result[f]=(key,row.get('video_start',row['source_start'])+f-row['start_frame']-old['boards'][key]['src_in'])
    return result

class Renderer:
    def __init__(self,spec):
        self.spec=spec; im=cv2.imread(spec['image']);self.ih,self.iw=im.shape[:2]; self.up=spec['upscale']
        self.big=cv2.resize(im,(self.iw*self.up,self.ih*self.up),interpolation=cv2.INTER_LANCZOS4)
        self.rings=rings_for(spec);self.cameras=[]
        for label,n,a,b in resolve(spec,16/9,1280,self.up):
            for k in range(n):
                t=smoothstep(k/(n-1)) if n>1 else 1
                self.cameras.append(tuple(a[j]+(b[j]-a[j])*t for j in range(3)))
    def geometry(self,local):
        camera=self.cameras[local]; active=tuple(i for i,r in enumerate(self.rings) if r[0]<=local<r[1])
        return camera,active
    @functools.lru_cache(maxsize=8)
    def render(self,camera,active):
        x,y,w,h=window(*camera,16/9,self.iw,self.ih);up=self.up
        xx,yy,ww,hh=[int(round(v*up)) for v in (x,y,w,h)]
        base=cv2.resize(self.big[yy:yy+hh,xx:xx+ww],(1280,720),interpolation=cv2.INTER_AREA if ww>1280 else cv2.INTER_LANCZOS4)
        frame=base.copy();geo=[]
        for i in active:
            a,b,(rx,ry,rw,rh),color,pad,radius=self.rings[i];scale=1280/w;t=ring_px(720);half=t/2
            box=[(rx-pad-x)*scale-half,(ry-pad-y)*scale-half,(rx+rw+pad-x)*scale+half,(ry+rh+pad-y)*scale+half]
            assert box[0]-half>=0 and box[1]-half>=0 and box[2]+half<1280 and box[3]+half<720,box
            draw_ring(frame,*box,color,radius*scale+half,t)
            geo.append(dict(centerline=box,color_bgr=color,ring_index=i))
        return frame,base,geo
    def at(self,n):return self.render(*self.geometry(n))

def runs(mapping_,breaks):
    result=[]
    for f,item in enumerate(mapping_):
        key=item[0] if item and not any(b['start']<=f<b['end'] for b in breaks) else None
        if key:
            if result and result[-1]['key']==key and result[-1]['end']==f:result[-1]['end']=f+1
            else:result.append(dict(key=key,start=f,end=f+1))
    for r in result:r['seconds']=(r['end']-r['start'])/FPS
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    assert sha(SOURCE)==EXPECTED,'Source has changed'
    assert not DEST.exists(),'Never overwrite a review candidate'
    OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    record=OUT/'source-snapshot.json'
    if record.exists():snapshot=Path(json.loads(record.read_text())['path'])
    else:
        snapshot=Path(tempfile.mkdtemp(prefix='training-v7-'))/'source-v6.mp4';shutil.copyfile(SOURCE,snapshot)
        record.write_text(json.dumps(dict(path=str(snapshot),sha256=EXPECTED),indent=2))
    assert sha(snapshot)==EXPECTED
    old=json.loads((OLD/'edit-manifest.json').read_text());assert old['render_sha256']==EXPECTED
    protected=[SOURCE,ROOT/'lessons/training.md',*sorted((ROOT/'course-assets/training').glob('*.jpg'))]
    hashes={str(p):sha(p) for p in protected};build=Build(ROOT,snapshot,OUT,DEST,protected=protected);build.tall_margin=True
    specs={};renderers={}
    for key,b in old['boards'].items():
        asset=ROOT/b['asset'];assert sha(asset)==b['sha256']
        canvas,cw,ch,ox,oy=build.compose(asset,key);assert [ox,oy]==b['canvas_offset']
        spec=json.loads((OLD/f'leg-{key}.json').read_text());spec['image']=str(canvas)
        # Compact setup board remains at full view; remove its tiny legacy push.
        if key=='before':spec['beats'][0]['to']=spec['beats'][0]['from']
        spec['provenance']=dict(asset=str(asset),sha256=sha(asset),density=b['density'],ring_px=ring_px(720),rasterizer='supersampled rounded rectangle difference')
        specs[key]=spec;renderers[key]=Renderer(spec);(OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2))
    mapped=mapping(old)
    # Read selected donors sequentially: exclude basketball entrance/exit dissolves
    # and the weights entrance dissolve. Play each once, hold its last clean frame.
    donor={};cap=cv2.VideoCapture(str(snapshot))
    selected=set(f for b in BREAKS for f in range(b['donor_start'],b['donor_end']))
    for f in range(max(selected)+1):
        ok,im=cap.read();assert ok
        if f in selected:donor[f]=im
    cap.release()
    # Inspect every ring at a settled, visible state plus each full-board opening.
    samples=[];seen=set()
    for f,item in enumerate(mapped):
        if item is None or any(b['start']<=f<b['end'] for b in BREAKS):continue
        key,local=item;r=renderers[key];camera,active=r.geometry(local)
        state=(key,active)
        if state in seen:continue
        # Exclude moving cameras and first 12 frames of each ring for compression measurements.
        if active and (local<12 or camera!=r.cameras[max(0,local-12)] or any(local-r.rings[i][0]<12 for i in active)):continue
        frame,base,geo=r.at(local);cv2.imwrite(str(OUT/'preview'/f'{f:05d}-{key}.png'),frame)
        cv2.imwrite(str(OUT/'preview'/f'{f:05d}-{key}-base.png'),base)
        samples.append(dict(frame=f,key=key,local=local,rings=geo));seen.add(state)
    (OUT/'preview-samples.json').write_text(json.dumps(samples,indent=2))
    boundaries=old['boundaries']+[dict(frame=b[e],label=f"{b['key']}-{'in' if e=='start' else 'out'}") for b in BREAKS for e in ['start','end']]
    rr=runs(mapped,BREAKS);chains=[]
    for r in rr:
        if chains and chains[-1][1]==r['start']:chains[-1][1]=r['end']
        else:chains.append([r['start'],r['end']])
    manifest=dict(scope='Approved narrow visual repair; review only, no publication.',approval='David: Build it please, following Training plan.',
        source=str(SOURCE),source_snapshot=str(snapshot),source_sha256=EXPECTED,output=str(DEST),fps=FPS,total_frames=TOTAL,duration=TOTAL/FPS,
        audio='Original AAC stream copied; all narration, pauses and existing grafts unchanged.',boards=specs,notebook_interleaves=BREAKS,
        donor_treatment='Play selected existing animation once at original speed, then hold its final clean frame for remaining break time.',
        board_runs=rr,board_chains=chains,longest_board_seconds=max(r['seconds'] for r in rr),longest_board_chain_seconds=max((b-a)/FPS for a,b in chains),
        boundaries=sorted(boundaries,key=lambda b:b['frame']),protected_hashes=hashes,close=dict(start=8402,end=TOTAL,treatment='Original source picture'),
        limitations=['Only finished published video survives; retained picture re-encoded once.', 'No real-time end-to-end playback/listening or mobile review.',
        'Opening paper-craft imagery and original Notebook loop diagrams retained outside approved replacement scope.',
        'Weights donor contains illustrative numeric labels and an Optimal Output label from the original source, not measured model results.'],
        approved_pacing_exceptions='Residual phase-board runs 28.87s, 25.47s and 27.80s; setup board 20.63s. No extra filler or pauses.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
    if args.prepare_only:print('Prepared candidate frames and timeline.');return
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-n','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(snapshot),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);cap=cv2.VideoCapture(str(snapshot));count=0
    while True:
        ok,frame=cap.read()
        if not ok:break
        br=next((b for b in BREAKS if b['start']<=count<b['end']),None)
        if br:frame=donor[min(br['donor_start']+count-br['start'],br['donor_end']-1)]
        elif mapped[count]:
            key,local=mapped[count];frame=renderers[key].at(local)[0]
        proc.stdin.write(frame.tobytes());count+=1
        if count%900==0:print(f'Encoded {count}/{TOTAL}',flush=True)
    cap.release();proc.stdin.close();assert proc.wait()==0;assert count==TOTAL
    manifest['render_sha256']=sha(DEST);manifest['encode_command']=cmd
    manifest['protected_files_unchanged']={p:sha(p)==h for p,h in hashes.items()};assert all(manifest['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print(DEST,flush=True)

if __name__=='__main__':
    cv2.setNumThreads(1);main()
