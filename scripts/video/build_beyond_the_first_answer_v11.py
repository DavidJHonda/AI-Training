#!/usr/bin/env python3
"""Approved v2 opening (through 'process') + v10 overview and remainder."""
from pathlib import Path
import json,subprocess
import cv2,numpy as np
import build_beyond_the_first_answer_v10 as prev

ROOT=prev.ROOT
AUDIT=ROOT/'video-audit/beyond-the-first-answer-intro-v11-2026-11-09'
DEST=ROOT/'Prompts/beyond-the-first-answer-v11.mp4'
INTRO=ROOT/'Prompts/beyond-the-first-answer-v2.mp4'
INTRO_SHA='bb128f1ddae843fa9f5a32154455adabb0a1d933842c278e38b01996abb7fc1c'
PREV_SHA='626381f9c9b5064d2e0be46dafaa40083fbdc74b4cd8f27f2ee0b067993614b2'
JOIN=823 # 34.291667 sec; safely inside v2's 34.061–34.675 silence.
SHIFT=JOIN-prev.CUT
TOTAL=prev.TOTAL+SHIFT
GAIN_DB=1.0 # Limited constant gain; preserve peak headroom and original dynamics.
FF=prev.v8.base.FF

def intro_frames():
    cap=cv2.VideoCapture(str(INTRO));assert cap.get(cv2.CAP_PROP_FPS)==30
    mapping=[n*30//24 for n in range(JOIN)];needed=set(mapping);cache={};n=0
    while cap.grab():
        if n in needed:
            ok,im=cap.retrieve();assert ok
            cache[n]=cv2.imencode('.png',im)[1]
        n+=1
        if n>max(needed):break
    cap.release();assert len(cache)==len(needed)
    return mapping,cache

def audio():
    original=prev.decode_audio(INTRO)[:JOIN*2000].copy()
    original*=10**(GAIN_DB/20)
    assert np.max(np.abs(original))<.99
    old=prev.decode_audio(prev.AUDIT/'assembled-audio.wav')
    tail=old[prev.CUT*2000:prev.TOTAL*2000]
    result=np.concatenate([original,tail]);assert len(result)==TOTAL*2000
    dest=AUDIT/'assembled-audio.wav'
    subprocess.run([FF,'-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(dest)],input=result.tobytes(),check=True)
    return dest,dict(intro_gain_db=GAIN_DB,intro_peak_after_gain=float(np.max(np.abs(original))),tail_pcm_preserved=True,tail_source=str(prev.AUDIT/'assembled-audio.wav'),tail_source_sha256=prev.v8.base.sha(prev.AUDIT/'assembled-audio.wav'),intro_integrated_lufs=-21.48,comparison_tail_lufs=-19.14,gain_reason='Reduce the measured level difference without clipping or adding compression.')

def main():
    AUDIT.mkdir(exist_ok=True);assert not DEST.exists()
    assert prev.v8.base.sha(INTRO)==INTRO_SHA
    assert prev.v8.base.sha(prev.DEST)==PREV_SHA
    assert prev.v8.base.sha(prev.v8.SOURCE)==prev.v8.base.EXPECTED
    for k,p in prev.v8.ROLLS.items():assert prev.v8.base.sha(p)==prev.v8.EXPECTED[k]
    protected={str(p):prev.v8.base.sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/manifest.json',ROOT/'lessons/beyond-the-first-answer.md',*prev.v8.base.ASSETS.glob('*')] if p.is_file()}
    (AUDIT/'protected-before.json').write_text(json.dumps(protected,indent=2))
    sound,levels=audio();mapping,intro=intro_frames();images=prev.art()
    cv2.imwrite(str(AUDIT/'poster.jpg'),prev.overview(24,images))
    plan=dict(scope='Approved v2 intro replaces v10 first 27.083333 seconds; corrected overview and rest retained.',source_intro=str(INTRO),source_intro_sha256=INTRO_SHA,source_previous=str(prev.DEST),source_previous_sha256=PREV_SHA,intro_source_seconds=[0,JOIN/24],previous_retained_seconds=[prev.CUT/24,prev.TOTAL/24],join_frame=JOIN,shift_frames=SHIFT,frames=TOTAL,duration_seconds=TOTAL/24,overview_seconds=[JOIN/24,(JOIN+prev.INSERT)/24],transition_line='There are four distinct moves to this process.',excluded_following_line='Think, learn, start, and iterate.',audio=levels,source_limitations='Opening uses the approved finished v2 picture with one additional encode and 30-to-24fps frame sampling. Remaining pictures rebuilt from raw donors and canonical lesson assets using the v10 recipe.',publication='Review only; installed video unchanged',listening='Not performed; narrator/cadence seam still needs listening review.')
    (AUDIT/'edit-plan.json').write_text(json.dumps(plan,indent=2))
    prev.v8.base.AUDIT=AUDIT
    boards,close=prev.v8.base.prepare();donors,_=prev.v8.load_donors()
    cmd=[FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','24','-i','pipe:0','-i',str(sound),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
    (AUDIT/'encode-command.json').write_text(json.dumps(cmd,indent=2))
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(TOTAL):
        if n<JOIN:im=cv2.imdecode(intro[mapping[n]],cv2.IMREAD_COLOR)
        elif n<JOIN+prev.INSERT:im=prev.overview(n-JOIN,images)
        else:im=prev.old_frame(n-SHIFT-prev.INSERT,boards,close,donors)
        p.stdin.write(im.tobytes())
        if (n+1)%720==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    p.stdin.close();assert p.wait()==0
    changed=[path for path,h in protected.items() if prev.v8.base.sha(path)!=h]
    assert all(path in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')] for path in changed),changed
    assert prev.v8.base.sha(INTRO)==INTRO_SHA and prev.v8.base.sha(prev.DEST)==PREV_SHA
    plan.update(candidate=str(DEST),candidate_sha256=prev.v8.base.sha(DEST),protected_lesson_assets_unchanged=True,concurrent_shared_file_changes=changed)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(plan,indent=2))
    print('Complete:',DEST,flush=True)

if __name__=='__main__':main()
