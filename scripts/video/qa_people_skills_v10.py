#!/usr/bin/env python3
"""Check the transition repair and preservation of unaffected v9 content."""
import json,subprocess,sys,wave
import av,cv2,numpy as np
from imageio_ffmpeg import get_ffmpeg_exe
from build_people_skills_v10 import ROOT,OUT,DEST,PREVIOUS,base

def wav(p):
    with wave.open(str(p)) as w:
        assert w.getnchannels()==1 and w.getframerate()==48000
        return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(float)

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text())
    row=next(r for r in m['timeline'] if r.get('label')=='People skills matter even more in the AI future')
    start,end=row['start_frame'],row['end_frame'];shift=36;total=m['total_frames']
    assert total==4249 and start==1547 and end==1638
    assert all(base.sha(p)==h for p,h in m['protected_hashes'].items())
    old=base.Reader(PREVIOUS);samples=[];pts=[]
    out=OUT/'encoded-frames';out.mkdir(exist_ok=True)
    # The repaired introduction also corrects the first ring's spoken onset.
    wanted=set(range(0,total,120))|{start-1,start,start+30,end-1,end,end+12,total-1}
    with av.open(str(DEST)) as c:
        for f,frame in enumerate(c.decode(c.streams.video[0])):
            pts.append(float(frame.pts*frame.time_base))
            if f not in wanted:continue
            actual=frame.to_ndarray(format='bgr24')
            cv2.imwrite(str(out/f'f{f:05d}.jpg'),actual,[cv2.IMWRITE_JPEG_QUALITY,94])
            if start<=f<1650:continue
            prior=f if f<start else f+shift
            expected=old.at(prior)
            mse=np.mean((actual.astype(float)-expected.astype(float))**2)
            score=99 if not mse else float(10*np.log10(255**2/mse))
            samples.append(dict(frame=f,previous_frame=prior,psnr=score))
    assert len(pts)==total
    cadence=float(np.max(abs(np.diff(pts)-1/30)));assert cadence<1e-6
    assert min(s['psnr'] for s in samples)>35
    ff=get_ffmpeg_exe()
    subprocess.run([ff,'-v','error','-y','-i',str(DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
    master=wav(OUT/'edited.wav');previous=wav(ROOT/'video-audit/people-skills-build-v9-2026-10-26/edited.wav')
    assert np.array_equal(master[:start*1600],previous[:start*1600])
    # Shortening this keep changes the loop phase of its final 5 ms room-tone
    # crossfade. Verify the speech exactly and bound that silence-only change.
    resume=next(r for r in m['timeline'] if r['start_frame']==end)
    fade_end=resume['end_frame']*1600;fade_start=fade_end-240
    assert np.array_equal(master[end*1600+240:fade_start],previous[(end+shift)*1600+240:fade_start+shift*1600])
    assert np.array_equal(master[fade_end:],previous[fade_end+shift*1600:])
    tone_delta=float(np.max(abs(master[fade_start:fade_end]-previous[fade_start+shift*1600:fade_end+shift*1600])))
    assert tone_delta<40
    audio=wav(OUT/'encoded.wav');assert 0<=len(audio)-len(master)<2048
    audio=audio[:len(master)];snr=float(10*np.log10(np.sum(master**2)/np.sum((audio-master)**2)));assert snr>25
    with wave.open(str(OUT/'transition-review.wav'),'w') as w:
        w.setparams((1,2,48000,0,'NONE','not compressed'));w.writeframes(audio[47*48000:63*48000].astype(np.int16).tobytes())
    q=dict(candidate=str(DEST),sha256=base.sha(DEST),frames=total,duration=total/30,
       original_frames=4285,removed_frames=shift,repair_output_frames=[start,1650],
       unchanged_picture_samples=samples,unchanged_picture_min_psnr=min(s['psnr'] for s in samples),
       unaffected_master_speech_bit_identical=True,changed_end_crossfade_ms=5,room_tone_max_sample_delta=tone_delta,audio_master_snr_db=snr,
       audio_peak_dbfs=float(20*np.log10(np.max(abs(audio))/32768)),pts_max_error=cadence,
       sources_unchanged=True,direct_listening_performed=False,continuous_playback_performed=False)
    (OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
    subprocess.run([sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),
       '--outdir',str(OUT/'transitions'),'--boundary',f'{start}:explicit-AI-future-bridge',
       '--boundary',f'{end}:return-to-roll5','--boundary','1649:first-card-highlight'],check=True)
    print(json.dumps({k:v for k,v in q.items() if k!='unchanged_picture_samples'},indent=2))

if __name__=='__main__':
    cv2.setNumThreads(2);main()
