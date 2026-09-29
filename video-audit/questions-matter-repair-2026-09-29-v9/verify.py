"""Verify the exact encoded candidate without treating ASR as a listening pass."""
from pathlib import Path
import hashlib
import json
import sys

import av
import cv2
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts/video'))
import build_questions_matter_v9 as b


def packets(path, media):
    with av.open(str(path)) as container:
        stream = next(s for s in container.streams if s.type == media)
        rows=[]
        for p in container.demux(stream):
            if not p.size: continue
            row={'pts':str(p.pts*p.time_base) if p.pts is not None else None,
                 'duration':str(p.duration*p.time_base)}
            if media=='audio': row['sha256']=hashlib.sha256(bytes(p)).hexdigest()
            rows.append(row)
    return sorted(rows,key=lambda r:float(__import__('fractions').Fraction(r['pts'])))


def main():
    src=cv2.VideoCapture(str(b.SOURCE)); dst=cv2.VideoCapture(str(b.DEST))
    indices=[372,737,738,850,917,918,1094,1095,1210,1279,1280,1807,1808,1850,1891,1892,1902,1903,2569,4259,6097,6394,6592,6673]
    selected={}; kept=[]; inserted=[]; index=0
    refs={'library-research':b.fit_photo(b.ASSETS/'library-research.png'),
          'web-research':b.fit_photo(b.ASSETS/'web-research.png'),
          'value-introduction':b.value_frame()}
    while True:
        ok,a=src.read(); ok2,c=dst.read()
        assert ok==ok2, f'length mismatch at {index}'
        if not ok:break
        target=next((key for lo,hi,key,_ in b.SPANS if lo<=index<hi),None)
        reference=refs[target] if target else a
        small=lambda f:cv2.resize(f,(320,180),interpolation=cv2.INTER_AREA).astype(np.float32)
        mae=float(np.abs(small(reference)-small(c)).mean())
        (inserted if target else kept).append(mae)
        if index in indices:
            selected[index]=c
            cv2.imwrite(str(b.AUDIT/f'encoded-{index:06d}.jpg'),c)
        index+=1
    src.release();dst.release()
    assert index==b.TOTAL
    assert max(kept)<3, max(kept)
    assert max(inserted)<3,max(inserted)
    audio_equal=packets(b.SOURCE,'audio')==packets(b.DEST,'audio')
    video_timing_equal=packets(b.SOURCE,'video')==packets(b.DEST,'video')
    assert audio_equal and video_timing_equal
    data={'decoded_frames':index,'audio_payloads_pts_durations_identical':audio_equal,
          'video_pts_durations_identical':video_timing_equal,
          'unchanged_picture_frames':len(kept),'unchanged_picture_mae_mean':float(np.mean(kept)),
          'unchanged_picture_mae_max':max(kept),'inserted_picture_mae_max':max(inserted),
          'comparison':'Every decoded frame; 320x180 BGR MAE, allowing ordinary H.264 re-encode differences',
          'listening':'Not performed','real_time_playback':'Not performed'}
    (b.AUDIT/'verification.json').write_text(json.dumps(data,indent=2)+'\n')
    for page in range(2):
        sheet=Image.new('RGB',(1280,4*264),'#ddd');draw=ImageDraw.Draw(sheet)
        for n,i in enumerate(indices[page*12:page*12+12]):
            im=Image.fromarray(cv2.cvtColor(selected[i],cv2.COLOR_BGR2RGB)).resize((426,240))
            x=(n%3)*426;y=(n//3)*264;sheet.paste(im,(x,y))
            draw.text((x+4,y+242),f'f{i}  {i/30:.3f}s',fill='black')
        sheet.save(b.AUDIT/f'encoded-sheet-{page+1}.jpg')
    print(json.dumps(data,indent=2))


if __name__=='__main__': main()
