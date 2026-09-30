#!/usr/bin/env python3
"""Encoded-frame, cut-audio, transition, and retained-word checks for v12."""
import json,subprocess,sys
import cv2,numpy as np
import build_support_trap_v12 as edit
b=edit.b

def main():
    out=b.OUT;qa=out/'qa';qa.mkdir(exist_ok=True)
    m=json.loads((out/'edit-manifest.json').read_text())
    cmd=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(out/'transitions')]
    for r in m['boundaries']:cmd+=['--boundary',f'{r["frame"]}:{r["label"]}']
    subprocess.run(cmd,check=True)
    source=b.wavread(edit.PCM);planned=b.wavread(out/'edited.wav')
    expected=np.concatenate([source[a*b.SPF:z*b.SPF] for a,z in edit.KEEP])
    mask=np.ones(len(planned),dtype=bool)
    for a,z in edit.CUTS:
        n=edit.mapped(a)*b.SPF;mask[n-240:n+240]=False
    assert np.array_equal(planned[mask],expected[mask])
    subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(out/'encoded-audio.wav')],check=True)
    encoded=b.wavread(out/'encoded-audio.wav');corr=float(np.corrcoef(planned,encoded[:len(planned)])[0,1]);assert corr>.999
    cap=cv2.VideoCapture(str(b.DEST));old=b.Reader(edit.BASE);pts=[];n=0;diff=[];captures={}
    points=[edit.HOLD_A,edit.HOLD_B]+[edit.mapped(a) for a,z in edit.CUTS]
    wants={f for at in points for f in [at-1,at,at+5,at+12]}|{edit.TOTAL-1,edit.HOLD_B-1}
    hold_frames=[]
    while True:
        ok,im=cap.read()
        if not ok:break
        pts.append(cap.get(cv2.CAP_PROP_POS_MSEC));original=edit.original(n)
        if n%30==0 and not(edit.HOLD_A<=original<edit.HOLD_B or 4450<=original<4681):
            prev=old.at(original)
            diff.append(float(np.abs(cv2.resize(im,(320,180)).astype(float)-cv2.resize(prev,(320,180)).astype(float)).mean()))
        if n in wants:captures[n]=im;cv2.imwrite(str(qa/f'{n:06d}.jpg'),im)
        if edit.HOLD_A<=n<edit.HOLD_B:hold_frames.append(im)
        n+=1
    cap.release();old.cap.release()
    assert n==edit.TOTAL==8159
    assert np.allclose(np.diff(pts),1000/30,atol=.001)
    assert max(diff)<1.0
    # The native third-column region must remain identical throughout the hold.
    first=hold_frames[0][110:630,870:1165].astype(float)
    hold_diff=max(float(np.abs(x[110:630,870:1165].astype(float)-first).mean()) for x in hold_frames)
    assert hold_diff<.5
    strips=[]
    for at in points:
        cells=[]
        for f in [at-1,at,at+5,at+12]:
            tile=cv2.resize(captures[f],(320,180));cv2.putText(tile,f'{f} / {f/30:.2f}s',(6,19),0,.5,(0,0,255),1);cells.append(tile)
        strips.append(cv2.hconcat(cells))
    cv2.imwrite(str(qa/'changed-boundaries.jpg'),cv2.vconcat(strips))
    q=dict(decoded_frames=n,duration=n/30,uniform_frame_timing=True,
        retained_PCM_identical_except_5ms_join_edges=True,encoded_audio_correlation=corr,
        unchanged_regions_max_mean_pixel_difference=max(diff),third_column_hold_max_mean_pixel_difference=hold_diff,
        sha256=b.sha(b.DEST),protected_files_unchanged=all(m['protected_files_unchanged'].values()),
        full_playback_and_perceptual_listening='Not performed; waveform, transcript, and sampled-frame checks only.')
    (out/'qa-results.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2),flush=True)
    from faster_whisper import WhisperModel
    model=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
    transcripts=[]
    for label,start,end in [('urgency-join',137,150),('closing-join',255,edit.TOTAL/30)]:
        clip=qa/(label+'.wav')
        subprocess.run([b.FF,'-y','-v','error','-ss',str(start),'-t',str(end-start),'-i',str(b.DEST),'-vn','-ac','1','-ar','16000',str(clip)],check=True)
        segs,_=model.transcribe(str(clip),language='en',beam_size=5,word_timestamps=True,vad_filter=False)
        rows=[dict(start=s.start+start,end=s.end+start,text=s.text.strip()) for s in segs]
        transcripts.append(dict(label=label,segments=rows))
        print(label,rows,flush=True)
        silence=subprocess.run([b.FF,'-v','info','-i',str(clip),'-af','silencedetect=noise=-35dB:d=0.15','-f','null','-'],capture_output=True,text=True)
        (qa/(label+'-silence.txt')).write_text(silence.stderr)
    (qa/'join-transcripts.json').write_text(json.dumps(transcripts,indent=2)+'\n')

if __name__=='__main__':main()
