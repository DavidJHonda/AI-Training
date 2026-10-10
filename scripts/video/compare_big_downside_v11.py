#!/usr/bin/env python3
"""Before/after excerpts with shared narration and surrounding context."""
import subprocess
import cv2
import build_big_downside_v11 as version

b=version.build
for name,start,end,poster in [('overview-and-section-1',9.5,23.5,17),('section-2',75.5,86,81),('section-3',146.5,155.5,150)]:
    dest=b.OUT/f'compare-{name}.mp4'
    assert not dest.exists()
    duration=end-start
    # Letterboxing gives each picture room for an explicit version label.
    graph="[0:v]scale=640:360,pad=640:390:0:30:white,drawtext=text='Before - v9':x=12:y=6:fontsize=19:fontcolor=black[l];[1:v]scale=640:360,pad=640:390:0:30:white,drawtext=text='After - v11':x=12:y=6:fontsize=19:fontcolor=black[r];[l][r]hstack[v]"
    subprocess.run([b.FF,'-v','error','-ss',str(start),'-i',str(b.BASE),'-ss',str(start),'-i',str(b.DEST),'-filter_complex',graph,'-map','[v]','-map','1:a:0','-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-threads','4','-c:a','aac','-b:a','160k','-movflags','+faststart',str(dest)],check=True)
    capture=cv2.VideoCapture(str(dest));count=0
    while True:
        ok,im=capture.read()
        if not ok:break
        if count==round((poster-start)*30):cv2.imwrite(str(dest.with_suffix('.jpg')),im)
        count+=1
    capture.release();assert count==round(duration*30),(name,count)
    print(name,count,flush=True)
