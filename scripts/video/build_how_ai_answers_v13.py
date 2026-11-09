#!/usr/bin/env python3
"""Approved redundancy cuts and landscape token motion. Review candidate only."""
import argparse, json, subprocess
from pathlib import Path
import cv2, numpy as np, imageio_ffmpeg
import build_how_ai_answers_v11 as old
import build_how_ai_answers_v12 as v12
import render_how_ai_answers_wide as scene
from editspec_build import sha

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/how-ai-answers-tighten-v13-2026-11-09'
DEST=ROOT/'Prompts/how-ai-answers-v13.mp4'
BASE=ROOT/'Prompts/how-ai-answers-v12.mp4'
SOURCE=Path('/private/tmp/how-ai-answers-v13-source.mp4')
SOURCE_SHA='c0e56437479d467ffaea26ff6ca51e93019e7cb18a041f3b980b038f7ff3f1fa'
BASE_SHA='26b6d74df4962884b4884afcf931218c8d4fd498d1d54a8f0a8d44b7ca2a5fd0'
FF=imageio_ffmpeg.get_ffmpeg_exe()
CUTS=[
    (1176,1766,'Repeated reading-to-writing setup and initial final-token preview'),
    (2247,2490,'Launching-pad restatement'),
    (2577,2803,'Repeated final-token probability calculation'),
    (3220,3408,'Repeated question-mark explanation, including solely'),
    (6023,6141,'First inference definition; retain the closing definition'),
]
MAPPING=[f for f in range(6448) if not any(a<=f<b for a,b,_ in CUTS)]
REVERSE={f:n for n,f in enumerate(MAPPING)}
V11=v12.frames()
TOTAL=len(MAPPING)
DEMO=(3106,4927)
EXTRA_HOLDS=[]

def recover_source():
    if not SOURCE.exists():
        data=subprocess.check_output(['git','show','ec30a9f5:course-assets/how-ai-answers/how-ai-answers.mp4'],cwd=ROOT)
        SOURCE.write_bytes(data)
    assert sha(SOURCE)==SOURCE_SHA

def original_setup():
    """Rebuild v11 picture from its source, redirecting all scratch to this audit."""
    rebuild=OUT/'reconstruction';rebuild.mkdir(exist_ok=True)
    old.OUT=rebuild;old.DEST=DEST
    v8=old.prior.prior.base
    original=v8.setup
    def redirected():
        (v8.OUT/'source-snapshot.json').write_text(json.dumps({'path':str(SOURCE)}))
        return original()
    v8.setup=redirected
    try:return old.setup()
    finally:v8.setup=original

