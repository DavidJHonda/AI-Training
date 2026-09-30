#!/usr/bin/env python3
"""Approved repair of the public-identical finished v8; review candidate only.

No raw roll survives. Copy untouched picture spans from v8, overlay three
approved supporting images, restore the complete final-board takeaway, and
make one narration deletion. Decode/encode once; never fade audio at visual cuts.
"""
from pathlib import Path
import json
import subprocess

import cv2
import numpy as np
import imageio_ffmpeg
from editspec_build import Build, readwav, writewav, sha, banner_rect
import ken_burns_path as kb

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'course-assets/pace-of-change/pace-of-change.mp4'
DEST = ROOT / 'Prompts/pace-of-change-v9.mp4'
OUT = ROOT / 'video-audit/pace-of-change-build-2026-09-30-v9'
ASSETS = ROOT / 'scripts/video/assets/pace-of-change-cutaways-2026-09-30'
EXPECTED = '4cce8f2cb230d865ad54e6ff165a603fc779c6180514bd83bb8965cc8f6680d7'
FPS, SR, SPF, TOTAL = 30, 48000, 1600, 8757
CUT_A, CUT_B = 3291, 3816  # 109.700 / 127.200, inside measured sentence silences
REMOVED = CUT_B - CUT_A
INSERTS = [
    dict(key='research', start=6060, end=6288, label='Human-directed research workflow'),
    dict(key='contrast', start=6930, end=7203, label='Human direction versus hypothetical autonomous loop'),
    dict(key='asi', start=7902, end=8145, label='Hypothetical breadth beyond the best humans'),
]
TAIL_A, TAIL_B, BANNER = 8145, 8283, 8189
FF = imageio_ffmpeg.get_ffmpeg_exe()


def mapped(frame):
    return frame if frame < CUT_A else max(CUT_A, frame - REMOVED)


def make_tail():
    b = Build(ROOT, SRC, OUT, DEST)
    asset = SRC.parent / 'pace-of-change-how-far-can-ai-go.jpg'
    canvas, cw, ch, ox, oy = b.compose(asset, 'far-tail')
    full = cv2.resize(cv2.imread(str(canvas)), (1280, 720), interpolation=cv2.INTER_AREA)
    scale = 1280 / cw
    views = {}
    for key, rect, color in [('asi', [816, 127, 1560, 759], '#c41f28'),
                             ('banner', banner_rect(cv2.imread(str(asset))), '#6e51ff')]:
        x0,y0,x1,y1 = rect
        image = full.copy()
        thickness = kb.ring_px(720)
        kb.draw_ring(image, (x0+ox)*scale-thickness/2, (y0+oy)*scale-thickness/2,
                     (x1+ox)*scale+thickness/2, (y1+oy)*scale+thickness/2,
                     kb.hex_bgr(color), 18*scale+thickness/2, thickness)
        views[key] = image
    return views, dict(asset=str(asset), canvas=str(canvas), full_view=True,
                       full_view_returns_source_frame=TAIL_A,
                       banner_onset_source_frame=BANNER,
                       ring_pixels=4, canonical_banner=banner_rect(cv2.imread(str(asset))))


