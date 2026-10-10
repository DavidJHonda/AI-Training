#!/usr/bin/env python3
"""Verify copied audio, full decode, retained boards, new pictures and transitions."""
import hashlib,json,subprocess
import cv2,numpy as np
from build_big_downside_v8 import OUT,PREV,ROOT,BASE,DEST,FF,sha
from build_big_downside_v7 import lesson_signature
from build_creative_thinking_v8 import BoardRenderer

def stream_hash(path,pcm=False):
    args=[FF,'-v','error','-i',str(path),'-map','0:a:0','-c:a','pcm_s16le' if pcm else 'copy',
          '-f','hash','-hash','sha256','pipe:1']
    return subprocess.check_output(args,text=True).strip()

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text());assert sha(DEST)==m['render_sha256']
    audio={kind:{'v7':stream_hash(BASE,pcm),'v8':stream_hash(DEST,pcm)} for kind,pcm in [('packets',False),('pcm',True)]}
    for a in audio.values():assert a['v7']==a['v8'],audio
    boards={k:BoardRenderer(PREV/f'leg-{k}.json') for k in m['boards']}
    c=cv2.VideoCapture(str(DEST));assert c.get(cv2.CAP_PROP_FPS)==30
    original=cv2.VideoCapture(str(BASE));(OUT/'encoded-preview').mkdir(exist_ok=True)
    targets={0,m['total_frames']-1}
    for r in m['inserts']:
        targets.update(range(r['start_frame'],r['end_frame'],30));targets.add(r['end_frame']-1)
    for b in m['boundaries']:targets.update([b['frame']-1,b['frame']])
    checks=[];unchanged=[];overview=[];i=0
    while True:
        ok,im=c.read();ok0,old=original.read();assert ok==ok0
        if not ok:break
        assert im.shape==(720,1280,3)
        r=next(r for r in m['timeline'] if r['start_frame']<=i<r['end_frame'])
        if i in targets:
            cv2.imwrite(str(OUT/'encoded-preview'/f'{i:06}.jpg'),im)
            if r['visual'] in boards:
                ref=boards[r['visual']].frame(i-m['boards'][r['visual']]['src_in'])
                mad=float(np.abs(im.astype(float)-ref.astype(float)).mean());assert mad<4,(i,mad)
                checks.append(dict(frame=i,board=r['visual'],mad=mad))
        if i%60==0 and r['kind']=='inherited' and r['visual']!='close':
            mad=float(np.abs(im.astype(float)-old.astype(float)).mean());assert mad<3,(i,mad)
            unchanged.append(dict(frame=i,mad=mad))
        if i%240==0 or i==m['total_frames']-1:
            cell=cv2.resize(im,(384,216));cv2.putText(cell,f'{i/30:.2f}s',(8,24),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,230),2);overview.append(cell)
        i+=1
    c.release();original.release();assert i==m['total_frames']==7514
    while len(overview)%4:overview.append(np.full_like(overview[0],255))
    cv2.imwrite(str(OUT/'encoded-overview.jpg'),cv2.vconcat([cv2.hconcat(overview[j:j+4]) for j in range(0,len(overview),4)]))
    q=dict(decoded_frames=i,duration=i/30,fps=30,size=[1280,720],audio=audio,
           board_samples=checks,unchanged_samples=unchanged,
           protected_unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()},
           lesson_scope_unchanged=lesson_signature((ROOT/'index.html').read_text())==m['lesson_scope_sha256'],
           listening='Not directly auditioned. Exact AAC payload and decoded PCM equality verified.',
           motion='Full sequential decode; selected encoded animation states and boundary strips inspected separately.')
    (OUT/'qa.json').write_text(json.dumps(q,indent=2))
    assert all(v for p,v in q['protected_unchanged'].items() if p!=str(ROOT/'index.html'))
    assert q['lesson_scope_unchanged']
    print('DECODE, AUDIO, BOARDS, UNCHANGED PICTURES PASS',flush=True)
    cmd=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'transitions'),'--cut-threshold','8']
    for b in m['boundaries']:cmd+=['--boundary',f"{b['frame']}:{b['label']}"]
    result=subprocess.run(cmd)
    q['transition_guard_exit']=result.returncode
    (OUT/'qa.json').write_text(json.dumps(q,indent=2))
    print('TRANSITION STATUS',result.returncode,flush=True)

if __name__=='__main__':main()
