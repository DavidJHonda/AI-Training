#!/usr/bin/env python3
"""Replace the overview's processing-time sentence with roll 6's thinking time.
Preserve v17 edits, use original picture sources and PCM; review only.
"""
import json
import subprocess
from pathlib import Path
import cv2
import numpy as np
import imageio_ffmpeg
import build_why_answers_vary_v17 as previous
from build_embeddings_v7 import Renderer
from editspec_build import readwav,writewav,sha

ROOT=previous.ROOT
OLD=previous.OUT
OUT=ROOT/'video-audit/why-answers-vary-build-v18-2026-11-10'
DEST=ROOT/'Prompts/why-answers-vary-v18.mp4'
START,END=525,633                 # v17 17.50–21.10, quiet sentence boundaries
DONOR_START,DONOR_END=537,663     # roll 6 17.90–22.10, full sentence
ADD=(DONOR_END-DONOR_START)-(END-START)
SPF=1600

def old_frame(f):
    if f<END:return f
    if f<END+ADD:return END-1
    return f-ADD

def main():
    assert not DEST.exists(),'Do not overwrite review candidates'
    OUT.mkdir(exist_ok=True)
    m=json.loads((OLD/'edit-manifest.json').read_text())
    assert sha(m['candidate'])==m['candidate_sha256']
    assert all(sha(p)==h for p,h in m['protected'].items())
    source=readwav(OLD/'edited.wav')
    donor=readwav(previous.PICTURES/'roll-6.wav')
    gain=10**(-0.5185274864835563/20)  # established whole-roll speech-level match
    clip=donor[DONOR_START*SPF:DONOR_END*SPF].copy()*gain
    left=source[:START*SPF].copy();right=source[END*SPF:].copy()
    tone=readwav(previous.PICTURES/'roll-4.wav')[round(216.3*48000):round(216.4*48000)]
    tone-=tone.mean();bed=np.resize(np.r_[tone,tone[::-1]],480)
    ramp=np.linspace(0,1,240)
    left[-240:]=left[-240:]*(1-ramp)+bed[:240]*ramp
    clip[:240]=bed[240:]*(1-ramp)+clip[:240]*ramp
    clip[-240:]=clip[-240:]*(1-ramp)+bed[:240]*ramp
    right[:240]=bed[240:]*(1-ramp)+right[:240]*ramp
    audio=np.concatenate([left,clip,right]);total=m['frames']+ADD
    assert len(audio)==total*SPF
    assert np.array_equal(audio[:START*SPF-240],source[:START*SPF-240])
    assert np.array_equal(audio[(END+ADD)*SPF+240:],source[END*SPF+240:])
    writewav(OUT/'edited.wav',audio)

    # Reconstruct the v17 picture assembly without overwriting any old audit.
    source_manifest=json.loads(Path(m['source_visual_manifest']).read_text())
    film=previous.prior.Film();film.spans=source_manifest['visual_timeline']
    for r in film.spans:
        if r['kind']=='board':film.boards[r['key']]=Renderer(json.loads(Path(r['spec']).read_text()))
    film.close=cv2.imread(str(previous.PICTURES/'close.png'))
    temp=Renderer(json.loads(Path(m['temperature']['spec']).read_text()))
    protected={**m['protected'],m['candidate']:m['candidate_sha256']}
    bounds={f+(ADD if f>=END else 0) for f in m['boundaries']}|{START,END,END+ADD}
    # First overview highlight starts on the same syllable; later rings follow
    # the .6-second shift. Include its changes in this narrow edit's checks.
    bounds|={531,641+ADD,775+ADD}
    manifest=dict(candidate=str(DEST),previous_candidate=m['candidate'],fps=30,frames=total,duration=total/30,
        boundaries=sorted(bounds),protected=protected,source_visual_manifest=str(OLD/'edit-manifest.json'),
        audio_repair=dict(old_frames=[START,END],donor_roll=6,donor_frames=[DONOR_START,DONOR_END],
            output_frames=[START,END+ADD],added_frames=ADD,gain_db=-0.5185274864835563,crossfade_ms=5,
            text='First, the model you use and its thinking time changes the answer.'),
        visual_repair=dict(hold_frame=END-1,hold_frames=ADD,reason='Keep first overview card highlighted for the complete donor sentence'),
        audio=dict(clipped_samples=int(np.sum(np.abs(audio)>32767)),unaffected_pcm_identical=True),
        remaining_narration=m['remaining_narration'],listening_performed=False,continuous_playback_performed=False,
        status='Review candidate; not installed',approval='User requested roll 6 narration using thinking time.')
    path=OUT/'edit-manifest.json';path.write_text(json.dumps(manifest,indent=2)+'\n')
    p=subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
        '-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','4',
        '-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for f in range(total):
        old=old_frame(f)
        if m['temperature']['start_frame']<=old<m['temperature']['end_frame']:
            im=temp.at(old-m['temperature']['start_frame'])[0]
        else:im=film.frame(previous.original(old))
        p.stdin.write(im.tobytes())
        if f%900==899:print(f'Rendered {f+1}/{total}',flush=True)
    p.stdin.close();assert p.wait()==0;film.release()
    manifest['candidate_sha256']=sha(DEST)
    manifest['protected_unchanged']={p:sha(p)==h for p,h in protected.items()}
    assert all(manifest['protected_unchanged'].values())
    path.write_text(json.dumps(manifest,indent=2)+'\n');print(DEST,flush=True)

if __name__=='__main__':main()
