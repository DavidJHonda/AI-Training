#!/usr/bin/env python3
"""Decode the candidate, confirm copied audio, inspect camera coverage and cuts."""
from pathlib import Path
import json, subprocess
import cv2
import numpy as np
import build_engagement_trap_v14 as v

def audio_hash(path):
    return subprocess.check_output([v.b.FF,'-v','error','-i',str(path),'-map','0:a:0',
        '-c','copy','-f','hash','-hash','sha256','-'],text=True).strip()

def main():
    m=json.loads((v.OUT/'edit-manifest.json').read_text())
    old=cv2.VideoCapture(str(v.AUDIO));new=cv2.VideoCapture(str(v.DEST))
    assert old.isOpened() and new.isOpened()
    assert new.get(cv2.CAP_PROP_FPS)==old.get(cv2.CAP_PROP_FPS)==30
    assert new.get(cv2.CAP_PROP_FRAME_WIDTH)==1280 and new.get(cv2.CAP_PROP_FRAME_HEIGHT)==720
    count=0;diffs=[];tiles=[]
    while True:
        ok,a=old.read();ok2,b=new.read();assert ok==ok2
        if not ok:break
        if not any(s<=count<e for s,e in v.SPANS):
            # Identical pre-encode pictures can acquire small codec differences
            # after a changed GOP. Compare every unaffected decoded frame.
            delta=float(np.abs(cv2.resize(a,(320,180)).astype(float)-cv2.resize(b,(320,180))).mean())
            assert delta<3,(count,delta)
            diffs.append((delta,count))
        if count in v.PREVIEWS:
            cv2.imwrite(str(v.OUT/f'encoded-{count:05d}.jpg'),b)
            tile=cv2.resize(b,(384,216));cv2.rectangle(tile,(0,0),(384,22),(255,255,255),-1)
            cv2.putText(tile,f'{count/30:.2f}s / frame {count}',(8,16),cv2.FONT_HERSHEY_SIMPLEX,.43,(20,20,20),1)
            tiles.append(tile)
        count+=1
    old.release();new.release();assert count==7832
    while len(tiles)%4:tiles.append(np.full_like(tiles[0],255))
    cv2.imwrite(str(v.OUT/'camera-contact-sheet.jpg'),cv2.vconcat([cv2.hconcat(tiles[i:i+4]) for i in range(0,len(tiles),4)]))
    h1=audio_hash(v.AUDIO);h2=audio_hash(v.DEST);assert h1==h2
    board=v.CameraBoard()
    for s,e in v.SPANS:
        for n in range(s,e):board.frame(n) # Includes full-ring bounds assertions.
    assert all(v.b.sha(Path(p))==h for p,h in m['protected'].items())
    result=dict(decoded_frames=count,fps=30,duration=count/30,audio_packet_hash=h2,audio_identical_to_v13=True,
        unaffected_frames_compared=len(diffs),max_unaffected_thumbnail_mae=max(diffs),
        complete_highlight_bounds_checked_each_frame=True,full_board_unmarked_opening_seconds=96/30,
        fixed_post_crop_ring_width_px=4,protected_files_unchanged=True,candidate_sha256=v.b.sha(v.DEST),
        listening='Not performed; audio stream copied exactly from v13.',continuous_playback='Not performed; encoded frames and transition strips inspected separately.')
    (v.OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
    # Keep transition audit on the existing shared implementation.
    import sys
    args=[sys.executable,str(v.b.ROOT/'scripts/video/transition_guard.py'),str(v.DEST),'--outdir',str(v.OUT/'transitions')]
    for n in m['declared_boundaries']:args+=['--boundary',str(n)]
    subprocess.run(args,check=True)

if __name__=='__main__':main()
