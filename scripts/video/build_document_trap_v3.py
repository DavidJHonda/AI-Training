#!/usr/bin/env python3
"""Preserve v2 fixes; extend quote visual over the final moves-board return."""
import json,subprocess
from pathlib import Path
import cv2,imageio_ffmpeg
import build_document_trap_v2 as base

ROOT=base.ROOT
OUT=ROOT/'video-audit/document-trap-repair-2026-09-29-v3'
DEST=ROOT/'Prompts/document-trap-v3.mp4'
START,END=5806,5930

def main():
    assert base.sha(base.SRC)==base.EXPECTED
    assert not DEST.exists(), 'Do not overwrite a review candidate.'
    OUT.mkdir(parents=True,exist_ok=True)
    refs=base.collect()
    # Read from the original hash-locked source, not the already encoded v2.
    cap=cv2.VideoCapture(str(base.SRC));hold=None
    for n in range(START):
        ok,hold=cap.read();assert ok,n
    cap.release()
    assert hold is not None
    manifest=json.loads((base.OUT/'edit-manifest.json').read_text())
    manifest.update(output=str(DEST),approval='User approved keeping narration and extending the passage/quote visual through 3:13–3:17.',
                    status='Requested board-return removal built; previously pending narration corrections remain.',
                    parent_visual_recipe='scripts/video/build_document_trap_v2.py')
    manifest.pop('render_sha256',None)
    manifest['changed_spans'].append(dict(frames=[START,END],source_frame=START-1,
        purpose='Hold settled passage-and-quote visual through checking sentence; remove four-second moves-board return.'))
    manifest['board_runs_seconds']['moves']=[14.5333,16.2667]
    manifest['new_scope']='Only frames 5806–5929 differ from the v2 visual recipe; audio and timing unchanged.'
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    cmd=[ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(base.SRC),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-threads','2','-pix_fmt','yuv420p',
         '-c:a','copy','-video_track_timescale','15360','-movflags','+faststart',str(DEST)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    cap=cv2.VideoCapture(str(base.SRC));n=0
    try:
        while True:
            ok,im=cap.read()
            if not ok:break
            frame=hold if START<=n<END else base.edited(im,n,refs)
            proc.stdin.write(frame.tobytes());n+=1
            if n%1800==0:print(f'Rendered {n}/6780 frames',flush=True)
    finally:
        cap.release();proc.stdin.close()
    assert proc.wait()==0 and n==6780
    assert base.sha(base.SRC)==base.EXPECTED
    manifest.update(render_sha256=base.sha(DEST),encoded_input_frames=n)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':main()
