"""Match the live lesson map sequences to the existing narration; preserve AAC."""
import hashlib,json,subprocess
from pathlib import Path
import cv2
import numpy as np
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'course-assets/vector-space/vector-space.mp4'
DEST=ROOT/'Prompts/vector-space-v14.mp4'
OUT=ROOT/'video-audit/vector-space-maps-2026-10-04'
FRAMES=OUT/'frames'
EXPECTED='91fc722c8173cd7903a11ac6e9bfb16de44a3188912ffcd02ac9632963f6b280'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert sha(SOURCE)==EXPECTED,'Installed source differs from the reviewed v11'
    assert not DEST.exists(),'Never overwrite an existing review candidate'
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    def yuv(p):
        data=subprocess.check_output([ff,'-v','error','-i',str(p),'-frames:v','1','-f','rawvideo','-pix_fmt','yuv420p','pipe:1'])
        assert len(data)==1280*720*3//2
        return np.frombuffer(data,dtype=np.uint8)
    states={f'{kind}-{s}':yuv(FRAMES/f'{kind}-{s}.png') for kind,count in [('cities',5),('drinks',7),('context',2)] for s in range(count)}
    motion=[yuv(FRAMES/f'context-motion-{n:03}.png') for n in range(49)]
    # Absolute frame cues, based on the reviewed v10 transcript (v11 AAC is identical).
    scenes=[
        {'start':950,'end':2090,'kind':'cities','cues':[[950,0],[1782,1],[1848,2],[1890,3],[1944,4]]},
        {'start':3187,'end':4387,'kind':'drinks','cues':[[3187,0],[3270,1],[3309,2],[3477,3],[3749,4],[3840,5],[3954,6]]},
        {'start':5200,'end':5846,'kind':'context','cues':[[5200,0],[5556,1]]}
    ]
    decoder=subprocess.Popen([ff,'-v','error','-i',str(SOURCE),'-map','0:v:0','-f','rawvideo','-pix_fmt','yuv420p','pipe:1'],stdout=subprocess.PIPE)
    process=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','yuv420p','-s','1280x720','-r','30','-i','pipe:0','-i',str(SOURCE),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    try:
        for n in range(6278):
            data=decoder.stdout.read(1280*720*3//2);assert len(data)==1280*720*3//2,f'Source stopped at {n}'
            frame=np.frombuffer(data,dtype=np.uint8)
            scene=next((s for s in scenes if s['start']<=n<s['end']),None)
            if scene:
                cue,step=next((c for c in reversed(scene['cues']) if c[0]<=n))
                kind=scene['kind'];frame=states[f'{kind}-{step}']
                if kind=='context' and step==1 and n-cue<49:frame=motion[n-cue]
                elif kind!='context' and step>0 and n-cue<20:
                    # A 650ms fade matches the lesson's point/line reveal. Known
                    # locations remain fixed because all states share geometry.
                    a=min(1,(n-cue+1)/20);a=1-(1-a)**2
                    frame=np.round(states[f'{kind}-{step-1}'].astype(float)*(1-a)+frame.astype(float)*a).astype(np.uint8)
            process.stdin.write(frame.tobytes())
            if n%900==0:print(f'Rendered {n}/6278',flush=True)
        process.stdin.close();assert process.wait()==0
    finally:
        decoder.stdout.close();assert decoder.wait()==0
    assert sha(SOURCE)==EXPECTED
    manifest={'source':str(SOURCE),'source_sha256':EXPECTED,'output':str(DEST),'output_sha256':sha(DEST),'fps':30,'frames':6278,'scenes':scenes,'audio':'copied AAC; no timing changes','shared_source_sha256':sha(ROOT/'index.html'),'preview_generator':'scripts/video/preview_vector_space.cjs','animation_capture':'scripts/video/capture_vector_space.cjs'}
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST)
if __name__=='__main__':main()
