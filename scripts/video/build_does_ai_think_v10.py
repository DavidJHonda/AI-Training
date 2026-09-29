#!/usr/bin/env python3
"""Owner-requested visual repair: keep the Chinese Room illustration at 1:26.

Reuse v9's pristine assembly, omitting only its 85.7–92.0 second cutaway.
Copy the approved parent's encoded AAC packets without changing the narration.
"""
from pathlib import Path
from types import SimpleNamespace
import json, subprocess
import cv2
import imageio_ffmpeg
import build_does_ai_think_v9 as v9
from editspec_build import sha

OUT=v9.ROOT/'video-audit/does-ai-think-repair-2026-09-29-v10'
DEST=v9.ROOT/'Prompts/does-ai-think-v10.mp4'
PARENT=v9.DEST
EXPECTED='0f9f12e310a522ca97a867e0436ac04795173bee8e6e93491aef9321c4a7f8c9'
SPAN=(2571,2760)

def audio_hash(ff,path):
    return subprocess.check_output([ff,'-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()

def main():
    assert not DEST.exists(),'Never overwrite a review candidate'
    assert sha(PARENT)==EXPECTED
    old=json.loads((v9.OUT/'edit-manifest.json').read_text())
    for p,h in old['protected_hashes'].items():assert sha(p)==h,p
    OUT.mkdir(exist_ok=True);(OUT/'encoded').mkdir(exist_ok=True)
    v9.CUTAWAYS=[r for r in v9.CUTAWAYS if (r['start'],r['end'])!=SPAN]
    asm=v9.Assembly(SimpleNamespace(close_img=cv2.imread(str(v9.OUT/'close.png'))))
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    wanted={2570,2571,2580,2625,2700,2759,2760,2790,2826,v9.TOTAL-1}
    p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(PARENT),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for f in range(v9.TOTAL):
        im=asm.frame(f);p.stdin.write(im.tobytes())
        if f%900==899:print('Rendered',f+1,'/',v9.TOTAL,flush=True)
    p.stdin.close();assert p.wait()==0;asm.release()
    # Verify exact audio retention, full frame count and decoded repair frames.
    parent_audio=audio_hash(ff,PARENT);new_audio=audio_hash(ff,DEST);assert parent_audio==new_audio
    c=cv2.VideoCapture(str(DEST));fps=c.get(cv2.CAP_PROP_FPS);n=0;cells=[]
    while True:
        ok,im=c.read()
        if not ok:break
        assert im.shape==(720,1280,3)
        if n in wanted:
            cv2.imwrite(str(OUT/'encoded'/f'{n:05d}.jpg'),im)
            tile=cv2.resize(im,(640,360));cv2.putText(tile,f'{n/30:.3f}s / f{n}',(10,27),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,255),2);cells.append(tile)
        n+=1
    c.release();assert n==v9.TOTAL and fps==30
    while len(cells)%2:cells.append(cells[-1]*0)
    cv2.imwrite(str(OUT/'repair-sheet.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+2]) for i in range(0,len(cells),2)]))
    m={**old,'output':str(DEST),'render_sha256':sha(DEST),'parent':str(PARENT),'parent_sha256':EXPECTED,'cutaways':v9.CUTAWAYS,
       'visual_boundaries':[f for f in old['visual_boundaries'] if f not in SPAN],
       'scope':'Narrow owner-requested repair: replace the 1:25.70–1:32 cutaway with the same canonical Chinese Room Step 3 view. Everything else retains v9 treatment; no shipping.',
       'repair':{'output_frames':SPAN,'seconds':[85.7,92.0],'visual':'Canonical Chinese Room Step 3 callout; existing camera path continues into outside-observer callout at 1:33.',
                 'picture_sources':'Original raw rolls and v9 canonical canvases, avoiding an additional generation on the parent video.',
                 'audio_packets_identical':True,'audio_sha256':new_audio,'decoded_frames':n,'fps':fps,
                 'longest_unbroken_chinese_room_run_seconds':(3305-2085)/30,
                 'board_run_exception':'40.67 second continuous board run explicitly requested to preserve the Chinese Room illustration at 1:26.',
                 'prior_review_limits':'v9 listening and continuous playback limitations remain; no new audio edits.'},
       'corner_mark':asm.counts}
    m['protected_files_unchanged']={p:sha(p)==h for p,h in old['protected_hashes'].items()};assert all(m['protected_files_unchanged'].values());assert sha(PARENT)==EXPECTED
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    guard=subprocess.run([str(v9.ROOT/'.video-venv/bin/python'),str(v9.ROOT/'scripts/video/transition_guard.py'),str(DEST),'--boundary','2571:removed-cutaway-start','--boundary','2760:removed-cutaway-end','--boundary','2790:outside-camera-onset','--outdir',str(OUT/'transitions')],check=False)
    m['repair']['transition_guard_exit']=guard.returncode
    m['repair']['transition_guard_note']='Inspect every-frame strips. The pre-existing continuous camera pan at frame 2790 can trigger the cut detector; no automatic waiver is applied.'
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':main()
