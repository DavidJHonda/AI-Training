"""Verify encoded sentence repair and unaffected picture/audio spans."""
from pathlib import Path
import sys, json, subprocess
import cv2, numpy as np, imageio_ffmpeg
from PIL import Image, ImageDraw
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/video'))
from editspec_build import sha
OUT=Path(__file__).resolve().parent
m=json.loads((OUT/'v19-manifest.json').read_text())
new=Path(m['output']); old=Path(m['base']); ff=imageio_ffmpeg.get_ffmpeg_exe()
inspection=OUT/'v19-inspection';inspection.mkdir(exist_ok=True)
ca,cb=cv2.VideoCapture(str(new)),cv2.VideoCapture(str(old))
assert (ca.get(cv2.CAP_PROP_FPS),ca.get(cv2.CAP_PROP_FRAME_WIDTH),ca.get(cv2.CAP_PROP_FRAME_HEIGHT))==(30,1280,720)
keys={0,600,2400,5500,6187,6188,6369,6370,6517,6518,6533,6534,6594,7692}
keys.update(x['frame']+15 for x in m['boundaries'])
frames={};stats=[];new_i=0;old_i=-1;old_image=None
while True:
    ok,im=ca.read()
    if not ok:break
    wanted_old=new_i if new_i<6370 else new_i+6
    while old_i<wanted_old:
        ok,old_image=cb.read();assert ok
        old_i+=1
    if not 6188<=new_i<6534:
        # Every retained frame checked for stale/reordered imagery.
        aa=cv2.resize(im,(160,90),interpolation=cv2.INTER_AREA).astype(float)
        bb=cv2.resize(old_image,(160,90),interpolation=cv2.INTER_AREA).astype(float)
        err=float(np.abs(aa-bb).mean())
        stats.append(err)
        assert err<2,(new_i,err)
    if new_i in keys:
        frames[new_i]=im.copy()
        cv2.imwrite(str(inspection/f'frame-{new_i:05d}.jpg'),im)
    new_i+=1
assert new_i==7693,new_i
ca.release();cb.release()
expected=cv2.imread(str(OUT/'proposed-sentence-card.png'))
sentence_errors=[]
for n in [6188,6369,6370,6517,6518,6533]:
    err=float(abs(frames[n].astype(float)-expected.astype(float)).mean())
    # RGB source -> delivered YUV420 -> OpenCV RGB adds a ~3-code-value
    # background offset. The encoded frame has been visually checked; allow
    # that measured conversion error rather than requiring RGB identity.
    assert err<4,(n,err)
    sentence_errors.append({'frame':n,'pixel_mae':err})
tiles=[]
for n in sorted(frames):
    tile=Image.new('RGB',(320,205),'white')
    tile.paste(Image.fromarray(cv2.cvtColor(frames[n],cv2.COLOR_BGR2RGB)).resize((320,180)),(0,25))
    ImageDraw.Draw(tile).text((8,5),f'Frame {n} / {n/30:.3f}s',fill='black')
    tiles.append(tile)
sheet=Image.new('RGB',(1280,205*((len(tiles)+3)//4)),'white')
for k,tile in enumerate(tiles):sheet.paste(tile,((k%4)*320,(k//4)*205))
sheet.save(inspection/'contact.jpg')
def pcm(path):
    return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(path),'-vn','-ar','48000','-ac','1','-f','f32le','-']),np.float32)
a=pcm(old);c=pcm(new)
comparisons=[]
for s,e in [(1,30),(80,100),(190,211),(218,240),(247,252)]:
    shift=0 if e<212 else -.2
    x=a[round(s*48000):round(e*48000)]
    y=c[round((s+shift)*48000):round((e+shift)*48000)]
    corr=float(np.corrcoef(x,y)[0,1]);assert corr>.995,(s,corr)
    comparisons.append(dict(base_seconds=[s,e],output_seconds=[s+shift,e+shift],correlation=corr))
clip=OUT/'v19-context-review.wav'
subprocess.run([ff,'-v','error','-i',str(new),'-ss','206','-t','24','-vn','-c:a','pcm_s16le',str(clip)],check=True)
sil=subprocess.run([ff,'-hide_banner','-i',str(new),'-ss','206','-t','24','-vn','-af','silencedetect=noise=-40dB:d=0.1','-f','null','-'],capture_output=True,text=True,check=True)
(OUT/'v19-silence.log').write_text(sil.stderr)
args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(new),'--outdir',str(OUT/'v19-transitions')]
for item in m['boundaries']:args.extend(['--boundary',f"{item['frame']}:{item['label']}"])
subprocess.run(args,check=True)
assert all(sha(Path(p))==digest for p,digest in m['protected_hashes'].items())
result=dict(decoded_frames=new_i,duration=new_i/30,fps=30,resolution=[1280,720],
    preserved_frame_count=len(stats),preserved_frame_max_thumbnail_mae=max(stats),
    sentence_frame_checks=sentence_errors,unaffected_audio_checks=comparisons,
    decoded_audio_peak=float(abs(c).max()),protected_files_unchanged=True,
    direct_listening=False,full_file_watch=False)
(OUT/'v19-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
