#!/usr/bin/env python3
"""Owner-requested banner, pre-question pause, and spoken-choice cues."""
import json, subprocess
from pathlib import Path
import cv2, numpy as np
import build_how_ai_answers_v15 as previous
from build_embeddings_v7 import Renderer
from editspec_build import sha

base=previous.base;ROOT=base.ROOT;FF=base.FF
OUT=ROOT/'video-audit/how-ai-answers-cues-v16-2026-11-09'
DEST=ROOT/'Prompts/how-ai-answers-v16.mp4'
SOURCE=ROOT/'Prompts/how-ai-answers-v15.mp4'
EXPECTED='868053d29e39724862a544b44af9438faccdaf62bd2510536f05b7fbc9b88964'
PAUSE_AT=2052;ADDED=18;TOTAL=base.TOTAL+ADDED
# Measured v15 speech onsets, checked against the retained medium.en words.
# Half-open spans. The last row ends with its spoken percentage.
CUES=[(2237,2285,0,'You'),(2285,2344,1,'A'),(2344,2370,2,'Great'),
      (3272,3325,0,'Spot'),(3325,3397,1,'Max'),(3397,3426,2,'Buddy')]
def out_frame(f):return f+(ADDED if f>=PAUSE_AT else 0)
def source_frame(n):
    if PAUSE_AT<=n<PAUSE_AT+ADDED:return None
    return n if n<PAUSE_AT else n-ADDED

def audio():
    base.assemble_audio()
    p=OUT/'assembled-audio.f32';a=np.fromfile(p,np.float32).reshape(-1,2)
    old=ROOT/'video-audit/how-ai-answers-tighten-v15-2026-11-09/assembled-audio.f32'
    assert np.array_equal(a,np.fromfile(old,np.float32).reshape(-1,2))
    k=PAUSE_AT*1600;seed=a[round(68.34*48000):round(68.43*48000)].copy()
    tone=np.tile(np.concatenate([seed,seed[::-1]]),(4,1))[:ADDED*1600].copy()
    assert len(tone)==ADDED*1600
    ramp=np.linspace(0,1,240,dtype=np.float32)[:,None]
    tone[:240]=a[k-1]*(1-ramp)+tone[:240]*ramp
    tone[-240:]=tone[-240:]*(1-ramp)+a[k]*ramp
    result=np.concatenate([a[:k],tone,a[k:]])
    assert np.array_equal(result[:k],a[:k]) and np.array_equal(result[k+len(tone):],a[k:])
    assert np.max(np.abs(result[k]-result[k-1]))<1e-8
    assert np.max(np.abs(result[k+len(tone)]-result[k+len(tone)-1]))<1e-8
    result.tofile(p)
    return dict(insert_v15_frame=PAUSE_AT,insert_v15_seconds=PAUSE_AT/30,added_frames=ADDED,added_seconds=ADDED/30,
        existing_spoken_gap_seconds=.42,target_spoken_gap_seconds=1.02,
        tone_seed_seconds=[68.34,68.43],tone_rms=float(np.sqrt(np.mean(tone*tone))),retained_pcm_identical=True)

