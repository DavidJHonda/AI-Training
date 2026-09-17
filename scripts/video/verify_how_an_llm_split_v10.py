#!/usr/bin/env python3
"""Read-only checks of the exact encoded v10; writes audit evidence only."""
from pathlib import Path
import json
import re
import subprocess
import cv2
import numpy as np
from build_how_an_llm_works_v10_review import OUT,DEST,ROOT,TOTAL,SPF,SR
from editspec_build import readwav,sha
import imageio_ffmpeg


def main():
    m=json.loads((OUT/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
    qa=OUT/'encoded-checks';qa.mkdir(exist_ok=True)
    states={};sourcewant={};checks={}
    for key,b in m['boards'].items():
        n=b['src_out']-b['src_in']
        want={0,n-1,*[min(n-1,r['start']+26) for r in b['rings']]}
        for f in want:states.setdefault(b['src_in']+f,[]).append(f'{key}-f{f:05d}')
    for row in m['timeline']:
        if row['visual']=='source':
            for f in set([row['end_frame']-1,*range(row['start_frame'],row['end_frame'],30)]):
                sourcewant[f]=row['label']
    states[TOTAL-1]=['final-close']
    c=cv2.VideoCapture(str(DEST));fps=c.get(cv2.CAP_PROP_FPS);size=[int(c.get(3)),int(c.get(4))]
    f=0;visualcells=[];sourcecells=[]
    while True:
        ok,im=c.read()
        if not ok:break
        if f in states:
            for label in states[f]:
                cv2.imwrite(str(qa/f'{label}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
                cell=cv2.resize(im,(640,360));cv2.putText(cell,f'{f/30:.2f}s {label}',(8,24),cv2.FONT_HERSHEY_SIMPLEX,.55,(0,0,200),2)
                visualcells.append(cell)
        if f in sourcewant:
            cell=cv2.resize(im,(480,270));cv2.putText(cell,f'{f/30:.2f}s f{f}',(8,24),cv2.FONT_HERSHEY_SIMPLEX,.6,(0,0,200),2)
            sourcecells.append(cell)
        f+=1
    c.release();assert f==TOTAL and fps==30 and size==[1280,720],(f,fps,size)
    for prefix,cells,cols,batch in [('board-states',visualcells,2,8),('kept-drawings',sourcecells,3,12)]:
        for k in range(0,len(cells),batch):
            chunk=cells[k:k+batch]
            while len(chunk)%cols:chunk.append(np.zeros_like(chunk[0]))
            cv2.imwrite(str(qa/f'{prefix}-{k//batch:02d}.jpg'),cv2.vconcat([cv2.hconcat(chunk[i:i+cols]) for i in range(0,len(chunk),cols)]))
    checks.update(decoded_frames=f,fps=fps,size=size,render_sha256=sha(DEST))
    checks['protected_unchanged']={p:sha(p)==h for p,h in m['protected_hashes'].items()}
    assert all(checks['protected_unchanged'].values())
    master=readwav(OUT/'edited.wav');assert len(master)==TOTAL*SPF
    head=10**(m['audio']['final_headroom_gain_db']/20)
    equivalence=[]
    for r in m['audio']['timeline']:
        name=Path(r['source']).stem.replace('how-the-model-','')
        source=readwav(OUT/f'{name}.wav')
        expected=(source[r['source_in']*SPF:r['source_out']*SPF]*10**(r['gain_db']/20)*head).astype(np.int16)
        actual=master[r['start_frame']*SPF:r['end_frame']*SPF]
        error=float(abs(expected[240:-240].astype(float)-actual[240:-240]).max())
        assert error==0,(name,error)
        equivalence.append(dict(source=name,output_frames=[r['start_frame'],r['end_frame']],max_sample_error_excluding_5ms_handles=error))
    checks['source_speech_preservation']=equivalence
    proc=subprocess.run([ff,'-hide_banner','-i',str(DEST),'-af','loudnorm=I=-18:TP=-2:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    checks['encoded_loudness']=json.JSONDecoder().raw_decode(proc.stderr[proc.stderr.rfind('{'):])[0]
    assert float(checks['encoded_loudness']['input_tp'])<0
    proc=subprocess.run([ff,'-hide_banner','-i',str(DEST),'-af','silencedetect=noise=-35dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True)
    (qa/'silencedetect.txt').write_text(proc.stderr)
    starts=re.findall(r'silence_start: ([0-9.]+)',proc.stderr)
    ends=re.findall(r'silence_end: ([0-9.]+)',proc.stderr)
    gaps=[(float(s),float(e)) for s,e in zip(starts,ends)]
    checks['audio_join_gaps']=[dict(join_frame=f,join_seconds=f/30,measured_gap=next(([s,e,e-s] for s,e in gaps if s<=f/30<=e),None)) for f in m['audio']['join_frames']]
    (qa/'verification.json').write_text(json.dumps(checks,indent=2))
    boundaries={r['start_frame']:r['label'] for r in m['timeline'][1:]}
    for i,f in enumerate(m['audio']['join_frames']):boundaries.setdefault(f,f'audio-join-{i+1}')
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions')]
    for f,label in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{label}']
    subprocess.run(cmd,check=True)
    print(json.dumps({k:v for k,v in checks.items() if k not in ('protected_unchanged','source_speech_preservation')},indent=2))


if __name__=='__main__':main()
