#!/usr/bin/env python3
"""Narrow visual repair: retitle four lesson boards around the ideas being taught."""
import json, subprocess
import cv2
import build_beyond_the_first_answer_v12 as prev

ROOT=prev.ROOT
AUDIT=ROOT/'video-audit/beyond-the-first-answer-titles-v14-2026-11-09'
DEST=ROOT/'Prompts/beyond-the-first-answer-v14.mp4'
SOURCE=ROOT/'Prompts/beyond-the-first-answer-v13.mp4'
PREV_SHA='93fba6da0374db32bce15f850c1a2ac38fe65483ad4f52fd5a91f8c21ebade98'
v8=prev.old.prev.v8
base=v8.base
FF=prev.FF
TOTAL=prev.TOTAL
OFFSET=prev.SHIFT+prev.old.SHIFT+prev.old.prev.INSERT
START=4397+OFFSET
END=START+56 # Title phrase, then definition begins at 203.685 seconds.
TITLE=(START,END,'3',5258,5314,'iteration-title','Iterate With AI')

def main():
    AUDIT.mkdir(exist_ok=True);assert not DEST.exists()
    assert base.sha(SOURCE)==PREV_SHA
    assert base.sha(prev.old.INTRO)==prev.old.INTRO_SHA
    for k,p in v8.ROLLS.items():assert base.sha(p)==v8.EXPECTED[k]
    protected={str(p):base.sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/manifest.json',ROOT/'lessons/beyond-the-first-answer.md',*base.ASSETS.glob('*')] if p.is_file()}
    (AUDIT/'protected-before.json').write_text(json.dumps(protected,indent=2))
    plan=dict(scope='Retitle only the four lesson boards around the ideas taught; retain v13 cinematic introduction, audio, runtime, examples, artwork, camera paths and highlights.',previous=str(SOURCE),previous_sha256=PREV_SHA,board_spans={slug:[a+OFFSET,z+OFFSET] for slug,(a,z) in v8.SPANS.items()},titles={b.slug:b.title for b in base.BOARDS},frames=TOTAL,fps=24,duration_seconds=TOTAL/24,publication='Updated lesson boards locally; video is a review candidate only. Installed video unchanged.',limitations=['Inherited v12 narration joins still require listening review. No new listening pass claimed.','Previously proposed redundancy cuts remain unapplied.'])
    (AUDIT/'edit-plan.json').write_text(json.dumps(plan,indent=2))
    mapping,intro=prev.old.intro_frames();images=prev.old.prev.art()
    base.AUDIT=AUDIT
    boards,close=base.prepare();donors,_=v8.load_donors()
    samples={n for slug,(a,z) in v8.SPANS.items() for n in (a+OFFSET,(a+z)//2+OFFSET,z-1+OFFSET)}
    cmd=[FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','24','-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
    (AUDIT/'encode-command.json').write_text(json.dumps(cmd,indent=2))
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(TOTAL):
        if START<=n<END:im=v8.scene_frame(TITLE,n,donors)
        elif n<prev.JOIN:im=cv2.imdecode(intro[mapping[n]],cv2.IMREAD_COLOR)
        elif n<prev.JOIN+prev.OVERVIEW:im=prev.overview(n-prev.JOIN,images)
        else:im=prev.old.prev.old_frame(n-OFFSET,boards,close,donors)
        if n in samples:cv2.imwrite(str(AUDIT/f'expected-{n}.png'),im)
        if n==v8.SPANS['summer-business'][0]+OFFSET:cv2.imwrite(str(AUDIT/'poster.jpg'),im)
        proc.stdin.write(im.tobytes())
        if (n+1)%720==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    proc.stdin.close();assert proc.wait()==0
    changes=[p for p,h in protected.items() if base.sha(p)!=h]
    assert all(p in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')] for p in changes),changes
    assert base.sha(SOURCE)==PREV_SHA
    audio=base.audio_sha(DEST);assert audio==base.audio_sha(SOURCE)
    plan.update(candidate=str(DEST),candidate_sha256=base.sha(DEST),audio_payload_sha256=audio,audio_packets_identical=True,protected_lesson_files_unchanged=True,concurrent_shared_file_changes=changes)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(plan,indent=2))
    print('Complete:',DEST,flush=True)

if __name__=='__main__':main()
