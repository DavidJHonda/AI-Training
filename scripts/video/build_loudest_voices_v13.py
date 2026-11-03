#!/usr/bin/env python3
"""Match the approved two-example lesson; copy unaffected v12 video packets."""
from pathlib import Path
import hashlib, json, subprocess
import av, cv2, numpy as np, imageio_ffmpeg
from ken_burns_path import draw_ring, hex_bgr

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/loudest-voices-two-examples-2026-11-03'
SOURCE = ROOT / 'Prompts/loudest-voices-v12.mp4'
DEST = ROOT / 'Prompts/loudest-voices-v13.mp4'
BOARD = ROOT / 'course-assets/loudest-voices/loudest-voices-missed-predictions.jpg'
FF = imageio_ffmpeg.get_ffmpeg_exe()
A, B = 3064, 5241
CUTS = [(3387,3557),(3838,4436),(4728,5178)]
KEEPS = [(0,3387),(3557,3838),(4436,4728),(5178,8302)]
SHIFT = sum(b-a for a,b in CUTS)
FRAMES = 8302-SHIFT
RECTS = [(40,127,784,759),(816,127,1560,759)]
COLORS = ['#4f2fc4','#a9760c']

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pcm(p):
    return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-']),np.float32).reshape(-1,2)

def board_frame(active=None):
    image=cv2.imread(str(BOARD)); assert image.shape[:2]==(799,1600)
    frame=np.full((720,1280,3),250,np.uint8)
    frame[40:679]=cv2.resize(image,(1280,639),interpolation=cv2.INTER_LANCZOS4)
    if active is not None:
        x,y,r,b=RECTS[active]
        draw_ring(frame,x*.8,40+y*639/799,r*.8,40+b*639/799,hex_bgr(COLORS[active]),11,4)
    return frame