def assemble_audio():
    raw=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(SOURCE),'-vn','-ar','48000','-ac','2','-f','f32le','pipe:1']),np.float32).reshape(-1,2)
    def fades(parts):
        for i,p in enumerate(parts):
            if i:p[:240]*=np.linspace(0,1,240,dtype=np.float32)[:,None]
            if i<len(parts)-1:p[-240:]*=np.linspace(1,0,240,dtype=np.float32)[:,None]
        return np.concatenate(parts)
    a=fades([raw[x*1600:y*1600].copy() for x,y in [(0,3108),(330,391),(3108,6221),(7309,7617)]])
    keep=[];start=0
    for x,y in v12.CUTS:keep.append((start,x));start=y
    keep.append((start,6590))
    a=fades([a[x*1600:y*1600].copy() for x,y in keep])
    assert len(a)==6448*1600
    ref=ROOT/'video-audit/how-ai-answers-guided-2026-10-06-v12/edited-audio.f32'
    if ref.exists():assert np.array_equal(a,np.fromfile(ref,np.float32).reshape(-1,2))
    a.tofile(OUT/'source-v12-audio.f32')
    keep=[];start=0;joins=[]
    for x,y,label in CUTS:
        keep.append((start,x));start=y
        joins.append(dict(label=label,source_frames=[x,y],source_seconds=[x/30,y/30],
            output_frame=REVERSE[y],output_seconds=REVERSE[y]/30,
            edge_rms=[float(np.sqrt(np.mean(a[k*1600-480:k*1600+480]**2))) for k in (x,y)]))
    keep.append((start,6448))
    untouched=np.concatenate([a[x*1600:y*1600] for x,y in keep])
    result=fades([a[x*1600:y*1600].copy() for x,y in keep])
    mask=np.ones(len(result),bool)
    for j in joins:mask[j['output_frame']*1600-240:j['output_frame']*1600+240]=False
    assert np.array_equal(result[mask],untouched[mask])
    assert max(max(j['edge_rms']) for j in joins)<.002
    result.tofile(OUT/'assembled-audio.f32')
    return joins

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    OUT.mkdir(exist_ok=True);(OUT/'expected').mkdir(exist_ok=True)
    recover_source();assert sha(BASE)==BASE_SHA
    protected={str(p):sha(p) for p in [BASE,ROOT/'course-assets/how-ai-answers/how-ai-answers.mp4',ROOT/'lessons/how-ai-answers.md',*sorted((ROOT/'course-assets/how-ai-answers').glob('*.jpg'))]}
    joins=assemble_audio()
    _,base_frame,previous,refs=original_setup()
    held=[]
    for a,b,source_frame in EXTRA_HOLDS:
        rd=old.Reader(SOURCE);im=base_frame(source_frame,rd);rd.c.release()
        held.append((a,b,im))
    # After cutting the board's spoken preamble, give the complete board a
    # two-second unmarked opening. Its first ring begins on "question mark".
    from build_embeddings_v7 import Renderer
    spec=json.loads((OUT/'reconstruction/leg-b2.json').read_text())
    spec['rings'][0]['start']=round(61.9*30)-1472
    bridge=Renderer(spec)
    old_manifest=json.loads((ROOT/'video-audit/how-ai-answers-guided-2026-10-06-v12/edit-manifest.json').read_text())
    boundaries={REVERSE[f] for f in old_manifest['boundaries'] if f in REVERSE and not DEMO[0]<f<DEMO[1]}
    boundaries.update(j['output_frame'] for j in joins)
    boundaries.update(REVERSE[f] for f in DEMO)
    for e in scene.EVENTS:
        boundaries.update(REVERSE[f] for f in e if f in REVERSE)
    samples={0,TOTAL-1,*[j['output_frame']+offset for j in joins for offset in (-1,0,1,25)]}
    samples.update(REVERSE[f] for e in scene.EVENTS for f in (*e,(e[2]+e[3])//2) if f in REVERSE)
    samples.update(REVERSE[f] for f in [3106,3500,4030,4300,4600,4926,5000,5600,5900] if f in REVERSE)
    plan=dict(candidate=str(DEST),based_on=str(BASE),base_sha256=BASE_SHA,source=str(SOURCE),source_sha256=SOURCE_SHA,
        source_recovery='git ec30a9f5:course-assets/how-ai-answers/how-ai-answers.mp4',
        scope='Approved narration tightening and video-only wider animated token demonstration. Two final-token teaching moments. Original dog-name explanation and complete close retained.',
        fps=30,frames=TOTAL,duration_seconds=TOTAL/30,removed_seconds=(6448-TOTAL)/30,cuts=joins,
        mapping_v12_frames=MAPPING,boundaries=sorted(boundaries),protected=protected,
        demo_output_frames=[REVERSE[f] for f in DEMO],
        scene_events=[dict(token=token,source_v12_frames=list(e),output_frames=[REVERSE[f] for f in e]) for token,e in zip(scene.TOKENS,scene.EVENTS)],
        board_treatment=[
            dict(title='Before the Answer Begins',treatment='Retain original dense board camera and highlights through the layers explanation; remove recap and final-token preview.'),
            dict(title='Why the Final Token Matters',treatment='Full compact canonical board for retained explanation. Two-second unmarked opening, question ring at spoken question mark, final-token card at spoken vector. Remove launching-pad restatement.'),
            dict(title='The Answer, Token by Token',treatment='Approved landscape video-only scene. Fixed camera, question above, large reply left, three probability rows right; selected token flies into reply. All other tokens in one small line, bottom 110px clear.'),
            dict(title='Closing message',treatment='Keep canonical close and its complete narration. Remove preceding duplicate inference definition.')],
        audio='Original PCM reconstructed identically to v12, five new silence-aligned cuts, 5ms fades only at those joins. No added pauses, no voice generation.',
        visual_join_holds=[dict(v12_frames=[a,b],source_v11_frame=f) for a,b,f in EXTRA_HOLDS],
        listening_performed=False,continuous_playback_performed=False,publication='Review candidate only',
        approval='David: Agree. Build it please. November 9, 2026.')
    (OUT/'edit-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    reader=old.Reader(SOURCE)
    proc=None
    if not args.preview:
        assert not DEST.exists(),'Never overwrite a review candidate'
        proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
            '-f','f32le','-ar','48000','-ac','2','-i',str(OUT/'assembled-audio.f32'),'-map','0:v:0','-map','1:a:0',
            '-c:v','libx264','-threads','4','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for n,f in enumerate(MAPPING):
        if args.preview and n not in samples:continue
        if DEMO[0]<=f<DEMO[1]:im=scene.render(f)
        elif 1766<=f<2247:im=bridge.at(f-1472)[0].copy()
        elif any(a<=f<b for a,b,_ in held):im=next(im.copy() for a,b,im in held if a<=f<b)
        else:
            oldf=V11[f];im=base_frame(oldf,reader)
            if old.DOG[0]<=oldf<old.DOG[1]:im,_=old.dog(im)
            if old.EOS[0]<=oldf<old.EOS[1]:im,_=old.brighten(im,refs)
        if n in samples:cv2.imwrite(str(OUT/'expected'/f'{n:05d}.png'),im)
        if proc:proc.stdin.write(im.tobytes())
        if proc and (n+1)%600==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    reader.c.release()
    if proc:
        proc.stdin.close();assert proc.wait()==0
        plan['candidate_sha256']=sha(DEST)
        (OUT/'edit-manifest.json').write_text(json.dumps(plan,indent=2)+'\n')
    assert all(sha(Path(p))==h for p,h in protected.items())
    print('Preview ready' if args.preview else str(DEST),flush=True)

if __name__=='__main__':main()
