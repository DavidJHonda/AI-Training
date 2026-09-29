from pathlib import Path
import json,subprocess,sys,hashlib,re
import cv2,numpy as np
from PIL import Image,ImageDraw
import imageio_ffmpeg
ROOT=Path.cwd();OUT=ROOT/'video-audit/your-home-base-zoom-cut-2026-09-29-v8';DEST=ROOT/'Prompts/your-home-base-v8.mp4';FF=imageio_ffmpeg.get_ffmpeg_exe()
m=json.loads((OUT/'edit-manifest.json').read_text());(OUT/'encoded').mkdir(exist_ok=True)
fmap=lambda n:n if n<2044 else n-144
# Every event, settled move, leg entry/exit plus preservation frames.
sourceframes={1518,1527,1545,1770,1835,2043,2188,2189,4651,5017,5678,6275,6407,6669,6995}
for board in m['boards']:
 for a,b in board['source_spans']:sourceframes|={a,b-1}
 for ev in board['ring_events']:sourceframes.add(ev[0]);sourceframes.add(ev[0]+12)
 for move in board['moves']:sourceframes|={move['source_frame'],move['source_frame']+move['frames']-1}
picks={fmap(n) for n in sourceframes};cap=cv2.VideoCapture(str(DEST));fps=cap.get(cv2.CAP_PROP_FPS);n=0;captured=[]
while True:
 ok,fr=cap.read()
 if not ok:break
 if n in picks:
  cv2.imwrite(str(OUT/'encoded'/f'{n:06d}.jpg'),fr,[cv2.IMWRITE_JPEG_QUALITY,95]);captured.append(n)
 n+=1
cap.release();assert n==6852 and fps==30
for k,off in enumerate(range(0,len(captured),12)):
 sh=Image.new('RGB',(1440,1080),'white')
 for j,frame in enumerate(captured[off:off+12]):
  im=Image.open(OUT/'encoded'/f'{frame:06d}.jpg').resize((480,270));ImageDraw.Draw(im).text((4,4),f'{frame/30:.3f}s  f{frame}',fill='red',stroke_width=1,stroke_fill='white');sh.paste(im,(j%3*480,j//3*270))
 sh.save(OUT/f'encoded-sheet-{k}.jpg')
ref=np.fromfile(OUT/'edited-audio.f32',np.float32)
actual=np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(DEST),'-map','0:a:0','-f','f32le','-ac','1','-ar','48000','-']),np.float32)
assert len(actual)>=len(ref);audlen=len(actual);actual=actual[:len(ref)]
err=actual-ref;snr=float(10*np.log10(np.sum(ref.astype(float)**2)/np.sum(err.astype(float)**2)))
checks=[]
for t in [30,67,69,90,150,220]:
 a=int(t*48000);z=ref[a:a+48000];errors=[float(np.mean((z-actual[a+lag:a+48000+lag])**2)) for lag in range(-4,5)];best=np.argmin(errors)-4;checks.append({'t':t,'best_lag_samples':int(best),'corr':float(np.corrcoef(z,actual[a:a+48000])[0,1])})
assert all(x['best_lag_samples']==0 and x['corr']>.995 for x in checks)
subprocess.run([FF,'-v','error','-y','-ss','64.5','-i',str(DEST),'-t','10.5','-vn','-c:a','pcm_s16le',str(OUT/'cut-context-encoded.wav')],check=True)
r=subprocess.run([FF,'-hide_banner','-ss','66','-i',str(DEST),'-t','5','-af','silencedetect=noise=-40dB:d=0.15','-f','null','-'],capture_output=True,text=True);(OUT/'cut-silences.txt').write_text(r.stderr)
starts=[float(x)+66 for x in re.findall(r'silence_start: ([\d.]+)',r.stderr)];ends=[float(x)+66 for x in re.findall(r'silence_end: ([\d.]+)',r.stderr)];gaps=[[a,b,b-a] for a,b in zip(starts,ends) if a<=2044/30<=b]
r=subprocess.run([FF,'-v','error','-i',str(DEST),'-f','null','-'],capture_output=True,text=True);assert r.returncode==0 and not r.stderr
q={'frames':n,'fps':fps,'duration':n/fps,'expected_samples':len(ref),'decoded_audio_samples_with_codec_padding':audlen,'audio_reference_SNR_dB':snr,'audio_alignment_checks':checks,'cut_gap_minus40dB':gaps,'full_decode':{'exit':r.returncode,'errors':r.stderr},'source_unchanged':hashlib.sha256(Path(m['source']).read_bytes()).hexdigest()==m['source_sha256'],'boards_unchanged':all(hashlib.sha256(Path(x['asset']).read_bytes()).hexdigest()==x['sha256'] for x in m['boards'])}
(OUT/'verification.json').write_text(json.dumps(q,indent=2));print(json.dumps(q,indent=2),flush=True)
bounds={1519:'retained-training-label-fade',1835:'retained-training-end',2044:'philosophy-cut-board-in',4098:'big-three-out',5534:'how-we-used-in',6131:'how-we-used-cutaway',6263:'how-we-used-return',6525:'close'}
for a,b in m['boards'][0]['output_spans']:
 bounds.setdefault(a,'big-three-return');bounds.setdefault(b,'big-three-cutaway')
args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
for n,label in sorted(bounds.items()):args+=['--boundary',f'{n}:{label}']
subprocess.run(args,check=True)
