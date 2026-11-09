#!/usr/bin/env python3
"""Narrow visual repair: give Iterate With AI the matching cinematic title beat."""
import json, subprocess
import cv2
import build_beyond_the_first_answer_v12 as prev

ROOT=prev.ROOT
AUDIT=ROOT/'video-audit/beyond-the-first-answer-iteration-v13-2026-11-09'
DEST=ROOT/'Prompts/beyond-the-first-answer-v13.mp4'
PREV_SHA='ce8e3232b09dd360090452ba3ea401865365801e58dfd0f65ec4528e6420c332'
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
    assert base.sha(prev.DEST)==PREV_SHA
    assert base.sha(prev.old.INTRO)==prev.old.INTRO_SHA
    for k,p in v8.ROLLS.items():assert base.sha(p)==v8.EXPECTED[k]
    protected={str(p):base.sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/manifest.json',ROOT/'lessons/beyond-the-first-answer.md',*base.ASSETS.glob('*')] if p.is_file()}
    (AUDIT/'protected-before.json').write_text(json.dumps(protected,indent=2))
    plan=dict(scope='Visual-only title introduction for Iterate With AI; all narration, timing, boards and other scenes retained.',previous=str(prev.DEST),previous_sha256=PREV_SHA,changed_frames=[START,END],changed_seconds=[START/24,END/24],source=str(v8.ROLLS['3']),source_frames=[5258,5314],source_fps=30,title='Iterate With AI',treatment='Existing cinematic sketch-to-business-plan moving illustration with the same top-left font, size, placement and color as the other three move titles. Unmarked full frame. Cut back to original diagram as the definition begins.',frames=TOTAL,fps=24,duration_seconds=TOTAL/24,publication='Review candidate only; installed lesson unchanged',limitations=['Inherited v12 narration joins still require listening review. No new listening pass claimed.','Previously proposed redundancy cuts remain unapplied.'])
    (AUDIT/'edit-plan.json').write_text(json.dumps(plan,indent=2))
    mapping,intro=prev.old.intro_frames();images=prev.old.prev.art()
    base.AUDIT=AUDIT
    boards,close=base.prepare();donors,_=v8.load_donors()
    for n in [START,START+28,END-1]:
        im=v8.scene_frame(TITLE,n,donors)
        cv2.imwrite(str(AUDIT/f'expected-{n}.png'),im)
    cv2.imwrite(str(AUDIT/'poster.jpg'),v8.scene_frame(TITLE,START+28,donors))
    cmd=[FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','24','-i','pipe:0','-i',str(prev.DEST),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
    (AUDIT/'encode-command.json').write_text(json.dumps(cmd,indent=2))
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(TOTAL):
        if START<=n<END:im=v8.scene_frame(TITLE,n,donors)
        elif n<prev.JOIN:im=cv2.imdecode(intro[mapping[n]],cv2.IMREAD_COLOR)
        elif n<prev.JOIN+prev.OVERVIEW:im=prev.overview(n-prev.JOIN,images)
        else:im=prev.old.prev.old_frame(n-OFFSET,boards,close,donors)
        proc.stdin.write(im.tobytes())
        if (n+1)%720==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    proc.stdin.close();assert proc.wait()==0
    changes=[p for p,h in protected.items() if base.sha(p)!=h]
    assert all(p in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')] for p in changes),changes
    assert base.sha(prev.DEST)==PREV_SHA
    audio=base.audio_sha(DEST);assert audio==base.audio_sha(prev.DEST)
    plan.update(candidate=str(DEST),candidate_sha256=base.sha(DEST),audio_payload_sha256=audio,audio_packets_identical=True,protected_lesson_files_unchanged=True,concurrent_shared_file_changes=changes)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(plan,indent=2))
    print('Complete:',DEST,flush=True)

if __name__=='__main__':main()
