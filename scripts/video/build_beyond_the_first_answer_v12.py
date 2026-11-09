#!/usr/bin/env python3
"""Replace v11 overview narration with the owner's supplied WAV, at natural speed."""
import json,subprocess
import cv2,numpy as np
import build_beyond_the_first_answer_v11 as old

ROOT=old.ROOT
AUDIT=ROOT/'video-audit/beyond-the-first-answer-audio-v12-2026-11-09'
DEST=ROOT/'Prompts/beyond-the-first-answer-v12.mp4'
RECORDING=ROOT/'Prompts/Beyond-the-first-answer audio.wav'
RECORDING_SHA='baeac0dd8bd4b3f83f3713a59f39169bf74c67ee9e3b01485984601f51a837ed'
OLD_SHA='7c82b47ee5fa261dab247f9fadf45988c0e1f67dd82da878ad2c33ac04c0a531'
JOIN=old.JOIN
OVERVIEW=262 # 0.5s lead + complete 10.4s WAV + 1/60s frame-alignment pad.
SHIFT=OVERVIEW-old.prev.INSERT
TOTAL=old.TOTAL+SHIFT
LEAD=.5
GAIN=-1.2
ONSETS=[.68,2.89,5.72,8.60]
FF=old.FF

def overview(n,images):
    original=old.prev.ONSET
    old.prev.ONSET=ONSETS
    try:return old.prev.overview(n,images)
    finally:old.prev.ONSET=original

def audio():
    x=old.prev.decode_audio(old.AUDIT/'assembled-audio.wav')
    recording=old.prev.decode_audio(RECORDING)
    assert len(recording)==499200
    insert=np.zeros(OVERVIEW*2000,np.float32)
    insert[24000:24000+len(recording)]=recording*10**(GAIN/20)
    result=np.concatenate([x[:JOIN*2000],insert,x[(JOIN+old.prev.INSERT)*2000:]])
    assert len(result)==TOTAL*2000 and np.max(np.abs(insert))<1
    assert np.array_equal(result[:JOIN*2000],x[:JOIN*2000])
    assert np.array_equal(result[(JOIN+OVERVIEW)*2000:],x[(JOIN+old.prev.INSERT)*2000:])
    dest=AUDIT/'assembled-audio.wav'
    subprocess.run([FF,'-y','-v','error','-f','f32le','-ar','48000','-ac','1','-i','pipe:0','-c:a','pcm_f32le',str(dest)],input=result.tobytes(),check=True)
    return dest

def main():
    AUDIT.mkdir(exist_ok=True);assert not DEST.exists()
    sha=old.prev.v8.base.sha
    assert sha(old.DEST)==OLD_SHA and sha(RECORDING)==RECORDING_SHA
    assert sha(old.INTRO)==old.INTRO_SHA
    for k,p in old.prev.v8.ROLLS.items():assert sha(p)==old.prev.v8.EXPECTED[k]
    protected={str(p):sha(p) for p in [ROOT/'index.html',ROOT/'course-assets/manifest.json',ROOT/'lessons/beyond-the-first-answer.md',*old.prev.v8.base.ASSETS.glob('*')] if p.is_file()}
    (AUDIT/'protected-before.json').write_text(json.dumps(protected,indent=2))
    sound=audio();mapping,intro=old.intro_frames();images=old.prev.art()
    cv2.imwrite(str(AUDIT/'poster.jpg'),overview(36,images))
    plan=dict(scope='Replace only four-way overview narration with supplied recording. No redundancy cuts.',source_previous=str(old.DEST),source_previous_sha256=OLD_SHA,recording=str(RECORDING),recording_sha256=RECORDING_SHA,recording_duration=10.4,recording_gain_db=GAIN,recording_rate_change=False,recording_output_start_seconds=JOIN/24+LEAD,removed_old_audio_seconds=[JOIN/24,(JOIN+old.prev.INSERT)/24],overview_seconds=[JOIN/24,(JOIN+OVERVIEW)/24],overview_frames=[JOIN,JOIN+OVERVIEW],highlight_seconds=[JOIN/24+t for t in ONSETS],added_frames=SHIFT,added_seconds=SHIFT/24,frames=TOTAL,duration_seconds=TOTAL/24,untouched_audio_pcm_identical=True,prior_pcm_source_sha256=sha(old.AUDIT/'assembled-audio.wav'),picture_sources='v2 opening as approved; v11 tail rebuilt from pristine donors/current boards. Only overview duration and highlight times change.',publication='Review candidate; lesson and installed video unchanged',listening='No listening pass claimed; source/candidate transcription and signal checks only.')
    (AUDIT/'edit-plan.json').write_text(json.dumps(plan,indent=2))
    old.prev.v8.base.AUDIT=AUDIT
    boards,close=old.prev.v8.base.prepare();donors,_=old.prev.v8.load_donors()
    cmd=[FF,'-v','error','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','24','-i','pipe:0','-i',str(sound),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
    (AUDIT/'encode-command.json').write_text(json.dumps(cmd,indent=2))
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for n in range(TOTAL):
        if n<JOIN:im=cv2.imdecode(intro[mapping[n]],cv2.IMREAD_COLOR)
        elif n<JOIN+OVERVIEW:im=overview(n-JOIN,images)
        else:im=old.prev.old_frame(n-SHIFT-old.SHIFT-old.prev.INSERT,boards,close,donors)
        p.stdin.write(im.tobytes())
        if (n+1)%720==0:print(f'Rendered {n+1}/{TOTAL}',flush=True)
    p.stdin.close();assert p.wait()==0
    changed=[p for p,h in protected.items() if sha(p)!=h]
    assert all(p in [str(ROOT/'index.html'),str(ROOT/'course-assets/manifest.json')] for p in changed),changed
    assert sha(RECORDING)==RECORDING_SHA and sha(old.DEST)==OLD_SHA
    plan.update(candidate=str(DEST),candidate_sha256=sha(DEST),protected_lesson_assets_unchanged=True,concurrent_shared_file_changes=changed)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(plan,indent=2))
    print('Complete:',DEST,flush=True)

if __name__=='__main__':main()
