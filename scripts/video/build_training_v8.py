#!/usr/bin/env python3
"""Approved Training reorder, built once from published v6 and current boards.
Audio changes are the approved complete-sentence moves/cuts; no generated voice.
"""
from pathlib import Path
import argparse,json,shutil,tempfile,subprocess,wave
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader
from build_training_v7 import Renderer,mapping,sha,BREAKS

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/training/training.mp4'
EXPECTED='01a8b51a707a59d6c29288ee9d86c5500aa5546882dc45c26b307f80d1755ebe'
OLD=ROOT/'video-audit/training-comparison-2026-09-22/build-v6'
OUT=ROOT/'video-audit/training-repair-2026-09-27-v8'
DEST=ROOT/'Prompts/training-v8.mp4'
PLAN=ROOT/'video-audit/training-current-flow-review-2026-09-27/proposed-timeline.json'
FPS,SR,SPF=30,48000,1600

def picture_plan(rows,old):
    mapped=mapping(old);result=[]
    for row in rows:
        a,b=row['source_frames'];out_start=len(result)
        for sf in range(a,b):
            item=mapped[sf];kind='source';local=sf
            if item:kind,local=item
            # Begin the canonical board at the audio introduction, not one frame later.
            if row['label']=='Peanut-butter worked example' and sf==872:kind,local='loop',0
            if row['label']=='Pretraining introduction and scale' and sf<3334:kind,local='pre',0
            if row['label']=='Three-phase overview' and sf<2715:kind,local='drawing',min(380+sf-a,556)
            if row['label']=='Shared loop introduction':kind,local='drawing',min(435+sf-a,556)
            if row['label']=='Weights definition':kind,local='drawing',min(750+sf-a,866)
            for br in BREAKS:
                if br['start']<=sf<br['end']:
                    kind,local='drawing',min(br['donor_start']+sf-br['start'],br['donor_end']-1)
                    break
            result.append([kind,local,sf])
        row['output_frames']=[out_start,len(result)]
    return result

def board_runs(pics):
    result=[]
    for i,(key,local,sf) in enumerate(pics):
        if key in ('source','drawing'):continue
        if result and result[-1]['key']==key and result[-1]['end']==i:result[-1]['end']=i+1
        else:result.append(dict(key=key,start=i,end=i+1))
    for r in result:r['seconds']=(r['end']-r['start'])/30
    return result

