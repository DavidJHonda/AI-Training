#!/usr/bin/env python3
"""Verify the encoded v10 visual repair and unchanged copied AAC."""
import json, subprocess, sys
import cv2, numpy as np
import build_support_trap_v10 as edit
b=edit.b

def audio_hash(path):
    return subprocess.check_output([b.FF,'-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()

def main():
    out=b.OUT;qa=out/'qa';qa.mkdir(exist_ok=True)
    m=json.loads((out/'edit-manifest.json').read_text())
    cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(out/'transitions')]
    for r in m['boundaries']:cmd+=['--boundary',f'{r["frame"]}:{r["label"]}']
    subprocess.run(cmd,check=True)
    oldhash,newhash=audio_hash(edit.BASE),audio_hash(b.DEST);assert oldhash==newhash
    caps=[cv2.VideoCapture(str(p)) for p in [edit.BASE,b.DEST]]
    wants={f for r in m['boundaries'] if edit.START<=r['frame']<=edit.END for f in [r['frame']-1,r['frame'],r['frame']+5,r['frame']+12]}
    wants|={s['spoken_onset_source_frame']+15 for s in m['boards']['jobs']['states']}
    wants|={2773,8564};captured={};samples=[];pts=[];diff=[];n=0
    while True:
        ok,im=caps[1].read();oldok,old=caps[0].read()
        assert ok==oldok
        if not ok:break
        pts.append(caps[1].get(cv2.CAP_PROP_POS_MSEC))
        if not edit.START<=n<edit.END and n%15==0:
            diff.append(float(np.abs(cv2.resize(im,(320,180)).astype(float)-cv2.resize(old,(320,180)).astype(float)).mean()))
        if n in wants:
            captured[n]=im;cv2.imwrite(str(qa/f'{n:06d}.jpg'),im)
        if edit.START<=n<edit.END and n%60==0:
            tile=cv2.resize(im,(426,240));cv2.putText(tile,f'{n/30:.2f}s / {n}',(6,20),0,.6,(0,0,255),1);samples.append(tile)
        n+=1
    for c in caps:c.release()
    assert n==m['total_frames']==8565
    assert np.allclose(np.diff(pts),1000/30,atol=.001)
    assert max(diff)<1.0,max(diff)
    for i in range(0,len(samples),12):
        cells=samples[i:i+12]
        while len(cells)%3:cells.append(np.zeros_like(cells[0]))
        cv2.imwrite(str(qa/f'changed-{i//12:02d}.jpg'),cv2.vconcat([cv2.hconcat(cells[k:k+3]) for k in range(0,len(cells),3)]))
    strips=[]
    for r in m['boundaries']:
        f=r['frame']
        if not edit.START<=f<=edit.END:continue
        cells=[]
        for at in [f-1,f,f+5,f+12]:
            im=cv2.resize(captured[at],(320,180));cv2.putText(im,str(at),(6,20),0,.5,(0,0,255),1);cells.append(im)
        strips.append(cv2.hconcat(cells))
    for i in range(0,len(strips),4):cv2.imwrite(str(qa/f'seams-{i//4}.jpg'),cv2.vconcat(strips[i:i+4]))
    q=dict(decoded_frames=n,duration=n/30,fps=30,uniform_frame_timing=True,copied_AAC_identical=True,audio_sha256=newhash,
           unchanged_regions_sampled_every_frames=15,unchanged_regions_max_mean_pixel_difference=max(diff),
           protected_files_unchanged=m['protected_files_unchanged'],sha256=b.sha(b.DEST),
           scope='Narrow visual repair. Full continuous audiovisual playback and listening not performed; audio copied unchanged from v9.')
    (out/'qa-results.json').write_text(json.dumps(q,indent=2)+'\n')
    print(json.dumps({k:v for k,v in q.items() if k!='protected_files_unchanged'},indent=2),flush=True)

if __name__=='__main__':main()
