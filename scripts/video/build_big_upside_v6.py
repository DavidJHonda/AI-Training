#!/usr/bin/env python3
"""Approved visual-only Big Upside repair. Preserve the source AAC and timeline."""
import argparse
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, sha
from build_embeddings_v7 import Renderer

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'course-assets/big-upside/big-upside.mp4'
EXPECTED = 'a7d56ee3a5a5f4e4968c125719077130c7317f31872fc1c52d3ce22ecffb4c06'
DEST = ROOT / 'Prompts/big-upside-v6.mp4'
OUT = ROOT / 'video-audit/big-upside-cutaways-2026-09-30-v6'
ASSETS = ROOT / 'scripts/video/assets/big-upside-cutaways-2026-09-30'
OLD = ROOT / 'video-audit/big-upside-v5-2026-09-24/build'
FPS, TOTAL = 30, 7719
BOARDS = {'health': (3049, 4706), 'everyday': (4706, 6349)}
CUTAWAYS = [
    dict(name='scan-review', start=3690, end=3930, purpose='A doctor reviews an AI-flagged possible finding; no diagnosis claim.'),
    dict(name='antibiotic-lab', start=4350, end=4500, purpose='Candidate molecules undergo laboratory testing, not clinical treatment.'),
    dict(name='menu-reading', start=5130, end=5310, purpose='Phone camera reads a menu for an independent student.'),
    dict(name='weed-spraying', start=5910, end=6060, purpose='Camera-guided nozzle targets a weed while adjacent crops remain unsprayed.'),
]


def changed(n):
    return 3049 <= n < 6349


def setup():
    cv2.setNumThreads(1)
    OUT.mkdir(exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    assert sha(SRC) == EXPECTED, 'Source changed; re-evaluate before building'
    old = json.loads((OLD / 'edit-manifest.json').read_text())
    helper = Build(ROOT, SRC, OUT, DEST)
    renderers, specs = {}, {}
    for key, (start, end) in BOARDS.items():
        meta = old['boards'][key]
        asset = ROOT / meta['asset']
        assert sha(asset) == meta['sha256'], 'Board geometry is tied to this exact asset'
        canvas, cw, ch, ox, oy = helper.compose(asset, key)
        assert [ox, oy] == meta['canvas_offset']
        spec = json.loads((OLD / f'leg-{key}.json').read_text())
        spec['image'] = str(canvas)
        # Preserve the original slow camera path; hold its final state over the
        # removed 51-frame milestones insert, rather than restart the board.
        specs[key] = spec
        renderers[key] = Renderer(spec)
        (OUT / f'leg-{key}.json').write_text(json.dumps(spec, indent=2) + '\n')
    images = {}
    for c in CUTAWAYS:
        path = ASSETS / (c['name'] + '.png')
        im = cv2.imread(str(path))
        assert im is not None, path
        images[c['name']] = im
    return old, renderers, specs, images


def scene(im, n, c):
    u = (n-c['start']) / (c['end']-c['start']-1)
    u = u*u*(3-2*u)
    h, w = im.shape[:2]
    width = min(w, h*16/9) / (1 + .025*u)
    height = width*9/16
    matrix = np.float32([[width/1280, 0, (w-width)/2], [0, height/720, (h-height)/2]])
    return cv2.warpAffine(im, matrix, (1280,720), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP)


def replacement(n, renderers, specs, images):
    for c in CUTAWAYS:
        if c['start'] <= n < c['end']:
            return scene(images[c['name']], n, c)
    for key, (start, end) in BOARDS.items():
        if start <= n < end:
            count = sum(b['frames'] for b in specs[key]['beats'])
            return renderers[key].at(min(n-start, count-1))[0]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    old, renderers, specs, images = setup()
    protected = {str(p): sha(p) for p in [SRC, ROOT/'lessons/big-upside.md',
                 *sorted((ROOT/'course-assets/big-upside').glob('*.jpg')),
                 *sorted(ASSETS.glob('*.png'))]}
    bounds = {x['frame']:x['label'] for x in old['boundaries'] if x['frame'] != 6298}
    for c in CUTAWAYS:
        bounds[c['start']] = c['name']+'-in'
        bounds[c['end']] = c['name']+'-out'
    wanted = {3049, 4706, 6297, 6298, 6348, 6349, TOTAL-1}
    for key, (start, end) in BOARDS.items():
        wanted |= {start+r['start']+15 for r in specs[key]['rings']}
    for c in CUTAWAYS:
        wanted |= {c['start'], c['start']+15, (c['start']+c['end'])//2, c['end']-1, c['end']}
    for n in sorted(wanted):
        im = replacement(n, renderers, specs, images)
        if im is not None:
            cv2.imwrite(str(OUT/'preview'/f'{n:05d}.png'), im)
    manifest = dict(source=str(SRC), source_sha256=EXPECTED, candidate=str(DEST),
        scope='User-approved visual repair: four example cutaways and replacement of unfinished milestones insert. Build only.',
        source_limitation='Raw rolls no longer exist. One video encode from verified shipped v5; AAC copied unchanged.',
        fps=FPS, frames=TOTAL, duration=TOTAL/FPS, protected=protected,
        cutaways=CUTAWAYS, board_spans=BOARDS, changed_spans=[[3049,6349]],
        unfinished_insert_replacement=dict(start=6298,end=6349,visual='Hold canonical everyday board final banner state'),
        rings='Current fixed 4px at 720p on the two rebuilt boards. Unaffected boards retain shipped treatment.',
        boundaries=[dict(frame=f,label=label) for f,label in sorted(bounds.items())],
        audio='Copy original AAC; no cuts, grafts, pauses, gain changes or new audio joins.',
        generation_prompts=str(ASSETS/'PROMPTS.txt'),listening_performed=False)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if args.prepare_only:
        print('Prepared', OUT/'preview'); return
    assert not DEST.exists(), 'Never overwrite an existing review candidate'
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    encoder = subprocess.Popen([ff,'-hide_banner','-loglevel','error','-threads','1',
        '-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
        '-threads','1','-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264',
        '-threads','2','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy',
        '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE,stderr=(OUT/'encode.log').open('w'))
    decoder = subprocess.Popen([ff,'-v','error','-threads','1','-i',str(SRC),'-map','0:v:0',
        '-threads','1','-f','rawvideo','-pix_fmt','bgr24','pipe:1'],stdout=subprocess.PIPE)
    count=0
    try:
        while True:
            raw=decoder.stdout.read(1280*720*3)
            if not raw: break
            assert len(raw)==1280*720*3
            im=replacement(count,renderers,specs,images)
            encoder.stdin.write(im.tobytes() if im is not None else raw)
            count+=1
            if count%900==0: print(f'Rendered {count}/{TOTAL}',flush=True)
        encoder.stdin.close()
        assert decoder.wait()==0 and encoder.wait()==0
    finally:
        if decoder.poll() is None: decoder.terminate()
        if encoder.poll() is None: encoder.terminate()
    assert count==TOTAL
    assert all(sha(Path(p))==h for p,h in protected.items())
    manifest['candidate_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST,flush=True)


if __name__=='__main__':
    main()
