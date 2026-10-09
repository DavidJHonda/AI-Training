#!/usr/bin/env python3
"""Approved visual-only One More Thing repair; review candidate, no publication.

Requires the exact Sept. 23 shipped bytes. Donor stills are sequentially extracted
into this active review folder and hash-recorded, so reuse never silently follows
a subsequently changed live filename. Original audio is stream-copied at mux.
"""
from pathlib import Path
import argparse, copy, json, subprocess
import cv2
import numpy as np
import imageio_ffmpeg
from editspec_build import Build, Reader, sha
from build_embeddings_v7 import Renderer

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'course-assets/the-next-token/the-next-token.mp4'
EXPECTED = 'bd076d8d401a95a87e82ad3e317766f61c4bce3985120e4e313971425ad3eea8'
OLD = ROOT / 'video-audit/one-more-thing-build-2026-09-23b'
OUT = ROOT / 'video-audit/one-more-thing-repair-2026-09-28-v12'
DEST = ROOT / 'Prompts/one-more-thing-v12.mp4'
TOTAL = 6717
# Half-open output-frame intervals; same length and FPS as the original.
PATCHES = [
 (505, 654, 'dog', 'Extend existing dog drawing through probability introduction'),
 (654, 1029, 'early-probabilities', 'Current probability board for Spot leading at 22%'),
 (1029, 1287, 'trials', 'Retain existing 100-trial illustration for the 22-in-100 explanation'),
 (1287, 1618, 'name', 'Name sketch replaces inconsistent sampling tree and joins original lead-in'),
 (1618, 2387, '1-draws', 'Current board, probability column then five picks, fixed 4px rings'),
 (2387, 2466, 'name', 'Brief drawing under another five picks could turn out differently'),
 (2466, 2751, '1-draws', 'Return for best chance is not a guarantee'),
 (4978, 5752, '3-bill', 'Current math board, complete cards, fixed 4px rings'),
 (5752, 5911, 'scale', 'Hypothetical-model illustration under estimates qualification'),
 (5911, 6315, '3-bill', 'Return for conclusion and preserve existing pause'),
]
STILLS = {'dog': 504, 'trials': 1215, 'name': 1560, 'scale': 4470}

def gentle_push(im, n, total, amount=.015):
    q = n / max(1, total-1); q = q*q*(3-2*q)
    z = 1 + amount*q
    h,w = im.shape[:2]; cw = w/z; ch=h/z
    return cv2.warpAffine(im, np.float32([[cw/1280,0,(w-cw)/2],[0,ch/720,(h-ch)/2]]),
                          (1280,720), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)

def prepare():
    assert sha(SRC) == EXPECTED, 'Live source changed; review and rebase before rendering'
    OUT.mkdir(exist_ok=True); (OUT/'preview').mkdir(exist_ok=True)
    old = json.loads((OLD/'edit-manifest.json').read_text())
    assert old['render_sha256'] == EXPECTED
    b=Build(ROOT,SRC,OUT,DEST)
    specs={}; renderers={}
    for key in ['1-draws','3-bill']:
        meta=old['boards'][key]; asset=ROOT/meta['asset']
        assert sha(asset)==meta['sha256']
        canvas,cw,ch,ox,oy=b.compose(asset,key)
        assert [ox,oy]==meta['canvas_offset']
        spec=json.loads((OLD/f'leg-{key}.json').read_text());spec['image']=str(canvas)
        specs[key]=spec;renderers[key]=Renderer(spec)
    early=copy.deepcopy(specs['1-draws'])
    full=early['beats'][0]['from']
    early['beats']=[{'label':'full probability board','frames':375,'from':full,'to':full}]
    early['rings']=[dict(early['rings'][0],start=71,end=375)]
    specs['early-probabilities']=early;renderers['early-probabilities']=Renderer(early)
    for key,spec in specs.items():(OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
    rd=Reader(SRC);stills={};provenance={}
    for key,f in sorted(STILLS.items(),key=lambda x:x[1]):
        im=rd.at(f);p=OUT/f'donor-{key}.png';cv2.imwrite(str(p),im)
        stills[key]=im;provenance[key]={'path':str(p),'sha256':sha(p),'source_frame':f,'source_sha256':EXPECTED}
    rd.c.release()
    protected={str(p):sha(p) for p in [SRC,ROOT/'lessons/the-next-token.md',ROOT/'gemini-notebook/the-next-token/PROMPT.txt',*sorted((ROOT/'course-assets/the-next-token').glob('*.jpg'))]}
    states=[]
    def frame(f):
        patch=next((p for p in PATCHES if p[0]<=f<p[1]),None)
        if not patch:return None
        a,z,key,_=patch
        if key in stills:
            return stills[key].copy() if key=='dog' else gentle_push(stills[key],f-a,z-a)
        start=654 if key=='early-probabilities' else 1618 if key=='1-draws' else 4978
        local=min(f-start,len(renderers[key].cameras)-1)
        return renderers[key].at(local)[0]
    # Preview each arrival/exit and every settled ring state that is actually shown.
    wanted=set()
    for a,z,key,label in PATCHES:wanted.update([a,(a+z)//2,z-1])
    for key,r in renderers.items():
        start=654 if key=='early-probabilities' else 1618 if key=='1-draws' else 4978
        for a,z,*_ in r.rings:
            f=start+a+15
            if any(p[0]<=f<p[1] and p[2]==key for p in PATCHES):wanted.add(f)
    for f in sorted(wanted):
        im=frame(f);p=OUT/'preview'/f'{f:06d}.jpg';cv2.imwrite(str(p),im)
        states.append({'frame':f,'path':str(p)})
    boundaries=sorted(set([p[i] for p in PATCHES for i in [0,1]]+[r['start_frame'] for r in old['timeline'][1:]]))
    manifest={'source':str(SRC),'source_sha256':EXPECTED,'candidate':str(DEST),'frames':TOTAL,'fps':30,'duration':TOTAL/30,
              'scope':'Approved visual-only repair. Copy original audio and preserve all pauses; no publication.',
              'patches':[dict(start_frame=a,end_frame=z,visual=k,reason=label) for a,z,k,label in PATCHES],
              'donor_stills':provenance,'boundaries':boundaries,'protected_hashes':protected,'prepared_states':states,
              'board_spans':[[654,1029],[1618,2387],[2466,2751],[3159,4096],[4978,5752],[5911,6315]],
              'longest_teaching_board_run_seconds':(4096-3159)/30,'longest_board_chain_including_close_seconds':(6717-5911)/30,
              'pacing_exceptions':'Temperature comparison retained 31.23s; first probability walk 25.63s; math walk 25.8s. No filler added.',
              'source_limitation':'Original raw rolls unavailable; one re-encode from exact shipped picture, with pristine canonical boards for changed board spans.',
              'listening_performed':False}
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return frame,manifest

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    assert not DEST.exists(),'Never overwrite a review candidate'
    frame,m=prepare();print('Prepared',TOTAL,'frames; longest teaching board',m['longest_teaching_board_run_seconds'],flush=True)
    if args.prepare_only:return
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
                           '-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast',
                           '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    rd=Reader(SRC)
    for f in range(TOTAL):
        im=frame(f)
        if im is None:im=rd.at(f)
        proc.stdin.write(im.tobytes())
        if f%1000==999:print('Rendered',f+1,flush=True)
    proc.stdin.close();assert proc.wait()==0;rd.c.release()
    m['render_sha256']=sha(DEST)
    m['protected_files_unchanged']={p:sha(Path(p))==h for p,h in m['protected_hashes'].items()}
    assert all(m['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()