def main():
    assert sha(SOURCE)=='31a18fc49cc76e576ea736d23160bc516f486e9160df6557c5f0a018ad4edc37'
    assert not DEST.exists(), 'Never overwrite a review candidate'
    OUT.mkdir(exist_ok=True)
    # Reconstruct the retained pre-AAC assembly from its hash-identified donors.
    donors={'lv':ROOT/'Prompts/loudest-voices-v8.mp4','hands':ROOT/'Prompts/in-your-hands-v6.mp4'}
    expected={'lv':'d553d341c258f1420b8a5927f6a6cdd2652a12b1f0d6fafe5d55f66089b497a4','hands':'721e0738684fa09007104865ef0ca292dac2951a93766d04e7db8bcfbde2151c'}
    for k,p in donors.items(): assert sha(p)==expected[k]
    plan=[('lv',0,2751),('lv',3612,3823),('lv',3884,6488),('hands',1074,3477),('hands',5019,5508)]
    audio={k:pcm(p) for k,p in donors.items()}; pieces=[]
    for i,(key,start,end) in enumerate(plan):
        piece=audio[key][start*1600:end*1600].copy()
        if i: piece[:240]*=(np.arange(240)/240)[:,None]
        if i<len(plan)-1: piece[-240:]*=(1-np.arange(240)/240)[:,None]
        pieces.append(piece)
    original=(np.clip(np.concatenate(pieces),-1,1)*32767).astype('<i2').astype(np.float32)/32768
    left=original[:708*1600].copy();right=original[864*1600:].copy()
    left[-240:]*=(1-np.arange(240)/240)[:,None];right[:240]*=(np.arange(240)/240)[:,None]
    original=np.concatenate([left,right])
    corr=float(np.corrcoef(original.ravel(),pcm(SOURCE)[:len(original)].ravel())[0,1]);assert corr>.995
    pieces=[];timeline=[];offset=0
    for i,(start,end) in enumerate(KEEPS):
        piece=original[start*1600:end*1600].copy()
        if i:piece[:240]*=(np.arange(240)/240)[:,None]
        if i<len(KEEPS)-1:piece[-240:]*=(1-np.arange(240)/240)[:,None]
        pieces.append(piece)
        timeline.append({'source_start_frame':start,'source_end_frame':end,'output_start_frame':offset,'output_end_frame':offset+end-start})
        offset+=end-start
    sound=np.concatenate(pieces);assert len(sound)==FRAMES*1600
    raw=OUT/'edited-audio.f32';sound.tofile(raw)
    audiofile=OUT/'edited-audio.m4a'
    subprocess.run([FF,'-v','error','-y','-f','f32le','-ar','48000','-ac','2','-i',str(raw),'-c:a','aac','-b:a','192k',str(audiofile)],check=True)
    leg=OUT/'replacement-leg.mp4'
    cmd=[FF,'-v','error','-y','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','-','-an','-c:v','libx264','-threads','4','-crf','18','-preset','medium','-pix_fmt','yuv420p','-r','30','-video_track_timescale','15360',str(leg)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    states={k:board_frame(k) for k in (None,0,1)};count=0
    with av.open(str(SOURCE)) as source:
        for n,im in enumerate(source.decode(video=0)):
            if n<A:continue
            if n>=B:break
            if any(a<=n<b for a,b in CUTS):continue
            if n<5178:
                active=None if n<3566 else 0 if n<4436 else 1
                if 4436<=n<4442:active=0
                frame=states[active]
            else:frame=im.to_ndarray(format='bgr24')
            proc.stdin.write(frame.tobytes());count+=1
    proc.stdin.close();assert proc.wait()==0;assert count==B-A-SHIFT
    source=av.open(str(SOURCE));v=source.streams.video[0]
    patch=av.open(str(leg));pv=patch.streams.video[0]
    assert pv.time_base==v.time_base and pv.codec_context.extradata==v.codec_context.extradata
    snd=av.open(str(audiofile));a=snd.streams.audio[0];packets=[];keys=[];retained=0
    for p in source.demux(v):
        if p.dts is None:continue
        f=round(p.pts/512)
        if p.is_keyframe:keys.append(f)
        if A<=f<B:continue
        if f>=B:p.pts-=SHIFT*512;p.dts-=SHIFT*512
        packets.append((True,p));retained+=1
    assert A in keys and B in keys
    for p in patch.demux(pv):
        if p.dts is None:continue
        p.pts+=A*512;p.dts+=A*512;packets.append((True,p))
    for p in snd.demux(a):
        if p.dts is not None:packets.append((False,p))
    packets.sort(key=lambda x:(x[1].dts*x[1].time_base,not x[0]))
    with av.open(str(DEST),'w',options={'movflags':'+faststart'}) as dest:
        ov=dest.add_stream_from_template(v);oa=dest.add_stream_from_template(a)
        for isvideo,p in packets:p.stream=ov if isvideo else oa;dest.mux(p)
    boundaries=[A]+[row['output_start_frame'] for row in timeline[1:]]+[B-SHIFT]
    m={'candidate':str(DEST.relative_to(ROOT)),'sha256':sha(DEST),'source':str(SOURCE.relative_to(ROOT)),'source_sha256':sha(SOURCE),'board':str(BOARD.relative_to(ROOT)),'board_sha256':sha(BOARD),'frames':FRAMES,'fps':30,'duration':FRAMES/30,'removed_seconds':SHIFT/30,'cuts_source_frames':CUTS,'timeline':timeline,'boundaries':boundaries,'patch_source_frames':[A,B],'retained_video_packets':retained,'rendered_video_frames':count,'density':'compact; complete board at full view throughout, 4px whole-card rings','card_rectangles':RECTS,'board_placement':[0,40,1280,639],'ring_source_onsets':[3566,4442],'audio_source_hashes':{str(p.relative_to(ROOT)):sha(p) for p in donors.values()},'reconstructed_audio_correlation_to_v12':corr,'audio':'Reconstructed pre-AAC assembly; 5ms fades in quiet cut handles; one AAC encode; no added pauses or generated voice.','status':'Review candidate only; not installed. Listening review remains required.'}
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(json.dumps(m,indent=2),flush=True)

if __name__=='__main__':main()
