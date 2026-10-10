#!/usr/bin/env python3
"""Authorized Roll 2 visual pass; pristine source pictures and copied v7 audio."""
from pathlib import Path
import copy, json, subprocess, sys
import cv2
import numpy as np
from editspec_build import Reader, sha, fr
from build_big_downside_v7 import ROOT, FF, lesson_signature
from build_creative_thinking_v8 import BoardRenderer
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import smoothstep

PREV=ROOT/'video-audit/big-downside-build-2026-10-09-v7'
OUT=ROOT/'video-audit/big-downside-build-2026-10-10-v8'
BASE=ROOT/'Prompts/big-downside-v7.mp4'
DEST=ROOT/'Prompts/big-downside-v8.mp4'
DONOR=ROOT/'Prompts/big-downside-2.mp4'

def prepare():
    old=json.loads((PREV/'edit-manifest.json').read_text())
    assert sha(BASE)==old['render_sha256']
    for p,h in old['protected_hashes'].items():
        if p!=str(ROOT/'index.html'): assert sha(p)==h,p
    OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    inserts=[]
    def insert(label,a,z,s,e,why,anchors=None):
        inserts.append(dict(label=label,start_frame=fr(a),end_frame=fr(z),visual='source',
            video_source=str(DONOR),video_start=fr(s),video_end=fr(e),
            anchors=anchors,why=why,kind='roll2_insert'))
    insert('Rules become learned patterns',22.8,31.6666667,30.2,41.5,
           'Show the change from explicit rules to learned connections.',
           [[fr(22.8),fr(30.2)],[fr(26.7333333),fr(35.3)],[fr(31.6666667)-1,fr(41.5)-1]])
    insert('Dog-name example',31.6666667,36.3666667,41.5,45.5,
           'Make the dog-name question concrete, then return to incomplete explanation.')
    insert('Prompt bypasses guardrails',84.1666667,93.6333333,106.7,118.3666667,
           'Retain failed attempts, successful passage, and the final state before the board.')
    insert('Ordinary-looking voice request',122.3,125.6666667,166.6,171.2333333,
           'Show a benign-looking request, then return to the harmful combined plan.')
    insert('Complete unintended-route sequence',153.7333333,162.4,184.8333333,195.9666667,
           'Show the goal, boundary, unauthorized detour and reached-goal payoff.')
    insert('Completed-route reminder during incident',177.1333333,181.4666667,191.6333333,195.9666667,
           'Replace the earlier truncated excerpt with the completed route; no mid-route exit.')
    insert('Testing and updating is a continuing cycle',233.2666667,241.8,287.3666667,292.3666667,
           'Preserve the loop through the continuous-testing sentence; close follows it.')
    cuts=sorted({0,old['total_frames'],*[r['start_frame'] for r in old['timeline']],
                 *[r['end_frame'] for r in old['timeline']],
                 *[r['start_frame'] for r in inserts],*[r['end_frame'] for r in inserts]})
    timeline=[]
    for a,z in zip(cuts,cuts[1:]):
        override=next((r for r in inserts if r['start_frame']<=a<r['end_frame']),None)
        src=override or next(r for r in old['timeline'] if r['start_frame']<=a<r['end_frame'])
        r=copy.deepcopy(src)
        r.update(start_frame=a,end_frame=z,map_start=src['start_frame'],map_end=src['end_frame'],
                 kind='roll2_insert' if override else 'inherited')
        timeline.append(r)
    m=copy.deepcopy(old)
    m.update(output=str(DEST),base=str(BASE),base_sha256=sha(BASE),timeline=timeline,inserts=inserts,
             audio_timeline=old['timeline'],audio='AAC stream copied from v7 without decoding or re-encoding.',
             scope='User approved six Roll 2 visual candidates. Visual-only build; no installation or publishing.',
             protected_hashes={p:sha(p) for p in [*old['protected_hashes'],str(BASE)]},
             lesson_scope_sha256=lesson_signature((ROOT/'index.html').read_text()))
    for k in ['render_sha256','corner_mark','protected_files_unchanged','concurrent_index_change']:
        m.pop(k,None)
    m['close']=dict(start_frame=fr(241.8),prehold=48,push=150,endpoint=1.2,
                    settled=old['total_frames']-fr(241.8)-198)
    # Retain every prior boundary for comparison, even when a new insert spans it.
    labels={b['frame']:b['label'] for b in old['boundaries']}
    for r in inserts:
        labels[r['start_frame']]='Enter '+r['label'];labels[r['end_frame']]='Exit '+r['label']
    m['boundaries']=[dict(frame=f,label=label) for f,label in sorted(labels.items())]
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    return m

def source_frame(r,f):
    if r['kind']=='inherited':
        return min(r['video_start']+f-r['map_start'],r['video_end']-1)
    if r.get('anchors'):
        return round(float(np.interp(f,*np.array(r['anchors']).T)))
    return r['video_start']+round((f-r['map_start'])*(r['video_end']-r['video_start']-1)/(r['map_end']-r['map_start']-1))

def render(m):
    assert not DEST.exists(),'Never overwrite a review candidate'
    cv2.setNumThreads(2)
    boards={k:BoardRenderer(PREV/f'leg-{k}.json') for k in m['boards']}
    close=cv2.imread(str(PREV/'close.png'));mask=glyph_mask();readers={};counts={}
    process=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
        '-r','30','-i','pipe:0','-i',str(BASE),'-map','0:v:0','-map','1:a:0',
        '-c:v','libx264','-preset','fast','-crf','18','-threads','4','-pix_fmt','yuv420p',
        '-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for r in m['timeline']:
        key=r['visual']
        for f in range(r['start_frame'],r['end_frame']):
            if key in boards:im=boards[key].frame(f-m['boards'][key]['src_in'])
            elif key=='close':
                q=np.clip((f-m['close']['start_frame']-48)/149,0,1);z=1+.2*smoothstep(q)
                h,w=close.shape[:2];ww=w/z;hh=ww*9/16
                im=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),
                    (1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            else:
                path=r['video_source'];vf=source_frame(r,f);rd=readers.get(path)
                if rd is None or rd.n>vf:
                    if rd:rd.c.release()
                    rd=Reader(path);readers[path]=rd
                im,how=clean_frame(rd.at(vf),mask);counts[str(how)]=counts.get(str(how),0)+1
            if f in (r['start_frame'],r['end_frame']-1) or (r['kind']=='roll2_insert' and f%30==0):
                cv2.imwrite(str(OUT/'preview'/f'{f:06}.jpg'),im)
            process.stdin.write(im.tobytes())
        print(f"{r['end_frame']}/{m['total_frames']} {r['label']}",flush=True)
    process.stdin.close();assert process.wait()==0
    for rd in readers.values():rd.c.release()
    m.update(render_sha256=sha(DEST),corner_mark=counts,
             protected_files_unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()},
             lesson_scope_unchanged=lesson_signature((ROOT/'index.html').read_text())==m['lesson_scope_sha256'])
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    assert all(v for p,v in m['protected_files_unchanged'].items() if p!=str(ROOT/'index.html'))
    assert m['lesson_scope_unchanged']
    print('COMPLETE',DEST,flush=True)

if __name__=='__main__':
    m=prepare()
    if '--plan-only' not in sys.argv:render(m)
