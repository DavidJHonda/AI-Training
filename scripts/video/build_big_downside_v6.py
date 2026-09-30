#!/usr/bin/env python3
"""User-requested localized de-clicks and earlier guardrail board; retain v5 repairs.
Rebuild from the hash-pinned shipped source in one encode, never from v5.
"""
from pathlib import Path
import json, subprocess
import numpy as np
import cv2
import build_big_downside_v5 as config
from editspec_build import readwav, writewav, sha, Reader
b=config.b
b.OUT=b.ROOT/'video-audit/big-downside-repair-2026-09-30-v6'
b.DEST=b.ROOT/'Prompts/big-downside-v6.mp4'
GUARD=b.ROOT/'course-assets/big-downside/big-downside-safety-guardrails.jpg'
GUARD_A,GUARD_B=2262,2333
# Small repair windows around reported clicks. Context is filtered first, then
# only these regions are used, avoiding the filter's segment-start transient.
PATCHES=[(37,40,38.60,39.00),(175,179,177.00,177.35)]
original_prepare=b.prepare
base_reader=b.Reader
patch_records=[]

def prepare():
    build,source,edited,board,geom,history,overlays=original_prepare()
    before=edited.copy()
    for start,end,a,z in PATCHES:
        stem=b.OUT/f'declick-{start}'
        writewav(stem.with_suffix('.in.wav'),source[start*b.SR:end*b.SR])
        proc=subprocess.run([build.ff,'-y','-i',str(stem.with_suffix('.in.wav')),'-af','adeclick=t=4:b=2:a=2','-c:a','pcm_s16le',str(stem.with_suffix('.out.wav'))],capture_output=True,text=True,check=True)
        stem.with_suffix('.log').write_text(proc.stderr)
        filtered=readwav(stem.with_suffix('.out.wav'))
        ia,iz=round(a*b.SR),round(z*b.SR)
        part=filtered[ia-start*b.SR:iz-start*b.SR].copy()
        weight=np.ones(len(part));weight[:240]=np.linspace(0,1,240);weight[-240:]=np.linspace(1,0,240)
        edited[ia:iz]=np.rint(source[ia:iz]*(1-weight)+part*weight)
        patch_records.append(dict(seconds=[a,z],context_seconds=[start,end],filter='adeclick=t=4:b=2:a=2',ramps_ms=5,changed_samples=int(np.count_nonzero(edited[ia:iz]!=before[ia:iz])),peak_correction=int(np.max(abs(edited[ia:iz]-before[ia:iz])))))
        writewav(b.OUT/f'before-{start}.wav',before[start*b.SR:end*b.SR])
        writewav(b.OUT/f'after-{start}.wav',edited[start*b.SR:end*b.SR])
    writewav(b.OUT/'edited.wav',edited)
    # The existing board was rendered from this exact current canonical JPG.
    # Extend its literal first unmarked frame backwards so the old seam disappears.
    old=json.loads((b.ROOT/'video-audit/big-downside-v2-2026-09-24/build-v3/edit-manifest.json').read_text())
    assert sha(GUARD)==old['protected_hashes'][str(GUARD)]
    r=base_reader(b.SRC);guard_frame=r.at(GUARD_B);r.c.release()
    class EarlyBoardReader(base_reader):
        def at(self,n):
            frame=super().at(n)
            return guard_frame.copy() if GUARD_A<=n<GUARD_B else frame
    b.Reader=EarlyBoardReader
    cv2.imwrite(str(b.OUT/'preview'/'guardrail-early.jpg'),guard_frame)
    return build,source,edited,board,geom,history,overlays

b.prepare=prepare
if __name__=='__main__':
    b.main()
    p=b.OUT/'edit-manifest.json';m=json.loads(p.read_text())
    m['approval']='User feedback: audio glitches around 0:38 and 2:57; show board at This chart around 1:16. Narrow repair; no shipping authorization.'
    m['audio']['other_PCM_unchanged']=False
    m['audio']['localized_declicks']=patch_records
    m['guardrail_extension']=dict(asset=str(GUARD),sha256=sha(GUARD),output_span=[GUARD_A,GUARD_B],frame_from_source=GUARD_B,treatment='Extend first canonical unmarked board frame; existing subsequent motion and highlights unchanged.')
    m['boundaries']=[dict(frame=GUARD_A,label='early canonical guardrail board'),dict(frame=GUARD_B,label='resume existing guardrail motion')]+m['boundaries']
    p.write_text(json.dumps(m,indent=2)+'\n')
