#!/usr/bin/env python3
"""November 7 lesson cuts and compact cat-board retrofit; review candidate only."""
from pathlib import Path
import argparse
import copy
import json
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, readwav, writewav, sha
from build_tokens_v12 import ROOT, S4, S6, diagram
from build_tokens_v14 import Repaired, EdgeRenderer, previous_frame
from build_tokens_v9 import Renderer

OUT = ROOT / 'video-audit/tokens-lesson-cuts-2026-11-07-v15'
DEST = ROOT / 'Prompts/tokens-v15.mp4'
PARENT = ROOT / 'Prompts/tokens-v14.mp4'
PREV = ROOT / 'video-audit/tokens-repair-2026-10-06-v14'
PCM = ROOT / 'video-audit/tokens-build-2026-10-04-v12/edited.wav'
CUTS = [(410, 474), (560, 1172), (5375, 5492)]
KEEP = [(0, 410), (474, 560), (1172, 5375), (5492, 6857)]
MAP = [f for a, z in KEEP for f in range(a, z)]
TOTAL = len(MAP)
CAT_START, CAT_END = 4761, 5375


def output_frame(f):
    cursor = 0
    for a, z in KEEP:
        if a <= f < z:
            return cursor + f - a
        cursor += z - a
    if f == 6857:
        return TOTAL
    raise ValueError(f)