def write_wav(p,x):
    with wave.open(str(p),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(x.astype('<i2').tobytes())

def prepare_audio(snapshot,rows):
    raw=subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(snapshot),'-vn','-ac','1','-ar',str(SR),'-f','s16le','-'])
    source=np.frombuffer(raw,dtype='<i2');pieces=[source[a*SPF:b*SPF].copy() for a,b in [r['source_frames'] for r in rows]]
    audio=np.concatenate(pieces).astype(float);seams=[];fade=240
    for i,row in enumerate(rows[1:],1):
        f=row['output_frames'][0];j=f*SPF;left=audio[j-fade:j].copy();right=audio[j:j+fade].copy()
        db=lambda x:float(20*np.log10(np.sqrt(np.mean(x*x))/32768+1e-12))
        assert max(db(left),db(right)) < -35,(f,db(left),db(right))
        common=(audio[j-1]+audio[j])/2;before=float(audio[j]-audio[j-1]);ramp=np.linspace(0,1,fade)
        audio[j-fade:j]=left*(1-ramp)+common*ramp;audio[j:j+fade]=common*(1-ramp)+right*ramp
        # Document quiet windows from 10ms RMS around the seam, without claiming audition.
        window=audio[max(0,j-SR):j+SR];v=window[:len(window)//480*480].reshape(-1,480)
        levels=20*np.log10(np.sqrt(np.mean(v*v,axis=1))/32768+1e-12);mid=100
        lo=mid;hi=mid
        while lo>0 and levels[lo-1]<-35:lo-=1
        while hi<len(levels) and levels[hi]<-35:hi+=1
        seams.append(dict(output_frame=f,output_seconds=f/30,from_source_frame=rows[i-1]['source_frames'][1],to_source_frame=row['source_frames'][0],left_5ms_dbfs=db(left),right_5ms_dbfs=db(right),sample_jump_before=before,sample_jump_after=float(audio[j]-audio[j-1]),quiet_gap_seconds=(hi-lo)/100,treatment='5ms smoothing on each quiet side to common boundary value; no samples inserted/deleted; no speech alteration',listening='Not auditioned'))
    audio=np.rint(audio).astype('<i2');write_wav(OUT/'edited.wav',audio)
    for i,s in enumerate(seams):
        j=s['output_frame']*SPF;write_wav(OUT/f"join-{i+1:02d}-{s['output_frame']:05d}.wav",audio[max(0,j-3*SR):j+4*SR])
    return seams

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    assert not DEST.exists(),'Never overwrite an existing review candidate';assert sha(SOURCE)==EXPECTED
    OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    rec=OUT/'source-snapshot.json'
    if rec.exists():snapshot=Path(json.loads(rec.read_text())['path'])
    else:
        snapshot=Path(tempfile.mkdtemp(prefix='training-v8-'))/'source-v6.mp4';shutil.copyfile(SOURCE,snapshot);rec.write_text(json.dumps(dict(path=str(snapshot),sha256=EXPECTED),indent=2))
    assert sha(snapshot)==EXPECTED
    old=json.loads((OLD/'edit-manifest.json').read_text());plan=json.loads(PLAN.read_text());assert sha(ROOT/'lessons/training.md')==plan['lesson_sha256']
    rows=plan['rows'];pics=picture_plan(rows,old);total=len(pics);assert total==8132
    (OUT/'frame-map.json').write_text(json.dumps(pics))
    protected=[SOURCE,ROOT/'lessons/training.md',*sorted((ROOT/'course-assets/training').glob('*.jpg'))]
    hashes={str(p):sha(p) for p in protected};b=Build(ROOT,snapshot,OUT,DEST,protected=protected);specs={};renderers={}
    for key,board in old['boards'].items():
        asset=ROOT/board['asset']
        if key!='pre':assert sha(asset)==board['sha256']
        canvas,cw,ch,ox,oy=b.compose(asset,key);assert [ox,oy]==board['canvas_offset']
        spec=json.loads((OLD/f'leg-{key}.json').read_text());spec['image']=str(canvas)
        if key=='before':spec['beats'][0]['to']=spec['beats'][0]['from']
        spec['provenance']=dict(asset=str(asset),sha256=sha(asset),density=board['density'],ring_px=4,pretraining_panel='Current What Pretraining Builds wording' if key=='pre' else None)
        # Setup's first ring still lands on 'First, engineers'; start 12f before it unmarked.
        specs[key]=spec;renderers[key]=Renderer(spec);(OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2))
    seams=prepare_audio(snapshot,rows)
    samples=[];seen=set()
    for f,(key,local,sf) in enumerate(pics):
        if key not in renderers:continue
        renderer=renderers[key];cam,active=renderer.geometry(local);state=(key,active)
        if state in seen:continue
        if active and (local<12 or cam!=renderer.cameras[max(0,local-12)] or any(local-renderer.rings[i][0]<12 for i in active)):continue
        frame,base,geo=renderer.at(local);cv2.imwrite(str(OUT/'preview'/f'{f:05d}-{key}.png'),frame);cv2.imwrite(str(OUT/'preview'/f'{f:05d}-{key}-base.png'),base)
        samples.append(dict(frame=f,key=key,local=local,rings=geo));seen.add(state)
    (OUT/'preview-samples.json').write_text(json.dumps(samples,indent=2))
    boundaries={s['output_frame']:'Narration reorder: '+rows[i+1]['label'] for i,s in enumerate(seams)}
    for f in range(1,total):
        if pics[f][0]!=pics[f-1][0]:boundaries.setdefault(f,f'{pics[f-1][0]} to {pics[f][0]}')
    for row in rows:
        a,e=row['source_frames'];out=row['output_frames'][0]
        for seam in old['boundaries']:
            if a<seam['frame']<e:boundaries.setdefault(out+seam['frame']-a,'Retained: '+seam['label'])
    runs=board_runs(pics);chains=[]
    for run in runs:
        if chains and chains[-1][1]==run['start']:chains[-1][1]=run['end']
        else:chains.append([run['start'],run['end']])
    drawings=[]
    for f,(key,local,sf) in enumerate(pics):
        if key!='drawing':continue
        if drawings and drawings[-1]['end']==f:drawings[-1]['end']=f+1
        else:drawings.append(dict(start=f,end=f+1,first_donor_frame=local))
        drawings[-1]['last_donor_frame']=local
    manifest=dict(scope='Approved Training lesson-flow repair; review candidate only.',approval='David: ok. Build the new version.',source=str(SOURCE),source_snapshot=str(snapshot),source_sha256=EXPECTED,output=str(DEST),fps=30,total_frames=total,duration=total/30,rows=rows,boards=specs,audio_seams=seams,notebook_interleaves=drawings,board_runs=runs,board_chains=chains,longest_board_seconds=max(x['seconds'] for x in runs),longest_board_chain_seconds=max((e-a)/30 for a,e in chains),boundaries=[dict(frame=f,label=label) for f,label in sorted(boundaries.items())],protected_hashes=hashes,limitations=['Exact new lesson bridge words are not present; approved equivalent existing narration used.','No real-time listening or mobile playback certification.','Only published source survives; picture and audio re-encoded once after approved edits.','Original opening paper-craft imagery and illustrative donor numerical labels retained.'])
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
    if args.prepare_only:print('Prepared board states, audio joins and timeline.');return
    needed={n for key,n,sf in pics if key=='drawing'};donors={};reader=Reader(snapshot)
    for n in sorted(needed):donors[n]=reader.at(n)
    reader.c.release()
    cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-n','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);reader=Reader(snapshot)
    for f,(key,n,sf) in enumerate(pics):
        if key in renderers:frame=renderers[key].at(n)[0]
        elif key=='drawing':frame=donors[n]
        else:
            if n<reader.n:reader.c.release();reader=Reader(snapshot)
            frame=reader.at(n)
        proc.stdin.write(frame.tobytes())
        if f%900==0:print(f'Encoded {f}/{total}',flush=True)
    reader.c.release();proc.stdin.close();assert proc.wait()==0
    manifest['render_sha256']=sha(DEST);manifest['encode_command']=cmd;manifest['protected_files_unchanged']={p:sha(p)==h for p,h in hashes.items()};assert all(manifest['protected_files_unchanged'].values());(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2));print(DEST,flush=True)

if __name__=='__main__':cv2.setNumThreads(1);main()
