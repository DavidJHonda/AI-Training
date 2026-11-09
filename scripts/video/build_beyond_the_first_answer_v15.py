#!/usr/bin/env python3
"""Approved three redundancy cuts, rebuilt from original picture and PCM sources."""
import json, subprocess
import cv2, numpy as np
import build_beyond_the_first_answer_v14 as old

ROOT=old.ROOT; FF=old.FF; base=old.base
AUDIT=ROOT/'video-audit/beyond-the-first-answer-cuts-v15-2026-11-09'
DEST=ROOT/'Prompts/beyond-the-first-answer-v15.mp4'
SOURCE=old.DEST
EXPECTED='4804170623ccdbd7f0df7f8070adde44c3fcd040f904638177b5df827830de35'
# Half-open v14 frame ranges; each endpoint is in measured inter-sentence quiet.
CUTS=[(1176,1289,'repeated-group-project'),(1487,1774,'strengths-preview'),(2835,3112,'lawn-mowing-setup')]
MAPPING=[n for n in range(old.TOTAL) if not any(a<=n<z for a,z,_ in CUTS)]
TOTAL=len(MAPPING)
JOINS=[a-sum(e-s for s,e,_ in CUTS if e<=a) for a,z,_ in CUTS]

def output_frame(n):
    assert not any(a<=n<z for a,z,_ in CUTS)
    return n-sum(z-a for a,z,_ in CUTS if z<=n)

def audio():
    path=old.prev.AUDIT/'assembled-audio.wav'
    x=old.prev.old.prev.decode_audio(path)
    assert len(x)==old.TOTAL*2000
    pieces=[];start=0
    for a,z,_ in CUTS:
        pieces.append(x[start*2000:a*2000]);start=z
    pieces.append(x[start*2000:old.TOTAL*2000]);untouched=np.concatenate(pieces)
    result=untouched.copy();joins=[]
    for n in JOINS:
        k=n*2000;fade=240
        before=result[k-fade:k].copy();after=result[k:k+fade].copy()
        assert max(np.max(np.abs(before)),np.max(np.abs(after)))<.003
        result[k-fade:k]*=np.linspace(1,0,fade)
        result[k:k+fade]*=np.linspace(0,1,fade)
        joins.append(dict(frame=n,seconds=n/24,fade_ms=5,peak_before=float(np.max(np.abs(before))),peak_after=float(np.max(np.abs(after)))))
    mask=np.ones(len(result),bool)
    for n in JOINS:mask[n*2000-240:n*2000+240]=False
    assert np.array_equal(result[mask],untouched[mask]) and len(result)==TOTAL*2000
    p=AUDIT/'assembled-audio.wav'
    subprocess.run([FF,'-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(p)],input=result.tobytes(),check=True)
    return p,dict(source=str(path),source_sha256=base.sha(path),outside_join_fades_pcm_identical=True,joins=joins)

def prepare_boards():
    base.AUDIT=AUDIT
    boards,close=base.prepare()
    # Restart the existing restrained push at the new full-board entrances.
    boards['summer-business']['span'][0]=CUTS[1][1]-old.OFFSET
    boards['summer-business']['rings']=[r for r in boards['summer-business']['rings'] if r['end']>CUTS[1][1]-old.OFFSET]
    boards['profit']['span'][0]=CUTS[2][1]-old.OFFSET
    boards['profit']['rings'][0]['start']=3137-old.OFFSET # First word of the student's prompt.
    return boards,close

def main():
    AUDIT.mkdir(exist_ok=True);assert not DEST.exists()
    assert base.sha(SOURCE)==EXPECTED
    assert base.sha(old.prev.old.INTRO)==old.prev.old.INTRO_SHA
    for k,p in old.v8.ROLLS.items():assert base.sha(p)==old.v8.EXPECTED[k]
    protected={str(p):base.sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/manifest.json',ROOT/'lessons/beyond-the-first-answer.md',*base.ASSETS.glob('*')] if p.is_file()}
    (AUDIT/'protected-before.json').write_text(json.dumps(protected,indent=2))
    sound,ainfo=audio()
    plan=dict(scope='Three approved narration cuts only; retain both optional passages, all twelve dialogue turns, four idea titles, iteration introduction and close.',source=str(SOURCE),source_sha256=EXPECTED,cuts=[dict(label=label,source_frames=[a,z],source_seconds=[a/24,z/24],output_join_frame=j,output_join_seconds=j/24) for (a,z,label),j in zip(CUTS,JOINS)],removed_frames=old.TOTAL-TOTAL,removed_seconds=(old.TOTAL-TOTAL)/24,frames=TOTAL,duration_seconds=TOTAL/24,audio=ainfo,publication='Review candidate only; installed lesson/video unchanged',limitations=['Transcript, waveform and frame review do not establish a listening pass; the three joins require listening review.'])
    (AUDIT/'edit-plan.json').write_text(json.dumps(plan,indent=2))
    mapping,intro=old.prev.old.intro_frames();images=old.prev.old.prev.art()
    boards,close=prepare_boards();donors,_=old.v8.load_donors()
    spans={slug:[output_frame(b['span'][0]+old.OFFSET),output_frame(b['span'][1]+old.OFFSET)] for slug,b in boards.items()}
    plan['board_spans']=spans
    plan['board_treatment']='Existing full-board framing and restrained 2% push, restarted at shortened Thought Partner/Learn entrances. Removed preview highlight cues; Learn first prompt highlight aligns to spoken I might. Other highlights follow retained audio unchanged.'
    samples={0,TOTAL-1,*JOINS,*[j-1 for j in JOINS],*[j+24 for j in JOINS]}
    for a,z in spans.values():samples.update([a,(a+z)//2,z-1])
    samples.update([output_frame(old.START),output_frame(old.END)])
    cmd=[FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','24','-i','pipe:0','-i',str(sound),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
    (AUDIT/'encode-command.json').write_text(json.dumps(cmd,indent=2))
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n,source_n in enumerate(MAPPING):
        if old.START<=source_n<old.END:im=old.v8.scene_frame(old.TITLE,source_n,donors)
        elif source_n<old.prev.JOIN:im=cv2.imdecode(intro[mapping[source_n]],cv2.IMREAD_COLOR)
        elif source_n<old.prev.JOIN+old.prev.OVERVIEW:im=old.prev.overview(source_n-old.prev.JOIN,images)
        else:im=old.prev.old.prev.old_frame(source_n-old.OFFSET,boards,close,donors)
        if n in samples:cv2.imwrite(str(AUDIT/f'expected-{n}.png'),im)
        if n==spans['summer-business'][0]:cv2.imwrite(str(AUDIT/'poster.jpg'),im)
        proc.stdin.write(im.tobytes())
        if (n+1)%720==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    proc.stdin.close();assert proc.wait()==0
    changes=[p for p,h in protected.items() if base.sha(p)!=h]
    assert all(p in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')] for p in changes),changes
    assert base.sha(SOURCE)==EXPECTED
    plan.update(candidate=str(DEST),candidate_sha256=base.sha(DEST),protected_lesson_files_unchanged=True,concurrent_shared_file_changes=changes)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(plan,indent=2))
    print('Complete:',DEST,flush=True)

if __name__=='__main__':main()