def prepare():
    old = json.loads((PREV / 'edit-manifest.json').read_text())
    assert sha(PARENT) == old['render_sha256']
    assert all(sha(Path(k)) == v for k, v in old['sources'].items())
    b = Build(ROOT, S4, OUT, DEST)
    b.make_close('tokens')
    specs, renderers = {}, {}
    for key in ['examples', 'send']:
        board = next(x for x in old['boards'] if x['key'] == key)
        asset = ROOT / 'course-assets/tokens' / board['asset']
        assert sha(asset) == old['protected'][str(asset)]
        path, cw, ch, ox, oy = b.compose(asset, key)
        assert [ox, oy] == board['canvas_offset']
        spec = json.loads((PREV / f'leg-{key}.json').read_text())
        spec['image'] = str(path)
        specs[key] = spec
        renderers[key] = Renderer(spec)

    asset = ROOT / 'course-assets/tokens/tokens-cat-token-id.jpg'
    im = cv2.imread(str(asset))
    assert im.shape[:2] == (870, 1808)
    # Exact current JPG on a temporary larger stage for complete-card cameras.
    ox, oy = 396, 315
    canvas = np.full((1500, 2600, 3), im[4, 4], np.uint8)
    canvas[oy:oy + 870, ox:ox + 1808] = im
    path = OUT / 'canvas-cat.png'
    cv2.imwrite(str(path), canvas)
    full = [1300, 750, 1808]
    left = [ox + 466.5, oy + 478, 1288]
    right = [ox + 1344, oy + 478, 1288]
    length = CAT_END - CAT_START
    spec = dict(image=str(path), fps=30, out_w=1280, out_h=720, upscale=2,
                rings=[
                    dict(start=139, end=301, rect=[ox+46, oy+144, 841, 668], color='#0e8f86', pad=0, radius=19),
                    dict(start=301, end=length, rect=[ox+924, oy+144, 840, 668], color='#4f2fc4', pad=0, radius=19)],
                beats=[
                    dict(label='complete unmarked opening', frames=139, **{'from': full, 'to': full}),
                    dict(label='complete human card dive', frames=24, to=left),
                    dict(label='human card explanation', frames=114, to=left),
                    dict(label='return through full view', frames=24, to=full),
                    dict(label='complete AI card dive', frames=24, to=right),
                    dict(label='AI card explanation', frames=length-349, to=right),
                    dict(label='return at end of explanation', frames=24, to=full)])
    assert sum(x['frames'] for x in spec['beats']) == length
    specs['cat'] = spec
    renderers['cat'] = EdgeRenderer(spec)
    for key, spec in specs.items():
        (OUT / f'leg-{key}.json').write_text(json.dumps(spec, indent=2)+'\n')
    for n in [0, 138, 163, 276, 300, 325, length-25, length-1]:
        cv2.imwrite(str(OUT / 'preview' / f'cat-{n:04d}.jpg'), renderers['cat'].at(n)[0])
    # Validate every moving frame, including the active card throughout the dive.
    for n in range(length):
        renderers['cat'].at(n)

    base = readwav(PCM)
    parent_audio = np.r_[base[:6130*1600], base[6432*1600:]]
    audio = np.concatenate([parent_audio[a*1600:z*1600] for a,z in KEEP])
    assert len(audio) == TOTAL*1600
    writewav(OUT/'edited.wav', audio)
    seams = []
    for a,z in CUTS:
        at = sum(max(0, min(a, k2)-k1) for k1,k2 in KEEP)
        gap = audio[at*1600-4800:at*1600+4800]
        db = float(20*np.log10(max(1e-9, np.sqrt(np.mean(gap*gap)))/32768))
        assert db < -60, (a,z,db)
        seams.append(dict(removed_parent_frames=[a,z], removed_parent_seconds=[a/30,z/30], output_frame=at, output_seconds=at/30, join_200ms_rms_dbfs=db))
    protected = {str(p):sha(p) for p in [ROOT/'index.html',ROOT/'lessons/tokens.md',ROOT/'course-assets/tokens/tokens.mp4',*sorted((ROOT/'course-assets/tokens').glob('*.jpg'))]}
    boundaries = {}
    previous = json.loads((PREV/'encoded-check/transitions/transition-guard.json').read_text())
    for row in previous['boundaries']:
        try: boundaries[output_frame(row['frame'])] = row['label']
        except ValueError: pass
    for s,label in zip(seams,['opening-to-AI-bridge','AI-bridge-to-questions','cat-to-Send-without-repeated-takeaway']):
        boundaries[s['output_frame']] = label
    boards = []
    for key, a,z in [('examples',2266,3758), ('cat',CAT_START,CAT_END), ('send',5492,6239)]:
        boards.append(dict(key=key,start_frame=output_frame(a),end_frame=output_frame(z-1)+1,asset=str(ROOT/'course-assets/tokens'/next(x['asset'] for x in old['boards'] if x['key']==key))))
    m = dict(candidate=str(DEST), parent=str(PARENT), parent_sha256=sha(PARENT),
             scope='Authorized lesson changes: remove chat setup/exchange/back-reference, remove repeated cat takeaway, fit current shorter cat board',
             sources=old['sources'], lossless_audio_source=str(PCM), lossless_audio_sha256=sha(PCM),
             frames=TOTAL, fps=30, duration=TOTAL/30, parent_frames=6857,
             keep_parent_frames=KEEP, cuts=seams, boards=boards,
             close_start=output_frame(old['close_start']), boundaries=boundaries,
             protected=protected, extra_pauses=0, speed_unchanged=True,
             cat_geometry=dict(asset_sha256=sha(asset),image_size=[1808,870],canvas_offset=[ox,oy],card_rects=[[46,144,841,668],[924,144,840,668]],density='complete-card zoom, same approved treatment refitted to current image',camera_width=1288,ring_stroke_px=4),
             bridge='Retains existing spoken sentences: The exact same rule applies to AI. How did your words become numbers that AI could work with, and how did AI’s response turn back into words you could read?',
             listening='Not directly auditioned. PCM and ASR checks do not certify cadence or pronunciation.')
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    parent_boards = copy.deepcopy(old['boards'])
    for row in parent_boards:
        row['start_frame'] = row['parent_start_frame']
        row['end_frame'] = row['parent_end_frame']
    return b, renderers, parent_boards, m


class Revised(Repaired):
    def at_parent(self, f):
        if 474 <= f < 560:
            # The surviving AI bridge uses the existing question/AI/reply diagram.
            return diagram('questions', 0)
        if CAT_START <= f < CAT_END:
            return self.renderers['cat'].at(f-CAT_START)[0]
        return super().at(previous_frame(f))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prepare-only',action='store_true')
    args=ap.parse_args()
    assert not DEST.exists(), 'Never overwrite a review candidate'
    b,rd,boards,m=prepare()
    if args.prepare_only:
        print(json.dumps({k:m[k] for k in ['frames','duration','cuts','boards']},indent=2))
        return
    v=Revised(b,rd,boards)
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    p=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for n,f in enumerate(MAP):
        p.stdin.write(v.at_parent(f).tobytes())
        if n%900==899: print('Rendered',n+1,'/',TOTAL,flush=True)
    p.stdin.close()
    assert p.wait()==0
    v.close()
    assert all(sha(Path(p))==h for p,h in m['protected'].items())
    m['render_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(DEST,flush=True)


if __name__=='__main__':
    main()
