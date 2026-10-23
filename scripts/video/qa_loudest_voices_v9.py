#!/usr/bin/env python3
"""Check the encoded v9's source mapping, timing, audio and review frames."""
from pathlib import Path
import json, subprocess, hashlib
import av, cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/loudest-voices-build-v9-2026-10-22'
FF=imageio_ffmpeg.get_ffmpeg_exe()
cv2.setNumThreads(1)

def pcm(p):
    raw=subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','-'])
    return np.frombuffer(raw,dtype=np.float32)

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text());video=ROOT/m['candidate']
    cap=cv2.VideoCapture(str(video));err=[];sampled=[];n=0
    wanted={0,720,1200,2250,3100,3750,4500,5000,5750,6300,6487,6488,6510,6800,7190,7400,7600,7860,8450,8650,8890,8891,8938,8939,9088,9380-1}
    for leg in m['timeline'][:2]:
        src=cv2.VideoCapture(str(ROOT/leg['source']))
        # Sequential decode: frame-accurate; never use timestamp-based cv2 seeks.
        for k in range(leg['source_end_frame']):
            ok,ref=src.read();assert ok
            if k < leg['source_start_frame']:continue
            ok,frame=cap.read();assert ok
            # Compare every retained frame at half-resolution, allowing one encode's noise.
            diff=float(np.abs(cv2.resize(frame,(640,360)).astype(np.int16)-cv2.resize(ref,(640,360)).astype(np.int16)).mean())
            err.append(diff)
            if n in wanted:sampled.append((n,frame.copy()))
            n+=1
        src.release()
    while True:
        ok,frame=cap.read()
        if not ok:break
        if n in wanted:sampled.append((n,frame.copy()))
        n+=1
    cap.release();assert n==m['frames'],(n,m['frames'])
    assert max(err)<8, max(err)
    with av.open(str(video)) as c:
        stream=c.streams.video[0]
        meta={'width':stream.width,'height':stream.height,'fps':float(stream.average_rate),'duration':float(c.duration/av.time_base)}
        pts=np.array([float(f.pts*f.time_base) for f in c.decode(video=0)])
    assert meta['fps']==30 and meta['width']==1280 and meta['height']==720
    assert np.max(np.abs(np.diff(pts)-1/30))<0.0001
    sources={p:pcm(ROOT/p) for p in {s['source'] for s in m['timeline']}}
    legs=[]
    for i,leg in enumerate(m['timeline']):
        audio=sources[leg['source']][leg['source_start_frame']*1600:leg['source_end_frame']*1600].copy()
        if i>0:audio[:240]*=np.arange(240)/240
        if i<2:audio[-240:]*=1-np.arange(240)/240
        legs.append(audio)
    expected=np.concatenate(legs);actual=pcm(video)[:len(expected)]
    assert len(actual)==len(expected)
    corr=float(np.corrcoef(actual,expected)[0,1]);assert corr>0.995,corr
    audio_error=float(np.sqrt(np.mean((actual-expected)**2)))
    seams=[]
    for boundary in m['boundaries']:
        s=boundary['frame']*1600;window=actual[s-48000:s+48000]
        seams.append({'frame':boundary['frame'],'seconds':s/48000,
                      'sample_step_at_join':float(abs(actual[s]-actual[s-1])),
                      'rms_dbfs_10ms_before':float(20*np.log10(np.sqrt(np.mean(actual[s-480:s]**2))+1e-12)),
                      'rms_dbfs_10ms_after':float(20*np.log10(np.sqrt(np.mean(actual[s:s+480]**2))+1e-12)),
                      'max_step_within_one_second':float(np.abs(np.diff(window)).max())})
        subprocess.run([FF,'-v','error','-y','-ss',str(s/48000-6),'-t','18','-i',str(video),'-c','copy',str(OUT/f'join-{boundary["frame"]}.mp4')],check=True)
    sheet=Image.new('RGB',(1280,((len(sampled)+2)//3)*264),'white');d=ImageDraw.Draw(sheet)
    for i,(index,frame) in enumerate(sampled):
        p=OUT/f'encoded-{index:06d}.jpg';cv2.imwrite(str(p),frame)
        x=i%3*426;y=i//3*264
        sheet.paste(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).resize((426,240)),(x,y))
        d.text((x+6,y+242),f'{index/30:.3f}s / frame {index}',fill='black')
    sheet.save(OUT/'encoded-contact-sheet.jpg')
    before=m['protected'];assert before=={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in before}
    result={'candidate':m['candidate'],'sha256':hashlib.sha256(video.read_bytes()).hexdigest(),
            'decoded_frames':n,**meta,'retained_frames_compared':len(err),
            'retained_frame_mean_error':float(np.mean(err)),'retained_frame_max_error':max(err),
            'audio_sample_count':len(expected),'audio_correlation':corr,'audio_rms_error':audio_error,
            'audio_peak_dbfs':float(20*np.log10(np.abs(actual).max())),
            'seams':seams,'protected_sources_unchanged':True,
            'listening':'Not performed; numeric checks do not certify voice continuity or cadence.'}
    (OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
