#!/usr/bin/env python3
"""Approved title, prompt highlight and two repetition cuts. Review only."""
from pathlib import Path
import argparse
import json
import subprocess

import cv2
import numpy as np
import imageio_ffmpeg

from editspec_build import Build, Reader, sha, readwav, writewav
from build_embeddings_v7 import Renderer
from ken_burns_path import smoothstep

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/how-an-llm-works-v15.mp4'
EXPECTED = '9fa099494fcffd819b1ac159e4ca6eac499d2980ba0a1c457c203770bf64c8a6'
PREVIOUS = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-28-v15'
OLD = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-17-v13'
OUT = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-29-v16'
DEST = ROOT / 'Prompts/how-an-llm-works-v16.mp4'
CUTS = [(4992, 5151), (6610, 6790)]
KEEP = [(0, 4992), (5151, 6610), (6790, 9114)]
FRAMES = [f for a, b in KEEP for f in range(a, b)]
SPF = 1600


def setup():
    assert sha(SOURCE) == EXPECTED
    previous = json.loads((PREVIOUS / 'edit-manifest.json').read_text())
    old = json.loads((OLD / 'edit-manifest.json').read_text())
    mapped = previous['board_mapping']
    build = Build(ROOT, SOURCE, OUT, DEST)
    build.tall_margin = False
    renderers, specs = {}, {}
    for key in ['patterns', 'odds-intro', 'odds']:
        meta = old['boards'][key]
        canvas, _, _, ox, oy = build.compose(ROOT / meta['asset'], key)
        assert [ox, oy] == meta['canvas_offset']
        spec = json.loads((PREVIOUS / f'leg-{key}.json').read_text())
        spec['image'] = str(canvas)
        if key == 'odds-intro':
            spec['rings'] = [dict(start=50, end=119, rect=[130,169,662,165],
                                  color='#4f2fc4', pad=0, radius=14)]
        specs[key] = spec
        renderers[key] = Renderer(spec)
        (OUT / f'leg-{key}.json').write_text(json.dumps(spec, indent=2) + '\n')

    def visual(out, source):
        item = mapped[source]
        if not item or item[0] not in renderers:
            return None
        key, local = item
        r = renderers[key]
        if key != 'odds':
            return r.at(local)
        camera = r.cameras[local]
        active = tuple(i for i, ring in enumerate(r.rings) if ring[0] <= local < ring[1])
        # Preserve two complete seconds of full-board context across the cut.
        full = tuple(specs[key]['beats'][0]['from'])
        left = tuple(specs[key]['beats'][1]['to'])
        if out < 5031:
            camera = full
        elif out < 5055:
            q = smoothstep((out - 5031) / 23)
            camera = tuple(a + (b-a)*q for a,b in zip(full,left))
        if out < 5000:
            active = ()
        elif out < 5067:
            active = (0,)
        # Resume directly on the paired comparison, avoiding a four-frame flash.
        if 6790 <= source < 6794:
            active = (7,8)
        return r.render(camera, active)

    protected = {str(p): sha(p) for p in [SOURCE,
        ROOT/'course-assets/whats-an-llm/whats-an-llm.mp4',
        ROOT/'lessons/whats-an-llm.md',
        *sorted((ROOT/'course-assets/whats-an-llm').glob('*.jpg'))]}
    inverse = {f:i for i,f in enumerate(FRAMES)}
    boundaries = sorted({inverse[b] for b in previous['boundaries'] if b in inverse}
                        | {4992,6451,4271,4340,5000,5031,5055,5067})
    previews = []
    for out in [3117,3270,3440,4221,4270,4271,4300,4339,4340,
                4971,4991,4992,5000,5030,5043,5054,5067,6450,6451,6500,6600]:
        item = visual(out, FRAMES[out])
        if item:
            im, _, geo = item
            path = OUT/'preview'/f'{out:05d}.jpg'
            cv2.imwrite(str(path), im)
            previews.append(dict(frame=out, source_frame=FRAMES[out], path=str(path), geometry=geo))
    manifest = dict(source=str(SOURCE), source_sha256=EXPECTED, candidate=str(DEST),
        frames=len(FRAMES), fps=30, duration=len(FRAMES)/30, source_frame_mapping=FRAMES,
        board_mapping=[mapped[f] for f in FRAMES], cuts_source_frames=CUTS,
        cuts_source_seconds=[[a/30,b/30] for a,b in CUTS], keep_source_frames=KEEP,
        audio_cuts_samples=[[a*SPF,b*SPF] for a,b in CUTS],
        audio='Frame-aligned sentence cuts in measured silence; 5ms matched-room-tone edge blends. No added pauses.',
        changes=['Patterns AI Learns board title', 'First spoken prompt highlighted at source 142.367–144.667 s',
                 'Repeated left prompt introduction removed', 'Redundant banana restatement removed; 41% to 2% comparison retained'],
        camera_override='Probability detail full for 60 output frames, then 24-frame dive; first whole-card ring at f5000, table ring at f5067.',
        preserved_exception=previous['preserved_exception'],
        unresolved_audio='Previously reported glitch around 44.5 s remains unchanged; no speculative repair.',
        approval='User: agree. Build it please. Review candidate only; no publication.',
        boundaries=boundaries, previews=previews, protected=protected)
    return visual, manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prepare-only', action='store_true')
    args = ap.parse_args()
    assert not DEST.exists(), 'Never overwrite a review candidate'
    visual, manifest = setup()
    mp = OUT/'edit-manifest.json'
    mp.write_text(json.dumps(manifest, indent=2)+'\n')
    if args.prepare_only:
        return
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    wav = OUT/'source.wav'
    subprocess.run([ff,'-y','-v','error','-i',str(SOURCE),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(wav)], check=True)
    source = readwav(wav)
    assert len(source) >= 9114*SPF
    parts = [source[a*SPF:b*SPF].copy() for a,b in KEEP]
    # Blend into actual low-level room tone without changing timing or length.
    fade = 240
    tone = source[round(220.4*48000):round(220.4*48000)+2*fade]
    for i in range(len(parts)-1):
        t = np.linspace(0,1,fade)
        parts[i][-fade:] = parts[i][-fade:]*(1-t)+tone[:fade]*t
        parts[i+1][:fade] = tone[fade:]*(1-t)+parts[i+1][:fade]*t
    audio = np.concatenate(parts)
    assert len(audio) == len(FRAMES)*SPF == 14040000
    writewav(OUT/'edited.wav', audio)
    p = subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24',
        '-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),
        '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16',
        '-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    rd = Reader(SOURCE)
    for out, sf in enumerate(FRAMES):
        result = visual(out,sf)
        im = result[0] if result else rd.at(sf)
        p.stdin.write(im.tobytes())
        if out % 1000 == 999:
            print(f'Rendered {out+1}/{len(FRAMES)}',flush=True)
    p.stdin.close()
    assert p.wait() == 0
    rd.c.release()
    assert all(sha(Path(path)) == h for path,h in manifest['protected'].items())
    manifest['candidate_sha256'] = sha(DEST)
    mp.write_text(json.dumps(manifest,indent=2)+'\n')
    print(DEST,flush=True)


if __name__ == '__main__':
    main()
