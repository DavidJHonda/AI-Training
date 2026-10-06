"""Check the encoded candidate and retain representative frames."""
import hashlib,json,subprocess
from pathlib import Path
import cv2,numpy as np,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'video-audit/vector-space-maps-2026-10-04'
SOURCE=ROOT/'course-assets/vector-space/vector-space.mp4';DEST=ROOT/'Prompts/vector-space-v14.mp4'
ff=imageio_ffmpeg.get_ffmpeg_exe()
def audio_sha(p):return hashlib.sha256(subprocess.check_output([ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()
def main():
    manifest=json.loads((OUT/'edit-manifest.json').read_text());assert manifest['output']==str(DEST)
    assert hashlib.sha256(DEST.read_bytes()).hexdigest()==manifest['output_sha256']
    same_audio=audio_sha(SOURCE)==audio_sha(DEST);assert same_audio
    subprocess.run([ff,'-v','error','-xerror','-i',str(DEST),'-f','null','-'],check=True)
    source=cv2.VideoCapture(str(SOURCE));cap=cv2.VideoCapture(str(DEST))
    assert int(cap.get(cv2.CAP_PROP_FRAME_COUNT))==6278
    assert cap.get(cv2.CAP_PROP_FPS)==30
    out=OUT/'encoded';out.mkdir(exist_ok=True)
    # Settled states, before/after each new item, and within the IT move.
    samples=[949,950,1781,1805,1847,1870,1889,1912,1943,1970,2089,2090,3186,3187,3294,3332,3500,3748,3773,3864,3980,4386,4387,5199,5200,5555,5556,5568,5580,5592,5604,5845,5846]
    for n in samples:
        cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,im=cap.read();assert ok
        cv2.imwrite(str(out/f'frame-{n:04}.jpg'),im)
    # State captures and decoded frames should agree, allowing H.264 rounding.
    checks=[]
    for n,name in [(970,'cities-0'),(1810,'cities-1'),(1875,'cities-2'),(2000,'cities-4'),(3350,'drinks-2'),(3500,'drinks-3'),(3780,'drinks-4'),(3880,'drinks-5'),(4000,'drinks-6'),(5230,'context-0'),(5580,'context-motion-024'),(5620,'context-1')]:
        cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,im=cap.read();assert ok
        reference=cv2.imread(str(OUT/'frames'/f'{name}.png'));error=float(np.abs(im.astype(float)-reference).mean());assert error<3,(n,name,error)
        checks.append({'frame':n,'state':name,'mean_error_255':error})
    outside=[]
    for n in [100,750,2200,3000,4500,5000,5950,6200]:
        cap.set(cv2.CAP_PROP_POS_FRAMES,n);ok,im=cap.read();assert ok
        source.set(cv2.CAP_PROP_POS_FRAMES,n);ok,original=source.read();assert ok
        error=float(np.abs(im.astype(float)-original).mean());assert error<3,(n,error);outside.append(error)
    # Contact sheets are for encoded-output inspection, not source-only QA.
    for group,ids in [('cities',[950,1805,1870,1912,1970,2089]),('drinks',[3187,3294,3332,3500,3773,3980]),('context',[5200,5555,5556,5568,5580,5604])]:
        tiles=[cv2.resize(cv2.imread(str(out/f'frame-{n:04}.jpg')),(640,360)) for n in ids]
        sheet=np.vstack([np.hstack(tiles[i:i+2]) for i in range(0,6,2)])
        cv2.imwrite(str(OUT/f'contact-{group}.jpg'),sheet)
    report={'frames':6278,'fps':30,'duration_seconds':6278/30,'compressed_audio_identical':same_audio,'audio_sha256':audio_sha(DEST),'decode':'passed','shared_scene_checks':checks,'unchanged_span_max_mean_error_255':max(outside),'source_unchanged':hashlib.sha256(SOURCE.read_bytes()).hexdigest()==manifest['source_sha256']}
    assert report['source_unchanged'];(OUT/'qa.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    cap.release();source.release()
if __name__=='__main__':main()
