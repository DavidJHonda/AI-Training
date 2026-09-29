#!/usr/bin/env python3
"""Approved Document Trap visual repairs; narration remains pending donor audio.

Reads the exact hash-locked shipped build. No audio samples are edited.
Sequential decoding only. Preserves original animation outside the label.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'course-assets/document-trap/document-trap.mp4'
OUT = ROOT / 'video-audit/document-trap-repair-2026-09-29-v2'
DEST = ROOT / 'Prompts/document-trap-v2.mp4'
EXPECTED = '3451967266e89b0543cdcd567f7c8c50b5843d9a8cacf4c745b316215de5329c'
INSERT = (2595, 2715)  # 1:26.50–1:30.50, within the search explanation
DONOR = (2085, 2205)   # 1:09.50–1:13.50, selection/load animation
NOTE = (3951, 4083)    # 2:11.70–2:16.10, pseudo-handwriting
LABEL = (3540, 3660)   # includes the complete output-box fade in/out
cv2.setNumThreads(2)

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def collect():
    wanted = set(range(*DONOR)) | {3530, 3600, 3900, 3950, 3650, 3570}
    c = cv2.VideoCapture(str(SRC)); found = {}; n = 0
    while wanted:
        ok, im = c.read(); assert ok, n
        if n in wanted:
            found[n] = im; wanted.remove(n)
        n += 1
    c.release()
    return found

def label_patch(im, blank, full):
    """Replace only the interior lettering, with the source panel's fade."""
    x0,y0,x1,y1 = 1100,357,1230,417
    # Estimate opacity from a text-free strip inside the original panel.
    b = blank[350:415,1082:1095].astype(float).mean()
    s = im[350:415,1082:1095].astype(float).mean()
    f = full[350:415,1082:1095].astype(float).mean()
    a = float(np.clip((b-s)/(b-f), 0, 1))
    if a < .005:
        return im
    base = blank[y0:y1,x0:x1].astype(float)
    color = np.median(full[350:415,1082:1095].reshape(-1,3),axis=0)
    patch = np.uint8(np.round(base*(1-a)+color*a))
    # Render at 3x for clean lettering at delivery size.
    scale = 3; w=x1-x0; h=y1-y0
    layer = Image.new('RGBA',(w*scale,h*scale),(0,0,0,0))
    draw = ImageDraw.Draw(layer)
    font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',21*scale)
    draw.text((w*scale/2,h*scale/2),'Answer',font=font,anchor='mm',fill=(239,240,232,round(255*a)))
    overlay = layer.resize((w,h),Image.Resampling.LANCZOS)
    bg = Image.fromarray(cv2.cvtColor(patch,cv2.COLOR_BGR2RGB)).convert('RGBA')
    im[y0:y1,x0:x1] = cv2.cvtColor(np.asarray(Image.alpha_composite(bg,overlay).convert('RGB')),cv2.COLOR_RGB2BGR)
    return im

def edited(im,n,refs):
    if INSERT[0] <= n < INSERT[1]:
        return refs[DONOR[0]+n-INSERT[0]].copy()
    if LABEL[0] <= n < LABEL[1]:
        return label_patch(im,refs[3530],refs[3600])
    if NOTE[0] <= n < NOTE[1]:
        # Continue the same comparison instead of the unrelated pseudo-text.
        return refs[3900].copy()
    return im

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');args=ap.parse_args()
    assert sha(SRC)==EXPECTED, 'Source changed; rebase the edit explicitly.'
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'qa').mkdir(exist_ok=True)
    refs=collect()
    for n in [3570,3600,3650,3951,4020]:
        src=refs.get(n,refs[3900]).copy()
        cv2.imwrite(str(OUT/'qa'/f'preview-{n:05d}.jpg'),edited(src,n,refs))
    manifest=dict(source=str(SRC),source_sha256=EXPECTED,output=str(DEST),fps=30,frames=6780,duration=226,
        approval='User: Agree. Build it please. (2026-09-29)',
        status='Visual-stage candidate only; replacement narration unavailable.',
        audio='Copy exact original AAC packets; no narration or timing changes.',
        changed_spans=[dict(frames=list(INSERT),source_frames=list(DONOR),purpose='Break process board with existing selection/load animation'),
                       dict(frames=list(LABEL),purpose='Ground Truth Output -> Answer, preserving fade and surrounding animation'),
                       dict(frames=list(NOTE),source_frame=3900,purpose='Replace pseudo-text with continued complete/incomplete comparison')],
        pending_audio=[dict(seconds=[64.7,74.2],text='A short file may fit there in full. With a long file, the system may search for the parts that seem most relevant and add those passages instead.'),
                       dict(seconds=[127.5,131.6],text='When retrieval misses something important, AI may miss it too.'),
                       dict(seconds=[184.5,193.7],text='In this example, the tournament rule allows six fouls.')],
        board_runs_seconds=dict(uploaded=21.3667,flow=[12.2333,12.7667],moves=[14.5333,16.2667,4.1333]),
        limitations=['Narration defects remain pending complete correct donor sentences.', 'No real-time listening certification.'])
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if args.preview_only:return
    assert not DEST.exists(), 'Never overwrite an existing candidate.'
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    cmd=[ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SRC),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-threads','2','-pix_fmt','yuv420p',
         '-c:a','copy','-video_track_timescale','15360','-movflags','+faststart',str(DEST)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c=cv2.VideoCapture(str(SRC));n=0
    try:
        while True:
            ok,im=c.read()
            if not ok:break
            p.stdin.write(edited(im,n,refs).tobytes());n+=1
            if n%900==0:print(f'Rendered {n}/6780 frames',flush=True)
    finally:
        c.release();p.stdin.close()
    assert p.wait()==0
    assert n==6780 and sha(SRC)==EXPECTED
    manifest.update(render_sha256=sha(DEST),encoded_input_frames=n)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST,flush=True)

if __name__=='__main__':main()
