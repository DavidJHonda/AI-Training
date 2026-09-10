#!/usr/bin/env python3
"""Preserve v5; expand positional encoding with approved live narration/visuals."""
from pathlib import Path
import argparse, hashlib, json, subprocess, wave
import cv2, numpy as np, imageio_ffmpeg
from build_one_more_thing_review_repair import ring

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/transformer-full-2026-09-10/v7'
DEST=ROOT/'videos/transformer-v7.mp4'
PREV=OUT.parent/'v5'
FPS=30; SR=48000
def fr(t): return round(t*FPS)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def wav(p):
    with wave.open(str(p)) as w:
        assert w.getframerate()==SR and w.getnchannels()==1
        return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(float)
class Reader:
    def __init__(self,p): self.c=cv2.VideoCapture(str(p));self.i=-1;self.im=None
    def at(self,n):
        assert n>=self.i,(n,self.i)
        while self.i<n:
            ok,self.im=self.c.read();assert ok,n;self.i+=1
        return self.im.copy()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    (OUT/'states').mkdir(parents=True,exist_ok=True)
    previous=json.loads((PREV/'edit-manifest.json').read_text())
    protected=[ROOT/'videos/transformer.mp4',ROOT/'videos/transformer-v5.mp4',ROOT/'videos/transformer-v4.mp4',ROOT/'videos/transformer-v6.mp4',ROOT/'Prompts/transformer-1.mp4',ROOT/'Prompts/transformer-2.mp4',ROOT/'index.html',ROOT/'lessons/transformer.md',ROOT/'lessons/transformer-word-order-editorial.jpg']
    hashes={str(p):sha(p) for p in protected}
    audio={'v5':wav(PREV/'edited.wav'),'live':wav(OUT.parent/'v6/live.wav')}
    def speech_rms(a):
        a=a[:len(a)//480*480].reshape(-1,480);r=np.sqrt(np.mean(a*a,axis=1));return np.sqrt(np.mean(a[r>700]**2))
    gain=float(speech_rms(audio['v5'][fr(170.5)*1600:fr(189)*1600])/speech_rms(audio['live'][fr(208.4)*1600:fr(224.4)*1600]))
    original=wav(ROOT/'video-audit/transformer-repair-2026-09-10/source-1.wav')
    seed=original[round(98.07*SR):round(98.17*SR)];seed-=seed.mean();loop=np.r_[seed,seed[::-1]]
    def tone(n):return np.resize(loop,n).copy()
    rows=[];parts=[];cursor=0
    def keep(src,a,b,label,visual,clamp=None):
        nonlocal cursor
        s,e=fr(a),fr(b);data=audio[src][s*1600:e*1600].copy()
        if src=='live':
            data*=gain;r=np.linspace(0,1,240);bed=tone(len(data))
            data[:240]=data[:240]*r+bed[:240]*(1-r)
            data[-240:]=data[-240:]*(1-r)+bed[-240:]*r
        row=dict(kind='source',source_id=src,source_start=s,source_end=e,start_frame=cursor,end_frame=cursor+e-s,label=label,visual=visual,clamp=clamp)
        rows.append(row);parts.append(data);cursor+=e-s
    def pause(seconds,label):
        nonlocal cursor
        count=fr(seconds);rows.append(dict(kind='room_tone',start_frame=cursor,end_frame=cursor+count,label=label,hold_frame=cursor-1));parts.append(tone(count*1600));cursor+=count
    keep('v5',0,211.3,'Preserved approved edit through CAT and milk explanation','v5')
    pause(1,'Pause from CAT and milk to word order')
    keep('live',208.4,224.8,'Full DOG and MAN comparison','live',fr(210.4))
    keep('live',224.8,228.0,'To solve this the architecture includes an extra step','live',fr(226.2))
    pause(.4,'Natural sentence gap after extra step')
    keep('live',235.8333333333,241.8,'Numbered-token position-stamp demonstration','live',fr(236.8333333333))
    keep('live',241.8,246.1666666667,'Name positional encoding on the current lesson board','order')
    keep('live',253.0333333333,260.0333333333,'Explain simultaneous processing with order preserved','order')
    pause(1,'Pause before closing message')
    close_start=cursor
    keep('v5',243.4666666667,251.1333333333,'Preserved v5 closing narration and camera','v5')
    data=np.clip(np.concatenate(parts),-32768,32767).astype(np.int16)
    with wave.open(str(OUT/'edited.wav'),'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(data.tobytes())
    board=cv2.imread(str(ROOT/'lessons/transformer-word-order-editorial.jpg'));h,w=board.shape[:2];scale=min(1210/w,660/h);x=(1280-w*scale)/2;y=(720-h*scale)/2
    plain=cv2.warpAffine(board,np.float32([[scale,0,x],[0,scale,y]]),(1280,720),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_CONSTANT,borderValue=(251,245,246))
    frames={'establish':plain}
    for label,rect in [('positions',[816,299,1560,760]),('takeaway',[40,800,1560,889])]:
        im=plain.copy();a,b,c,d=rect;ring(im,[a*scale+x,b*scale+y,c*scale+x,d*scale+y],'#4f2fc4' if label=='positions' else '#6e51ff');frames[label]=im
    for k,im in frames.items():cv2.imwrite(str(OUT/'states'/f'order-{k}.png'),im)
    boundaries=[b for b in previous['boundaries'] if b['frame']<fr(211.3)]
    boundaries += [dict(frame=t['start_frame'],label=t['label']) for t in rows[1:]]
    name_row=next(t for t in rows if t.get('visual')=='order')
    highlight_frame=name_row['start_frame']+fr(2.6)
    benefit_row=rows[-3];takeaway_frame=benefit_row['start_frame']+fr(3.8)
    boundaries += [dict(frame=highlight_frame,label='Highlight position stamps'),dict(frame=takeaway_frame,label='Highlight order takeaway')]
    m=dict(output=str(DEST),source=str(ROOT/'videos/transformer-v5.mp4'),donor=str(ROOT/'videos/transformer.mp4'),fps=30,duration=cursor/30,total_frames=cursor,close_start_frame=close_start,timeline=rows,protected_hashes=hashes,boundaries=sorted(boundaries,key=lambda b:b['frame']),audio=dict(live_gain=gain,room_tone_source=[98.07,98.17],crossfade_ms=5),inherited_manifest=str(PREV/'edit-manifest.json'),inherited_prefix_frames=fr(211.3),narration_cuts_live=[[228,235.8333333333],[246.1666666667,253.0333333333]],removed_v6_frames=[6339,6542],scope='Review only; live and previous candidates unchanged')
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print('Prepared',cursor,cursor/30,'live gain',gain,flush=True)
    if args.prepare_only:return
    assert not DEST.exists(),DEST
    readers={'v5':Reader(ROOT/'videos/transformer-v5.mp4'),'live':Reader(OUT.parent/'v6/live-cfr.mp4')}
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    ri=0;last=None
    for f in range(cursor):
        while f>=rows[ri]['end_frame']:ri+=1
        t=rows[ri]
        if t['kind']=='room_tone':im=last.copy()
        elif t['visual']=='order':im=frames['takeaway' if f>=takeaway_frame else 'positions' if f>=highlight_frame else 'establish']
        else:
            n=t['source_start']+f-t['start_frame']
            if t['clamp'] is not None:n=max(n,t['clamp'])
            im=readers[t['visual']].at(n)
        proc.stdin.write(im.tobytes());last=im
        if f%1800==0:print('Rendered',f,cursor,flush=True)
    proc.stdin.close();assert proc.wait()==0
    for reader in readers.values():reader.c.release()
    m['render_sha256']=sha(DEST);m['protected_files_unchanged']={str(p):sha(p)==hashes[str(p)] for p in protected};m['shared_files_changed_during_render']=[p for p,ok in m['protected_files_unchanged'].items() if not ok];assert all(Path(p).name=='index.html' for p in m['shared_files_changed_during_render'])
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));print(DEST,flush=True)
if __name__=='__main__':main()
