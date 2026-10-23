import sys,json,subprocess
from pathlib import Path
import av,cv2,numpy as np,imageio_ffmpeg
sys.path.insert(0,str(Path.cwd()/'scripts/video'))
import build_what_is_ai_working_v13 as b
from editspec_build import Reader,sha
specs,renderers=b.setup()
m=json.loads((b.OUT/'edit-manifest.json').read_text()); mapping=[(k,n) for k,a,z in b.KEEP for n in range(a,z)]
readers={k:Reader(v) for k,v in b.SOURCES.items()}; errors=[]; pts=[]; samples=[]
container=av.open(str(b.DEST)); stream=container.streams.video[0]
assert stream.average_rate==30
wanted=set(range(0,len(mapping),300))|{1283,1284,3134,3135,3289,3456,3561,3725,3726,3905,3906,3980,4046,4047,4174,4403,4404,4464,4571}
for i,frame in enumerate(container.decode(video=0)):
    assert i<len(mapping)
    k,n=mapping[i]; item=b.visual(n) if k=='base' else None
    expected=renderers[item[0]].at(item[1])[0] if item else readers[k].at(n)
    actual=frame.to_ndarray(format='bgr24')
    errors.append(float(np.abs(actual.astype(np.int16)-expected.astype(np.int16)).mean()))
    pts.append(float(frame.pts*frame.time_base))
    if i in wanted:
        name=f'encoded-{i:05d}.jpg';cv2.imwrite(str(b.OUT/'preview'/name),actual);samples.append(name)
assert len(errors)==4572
assert np.max(np.abs(np.diff(pts)-1/30))<1e-6
assert max(errors)<7,(max(errors),np.argmax(errors))
ff=imageio_ffmpeg.get_ffmpeg_exe()
def pcm(p):return np.frombuffer(subprocess.check_output([ff,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1']),np.float32)
actual=pcm(b.DEST);expected=pcm(b.OUT/'edited.wav');a=actual[:len(expected)]
corr=float(np.corrcoef(a,expected)[0,1]);assert corr>.995,corr
rms=lambda x:float(20*np.log10(max(1e-10,np.sqrt(np.mean(x*x)))))
seams=[dict(frame=f,before_dbfs=rms(expected[f*1600-2400:f*1600]),after_dbfs=rms(expected[f*1600:f*1600+2400])) for f in [1284,3135,4047]]
assert all(sha(Path(p))==h for p,h in m['protected'].items())
result=dict(frames=len(errors),fps=30,duration=len(errors)/30,continuous_pts=True,all_frame_MAE_max=max(errors),all_frame_MAE_mean=float(np.mean(errors)),audio_correlation=corr,seams=seams,protected_unchanged=True,samples=samples,limitation='Frames and audio measured; no direct listening audition.')
(b.OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
