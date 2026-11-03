#!/usr/bin/env python3
"""Decode and verify the v11 candidate; listening is explicitly not certified."""
from pathlib import Path
import json,subprocess,sys
import cv2,numpy as np
from PIL import Image,ImageDraw
import build_pace_of_change_v11 as b

def main():
    cv2.setNumThreads(2)
    m=json.loads((b.OUT/'edit-manifest.json').read_text());spans=m['visual_timeline'];n=m['frames']
    boundaries=sorted(set([r['start_frame'] for r in spans[1:]]+m['audio_joins']))
    wanted=set(range(0,n,120))|{n-1}
    for r in spans:wanted.update([r['start_frame'],min(r['start_frame']+30,r['end_frame']-1),r['end_frame']-1])
    for f in boundaries:wanted.update([f-1,f,f+1])
    views,_=b.board_views();cap=cv2.VideoCapture(str(b.DEST));frames={};count=0;checks=[];prev=None;cuts=[]
    assert cap.get(cv2.CAP_PROP_FPS)==30
    assert (cap.get(cv2.CAP_PROP_FRAME_WIDTH),cap.get(cv2.CAP_PROP_FRAME_HEIGHT))==(1280,720)
    while True:
        ok,im=cap.read()
        if not ok:break
        small=cv2.resize(im,(320,180),interpolation=cv2.INTER_AREA)
        if prev is not None and np.abs(small.astype(float)-prev).mean()>12:cuts.append(count)
        prev=small.astype(float)
        if count in wanted:
            frames[count]=cv2.cvtColor(small,cv2.COLOR_BGR2RGB)
            row=next(r for r in spans if r['start_frame']<=count<r['end_frame'])
            if row['state'][0]=='board':
                expected=views[tuple(row['state'][1:])]
                mad=float(np.abs(im.astype(float)-expected.astype(float)).mean());assert mad<4,(count,mad)
                checks.append(dict(frame=count,mad=mad,state=row['state']))
            if count==n-1 or count==min(row['start_frame']+30,row['end_frame']-1):cv2.imwrite(str(b.OUT/f'encoded-{count:06d}.jpg'),im)
        count+=1
    cap.release();assert count==n,(count,n)
    raw=subprocess.check_output([b.FF,'-v','error','-i',str(b.DEST),'-vn','-ar','48000','-ac','1','-f','s16le','-'])
    actual=np.frombuffer(raw,dtype='<i2').astype(float);reference=b.readwav(b.OUT/'edited.wav')
    assert len(actual)>=len(reference);actual=actual[:len(reference)]
    snr=float(10*np.log10(np.sum(reference**2)/np.sum((actual-reference)**2)));assert snr>25,snr
    donors={i:b.readwav(b.OUT/f'source-{i}.wav') for i in (1,2)}
    original=np.concatenate([donors[r['roll']][r['source_start']*1600:r['source_end']*1600]*10**(r['gain_db']/20) for r in m['audio_timeline']])
    mask=np.ones(len(original),bool)
    for f in m['audio_joins']:mask[f*1600-240:f*1600+240]=False
    parity=np.array_equal(original[mask].astype(np.int16).astype(float),reference[mask]);assert parity
    joins=[]
    for f in m['audio_joins']:
        x=actual[(f*1600-480):(f*1600+480)]/32768
        joins.append(dict(output_frame=f,seconds=f/30,local_peak_dbfs=float(20*np.log10(max(abs(x).max(),1e-9))),jump_dbfs=float(20*np.log10(max(abs(x[480]-x[479]),1e-9)))))
    for k,start in enumerate(range(0,len(sorted(wanted)),16)):
        sheet=Image.new('RGB',(1280,800),'white');d=ImageDraw.Draw(sheet)
        for i,f in enumerate(sorted(wanted)[start:start+16]):
            x=i%4*320;y=i//4*200;sheet.paste(Image.fromarray(frames[f]),(x,y+20));d.text((x+5,y+3),f'{f/30:.2f}s f{f}',fill='black')
        sheet.save(b.OUT/f'qa-sheet-{k:02d}.jpg',quality=93)
    # Three consecutive frames at each edit make first-frame correctness easy to inspect.
    for k,start in enumerate(range(0,len(boundaries),6)):
        sheet=Image.new('RGB',(960,1200),'white');d=ImageDraw.Draw(sheet)
        for i,f in enumerate(boundaries[start:start+6]):
            for j,offset in enumerate((-1,0,1)):
                x=j*320;y=i*200;sheet.paste(Image.fromarray(frames[f+offset]),(x,y+20));d.text((x+5,y+3),f'{(f+offset)/30:.2f}s f{f+offset}',fill='black')
        sheet.save(b.OUT/f'seam-summary-{k:02d}.jpg',quality=93)
    runs=[];start=None;kind=None
    for r in spans:
        state=r['state'];new=state[1] if state[0]=='board' else None
        if new!=kind:
            if kind is not None:runs.append(dict(board=kind,start=start/30,end=r['start_frame']/30,seconds=(r['start_frame']-start)/30))
            kind=new;start=r['start_frame']
    protected=all(b.sha(Path(p))==h for p,h in m['protected_hashes'].items());assert protected
    result=dict(decoded_frames=count,duration=count/30,dimensions=[1280,720],fps=30,encoded_audio_snr_db=snr,preencode_audio_unchanged_outside_gain_and_join_handles=parity,
                board_frame_checks=len(checks),maximum_board_frame_mad=max(r['mad'] for r in checks),audio_join_measurements=joins,board_runs=runs,
                longest_board_only_run_seconds=max(r['seconds'] for r in runs),detected_visual_cuts=cuts,protected_files_unchanged=protected,
                listening_completed=False,continuous_playback_review_completed=False)
    (b.OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (b.OUT/'board-comparison.json').write_text(json.dumps(checks,indent=2)+'\n')
    command=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'transition-guard')]
    # Fast animation yields many frame deltas; those are not scene boundaries.
    # Audit every authored splice plus isolated native cuts. Retain the complete
    # unfiltered delta list in verification.json for examination of animation.
    isolated=[f for i,f in enumerate(cuts) if (i==0 or f-cuts[i-1]>24) and (i==len(cuts)-1 or cuts[i+1]-f>24)]
    for f in sorted(set(boundaries+isolated)):command+=['--boundary',f'{f}:edit-or-source-scene']
    subprocess.run(command,check=True)
    print(json.dumps({k:v for k,v in result.items() if k not in ('audio_join_measurements','board_runs','detected_visual_cuts')},indent=2),flush=True)

if __name__=='__main__':main()