def main():
    cv2.setNumThreads(2)
    assert sha(SRC) == EXPECTED, 'Source changed; do not use old timings'
    assert not DEST.exists(), 'Never overwrite a review candidate'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'preview').mkdir(exist_ok=True)
    protected = {str(p):sha(p) for p in [SRC, *SRC.parent.glob('*.jpg')]}
    if not (OUT/'source.wav').exists():
        subprocess.run([FF,'-v','error','-i',str(SRC),'-vn','-ar',str(SR),'-ac','1',
                        '-c:a','pcm_s16le',str(OUT/'source.wav')],check=True)
    source = readwav(OUT/'source.wav')[:TOTAL*SPF]
    assert len(source) == TOTAL*SPF
    edited = np.concatenate([source[:CUT_A*SPF], source[CUT_B*SPF:]])
    seam = CUT_A*SPF
    # Four milliseconds of interpolation, wholly inside the quiet join. There
    # are no changes at image boundaries, no gain changes, and no added pauses.
    edited[seam-96:seam+96] = np.linspace(edited[seam-96], edited[seam+95], 192)
    writewav(OUT/'edited.wav', edited)
    writewav(OUT/'narration-join.wav', edited[(CUT_A-120)*SPF:(CUT_A+210)*SPF])
    pcm_equal = np.array_equal(source[:CUT_A*SPF-96],edited[:CUT_A*SPF-96]) and np.array_equal(source[CUT_B*SPF+96:],edited[CUT_A*SPF+96:])
    assert pcm_equal
    images = {}
    for row in INSERTS:
        p=ASSETS/(row['key']+'.png')
        im=cv2.imread(str(p));assert im is not None,p
        images[row['key']] = cv2.resize(im,(1280,720),interpolation=cv2.INTER_AREA)
        row.update(asset=str(p),asset_sha256=sha(p))
    tail, tailmeta = make_tail()
    # Read every original frame sequentially, including the deleted interval.
    # Finished source is already corner-cleaned; do not inpaint it again.
    reader=cv2.VideoCapture(str(SRC))
    assert reader.get(cv2.CAP_PROP_FPS)==FPS
    temp=OUT/'rendering.mp4';assert not temp.exists()
    command=[FF,'-v','warning','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720',
             '-r',str(FPS),'-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v',
             '-map','1:a','-c:v','libx264','-preset','fast','-crf','16','-threads','2',
             '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)]
    (OUT/'command.json').write_text(json.dumps(command,indent=2)+'\n')
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    wanted={CUT_A-1,CUT_B,TAIL_A, BANNER-1,BANNER,TAIL_B-1,TOTAL-1}
    for r in INSERTS:wanted.update([r['start']-1,r['start'],r['start']+30,r['end']-1,r['end']])
    written=0
    for f in range(TOTAL):
        ok,im=reader.read();assert ok,f
        if CUT_A<=f<CUT_B:continue
        row=next((r for r in INSERTS if r['start']<=f<r['end']),None)
        if row:im=images[row['key']]
        elif TAIL_A<=f<TAIL_B:im=tail['banner' if f>=BANNER else 'asi']
        if f in wanted:cv2.imwrite(str(OUT/'preview'/f'{mapped(f):06d}.jpg'),im)
        proc.stdin.write(im.tobytes());written+=1
        if f%900==0:print(f'Render source {f/FPS:.0f}s / {TOTAL/FPS:.1f}s',flush=True)
    assert not reader.read()[0]
    reader.release();proc.stdin.close()
    assert proc.wait()==0 and written==TOTAL-REMOVED
    assert all(sha(Path(p))==h for p,h in protected.items())
    temp.rename(DEST)
    prior=json.loads((ROOT/'video-audit/pace-of-change-rerolls-2026-09-24/build-v8/edit-manifest.json').read_text())
    boundaries={mapped(r['start_frame']):r['label'] for r in prior['timeline'][1:]
                if not CUT_A<=r['start_frame']<CUT_B and not any(i['start']<r['start_frame']<i['end'] for i in INSERTS)}
    boundaries[CUT_A]='Remove model replacement claim; resume limitation sentence'
    for r in INSERTS:
        boundaries[mapped(r['start'])]=r['label']
        boundaries[mapped(r['end'])]='Return after '+r['key']
    boundaries[mapped(TAIL_A)]='Full final board restored after ASI insert'
    boundaries[mapped(TAIL_B)]='Retained forked uncertainty graphic'
    breaks=sorted({0,TOTAL,CUT_A,CUT_B,TAIL_A,TAIL_B,*[r[k] for r in INSERTS for k in ['start','end']]})
    timeline=[]
    for a,z in zip(breaks,breaks[1:]):
        if CUT_A<=a<CUT_B:continue
        row=next((r for r in INSERTS if r['start']<=a<r['end']),None)
        kind=row['key'] if row else ('far-tail' if TAIL_A<=a<TAIL_B else 'source')
        timeline.append(dict(source_start=a,source_end=z,start_frame=mapped(a),end_frame=mapped(z),visual=kind))
    m=dict(candidate=str(DEST),candidate_sha256=sha(DEST),source=str(SRC),source_sha256=EXPECTED,
           source_limitation='Only finished v8 survives locally; untouched scenes undergo one new encode.',
           approval='User: Agree. Build it please. (2026-09-30), approving the linked evaluation plan.',
           scope='Review candidate; no shipping, commit, or deployment.',fps=FPS,total_frames=written,duration=written/FPS,
           cut=dict(source_start_frame=CUT_A,source_end_frame=CUT_B,removed_seconds=REMOVED/FPS,
                    silence_before=[109.467229,109.982146],silence_after=[126.989417,127.411896],
                    resulting_gap_seconds=(CUT_A/FPS-109.467229)+(127.411896-CUT_B/FPS)),
           audio=dict(sample_rate=SR,expected_samples=len(edited),unchanged_outside_seam=bool(pcm_equal),
                      seam_interpolation_ms=4,audio_join_output_frames=[CUT_A],added_pauses=[],listening_completed=False),
           timeline=timeline,inserts=INSERTS,board_tail=tailmeta,
           boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],
           protected_hashes=protected,protected_files_unchanged=True)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print('COMPLETE',DEST,written/FPS,sha(DEST),flush=True)


if __name__=='__main__':main()