def main():
    assert not DEST.exists();assert sha(SOURCE)==EXPECTED
    OUT.mkdir(exist_ok=True);(OUT/'expected').mkdir(exist_ok=True)
    base.OUT=OUT;base.DEST=DEST;base.recover_source()
    protected={str(p):sha(p) for p in [SOURCE,ROOT/'course-assets/how-ai-answers/how-ai-answers.mp4',ROOT/'lessons/how-ai-answers.md',*sorted((ROOT/'course-assets/how-ai-answers').glob('*.jpg'))]}
    pause=audio();_,original,_,refs=base.original_setup()
    spec=json.loads((OUT/'reconstruction/leg-b2.json').read_text())
    spec['rings']=[r for r in spec['rings'] if r['label']!='takeaway']
    spec['rings'][0]['start']=round(61.9*30)-1472
    bridge=Renderer(spec)
    (OUT/'reconstruction/leg-b2-no-banner.json').write_text(json.dumps(spec,indent=2))
    holds={}
    for f in [2576,base.V11[base.MAPPING[2046]]]:
        rd=base.old.Reader(base.SOURCE);holds[f]=original(f,rd);rd.c.release()
    hold=holds[base.V11[base.MAPPING[2046]]]
    old=json.loads((ROOT/'video-audit/how-ai-answers-tighten-v15-2026-11-09/edit-manifest.json').read_text())
    boundaries={out_frame(n) for n in old['boundaries'] if n!=2047}
    boundaries.update([PAUSE_AT,PAUSE_AT+ADDED])
    boundaries.update(out_frame(f) for a,b,_,_ in CUES for f in (a,b))
    samples={0,TOTAL-1,*[out_frame(f) for f in [1656,1657,1680,1683,1684,2046,2047,2051,2052,2055,3680,4300]]}
    samples.update([PAUSE_AT-1,PAUSE_AT,PAUSE_AT+ADDED-1,PAUSE_AT+ADDED])
    samples.update(out_frame(f) for a,b,_,_ in CUES for f in [a-1,a,a+2,(a+b)//2,b-1,b])
    manifest=dict(candidate=str(DEST),base=str(SOURCE),base_sha256=EXPECTED,source=str(base.SOURCE),source_sha256=base.SOURCE_SHA,
        scope='Three requested changes only: remove unspoken banner ring, short pause before question reprise, cue each spoken probability choice.',
        frames=TOTAL,fps=30,duration_seconds=TOTAL/30,pause=pause,boundaries=sorted(boundaries),
        removed_banner_ring_v15_frames=[1657,1684],
        choice_cues=[dict(token=t,row=r,v15_frames=[a,b],output_frames=[out_frame(a),out_frame(b)]) for a,b,r,t in CUES],
        highlight='Blue 4px row outline for the spoken choice; existing purple outline and flight for the selected token.',
        picture_pause='Hold preceding loop scene through the extended gap; reveal the question board immediately before the spoken reprise.',
        protected=protected,approval='David requested the banner deletion, short pre-question pause and spoken-choice highlights on November 9, 2026.',
        publication='Review candidate only',listening_performed=False,continuous_playback_performed=False)
    (OUT/'edit-plan.json').write_text(json.dumps(manifest,indent=2))
    proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
        '-f','f32le','-ar','48000','-ac','2','-i',str(OUT/'assembled-audio.f32'),'-map','0:v:0','-map','1:a:0',
        '-c:v','libx264','-threads','4','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    reader=base.old.Reader(base.SOURCE)
    for n in range(TOTAL):
        s=source_frame(n)
        if s is None or 2047<=s<PAUSE_AT:im=hold.copy()
        else:
            f=base.MAPPING[s]
            if base.DEMO[0]<=f<base.DEMO[1]:
                row=next((r for a,b,r,_ in CUES if a<=s<b),-1)
                im=base.scene.render_state(base.scene.signature(f),True,row).copy()
            elif 1766<=f<2517:im=bridge.at(f-1472)[0].copy()
            elif 2803<=f<2819:im=holds[2576].copy()
            else:
                oldf=base.V11[f];im=original(oldf,reader)
                if base.old.DOG[0]<=oldf<base.old.DOG[1]:im,_=base.old.dog(im)
                if base.old.EOS[0]<=oldf<base.old.EOS[1]:im,_=base.old.brighten(im,refs)
        if n in samples:cv2.imwrite(str(OUT/'expected'/f'{n:05d}.png'),im)
        proc.stdin.write(im.tobytes())
        if (n+1)%900==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    proc.stdin.close();assert proc.wait()==0;reader.c.release()
    assert all(sha(Path(p))==h for p,h in protected.items())
    manifest['candidate_sha256']=sha(DEST);(OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
    print(DEST,flush=True)

if __name__=='__main__':main()
