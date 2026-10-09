#!/usr/bin/env python3
"""Approved visual-only GPA repair: roll-4 reveal, headings, correct 3.57 GPA.

Reassemble the established v14 timeline from its original sources. Copy v14's
encoded audio unchanged. The only changed picture span is [4973, 5360).
"""
from pathlib import Path
import argparse
import copy
import json
import os
import subprocess
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, sha

ROOT = Path(__file__).resolve().parents[2]
OLD = ROOT / 'video-audit/ai-is-different-build-2026-10-09-v14'
OUT = ROOT / 'video-audit/ai-is-different-build-2026-10-09-v15'
PREVIOUS = ROOT / 'Prompts/ai-is-different-v14.mp4'
DEST = ROOT / 'Prompts/ai-is-different-v15.mp4'
R4 = ROOT / 'Prompts/ai-is-different-4.mp4'
LEG = OUT / 'repaired-gpa.mkv'
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'


def prepare_gpa(ff):
    cap = cv2.VideoCapture(str(R4))
    frames = {}
    for f in range(4695):
        ok, im = cap.read()
        assert ok
        if 4470 <= f < 4695:
            frames[f] = im
    cap.release()
    blank, complete_top = frames[4470], frames[4590]
    # Current diagram is stationary after f4470. Preserve all row/field reveals.
    # The generated sticker later covers the blank header: restore that small
    # region from the same diagram before the sticker appears, then label it.
    fonts = {s:ImageFont.truetype(FONT,s) for s in (24,28,32)}
    proc = subprocess.Popen([ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24',
        '-s','1280x720','-r','30','-i','pipe:0','-an','-c:v','ffv1','-level','3',str(LEG)],stdin=subprocess.PIPE)
    mapping = []
    for k in range(387):
        # 7.5 seconds of original reveal over 9.5 seconds, then a 3.4s final hold.
        f = 4470 + min(224, round(min(k,284)*224/284))
        original = frames[f]
        im = original.copy()
        if f < 4590:
            im[:203] = blank[:203]
        else:
            im[:273] = complete_top[:273]
        # Preserve the original footer's blue-fill reveal and replace its label.
        footer_color = np.median(original[510:540,300:500],axis=(0,1))
        blue_amount = float(np.clip((footer_color[0]-footer_color[2])/150,0,1))
        im[485:565,165:1115] = original[485:565,300:301]
        pil = Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil)
        draw.text((640,49),'STRUCTURED DATA',font=fonts[24],fill='#252825',anchor='mm')
        draw.text((640,86),'Consistent Fields',font=fonts[28],fill='#3184b8',anchor='mm')
        for cx,label in [(353,'Course'),(639,'Grade'),(830,'Credits'),(1021,'Points')]:
            draw.text((cx,165),label,font=fonts[28],fill='#252825',anchor='mm')
        if blue_amount > .05:
            overlay = Image.new('RGBA',pil.size)
            d = ImageDraw.Draw(overlay)
            d.text((1065,525),'Calculated GPA: 3.57',font=fonts[32],
                   fill=(255,255,255,round(255*blue_amount)),anchor='rm')
            pil = Image.alpha_composite(pil.convert('RGBA'),overlay).convert('RGB')
        im = cv2.cvtColor(np.asarray(pil),cv2.COLOR_RGB2BGR)
        if k in (0,60,120,180,240,284,386):
            cv2.imwrite(str(OUT/f'gpa-state-{k:03d}.png'),im)
        proc.stdin.write(im.tobytes())
        mapping.append(f)
    proc.stdin.close()
    assert proc.wait()==0
    (OUT/'gpa-frame-map.json').write_text(json.dumps(mapping))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prepare-only',action='store_true')
    ap.add_argument('--reuse-leg',action='store_true')
    args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    m=json.loads((OLD/'edit-manifest.json').read_text())
    assert sha(PREVIOUS)==m['render_sha256']
    b=Build(ROOT,m['source'],OUT,OUT/'video-render.mp4')
    if not args.reuse_leg:
        prepare_gpa(b.ff)
    if args.prepare_only:
        return
    assert not DEST.exists()
    for name in ('leg-rules.mkv','leg-cooking.mkv','edited.wav','close.png'):
        if not (OUT/name).exists():
            os.link(OLD/name,OUT/name)
    b.rows=copy.deepcopy(m['timeline'])
    row=next(r for r in b.rows if r['start_frame']==4973)
    assert row['end_frame']==5360
    row.update(video_src=str(LEG),video_start=0,video_end=387,
               label='Roll-4 GPA reveal: clear headings, correct 3.57 total')
    b.boards=m['boards'];b.grafts=m['grafts'];b.total=m['total_frames']
    b.close_start=m['close']['start_frame'];b.make_close('aivscode')
    b.hashes={**m['protected_hashes'],str(PREVIOUS):sha(PREVIOUS)}
    m.update(output=str(b.dest),timeline=b.rows,protected_hashes=b.hashes,
        scope='Approved narrow visual-only GPA repair; candidate only',
        approval='User: Agree, following proposal to use roll 4 with headings and GPA 3.57',
        boundaries=[dict(frame=r['start_frame'],label=r['label']) for r in b.rows[1:]],
        visual_qa_repair={'source':str(R4),'source_frames':[4470,4695],
            'output_frames':[4973,5360],'headers':['Course','Grade','Credits','Points'],
            'calculation':'(16 + 9 + 16 + 9) / (4 + 3 + 4 + 3) = 50 / 14 = 3.57 rounded',
            'label_relocation':'Consistent Fields placed above table so column headings remain visible',
            'motion':'Original row/field reveal retimed to 285 frames, followed by 102-frame hold',
            'audio':'Copy encoded AAC from v14 without re-encoding'})
    m.pop('render_sha256',None)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    print('Rendering original timeline with repaired GPA span',flush=True)
    b.render()
    subprocess.run([b.ff,'-v','error','-i',str(b.dest),'-i',str(PREVIOUS),
        '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(DEST)],check=True)
    m=json.loads((OUT/'edit-manifest.json').read_text())
    m.update(output=str(DEST),render_sha256=sha(DEST),audio_copy_source=str(PREVIOUS))
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    print(DEST,flush=True)


if __name__=='__main__':
    main()
